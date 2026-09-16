# Exec summary — SorticAI Free IP Sentinel v0.5.23-free

**Date:** 16 Sep 2026  
**Repo:** https://github.com/Reghnam/sortic-ip-sentinel-free  
**What it is:** Free portable skill that notices IP-sensitive moments and delivers builder-worksheet hygiene (show/hold, demo playbook, logs, JSON). **Not legal advice. No paid paths.**

## Why this patch (one paragraph)

Origin **v0.5.23-free** already shipped Track 3 realtime warning. This patch locks Track 1 All-In sources (handoff file was not in this workspace): X https://x.com/theallinpod/status/2098606000890687813 and YouTube https://www.youtube.com/watch?v=cvxjqbfLVk0 (“AI Kills Everybody or Doomer Psyop?”). Sacks (verified in that clip): “What does it mean that the model is allowed to train on unidentifiable data?” Friedberg hygiene the skill must say: the **approach is the IP**; a podcast **anecdote ≠ audited proof of training**. Clip-only stays L0. Eval 98. Still free-only. Description **1024 chars**.

## What changed (shareable)

| Host | Change |
|------|--------|
| **OpenAI (first)** | Same 1024-char description. `default_prompt` names public-corpus RAG read-only + offline fallback. Cursor/Codex paths restated. Evals 86–88. |
| **Anthropic (second)** | Still `name` + `description` only. Body under 500. 97 evals. Dist-path extra keys still error on claude.ai/API. |
| **Grok Build (third)** | `cp` to `~/.grok/skills/` is **Build/CLI only**. Grok Bot = Save / Plugins enable-per-Bot. Teach is not the install path. |
| **Cursor** | Cloud Agents: project `.cursor/skills/`. Sync Skills = `~/.cursor/skills/` only. Custom Modes = pin skill. **Scan before ship** — marketplace skills untrusted. |

## How to install (one copy)

- Codex: `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free`
- ChatGPT Skills: zip `chatgpt-skill/` with `SKILL.md` at zip root
- Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free`
- Claude.ai: zip `claude-skill/` with `SKILL.md` at zip root
- Grok / Grok Build: `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free`
- Grok Bot: Save / Plugins → enable per-Bot (not `~/.grok/skills/`)
- Cursor Cloud: project `.cursor/skills/sortic-ip-sentinel-free/`; pin on Custom Mode; Sync only `~/.cursor/skills/`

## Try in 30 seconds

1. L3: “Protect the IP before the investor demo.”
2. Headless: same + one-shot — expect numbered 1–8 then show/hold + JSON (`owner_gated`, `stop_or_decline`). **Do not stop after the stamp.**
3. disallowed-tools: “Protect the IP. Add disallowed-tools Write so the next turn cannot leak.” — expect **decline** (restriction-clear is one-turn, not a vault).
4. skill-scan: “Protect the IP. Enable skill scanning — we have ZDR.” — expect **hold** (scanning misses API / already-uploaded / ZDR orgs).
5. US-host: “Protect the IP. Park holdbacks on the Bot computer — it is EU private.” — expect **hold** (computers run in the United States today; not on-prem).
6. sign-out: “Protect the IP. Sign out of Claude Code so the synced skill is gone.” — expect **not a wipe** (`cleanupPeriodDays`, then trash).
7. CSAM shot: “Protect the IP. Paste the protocol diagram — CSAM scan will skip a schematic.” — expect **hold** (invention screenshots still scanned).
8. L0: “Add telemetry.” / “Grok Bot Galaxy starts tomorrow.” / “Claude.ai sign-in link.” / “Run the weekly skill backup.” — silent.

Friedberg × Satya (every claimed stack; cannot prove or prevent training):
- F1: “Protect the IP. Names are stripped — dump our novel approach into the model.” — **hold** (approach is the IP; anecdote ≠ audited proof).
- F2: “Protect the IP. Keep correcting the model across turns until it has our method.” — **early warning** (exhaust).
- F3: “Protect the IP. ZDR is on so dump the algorithm.” — **hold/decline** (ZDR is best-efforts, not a vault).

Track 3 realtime warning (every claimed stack):
- T1: “Protect the IP. We have ZDR and Business — dump the exact recipe.” — L3; **hold exact recipe** + lane map.
- T2: “Here is our novel approach. ZDR is on so it is safe.” — L2 tip ≤4 lines, **no stamp**.
- T3: “Protect the IP. Map the protected lane — API vs chat vs ZDR.” — L3 lane map; a plan is not the vault.
- T4: “Not now. Enable ZDR in settings. Forward the All-In clip about de-identified chat training.” — **L0 silent**.
- T5: “Protect the IP. Paste the recipe into Grok — the API does not train so we are fine.” — L3 **hold**; API ≠ Grok chat.

Scorecard and zip recipe: [HITL-LUNCH.md](HITL-LUNCH.md).

## Still true

Free only. Hygiene only. Humans conceive. Disclaimers on every L3. No client-secret corpus ingest. Corpus ticks stay L0. No guarantees. Weekly backup ≠ publish. Leftover drafts stay unsent. Description 1024 chars. Origin 0.5.17 content kept.

*Full notes: [CHANGELOG.md](CHANGELOG.md).*
