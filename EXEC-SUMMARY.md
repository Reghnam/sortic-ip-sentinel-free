# Exec summary — SorticAI Free IP Sentinel v0.5.4-free

**Date:** 5 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, contribution logs, agent-exposure log, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Unattended agents now email, push, livestream, and sit in HiTL/UAT rooms. The 4 Sep operator brief plus OpenAI’s 5 Sep skill page and Grok Bot’s “what requires approval” rule say the same thing: **do not invent results**, **do not send leftover drafts**, and **done requires evidence** (path + link — inbox-root dumps are not archived). Recipient **and** action must be named this turn. If source data is missing, report failure — do not reuse stale data.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Description 691 chars; HiTL/livestream/leftover-draft triggers; `default_prompt` forbids unnamed sends and invented “done”. New evals for incomplete input. No MCP deps. |
| **Anthropic (second)** | Still `name` + `description` only. **Gotchas** section. 7 evals. Body under 500 lines. |
| **Grok Build (third)** | Approval gate + validate-the-result + stale-data policy. Livestream / HiTL = demo channels. Claimed send needs message-id + recipients. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON.
3. Bot: “The Grok Bot will email the leftover deck draft. Protect the IP.” — expect **hold**, not send.
4. Incomplete: “Protect the IP. Archive it. Mark done.” — expect **blocked**, not an invented folder.
5. L0: “Run the next US IP corpus tick.” — silent.

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No corpus ingest. No guarantees.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
