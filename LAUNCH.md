# LAUNCH: SorticAI Free IP Sentinel v0.5.14-free

**Status**: Public on GitHub. v0.5.14-free patched 2026-09-14 (OpenAI → Anthropic → Grok Build: Astra define-completion / over-refusal; claude.ai→Cowork/cloud sync is a publish; App Builder preview is a demo, Vercel deploy is a publish; Grok zero-config `~/.agents/skills/` discovery). All files sanitized for free-only use. Strong disclaimers included.

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
2. Skills tab → upload. Invoke with `@`. Zip is scanned — no secrets.

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

Grok Build / project: `.grok/skills/sortic-ip-sentinel-free/`. Headless (`grok -p`) and **Grok Bot** use numbered options + optional JSON. Do not ask the Grok viewer to run shell commands. Bot must not email third parties unless this turn names them. Backup is not publish.

## 4. Verification Checklist

- [ ] L3 triggers ("protect the IP", "IP sensitive moment", "Bot will email the deck — protect the IP")
- [ ] L0 silence on privacy/config/meta work, US IP corpus ticks, workspace renewal, weekly backup, livestream attend
- [ ] Headless: stamp → numbered 1–8 → JSON schema `sorticai.hygiene_package.v1` (includes `agent_exposure`, `owner_gated`)
- [ ] Unnamed headless default-delivers 1+8 same turn
- [ ] Disclaimers appear on all outputs
- [ ] All deliverables are free-only (no paid language)
- [ ] Evals in `references/evals.md` still pass (now 67: Astra define-completion, claude.ai sync, App Builder vs Vercel, Grok discovery, scheduled-task flag, inspect-before-attach)
- [ ] Unnamed GitHub auto-push / registrar login / partner send / pay / identity / voice provision / yolo-send → decline
- [ ] Backup ≠ publish; truncated/junk/placeholder files are not originals; image-only ≠ numbered facts
- [ ] Bot share / marketplace clone is a demo channel; callable hops hold internals
- [ ] API no-train is not treated as ChatGPT no-train; Skills execution is not treated as ZDR-covered
- [ ] Bot screens are not treated as isolation; Bot-to-Bot DM is a hop
- [ ] Astra define-completion: do not stop after the L3 stamp; do not pad extra refuse language
- [ ] App Builder live preview is a demo; unnamed Vercel deploy is declined
- [ ] claude.ai enablement / CLAUDE_CODE_SYNC_SKILLS=1 is a publish; local ~/.claude/skills/ still does not auto-sync

**This is free procedural hygiene only. Not legal advice. No guarantees.**
