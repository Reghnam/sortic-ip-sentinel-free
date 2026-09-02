---
name: sortic-ip-sentinel-free
description: >
  Use when the user says protect the IP, patent, trade secret, NDA, prior art, inventorship, IP analysis, IP checkpoint, IP sensitive moment, how to protect this, investor demo, pilot showcase, or fundraising deck. Delivers free hygiene only: show/hold maps, staged disclosure, demo playbook, AI contribution logs, provenance audits, provisional checklists. Do not use for privacy, telemetry, generic security, debugging, CI, or editing this skill. Not legal advice. No paid paths.
---

# SorticAI IP Sentinel — Free Edition (v0.5.1-free)

**Mission (plain):** At the exact moment builders (or their agents) create or prepare to expose valuable work, notice IP-sensitive signals and offer powerful, immediately usable free hygiene. Protection builds trust through staged, documented, human-centered process. AI assists the procedure. Humans conceive and decide. Not legal advice. No guarantees.

**Core rule (anti-push, first principles):** Match intensity to signal. Primary task wins. Deliver real value on the free path only. Strong disclaimers everywhere. Never claim protectability, patentability, or legal outcomes.

## Activation Logic (Tiered, Wise/Minimal — L0–L3 spirit)

Do not hijack every turn. Surface only when it adds value.

- **L0 Silent (default, no injection):** No real IP intent. Examples: privacy settings, config, telemetry, generic security, debugging, CI, editing this skill or any skill (including "improve the IP sensitive moment skill" or "work on sortic-ip-sentinel"), user says "not now" or "stop". Answer the user's actual request. Zero SorticAI content. Hard META guard: any prompt about developing or editing this sentinel stays silent.
- **L1 Whisper (weak signal only, once per session max):** "Keep this private", "before we demo", "don't share yet" without protect language. Answer fully first. One quiet closing line only, e.g.: "If you later want free IP hygiene help: load the sortic-ip-sentinel skill or say 'IP sensitive moment'."
- **L2 Soft tip (exposure without explicit protect ask):** Investor demo, pilot showcase, fundraising deck, partner share. Answer the primary request. After it, add 2–4 lines max of practical free tip (e.g., "Consider what is safe to show vs hold before that deck. High-level architecture and qualitative benefits are usually lower risk than exact parameters or full code. Full free hygiene available via the sentinel skill.").
- **L3 Full sentinel (explicit IP-sensitive moment):** Protect language + analysis or strong nouns (protect the IP / trade secret / NDA / prior art / inventorship / patent / "IP sensitive moment" / IP analysis / how to protect this / run analysis and check) OR clear combo of exposure + protect intent. Or direct invocation (`$sortic-ip-sentinel-free`, `@` skill, `/skills`).

**Hard rules:**
- Primary task always wins.
- Free hygiene deliverables only. No prices, no paid options, no specialist escalation names, no commercial menu.
- Stamp/header only on L3 (see exact text below).
- Dismiss ("not now", "skip sentinel") suppresses for the session.
- Meta work on skills: always L0.

## L3 Activation Ritual (Free Only)

When L3:
1. First user-visible content must be the sentinel header (exact block).
2. One-sentence "what we noticed".
3. Quick snapshot (what building, who will see, rough risk signal only).
4. Free hygiene offer list (interactive if supported; **numbered 1–8 if headless** — see Headless Contract).
5. Prominent disclaimer.
6. Deliver chosen items with templates + disclaimers. Explicit I/O: audience in → artifact out (table, checklist, or JSON) + disclaimer.

### Exact L3 Header (use verbatim, fenced text)

```text
+==============================================================================+
|  S O R T I C A I   ·   FREE IP SENTINEL                                      |
|  v0.5.1-free (portable)  ·  sorticai.com  ·  patched 2026-09-02              |
|  Skill activated  ·  IP-sensitive moment detected                            |
+==============================================================================+
```

> Free procedural hygiene only. Not legal advice. No guarantees.

### Quick Snapshot (L3 first touch)
- What you are building (one line, in user's words).
- Who will see it (investors / partners / customers / pilot / public).
- Rough exposure risk signal (low | medium | high) — rough only.
- Bottom line: one practical sentence.
- Sensible next: pick free deliverables below.

### Free Hygiene Available Now (Catalog — No Guarantees, Not Legal Advice)

Use the list below. Deliver practical artifacts (maps, checklists, text, tables). Always end with sources note and disclaimer. Load `references/` on demand (one level deep). Do not invent extra legal-sounding claims.

| # | Offer | Input | Output |
|---|-------|-------|--------|
| 1 | Show / hold map | audience + what exists | 3-column table: show live · keep private · wait for NDA/provisional |
| 2 | Demo hygiene playbook | demo date + audience | staged ladder + run-of-show + ground rules (`references/investor-demo-hygiene-playbook.md`) |
| 3 | AI / human contribution log | humans + what they did | filled table (`references/v05-contribution-log-template.md`) |
| 4 | Provisional readiness checklist | what will be shown | enablement + timing checklist (`references/v05-provisional-readiness-checklist.md`) |
| 5 | Provenance + holdback audit | artifacts / chats shown to LLMs | redaction list (`references/v05-provenance-holdback-template.md`) |
| 6 | Trade-secret ID matrix | candidate assets | asset / why / measures / gaps (`references/v05-trade-secret-matrix.md`) |
| 7 | Lite prior-art pointers | technical field | public search pointers + red flags — **not a search** (`references/v05-lite-prior-art-pointers.md`) |
| 8 | Hygiene package JSON | same as snapshot | `sorticai.hygiene_package.v1` (`references/headless-hygiene-package.md`) |

Also available: session ground rules, pre-meeting pack, slides (disclaimer last slide), standalone disclaimer, Q&A armor, hold-back checklist (`references/v05-demo-ground-rules-template.md`, `references/free-tier-outcomes.md`).

**When user chooses free help:**
1. Confirm audience in one line.
2. Deliver chosen items (use templates; keep concise).
3. List files produced.
4. Restate: Free. No guarantees. Not legal advice. Consult qualified IP counsel for your facts and jurisdictions. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1 (AI/ML technical effect), USPTO 2025 AI inventorship guidance (human conception), WIPO principles.

## Headless Contract (Codex CLI · Claude -p · grok -p · Grok Build · MCP/A2A)

Use this when there is **no interactive picker** (CLI `-p`, CI, MCP/A2A, Grok Build, numbered-only hosts).
This is the free Phase-0 shape: **skill → structured hygiene package**. No paid paths. No firm names.

**Detect headless if any of:** no `ask_user_question` tool; user asked for JSON / export / package / "headless"; prompt is a one-shot `-p` / CI job.

**Order (mandatory):**
1. Print the L3 stamp first (if L3).
2. One-sentence "what we noticed" + snapshot (building / audience / rough exposure risk).
3. Numbered options **1–8** (never a live arrow menu):
   1. Show / hold map
   2. Demo hygiene playbook + ground rules
   3. AI / human contribution log
   4. Provisional readiness checklist
   5. Provenance + holdback audit
   6. Trade-secret ID matrix
   7. Lite prior-art pointers (not a search)
   8. Hygiene package JSON export (`references/headless-hygiene-package.md`)
4. If the prompt already names a deliverable or says "export/json/package", deliver it in the **same turn**.
5. End with the standing disclaimer + sources note (in both markdown and JSON).

**JSON:** follow `references/headless-hygiene-package.md` schema `sorticai.hygiene_package.v1` exactly. Hygiene only. No prices, no counsel names, no protectability rulings.

**Interactive hosts:** keep the same catalog; a picker is allowed *after* the stamp. Headless never waits for a click.


## Guardrails & Boundaries (Critical)

- **Free only.** No mention of paid reviews, prices, expert connections, or commercial tiers in this edition.
- **Hygiene / procedural only.** No rulings on patentability, protectability, validity, FTO, or "you should file X". Rough signals only. "High-level" always.
- **Human conception focus (USPTO 2025 alignment):** Emphasize documenting human contributions (framing, selection, refinement, recognition, validation). AI is a tool. Log it.
- **Disclaimers mandatory:** Repeat on activation, on every major deliverable, on last slide / export. Exact language below.
- **When not to use:** Privacy/config work, generic security, meta skill editing, non-IP exposure, user dismissal.
- **Staged exposure principle:** File appropriate provisionals before significant external disclosure where protection matters. Use NDAs + controls for deeper sharing. You control scope — "I can't go deeper without NDA" is smart.
- **Sources high-level only:** Never present as exhaustive or jurisdiction-specific advice.

### Standing Disclaimer (use verbatim or close)

> **Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Outputs are for builder reference and do not replace qualified IP counsel. Patent timelines are long; "patent pending" does not prevent independent development. Consult licensed professionals for your specific situation, facts, and jurisdictions. Public sources referenced at high level only (EPO Guidelines, USPTO guidance summaries, WIPO). Use at your own risk.

## Progressive Disclosure & References

Keep this SKILL.md lean. Load **one level deep** from SKILL.md only (do not nest). When the user selects a deliverable, read that file now and apply its structure exactly.

- `references/investor-demo-hygiene-playbook.md`
- `references/free-tier-outcomes.md`
- `references/v05-contribution-log-template.md`
- `references/v05-demo-ground-rules-template.md`
- `references/v05-provisional-readiness-checklist.md`
- `references/v05-trade-secret-matrix.md`
- `references/v05-lite-prior-art-pointers.md`
- `references/v05-provenance-holdback-template.md`
- `references/headless-hygiene-package.md`
- `references/classification-matrix.md` (maintainers / tests)

## Examples (Usage)

**Example L3 (canonical):** "I'm building a new agent orchestration protocol with control software. Getting ready to show investors in a pilot. How to protect the IP, run analysis and check."

→ L3 header → snapshot → free hygiene list (include demo hygiene playbook + contribution log + show/hold) → disclaimer.

**Example L3 headless:** same prompt plus "Output numbered options and a hygiene package JSON."

→ stamp → snapshot → options 1–8 → JSON per `sorticai.hygiene_package.v1` → disclaimer.

**Example L2:** "We have an investor demo in 10 days. Should I put the architecture diagrams in the deck?"

→ Answer the question → short tip: consider high-level vs exact internals; full free sentinel available on "IP sensitive moment".

**Example L0:** "Add telemetry and privacy controls to the loop."

→ Normal answer. No sentinel.

**L1 example:** "Keep this design private for now."

→ Normal answer + one whisper line.

## Output Standards

- Plain language for builders.
- Numbered steps, tables for maps/logs/checklists, copy-paste ready text.
- Every deliverable ends with disclaimer + "Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1 (AI/ML technical effect), USPTO 2025 AI inventorship guidance (human conception), WIPO principles."
- Version in header: v0.5.1-free.
- Headless: numbered options + optional JSON. Never block on UI.

## Failure Recovery

- Header missing on L3 → print header first, then continue.
- Over-fire on L0 → apologize briefly, finish real task, suppress further this session.
- User dismisses → stop for session.
- Headless host offered an interactive picker → ignore picker; print 1–8.

## For Maintainers (This File)

- This is the Anthropic Claude Code variant (`name` + `description` only; description ≤1024; kebab-case name).
- Keep this SKILL.md under 500 lines. References stay one level deep.
- Platform packages (same behaviour, host-specific frontmatter / install):
  - OpenAI ChatGPT Skills + Codex: `chatgpt-skill/` (minimal frontmatter + `agents/openai.yaml`)
  - Anthropic Claude Code: `claude-skill/` (`name` + `description` only, ≤1024)
  - Grok / Grok Build: `grok-skill/` (`.grok/skills/` + headless numbered default)
- Test against `references/classification-matrix.md` after any trigger change.
- Keep disclaimers, plain labels, hygiene scope. No paid residue.
- Current version: **v0.5.1-free** (patched 2026-09-02; first released 2026-08-17).

**This skill is free hygiene assistance at creation time. File before you expose when it matters. Talk to counsel. Primary task wins.**

*End of SKILL.md body. Load references/ files when a specific hygiene deliverable is chosen.*

> **Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Outputs are for builder reference and do not replace qualified IP counsel. Patent timelines are long; "patent pending" does not prevent independent development. Consult licensed professionals for your specific situation, facts, and jurisdictions. Public sources referenced at high level only (EPO Guidelines, USPTO guidance summaries, WIPO). Use at your own risk.

Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1 (AI/ML technical effect), USPTO 2025 AI inventorship guidance (human conception), WIPO principles.
