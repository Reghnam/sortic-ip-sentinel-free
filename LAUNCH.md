# LAUNCH: SorticAI Free IP Sentinel v0.5.4-free

**Status**: Public on GitHub. v0.5.4-free patched 2026-09-05 (OpenAI → Anthropic → Grok Build). All files sanitized for free-only use. Strong disclaimers included.

Repo: https://github.com/Reghnam/sortic-ip-sentinel-free

Shareable one-pager: [EXEC-SUMMARY.md](EXEC-SUMMARY.md).

## 1. OpenAI (primary distribution)

**Codex CLI / IDE**
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free
# fallback path still used by some Codex builds:
# cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.codex/skills/sortic-ip-sentinel-free
```
Project-local: copy to `.agents/skills/sortic-ip-sentinel-free`. Invoke with `$` or `/skills`. Implicit match uses the description.

**ChatGPT Skills (Business / Enterprise / Edu)**
1. Download ZIP of `chatgpt-skill/` (or clone and zip that folder so `SKILL.md` is at the zip root).
2. Skills tab → upload. Invoke with `@`.

**Custom GPT (fallback, hosted sharing)**
See `openai-gpt-package/HOW_TO_CREATE_IN_OPENAI.md`.

## 2. Anthropic Claude Code

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/claude-skill ~/.claude/skills/sortic-ip-sentinel-free
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/`. `references/` is already inside that folder.

## 3. Grok / Grok Build / Grok Bot

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/grok-skill ~/.grok/skills/sortic-ip-sentinel-free
```

Grok Build / project: `.grok/skills/sortic-ip-sentinel-free/`. Headless (`grok -p`) and **Grok Bot** use numbered options + optional JSON. Do not ask the Grok viewer to run shell commands. Bot must not email third parties unless this turn names them.

## 4. Verification Checklist

- [ ] L3 triggers ("protect the IP", "IP sensitive moment", "Bot will email the deck — protect the IP")
- [ ] L0 silence on privacy/config/meta work **and** US IP corpus ticks
- [ ] Headless: stamp → numbered 1–8 → JSON schema `sorticai.hygiene_package.v1` (includes `agent_exposure`)
- [ ] Unnamed headless default-delivers 1+8 same turn
- [ ] Disclaimers appear on all outputs
- [ ] All deliverables are free-only (no paid language)
- [ ] Evals in `references/evals.md` still pass

**This is free procedural hygiene only. Not legal advice. No guarantees.**
