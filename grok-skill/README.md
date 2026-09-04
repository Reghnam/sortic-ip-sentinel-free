# SorticAI Free IP Sentinel — Grok / Grok Build / Grok Bot (v0.5.3-free)

Grok-native package. Headless numbered options are the **default** (Grok Build viewers cannot run a TUI picker; `grok -p` is one-shot; **Grok Bot is unattended**). Unnamed L3 **default-delivers 1 (show/hold) + 8 (JSON)** so an unattended run is not blank.

`references/` is **bundled**. One copy is a complete skill.

Frontmatter extras vs other hosts: `when-to-use`, `argument-hint` (slash autocomplete), `disable-model-invocation: false`.

## Install

User-level:
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/grok-skill ~/.grok/skills/sortic-ip-sentinel-free
```

Grok Build / project: `.grok/skills/sortic-ip-sentinel-free/` (already includes `references/`).

Grok Bot: same folder on the Bot’s machine. Treat email / GitHub push / browser-use / Clip-Bot / social post as **live demo channels**. Apply show/hold before the paste/send. Never invent status. Never email third parties unless this turn names them.

## Behaviour notes
- Match L0–L3. Meta work on this skill stays L0. US IP corpus ticks stay L0.
- Never ask the Grok viewer to open localhost, run shell, or paste logs.
- Headless contract: stamp → snapshot → options 1–8 → default 1+8 if unnamed → disclaimer. JSON schema `sorticai.hygiene_package.v1` (`output_register`, `not_for_third_party`, `agent_exposure`).
- This is the free Phase-0 shape (skill → structured hygiene package). No paid menu.
- Builder worksheet: not legal advice; do not send outputs as legal analysis.

**Not legal advice. No guarantees. Free only.**
