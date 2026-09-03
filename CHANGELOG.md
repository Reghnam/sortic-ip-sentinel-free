# Changelog — SorticAI Free IP Sentinel

All notable changes to the portable free edition. Hygiene only. Not legal advice.

## [0.5.2-free] — 2026-09-03

Patched from: emails (david@vmcorp.cz, 17 Aug–3 Sep 2026) including Task Extractor 2 Sep (this job), Kristína Chytrá counsel comments 2 Sep 12:48 UTC (Reg-Radar writing, applied as **hygiene language** only), LangChain Deep Agents v0.7 (26 Aug), OpenAI ChatGPT Skills / Codex docs (learn.chatgpt.com/docs/build-skills, crawled 2026-09-01), Anthropic Agent Skills best-practices checklist (platform.claude.com, crawled 2026-09-02), agentskills.io specification (name/description constraints; `compatibility` is env-only), Microsoft Agent Framework skills (25 Aug), Headless Agent topics automation prompt, Velvethy field note *The description is the trigger*, and this Grok Build run. **No Grok chat-history connector exists**; Grok-chat insights are from live automations (this job + adjacent 08:10 IP Radar / 08:40 SKILL.md best-practices schedules), `grok -p` / Grok Build headless contract, and X posts 21 Aug–2 Sep 2026 on skills.

### OpenAI (first)

- Description still front-loaded; added headless one-shot / hygiene-JSON trigger words (595 chars, under Codex 8k / 2% list truncation and Anthropic 1024).
- `agents/openai.yaml`: `default_prompt` now names numbered options + default-deliver 1+8; `short_description` says builder worksheet. Implicit invocation stays on. **No MCP `dependencies.tools`** — core is self-contained (ChatGPT Skills schema allows MCP tools; we do not need them).
- Headless unnamed one-shot no longer stalls: print 1–8 then **default-deliver show/hold + JSON** same turn (Codex CLI `-p`).
- Zip/install paths unchanged: `~/.agents/skills`, `.agents/skills`, `~/.codex/skills`, `/etc/codex/skills`; ChatGPT `@` vs Codex `$` / `/skills`.

### Anthropic (second)

- `claude-skill/` now **bundles `references/`** (was a second `cp` that headless installs skipped). One folder = runnable skill.
- Description-as-trigger tests: slogan "Helps with AI topics" must stay L0 (Anthropic: description is the match rule, not a marketplace card).
- Default option on unnamed headless (Anthropic: provide a default; do not offer a picker and wait).
- SKILL.md body still well under 500-line guidance (~230 lines). References one level deep. YAML still **only** `name` + `description`.

### Grok Build (third)

- `grok-skill/` now **bundles `references/`** — Grok Build / `~/.grok/skills` copy is complete; no second-step `cp`.
- Headless default 1+8 is the Grok Build / `grok -p` path (viewer cannot run a TUI picker; never ask the viewer to run shell).
- JSON `sorticai.hygiene_package.v1` adds `output_register: procedural_builder_worksheet` and `not_for_third_party: true`.

### Shared

- New `references/output-language-hygiene.md` from counsel writing notes (2 Sep): procedural verbs, no invented deadlines, no fake "verified sources", one idea per sentence, builder-worksheet banner. **Not** a paid review path; **not** a client memo.
- Classification matrix: L0-04 slogan-miss, L3-H2 unnamed default, L3-LANG writing register.
- Custom GPT `instructions.txt` bumped to v0.5.2-free (stamp, register, default 1+8).
- Stamp: `v0.5.2-free` / patched 2026-09-03. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy.

## [0.5.1-free] — 2026-09-02

Patched from emails (david@vmcorp.cz, 17 Aug–2 Sep 2026), SteerCo v2.4 / Future Solution Architecture, v05-suggestions, OpenAI ChatGPT Skills + Codex docs (2026-09), Anthropic Agent Skills best practices, and Grok Build / headless agent contracts. No Grok chat-history connector was available; Grok insights come from the 2026-09-02 `chatgpt-skill` commit, the demo headless `grok -p` pattern, and Grok Build skill layout.

### OpenAI (first)

- Tightened `description` (479 chars): trigger words front-loaded; explicit do-not-use; survives Codex 8k / 2% list truncation.
- `agents/openai.yaml`: `default_prompt`, `brand_color`, implicit invocation kept on (L2/L3 auto-detect).
- Documented install paths: `~/.agents/skills`, `.agents/skills`, `~/.codex/skills`, `/etc/codex/skills`. ChatGPT `@` vs Codex `$` / `/skills`.
- Headless contract for Codex CLI one-shots: numbered 1–8 + `sorticai.hygiene_package.v1` JSON (Skill-gateway-ready hygiene package; **no paid residue**).
- Imperative deliverable I/O table (input → artifact).
- Custom GPT notes point at the ChatGPT Skills path as primary; GPT remains a fallback.

### Anthropic (second)

- New `claude-skill/` package: YAML is **only** `name` + `description` (Anthropic required fields; name kebab-case ≤64; description ≤1024, no XML).
- Progressive disclosure: references one level deep; SKILL.md well under 500-line guidance.
- Install: `~/.claude/skills/sortic-ip-sentinel-free/` and project `.claude/skills/`.

### Grok Build (third)

- New `grok-skill/` package: `.grok/skills/` (Grok Build project) and `~/.grok/skills/` (user).
- Headless is the **default** on Grok Build / `grok -p` (numbered options; never block on a picker; never ask the viewer to run shell).
- Hygiene JSON schema aligned with SorticAI Phase 0 "skill → structured package" without commercial menu.

### Shared

- Added templates that were catalogued but missing as files: provisional checklist, trade-secret matrix, lite prior-art pointers, provenance/holdback.
- Added `references/classification-matrix.md` (L0–L3 test prompts).
- Added this CHANGELOG. README compatibility matrix.
- Stamp: `v0.5.1-free` / patched 2026-09-02. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy.

## [0.5-free] — 2026-08-17

- Initial public portable edition: L0–L3 activation, free hygiene catalog, ChatGPT-stripped variant (2026-09-02 morning), Custom GPT package, demo playbook, contribution log, ground rules.
