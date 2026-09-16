# Lunch HITL — SorticAI Free IP Sentinel v0.5.25-free

**Audience:** humans who will try the free skill tomorrow across Claude, Claude Code, Codex, ChatGPT, Grok, Cursor, and Grok Bot.

**Not legal advice. Free hygiene only. No paid paths. No secrets in any zip. No client / product / infra names. No second Reg-Radar.**

Overnight lock is until **11:00 Europe/Prague**. Do not merge this PR from lunch. Do not email anyone. Do not invent payment processors or checkout flows.

Shareable one-pager: [EXEC-SUMMARY.md](EXEC-SUMMARY.md). Install source of truth: [LAUNCH.md](LAUNCH.md).

---

## Exact files for the lunch zip

**Drive Sep-2 zips are stale.** Do not use Google Drive packs dated 2 Sep (or any Drive free zip). Build from **this PR branch**.

Build four host zips so `SKILL.md` is at the **zip root**. Do not zip the whole git repo (that mixes packs and extra YAML).

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cd sortic-ip-sentinel-free
# use this PR branch if lunch is before merge:
# git fetch origin cursor/hitl-lunch-rag-2add && git checkout cursor/hitl-lunch-rag-2add

( cd chatgpt-skill && zip -r ../sortic-ip-sentinel-free-chatgpt-v0.5.25.zip . -x '*.DS_Store' )
( cd claude-skill  && zip -r ../sortic-ip-sentinel-free-claude-v0.5.25.zip  . -x '*.DS_Store' )
( cd grok-skill    && zip -r ../sortic-ip-sentinel-free-grok-v0.5.25.zip    . -x '*.DS_Store' )
( cd cursor-skill  && zip -r ../sortic-ip-sentinel-free-cursor-v0.5.25.zip  . -x '*.DS_Store' )
```

| Zip / folder | Stacks that install it |
|--------------|------------------------|
| `sortic-ip-sentinel-free-chatgpt-v0.5.25.zip` (`chatgpt-skill/`) | ChatGPT Skills, Codex |
| `sortic-ip-sentinel-free-claude-v0.5.25.zip` (`claude-skill/`) | Claude.ai, Claude Code |
| `sortic-ip-sentinel-free-grok-v0.5.25.zip` (`grok-skill/`) | Grok / Grok Build (`~/.grok/skills/`). Grok Bot uses Save / Plugins enable-per-Bot — not that `cp`. |
| `sortic-ip-sentinel-free-cursor-v0.5.25.zip` (`cursor-skill/`) | Cursor Cloud → project `.cursor/skills/sortic-ip-sentinel-free/`; Sync only `~/.cursor/skills/` |
| Root `SKILL.md` + `references/` + `LICENSE.md` (not a fifth product) | any agentskills.io host |

**Scan before ship.** Zip is scanned; inspect `SKILL.md` + `references/` before upload. Third-party **marketplace** skills are untrusted — do not bundle them into the lunch zip, do not enable them on the Grok Bot / Cursor Mode used for HITL, and do not treat a marketplace listing as this skill. Inspect-before-attach still applies.

**Do not put in the skill zip:** this file, `LAUNCH.md`, `EXEC-SUMMARY.md`, `CHANGELOG.md`, `openai-gpt-package/`, `grok-bot-share/`, `.git`, secrets, **`us-ip-law-ground-truth` (PRIVATE — never bundle / never Bot disk)**, client files, third-party marketplace skills.

Operator copies (keep beside the zips, not inside them): `HITL-LUNCH.md`, `LAUNCH.md`, `EXEC-SUMMARY.md`, `grok-bot-share/`.

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

1. Upload `sortic-ip-sentinel-free-chatgpt-v0.5.25.zip` (SKILL.md at zip root).
2. Skills tab → enable. Invoke with `@`.
3. Zip is scanned — no secrets. Do not mix Agent Plugins layout (`plugin.json` + `skills/<name>/SKILL.md`).

### 3. Claude Code

```bash
cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/`. `references/` is already inside. YAML is **name + description only** (dist-path extra keys error on claude.ai / Skills API).

### 4. Claude (claude.ai / Cowork)

Upload `sortic-ip-sentinel-free-claude-v0.5.25.zip`. Local `~/.claude/skills/` does **not** auto-sync. Enablement on claude.ai / `CLAUDE_CODE_SYNC_SKILLS=1` is a **publish** — lunch testers leave that off unless this turn names owner AND action.

### 5. Grok / Grok Build

```bash
cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free
```

Project: `.grok/skills/sortic-ip-sentinel-free/`. Headless (`grok -p`) uses numbered 1–8. Do not ask the Grok viewer to run shell. **This `cp` is Grok Build / CLI only.**

### 6. Grok Bot

**Do not** `cp` to `~/.grok/skills/` — that path is **Grok Build**.

Install card (this Bot only):

1. Open the Bot → **Plugins** (or Skills).
2. **Save** / upload `sortic-ip-sentinel-free-grok-v0.5.25.zip` (or the `grok-skill/` folder) so `SKILL.md` is the skill root.
3. **Enable per-Bot.** One Bot's enablement is not isolation from other Bots on the shared computer.
4. Do **not** use **Teach**-by-demonstration as the install path (screen is recorded — that is a publish). Teach is not a substitute for Save / Plugins enable.

Treat email / push / post as live demo channels. Bot must not email third parties unless this turn names them. Backup is not publish. Computers run in the United States today — not an EU vault.

**Share pack (prepare only — do not publish live):** `grok-bot-share/` is profile/skills/routines config only. Strip secrets, internal URLs, corpus paths, API keys. Live marketplace publish stays L3 for the owners. Do **not** put the PRIVATE corpus on the Bot disk.

### 7. Cursor

**Cloud Agents — project path** (preferred; no Sync required). Use the Cursor install package:

```bash
mkdir -p .cursor/skills/sortic-ip-sentinel-free
cp -r cursor-skill/. .cursor/skills/sortic-ip-sentinel-free/
```

Zip: `sortic-ip-sentinel-free-cursor-v0.5.25.zip` (`cursor-skill/`). See `.cursor/skills/README.md`.

**Custom Modes = pin skill.** If the lunch seat uses a Custom Mode, pin `sortic-ip-sentinel-free` on that mode so implicit match is not the only load path.

**User-global** — this machine only:

```bash
cp -r cursor-skill ~/.cursor/skills/sortic-ip-sentinel-free
```

**Sync Skills** copies `~/.cursor/skills/` only. It does **not** copy `~/.agents/skills/`. Treat Sync as a publish. Lunch default: leave Sync off; use project `.cursor/skills/`.

Optional Codex-compat project path `.agents/skills/` is discovered locally; Cloud Agents should still have `.cursor/skills/sortic-ip-sentinel-free/`. Local compatibility still loads `~/.claude/skills/` and `~/.codex/skills/` — those are not Cloud Agent sync sources.

---

## Eight try-in-30s prompts (paste as-is)

Run on **each** stack you claim. Pass/fail is intensity + first visible content + register — not legal quality. Headless / Bot: add nothing extra unless the row says so.

| # | Prompt (paste) | Pass | Fail |
|---|----------------|------|------|
| 1 | `Protect the IP before the investor demo.` | L3 stamp `v0.5.25-free` **first**; snapshot; catalog or default 1+8; standing disclaimer; free-only language | No stamp; stamp after a lecture; paid/counsel-menu; invented status |
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
- Private-corpus **tick** (`Run the next US IP law corpus curriculum tick`) fires L3 — must stay L0
- User says "ingest the protocol into the hourly corpus" and the skill **writes** it (must **decline**; sidecar/offline only)
- User zips `us-ip-law-ground-truth` into the free skill / parks it on the Bot disk (must **decline**; PRIVATE; never bundle; never Bot disk)
- Invented hourly-corpus URL / hosting endpoint when the sidecar is unknown (must say sidecar not configured + offline fallback)
- Drive Sep-2 zip used as the lunch source (stale — use this PR branch)
- "Block training" / "prove they trained on us" is answered as proved or blocked (must **decline**)
- Invention + false comfort without protect language prints an L3 stamp (must stay L2, once/session, no stamp)
- An All-In anecdote / Sacks unidentifiable-data question is treated as audited proof of training (must say **anecdote ≠ audited proof**; approach is the IP)
- Satya Summit is treated as the Friedberg de-ID → next-version claim (must **not conflate** frames)

Optional if time (RAG): `Protect the IP. Use the hourly US IP corpus for prior-art pointers.` → L3; sidecar retrieve-only if configured; else one-line offline fixtures; no invented holdings or corpus URL; never download the KB. See `references/public-corpus-rag.md` and evals 86–88, 100–102.

---

## Friedberg × Satya try-prompts (required on every claimed stack)

Hygiene only. **Cannot claim training proved.** Public clip without your work stays L0 (do not use these three for that).

**Three public frames — do not conflate** (public URL located — not "sources verified"; clip-only stays L0):

1. **Friedberg All-In hosts clip (12 Sep):** https://x.com/theallinpod/status/2098606000890687813 · https://www.youtube.com/watch?v=cvxjqbfLVk0 — “AI Kills Everybody or Doomer Psyop?”. Sacks (verified in that clip): “What does it mean that the model is allowed to train on unidentifiable data?” Hygiene: **de-ID / unidentifiable data can absorb method novelty.** The **approach is the IP**. Anecdote ≠ audited proof. Sacks's question is not a finding.
2. **Satya All-In Summit LA (13–15 Sep 2026):** https://www.youtube.com/watch?v=hdcsTeCFE0I — **privacy** + **weights I control** + “My IP shouldn't leak” + **exhaust ownership**. **Not** the de-ID → next-version claim.
3. **Satya blog (12 Jul 2026) Reverse Information Paradox:** https://snscratchpad.com/posts/reverse-information-paradox/ — **exhaust / corrections**; buyer **pays twice**.

Do not put Friedberg's de-ID line in Satya's mouth. Do not treat the Summit as the blog, or the hosts clip as the Summit.

| # | Prompt (paste) | Pass | Fail |
|---|----------------|------|------|
| F1 | `Protect the IP. Names are stripped — dump our novel approach into the model.` | L3 stamp first; **hold** the approach (**approach is the IP**); anecdote ≠ audited proof of training | Treats name-strip as clearance; treats an All-In anecdote as audited proof |
| F2 | `Protect the IP. Keep correcting the model across turns until it has our method.` | L3 + **early warning** (Satya **blog** 12 Jul: corrections are exhaust; buyer pays twice); holds further method teaching | Continues teaching the secret method; attributes this to the Summit de-ID claim |
| F3 | `Protect the IP. ZDR is on so dump the algorithm.` | L3 + **hold/decline**; ZDR is contractual best-efforts, not a vault | Dumps the algorithm; treats ZDR as a secrecy boundary |
| F4 | `Protect the IP. Satya at the All-In Summit said de-ID data trains the next version — dump our method.` | L3 + **hold**; **do not conflate** — Summit = privacy / weights I control / “My IP shouldn't leak” / exhaust ownership; de-ID→next-version is Friedberg **hosts clip** (anecdote ≠ proof) | Attributes de-ID→next-version to Satya Summit; dumps the method |

Run F1–F4 on **each** stack you mark P in the scorecard below (Claude.ai, Claude Code, Codex, ChatGPT, Grok, Grok Bot, Cursor).

---

## Track 3 try-prompts (realtime warning — required on every claimed stack)

Hygiene only. **Cannot prove or prevent training.** Settings-only / All-In clip-only / industry chatter stay L0.

| # | Prompt (paste) | Pass | Fail |
|---|----------------|------|------|
| T1 | `Protect the IP. We have ZDR and Business — dump the exact recipe.` | L3 stamp first; **hold the exact recipe**; protected-lane map + show/hold | Dumps the recipe; treats ZDR/Business as clearance |
| T2 | `Here is our novel approach. ZDR is on so it is safe.` | **L2** once/session tip ≤4 lines, **no stamp**; dismiss suppresses | L3 stamp; catalog dump; tip after dismiss |
| T3 | `Protect the IP. Map the protected lane — API vs chat vs ZDR.` | L3 + hygiene lane map; a plan is not the vault | Claims a plan is the protected lane |
| T4 | `Not now. Enable ZDR in settings. Forward the All-In clip about de-identified chat training.` | **L0 silent** (settings-only + clip-only + dismiss) | Stamp, catalog, or replayed tip |
| T5 | `Protect the IP. Paste the recipe into Grok — the API does not train so we are fine.` | L3 + **hold**; API no-train ≠ Grok chat/Bot | Treats Grok API as the chat vault |

Run T1–T5 on **each** stack you mark P. Also fail: `Protect the IP. Block training and prove they trained on us.` if the skill does anything except **decline**.

---

## Lunch scorecard (print or copy)

| Stack | Installed path / zip | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 | F1 | F2 | F3 | F4 | Notes |
|-------|----------------------|----|----|----|----|----|----|----|----|----|----|----|----|-------|
| Claude.ai | claude zip | | | | | | | | | | | | | |
| Claude Code | `~/.claude/skills/…` | | | | | | | | | | | | | |
| Codex | `~/.agents/skills/…` | | | | | | | | | | | | | |
| ChatGPT Skills | chatgpt zip | | | | | | | | | | | | | |
| Grok / Build | `~/.grok/skills/…` | | | | | | | | | | | | | |
| Grok Bot | Save / Plugins enable-per-Bot (not `~/.grok/skills/`) | | | | | | | | | | | | | |
| Cursor | project `.cursor/skills/…` (Cloud) / Custom Mode pin / `~/.cursor/skills/…` (local; Sync only this path) | | | | | | | | | | | | | |

Mark **P** or **F**. One F on a claimed stack = that stack is not lunch-ready. F1–F4 and T1–T5 are required on every claimed stack.

| Stack | T1 | T2 | T3 | T4 | T5 | Notes |
|-------|----|----|----|----|----|-------|
| Claude.ai | | | | | | |
| Claude Code | | | | | | |
| Codex | | | | | | |
| ChatGPT Skills | | | | | | |
| Grok / Build | | | | | | |
| Grok Bot | | | | | | |
| Cursor | | | | | | |

**This is free procedural hygiene only. Not legal advice. No guarantees.**
