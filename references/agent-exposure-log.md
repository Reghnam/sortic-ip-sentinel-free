# Agent / computer-use exposure log — Template (v0.5.3-free)

**Free only · Builder worksheet · Not legal advice · No guarantees**

Use when a **headless agent, Grok Bot, Codex/Claude `-p`, computer-use, or browser-use plugin** can show, email, push, post, or paste work into a public surface. Fold this into catalog item **5** (provenance + holdback). Do not add a ninth picker option.

An agent with its own computer is a **live demo channel**. Treat it like an investor screen-share: apply show/hold *before* the paste/send/push.

## What the agent did (redact secrets in this table)

| When | Runtime (Bot / CLI / MCP) | Channel (browser / email / GitHub / social / file) | What was shown or sent | Audience (named?) | Hold or ok? | Evidence pointer |
|------|---------------------------|-----------------------------------------------------|------------------------|-------------------|-------------|------------------|
|      |                           |                                                     |                        |                   |             |                  |

## Pre-send checklist (computer-use)

- [ ] Exact parameters / recipes / full source are **not** in the paste, email, commit, or public page.
- [ ] Recipient was **named in this turn**. If not named, do not email or post. (`not_for_third_party`)
- [ ] No invented status ("filed", "cleared", "counsel approved").
- [ ] Contribution log names the **human** who conceived vs the **runtime** that produced the bytes.
- [ ] Public browser / Clip-Bot / social post is treated as **public** exposure, not a private workspace.

## Rules (from operator briefs + Grok Bot practice)

1. **Do not invent status.** Unknown = unknown. Write "not found" or "not in this turn".
2. **Do not email or post to third parties** unless this turn names the recipient.
3. **Do not paste holdbacks into computer-use.** Browser-use, MCP servers, and social schedulers are public-adjacent.
4. **Log the runtime.** "Grok Bot", "Codex `-p`", "Claude `-p`", plugin name. Helps later inventorship hygiene (human conception vs tool).
5. **Publishing a skill or Bot** without protect language is L2 (soft tip). With protect language it is L3.

JSON: emit as `agent_exposure` on `sorticai.hygiene_package.v1` (see `headless-hygiene-package.md`). Prefer empty arrays over invented rows.

> **Builder worksheet.** Do not send this table to third parties as legal analysis. Not legal advice. No guarantees.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance (human conception), WIPO principles.
