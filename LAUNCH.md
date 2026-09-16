# LAUNCH: SorticAI Free IP Sentinel v0.5.22-free

**Status**: Public on GitHub. v0.5.22-free patched 2026-09-16 (Track 3 realtime warning: L2 false-comfort tip, L3 hold-recipe + lane map, L0 settings/clip/chatter; decline block/prove training; evals 93–97; origin 0.5.21 install cards + F1–F3 kept). All files sanitized for free-only use. Strong disclaimers included.

Repo: https://github.com/Reghnam/sortic-ip-sentinel-free

Shareable one-pager: [EXEC-SUMMARY.md](EXEC-SUMMARY.md). Lunch try sheet: [HITL-LUNCH.md](HITL-LUNCH.md).

## 1. OpenAI (primary distribution)

**Codex CLI / IDE**
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free
# fallback path still used by some Codex builds:
# cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.codex/skills/sortic-ip-sentinel-free
```
Project-local: copy to `.agents/skills/sortic-ip-sentinel-free`. Invoke with `$` or `/skills`. Implicit match uses the description.

**ChatGPT Skills (Business / Enterprise / Edu)**
1. Download ZIP of `chatgpt-skill/` (or clone and zip that folder so `SKILL.md` is at the zip root).
2. Skills tab → upload. Invoke with `@`. Zip is scanned — no secrets.

**Custom GPT (fallback, hosted sharing)**
See `openai-gpt-package/HOW_TO_CREATE_IN_OPENAI.md`.

## 2. Anthropic Claude Code

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/claude-skill ~/.claude/skills/sortic-ip-sentinel-free
```

Project-local: `.claude/skills/sortic-ip-sentinel-free/`. `references/` is already inside that folder.

**Claude.ai / Cowork:** zip `claude-skill/` with `SKILL.md` at the zip root. Local `~/.claude/skills/` still does not auto-sync. Enablement / `CLAUDE_CODE_SYNC_SKILLS=1` is a publish.

## 3. Grok / Grok Build

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/grok-skill ~/.grok/skills/sortic-ip-sentinel-free
```

Grok Build / project: `.grok/skills/sortic-ip-sentinel-free/`. Headless (`grok -p`) uses numbered options + optional JSON. Do not ask the Grok viewer to run shell commands. **This `cp` is Grok Build / CLI — not Grok Bot.**

**Grok Bot:** Save / Plugins → enable `sortic-ip-sentinel-free` **per Bot**. Do not `cp` to `~/.grok/skills/`. Do not use Teach-by-demonstration as the install path (publish). Bot must not email third parties unless this turn names them. Backup is not publish.

## 4. Cursor

**Cloud Agents — project `.cursor/skills/`:**

```bash
mkdir -p .cursor/skills/sortic-ip-sentinel-free
cp -r chatgpt-skill/. .cursor/skills/sortic-ip-sentinel-free/
```

**Custom Modes = pin skill.** Pin `sortic-ip-sentinel-free` on the lunch Custom Mode.

**User-global:** `cp -r chatgpt-skill ~/.cursor/skills/sortic-ip-sentinel-free`

**Sync Skills** copies `~/.cursor/skills/` only — not `~/.agents/skills/`. Treat Sync as a publish; lunch default off.

**Scan before ship.** Third-party marketplace skills are untrusted — inspect before attach; do not bundle them into the lunch zip.

Root `SKILL.md` + `references/` is the agentskills.io canonical pack (same behaviour, rich frontmatter).

## 5. Verification Checklist

- [ ] L3 triggers ("protect the IP", "IP sensitive moment", "Bot will email the deck — protect the IP")
- [ ] L0 silence on privacy/config/meta work, US IP corpus ticks, workspace renewal, weekly backup, livestream attend
- [ ] Headless: stamp → numbered 1–8 → JSON schema `sorticai.hygiene_package.v1` (includes `agent_exposure`, `owner_gated`)
- [ ] Unnamed headless default-delivers 1+8 same turn
- [ ] Disclaimers appear on all outputs
- [ ] All deliverables are free-only (no paid language)
- [ ] Evals in `references/evals.md` still pass (now 97: 90–92 Friedberg × Satya kept; 93–97 false-comfort L3/L2, lane map, spam guard, Grok API≠chat)
- [ ] Unnamed GitHub auto-push / registrar login / partner send / pay / identity / voice provision / yolo-send → decline
- [ ] Backup ≠ publish; truncated/junk/placeholder files are not originals; image-only ≠ numbered facts
- [ ] Bot share / marketplace clone is a demo channel; callable hops hold internals
- [ ] API no-train is not treated as ChatGPT no-train; Skills execution is not treated as ZDR-covered
- [ ] Bot screens are not treated as isolation; Bot-to-Bot DM is a hop
- [ ] Astra define-completion: do not stop after the L3 stamp; do not pad extra refuse language
- [ ] App Builder live preview is a demo; unnamed Vercel deploy is declined
- [ ] claude.ai enablement / CLAUDE_CODE_SYNC_SKILLS=1 is a publish; local ~/.claude/skills/ still does not auto-sync
- [ ] disallowed-tools / skill-scan / US-host are not vaults; sign-out is not a wipe; invention screenshots still CSAM-scanned
- [ ] Public-corpus RAG is read-only; unknown path → offline fallback; ingest of client work is declined; ticks stay L0
- [ ] Cursor Cloud Agents use project `.cursor/skills/` / `.agents/skills/` or Sync of `~/.cursor/skills/` only (not `~/.agents/skills/`)
- [ ] Lunch HITL eight prompts plus F1–F3 and T1–T5 (Track 3 realtime warning) in HITL-LUNCH.md pass on each claimed stack
- [ ] Grok Bot install is Save / Plugins enable-per-Bot — not `cp ~/.grok/skills/` (Build)
- [ ] Scan before ship: third-party marketplace skills untrusted; inspect-before-attach

**This is free procedural hygiene only. Not legal advice. No guarantees.**
