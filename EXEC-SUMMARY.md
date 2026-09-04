# Exec summary — SorticAI Free IP Sentinel v0.5.3-free

**Date:** 4 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, contribution logs, agent-exposure log, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Headless agents now have their own computers (Grok Bot, Codex/Claude `-p`, browser-use). That is a live demo channel — they can email, push, and post. Operator briefs from 1–3 Sep 2026 said the same two rules we now bake in: **do not invent status** and **do not email third parties unless this turn names them**. Adjacent hourly IP-lawyer training stays a separate corpus; this skill stays hygiene-only.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Description front-loads Bot/computer-use triggers (564 chars). `default_prompt` forbids unnamed third-party sends. Agent-exposure folded into catalog item 5 (not a 9th picker). |
| **Anthropic (second)** | Still `name` + `description` only. New `references/evals.md` (≥3 evals). Body ~231 lines. Default 1+8 unchanged. |
| **Grok Build (third)** | `argument-hint` for slash commands. Grok Bot = headless. Email/push/browser/social = demo channels. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON.
3. Bot: “The Grok Bot will email the deck. Protect the IP.” — expect holdbacks; **no send** unless you named the recipient.
4. L0: “Run the next US IP corpus tick.” — silent.

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No corpus ingest. No guarantees.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
