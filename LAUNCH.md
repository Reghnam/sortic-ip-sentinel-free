# LAUNCH: SorticAI Free IP Sentinel v0.5-free

**Status**: Ready for distribution. All files sanitized for free-only use. Strong disclaimers included.

## 1. Push to GitHub (Required First Step)

1. On GitHub, create a **new public** repository named exactly `sortic-ip-sentinel-free` (do **not** initialize with README).
2. In terminal, run the commands from `PUSH_TO_GITHUB.txt` in this folder.
   - It will set remote to https://github.com/Reghnam/sortic-ip-sentinel-free.git and push.

**Result**: This becomes the canonical public source for the portable skill.

## 2. Distribute as Portable Skill (Recommended Primary Path)

OpenAI supports the `SKILL.md` standard (agentskills.io).

**Codex CLI / Desktop:**
```bash
$skill-installer https://github.com/Reghnam/sortic-ip-sentinel-free
```

**ChatGPT (Business/Enterprise/Edu):**
- Go to Skills tab → Upload a zip of this folder, or use "Create with chat" + the GitHub link.

The skill will automatically activate on "IP sensitive moment" language.

## 3. Create Custom GPT (for Hosted Sharing)

Use the pre-built package:

1. Open ChatGPT → Create a new GPT
2. Name: `SorticAI Free IP Sentinel (v0.5-free)`
3. Paste the full content of `openai-gpt-package/instructions.txt` into **Instructions**
4. Upload all files from `openai-gpt-package/knowledge/` as Knowledge files
5. Add conversation starters:
   - "IP sensitive moment on our new protocol before investor demo"
   - "Help me create a show/hold map for this architecture"
6. Test key flows
7. Share via "Anyone with the link"

**Note**: Full GPT Store publishing requires a Business/Enterprise/Edu workspace + verified Builder Profile.

## 4. Verification Checklist

- [ ] GitHub repo is public
- [ ] L3 triggers work ("protect the IP", "IP sensitive moment")
- [ ] L0 silence on privacy/config/meta work
- [ ] Disclaimers appear on all outputs
- [ ] All deliverables are free-only (no paid language)

## Files

- `SKILL.md` — Portable skill definition (works in Codex, ChatGPT Skills, etc.)
- `openai-gpt-package/` — Everything needed for Custom GPT
- `references/` — Source templates

**This is free procedural hygiene only. Not legal advice. No guarantees.**

Sources (high-level): EPO Guidelines, USPTO 2025 AI inventorship guidance, WIPO principles.

---

**Next action for you**: Push the folder to GitHub, then run the Codex installer command to test.
