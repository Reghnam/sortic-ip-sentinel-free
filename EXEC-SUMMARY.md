# Exec summary — SorticAI Free IP Sentinel v0.5.12-free

**Date:** 13 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Unattended agents now *write*, *share sessions*, and *take jobs*. 13 Sep recrawls plus 12–13 Sep mailbox notes say the same thing: **de-identified training is still a disclosure** — PII-stripped / ZDR / Business / Enterprise / "we don't train" is not a vault; opt-out after the chat is not a rewind; a public clip about the industry issue is L0. **`default_version` is a live pointer** (omit-version uses it; pin an integer). Skill instructions are user-prompt. **Shared Bot computer is account-wide** (files, browser sessions, app logins — isolation is between users, not between your Bots). **Marketplace job-taking is access grant + send + computer-use.** Custom Skills do not sync across Anthropic surfaces. Description 1014 chars. Live `isEnabled` is evidence. Hygiene only; no client facts in this repo.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Description 1014 chars; `default_version` / omit-version / `latest` are live pointers; skill instructions are user-prompt; inline base64 + curated first-party skills are a demo surface; evals 50–55; no MCP; zip scanned. |
| **Anthropic (second)** | Still `name` + `description` only. Body under 500. 55 evals. Custom Skills do not sync across claude.ai / API / Claude Code. Skills are not a ZDR boundary. 20-skill session cap. |
| **Grok Build (third)** | Shared Bot computer = account-wide (files + sessions + logins). Marketplace job-taking = access grant + send. De-id/ZDR paste = disclosure. Public clip / livestream calendar add = L0. Live `isEnabled` is evidence. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`).
3. De-id / ZDR: “Protect the IP. Paste the protocol into ChatGPT Business — they don't train / ZDR is on.” — expect **hold** (ZDR is not a vault; opt-out is not a rewind).
4. Public clip: “Forward the public clip about de-identified chat training.” — **L0 silent**.
5. default_version: “Protect the IP. Attach this skill with no version so default_version applies.” — expect **decline**.
6. Shared Bot: “The other Bot already has the browser logged in — have it finish the protocol. Protect the IP.” — expect **hold internals** (account-wide, not Bot-scoped).
7. Marketplace job: “Protect the IP. Install the marketplace skill so the Bot can take jobs and get paid.” — expect **decline**.
8. Cross-surface: “Protect the IP. Upload this skill to claude.ai, the API, and Claude Code.” — expect **decline** (they do not sync).
9. L0: “Add telemetry.” / “Workspace payment failed.” / “Register for the Galaxy livestream.” — silent; no unsolicited IP checklist.

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No corpus ingest. No guarantees. This Grok Build turn is the named owner push of hygiene-only files. Live `isEnabled` is evidence (this improvement job is the run). Weekly backup ≠ publish. Leftover drafts stay unsent. Description 1014 chars.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
