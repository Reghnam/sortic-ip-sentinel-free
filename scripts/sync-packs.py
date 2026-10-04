#!/usr/bin/env python3
"""Copy the canonical skill into the host packs and stamp the current edition.

Source of truth is scripts/check-hygiene.py: VERSION and PACKS.
The root SKILL.md body (after frontmatter) and references/ are copied into
each pack. Folded descriptions are copied too, because the hygiene check
requires them to match. Pack frontmatter other than that description is kept.
openai-gpt-package/knowledge/ files that already share a name with a root
reference are the hand-synced knowledge copies. Same-name files are updated.
Other knowledge files are left alone. A file under a pack references/
directory that is absent from root references/ is deleted.

Edition slots are stamped only when they still carry the previous edition.
Historical pins, LICENSE titles, and CHANGELOG.md are not rewritten.
Running this on a tree that already matches is a no-op.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VER = r"\d+\.\d+\.\d+-free"
STAMP_EXT = {".md", ".txt", ".json", ".yml", ".yaml"}
SKIP_NAMES = {"CHANGELOG.md", "LICENSE.md"}


def _slot(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern)


AUTHORITATIVE = (
    _slot(rf'(?m)^(?P<pre>\s*version:\s*")(?P<ver>{VER})(?P<post>")'),
    _slot(rf'(?P<pre>"edition":\s*")(?P<ver>{VER})(?P<post>")'),
    _slot(
        rf'(?m)^(?P<pre>[^\n]*short-description:\s*"[^\n]*\bv)(?P<ver>{VER})(?P<post>)'
    ),
    _slot(rf'(?P<pre>\|  v)(?P<ver>{VER})(?P<post> \(portable\))'),
    _slot(rf'(?P<pre>Version in header: v)(?P<ver>{VER})(?P<post>)'),
    _slot(rf'(?P<pre>Current version: \*\*v)(?P<ver>{VER})(?P<post>\*\*)'),
    _slot(rf'(?P<pre>Free Edition \(v)(?P<ver>{VER})(?P<post>\))'),
)

EXTRA = (
    _slot(rf'(?m)^(?P<pre># [^\n]*\bv)(?P<ver>{VER})(?P<post>)'),
    _slot(rf'(?P<pre>Public on GitHub\. v)(?P<ver>{VER})(?P<post>)'),
    _slot(rf'(?P<pre>L3 stamp `v)(?P<ver>{VER})(?P<post>`)'),
    _slot(rf'(?P<pre>as \*\*v)(?P<ver>{VER})(?P<post>\*\*)'),
    _slot(rf'(?P<pre>Free IP Sentinel \(v)(?P<ver>{VER})(?P<post>\))'),
    _slot(rf'(?P<pre>hygiene sentinel \(\*\*v)(?P<ver>{VER})(?P<post>\*\*)'),
    _slot(rf'(?P<pre>\(v)(?P<ver>{VER})(?P<post> portable edition\))'),
    _slot(rf'(?P<pre>free edition\) v)(?P<ver>{VER})(?P<post>)'),
    _slot(rf'(?m)^(?P<pre>- [^\n]*\(v)(?P<ver>{VER})(?P<post>\)\s*$)'),
)

DESC_RE = re.compile(r"^description:\s*>\n(?:  .*\n)+", re.M)
KNOWLEDGE_DIR = Path("openai-gpt-package/knowledge")


@dataclass
class Plan:
    version: str
    packs: tuple[str, ...]
    ref_names: tuple[str, ...]
    knowledge_count: int
    writes: dict[str, bytes] = field(default_factory=dict)
    deletes: list[str] = field(default_factory=list)

    def diffs(self) -> list[str]:
        lines = [f"drift: {rel}" for rel in sorted(self.writes)]
        lines.extend(
            f"delete: {rel} (absent from root references/)"
            for rel in sorted(self.deletes)
        )
        return lines


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def read_version(root: Path) -> str:
    text = (root / "scripts" / "check-hygiene.py").read_text(encoding="utf-8")
    match = re.search(r'^VERSION = "([^"]+)"', text, re.M)
    if not match:
        raise SystemExit("scripts/check-hygiene.py is missing VERSION")
    return match.group(1)


def read_packs(root: Path) -> tuple[str, ...]:
    text = (root / "scripts" / "check-hygiene.py").read_text(encoding="utf-8")
    match = re.search(r"^PACKS = \(([^)]*)\)", text, re.M)
    if not match:
        raise SystemExit("scripts/check-hygiene.py is missing PACKS")
    names = tuple(re.findall(r'"([^"]+)"', match.group(1)))
    if not names:
        raise SystemExit("scripts/check-hygiene.py PACKS is empty")
    return names


def _stamp_candidates(root: Path) -> list[str]:
    found: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith((".git/", "dist/", "tests/", "scripts/")):
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.suffix.lower() not in STAMP_EXT:
            continue
        found.append(rel)
    return found


def _apply_slots(text: str, patterns: tuple[re.Pattern[str], ...], from_ver: str, target: str) -> str:
    def sub(match: re.Match[str]) -> str:
        if match.group("ver") != from_ver:
            return match.group(0)
        return match.group("pre") + target + match.group("post")

    for pattern in patterns:
        text = pattern.sub(sub, text)
    return text


def stamp_text(text: str, from_ver: str | None, target: str) -> str:
    if not from_ver or from_ver == target:
        return text
    text = _apply_slots(text, AUTHORITATIVE, from_ver, target)
    return _apply_slots(text, EXTRA, from_ver, target)


def _slot_versions(text: str) -> set[str]:
    found: set[str] = set()
    for pattern in AUTHORITATIVE:
        for match in pattern.finditer(text):
            found.add(match.group("ver"))
    return found


def detect_from_version(texts: dict[str, str], target: str) -> str | None:
    found: set[str] = set()
    for text in texts.values():
        found |= _slot_versions(text)
    found.discard(target)
    if not found:
        return None
    if len(found) > 1:
        joined = ", ".join(sorted(found))
        raise SystemExit(f"edition slots disagree: {joined}")
    return found.pop()


def split_skill(text: str) -> tuple[str, str]:
    """Split YAML frontmatter from the body.

    The closer is a line whose text is exactly ``---``. A ``---`` token
    inside a frontmatter value stays in the frontmatter.
    """
    if text.startswith("---\r\n"):
        newline = "\r\n"
    elif text.startswith("---\n"):
        newline = "\n"
    else:
        raise SystemExit("SKILL.md is missing YAML frontmatter")
    lines = text.split(newline)
    if not lines or lines[0] != "---":
        raise SystemExit("SKILL.md is missing YAML frontmatter")
    close = None
    for index in range(1, len(lines)):
        if lines[index] == "---":
            close = index
            break
    if close is None:
        raise SystemExit("SKILL.md frontmatter is not closed")
    front = newline.join(lines[: close + 1])
    if close == len(lines) - 1:
        body = ""
    else:
        body = newline + newline.join(lines[close + 1 :])
    return front, body


def description_block(text: str, label: str) -> str:
    match = DESC_RE.search(text)
    if not match:
        raise SystemExit(f"{label}: missing folded description")
    return match.group(0)


def replace_description(text: str, block: str, label: str) -> str:
    match = DESC_RE.search(text)
    if not match:
        raise SystemExit(f"{label}: missing folded description")
    if match.group(0) == block:
        return text
    return text[: match.start()] + block + text[match.end() :]


def _encode_like(original: bytes, text: str) -> bytes:
    if original.decode("utf-8") == text:
        return original
    return text.encode("utf-8")


def _reference_names(root: Path) -> tuple[str, ...]:
    ref_dir = root / "references"
    if not ref_dir.is_dir():
        raise SystemExit("references/ is missing")
    names = sorted(p.name for p in ref_dir.iterdir() if p.is_file())
    if not names:
        raise SystemExit("references/ has no files")
    return tuple(names)


def _is_pack_skill(rel: str, packs: tuple[str, ...]) -> bool:
    return any(rel == f"{pack}/SKILL.md" for pack in packs)


def _is_pack_reference(rel: str, packs: tuple[str, ...]) -> bool:
    return any(rel.startswith(f"{pack}/references/") for pack in packs)


def _is_knowledge_copy(rel: str, ref_names: set[str]) -> bool:
    prefix = KNOWLEDGE_DIR.as_posix() + "/"
    if not rel.startswith(prefix):
        return False
    return rel[len(prefix) :] in ref_names


def build_plan(root: Path) -> Plan:
    target = read_version(root)
    packs = read_packs(root)
    ref_names = _reference_names(root)
    ref_set = set(ref_names)
    originals: dict[str, bytes] = {}
    texts: dict[str, str] = {}
    for rel in _stamp_candidates(root):
        data = (root / rel).read_bytes()
        originals[rel] = data
        texts[rel] = data.decode("utf-8")
    from_ver = detect_from_version(texts, target)
    stamped = {rel: stamp_text(text, from_ver, target) for rel, text in texts.items()}

    writes: dict[str, bytes] = {}
    deletes: list[str] = []

    def consider(rel: str, data: bytes) -> None:
        path = root / rel
        current = path.read_bytes() if path.is_file() else None
        if current != data:
            writes[rel] = data

    for rel, text in stamped.items():
        if _is_pack_skill(rel, packs) or _is_pack_reference(rel, packs):
            continue
        if _is_knowledge_copy(rel, ref_set):
            continue
        consider(rel, _encode_like(originals[rel], text))

    if "SKILL.md" not in stamped:
        raise SystemExit("root SKILL.md is missing")
    root_skill = stamped["SKILL.md"]
    _front, root_body = split_skill(root_skill)
    root_desc = description_block(root_skill, "SKILL.md")

    ref_bytes: dict[str, bytes] = {}
    for name in ref_names:
        rel = f"references/{name}"
        if rel in stamped:
            ref_bytes[name] = _encode_like(originals[rel], stamped[rel])
        else:
            ref_bytes[name] = (root / rel).read_bytes()

    for pack in packs:
        skill_rel = f"{pack}/SKILL.md"
        skill_path = root / skill_rel
        if not skill_path.is_file():
            raise SystemExit(f"{skill_rel} is missing")
        original = skill_path.read_bytes()
        skill_text = original.decode("utf-8")
        skill_text = split_skill(skill_text)[0] + root_body
        skill_text = replace_description(skill_text, root_desc, skill_rel)
        skill_text = stamp_text(skill_text, from_ver, target)
        consider(skill_rel, _encode_like(original, skill_text))

        for name, data in ref_bytes.items():
            consider(f"{pack}/references/{name}", data)
        pack_refs = root / pack / "references"
        if pack_refs.is_dir():
            for path in pack_refs.iterdir():
                if path.is_file() and path.name not in ref_bytes:
                    deletes.append(f"{pack}/references/{path.name}")

    knowledge_count = 0
    knowledge = root / KNOWLEDGE_DIR
    if knowledge.is_dir():
        for path in sorted(knowledge.iterdir()):
            if path.is_file() and path.name in ref_bytes:
                knowledge_count += 1
                consider(f"{KNOWLEDGE_DIR.as_posix()}/{path.name}", ref_bytes[path.name])

    return Plan(
        version=target,
        packs=packs,
        ref_names=ref_names,
        knowledge_count=knowledge_count,
        writes=writes,
        deletes=deletes,
    )


def apply_plan(root: Path, plan: Plan) -> None:
    for rel in plan.deletes:
        (root / rel).unlink()
    for rel, data in plan.writes.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def format_ok(plan: Plan) -> str:
    return (
        f"sync check OK: {plan.version}; {len(plan.packs)} packs; "
        f"{len(plan.ref_names)} references; {plan.knowledge_count} knowledge copies"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync host packs from the repo root.")
    parser.add_argument("--check", action="store_true", help="exit 1 if a sync would change files")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = (args.root or repo_root_from_script()).resolve()
    plan = build_plan(root)
    diffs = plan.diffs()
    if args.check:
        if diffs:
            print("sync check FAILED")
            for line in diffs:
                print(f"- {line}")
            return 1
        print(format_ok(plan))
        return 0
    apply_plan(root, plan)
    if diffs:
        print(f"sync wrote {len(plan.writes)} files, deleted {len(plan.deletes)}")
    print(format_ok(plan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
