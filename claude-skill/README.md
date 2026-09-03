# SorticAI Free IP Sentinel — Claude Code (v0.5.2-free)

Anthropic-strict package. SKILL.md YAML is **only** `name` + `description` (required). Name is kebab-case, ≤64 chars. Description is 595 chars (limit 1024), includes what + when + do-not-use + headless JSON, no XML.

`references/` is **bundled** (v0.5.2). One copy is a complete skill.

## Install

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/claude-skill ~/.claude/skills/sortic-ip-sentinel-free
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/`.

## Authoring rules this package follows
- Progressive disclosure; references one level deep from SKILL.md.
- SKILL.md well under the 500-line body guidance (~212 lines).
- Unix paths only.
- Examples are input → expected intensity (L0/L1/L2/L3). Slogan "Helps with AI topics" stays L0.
- Headless: numbered 1–8; unnamed → default-deliver 1+8 JSON. Prefer instructions over scripts.
- Builder-worksheet register (`references/output-language-hygiene.md`).

**Not legal advice. No guarantees. Free only.**
