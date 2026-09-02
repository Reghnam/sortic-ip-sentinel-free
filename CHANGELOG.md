# Changelog — SorticAI Free IP Sentinel

All notable changes to the portable free edition. Hygiene only. Not legal advice.

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
