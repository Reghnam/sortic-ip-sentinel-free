# How to Publish the SorticAI Free IP Sentinel (v0.5.2-free) to OpenAI

Primary path in 2026 is **ChatGPT Skills + Codex SKILL.md**, not a Custom GPT.

## Path 1: Portable Skill (recommended)

Repo: https://github.com/Reghnam/sortic-ip-sentinel-free

**Codex**
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free
```
Fallback: `~/.codex/skills/`. Project: `.agents/skills/`. Invoke `$` or `/skills`. Description is front-loaded so implicit match survives list truncation.

**ChatGPT Skills (Business / Enterprise / Edu)**
Zip `chatgpt-skill/` with `SKILL.md` at the zip root → Skills tab. Invoke `@`.

`agents/openai.yaml` sets display name, default prompt, brand colour, and `allow_implicit_invocation: true`.

Headless: "Output numbered options and hygiene package JSON."

## Path 2: Custom GPT (fallback)

1. Create a GPT named `SorticAI Free IP Sentinel (v0.5.2-free)`.
2. Paste `instructions.txt` into Instructions.
3. Upload `knowledge/` files.
4. Starters: "IP sensitive moment on our new protocol before investor demo" / "Help me create a show/hold map".
5. Share via link. GPT Store still needs an eligible workspace + Builder Profile.

**This is free procedural hygiene only. Not legal advice. No guarantees.**
