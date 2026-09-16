# Agent / computer-use exposure log — Template (v0.5.20-free)

**Free only · Builder worksheet · Not legal advice · No guarantees**

Use when a **headless agent, Grok Bot, Codex/Claude `-p`, computer-use, or browser-use plugin** can show, email, push, post, or paste work into a public surface. Fold this into catalog item **5** (provenance + holdback). Do not add a ninth picker option.

An agent with its own computer is a **live demo channel**. Treat it like an investor screen-share: apply show/hold *before* the paste/send/push.

## What the agent did (redact secrets in this table)

| When | Runtime (Bot / CLI / MCP) | Channel (browser / email / GitHub / social / livestream / HiTL / board / backup / export / local-computer / callable / voice / voice-screen / routine / file / bot-share / marketplace / grok-share / reviewer / mailbox / iam-screenshot / access-grant / legal-draft / webhook / bot-duplicate / lifecycle-hook / astra-computer / console-shot / ci-apply / sites / async-board / repo-skill / fan-out / hooks-trust / remote-mac / workspace-plugin / responses-api / hosted-skill / counsel-release / livestream / claude-plugin / demo-skill / meet-notes / judge-model / deid-train / default-version / shared-bot-session / job-skill / cross-surface / protected-lane / skill-zdr / bot-dm / bot-screen / api-vs-chat / capdir / disallowed-tools / skill-scan / us-host / sign-out-wipe / dist-path / csam-shot) | What was shown or sent | Audience named this turn? | Action named this turn? | Hold / ok / not_sent / blocked / declined | Evidence (path+link or message-id) |
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
- [ ] Shared Bot cloud computer is **not** a secrecy boundary — do not park holdbacks there. Screens ≠ isolation. Bot-to-Bot DM / group chat is a hop. Local-computer execution is not a vault either.
- [ ] API no-train is not treated as ChatGPT no-train. Skills / Files / Conversations / Agents are not treated as ZDR-covered.
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
- [ ] Sites deploy treated as production; save-without-deploy to review; env/secrets not in prompts or Site content.
- [ ] Async board packet without the room treated as a demo; valuation/internals held.
- [ ] Project-repo skill commit declined unless named publish.
- [ ] Workflow fan-out: show/hold at every hop.
- [ ] Project `.grok/hooks/` not enabled without `/hooks-trust`.
- [ ] Remote Mac / phone-driven desktop treated as computer-use; Mac-as-remote-device register declined unless named; Messages/Mail typing held as a send; phone screenshots treated as a demo.
- [ ] Live isEnabled used as job-state evidence; prior brief not invented as disabled.
- [ ] Workspace-shared plugin / Copilot `.github/skills/` commit declined unless named publish.
- [ ] Responses API hosted skill / open catalog declined unless named publish; pin an integer version, not `latest`.
- [ ] Subagent spawned only if this skill is listed (`skills:` field or equivalent).

## Rules (from 4–11 Sep operator briefs + Grok Bot + OpenAI 2026-09-10 + Anthropic pin-latest)

1. **Do not invent, replace, or reroll a result.** Unknown = unknown. Write "not found" or "not in this turn". Stale nextRun ≠ didn't run.
2. **Approval = recipient AND action named this turn.** Leftover drafts, empty signature replies, auto-publish, partner pre-reads, pay, identity/live-copy, and resend stay on hold.
3. **Do not paste holdbacks into computer-use.** Browser-use, MCP servers, livestreams, and social schedulers are public-adjacent. Teaching records the screen — hold secrets.
4. **Log the runtime.** "Grok Bot", "Codex `-p`", "Claude `-p`", plugin name. Helps later inventorship hygiene (human conception vs tool).
5. **Publishing a skill or Bot** without protect language is L2 (soft tip). With protect language it is L3. HiTL / UAT / livestream / board without protect language is L2.
6. **Evidence-or-blocked.** Done requires path + link. If source data is unavailable, report failure — do not use stale data.
7. **Claimed send needs message-id + recipients.**
8. **Shared Bot computer ≠ vault.** All Bots on the account see the same files/logins/cookies. Screens are work surfaces, not security boundaries. Bot-to-Bot DM / group chat is a hop. Delete Bot ≠ wipe computer. Dedicated user for isolated credentials. Egress IP is not sticky. Auto Review does not review memory writes.
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
26. **Sites / user-override.** Every Sites URL is production. User instructions this turn beat skill guidelines; named recipient AND action is the override; quote SKILL.md on L3 decline. No unsolicited L0/L1 checklists.
27. **Async board / repo-skill / fan-out / hooks-trust.** Packet without the room is a demo. Project-repo skill commit is a publish (Copilot/VS Code included). Fan-out multiplies hops. Project hooks need `/hooks-trust`.
28. **Remote Mac / phone-driven desktop.** Registering a Mac as a Bot remote device is owner-gated. Desktop drive + phone screenshot = demo. Messages/Mail typing = send.
29. **Live isEnabled / workspace plugin.** Do not invent disabled from a prior brief. Workspace-shared plugins are a publish channel.
30. **Responses API / two zip layouts / subagent skills.** Versioned bundles; pin integer, not `latest` / `default_version` / omit-version. Do not expose this public repo as an open end-user catalog. Skills-tab zip ≠ plugin zip. Subagents do not inherit unless listed.
31. **De-identified / ZDR.** Invention-grade chats into a frontier lab are a disclosure even if PII-stripped. Skills are not a ZDR boundary.
32. **Shared Bot sessions / job-skill / cross-surface.** Account-wide files+logins. Marketplace job-taking is access grant + send. claude.ai enablement syncs to Cowork/cloud; local folder still does not auto-sync. Each enablement is a publish.
33. **Astra define-completion / over-refusal.** Do not stop after the stamp. Do not pad extra refuse language.
34. **App Builder / Vercel.** Preview is a demo. Vercel deploy is a publish.
35. **Grok zero-config discovery.** ~/.agents/skills/ and Claude Code plugins/skills/hooks/AGENTS.md are live channels.

JSON: emit as `agent_exposure` on `sorticai.hygiene_package.v1` (see `headless-hygiene-package.md`). Prefer empty arrays over invented rows. Set `owner_gated: true`.

> **Builder worksheet.** Do not send this table to third parties as legal analysis. Not legal advice. No guarantees.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance (human conception), WIPO principles.

- [ ] Counsel-release: "waiting for legal review" pack is **not** sent to a customer.
- [ ] Public livestream of internals declined unless named. Attending is L0.
- [ ] Demonstration-to-skill (walk once, save as skill) declined unless named. Screen is recorded.
- [ ] Claude-plugin directory submit declined unless named.
- [ ] Meet auto-notes of an IP/AI session treated as a demo channel.
- [ ] A second-model judge is **not** logged as counsel review.
- [ ] De-identified / ZDR-claimed frontier chat of invention-grade content treated as a disclosure (opt-out is not a rewind).
- [ ] Omit-version / default_version / latest treated as a live channel; pin an integer.
- [ ] Shared Bot computer (files, sessions, logins) treated as account-wide.
- [ ] Marketplace job-taking skill declined unless named (access grant + send).
- [ ] Cross-surface Claude install declined unless named.
- [ ] App Builder live preview treated as a demo; unnamed Vercel deploy declined.
- [ ] claude.ai enablement / CLAUDE_CODE_SYNC_SKILLS=1 declined unless named (publish).
- [ ] L3 completion defined (did not stop after the stamp).
- [ ] Grok ~/.agents/skills/ / Claude Code plugin discovery treated as a live channel.
- [ ] Desktop-egress unnamed enable declined (CDN, not a vault; update computer first).
- [ ] Ownership-pass / task-ownership unnamed declined (access grant + hop).
- [ ] /v1/videos not treated as ZDR (48h+30d; Eyes Off still retain).
- [ ] allowed-tools write grants not added.
- [ ] Legacy Privacy Mode not invented (Grok Bot requires cloud storage; Cursor opt-out).
- [ ] Engineers / Galaxy / role livestream calendar add treated as L0 attend.
- [ ] Local-computer-exec unnamed Always-allowed declined (Ask every time default).
- [ ] CSAM / image Eyes Off not treated as a wipe.
- [ ] None-retention videos project not treated as a protected lane.
- [ ] allowed-tools one-turn grant-clear not treated as a vault.
- [ ] Auto Review rules treated as desktop-local; Reset drops unsynced work.

36. **Desktop-egress CDN.** Settings → Updates → Update Grok Bot's Computer FIRST, then Settings → Computer → Route Computer traffic through this desktop. Reverse order errors. Laptop closed stops routing. Holdbacks on that desktop see Bot traffic.
37. **Ownership-pass.** Passing task ownership between Bots is access grant + hop. Isolated credentials need a dedicated user.
38. **Videos / Eyes Off / Legacy / allowed-tools.** Videos 48h+30d blocked for MAM/ZDR; Eyes Off still retain. No Legacy Privacy Mode. Do not add allowed-tools write grants. Conversations+items and threads+messages/runs/steps are granular-ineligible.

39. **Local-computer execution.** Settings → General → Agent → Execution on Local Computer. Default Ask every time. Never allowed unless named. Distinct from desktop-egress and from the cloud computer.
40. **CSAM / None-retention / grant-clear.** CSAM scan overrides ZDR. None-retention project to call videos is not a lane. allowed-tools grant clears next message — still do not add write grants.
- [ ] Grok Bot computer not treated as EU/on-prem vault (US-hosted today; not BYO).
- [ ] Sign-out not treated as wipe of claude.ai-synced skills.
- [ ] disallowed-tools / skill-scan not treated as a vault.
- [ ] Invention screenshots not treated as CSAM-exempt.
