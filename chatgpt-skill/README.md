# SorticAI Free IP Sentinel (ChatGPT / Codex compatible)

> This is a stripped-down, fully compatible variant for OpenAI tools.  
> The rich canonical version lives in the root of this repo.

This is the OpenAI-compatible variant of the SorticAI Free IP Sentinel (v0.5-free).

**Important:** The canonical rich source (with full frontmatter for Claude, Grok, Cursor, etc.) lives at:
https://github.com/Reghnam/sortic-ip-sentinel-free

This variant strips unsupported frontmatter for ChatGPT Skills / Codex compatibility and moves display/invocation policy into `agents/openai.yaml`.

## Quick Install

**OpenAI Codex CLI/Desktop**
```bash
# Recommended: clone the main repo and copy the subfolder
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.codex/skills/sortic-ip-sentinel-free
```

**ChatGPT Skills (Business/Enterprise/Edu)**
- Go directly to the folder on GitHub and click **"Download ZIP"** (top right when viewing the folder):
  https://github.com/Reghnam/sortic-ip-sentinel-free/tree/main/chatgpt-skill
- Or use "Create with chat" and paste the link above.

Then upload the downloaded zip in the Skills tab.

## Contents
- `SKILL.md` — minimal compliant frontmatter + full behaviour
- `agents/openai.yaml` — display name, short description, invocation policy
- `references/` — all hygiene templates and playbooks
- `LICENSE.md`

## Attribution
This is a distribution variant of the free portable edition. All core logic, disclaimers, and references are preserved from the canonical source.

**Not legal advice. No guarantees. Free only.**

See the main repo for full details, examples, and the richer version for other platforms.
