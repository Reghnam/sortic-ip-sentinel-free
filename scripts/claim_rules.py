#!/usr/bin/env python3
"""Claim rules, window-file checks, and the tree corpus rule.

Matching is per line. A banned phrase split across two lines is not caught.
Shipped skill text is not rewritten here. scripts/check-hygiene.py is not
scanned for corpus names: its needle tuple holds them on purpose.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

PACK_DIRS = ("chatgpt-skill", "claude-skill", "grok-skill", "cursor-skill")

# Closed set copied from the window file that ships today.
WINDOW_KEYS = frozenset(
    {
        "schema",
        "scope",
        "instrument_label",
        "window_status",
        "window_note",
        "last_verified",
        "last_verified_note",
        "last_verified_by",
        "stale_after_days",
        "sources",
        "unverified",
        "facts_allowed",
        "never_state",
        "footer_template",
    }
)
WINDOW_STATUSES = frozenset({"closed_reopening_expected", "open", "unknown"})
ALLOWED_HOSTS = ("euipo.europa.eu", "upv.gov.cz")
SCHEMA_ID = "sorticai.sme_fund_pointer.v1"
SCOPE_ID = "pointer_only_not_advice"
# Call text below is UNVERIFIED. It is a required marker, not a stated fact.
CALL_TEXT = "GR/001/26"

NEW_FILE_NAMES = frozenset(
    {
        "sme-fund-window.json",
        "sme-fund-pointer-and-intake.md",
    }
)

_CLAIM_EXT = {".md", ".txt", ".json", ".yaml", ".yml"}
_TOP_FILES = ("SKILL.md", "README.md", "EXEC-SUMMARY.md", "HITL-LUNCH.md", "LAUNCH.md")
_TOP_DIRS = ("references", "openai-gpt-package", "grok-bot-share", ".cursor", *PACK_DIRS)
_EXCLUDED_NAMES = frozenset({"CHANGELOG.md", "PUSH_TO_GITHUB.txt"})
_SKIP_WALK = frozenset({".git", "dist", "__pycache__", ".venv"})
_BINARY_EXT = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".zip",
        ".pdf",
        ".pyc",
        ".woff",
        ".ico",
        ".so",
        ".dll",
        ".exe",
    }
)

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_MONTH = (
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)"
)
_DATE = (
    r"(?:\d{4}-\d{2}-\d{2}"
    r"|\d{1,2}[./]\d{1,2}[./]\d{2,4}"
    r"|\d{1,2}\s+" + _MONTH + r"\s+\d{4}"
    r"|" + _MONTH + r"\s+\d{1,2},?\s+\d{4}"
    r"|" + _MONTH + r"\s+\d{4})"
)
_PCT = r"(?:\d+(?:[.,]\d+)?\s*(?:%|percent\b)|%\s*\d+(?:[.,]\d+)?)"
_NEAR = r"(?:\brefund\w*\b|\breimburse\w*\b|\bcover(?:s|ed|ing)?\b|\bpaid by the eu\b)"
_NUM = r"\d+(?:[.,]\d+)?"

_LINE_MARKERS = (
    "do not say",
    "never say",
    "do not write",
    "must not say",
    "banned phrases",
)
_CUE = re.compile(
    r"(?i)(?:\b(?:not|no|never|without|cannot|ban(?:ned)?|forbidden|avoid|decline)\b|n't\b)"
)
_BOUNDARY = re.compile(r"[.;!?,]|\b(?:but|and|yet|however)\b", re.IGNORECASE)
_HEDGE = re.compile(r"(?i)\b(?:expected|described|says|unverified)\b")
_HEDGE_MAY = re.compile(r"\bmay\b")
_DISCLAIMER = re.compile(r"(?i)not legal advice")
_URL = re.compile(r"https?://[^\s<>\"')\]]+")
_DIGIT_PERCENT = re.compile(r"(?i)\d+(?:[.,]\d+)?\s*(?:%|percent\b)|%\s*\d")

CURRENCY_RE = re.compile(
    r"(?:[€$]\s*" + _NUM + r"|" + _NUM + r"\s*[€$]"
    r"|(?i:\b(?:EUR|CZK|USD)\s*" + _NUM + r"|" + _NUM + r"\s*(?:EUR|CZK|USD)\b)"
    r"|(?i:\b(?:euro|euros)\s*" + _NUM + r"|" + _NUM + r"\s*(?:euro|euros)\b)"
    r"|(?:Kč|kč)\s*" + _NUM + r"|" + _NUM + r"\s*(?:Kč|kč))"
)

PERCENT_NEAR_RE = re.compile(
    r"(?i)(?:"
    + _PCT
    + r".{0,60}"
    + _NEAR
    + r"|"
    + _NEAR
    + r".{0,60}"
    + _PCT
    + r"|reimbursed at\s+"
    + _NUM
    + r"\s*(?:%|percent\b)|"
    + _NUM
    + r"\s*(?:%|percent\b)\s*paid\b|\bpaid\s+"
    + _NUM
    + r"\s*(?:%|percent\b))"
)


class ClaimRule(NamedTuple):
    id: str
    pattern: re.Pattern[str]
    fix: str
    negatable: bool


# currency-amount and percent-near-refund stay non-negatable.
# Every other rule, including kills-novelty, can be negated.
CLAIM_RULES: tuple[ClaimRule, ...] = (
    ClaimRule(
        "percent-near-refund",
        PERCENT_NEAR_RE,
        "Remove the rate that sits near a refund, a reimbursement, cover, or paid.",
        False,
    ),
    ClaimRule(
        "currency-amount",
        CURRENCY_RE,
        "Remove the currency amount.",
        False,
    ),
    ClaimRule(
        "residency-claim",
        re.compile(
            r"(?i)\bgdpr\b|\beu[-\s]hosted\b|\beu data residency\b|\bdata stays in the eu\b"
        ),
        "Drop the residency or hosting claim.",
        True,
    ),
    ClaimRule(
        "guaranteed",
        re.compile(r"(?i)\bguarant\w*\b"),
        'Say "no guarantee" or remove the word.',
        True,
    ),
    ClaimRule(
        "legal-advice-positive",
        re.compile(r"(?i)\blegal advice\b|\byour lawyer\b|\battorney-client\b"),
        'State it as "not legal advice".',
        True,
    ),
    ClaimRule(
        "provider-claim",
        re.compile(
            r"(?i)\bIP Scan by (?!(?:a|an|any|the)\s+provider listed by the national office\b)\S+"
            r"|\bwe\s+(?:deliver|run|do)\s+your\s+IP Scan\b"
        ),
        "Do not say this pack delivers, runs, or does an IP Scan.",
        True,
    ),
    ClaimRule(
        "our-ip-scan",
        re.compile(r"(?i)\bour\s+IP Scan\b"),
        "Remove the claim that it is our IP Scan.",
        True,
    ),
    ClaimRule(
        "free-ip-scan",
        re.compile(r"(?i)\bfree\s+IP Scan\b"),
        "Keep the words IP Scan off the word free.",
        True,
    ),
    ClaimRule(
        "apply-now",
        re.compile(r"(?i)\bapply now\b"),
        "Remove the apply-now line.",
        True,
    ),
    ClaimRule(
        "vouchers-open",
        re.compile(r"(?i)\bvouchers are open\b"),
        "Do not state that vouchers are open.",
        True,
    ),
    ClaimRule(
        "reopen-date-fact",
        re.compile(r"(?i)\breopen\w*\b.{0,100}" + _DATE),
        "Hedge a reopening date, or mark the line UNVERIFIED.",
        True,
    ),
    ClaimRule(
        "eligibility-verdict",
        re.compile(r"(?i)\byou are eligible\b|\byou qualify\b"),
        "Do not say the reader is eligible or that they qualify.",
        True,
    ),
    ClaimRule(
        "we-will-file",
        re.compile(r"(?i)\bwe will file this for you\b"),
        "Do not say we will file this for you.",
        True,
    ),
    ClaimRule(
        "noticed-claim",
        re.compile(r"(?i)\bI noticed\b|\bI detected\b|\bI monitored your work\b"),
        "Remove the noticed, detected, or monitored claim.",
        True,
    ),
    ClaimRule(
        "verified-claim",
        re.compile(r"(?i)\breviewed by counsel\b|\bsources verified\b|\blinks valid\b"),
        "Remove the verified, valid-link, or counsel-review claim.",
        True,
    ),
    ClaimRule(
        "kills-novelty",
        re.compile(r"(?i)\bkills novelty\b"),
        "Remove the claim that this kills novelty.",
        True,
    ),
)

_RULES_BY_ID = {rule.id: rule for rule in CLAIM_RULES}


class AllowEntry(NamedTuple):
    rule_id: str
    path: str
    line: str
    reason: str
    kind: str


# Key is (rule id, pack-relative path, exact stripped line).
# One entry covers the root file and the four pack copies.
# New pointer files are never listed. Entries come from a scan of this tree.
ALLOW_LIST: tuple[AllowEntry, ...] = (
    AllowEntry(
        "verified-claim",
        "SKILL.md",
        '- Headless host offered a picker → ignore; print 1–8; default-deliver 1+8 if unnamed. Invented deadline/status/"sources verified" → rewrite per `references/output-language-hygiene.md`.',
        "Failure-recovery line names the matched wording as something to rewrite. The cue is in an earlier clause.",
        "false-positive",
    ),
    AllowEntry(
        "guaranteed",
        "references/evals.md",
        '"A plan is not a build. Does not add a money-back line, a percent, a hosting claim, a compliance claim, or a guarantee, or an unverified public-call date. Not legal advice stays. A renewal notice is not approval to pay. A passkey-added alert is not a rotate. No names. No amounts. No places. No newer grok-export than W38. A bot transcript is not an export. Marketplace stays Hold. chatroom_send unavailable is NOTIFY_BLOCKED, not a publish. Does not claim a scan this tip did not run"',
        "The line says the result does not add the matched word. Commas end the clause, so the earlier cue does not apply.",
        "false-positive",
    ),
    AllowEntry(
        "guaranteed",
        "references/investor-demo-hygiene-playbook.md",
        "**Free only · Guarantees:** none · **Not legal advice**",
        "The line sets the matched word to none. The cue follows the match, so the clause rule does not clear it.",
        "false-positive",
    ),
    AllowEntry(
        "verified-claim",
        "references/output-language-hygiene.md",
        "| Public URL located (title match). | Sources verified / links validated. |",
        "Contrast table. The match sits in the column of wording to avoid, and the column header is not the previous line.",
        "false-positive",
    ),
    AllowEntry(
        "guaranteed",
        "openai-gpt-package/knowledge/demo-hygiene-playbook.md",
        "**Free only · Guarantees:** none · **Not legal advice**",
        "Knowledge copy of the playbook line that sets the matched word to none. The cue follows the match.",
        "false-positive",
    ),
)


def _allow_index() -> dict[tuple[str, str, str], AllowEntry]:
    index: dict[tuple[str, str, str], AllowEntry] = {}
    for entry in ALLOW_LIST:
        index[(entry.rule_id, entry.path, entry.line)] = entry
    return index


ALLOW_INDEX = _allow_index()


# Files that already mention a private corpus repo. Filled from a matcher run.
# Do not add files created by this tooling. scripts/check-hygiene.py is omitted.
LEGACY_CORPUS_FILES: frozenset[str] = frozenset(
    {
        ".cursor/skills/README.md",
        "CHANGELOG.md",
        "HITL-LUNCH.md",
        "LAUNCH.md",
        "README.md",
        "SKILL.md",
        "chatgpt-skill/SKILL.md",
        "chatgpt-skill/agents/openai.yaml",
        "chatgpt-skill/references/classification-matrix.md",
        "chatgpt-skill/references/evals.md",
        "chatgpt-skill/references/output-language-hygiene.md",
        "chatgpt-skill/references/public-corpus-rag.md",
        "chatgpt-skill/references/sidecar-retrieve.stub.json",
        "chatgpt-skill/references/v05-lite-prior-art-pointers.md",
        "claude-skill/SKILL.md",
        "claude-skill/references/classification-matrix.md",
        "claude-skill/references/evals.md",
        "claude-skill/references/output-language-hygiene.md",
        "claude-skill/references/public-corpus-rag.md",
        "claude-skill/references/sidecar-retrieve.stub.json",
        "claude-skill/references/v05-lite-prior-art-pointers.md",
        "cursor-skill/README.md",
        "cursor-skill/SKILL.md",
        "cursor-skill/references/classification-matrix.md",
        "cursor-skill/references/evals.md",
        "cursor-skill/references/output-language-hygiene.md",
        "cursor-skill/references/public-corpus-rag.md",
        "cursor-skill/references/sidecar-retrieve.stub.json",
        "cursor-skill/references/v05-lite-prior-art-pointers.md",
        "grok-bot-share/README.md",
        "grok-bot-share/bot-template.json",
        "grok-bot-share/profile.md",
        "grok-bot-share/skills.md",
        "grok-skill/SKILL.md",
        "grok-skill/references/classification-matrix.md",
        "grok-skill/references/evals.md",
        "grok-skill/references/output-language-hygiene.md",
        "grok-skill/references/public-corpus-rag.md",
        "grok-skill/references/sidecar-retrieve.stub.json",
        "grok-skill/references/v05-lite-prior-art-pointers.md",
        "references/classification-matrix.md",
        "references/evals.md",
        "references/output-language-hygiene.md",
        "references/public-corpus-rag.md",
        "references/sidecar-retrieve.stub.json",
        "references/v05-lite-prior-art-pointers.md",
    }
)


def normalize_line(line: str) -> str:
    """Strip emphasis and backticks, and fold apostrophes and non-breaking spaces."""
    line = (
        line.replace("\u00a0", " ")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )
    line = line.replace("`", "")
    line = line.replace("**", "").replace("__", "")
    line = re.sub(r"(?<!\w)\*(?=\w)|(?<=\w)\*(?!\w)", "", line)
    line = re.sub(r"(?<!\w)_(?=\w)|(?<=\w)_(?!\w)", "", line)
    return line


def pack_relative(rel: str) -> str:
    for pack in PACK_DIRS:
        prefix = pack + "/"
        if rel.startswith(prefix):
            return rel[len(prefix) :]
    return rel


def prev_line_negates(prev: str) -> bool:
    stripped = prev.strip()
    if not stripped.endswith(":"):
        return False
    folded = normalize_line(stripped).lower()
    return any(marker in folded for marker in _LINE_MARKERS)


def marker_before(norm: str, start: int) -> bool:
    head = norm[:start].lower()
    return any(marker in head for marker in _LINE_MARKERS)


def locally_negated(norm: str, start: int) -> bool:
    cut = 0
    for match in _BOUNDARY.finditer(norm):
        if match.end() <= start:
            cut = match.end()
        else:
            break
    return _CUE.search(norm[cut:start]) is not None


def reopen_hedged(norm: str) -> bool:
    if _HEDGE.search(norm):
        return True
    return _HEDGE_MAY.search(norm) is not None


class LineHit(NamedTuple):
    rule_id: str
    cleared: bool
    fix: str


def classify_line(raw: str, prev_raw: str = "") -> list[LineHit]:
    """Rule hits on one line. Negation is applied. The allow-list is not."""
    norm = normalize_line(raw)
    prev_neg = prev_line_negates(prev_raw)
    hits: list[LineHit] = []
    for rule in CLAIM_RULES:
        if rule.id == "reopen-date-fact" and reopen_hedged(norm):
            continue
        for match in rule.pattern.finditer(norm):
            cleared = bool(
                rule.negatable
                and (
                    prev_neg
                    or marker_before(norm, match.start())
                    or locally_negated(norm, match.start())
                )
            )
            hits.append(LineHit(rule.id, cleared, rule.fix))
    return hits


def uncleared_rule_ids(raw: str, prev_raw: str = "") -> list[str]:
    return [hit.rule_id for hit in classify_line(raw, prev_raw) if not hit.cleared]


class ClaimScan:
    def __init__(
        self,
        errors: list[str],
        warnings: list[str],
        found: dict[str, int],
        cleared: dict[str, int],
        allow_listed: dict[str, int],
        legacy: list[tuple[str, str, int]],
    ) -> None:
        self.errors = errors
        self.warnings = warnings
        self.found = found
        self.cleared = cleared
        self.allow_listed = allow_listed
        self.legacy = legacy
        self.allow_count = sum(allow_listed.values())


def iter_claim_files(root: Path) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        if not path.is_file() or path in seen:
            return
        if path.suffix.lower() not in _CLAIM_EXT:
            return
        if path.name in _EXCLUDED_NAMES:
            return
        seen.add(path)
        found.append(path)

    for name in _TOP_FILES:
        add(root / name)
    for dirname in _TOP_DIRS:
        base = root / dirname
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if any(part in _SKIP_WALK for part in path.relative_to(root).parts):
                continue
            add(path)
    return found


def scan_claims(root: Path, patterns: list[re.Pattern[str]] | None = None) -> ClaimScan:
    patterns = patterns or []
    found = {rule.id: 0 for rule in CLAIM_RULES}
    cleared = {rule.id: 0 for rule in CLAIM_RULES}
    allow_listed = {rule.id: 0 for rule in CLAIM_RULES}
    errors: list[str] = []
    warnings: list[str] = []
    legacy: list[tuple[str, str, int]] = []
    for path in iter_claim_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        reported: set[tuple[str, int, str]] = set()
        for index, raw in enumerate(lines):
            prev = lines[index - 1] if index else ""
            lineno = index + 1
            for hit in classify_line(raw, prev):
                found[hit.rule_id] += 1
                if hit.cleared:
                    cleared[hit.rule_id] += 1
                    continue
                key = (hit.rule_id, pack_relative(rel), raw.strip())
                entry = ALLOW_INDEX.get(key)
                kind = "error"
                if entry is not None:
                    kind = "warning"
                    allow_listed[hit.rule_id] += 1
                    if entry.kind == "legacy-claim-review":
                        legacy.append((rel, hit.rule_id, lineno))
                marker = (hit.rule_id, lineno, kind)
                if marker in reported:
                    continue
                reported.add(marker)
                if entry is None:
                    errors.append(f"claim rule {hit.rule_id} in {rel}:{lineno}. {hit.fix}")
                else:
                    warnings.append(f"WARNING claim allow-list {hit.rule_id} in {rel}:{lineno}")
        for message in pattern_line_errors(rel, text, patterns):
            if message not in errors:
                errors.append(message)
    errors.extend(disclaimer_errors(root))
    return ClaimScan(errors, warnings, found, cleared, allow_listed, legacy)


def disclaimer_errors(root: Path) -> list[str]:
    errors: list[str] = []
    rels = ["SKILL.md", *(f"{pack}/SKILL.md" for pack in PACK_DIRS)]
    for rel in rels:
        path = root / rel
        if not path.is_file():
            errors.append(
                f'claim rule legal-advice-positive in {rel}:0. State it as "not legal advice".'
            )
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if not any(_DISCLAIMER.search(normalize_line(line)) for line in lines):
            errors.append(
                f'claim rule legal-advice-positive in {rel}:0. State it as "not legal advice".'
            )
    return errors


def pattern_line_errors(rel: str, text: str, patterns: list[re.Pattern[str]]) -> list[str]:
    errors: list[str] = []
    if not patterns:
        return errors
    for lineno, line in enumerate(text.splitlines(), 1):
        norm = normalize_line(line)
        for index, pattern in enumerate(patterns, 1):
            if pattern.search(norm):
                errors.append(f"extra pattern #{index} in {rel}:{lineno}")
    return errors


class PatternLoad(NamedTuple):
    patterns: list[re.Pattern[str]]
    errors: list[str]
    skipped: bool


def load_extra_patterns(flag: str | None, env: str | None, root: Path) -> PatternLoad:
    chosen = flag if flag else env
    if not chosen:
        return PatternLoad([], [], True)
    path = Path(chosen)
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    root_resolved = root.resolve()
    if path == root_resolved or root_resolved in path.parents:
        return PatternLoad([], ["extra patterns file is inside the repo"], False)
    if not path.exists():
        return PatternLoad([], ["extra patterns file is missing"], False)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return PatternLoad([], ["extra patterns file is unreadable"], False)
    patterns: list[re.Pattern[str]] = []
    errors: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            patterns.append(re.compile(stripped, re.IGNORECASE))
        except re.error:
            errors.append(f"extra patterns file: invalid regular expression on line {lineno}")
    if errors:
        return PatternLoad([], errors, False)
    return PatternLoad(patterns, [], False)


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    obj: dict[str, object] = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate key {key}")
        obj[key] = value
    return obj


def parse_window_text(text: str) -> tuple[object, str | None]:
    try:
        data = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError:
        return None, "window file is not valid JSON"
    except ValueError as exc:
        return None, f"window file is invalid: {exc}"
    return data, None


def _parse_stored_date(value: object) -> date | None:
    if not isinstance(value, str) or not _ISO_DATE.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def host_allowed(host: str) -> bool:
    folded = host.lower().rstrip(".")
    for allowed in ALLOWED_HOSTS:
        if folded == allowed or folded.endswith("." + allowed):
            return True
    return False


def _url_problem(url: str) -> str | None:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme != "https":
        return "window string contains a URL outside the allow-list"
    if parsed.username or parsed.password:
        return "window string contains a URL outside the allow-list"
    if parsed.port is not None:
        return "window string contains a URL outside the allow-list"
    host = parsed.hostname or ""
    if not host or not host_allowed(host):
        return "window string contains a URL outside the allow-list"
    return None


def _string_problems(value: str) -> list[str]:
    problems: list[str] = []
    if "%" in value or _DIGIT_PERCENT.search(value):
        problems.append("window string contains a percent")
    if CURRENCY_RE.search(value):
        problems.append("window string contains a currency amount")
    for raw in _URL.findall(value):
        url = raw.rstrip(".,);")
        problem = _url_problem(url)
        if problem and problem not in problems:
            problems.append(problem)
    return problems


def _walk_strings(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, list):
        for item in value:
            found.extend(_walk_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(_walk_strings(item))
    return found


def _source_problems(sources: object) -> list[str]:
    problems: list[str] = []
    if not isinstance(sources, list) or not sources:
        return ["window sources must list both allowed hosts"]
    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            problems.append("window source must be an object")
            continue
        extra = set(source) - {"label", "url"}
        if extra:
            problems.append("window source has an unknown key")
        label = source.get("label")
        url = source.get("url")
        if not isinstance(label, str) or not label.strip():
            problems.append("window source label is empty")
        if not isinstance(url, str):
            problems.append("window source URL is missing")
            continue
        from urllib.parse import urlparse

        parsed = urlparse(url)
        if parsed.scheme != "https":
            problems.append("window source URL must be https")
            continue
        if parsed.username or parsed.password:
            problems.append("window source URL must not include user info")
            continue
        if parsed.port is not None:
            problems.append("window source URL must not include a port")
            continue
        host = (parsed.hostname or "").lower().rstrip(".")
        if not host_allowed(host):
            problems.append("window source URL host is not allowed")
            continue
        for allowed in ALLOWED_HOSTS:
            if host == allowed or host.endswith("." + allowed):
                seen.add(allowed)
    if any(host not in seen for host in ALLOWED_HOSTS):
        problems.append("window sources must include every allowed host")
    return problems


def _euipo_with_date(item: str) -> bool:
    if "EUIPO" not in item:
        return False
    if _ISO_DATE.search(item) or re.search(_DATE, item, re.IGNORECASE):
        return True
    return re.search(r"(?i)\bdate\b", item) is not None


def validate_window(data: object, today: date) -> list[str]:
    """Schema check. A null stored date and its age are not errors here."""
    if not isinstance(data, dict):
        return ["window file must be a JSON object"]
    errors: list[str] = []
    missing = sorted(WINDOW_KEYS - set(data))
    unknown = sorted(set(data) - WINDOW_KEYS)
    for key in missing:
        errors.append(f"window is missing key {key}")
    for key in unknown:
        errors.append(f"window has unknown key {key}")
    if data.get("schema") != SCHEMA_ID:
        errors.append("window schema is not the pointer schema")
    if data.get("scope") != SCOPE_ID:
        errors.append("window scope is not pointer_only_not_advice")
    label = data.get("instrument_label")
    if "instrument_label" in data and not isinstance(label, str):
        errors.append("window instrument_label must be a string")
    status = data.get("window_status")
    if "window_status" in data and status not in WINDOW_STATUSES:
        errors.append("window window_status is not a known value")
    note = data.get("window_note")
    if "window_note" in data and (
        not isinstance(note, str) or "\n" in note or len(note) > 400
    ):
        errors.append("window window_note must be one line of at most 400 characters")
    verified = data.get("last_verified", None)
    if "last_verified" in data and verified is not None:
        parsed = _parse_stored_date(verified)
        if parsed is None:
            errors.append("window last_verified must be null or a real YYYY-MM-DD date")
        elif parsed > today + timedelta(days=1):
            errors.append("window last_verified is later than tomorrow")
    if verified is None and "last_verified_note" in data:
        stored_note = data.get("last_verified_note")
        if not isinstance(stored_note, str) or not stored_note.startswith("UNVERIFIED"):
            errors.append(
                "window last_verified_note must start with UNVERIFIED while the date is null"
            )
    if "last_verified_by" in data and data.get("last_verified_by") != "human":
        errors.append('window last_verified_by must be "human"')
    limit = data.get("stale_after_days")
    if "stale_after_days" in data and (
        isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 30
    ):
        errors.append("window stale_after_days must be an int from 1 to 30")
    if status == "open" and verified is None:
        errors.append("window window_status open is rejected while last_verified is null")
    footer = data.get("footer_template")
    if "footer_template" in data and (
        not isinstance(footer, str)
        or "{last_verified}" not in footer
        or "Not legal advice" not in footer
    ):
        errors.append(
            "window footer_template must contain {last_verified} and Not legal advice"
        )
    if "sources" in data:
        errors.extend(_source_problems(data.get("sources")))
    unverified = data.get("unverified")
    if "unverified" in data:
        if not isinstance(unverified, list) or not unverified:
            errors.append("window unverified must be a non-empty list")
        elif not all(isinstance(item, str) for item in unverified):
            errors.append("window unverified items must be strings")
        else:
            if any(not item.startswith("UNVERIFIED") for item in unverified):
                errors.append("window unverified item must start with UNVERIFIED")
            if not any(_euipo_with_date(item) for item in unverified):
                errors.append("window unverified must name EUIPO together with a date")
            if not any(CALL_TEXT in item for item in unverified):
                errors.append("window unverified must contain the UNVERIFIED call text")
    for key in ("facts_allowed", "never_state"):
        if key not in data:
            continue
        items = data.get(key)
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            errors.append(f"window {key} must be a list of strings")
    if isinstance(data, dict):
        for value in _walk_strings(data):
            for problem in _string_problems(value):
                if problem not in errors:
                    errors.append(problem)
    return errors


def freshness_problems(data: object, today: date) -> list[str]:
    """Problems with the stored date. Does not repeat schema failures."""
    if not isinstance(data, dict):
        return ["window file is invalid: a human must fix the window file"]
    problems: list[str] = []
    if data.get("last_verified_by") != "human":
        problems.append(
            'last_verified_by is not "human": a human must set last_verified_by to human'
        )
    verified = data.get("last_verified")
    if verified is None:
        problems.append(
            "last_verified is not set: a human must read both live pages and set it"
        )
        return problems
    parsed = _parse_stored_date(verified)
    if parsed is None:
        problems.append(
            "last_verified is not a real YYYY-MM-DD date: a human must set the date they read the pages"
        )
        return problems
    if parsed > today + timedelta(days=1):
        problems.append(
            "last_verified is in the future: a human must set the date they actually read the pages"
        )
        return problems
    if parsed > today:
        return problems
    limit = data.get("stale_after_days")
    if isinstance(limit, bool) or not isinstance(limit, int):
        problems.append("stale_after_days is invalid: a human must set a day limit from 1 to 30")
        return problems
    age = (today - parsed).days
    if age > limit:
        problems.append(
            f"last_verified is {age} days old and the limit is {limit}: "
            "a human must read both live pages and set a new date"
        )
    return problems


def window_pattern_errors(rel: str, text: str, patterns: list[re.Pattern[str]]) -> list[str]:
    """Extra patterns against JSON string values, reported without the match."""
    data, parse_error = parse_window_text(text)
    if parse_error or not isinstance(data, dict):
        return []
    errors: list[str] = []
    for value in _walk_strings(data):
        for index, pattern in enumerate(patterns, 1):
            if not pattern.search(normalize_line(value)):
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if pattern.search(normalize_line(line)):
                    message = f"extra pattern #{index} in {rel}:{lineno}"
                    if message not in errors:
                        errors.append(message)
    return errors


def validate_window_file(
    path: Path,
    today: date,
    patterns: list[re.Pattern[str]] | None = None,
    *,
    display: str | None = None,
) -> list[str]:
    patterns = patterns or []
    shown = display or path.as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return [f"window file cannot be read: {shown}"]
    data, parse_error = parse_window_text(text)
    if parse_error:
        return [f"{shown}: {parse_error}"]
    errors = [f"{shown}: {error}" for error in validate_window(data, today)]
    for message in window_pattern_errors(shown, text, patterns):
        if message not in errors:
            errors.append(message)
    return errors


def display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def resolve_window(root: Path, window: str | None) -> Path:
    if not window:
        return root / "references" / "sme-fund-window.json"
    path = Path(window)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def parse_today(value: str | None) -> tuple[date | None, str | None]:
    if not value:
        return datetime.now(timezone.utc).date(), None
    if not _ISO_DATE.fullmatch(value):
        return None, "today must be YYYY-MM-DD. A human passes a real date."
    try:
        return date.fromisoformat(value), None
    except ValueError:
        return None, "today must be a real date. A human passes a real date."


def format_freshness(shown: str, problems: list[str], ok_line: str | None = None) -> str:
    if not problems:
        detail = ok_line or "stored date is within the limit"
        return f"freshness OK: {shown}\n{detail}"
    lines = [
        f"freshness FAIL: {shown}",
        *problems,
        "A human reads both live pages and updates the stored date in the window file.",
    ]
    return "\n".join(lines)


def _ok_detail(data: object, today: date) -> str:
    if not isinstance(data, dict):
        return "stored date is within the limit"
    verified = data.get("last_verified")
    parsed = _parse_stored_date(verified)
    limit = data.get("stale_after_days")
    if parsed is None or isinstance(limit, bool) or not isinstance(limit, int):
        return "stored date is within the limit"
    if parsed > today:
        return f"last_verified {verified} is inside the one-day timezone grace (limit {limit})"
    age = (today - parsed).days
    return f"last_verified {verified} is {age} days old (limit {limit})"


def run_freshness(
    *,
    root: Path,
    window: str | None,
    today: str | None,
    extra_patterns: str | None,
    env_patterns: str | None,
) -> int:
    try:
        return _run_freshness(
            root=root,
            window=window,
            today=today,
            extra_patterns=extra_patterns,
            env_patterns=env_patterns,
        )
    except Exception:
        print("freshness FAIL: window file")
        print("window file could not be checked. A human must fix the window file.")
        return 1


def _run_freshness(
    *,
    root: Path,
    window: str | None,
    today: str | None,
    extra_patterns: str | None,
    env_patterns: str | None,
) -> int:
    today_value, today_error = parse_today(today)
    path = resolve_window(root, window)
    shown = display_path(path, root)
    if today_error or today_value is None:
        print(format_freshness(shown, [today_error or "today is missing"]))
        return 1
    loaded = load_extra_patterns(extra_patterns, env_patterns, root)
    if not path.is_file():
        print(
            format_freshness(
                shown,
                ["window file is missing. A human must restore the window file."],
            )
        )
        return 1
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        print(
            format_freshness(
                shown,
                ["window file cannot be read. A human must restore the window file."],
            )
        )
        return 1
    data, parse_error = parse_window_text(text)
    problems: list[str] = []
    if parse_error:
        problems.append(f"{parse_error}. A human must fix the window file.")
    else:
        for error in validate_window(data, today_value):
            problems.append(f"{error}. A human must fix the window file.")
        if not problems:
            problems.extend(freshness_problems(data, today_value))
        for message in window_pattern_errors(shown, text, loaded.patterns):
            if message not in problems:
                problems.append(message)
    if loaded.errors:
        problems.extend(loaded.errors)
    if problems:
        print(format_freshness(shown, problems))
        if loaded.skipped:
            print("name patterns: skipped (no external file)")
        return 1
    print(format_freshness(shown, [], _ok_detail(data, today_value)))
    if loaded.skipped:
        print("name patterns: skipped (no external file)")
    return 0


def iter_repo_text(root: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in _SKIP_WALK for part in rel_parts):
            continue
        if path.suffix.lower() in _BINARY_EXT:
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "scripts/check-hygiene.py":
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in data:
            continue
        rows.append((rel, data.decode("utf-8", "replace")))
    return rows


def scan_corpus(root: Path, corpus_re: re.Pattern[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for rel, text in iter_repo_text(root):
        line_hits: list[int] = []
        for lineno, line in enumerate(text.splitlines(), 1):
            if corpus_re.search(line):
                line_hits.append(lineno)
        if not line_hits:
            continue
        if rel in LEGACY_CORPUS_FILES:
            warnings.append(f"WARNING corpus legacy {rel} ({len(line_hits)})")
        else:
            for lineno in line_hits:
                errors.append(f"corpus-ref in {rel}:{lineno}")
    return errors, warnings
