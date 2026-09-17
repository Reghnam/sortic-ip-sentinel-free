# SorticAI Free IP Sentinel — Cursor (v0.5.29-free)

Cursor host pack. Same behaviour as the root skill. `SKILL.md` at pack root so the zip is Cloud-ready.

`references/` is **bundled**. One copy is a complete skill.

## Install

**Cloud Agents — project `.cursor/skills/`** (preferred; no Sync required):

```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
mkdir -p .cursor/skills/sortic-ip-sentinel-free
cp -r sortic-ip-sentinel-free/cursor-skill/. .cursor/skills/sortic-ip-sentinel-free/
```

**Custom Modes = pin skill.** Pin `sortic-ip-sentinel-free` on the lunch Custom Mode.

**User-global** — this machine only:

```bash
cp -r sortic-ip-sentinel-free/cursor-skill ~/.cursor/skills/sortic-ip-sentinel-free
```

**Sync Skills** copies `~/.cursor/skills/` only. It does **not** copy `~/.agents/skills/`. Treat Sync as a publish. Lunch default: leave Sync off; use project `.cursor/skills/`.

See also `.cursor/skills/README.md` in this repo.

## Corpus / RAG

`Reghnam/us-ip-law-ground-truth` is **PRIVATE**. Never copy it into this pack, a Drive zip, or a Grok Bot disk. L3 RAG is retrieve-only sidecar / offline public-safe fixtures (`references/public-corpus-rag.md`). Do not invent a corpus URL. Ticks stay L0.

Drive Sep-2 zips are **stale**. Use this PR branch.

**Scan before ship.** Third-party marketplace skills are untrusted. Inspect-before-attach.

Builder worksheet: not legal advice; do not send outputs as legal analysis.

**Not legal advice. No guarantees. Free only.**
