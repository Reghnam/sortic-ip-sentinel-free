# Agent / computer-use exposure log — Template (v0.5.8-free)

**Free only · Builder worksheet · Not legal advice · No guarantees**

Use when a **headless agent, Grok Bot, Codex/Claude `-p`, computer-use, or browser-use plugin** can show, email, push, post, or paste work into a public surface. Fold this into catalog item **5** (provenance + holdback). Do not add a ninth picker option.

An agent with its own computer is a **live demo channel**. Treat it like an investor screen-share: apply show/hold *before* the paste/send/push.

## What the agent did (redact secrets in this table)

| When | Runtime (Bot / CLI / MCP) | Channel (browser / email / GitHub / social / livestream / HiTL / board / backup / export / local-computer / callable / voice / voice-screen / routine / file / bot-share / marketplace / grok-share / reviewer / mailbox / iam-screenshot / access-grant / legal-draft / webhook / bot-duplicate / lifecycle-hook / astra-computer / console-shot / ci-apply) | What was shown or sent | Audience named this turn? | Action named this turn? | Hold / ok / not_sent / blocked / declined | Evidence (path+link or message-id) |
|------|---------------------------|-----------------------------------------------------|------------------------|-------------------|-------------|------------------|
|      |                           |                                                     |                        |                       |                       |                              |                                      |

## Pre-send checklist (computer-use)

- [ ] Exact parameters / recipes / full source are **not** in the paste, email, commit, or public page.
- [ ] Recipient **and** action were **named in this turn**. If either is missing, do not email, post, auto-publish, pay, publish identity/live-copy, or send leftover drafts / partner pre-reads. (`approval_required`, `owner_gated`)
- [ ] Not a leftover draft or empty signature reply.
- [ ] No invented status ("filed", "cleared", "counsel approved", "sent", "didn't run").
- [ ] Contribution log names the **human** who conceived vs the **runtime** that produced the bytes.
- [ ] Public browser / Clip-Bot / livestream / HiTL / board / social post is treated as **public** exposure, not a private workspace.
- [ ] If claiming a send: message-id + recipients are written. Else log `not_sent`.
- [ ] If claiming done: folder path + link exist. Inbox-root dumps are `blocked_no_evidence`.
- [ ] Shared Bot cloud computer is **not** a secrecy boundary — do not park holdbacks there. Local-computer execution is not a vault either.
- [ ] GitHub auto-push of this public repo declined unless owner **and** action named this turn.
- [ ] Truncated/junk files are not originals.
- [ ] Subagent spawned only if this skill is listed on it.
- [ ] Task specs dispatched to computer-use contain no secrets / proprietary source / customer data.
- [ ] Backup pack is not treated as a publish. Project export is owner-desk.
- [ ] Registrar "new device" alert from rotating Bot egress → decline login.
- [ ] Callable hop: exact parameters / full source are **not** on the callable surface.
- [ ] Voice/phone provision declined unless owner **and** action named. `--yolo` is not that gate.
- [ ] Placeholders / MCP-size-blocked files are not originals.
- [ ] Bot share / marketplace clone: holdbacks are **not** in the shareable Bot.
- [ ] Image-only decks: no invented dollar figures.
- [ ] 2FA / CAPTCHA computer-takeover declined.
- [ ] Reviewer hop treated as a demo channel (not already private).
- [ ] Mailbox / Outlook connector not enabled on this skill.
- [ ] Public Grok share (`x.com/i/grok/share`) / Bot share (`x.ai/bot`) stripped of internals.
- [ ] IAM / webhook / secret screenshots not in the zip.
- [ ] Access grant declined unless named.
- [ ] Legal drafts not sent without named recipient AND action.
- [ ] Voice screen-share: holdbacks off the shared screen. Voice clone declined (identity).
- [ ] No production lifecycle hooks added.
- [ ] Astra / computer-use write-across-apps: internals held; connectors not treated as a vault.
- [ ] Console screenshots not attached to a partner mail unless NDA/show-hold and recipient AND action named.
- [ ] CI auto-apply of infra PRs declined unless owner AND action named.

## Rules (from 4–10 Sep operator briefs + Grok Bot + OpenAI 2026-09-10 + Anthropic pin-latest)

1. **Do not invent, replace, or reroll a result.** Unknown = unknown. Write "not found" or "not in this turn". Stale nextRun ≠ didn't run.
2. **Approval = recipient AND action named this turn.** Leftover drafts, empty signature replies, auto-publish, partner pre-reads, pay, identity/live-copy, and resend stay on hold.
3. **Do not paste holdbacks into computer-use.** Browser-use, MCP servers, livestreams, and social schedulers are public-adjacent. Teaching records the screen — hold secrets.
4. **Log the runtime.** "Grok Bot", "Codex `-p`", "Claude `-p`", plugin name. Helps later inventorship hygiene (human conception vs tool).
5. **Publishing a skill or Bot** without protect language is L2 (soft tip). With protect language it is L3. HiTL / UAT / livestream / board without protect language is L2.
6. **Evidence-or-blocked.** Done requires path + link. If source data is unavailable, report failure — do not use stale data.
7. **Claimed send needs message-id + recipients.**
8. **Shared Bot computer ≠ vault.** All Bots on the account see the same files/logins/cookies. Egress IP is not sticky.
9. **Public-repo auto-push is owner L3.** Decline unnamed.
10. **Subagents do not inherit this skill.** Pass it or do not spawn.
11. **Truncated ≠ original.** Clock-limited live rooms hold deeper internals.
12. **Backup ≠ publish.** Weekly backup / project export is owner-desk. Do not grow backup trees.
13. **Owner-gated even at IP L3:** send, publish, pay, identity, live title/copy.
14. **Skill zip is scanned.** No secrets, no client facts in ChatGPT/Codex uploads.
15. **Callable hops are demo channels.** Show/hold at every hop. Do not dump internals into the callable surface.
16. **`--yolo` is not owner approval.** Voice/phone provision, disabled-job re-enable, live-prompt rewrite, and fit-note send stay declined unless named.
17. **Placeholders / MCP-size-blocked files are not originals.**
18. **Bot share / marketplace clone is a demo channel.** Do not park holdbacks in a shareable Bot. Require Approval wins Always Allow.
19. **Image-only ≠ numbered facts.** Do not invent dollar figures from a PNG/chart. 2FA/CAPTCHA computer-takeover → decline login.
20. **Reviewer hop is a disclosure hop.** Human review before the customer is still a live channel.
21. **Mailbox / share URL / Bot duplicate.** Mailbox is MCP. `x.com/i/grok/share/…` and `x.ai/bot/…` are public cloneable config. Duplicate copies skills and routines, not history.
22. **Access grant / IAM / webhook / drafts.** Owner-gated identity. Screenshots are holdbacks. Drafts ≠ send. Two readings are not a verdict.
23. **Voice screen-share sees the browser.** Voice clone is identity publish. Plugin-bundled hooks stay skipped until trusted. This skill has none.
24. **Astra computer-use is a live demo.** Write-across-apps / browser-use without APIs is computer-use. Connectors are not a vault.
25. **Console-shot mail / CI auto-apply.** Partner-mail console shots are a demo. CI auto-apply is a production change. One focused skill.

JSON: emit as `agent_exposure` on `sorticai.hygiene_package.v1` (see `headless-hygiene-package.md`). Prefer empty arrays over invented rows. Set `owner_gated: true`.

> **Builder worksheet.** Do not send this table to third parties as legal analysis. Not legal advice. No guarantees.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance (human conception), WIPO principles.
