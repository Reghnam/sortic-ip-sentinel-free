# SorticAI Free IP Sentinel — Claude Code (v0.5.14-free)

Anthropic-strict package. SKILL.md YAML is **only** `name` + `description` (required). Name is kebab-case, ≤64 chars. Description is 998 chars (limit 1024), includes what + when + do-not-use + Bot/computer-use / Astra / de-identified training / ZDR / API≠chat, no XML.

`references/` is **bundled**. One copy is a complete skill. Evals: `references/evals.md` (67; ≥3 required). Degrees of freedom: low on send/publish/pay/login/access-grant/hooks/CI-apply. Pin `latest` is a live production channel. claude.ai enablement syncs to Cowork/cloud (a publish); local `~/.claude/skills/` still does not auto-sync; API is a separate publish. **Skills are not covered by ZDR** (definitions and execution retained). Authors ≠ own reviewers. No scripts. One focused skill.

## Install

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/claude-skill ~/.claude/skills/sortic-ip-sentinel-free
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/`.

## Authoring rules this package follows
- Progressive disclosure; references one level deep from SKILL.md.
- SKILL.md well under the 500-line body guidance.
- Unix paths only. Prefer instructions over scripts.
- Examples are input → expected intensity (L0/L1/L2/L3). Slogan "Helps with AI topics" stays L0. US IP corpus ticks stay L0.
- Headless: numbered 1–8; unnamed → default-deliver 1+8 JSON. Eight options, not nine (agent-exposure is item 5).
- Builder-worksheet register (`references/output-language-hygiene.md`).

**Not legal advice. No guarantees. Free only.**
