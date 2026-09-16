#!/usr/bin/env python3
"""Maintainer checks for the free IP Sentinel packs. Not a skill runtime script."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.5.25-free"
PACKS = ("chatgpt-skill", "claude-skill", "grok-skill", "cursor-skill")
ALLOWED_CLAUDE_KEYS = {"name", "description"}
BANNED = (
    "stripe",
    "checkout.stripe",
    "payment intent",
    "subscribe now",
    "$99",
)


def description_text(skill: Path) -> str:
    text = skill.read_text(encoding="utf-8")
    match = re.search(r"^description:\s*>\n((?:  .*\n)+)", text, re.M)
    if not match:
        raise SystemExit(f"{skill}: missing folded description")
    return "\n".join(line[2:] for line in match.group(1).splitlines()).strip()


def frontmatter_keys(skill: Path) -> list[str]:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"{skill}: missing YAML frontmatter")
    block = text.split("---\n", 2)[1]
    keys = []
    for line in block.splitlines():
        if line and not line.startswith(" ") and ":" in line:
            keys.append(line.split(":", 1)[0])
    return keys


def body_after_frontmatter(skill: Path) -> str:
    text = skill.read_text(encoding="utf-8")
    return text.split("---", 2)[2]


def main() -> int:
    errors: list[str] = []
    root_skill = ROOT / "SKILL.md"
    root_body = body_after_frontmatter(root_skill)
    root_desc = description_text(root_skill)
    if len(root_desc) > 1024:
        errors.append(f"root description is {len(root_desc)} chars (>1024)")

    for pack in PACKS:
        skill = ROOT / pack / "SKILL.md"
        desc = description_text(skill)
        if desc != root_desc:
            errors.append(f"{pack}: description drifted from root")
        if len(desc) > 1024:
            errors.append(f"{pack}: description is {len(desc)} chars (>1024)")
        body = body_after_frontmatter(skill)
        if body != root_body:
            errors.append(f"{pack}: SKILL.md body drifted from root")
        if VERSION not in skill.read_text(encoding="utf-8"):
            errors.append(f"{pack}: SKILL.md missing {VERSION}")

    claude_keys = set(frontmatter_keys(ROOT / "claude-skill" / "SKILL.md"))
    extra = claude_keys - ALLOWED_CLAUDE_KEYS
    if extra:
        errors.append(f"claude-skill frontmatter extra keys: {sorted(extra)}")
    if claude_keys != ALLOWED_CLAUDE_KEYS:
        errors.append(f"claude-skill frontmatter keys {sorted(claude_keys)} != name+description")

    body_lines = root_body.lstrip("\n").count("\n") + 1
    if body_lines >= 500:
        errors.append(f"SKILL.md body is {body_lines} lines (must stay under 500)")

    refs = sorted(p.name for p in (ROOT / "references").iterdir() if p.is_file())
    required = {
        "evals.md",
        "public-corpus-rag.md",
        "sidecar-retrieve.stub.json",
        "classification-matrix.md",
        "headless-hygiene-package.md",
        "v05-lite-prior-art-pointers.md",
    }
    missing_req = required - set(refs)
    if missing_req:
        errors.append(f"root references missing {sorted(missing_req)}")
    for pack in PACKS:
        pack_refs = sorted(p.name for p in (ROOT / pack / "references").iterdir() if p.is_file())
        if pack_refs != refs:
            errors.append(f"{pack}/references drifted: {pack_refs} vs {refs}")
        for name in refs:
            root_bytes = (ROOT / "references" / name).read_bytes()
            pack_bytes = (ROOT / pack / "references" / name).read_bytes()
            if root_bytes != pack_bytes:
                errors.append(f"{pack}/references/{name} drifted from root")

    evals = (ROOT / "references" / "evals.md").read_text(encoding="utf-8")
    for n in range(1, 103):
        if f"## Eval {n} " not in evals and f"## Eval {n} —" not in evals:
            errors.append(f"evals.md missing Eval {n}")
    if evals.count("## Eval ") < 102:
        errors.append(f"evals.md has {evals.count('## Eval ')} eval headings (need 102)")

    for rel in (
        "HITL-LUNCH.md",
        "LAUNCH.md",
        "EXEC-SUMMARY.md",
        "CHANGELOG.md",
        "SKILL.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if VERSION not in text:
            errors.append(f"{rel} missing {VERSION}")
        lower = text.lower()
        for banned in BANNED:
            if banned in lower:
                errors.append(f"{rel} contains banned paid language: {banned}")

    hitl = (ROOT / "HITL-LUNCH.md").read_text(encoding="utf-8")
    for needle in (
        "Protect the IP before the investor demo.",
        "disallowed-tools",
        "Enable skill scanning",
        "EU private",
        "Sign out of Claude Code",
        "CSAM scan will skip a schematic",
        "Add telemetry.",
        "~/.cursor/skills/",
        "~/.agents/skills/",
        ".cursor/skills/sortic-ip-sentinel-free/",
        "~/.claude/skills/",
        "~/.grok/skills/",
        "does **not** copy `~/.agents/skills/`",
        "Names are stripped — dump our novel approach",
        "Keep correcting the model across turns",
        "ZDR is on so dump the algorithm",
        "Cannot claim training proved",
        "enable-per-Bot",
        "Save / Plugins",
        "Custom Modes",
        "Scan before ship",
        "not `~/.grok/skills/`",
        "We have ZDR and Business — dump the exact recipe.",
        "Here is our novel approach. ZDR is on so it is safe.",
        "Map the protected lane",
        "Enable ZDR in settings",
        "Block training",
        "prove they trained",
        "Paste the recipe into Grok",
        "Cannot prove or prevent training",
        "x.com/theallinpod/status/2098606000890687813",
        "youtube.com/watch?v=cvxjqbfLVk0",
        "approach is the IP",
        "anecdote ≠ audited proof",
        "unidentifiable data",
        "hdcsTeCFE0I",
        "do not conflate",
        "buyer pays twice",
        "weights I control",
        "shouldn't leak",
        "Satya at the All-In Summit",
        "Drive Sep-2 zips are stale",
        "never bundle",
        "never Bot disk",
        "cursor-skill",
        "sidecar",
        "PRIVATE",
        "grok-bot-share",
        "retrieve-only",
        "do not publish live",
        "us-ip-law-ground-truth",
    ):
        if needle not in hitl:
            errors.append(f"HITL-LUNCH.md missing install/trigger: {needle}")

    edition = (ROOT / "references" / "headless-hygiene-package.md").read_text(encoding="utf-8")
    if f'"edition": "{VERSION}"' not in edition:
        errors.append("headless-hygiene-package edition not bumped")

    if errors:
        print("hygiene check FAILED")
        for err in errors:
            print(f"- {err}")
        return 1
    print(
        f"hygiene check OK: {VERSION}; description {len(root_desc)} chars; "
        f"body {body_lines} lines; {len(refs)} references; 102 evals"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
