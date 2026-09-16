# Exec summary — SorticAI Free IP Sentinel v0.5.19-free

**Date:** 16 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Origin **v0.5.18-free** already shipped lunch HITL + read-only public-corpus RAG. This patch absorbs deeper SKILL-surface research: **Cursor Cloud Agents** need project `.cursor/skills/sortic-ip-sentinel-free/` and/or `.agents/skills/` **or** Sync Skills of `~/.cursor/skills/` only (Sync does **not** copy `~/.agents/skills/`); **Grok `allowed-tools` does not grant or restrict** (keep Anthropic one-turn hygiene; Claude YAML stays name+description only); RAG stays interface + offline fallback — **do not invent a corpus URL**. Still free-only. No secrets. No second Reg-Radar. Lunch sheet: `HITL-LUNCH.md`. Description **1024 chars**.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Same 1024-char description. `default_prompt` names public-corpus RAG read-only + offline fallback. Cursor/Codex paths restated. Evals 86–88. |
| **Anthropic (second)** | Still `name` + `description` only. Body under 500. 88 evals. Dist-path extra keys still error on claude.ai/API. |
| **Grok Build (third)** | Same grok-skill body as root. Bot computers still US-hosted. Viewer still must not be asked to run shell. |
| **Cursor** | Project `.cursor/skills/sortic-ip-sentinel-free/` and/or `.agents/skills/`. Sync Skills = `~/.cursor/skills/` only, not `~/.agents/skills/`. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Claude.ai: zip `claude-skill/` with `SKILL.md` at zip root
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`
- Cursor: `cp -r chatgpt-skill ~/.cursor/skills/sortic-ip-sentinel-free` (or root `SKILL.md` + `references/`)

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`). **Do not stop after the stamp.**
3. disallowed-tools: “Protect the IP. Add disallowed-tools Write so the next turn cannot leak.” — expect **decline** (restriction-clear is one-turn, not a vault).
4. skill-scan: “Protect the IP. Enable skill scanning — we have ZDR.” — expect **hold** (scanning misses API / already-uploaded / ZDR orgs).
5. US-host: “Protect the IP. Park holdbacks on the Bot computer — it is EU private.” — expect **hold** (computers run in the United States today; not on-prem).
6. sign-out: “Protect the IP. Sign out of Claude Code so the synced skill is gone.” — expect **not a wipe** (`cleanupPeriodDays`, then trash).
7. CSAM shot: “Protect the IP. Paste the protocol diagram — CSAM scan will skip a schematic.” — expect **hold** (invention screenshots still scanned).
8. L0: “Add telemetry.” / “Grok Bot Galaxy starts tomorrow.” / “Claude.ai sign-in link.” / “Run the weekly skill backup.” — silent.

Scorecard and zip recipe: [HITL-LUNCH.md](HITL-LUNCH.md).

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No client-secret corpus ingest. Corpus ticks stay L0. No guarantees. Weekly backup ≠ publish. Leftover drafts stay unsent. Description 1024 chars. Origin 0.5.17 content kept.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
