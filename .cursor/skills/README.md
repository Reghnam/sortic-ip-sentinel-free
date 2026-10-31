# Cursor Cloud install package

Cloud Agents discover project skills under **`.cursor/skills/`**.

This repo ships the Cursor host pack at [`../../cursor-skill/`](../../cursor-skill/) (SKILL.md at pack root). Copy it here so the folder name matches YAML `name`:

```bash
mkdir -p .cursor/skills/sortic-ip-sentinel-free
cp -r cursor-skill/. .cursor/skills/sortic-ip-sentinel-free/
```

**Custom Modes = pin skill.** Pin `sortic-ip-sentinel-free` on the lunch Custom Mode.

**Sync Skills** copies `~/.cursor/skills/` only — not this project path and not `~/.agents/skills/`. Lunch default: leave Sync off; use this project path.

Do **not** put `us-ip-law-ground-truth` (PRIVATE) under `.cursor/skills/`. RAG is sidecar/offline only.

Drive Sep-2 zips are stale. Use this branch. Zip `free-ip-sentinel-cursor-v0.5.80-free.zip` from `cursor-skill/`.

**Not legal advice. No guarantees. Free only.** Progressive disclosure: this folder is the install copy. The skill stays instructions-only.
