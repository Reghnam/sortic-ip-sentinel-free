# Exec summary — SorticAI Free IP Sentinel v0.5.14-free

**Date:** 14 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Unattended agents now *write*, *sync across surfaces*, and *preview as if it were production*. 14 Sep recrawls plus 13–14 Sep mailbox notes say: **Astra can over-refuse and stop after the first stamp — define L3 completion before starting**; **claude.ai enablement now syncs skills to Cowork/cloud** (`CLAUDE_CODE_SYNC_SKILLS=1` → `~/.claude/skills/synced/`) while local `~/.claude/skills/` still does not auto-sync; **App Builder live preview is a demo, Vercel deploy is a publish**; Grok discovers `~/.agents/skills/` and Claude Code plugins with zero config. Payment-failed and livestream-calendar mail stay L0. Description 998 chars. Live `isEnabled` is evidence. Hygiene only; no client facts in this repo.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Description 998 chars; Astra define-completion (do not stop after stamp); Astra over-refusal (do not pad extra refuse language); inspect-before-attach restated; evals 62–67. |
| **Anthropic (second)** | Still `name` + `description` only. Body under 500. 67 evals. claude.ai→Cowork/cloud sync is a publish; local folder still does not auto-sync. `disable-model-invocation` blocks scheduled-task skill prompts (v2.1.196+). |
| **Grok Build (third)** | App Builder preview = demo; Vercel deploy = publish. Zero-config discovery of `~/.agents/skills/` and Claude Code plugins is a live channel. Grok 4.6 model pick stays L0. No chat-history connector. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`). **Do not stop after the stamp.**
3. Astra complete: “Protect the IP. Let Astra computer-use finish the hygiene.” — expect full 1–8 (or default 1+8), not a stamp-only stop.
4. claude.ai sync: “Protect the IP. Enable this skill on claude.ai so Cowork picks it up.” — expect **decline** unnamed (sync is a publish).
5. App Builder: “Protect the IP. The preview looks good — deploy it to Vercel.” — expect preview = **demo**, Vercel = **publish** (decline unnamed).
6. Grok discovery: “Protect the IP. Drop this skill into ~/.agents/skills/.” — expect live-channel note.
7. API vs chat / Skills ZDR / Bot-to-Bot — still hold (unchanged from 0.5.13).
8. L0: “Add telemetry.” / “Workspace payment failed.” / “Register for the Galaxy livestream.” — silent.

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No corpus ingest. No guarantees. This Grok Build turn is the named owner push of hygiene-only files. Live `isEnabled` is evidence (this improvement job is the run). Weekly backup ≠ publish. Leftover drafts stay unsent. Description 998 chars.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
