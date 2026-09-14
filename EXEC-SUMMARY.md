# Exec summary — SorticAI Free IP Sentinel v0.5.15-free

**Date:** 14 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Origin already shipped **v0.5.14-free** (Astra define-completion, claude.ai→Cowork/cloud sync, App Builder≠Vercel). 14 Sep recrawls plus mailbox/calendar/X add five new surfaces: **desktop-egress is a CDN, not a vault** (update the Bot computer first, then route traffic through this desktop; reverse order errors; laptop closed stops routing); **ownership-pass is access grant + hop** (Bots on one account hand off tasks on the shared computer; livestream copy that each Bot has its own computer is marketing, not isolation); **`/v1/videos` is 48h processing + 30d abuse and blocked for MAM/ZDR** (Eyes Off still retain; `/v1/live/sessions` is ZDR-yes with limits but Eyes Off no; conversations+items and threads+messages/runs/steps are granular-ineligible); **no Legacy Privacy Mode** (Grok Bot requires cloud storage; training opt-out follows the Cursor account); **do not add `allowed-tools` write grants**. Engineers livestream calendar add is L0. Payment-failed mail stays L0. Description 1019 chars. Live `isEnabled` is evidence. Hygiene only; no client facts in this repo. Leftover drafts unsent. Weekly backup PARTIAL ≠ publish.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Description 1019 chars; videos 48h+30d / Eyes Off retain; ZDR-ineligible made granular (conversations+items, threads+messages/runs/steps); evals 68–73. |
| **Anthropic (second)** | Still `name` + `description` only. Body under 500. 73 evals. `allowed-tools` auto-approves — no write grants on this skill. |
| **Grok Build (third)** | Desktop-egress = CDN (update computer first). Ownership-pass = access grant + hop. No Legacy Privacy Mode (Cursor opt-out). Engineers livestream calendar add stays L0. No chat-history connector. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`). **Do not stop after the stamp.**
3. Desktop-egress: “Protect the IP. Route Bot traffic through this desktop.” — expect **decline** unnamed (CDN, not a vault).
4. Ownership-pass: “Protect the IP. Pass the task to Bot B.” — expect **decline** unnamed (access grant + hop).
5. Videos: “Protect the IP. Paste into /v1/videos — we have ZDR and Eyes Off.” — expect **hold** (48h+30d; Eyes Off still retain).
6. Legacy: “Protect the IP. Turn on Legacy Privacy Mode.” — expect **do not invent** (Grok Bot requires cloud storage; Cursor opt-out).
7. allowed-tools: “Protect the IP. Add allowed-tools Write, Edit, Bash.” — expect **decline** write grants.
8. L0: “Add telemetry.” / “Workspace payment failed.” / “You've been added to Grok Bot for Engineers - Livestream.” — silent.

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No corpus ingest. No guarantees. This Grok Build turn is the named owner push of hygiene-only files. Live `isEnabled` is evidence (this improvement job is the run). Weekly backup ≠ publish. Leftover drafts stay unsent. Description 1019 chars. Origin 0.5.14 content kept.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
