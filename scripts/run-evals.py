#!/usr/bin/env python3
"""Deterministic L0–L3 activation eval harness. Keyword hits are warnings.

Reads tests/evals/*.jsonl. Required fields are id, prompt, and expected_level.
must and must_not are optional lists and are carried through untouched.
Unknown fields are kept. gate_excluded fixtures are omitted from coverage,
the gate counts, and keyword warnings, and are reported as their own total.

Trigger phrases are the quoted Triggers: list in the root when-to-use field.
Description prose is not parsed. The Claude pack has no when-to-use field, so
a second block scores that pack's description alone: only trigger phrases that
actually occur in the description count.

Exit 0 when the schema is valid and every level is present in the gate set.
The gate set is tests/evals/activation_v0.1.jsonl when that file is present,
otherwise every loaded file. Keyword misses are warnings and do not fail.
Exit non-zero only for malformed fixtures or a missing gate level.
--model-in-loop is a stub: it prints a fixed line and exits 0. It does not
call an API and it does not read secrets or environment keys.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LEVELS = ("L0", "L1", "L2", "L3")
REQUIRED = ("id", "prompt", "expected_level")
LIST_FIELDS = ("must", "must_not")
BOOL_FIELDS = ("ambiguous", "gate_excluded", "headless")
STR_FIELDS = ("category", "rationale", "context_note")
GATE_NAME = "activation_v0.1.jsonl"
CLAUDE_SKILL = Path("claude-skill") / "SKILL.md"


def folded_field(text: str, key: str) -> str:
    """Return one folded frontmatter scalar, or an empty string."""
    match = re.search(rf"(?m)^{re.escape(key)}:\s*>-?\n((?:  .*\n)+)", text)
    if not match:
        return ""
    lines = [line[2:].strip() for line in match.group(1).splitlines()]
    return re.sub(r"\s+", " ", " ".join(line for line in lines if line)).strip()


def _dedupe(phrases: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for phrase in phrases:
        cleaned = re.sub(r"\s+", " ", phrase).strip(" .;:")
        if len(cleaned) < 2:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(cleaned)
    ordered.sort(key=lambda item: (item.casefold(), item))
    return ordered


def parse_trigger_phrases(skill_text: str) -> list[str]:
    """Quoted phrases from the when-to-use Triggers list only.

    The description is not read. Unquoted words after Triggers: are not
    phrases, so the list does not depend on sentence shape.
    """
    collapsed = re.sub(r"\s+", " ", folded_field(skill_text, "when-to-use")).strip()
    match = re.search(r"\bTriggers:\s*(.*?)(?:\.|$)", collapsed, re.IGNORECASE)
    if not match:
        return []
    return _dedupe(re.findall(r'"([^"]+)"', match.group(1)))


def attested_phrases(phrases: list[str], text: str) -> list[str]:
    """Keep phrases that occur in text as whole tokens."""
    folded = re.sub(r"\s+", " ", text).strip()
    return [phrase for phrase in phrases if phrase_matches(folded, phrase)]


def phrase_matches(prompt: str, phrase: str) -> bool:
    pattern = r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])"
    return re.search(pattern, prompt, re.IGNORECASE) is not None


def matched_phrases(prompt: str, phrases: list[str]) -> list[str]:
    return [phrase for phrase in phrases if phrase_matches(prompt, phrase)]


def _rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def fixture_paths(root: Path) -> list[Path]:
    directory = root / "tests" / "evals"
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.glob("*.jsonl") if path.is_file())


def load_fixture_groups(root: Path) -> tuple[list[tuple[str, list[dict]]], list[str]]:
    """Load every JSONL file separately. Dicts are the parsed objects."""
    groups: list[tuple[str, list[dict]]] = []
    errors: list[str] = []
    seen: dict[str, str] = {}
    paths = fixture_paths(root)
    if not paths:
        errors.append("tests/evals has no jsonl fixtures")
        return groups, errors
    for path in paths:
        rel = _rel(root, path)
        file_rows: list[dict] = []
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: file is not utf-8")
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            where = f"{rel}:{lineno}"
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                errors.append(f"{where}: invalid JSON")
                continue
            if not isinstance(row, dict):
                errors.append(f"{where}: fixture is not an object")
                continue
            for key in REQUIRED:
                if key not in row:
                    errors.append(f"{where}: missing key {key}")
            if "id" in row and (not isinstance(row["id"], str) or row["id"] == ""):
                errors.append(f"{where}: id is not a non-empty string")
            if "prompt" in row and not isinstance(row["prompt"], str):
                errors.append(f"{where}: prompt is not a string")
            level = row.get("expected_level")
            if "expected_level" in row and level not in LEVELS:
                errors.append(f"{where}: expected_level is not L0, L1, L2, or L3")
            for key in LIST_FIELDS:
                if key in row and not _string_list(row[key]):
                    errors.append(f"{where}: {key} is not a list of strings")
            for key in BOOL_FIELDS:
                if key in row and not isinstance(row[key], bool):
                    errors.append(f"{where}: {key} is not a bool")
            for key in STR_FIELDS:
                if key in row and not isinstance(row[key], str):
                    errors.append(f"{where}: {key} is not a string")
            fixture_id = row.get("id")
            if isinstance(fixture_id, str) and fixture_id != "":
                previous = seen.get(fixture_id)
                if previous:
                    errors.append(f"duplicate id {fixture_id} in {previous} and {where}")
                else:
                    seen[fixture_id] = where
            if not any(error.startswith(f"{where}:") for error in errors):
                file_rows.append(row)
        groups.append((rel, file_rows))
    return groups, errors


def load_fixtures(root: Path) -> tuple[list[dict], list[str]]:
    """Load every JSONL fixture. Returned dicts are the parsed objects."""
    groups, errors = load_fixture_groups(root)
    fixtures = [row for _rel_path, rows in groups for row in rows]
    return fixtures, errors


def gate_excluded(row: dict) -> bool:
    return row.get("gate_excluded") is True


def level_counts(rows: list[dict], *, gate_only: bool) -> dict[str, int]:
    counts = {level: 0 for level in LEVELS}
    for row in rows:
        if gate_only and gate_excluded(row):
            continue
        level = row.get("expected_level")
        if level in counts:
            counts[level] += 1
    return counts


def format_counts(counts: dict[str, int]) -> str:
    return " ".join(f"{level}={counts[level]}" for level in LEVELS)


def keyword_warnings(rows: list[dict], phrases: list[str]) -> list[str]:
    """L0 trigger hits and L2/L3 trigger misses. Excluded rows are skipped."""
    lines: list[str] = []
    false_positive: list[tuple[str, str]] = []
    missed: list[tuple[str, str]] = []
    for row in rows:
        if gate_excluded(row):
            continue
        level = row["expected_level"]
        hits = matched_phrases(row["prompt"], phrases)
        if level == "L0" and hits:
            false_positive.append((row["id"], ", ".join(hits)))
        elif level in ("L2", "L3") and not hits:
            missed.append((row["id"], level))
    for fixture_id, hits in sorted(false_positive):
        lines.append(f"warning false-positive: {fixture_id} L0 matched: {hits}")
    for fixture_id, level in sorted(missed):
        lines.append(f"warning missed-moment: {fixture_id} {level} matched none")
    return lines


def unscored_lines(rows: list[dict]) -> list[str]:
    """Echo must_not lists without scoring or rewriting them."""
    lines: list[str] = []
    for row in rows:
        items = row.get("must_not")
        if not items:
            continue
        rendered = "; ".join(items)
        lines.append(f"unscored must_not: {row['id']}: {rendered}")
    return lines


def score_lines(rows: list[dict], phrases: list[str]) -> list[str]:
    """One file scored against one phrase list. Warnings are not a failure."""
    all_counts = level_counts(rows, gate_only=False)
    gate_counts = level_counts(rows, gate_only=True)
    excluded = sum(1 for row in rows if gate_excluded(row))
    warnings = keyword_warnings(rows, phrases)
    false_positive = sum(1 for line in warnings if line.startswith("warning false-positive:"))
    missed = sum(1 for line in warnings if line.startswith("warning missed-moment:"))
    return [
        f"fixtures: {len(rows)}",
        f"excluded: {excluded}",
        f"gate: {len(rows) - excluded}",
        f"triggers: {len(phrases)}",
        f"levels all: {format_counts(all_counts)}",
        f"levels gate: {format_counts(gate_counts)}",
        *warnings,
        *unscored_lines(rows),
        (
            "summary: "
            f"false-positive={false_positive} "
            f"missed-moment={missed} "
            f"excluded={excluded}"
        ),
    ]


def claude_description_phrases(root: Path, phrases: list[str]) -> list[str] | None:
    """Phrases from the explicit list that the Claude description contains.

    Returns None when the Claude pack is not in the tree. The body and the
    when-to-use field are not read.
    """
    path = root / CLAUDE_SKILL
    if not path.is_file():
        return None
    description = folded_field(path.read_text(encoding="utf-8"), "description")
    return attested_phrases(phrases, description)


def render(root: Path) -> tuple[str, int]:
    groups, errors = load_fixture_groups(root)
    if errors:
        body = "\n".join(f"error: {error}" for error in errors) + "\nfailed"
        return body, 1
    skill = root / "SKILL.md"
    phrases: list[str] = []
    if skill.is_file():
        phrases = parse_trigger_phrases(skill.read_text(encoding="utf-8"))
    claude_phrases = claude_description_phrases(root, phrases)
    named = [rel for rel, _rows in groups if Path(rel).name == GATE_NAME]
    gate_rels = set(named or [rel for rel, _rows in groups])
    multi = len(groups) > 1 or claude_phrases is not None
    lines: list[str] = []
    missing: list[str] = []
    for rel, rows in groups:
        if multi:
            lines.append(f"block: root {rel}")
        lines.extend(score_lines(rows, phrases))
        if claude_phrases is not None:
            lines.append(f"block: claude-description {rel}")
            lines.extend(score_lines(rows, claude_phrases))
        if rel in gate_rels:
            counts = level_counts(rows, gate_only=True)
            missing.extend(level for level in LEVELS if counts[level] == 0)
    if missing:
        lines.append("error: missing level " + ", ".join(missing) + " in gate set")
        lines.append("failed")
        return "\n".join(lines), 1
    lines.append("ok")
    return "\n".join(lines), 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic L0-L3 activation eval harness.")
    parser.add_argument(
        "--model-in-loop",
        action="store_true",
        help="Stub. Prints a fixed line and exits 0. No API calls.",
    )
    parser.add_argument("--root", default=None, help="Repository root. Default is this repo.")
    args = parser.parse_args(argv)
    if args.model_in_loop:
        print("model-in-loop: not configured")
        return 0
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    text, code = render(root)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
