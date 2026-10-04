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

# Pack-relative paths that already mention a private corpus repo on v0.5.47-free.
# Do not add paths for files created after that tree.
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

PUBLIC_MAILBOX_DOMAINS = frozenset(
    {
        "gmail.com",
        "googlemail.com",
        "outlook.com",
        "hotmail.com",
        "live.com",
        "yahoo.com",
        "yahoo.co.uk",
        "icloud.com",
        "me.com",
        "proton.me",
        "protonmail.com",
        "pm.me",
        "aol.com",
        "gmx.com",
        "gmx.de",
        "users.noreply.github.com",
    }
)

_EMAIL_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]+@((?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,})"
)
_PATH_RE = re.compile(r"/Users/|/home/|C:\\Users|C:/Users|handoffs/")


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


def _company_emails(text: str) -> int:
    found = 0
    for match in _EMAIL_RE.finditer(text):
        domain = match.group(1).lower().rstrip(".")
        if domain not in PUBLIC_MAILBOX_DOMAINS:
            found += 1
    return found


def scan_zip(
    path: Path,
    *,
    pack: str | None = None,
    legacy_paths: set[str] | None = None,
    max_files: int = MAX_FILES,
    max_uncompressed: int = MAX_UNCOMPRESSED,
) -> ScanResult:
    result = ScanResult()
    legacy = set(legacy_paths) if legacy_paths is not None else legacy_paths_for(pack)
    with zipfile.ZipFile(path) as zf:
        infos = list(zf.infolist())
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
            data = zf.read(info)
            if b"\x00" in data:
                result.failures.append(f"binary: {name}")
                continue
            text = data.decode("utf-8", "replace")
            if SECRET_RE.search(text):
                result.failures.append(f"secret-token: {name}")
            paths = _PATH_RE.findall(text)
            if paths:
                result.failures.append(f"local-path: {name} ({len(paths)})")
            emails = _company_emails(text)
            if emails:
                result.failures.append(f"company-email: {name} ({emails})")
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
