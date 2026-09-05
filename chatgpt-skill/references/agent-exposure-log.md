# Agent / computer-use exposure log — Template (v0.5.4-free)

**Free only · Builder worksheet · Not legal advice · No guarantees**

Use when a **headless agent, Grok Bot, Codex/Claude `-p`, computer-use, or browser-use plugin** can show, email, push, post, or paste work into a public surface. Fold this into catalog item **5** (provenance + holdback). Do not add a ninth picker option.

An agent with its own computer is a **live demo channel**. Treat it like an investor screen-share: apply show/hold *before* the paste/send/push.

## What the agent did (redact secrets in this table)

| When | Runtime (Bot / CLI / MCP) | Channel (browser / email / GitHub / social / livestream / HiTL / file) | What was shown or sent | Audience named this turn? | Action named this turn? | Hold / ok / not_sent / blocked | Evidence (path+link or message-id) |
|------|---------------------------|-----------------------------------------------------|------------------------|-------------------|-------------|------------------|
|      |                           |                                                     |                        |                       |                       |                              |                                      |

## Pre-send checklist (computer-use)

- [ ] Exact parameters / recipes / full source are **not** in the paste, email, commit, or public page.
- [ ] Recipient **and** action were **named in this turn**. If either is missing, do not email, post, auto-publish, or send leftover drafts. (`approval_required`)
- [ ] Not a leftover draft or empty signature reply.
- [ ] No invented status ("filed", "cleared", "counsel approved", "sent").
- [ ] Contribution log names the **human** who conceived vs the **runtime** that produced the bytes.
- [ ] Public browser / Clip-Bot / livestream / HiTL / social post is treated as **public** exposure, not a private workspace.
- [ ] If claiming a send: message-id + recipients are written. Else log `not_sent`.
- [ ] If claiming done: folder path + link exist. Inbox-root dumps are `blocked_no_evidence`.

## Rules (from 4 Sep operator briefs + Grok Bot + OpenAI 2026-09-05)

1. **Do not invent, replace, or reroll a result.** Unknown = unknown. Write "not found" or "not in this turn".
2. **Approval = recipient AND action named this turn.** Leftover drafts, empty signature replies, auto-publish, and resend stay on hold.
3. **Do not paste holdbacks into computer-use.** Browser-use, MCP servers, livestreams, and social schedulers are public-adjacent. Teaching records the screen — hold secrets.
4. **Log the runtime.** "Grok Bot", "Codex `-p`", "Claude `-p`", plugin name. Helps later inventorship hygiene (human conception vs tool).
5. **Publishing a skill or Bot** without protect language is L2 (soft tip). With protect language it is L3. HiTL / UAT / livestream without protect language is L2.
6. **Evidence-or-blocked.** Done requires path + link. If source data is unavailable, report failure — do not use stale data.
7. **Claimed send needs message-id + recipients.**

JSON: emit as `agent_exposure` on `sorticai.hygiene_package.v1` (see `headless-hygiene-package.md`). Prefer empty arrays over invented rows.

> **Builder worksheet.** Do not send this table to third parties as legal analysis. Not legal advice. No guarantees.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance (human conception), WIPO principles.
