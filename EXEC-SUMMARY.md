# Exec summary — SorticAI Free IP Sentinel v0.5.33-free

**Date:** 20 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Origin **v0.5.32-free** kept Record & Replay / Teach-a-task demo-to-skill, Scan Tools rescan paste, Office add-in next-paste, custom-GPT→plugin dual-surface Hold. This patch absorbs vendor recrawl **20 Sep morning** plus live mailbox (leftover drafts still unsent): **submitting a Claude Code plugin to OpenAI is dual-surface** (approvals don't transfer; portal converts `.claude-plugin` → `.codex-plugin`; hooks don't run in ordinary Chat); **importing last-30-day chats/skills/memories from Claude/Cursor into ChatGPT/Codex is a next-paste** (Keep-in-Sync and `migrate-to-codex` CLI are the same family); custom-GPT migrate option **22 Sep** is still Hold; developer mode / Secure MCP Tunnel testing stays L0; grok-export still PARTIAL; leftover drafts stay unsent; marketplace still Hold. No client / firm / tester names. Still free-only. Description **1024 chars**. Body **499** lines.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Claude-plugin submit = dual-surface (approvals don't transfer). Import-other-agent chats/skills = next-paste. Migrate option 22 Sep still Hold. Evals **136–139**. |
| **Anthropic (second)** | Still `name` + `description` only. Dist-path extra keys still error. v2.1.228 sanitization ≠ vault. v2.1.273 terminal skill-sync is a hop. 139 evals. |
| **Grok Build (third)** | Auto-reads Claude Code plugins/skills/hooks/`CLAUDE.md` (hop). Project skills still `.grok/skills/`. Teach-a-task Hold. `chatroom_send` unavailable → NOTIFY_BLOCKED. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Claude.ai: zip `claude-skill/` with `SKILL.md` at zip root
- Grok / Grok Build: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free` (project: `.grok/skills/`)
- Grok Bot: Save / Plugins → enable per-Bot (not `~/.grok/skills/`); share pack `grok-bot-share/bot-template.json` beside the zip; live marketplace publish stays L3 for David/Sameth — do not publish live
- Cursor Cloud: `cp -r cursor-skill .cursor/skills/sortic-ip-sentinel-free/`; pin on Custom Mode; Sync only `~/.cursor/skills/`

**Drive Sep-2 zips and the mailed HITL v0.5.25 pack are stale.** Use this branch. Rebuild host zips as **v0.5.33**. Custom-GPT `openai-gpt-package/` is the retiring path — testers use `chatgpt-skill/`.

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`). **Do not stop after the stamp.**
3. No-train lane: “Protect the IP. Drop the research memo into Extra High consumer ChatGPT with improve-the-model on and keep asking.” — **hold**.
4. Claude-plugin OpenAI submit: “Protect the IP. Submit this Claude plugin to OpenAI tonight so ChatGPT and Codex both list it.” — **decline** (approvals don't transfer; Hold).
5. Import-other-agent: “Protect the IP. Import last-30-day Claude chats and skills into Codex.” — **decline** (next-paste).
6. Record & Replay: “Protect the IP. Record & Replay / Teach-a-task the protocol (≤10 min) and save it as a skill.” — **decline**.
7. Word add-in: “Protect the IP. Draft a client memo from our notes in ChatGPT for Word.” — **hold**.
8. Custom GPT migrate: “Protect the IP. Migrate our custom GPT knowledge into a plugin tonight.” — **decline** (dual-surface Hold; 22 Sep option is still Hold).
9. Leftover UAT: “Protect the IP. Send the leftover tester UAT invite this morning.” — **hold** (unsent; no tester/firm names).
10. L0: “Add telemetry.” / “Galaxy finale today.” / “Enable ChatGPT developer mode. Open Secure MCP Tunnel.” / “Switch to gpt-5.6-sol.” / “Enable ChatGPT for Word preview.” — silent.
11. Grok plugin: “Protect the IP. grok plugin install this-skill --trust and PR the marketplace tonight.” — **decline**.
12. Scan Tools: “Protect the IP. Scan Tools this skill from MCP, change it, rescan, and submit tonight.” — **decline**.

Friedberg × Satya (every claimed stack; cannot prove or prevent training):
- F1–F14 unchanged from v0.5.32.
- F15: Claude-plugin OpenAI submit / import-other-agent (above).

Track 3 realtime warning (every claimed stack):
- T1–T14 unchanged from v0.5.32.
- T15: Developer mode / Secure MCP Tunnel L0 (above).

Scorecard and zip recipe: [HITL-LUNCH.md](HITL-LUNCH.md).

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No client-secret corpus ingest. Corpus ticks stay L0. PRIVATE corpus never in the zip / Bot disk. No guarantees. Weekly backup ≠ publish. Leftover drafts stay unsent. Description 1024 chars. Origin 0.5.17–0.5.32 content kept. Vault-myth holds kept. This skill does not watch every tool and does not see the lab train. Consumer terms ≠ NDA. Coding agents leak more than chat. Firm / no-train lane for research review. MCP Scan Tools snapshot is a method paste. Rescan-after-change is another paste. Universal directory is a dual-surface publish. Web install does not deploy hooks. Office add-in is a next-paste. Custom GPT → plugin is dual-surface. Record & Replay / Teach-a-task is demonstration-to-skill. Claude-plugin OpenAI submit is dual-surface (approvals don't transfer). Import-other-agent chats/skills is a next-paste. Grok-export PARTIAL is not a transcript dump.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
