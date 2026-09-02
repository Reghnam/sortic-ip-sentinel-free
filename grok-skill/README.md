# SorticAI Free IP Sentinel — Grok / Grok Build (v0.5.1-free)

Grok-native package. Headless numbered options are the **default** (Grok Build viewers cannot run a TUI picker; `grok -p` is one-shot).

## Install

User-level:
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/grok-skill ~/.grok/skills/sortic-ip-sentinel-free
cp -r sortic-ip-sentinel-free/references ~/.grok/skills/sortic-ip-sentinel-free/
```

Grok Build / project: `.grok/skills/sortic-ip-sentinel-free/` plus `references/`.

## Behaviour notes
- Match L0–L3. Meta work on this skill stays L0.
- Never ask the Grok viewer to open localhost, run shell, or paste logs.
- Headless contract: stamp → snapshot → options 1–8 → deliver if already named → disclaimer. JSON schema `sorticai.hygiene_package.v1` on export.
- This is the free Phase-0 shape (skill → structured hygiene package). No paid menu.

**Not legal advice. No guarantees. Free only.**
