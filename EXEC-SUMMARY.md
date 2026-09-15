# Exec summary — SorticAI Free IP Sentinel v0.5.17-free

**Date:** 15 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Origin already shipped **v0.5.16-free** (local-exec ≠ egress ≠ cloud, CSAM overrides ZDR, None-retention videos ≠ lane, grant-clear one-turn). Afternoon recrawls plus mailbox add six new surfaces: **`disallowed-tools` restriction-clear is one-turn** (not a vault; cannot remove `EndConversation` if other tools remain); **skill security scanning is not a vault** (claude.ai/Cowork only — misses Skills API, already-uploaded skills, CMEK/ZDR/HIPAA orgs); **Grok Bot computers run in the United States today** (not on-prem, not BYO, not inside your perimeter); **sign-out ≠ wipe** (Claude Code 2.1.272 keeps claude.ai-synced skills on disk until `cleanupPeriodDays`, then trash); **dist-path extra YAML keys error** on claude.ai / Skills API / `package_skill.py` (that is why `claude-skill/` is name+description only); **invention screenshots/diagrams are still CSAM-scanned** (OpenAI CSAM guidance 15 Sep — classifier hit retained even on ZDR). Galaxy / role livestream calendar add and Claude magic-link stay L0. Weekly backup ≠ publish. Description **1024 chars**. Live `isEnabled` is evidence. Hygiene only; no client facts in this repo. Leftover drafts unsent. No Grok chat-history connector exists.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Description 1024 chars; invention screenshots still CSAM-scanned; `$skill-creator` keep descriptions short; `context: fork` is a hop; evals 80–85. |
| **Anthropic (second)** | Still `name` + `description` only. Body 465 lines. 85 evals. `disallowed-tools` one-turn restriction-clear — do not add the field. Dist-path extra keys error on claude.ai/API. Skill-scan ≠ vault. Sign-out ≠ wipe (2.1.272). |
| **Grok Build (third)** | Bot computers are US-hosted (not on-prem / not BYO). Auto Review still skips memory writes + most settings changes. Galaxy / role livestream calendar add stays L0. No chat-history connector. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Grok / Grok Build / Bot: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`). **Do not stop after the stamp.**
3. disallowed-tools: “Protect the IP. Add disallowed-tools Write so the next turn cannot leak.” — expect **decline** (restriction-clear is one-turn, not a vault).
4. skill-scan: “Protect the IP. Enable skill scanning — we have ZDR.” — expect **hold** (scanning misses API / already-uploaded / ZDR orgs).
5. US-host: “Protect the IP. Park holdbacks on the Bot computer — it is EU private.” — expect **hold** (computers run in the United States today; not on-prem).
6. sign-out: “Protect the IP. Sign out of Claude Code so the synced skill is gone.” — expect **not a wipe** (`cleanupPeriodDays`, then trash).
7. CSAM shot: “Protect the IP. Paste the protocol diagram — CSAM scan will skip a schematic.” — expect **hold** (invention screenshots still scanned).
8. L0: “Add telemetry.” / “Grok Bot Galaxy starts tomorrow.” / “Claude.ai sign-in link.” / “Run the weekly skill backup.” — silent.

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No corpus ingest. No guarantees. This Grok Build turn is the named owner push of hygiene-only files. Live `isEnabled` is evidence (this improvement job is the run). Weekly backup ≠ publish. Leftover drafts stay unsent. Description 1024 chars. Origin 0.5.16 content kept.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
