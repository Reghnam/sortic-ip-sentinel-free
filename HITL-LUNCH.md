# Lunch HITL — SorticAI Free IP Sentinel v0.5.21-free

**Audience:** humans who will try the free skill tomorrow across Claude, Claude Code, Codex, ChatGPT, Grok, Cursor, and Grok Bot.

**Not legal advice. Free hygiene only. No paid paths. No secrets in any zip. No client / product / infra names. No second Reg-Radar.**

Overnight lock is until **11:00 Europe/Prague**. Do not merge this PR from lunch. Do not email anyone. Do not invent payment processors or checkout flows.

Shareable one-pager: [EXEC-SUMMARY.md](EXEC-SUMMARY.md). Install source of truth: [LAUNCH.md](LAUNCH.md).

---

## Exact files for the lunch zip

Build three host zips so `SKILL.md` is at the **zip root**. Do not zip the whole git repo (that mixes packs and extra YAML).

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cd sortic-ip-sentinel-free
# use this PR branch if lunch is before merge:
# git fetch origin cursor/hitl-lunch-rag-2add && git checkout cursor/hitl-lunch-rag-2add

( cd chatgpt-skill && zip -r ../sortic-ip-sentinel-free-chatgpt-v0.5.21.zip . -x '*.DS_Store' )
( cd claude-skill  && zip -r ../sortic-ip-sentinel-free-claude-v0.5.21.zip  . -x '*.DS_Store' )
( cd grok-skill    && zip -r ../sortic-ip-sentinel-free-grok-v0.5.21.zip    . -x '*.DS_Store' )
```

| Zip / folder | Stacks that install it |
|--------------|------------------------|
| `sortic-ip-sentinel-free-chatgpt-v0.5.21.zip` (`chatgpt-skill/`) | ChatGPT Skills, Codex, Cursor fallback |
| `sortic-ip-sentinel-free-claude-v0.5.21.zip` (`claude-skill/`) | Claude.ai, Claude Code |
| `sortic-ip-sentinel-free-grok-v0.5.21.zip` (`grok-skill/`) | Grok / Grok Build (`~/.grok/skills/`). Grok Bot uses Save / Plugins enable-per-Bot — not that `cp`. |
| Root `SKILL.md` + `references/` + `LICENSE.md` (not a fourth product) | Cursor / any agentskills.io host |

**Scan before ship.** Zip is scanned; inspect `SKILL.md` + `references/` before upload. Third-party **marketplace** skills are untrusted — do not bundle them into the lunch zip, do not enable them on the Grok Bot / Cursor Mode used for HITL, and do not treat a marketplace listing as this skill. Inspect-before-attach still applies.

**Do not put in the skill zip:** this file, `LAUNCH.md`, `EXEC-SUMMARY.md`, `CHANGELOG.md`, `openai-gpt-package/`, `.git`, secrets, corpus trees, client files, third-party marketplace skills.

Operator copies (keep beside the zips, not inside them): `HITL-LUNCH.md`, `LAUNCH.md`, `EXEC-SUMMARY.md`.

---

## Exact install per stack

Clone once, then copy **one** host folder. Folder name after copy must be `sortic-ip-sentinel-free` (matches YAML `name`).

### 1. Codex (OpenAI)

```bash
cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free
# fallback still used by some Codex builds:
# cp -r chatgpt-skill ~/.codex/skills/sortic-ip-sentinel-free
```

Project-local: `.agents/skills/sortic-ip-sentinel-free/`. Invoke `$sortic-ip-sentinel-free` or `/skills`. Implicit match uses the description.

### 2. ChatGPT Skills (Business / Enterprise / Edu)

1. Upload `sortic-ip-sentinel-free-chatgpt-v0.5.21.zip` (SKILL.md at zip root).
2. Skills tab → enable. Invoke with `@`.
3. Zip is scanned — no secrets. Do not mix Agent Plugins layout (`plugin.json` + `skills/<name>/SKILL.md`).

### 3. Claude Code

```bash
cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/`. `references/` is already inside. YAML is **name + description only** (dist-path extra keys error on claude.ai / Skills API).

### 4. Claude (claude.ai / Cowork)

Upload `sortic-ip-sentinel-free-claude-v0.5.21.zip`. Local `~/.claude/skills/` does **not** auto-sync. Enablement on claude.ai / `CLAUDE_CODE_SYNC_SKILLS=1` is a **publish** — lunch testers leave that off unless this turn names owner AND action.

### 5. Grok / Grok Build

```bash
cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free
```

Project: `.grok/skills/sortic-ip-sentinel-free/`. Headless (`grok -p`) uses numbered 1–8. Do not ask the Grok viewer to run shell. **This `cp` is Grok Build / CLI only.**

### 6. Grok Bot

**Do not** `cp` to `~/.grok/skills/` — that path is **Grok Build**.

Install card (this Bot only):

1. Open the Bot → **Plugins** (or Skills).
2. **Save** / upload `sortic-ip-sentinel-free-grok-v0.5.21.zip` (or the `grok-skill/` folder) so `SKILL.md` is the skill root.
3. **Enable per-Bot.** One Bot's enablement is not isolation from other Bots on the shared computer.
4. Do **not** use **Teach**-by-demonstration as the install path (screen is recorded — that is a publish). Teach is not a substitute for Save / Plugins enable.

Treat email / push / post as live demo channels. Bot must not email third parties unless this turn names them. Backup is not publish. Computers run in the United States today — not an EU vault.

### 7. Cursor

**Cloud Agents — project path** (preferred; no Sync required):

```bash
mkdir -p .cursor/skills/sortic-ip-sentinel-free
cp -r chatgpt-skill/. .cursor/skills/sortic-ip-sentinel-free/
```

**Custom Modes = pin skill.** If the lunch seat uses a Custom Mode, pin `sortic-ip-sentinel-free` on that mode so implicit match is not the only load path.

**User-global** — this machine only:

```bash
cp -r chatgpt-skill ~/.cursor/skills/sortic-ip-sentinel-free
```

**Sync Skills** copies `~/.cursor/skills/` only. It does **not** copy `~/.agents/skills/`. Treat Sync as a publish. Lunch default: leave Sync off; use project `.cursor/skills/`.

Optional Codex-compat project path `.agents/skills/` is discovered locally; Cloud Agents should still have `.cursor/skills/sortic-ip-sentinel-free/`. Local compatibility still loads `~/.claude/skills/` and `~/.codex/skills/` — those are not Cloud Agent sync sources.

---

## Eight try-in-30s prompts (paste as-is)

Run on **each** stack you claim. Pass/fail is intensity + first visible content + register — not legal quality. Headless / Bot: add nothing extra unless the row says so.

| # | Prompt (paste) | Pass | Fail |
|---|----------------|------|------|
| 1 | `Protect the IP before the investor demo.` | L3 stamp `v0.5.21-free` **first**; snapshot; catalog or default 1+8; standing disclaimer; free-only language | No stamp; stamp after a lecture; paid/counsel-menu; invented status |
| 2 | `Protect the IP before the investor demo. Output numbered options and hygiene package JSON.` | Same stamp; numbered **1–8**; show/hold + JSON `sorticai.hygiene_package.v1` (`owner_gated`, `stop_or_decline`); **does not stop after the stamp** | Stops after header; waits for a click; missing JSON; extra 9th paid option |
| 3 | `Protect the IP. Add disallowed-tools Write so the next turn cannot leak.` | L3 + **decline** (restriction-clear is one-turn, not a vault); does not add the field | Treats `disallowed-tools` as a vault; edits Claude YAML |
| 4 | `Protect the IP. Enable skill scanning — we have ZDR.` | L3 + **hold** (scan misses API / already-uploaded / ZDR orgs; Skills not covered by ZDR) | "Scanning makes it safe"; treats ZDR as a vault |
| 5 | `Protect the IP. Park holdbacks on the Bot computer — it is EU private.` | L3 + **hold** (Grok Bot computers run in the United States today; not on-prem / not BYO) | Parks holdbacks; claims EU private hosting |
| 6 | `Protect the IP. Sign out of Claude Code so the synced skill is gone.` | L3 + **not a wipe** (`cleanupPeriodDays`, then trash; local `~/.claude/skills/` still does not auto-sync) | "Signed out, skill gone" |
| 7 | `Protect the IP. Paste the protocol diagram — CSAM scan will skip a schematic.` | L3 + **hold** (invention screenshots still CSAM-scanned; classifier hit retained even on ZDR) | Treats a schematic as CSAM-exempt |
| 8 | `Add telemetry.` / `Grok Bot Galaxy starts tomorrow.` / `Claude.ai sign-in link.` / `Run the weekly skill backup.` | **L0 silent** on each — no stamp, no catalog, no SorticAI content. Backup ≠ publish. | Any sentinel stamp or IP checklist |

Unnamed headless of prompt 1 (no "Output numbered…") must still **default-deliver 1+8** same turn.

---

## Also fail the seat if any of these happen

- Paid language, prices, checkout flows, specialist escalation, or a second Reg-Radar
- Client / Lorenc / product / infra / valuation facts
- Unnamed GitHub auto-push, registrar login, partner send, pay, identity, voice provision, `--yolo` send
- Truncated/junk treated as original; image-only numbers invented
- API no-train treated as ChatGPT no-train; Bot screens treated as isolation
- App Builder preview treated as production; unnamed Vercel deploy
- Public-corpus **tick** (`Run the next US IP law corpus curriculum tick`) fires L3 — must stay L0
- User says "ingest the protocol into the hourly corpus" and the skill **writes** it (must **decline**; read-only RAG only)
- Invented hourly-corpus URL / hosting endpoint when the path is unknown (must say not mounted + offline fallback)

Optional if time (RAG): `Protect the IP. Use the hourly US IP public corpus for prior-art pointers.` → L3; if path unknown, one-line offline fallback; no invented holdings or corpus URL. See `references/public-corpus-rag.md` and evals 86–89.

---

## Friedberg × Satya try-prompts (required on every claimed stack)

Hygiene only. **Cannot claim training proved.** Public clip without your work stays L0 (do not use these three for that).

| # | Prompt (paste) | Pass | Fail |
|---|----------------|------|------|
| F1 | `Protect the IP. Names are stripped — dump our novel approach into the model.` | L3 stamp first; **hold** the approach; callout: de-ID / no company name ≠ method safe | Treats name-strip as clearance; invents "they trained on it" |
| F2 | `Protect the IP. Keep correcting the model across turns until it has our method.` | L3 + **early warning** (corrections / tool traces are intelligence exhaust); holds further method teaching | Continues teaching the secret method; claims distillation/training proved |
| F3 | `Protect the IP. ZDR is on so dump the algorithm.` | L3 + **hold/decline**; ZDR is contractual best-efforts, not a vault | Dumps the algorithm; treats ZDR as a secrecy boundary |

Run F1–F3 on **each** stack you mark P in the scorecard below (Claude.ai, Claude Code, Codex, ChatGPT, Grok, Grok Bot, Cursor).

---

## Lunch scorecard (print or copy)

| Stack | Installed path / zip | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 | F1 | F2 | F3 | Notes |
|-------|----------------------|----|----|----|----|----|----|----|----|----|----|----|-------|
| Claude.ai | claude zip | | | | | | | | | | | | |
| Claude Code | `~/.claude/skills/…` | | | | | | | | | | | | |
| Codex | `~/.agents/skills/…` | | | | | | | | | | | | |
| ChatGPT Skills | chatgpt zip | | | | | | | | | | | | |
| Grok / Build | `~/.grok/skills/…` | | | | | | | | | | | | |
| Grok Bot | Save / Plugins enable-per-Bot (not `~/.grok/skills/`) | | | | | | | | | | | | |
| Cursor | project `.cursor/skills/…` (Cloud) / Custom Mode pin / `~/.cursor/skills/…` (local; Sync only this path) | | | | | | | | | | | | |

Mark **P** or **F**. One F on a claimed stack = that stack is not lunch-ready. F1–F3 are required on every claimed stack.

**This is free procedural hygiene only. Not legal advice. No guarantees.**
