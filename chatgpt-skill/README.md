# SorticAI Free IP Sentinel — ChatGPT / Codex (v0.5.3-free)

OpenAI-first package. Minimal SKILL.md frontmatter (`name` + `description` + license/metadata). Display and invocation live in `agents/openai.yaml`.

Canonical rich source: https://github.com/Reghnam/sortic-ip-sentinel-free

## Install

**Codex CLI / IDE (preferred path, 2026 docs)**
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free
```
Also scanned: project `.agents/skills/`, `~/.codex/skills/`, `/etc/codex/skills`.

Invoke: `$sortic-ip-sentinel-free` or `/skills`. Implicit match uses the description (front-loaded triggers, 564 chars). Headless `-p`: unnamed L3 **default-delivers 1 (show/hold) + 8 (JSON)**; or add "Output numbered options and hygiene package JSON."

**ChatGPT Skills (Business / Enterprise / Edu)**
Zip **this folder** so `SKILL.md` is at the zip root. Skills tab → upload. Invoke with `@`.

## Why this variant
- OpenAI hosts may reject extra frontmatter keys (`when-to-use`, `user-invocable`, `compatibility`).
- Descriptions can be truncated in the Codex skills list — triggers are in the first sentence.
- `allow_implicit_invocation: true` so L2/L3 language can auto-load the skill.
- No MCP tool dependencies. Core hygiene is self-contained. Prefer instructions over scripts.
- Computer-use / Bot email-push-post is a demo channel (catalog item 5 + `agent_exposure` JSON). Never email third parties unless this turn names them.
- Builder worksheet: not legal advice; do not send outputs as legal analysis.

**Not legal advice. No guarantees. Free only.**
