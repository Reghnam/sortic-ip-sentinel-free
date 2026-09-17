# Grok Bot share pack — IP Sentinel (prepare only, v0.5.29-free)

**Hygiene only. Not legal advice. Free only. No secrets.**

This folder is a **shareable Bot template** (profile + skills + routines **config only**). It is **not** a live marketplace listing.

**Do not publish live overnight.** Live marketplace publish stays **L3 for David/Sameth**. Lunch testers install from this PR branch; they do not press marketplace publish.

## What this pack is

| File | Purpose |
|------|---------|
| [bot-template.json](bot-template.json) | Sanitized export (profile + skills + routines config only). |
| [profile.md](profile.md) | Public-safe Bot profile (name, blurb, boundaries). No secrets. |
| [skills.md](skills.md) | Which skill to enable (this free zip). No corpus paths. |
| [routines.md](routines.md) | Safe routine stubs only. No webhooks, no API keys. |

Export = `bot-template.json` plus these three surfaces. Strip secrets, internal URLs, corpus paths, and API keys before any share. This pack ships already stripped.

## Install (this Bot only — not marketplace)

1. Open the Grok Bot → **Plugins** (or Skills).
2. **Save** / upload `sortic-ip-sentinel-free-grok-v0.5.29.zip` so `SKILL.md` is the skill root.
3. **Enable per-Bot.** One Bot's enablement is not isolation from other Bots on the shared computer.
4. Paste `profile.md` into the Bot profile. Do **not** paste corpus paths or sidecar URLs.
5. Leave routines as the stubs in `routines.md` unless this turn names owner **and** action.
6. **Scan before ship.** Inspect `SKILL.md` + `references/` before upload.

**Do not** `cp` to `~/.grok/skills/` — that path is **Grok Build**.

**Do not** put `Reghnam/us-ip-law-ground-truth` (PRIVATE) on the Bot disk, in this folder, or in the skill zip.

**Do not** invent a corpus URL. RAG is retrieve-only sidecar / offline fixtures (`references/public-corpus-rag.md`).

Drive Sep-2 zips are **stale**. Use this PR branch.

## Never in this pack

- API keys, webhook signing secrets, mailbox connectors
- Internal / staging URLs, sidecar hosts, corpus mount paths
- Client / product / infra / valuation facts
- Paid paths or checkout language
- Third-party marketplace skills

## Live publish

Marketplace / public Bot share of this template is a **publish**. Decline unnamed. **David/Sameth** only, L3, not overnight.

**Not legal advice. No guarantees. Free only.**
