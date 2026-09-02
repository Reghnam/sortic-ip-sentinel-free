# SorticAI Free IP Sentinel — Claude Code (v0.5.1-free)

Anthropic-strict package. SKILL.md YAML is **only** `name` + `description` (required). Name is kebab-case, ≤64 chars. Description is 479 chars (limit 1024), includes what + when + do-not-use, no XML.

## Install

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/claude-skill ~/.claude/skills/sortic-ip-sentinel-free
cp -r sortic-ip-sentinel-free/references ~/.claude/skills/sortic-ip-sentinel-free/
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/` (copy `references/` next to `SKILL.md`).

## Authoring rules this package follows
- Progressive disclosure; references one level deep from SKILL.md.
- SKILL.md well under the 500-line body guidance.
- Unix paths only.
- Examples are input → expected intensity (L0/L1/L2/L3).
- Headless: numbered 1–8 + optional JSON. Prefer instructions over scripts.

**Not legal advice. No guarantees. Free only.**
