#!/usr/bin/env python3
"""Scan a skill zip before it can be shipped.

The filename deny list comes from HITL-LUNCH.md ("Do not put in the skill zip")
plus the internal push note, key files, databases, and binaries.
Corpus-repo mentions that already exist in the four packs are warnings.
The same mention in any other zip member is a failure.
"""

from __future__ import annotations

import re
import zipfile
import zlib
from dataclasses import dataclass, field
from pathlib import Path

MAX_FILES = 500
MAX_UNCOMPRESSED = 25 * 1024 * 1024

# Path fragment shared by the private corpus trees. Full repo names are
# assembled below so this file does not need a single contiguous copy.
_CORPUS_TAIL = "-ip-law-" + "ground-truth"
CORPUS_RE = re.compile(r"(?i)\b(?:us|eu)" + re.escape(_CORPUS_TAIL) + r"\b")

_COMMON_LEGACY = frozenset(
    {
        "SKILL.md",
        "references/classification-matrix.md",
        "references/evals.md",
        "references/output-language-hygiene.md",
        "references/public-corpus-rag.md",
        "references/sidecar-retrieve.stub.json",
        "references/v05-lite-prior-art-pointers.md",
    }
)

# Pack-relative paths that already mention a private corpus repo.
# Do not add paths for files created by this tooling.
LEGACY_CORPUS_PATHS = {
    "chatgpt-skill": _COMMON_LEGACY | {"agents/openai.yaml"},
    "claude-skill": _COMMON_LEGACY,
    "grok-skill": _COMMON_LEGACY,
    "cursor-skill": _COMMON_LEGACY | {"README.md"},
}

_DB_EXT = (".db", ".sqlite", ".sqlite3", ".mdb")
_BIN_EXT = (
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".pyc",
    ".pyo",
    ".class",
    ".wasm",
    ".o",
    ".a",
)
_EXACT_BASENAMES = frozenset(
    {
        ".env",
        "changelog.md",
        "launch.md",
        "exec-summary.md",
        "hitl-lunch.md",
        "push_to_github.txt",
        "plugin.json",
    }
)

# An address is allowed only when it is a noreply role mailbox.
# The local part is compared before any plus-tag. One noreply domain
# stays on the list because its local part is an id, not the role name.
_NOREPLY_LOCALS = frozenset({"noreply", "no-reply"})
_NOREPLY_DOMAINS = frozenset({"users.noreply.github.com"})

_EMAIL_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9._%+\-])([A-Za-z0-9._%+\-]+)@((?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,})"
)


def _link_pattern(labels: tuple[str, ...], path: str = "") -> re.Pattern[str]:
    host = r"\.".join(re.escape(label) for label in labels)
    if path:
        # A share path must not match a longer word such as "shared".
        tail = re.escape(path) + ("" if path.endswith("/") else r"(?![A-Za-z0-9])")
    else:
        tail = r"(?![A-Za-z0-9.-])"
    return re.compile(
        r"(?i)(?<![A-Za-z0-9@./-])(?:https?://)?(?:www\.)?" + host + tail
    )


_CHAT_SHARE = (
    _link_pattern(("grok", "com"), "/c/"),
    _link_pattern(("chatgpt", "com"), "/share"),
    _link_pattern(("claude", "ai"), "/share"),
)
_CLOUD_DRIVE = (
    _link_pattern(("drive", "google", "com")),
    _link_pattern(("docs", "google", "com")),
)
_PATH_RE = re.compile(r"/Users/|/home/|C:\\Users|C:/Users|handoffs/|/workspace/")


def _secret_re() -> re.Pattern[str]:
    parts = (
        "sk" + r"-[A-Za-z0-9]{20,}",
        "ghp" + r"_[A-Za-z0-9]{30,}",
        "github_pat_" + r"\w{20,}",
        "AKIA" + r"[0-9A-Z]{16}",
        "xox" + r"[baprs]-[A-Za-z0-9-]{10,}",
        "AIza" + r"[0-9A-Za-z_\-]{30,}",
        r"-----BEGIN [A-Z ]{0,40}PRIVATE KEY-----",
        "whsec" + r"_[A-Za-z0-9]{8,}",
        "Bearer " + r"[A-Za-z0-9._\-]{20,}",
    )
    return re.compile("|".join(parts))


SECRET_RE = _secret_re()


@dataclass
class ScanResult:
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    file_count: int = 0
    uncompressed: int = 0
    names: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures

    @property
    def warning_mentions(self) -> int:
        total = 0
        for line in self.warnings:
            head, _, _rest = line.partition(" ")
            if head.isdigit():
                total += int(head)
        return total


def legacy_paths_for(pack: str | None) -> set[str]:
    if pack is None:
        return set()
    return set(LEGACY_CORPUS_PATHS.get(pack, ()))


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = info.external_attr >> 16
    return (mode & 0o170000) == 0o120000


def _has_parent_segment(arcname: str) -> bool:
    return any(part == ".." for part in arcname.replace("\\", "/").split("/"))


def _member_name_failures(arcname: str) -> list[str]:
    failures: list[str] = []
    if "\\" in arcname:
        failures.append(f"backslash: {arcname}")
    if _has_parent_segment(arcname):
        failures.append(f"parent-segment: {arcname}")
    if arcname.startswith("/") or arcname.startswith("\\"):
        failures.append(f"absolute-path: {arcname}")
    elif len(arcname) >= 3 and arcname[0].isalpha() and arcname[1] == ":" and arcname[2] in "/\\":
        failures.append(f"absolute-path: {arcname}")
    normalized = arcname.replace("\\", "/")
    if "/workspace/" in normalized:
        failures.append(f"workspace-path: {arcname}")
    return failures


def forbidden_name(arcname: str) -> str | None:
    name = arcname.replace("\\", "/").strip("/")
    if not name:
        return None
    lower = name.lower()
    base = lower.rsplit("/", 1)[-1]
    if base in _EXACT_BASENAMES or base.startswith(".env."):
        return "forbidden-name"
    if base.startswith("id_rsa"):
        return "forbidden-name"
    if base.endswith(".pem"):
        return "forbidden-name"
    if "ground-truth" in lower:
        return "forbidden-name"
    if lower == ".git" or lower.startswith(".git/") or "/.git/" in f"/{lower}":
        return "forbidden-name"
    for prefix in ("openai-gpt-package", "grok-bot-share"):
        if lower == prefix or lower.startswith(prefix + "/"):
            return "forbidden-name"
    if base.endswith(_DB_EXT):
        return "database"
    if base.endswith(_BIN_EXT):
        return "binary"
    return None


def _layout_errors(names: list[str]) -> list[str]:
    errors: list[str] = []
    skills = [n for n in names if n == "SKILL.md" or n.endswith("/SKILL.md")]
    if skills != ["SKILL.md"]:
        errors.append(
            "layout: zip needs exactly one SKILL.md and it must sit at the zip root"
        )
    plugins = [n for n in names if n.rsplit("/", 1)[-1].lower() == "plugin.json"]
    if plugins:
        errors.append("layout: plugin.json must not be inside a skills zip")
    return errors


def _disallowed_emails(text: str) -> int:
    found = 0
    for match in _EMAIL_RE.finditer(text):
        local = match.group(1).lower().split("+", 1)[0]
        domain = match.group(2).lower().rstrip(".")
        if local in _NOREPLY_LOCALS or domain in _NOREPLY_DOMAINS:
            continue
        found += 1
    return found


def _pattern_hits(text: str, patterns: tuple[re.Pattern[str], ...]) -> int:
    return sum(len(pattern.findall(text)) for pattern in patterns)


def _extra_pattern_numbers(text: str, patterns: list[re.Pattern[str]]) -> list[int]:
    if not patterns:
        return []
    lines = text.splitlines() or [text]
    hits: list[int] = []
    for index, pattern in enumerate(patterns, 1):
        if any(pattern.search(line) for line in lines):
            hits.append(index)
    return hits


def scan_zip(
    path: Path,
    *,
    pack: str | None = None,
    legacy_paths: set[str] | None = None,
    max_files: int = MAX_FILES,
    max_uncompressed: int = MAX_UNCOMPRESSED,
    extra_patterns: list[re.Pattern[str]] | None = None,
) -> ScanResult:
    result = ScanResult()
    legacy = set(legacy_paths) if legacy_paths is not None else legacy_paths_for(pack)
    try:
        archive = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError):
        result.failures.append("unreadable-zip")
        return result
    with archive as zf:
        infos = list(zf.infolist())
        counts: dict[str, int] = {}
        for info in infos:
            counts[info.filename] = counts.get(info.filename, 0) + 1
        for raw_name in sorted(counts):
            result.failures.extend(_member_name_failures(raw_name))
            if counts[raw_name] > 1:
                result.failures.append(f"duplicate-name: {raw_name} ({counts[raw_name]})")
        folded: dict[str, list[str]] = {}
        for raw_name in counts:
            key = raw_name.replace("\\", "/").casefold()
            folded.setdefault(key, []).append(raw_name)
        for names in folded.values():
            distinct = sorted(set(names))
            if len(distinct) > 1:
                result.failures.append("case-duplicate: " + ", ".join(distinct))
        files = []
        for info in infos:
            name = info.filename.replace("\\", "/")
            if name.endswith("/"):
                why = forbidden_name(name)
                if why:
                    result.failures.append(f"{why}: {name}")
                continue
            files.append(info)
        result.file_count = len(files)
        result.uncompressed = sum(info.file_size for info in files)
        result.names = sorted(info.filename.replace("\\", "/") for info in files)
        if result.file_count > max_files:
            result.failures.append(
                f"size: {result.file_count} files (limit {max_files})"
            )
        if result.uncompressed > max_uncompressed:
            result.failures.append(
                f"size: {result.uncompressed} uncompressed bytes "
                f"(limit {max_uncompressed})"
            )
        result.failures.extend(_layout_errors(result.names))
        if result.uncompressed > max_uncompressed:
            return result
        for info in files:
            name = info.filename.replace("\\", "/")
            why = forbidden_name(name)
            if why:
                result.failures.append(f"{why}: {name}")
            if info.flag_bits & 0x1:
                result.failures.append(f"encrypted: {info.filename}")
                continue
            if _is_symlink(info):
                result.failures.append(f"symlink: {info.filename}")
                continue
            try:
                data = zf.read(info)
            except zlib.error:
                result.failures.append(f"unreadable-member: {info.filename}")
                continue
            except Exception:
                result.failures.append(f"unreadable-member: {info.filename}")
                continue
            if b"\x00" in data:
                result.failures.append(f"binary: {name}")
                continue
            text = data.decode("utf-8", "replace")
            if SECRET_RE.search(text):
                result.failures.append(f"secret-token: {name}")
            paths = _PATH_RE.findall(text)
            if paths:
                result.failures.append(f"local-path: {name} ({len(paths)})")
            emails = _disallowed_emails(text)
            if emails:
                result.failures.append(f"email: {name} ({emails})")
            shares = _pattern_hits(text, _CHAT_SHARE)
            if shares:
                result.failures.append(f"chat-share: {name} ({shares})")
            drives = _pattern_hits(text, _CLOUD_DRIVE)
            if drives:
                result.failures.append(f"cloud-drive: {name} ({drives})")
            for number in _extra_pattern_numbers(text, list(extra_patterns or [])):
                result.failures.append(f"extra-pattern #{number}: {name}")
            corpus_hits = CORPUS_RE.findall(text)
            if not corpus_hits:
                continue
            if name in legacy:
                result.warnings.append(f"{len(corpus_hits)} corpus legacy: {name}")
            else:
                result.failures.append(f"corpus-ref: {name} ({len(corpus_hits)})")
    return result


def format_report(result: ScanResult) -> str:
    lines = [
        f"files {result.file_count}",
        f"uncompressed {result.uncompressed}",
    ]
    for failure in result.failures:
        lines.append(f"FAIL {failure}")
    for warning in result.warnings:
        lines.append(f"WARNING {warning}")
    if result.warnings:
        lines.append(f"WARNING corpus legacy total: {result.warning_mentions}")
    if result.ok:
        lines.append("zip scan OK")
    else:
        lines.append("zip scan FAILED")
    return "\n".join(lines)
