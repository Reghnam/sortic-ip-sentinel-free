# Changelog — SorticAI Free IP Sentinel

All notable changes to the portable free edition. Hygiene only. Not legal advice.

## [0.5.11-free] — 2026-09-12

Patched from: david@ mailbox 8–12 Sep 2026 (meet auto-notes of an IP/AI session are a demo; counsel-release of AI output is a send — "waiting for legal review" is an internal hold, never a customer-facing artifact; leftover counsel draft that later sends is still a send; clock-limited UAT is a demo; weekly backup PARTIAL ≠ publish; leftover drafts unsent; access grant is owner-gated; live `isEnabled` is evidence — this improvement job is enabled even with a stale nextRun; Sentinel→GitHub auto-push is owner L3 — this Grok Build turn *is* the named owner push of hygiene-only files — **no client/product/infra names, no valuation figures in this repo**); OpenAI recrawl 2026-09-12 (developers.openai.com/plugins/build/skills + **plugins/guides/submit-claude-plugin** + **plugins/build/plugins** + **api/docs/guides/tools-skills** last noted 12 Sep 07:02 CEST: **three zip layouts** — Skills tab = `SKILL.md` at zip root, Agent Plugins = root `plugin.json` + `skills/<name>/SKILL.md`, Claude archive = `.claude-plugin/plugin.json` + `skills/<name>/SKILL.md` and the portal converts to `.codex-plugin`; exactly one `SKILL.md` per bundle, case-insensitive; zip limits **50 MB / 500 files / 25 MB uncompressed**; no secrets in archive, manifest, instructions, or defaults; inline base64 zip is a publish; unnamed Claude-plugin directory submit is a publish; Responses API Skills are versioned bundles — pin an integer version, `latest` is a live channel; hosted/container is a demo; inspect before attach; do not expose this public repo as an open end-user catalog; local shell does not take `skill_reference` attachments; Astra user instructions this turn beat skill guidelines; on L3 decline name and link SKILL.md; every Sites URL is production); Anthropic Agent Skills + Managed Agents recrawl 2026-09-12 (no new name/description limits: kebab ≤64, description ≤1024 — this patch **trims description to 1022 chars**; SKILL.md body <500; references one level deep; ≥3 evals; degrees of freedom; authors ≠ own reviewers; pin `latest` is a live channel; folder name must match `name`; Windows paths: forward slashes; do not assume tools installed; subagent `skills:` auto-loads listed skills only; `user-invocable:` only literal `true` counts; extra YAML keys ignored; subagent `permissionMode: bypassPermissions` is not owner approval; Managed Agents **20-skill session cap**; Skills are not a ZDR boundary); Grok Bot / Build recrawl 2026-09-12 (`docs.x.ai/grok-bot/overview` published 11 Sep: Bots **learn workflows from demonstration** — walk once, save as a skill; Teach-by-demonstration records the screen, ≤10 min; shared cloud computer is not a vault; Auto Review rules sync to the Bot computer; event-triggered routines from integrations are fan-out; X ingest 12 Sep: public Galaxy-style Bot livestream of a 72-hour build is a demo channel — attending is L0, streaming your internals is L2/L3). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, this Grok Build turn, live automations (stale nextRun ≠ didn't run; live `isEnabled` is evidence; weekly backup ≠ publish), and X ingest. Do not dump client/product facts into the public repo.

### OpenAI (first)

- Description **1022 chars** (was 1068 — over Anthropic 1024; now under Codex 8k / 2% truncation and Anthropic 1024). Front-loads counsel-release + livestream. States decline for login, DNS, unnamed repo push, partner send, pay, identity, access grant, webhook, voice/phone, CI auto-apply, Sites public publish, counsel-release.
- **Three zip layouts.** Skills tab = `SKILL.md` at zip root. Agent Plugins = portable root `plugin.json` + `skills/<name>/SKILL.md`. Claude archive = `.claude-plugin/plugin.json` + `skills/<name>/SKILL.md` (portal converts to `.codex-plugin`). Do not mix. Do not include marketplace.json / mcp.json / apps in a skills-only zip. Convert commands/agents to skills before a Claude-plugin submit. No secrets in archive, manifest, or defaults.
- Responses API Skills: versioned bundles; pin an integer version; `latest` is a live channel; zip upload 50 MB / 500 files / 25 MB uncompressed; inspect before attach; do not expose this public repo as an open end-user catalog.
- Astra: user instructions this turn beat skill guidelines. On L3 decline, name and link SKILL.md. Complete authorized work first. No unsolicited L0/L1 hypothetical-risk checklists. Counsel-unreviewed client send is a hold.
- `agents/openai.yaml` `default_prompt` names three zip layouts, counsel-release, Bot livestream, demonstration-to-skill, Claude-plugin submit, 20-skill cap. Implicit invocation stays on. **No MCP `dependencies.tools`.** No lifecycle hooks.
- New evals 44–49: counsel-release, public livestream, livestream-attend L0, Claude-plugin submit, demonstration-to-skill, meet auto-notes / judge-model.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description **1022 chars**, no XML. Body under 500.
- Gotchas: counsel-release; three zip layouts; Claude-plugin submit; 20-skill session cap; `user-invocable:` only literal `true`; extra YAML keys ignored; `bypassPermissions` is not owner approval; Teach-by-demonstration records the screen; authors ≠ own reviewers; pin `latest`.
- Evals now 49 (≥3 required). Eight options, not nine. References one level deep. No scripts.

### Grok Build (third)

- **Public Bot livestream** of internals is a demo (L2 without protect language; L3 with it). Attending a public livestream is L0.
- **Demonstration-to-skill is a publish.** Walking a Bot through a path once (screen recorded, ≤10 min) and saving it as a skill is a live channel.
- Meet auto-notes of an IP/AI session are a demo. Counsel-release is a send. A second-model judge is another hop, not counsel. Confidence = certainty of a finding, not priority or impact.
- Live `isEnabled` is evidence. This job fires when live metadata says enabled. Stale nextRun ≠ didn't run. Weekly backup ≠ publish.
- Subagents still do not inherit this skill. `--yolo` / `bypassPermissions` is not owner approval. Hide ≠ pause.
- GitHub auto-push of this public repo: decline unless this turn names owner AND action. (This Grok Build turn *is* the named owner push of hygiene-only files.)

### Shared

- JSON `sorticai.hygiene_package.v1` edition `0.5.11-free`. `agent_exposure.channel` may be `counsel-release | livestream | claude-plugin | demo-skill | meet-notes | judge-model` (plus prior values).
- Classification: L0-19 livestream attend; L2-19 meet auto-notes, L2-20 demonstration-to-skill; L3-COUNSEL, L3-LIVESTREAM, L3-CLAUDEZIP, L3-DEMOSKILL, L3-JUDGE.
- Output-language rules 33–36: counsel-release; three zip layouts / Claude-plugin submit; livestream / demo-to-skill; meet auto-notes / judge-model / 20-skill cap.
- Stamp: `v0.5.11-free` / patched 2026-09-12. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.10-free] — 2026-09-11

Patched from: david@ mailbox 8–11 Sep 2026 (phone-driven desktop / remote Mac is computer-use; leftover counsel draft that later sends is still a send; async board packet without the room is a demo; workspace billing/payment without protect intent stays L0; weekly backup ≠ publish; leftover drafts unsent; Sentinel→GitHub auto-push is owner L3 — this Grok Build turn *is* the named owner push of hygiene-only files; live `isEnabled` is evidence — do not invent disabled from a prior brief — **no client/product/infra names, no valuation figures in this repo**); OpenAI **plugins/build/skills** recrawl ~07:36 CEST plus **api/docs/guides/tools-skills** 08:40 CEST + Astra instruction-following + Codex Sites (developers.openai.com/plugins/build/skills live; **Responses API Skills are versioned bundles** — pin an integer version, `latest` is a live channel; hosted/container execution is a demo surface; inspect before attach; do not expose this public repo as an open end-user catalog; local shell does not take `skill_reference` attachments; **two zip layouts** — ChatGPT Skills tab = `SKILL.md` at zip root, Agent Plugins = `plugin.json` + `skills/<name>/SKILL.md`; exactly one `SKILL.md` per bundle, case-insensitive; smallest plugin shape is skill-only; MCP Scan Tools is a snapshot; zip scanned; **explicit user instructions this turn take precedence over skill guidelines**; on L3 decline **name and link** SKILL.md; no unsolicited warnings / disclaimers / approval flows / safety checklists; every **Sites deployment URL is production**; workspace-shared plugins are a demo/publish channel); Anthropic Agent Skills best-practices recrawl 2026-09-11 (no new limits: name kebab ≤64; description ≤1024; SKILL.md body <500; references one level deep; ≥3 evals; degrees of freedom; authors ≠ own reviewers; pin `latest` is a live production channel; folder name must match `name`; Windows paths: forward slashes; do not assume tools installed; Claude Code subagent frontmatter `skills:` auto-loads listed skills — they still do not inherit unless listed); Grok Bot / Build recrawl 2026-09-11 (`docs.x.ai/grok-bot/bots` last updated 7 Sep: share link is **public configuration**; hide ≠ pause; duplicate copies skills and routines; cloud computer is separate from the Mac in front of you; **Execution on Local Computer** is owner-gated; X ingest 9–11 Sep: phone-driven docked Mac / Messages typing / phone screenshots of local terminal are computer-use + send/demo; `docs.x.ai/build/features/skills-plugins-marketplaces`: skills from `./.grok/skills/` walked up to repo root — **a project-repo skill commit is a publish**; Copilot/VS Code also load `.github/skills/` and `.claude/skills/`; project `.grok/hooks/` **requires `/hooks-trust`**; subagents spawn independent child sessions and do not inherit). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, this Grok Build turn, live automations (stale nextRun ≠ didn't run; live `isEnabled` is evidence; weekly backup ≠ publish), and X ingest. Do not dump client/product facts into the public repo.

### OpenAI (first)

- Description 1019 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads remote Mac + Sites. States decline for login, DNS, unnamed repo push, partner send, pay, identity, access grant, webhook, voice/phone, CI auto-apply, Sites public publish.
- Responses API Skills (`api/docs/guides/tools-skills`): versioned bundles; pin an integer version in production; `latest` is a live channel; hosted/container is a demo; inspect before attach; do not expose this public repo as an open end-user catalog.
- Two zip layouts: Skills tab = `SKILL.md` at zip root; Agent Plugins = `plugin.json` + `skills/<name>/SKILL.md`. Exactly one `SKILL.md` per bundle. Zip is scanned. Prefer one focused skill. No MCP.
- Astra instruction-following: user instructions this turn beat skill guidelines. On L3 decline, name and link SKILL.md. Complete authorized work first. No unsolicited L0/L1 hypothetical-risk checklists.
- Codex/ChatGPT Sites: every deployment URL is production. Workspace-shared plugins are a demo/publish. Sites env/secrets are holdbacks. Workspace billing/payment stays L0.
- `agents/openai.yaml` `default_prompt` names remote Mac, live isEnabled, workspace plugin, Responses API pin-integer / two zip layouts, name+link SKILL.md. Implicit invocation stays on. **No MCP `dependencies.tools`.** No lifecycle hooks.
- New evals 37–43: remote Mac, live isEnabled, workspace plugin / Copilot, Astra name+link, Responses API open catalog / pin-latest, workspace billing L0, two zip layouts / subagent `skills:`.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 1019 chars, no XML. Body under 500.
- Gotchas: remote Mac; live isEnabled; workspace plugin / Copilot; Responses API `latest`; two zip layouts; subagent `skills:` does not inherit unless listed; folder name must match; forward slashes; do not assume tools installed; authors ≠ own reviewers; pin `latest`.
- Evals now 43 (≥3 required). Eight options, not nine. References one level deep. No scripts.

### Grok Build (third)

- Remote Mac / phone-driven desktop is **computer-use**. Registering a Mac as a Bot remote device is owner-gated access grant. Messages/Mail typing is a **send**. Phone screenshots of the local terminal are a demo. Cloud computer ≠ the Mac in front of you. Local-computer execution is not a vault.
- Live `isEnabled` is evidence. Do not invent disabled from a prior brief. Stale nextRun ≠ didn't run. This job fires when live metadata says enabled.
- Workspace-shared plugin and Copilot `.github/skills/` are a **publish**. Project-repo skill commit is a publish. Fan-out is a disclosure multiplier. `/hooks-trust` required for project hooks.
- Subagents still do not inherit this skill. `--yolo` is not owner approval. Hide ≠ pause.
- GitHub auto-push of this public repo: decline unless this turn names owner AND action. (This Grok Build turn *is* the named owner push of hygiene-only files.)

### Shared

- JSON `sorticai.hygiene_package.v1` edition `0.5.10-free`. `agent_exposure.channel` may be `remote-mac | workspace-plugin | responses-api | hosted-skill` (plus prior values).
- Classification: L0-17 live isEnabled, L0-18 workspace billing; L2-16..18 remote Mac / workspace plugin / Responses API hosted; L3-REMOTEMAC, L3-PLUGIN, L3-RESPAPI, L3-ZIPMIX.
- Output-language rules 29–32: remote Mac; live job-state / workspace plugin; Responses API / two zip layouts; subagent `skills:` / billing L0.
- Stamp: `v0.5.10-free` / patched 2026-09-11. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.9-free] — 2026-09-11

Patched from: david@ mailbox 8–11 Sep 2026 (async board packet without the room is a demo channel; leftover counsel draft that later sends is still a send; callable/headless chain remains a disclosure ladder including the **human reviewer hop**; **sortic-ip-sentinel-free automation stays disabled**; Sentinel→GitHub auto-push is owner L3 — this Grok Build turn *is* the named owner push of hygiene-only files; weekly backup ≠ publish; disabled jobs stay disabled; fit-note ≠ send; image-only ≠ numbered facts — **no client/product/infra names, no valuation figures in this repo**); OpenAI **plugins/build/skills** + Astra instruction-following + Codex Sites recrawl **2026-09-11** (developers.openai.com/plugins/build/skills live; developers.openai.com/api/docs/guides/latest-model: **explicit user instructions this turn take precedence over skill guidelines**; if a skill would pause/diverge, **quote SKILL.md**; complete authorized work first so approval is last; **do not introduce unsolicited warnings / disclaimers / hypothetical-risk checklists**; every **Sites deployment URL is production**; save-without-deploy to review; default owner+admins; workspace/public publish are demo channels; keep secrets out of prompts, attached files, Site content, and `.openai/hosting.json`; Astra computer-use is a live demo; connectors are not a vault; computer-use speed is not a vault; Astra credits/seats stay L0; smallest plugin shape is skill-only; MCP Scan Tools is a snapshot; zip scanned); Anthropic Agent Skills best-practices recrawl 2026-09-11 (no new limits: name kebab ≤64; description ≤1024; SKILL.md body <500; references one level deep; ≥3 evals; degrees of freedom; authors ≠ own reviewers; pin `latest` is a live production channel; keep Skills list order stable for prompt caching); Grok Bot / Build recrawl 2026-09-11 (`docs.x.ai/grok-bot/bots` last updated 7 Sep: share link is **public configuration**; hide ≠ pause; duplicate copies skills and routines; `docs.x.ai/build/features/skills-plugins-marketplaces`: skills from `./.grok/skills/` walked up to repo root — **a project-repo skill commit is a publish**; project `.grok/hooks/` **requires `/hooks-trust`**; Grok also reads `.claude/` skills; subagents spawn independent child sessions and do not inherit). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, this Grok Build turn, live automations (stale nextRun ≠ didn't run; disabled jobs stay disabled; weekly backup ≠ publish), and X ingest. Do not dump client/product facts into the public repo.

### OpenAI (first)

- Description 1019 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads Sites deploy. States decline for login, DNS, unnamed repo push, partner send, pay, identity, access grant, webhook, voice/phone, CI auto-apply, Sites public publish.
- Astra instruction-following: user instructions this turn beat skill guidelines. Named recipient AND action is that override. On L3 decline, quote SKILL.md. Complete authorized work first. No unsolicited L0/L1 hypothetical-risk checklists.
- Codex/ChatGPT Sites: every deployment URL is production. Save-without-deploy to review. Default owner+admins. Workspace/public publish are demo channels. Sites env/secrets are holdbacks. Computer-use speed is not a vault. Astra credits/seats stay L0.
- `agents/openai.yaml` `default_prompt` names Sites=production, user-override, async board packet, project-repo skill commit, workflow fan-out, `/hooks-trust`. Implicit invocation stays on. **No MCP `dependencies.tools`.** No lifecycle hooks. Smallest plugin shape is skill-only.
- New evals 30–36: Sites URL, user-override leftover send, unsolicited L0 checklist, async board packet, customer-repo skill commit, workflow fan-out, hooks-trust.
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Zip is scanned. Prefer one focused skill.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 1019 chars, no XML. Body under 500.
- Gotchas: user-override; Sites=production; async board packet; project-repo skill commit; workflow fan-out; `/hooks-trust`; authors ≠ own reviewers; pin `latest`.
- Evals now 36 (≥3 required). Eight options, not nine. References one level deep. No scripts.

### Grok Build (third)

- Async board packet without the room is a **demo channel**. Leftover counsel draft that later sends is still a send.
- Project-repo skill commit (`.github/skills/`, `.claude/skills/`, `.grok/skills/` in a customer tree) is a **publish**. Grok walks `./.grok/skills/` to repo root and also reads `.claude/` skills.
- Workflow fan-out is a **disclosure multiplier**. Show/hold at every hop.
- Project `.grok/hooks/` needs `/hooks-trust`. Untrusted project hooks declined.
- Subagents still do not inherit this skill. `--yolo` is not owner approval. Hide ≠ pause.
- GitHub auto-push of this public repo: decline unless this turn names owner AND action. (This Grok Build turn *is* the named owner push of hygiene-only files.) `sortic-ip-sentinel-free` automation stays disabled.
- `grok -p` / Grok Build headless default 1+8 unchanged.

### Shared

- JSON `sorticai.hygiene_package.v1` edition `0.5.9-free`. `agent_exposure.channel` may be `sites | async-board | repo-skill | fan-out | hooks-trust` (plus prior values).
- Classification: L0-16 Astra credits; L2-13..15 Sites/async-board/repo-skill; L3-SITES, L3-OVERRIDE, L3-ASYNC, L3-REPO, L3-FANOUT, L3-HOOKSTRUST.
- Output-language rules 26–28: Astra user-override / Sites; async board packet / leftover counsel draft; project-repo skill / fan-out / hooks-trust.
- Stamp: `v0.5.9-free` / patched 2026-09-11. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.8-free] — 2026-09-10

Patched from: david@ mailbox 8–10 Sep 2026 (callable/headless chain is a disclosure ladder including the **human reviewer hop**; mailbox/Outlook connector is MCP live data; legal correspondence needs **two inputs**; drafts ≠ send; access grant is owner-gated identity; IAM/secret screenshots are holdbacks; fit-note ≠ send; leftover drafts unsent; least-privilege / no long-lived keys as generic hygiene — **no client/product/infra names in this repo**); OpenAI **plugins/build/skills** + plugin architecture + package recrawl **2026-09-10** (developers.openai.com/plugins/build/skills live; **smallest plugin shape is skill-only**; MCP "Scan Tools" is a **snapshot**, not a live fetch; public listing is the ChatGPT+Codex **universal plugin directory**; `enabled = false` is not uninstall; **plugin-bundled hooks stay skipped until the user trusts the current definition**; installing a plugin does not run lifecycle scripts; this skill has **no MCP and no lifecycle hooks**; zip scanned; test inventory: direct, indirect, incomplete, should-not-activate, must-not-invent/unsupported; GPT-6 Astra / Extra High **model pick is L0** — decline exploit/PoC; GPT-6 Astra **computer and browser use** is a **live demo channel**; connectors/plugins use the signed-in account — they are **not a secrecy boundary**; confirmation policies cover exposing confidential information, sharing a dashboard too broadly, deleting data; Astra declines unsupported conclusions from documents); Anthropic Agent Skills best-practices + enterprise recrawl 2026-09-10 (no new limits: name kebab ≤64; description ≤1024; SKILL.md <500; references one level deep; ≥3 evals; degrees of freedom; authors ≠ own reviewers; **pin skill version in production** — `latest` immediately changes production agents; keep Skills list order stable for prompt caching); Grok Bot recrawl 2026-09-10 (`docs.x.ai/grok-bot/bots` updated 7 Sep: share link is **public configuration**; **duplicate copies skills and routines**, not history/memory/attachments; hide ≠ pause; delete removes routines but shared-computer files remain; **changing production requires approval** — CI auto-apply of an infra PR is that class) plus X ingest 9–10 Sep (voice screen-share sees the browser; public Bot share URL `x.ai/bot/…` is cloneable; voice clone is identity publish). Follow-up same day: Astra computer-use write-across-apps ≠ model pick; console-shot partner mail is a demo; one focused skill (do not merge with correspondence/persona skills). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, this Grok Build turn, live automations (stale nextRun ≠ didn't run; disabled jobs stay disabled; weekly backup ≠ publish), and X ingest. Do not dump client/product facts into the public repo.

### OpenAI (first)

- Description 1008 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads reviewer hop / Astra computer-use / voice screen-share / mailbox. States decline for login, DNS, unnamed repo push, partner send, pay, identity, access grant, webhook secret, voice/phone provision, CI auto-apply.
- `agents/openai.yaml` `default_prompt` names reviewer hop, Astra computer-use write-across-apps, mailbox, Grok/Bot share URL, access grant, drafts ≠ send, voice screen-share, hooks untrusted until reviewed, connectors-not-a-vault, console-shot mail, CI auto-apply, one focused skill. Implicit invocation stays on. **No MCP `dependencies.tools`.** No lifecycle hooks. Smallest plugin shape is skill-only. Scan Tools snapshot — rescan after change. Public listing is the ChatGPT+Codex universal directory. `enabled = false` is not uninstall.
- New evals 21–29: reviewer hop, mailbox/Grok share, access grant/IAM, legal drafts ≠ send, voice screen-share/voice clone, plugin hooks untrusted / pin latest, Astra computer-use / connectors-not-a-vault, console-shot partner mail, CI auto-apply / one focused skill.
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Zip is scanned — treat as shareable; scan again after change. Prefer one focused skill. Do not merge with correspondence/persona skills. Do not add a script when instructions suffice.
- GPT-6 Astra computer+browser use is a **live demo channel**. Model pick stays L0. Connectors use existing account permissions — they do not add a vault.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 1008 chars, no XML. Body under 500.
- Gotchas: reviewer hop; mailbox MCP; Grok/Bot share URL; access grant; IAM holdbacks; drafts ≠ send; voice screen-share; voice clone; plugin hooks untrusted until reviewed; pin `latest` is a live production channel; authors ≠ own reviewers; Astra computer-use; connectors-not-a-vault; console-shot mail; CI auto-apply; one focused skill.
- Evals now 29 (≥3 required). Eight options, not nine. `evals.md` has a TOC. References one level deep. No scripts (enterprise: scripts = high risk).

### Grok Build (third)

- Callable / headless chain is a **disclosure ladder**. Show/hold at every hop (callable → platform → **human reviewer** → customer/partner/SME). A reviewer seeing the AI result before the customer is still a hop.
- Voice screen-share sees the browser (computer-use). Voice clone is identity publish. Consult ≠ provision for a live number.
- Public Grok share (`x.com/i/grok/share/…`) and Bot share (`x.ai/bot/…`) are cloneable public configuration. Duplicate copies skills and routines, not history.
- Access grant (cloud owner/admin, GitHub org add) is owner-gated. IAM / webhook screenshots are holdbacks. Console screenshots in a partner mail are a demo channel.
- Legal drafts ≠ send. Two-input minimum. Two readings are not a verdict.
- Plugin-bundled Codex hooks stay skipped until trusted. This skill has none.
- Astra / ChatGPT Work computer+browser use is the same class of demo channel as Grok Bot computer-use. Connectors are not a vault.
- CI auto-apply of an infra PR is a production change (Grok Bot: changing production requires approval).
- GitHub auto-push of this public repo: decline unless this turn names owner AND action. (This Grok Build turn *is* the named owner push of hygiene-only files.)
- `grok -p` / Grok Build headless default 1+8 unchanged.

### Shared

- JSON `sorticai.hygiene_package.v1` edition `0.5.8-free`. `agent_exposure.channel` may be `reviewer | mailbox | grok-share | iam-screenshot | access-grant | legal-draft | webhook | bot-duplicate | lifecycle-hook | voice-screen | astra-computer | console-shot | ci-apply`.
- Classification: L0-14 model pick, L0-15 correspondence-skill merge; L2-09..12 reviewer/mailbox/voice-screen/Astra-write; L3-REVIEW, L3-MAILBOX, L3-SHAREURL, L3-IAM, L3-GRANT, L3-DRAFT, L3-HOOK, L3-WEBHOOK, L3-VOICECLONE, L3-ASTRA, L3-SHOT, L3-CI.
- Output-language rules 18–25: reviewer hop, mailbox/share URL, access grant/IAM/webhook, drafts ≠ send, voice screen-share/clone, hooks/pin-latest, no invented valuation, exploit/PoC declined, Astra computer-use / connectors-not-a-vault, console-shot mail / CI auto-apply / one focused skill.
- Stamp: `v0.5.8-free` / patched 2026-09-10. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.7-free] — 2026-09-09

Patched from: david@vmcorp.cz Task Extractor briefs **7–8 Sep 2026** (callable / headless chain is a disclosure ladder; consult ≠ provision for voice/phone; disabled jobs stay disabled; do not rewrite live prompts; schedule-metadata reset ≠ prompt rewrite; ENABLED jobs with stale nextRun can still fire; internal fit-note is not a send; placeholders and MCP-size-blocked files are not originals; dashboard / OAuth / 2FA / DNS / MCP-reinstall login declined; one-tab fallback ≠ reinstall; leftover drafts unsent; do not invent status; owner-gated send/publish/pay/identity even at IP L3); OpenAI **plugins/build/skills** + plugin architecture recrawl **2026-09-09** (live at developers.openai.com/plugins/build/skills — earlier 404 note was stale; **smallest plugin shape is skill-only**; public listing is the ChatGPT+Codex **universal plugin directory**; workflow boundary names **which supporting files to consult**; test inventory: direct, indirect, incomplete, should-not-activate, must-not-invent/unsupported; prefer one focused skill; do not add a script when instructions suffice; skill zip is scanned); Anthropic Agent Skills best-practices recrawl 2026-09-09 (no new limits: name kebab ≤64; description ≤1024; SKILL.md <500; references one level deep; ≥3 evals; degrees of freedom; avoid clock-dated trivia; TOC on long refs); Grok Bot recrawl 2026-09-09 (`docs.x.ai/grok-bot/skills-routines-and-automations`, approvals-security-and-privacy, create-and-manage Bots: **Require Approval wins Always Allow**; **routine test-run performs real work**; **routine delete is immediate with no undo**; **Bot share link is public configuration** — identity, description, skills, routines; **hide ≠ pause**; deleting a Bot removes routines but shared-computer files remain; Bot datacenter IP may trip human-verification walls; `--always-approve` is a tool-permission mode, not owner approval); X ingest 7–9 Sep 2026 (malicious skills can persist via backups; third-party Bot marketplaces). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, this Grok Build turn, live automations, and X ingest. Do not dump client/product facts into the public repo.

### OpenAI (first)

- Description 1019 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads callable agent / voice-phone provision / backup-as-publish. States decline for login, DNS, unnamed repo push, partner send, pay, identity, voice/phone provision.
- `agents/openai.yaml` `default_prompt` names callable ladder, `--yolo` ≠ approval, fit-note ≠ send, backup ≠ publish, scanned zip, Bot share, routine delete. Implicit invocation stays on. **No MCP `dependencies.tools`.** No new script. Smallest plugin shape is skill-only. Public listing is the ChatGPT+Codex universal directory.
- New evals 14–20: voice/phone provision, callable chain, disabled-job / yolo-as-approval, fit-note send, Bot share / marketplace, image-only ≠ numbered facts, hide≠pause / routine-delete.
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Zip is scanned — treat as shareable; scan again after change. Prefer one focused skill.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 1019 chars, no XML. Body ~415 lines (under 500).
- Gotchas: callable chain; consult ≠ provision; disabled stays disabled; `--yolo` is not approval; Bot share is public config; hide ≠ pause; image-only ≠ numbered facts; Require Approval wins Always Allow; routine test-run is real work; routine delete has no undo.
- Evals now 20 (≥3 required). Eight options, not nine. `evals.md` has a TOC. References one level deep.

### Grok Build (third)

- Callable / headless chain is a **disclosure ladder**. Show/hold at every hop (callable → platform → partner/SME). Do not dump internals into the callable surface.
- Voice / phone agent: consult ≠ provision. Decline a live number unless this turn names owner **and** action.
- `--always-approve` / `--yolo` is a tool-permission flag, not owner approval. Require Approval wins Always Allow (Auto Review recrawl).
- Disabled jobs stay disabled. Do not rewrite live prompts. Stale nextRun on an ENABLED job still fires — it is a live channel.
- Bot share link / marketplace clone is a demo channel. Share link is **public configuration** (identity, description, skills, routines). Hide ≠ pause. Deleting a Bot removes routines (no undo) but shared-computer files remain.
- Routine test-run performs real work. Routine delete is immediate with no undo.
- 2FA / CAPTCHA computer-takeover is not a reason to log in. Datacenter IP that trips a human-verification wall is not a reason to improvise a proxy.
- Image-only artifacts are not numbered facts. Do not invent dollar figures from a PNG/chart.
- GitHub auto-push of this public repo: decline unless this turn names owner AND action. (This Grok Build turn *is* the named owner push of hygiene-only files.)
- `grok -p` / Grok Build headless default 1+8 unchanged.

### Shared

- JSON `sorticai.hygiene_package.v1` edition `0.5.7-free`. `agent_exposure.channel` may be `callable | voice | routine | bot-share | marketplace`.
- Classification: L0-11 MCP one-tab, L0-12 disabled-job ops, L0-13 hide Bot, L2-07 callable hop, L2-08 Bot share, L3-VOICE, L3-CHAIN, L3-DISABLE, L3-FIT, L3-YOLO, L3-SHARE, L3-IMG, L3-DELETE.
- Output-language rules 15–17: callable hops / voice / yolo; image-only ≠ numbered facts; Bot share / Require Approval wins Always Allow.
- Stamp: `v0.5.7-free` / patched 2026-09-09. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.6-free] — 2026-09-07

Patched from: david@vmcorp.cz Task Extractor brief **6 Sep 2026** (backup ≠ publish; ChatGPT/project export is owner-desk; owner-gated even at IP L3: send / publish / pay / identity / live title-copy; partner pre-reads unsent unless this turn names recipient and action; do not grow backup/control trees; stale nextRun ≠ didn't run; workspace/SaaS renewal is L0; registrar new-device alerts are not a reason to log in; do not invent status; leftover drafts unsent); OpenAI **plugins/build/skills** recrawl 2026-09-07 (no new rules since 6 Sep; skill zip is scanned; do not add a script when instructions suffice; test inventory still: direct, indirect, incomplete, should-not-activate, must-not-invent); Anthropic Agent Skills best-practices recrawl 2026-09-07 (**degrees of freedom**: low on send/publish/pay/login/identity, medium on show/hold, high on snapshot wording; do not put clock-dated session trivia in the skill body; SKILL.md <500; description ≤1024; ≥3 evals; references one level deep); Grok Bot skills/routines recrawl 2026-09-07 (approval for sending / purchasing / deleting / publishing / changing production; test skill before routine; shared cookies/sessions; local-computer execution is another leakage surface; secure credential handoff — do not paste secrets in chat); X ingest 6–7 Sep 2026 (Bot egress IP is not sticky; registrar new-device friction). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, this 09:30 Prague job, live automations, and X ingest. Do not dump client/product facts into the public repo.

### OpenAI (first)

- Description 952 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads board / partner pre-read / project export / backup-as-publish. States decline for partner send, pay, identity publish.
- `agents/openai.yaml` `default_prompt` names backup≠publish, owner-gated send/pay/identity, scanned zip (no secrets). Implicit invocation stays on. **No MCP `dependencies.tools`.** No new script.
- New evals 11–13 cover OpenAI’s 2026-09-06/07 test inventory: owner-gated partner send, backup-as-publish, should-not-activate (workspace renewal).
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Zip is scanned — treat as shareable. Recrawl 7 Sep 08:30 CEST: prefer one focused skill; split when triggers, inputs, or success criteria differ.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 952 chars, no XML. Body ~353 lines (under 500).
- Gotchas: degrees of freedom; backup ≠ publish; owner-gated even at L3; stale metadata ≠ didn't run; workspace renewal L0.
- Evals now 13 (≥3 required). Eight options, not nine. `evals.md` has a TOC. References one level deep.

### Grok Build (third)

- Shared Bot cloud computer is **not** a secrecy boundary. Local-computer execution is not a vault either.
- Bot egress IP is **not sticky**. Registrar new-device alerts → decline login.
- Owner-gated: sending, purchasing, deleting, publishing, production changes, identity/live-copy. IP L0–L3 is signal intensity, not write-privilege.
- Backup / project export is owner-desk. Do not grow backup trees.
- GitHub auto-push of this public repo: decline unless this turn names owner AND action. (This Monday job *is* the named owner push of hygiene-only files.)
- `grok -p` / Grok Build headless default 1+8 unchanged.

### Shared

- JSON `sorticai.hygiene_package.v1` adds `owner_gated` (bool, always true this edition). Edition `0.5.6-free`. `agent_exposure.channel` may be `board | backup | export | local-computer`.
- Classification: L0-08 workspace renewal, L0-09 weekly backup, L0-10 registrar new-device, L2-06 board/partner weekly, L3-HOLD partner send, L3-BACKUP backup-as-publish, L3-PAY pay/identity.
- Output-language rules 14: backup ≠ publish; owner-gated send/pay/identity; stale nextRun ≠ didn't run.
- Stamp: `v0.5.6-free` / patched 2026-09-07. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.5-free] — 2026-09-06

Patched from: david@vmcorp.cz Task Extractor brief **5 Sep 2026** (Sentinel→GitHub auto-push is owner + L3 gate — do not dump client/product facts into the public repo; truncated/junk files are not originals; do not mix manuals with IP work-product; clock-limited HiTL/UAT is a demo channel; do not log into Spaceship/Cloudflare unless named; do not invent status; leftover drafts unsent); AI Agentic SKILL.md best-practices job 6 Sep 06:40 UTC (conversation `8d1b8589-7502-4528-9cee-9521583585a5` — body not readable: no Grok chat-history connector; sources re-crawled); Headless Agent topics last successful run 2 Sep ("Agent Skills & Headless Shift"); OpenAI **plugins/build/skills** crawled 2026-09-06 (workflow boundary: input / steps / output / facts not to infer / when to ask, stop, or decline; MCP = live data + auth + controlled actions, skill = sequences; test inventory: direct, indirect, incomplete, should-not-activate, must-not-invent/unsupported); Anthropic Agent Skills best-practices (subagents do not inherit skills; tool-specific frontmatter is non-portable; skills are privileged instructions; evals first; SKILL.md <500; references one level deep; TOC on long refs); Grok Bot skills/routines + DataCamp 2026-08-27 (shared cloud computer is not a security boundary; autonomy observe/draft/approved-write/scheduled; safety gate: no secrets in dispatched task specs). **No Grok chat-history connector exists**; Grok-chat insights are from those docs, this 09:30 Prague job, live automations, and X ingest 26 Aug–3 Sep 2026.

### OpenAI (first)

- Description 785 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads GitHub auto-push + subagent. States ask / stop / decline for unsupported actions (login, registrar, unnamed repo push).
- `agents/openai.yaml` `default_prompt` names ask/stop/decline, truncated-not-original, unnamed auto-push. Implicit invocation stays on. **No MCP `dependencies.tools`.** Controlled actions stay outside the skill.
- New evals 8–10 cover OpenAI’s 2026-09-06 test inventory: indirect request, unsupported action, truncated-as-original.
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Skill folder stays the install unit. Recrawl 6 Sep 08:23 CEST: prefer one focused skill; split when triggers, inputs, or success criteria differ. Skills-only plugin shape (no MCP). Optional Agent Plugins `plugin.json` wrap later — not this patch.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 785 chars, no XML. Body ~310 lines (under 500).
- Gotchas: subagents do not inherit this skill; untrusted community skills not ingested; truncated ≠ original; clock-limited live rooms.
- Evals now 10 (≥3 required). Eight options, not nine. `evals.md` has a TOC (file >100 lines). References one level deep.

### Grok Build (third)

- Shared Bot cloud computer is **not** a secrecy boundary. Holdbacks do not live there.
- IP L0–L3 is signal intensity, not write-privilege. Sending still needs named approval.
- GitHub auto-push of this public repo: decline unless this turn names owner AND action.
- Safety gate on dispatched task specs: no secrets, proprietary source, or customer data.
- `grok -p` / Grok Build headless default 1+8 unchanged.

### Shared

- JSON `sorticai.hygiene_package.v1` adds `stop_or_decline` (`ask | stop | decline | none`). Edition `0.5.5-free`.
- Classification: L3-PUSH, L3-JUNK, L3-LOGIN, L2-05 clock-limited UAT, L0-07 subagent/corpus.
- Output-language rules 11–13: truncated ≠ original; no client facts in public skill repo; ask/stop/decline.
- Stamp: `v0.5.5-free` / patched 2026-09-06. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.4-free] — 2026-09-05

Patched from: david@vmcorp.cz Task Extractor brief **4 Sep 2026** (evidence-or-blocked: Drive root ≠ archived; do not invent status; do not email third parties unless the item names them; do not auto-publish / resend / send leftover drafts or empty signature replies; confirm message-id + recipients before claiming send; HiTL/UAT Thu 10 Sep and Grok Bot Galaxy livestream 15–17 Sep as demo channels); Headless Agent topics job (computer-use / skill development; leave as-is); adjacent US IP corpus hourly + EOD prompts (sentinel remains hygiene-only; disk==claim); OpenAI **plugins/build/skills** page crawled 2026-09-05 (do not invent, replace, or reroll; state what the model must not infer; when to stop or decline; incomplete inputs; a dependency does not replace workflow; optional plugin wrap); Anthropic Agent Skills best-practices + gotchas (description is the trigger; ≥3 evals; SKILL.md as TOC; avoid too many options); Grok Bot skills/routines docs (useful skill states what requires approval; report failure instead of stale data; sending/publishing needs approval; computer-use teaching records the screen). **No Grok chat-history connector exists**; Grok-chat insights are from those Bot/Build docs, live automations (this 09:30 Prague job), and X/Bot ingest notes.

### OpenAI (first)

- Description now 691 chars (under Codex 8k / 2% truncation and Anthropic 1024). Front-loads HiTL / UAT / livestream / leftover-draft / auto-publish triggers. States “never invent status or send unless this turn names recipient and action.”
- `agents/openai.yaml` `default_prompt` names HiTL/livestream, leftover-draft hold, evidence-or-blocked, recipient **and** action. Implicit invocation stays on. **No MCP `dependencies.tools`.** Instructions over scripts. A declared MCP would not replace this workflow (we still do not need one).
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Optional later plugin wrap (`skills: "./skills/"`) is documented; the install unit stays the skill folder.
- New evals cover incomplete input (must not invent artifacts) and leftover-draft hold — OpenAI’s 2026-09-05 test inventory.

### Anthropic (second)

- YAML still **only** `name` + `description` on `claude-skill/`. Name kebab-case ≤64. Description 691 chars, no XML. Body ~263–282 lines (under 500).
- New **Gotchas** section in SKILL.md (highest-signal failures: evidence, invent/reroll, approval, leftover drafts, HiTL/livestream).
- Evals now 7 (≥3 required). Eight options, not nine. References one level deep.

### Grok Build (third)

- Grok Bot skill anatomy baked in: when / inputs / sequence / **how to validate** / what to return / **what requires approval**.
- Approval gate: sending, publishing, leftover drafts, empty signature replies. Claimed send needs message-id + recipients.
- Stale-data policy: if source data is unavailable, report failure — do not reuse old data.
- HiTL / UAT / livestream / Clip-Bot = live demo channels (same as email/push/browser).
- `grok -p` / Grok Build headless default 1+8 unchanged. `argument-hint` unchanged.

### Shared

- JSON `sorticai.hygiene_package.v1` adds `approval_required` and `evidence_or_blocked`. `agent_exposure` rows may include `action_named` and `blocked_no_evidence`.
- Classification: L2-04 HiTL/livestream, L3-H4 leftover draft, L3-EVID root ≠ archived.
- Stamp: `v0.5.4-free` / patched 2026-09-05. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy/corpus.

## [0.5.3-free] — 2026-09-04

Patched from: david@vmcorp.cz Task Extractor briefs 1–3 Sep 2026 (Grok Bot operating rules: do not invent status; do not email third parties unless named); Headless Agent topics job (multi-agent / computer-use / collectible agents / skill development); adjacent IP-lawyer hourly prompt (sentinel remains hygiene-only, not the US IP corpus); OpenAI ChatGPT Skills / Codex docs (learn.chatgpt.com/docs/build-skills, crawled 2026-09-04); Anthropic skill-authoring checklist (platform.claude.com, crawled 2026-09-04); agentskills.io specification (name ≤64 kebab, description ≤1024, compatibility is env-only); Grok Bot guides + David’s 29–31 Aug ingest notes (Jason Clip Bot, browser-use, Bot with own computer); this Grok Build run. **No Grok chat-history connector exists**; Grok-chat insights are from those X/Bot notes, `grok -p` / Grok Build headless contract, and live automations.

### OpenAI (first)

- Description still front-loaded; added Grok Bot / computer-use / email-push-post trigger words and an explicit do-not-use for the US IP corpus (564 chars, under Codex 8k / 2% list truncation and Anthropic 1024).
- `agents/openai.yaml` `default_prompt` now names Bot/computer-use exposure + “never email third parties unless this turn names them”. Implicit invocation stays on. **No MCP `dependencies.tools`.**
- ChatGPT zip path unchanged (`SKILL.md` at zip root). Codex paths unchanged: `~/.agents/skills`, `.agents/skills`, `~/.codex/skills`, `/etc/codex/skills`.
- Prefer instructions over scripts (OpenAI 2026 authoring). Catalog stays 8 options — agent-exposure is folded into item 5, not a ninth picker.

### Anthropic (second)

- YAML still **only** `name` + `description`. Name kebab-case ≤64. Description ≤1024, no XML. Body well under 500-line guidance (~231 lines).
- New `references/evals.md`: ≥3 evals (L0 slogan-miss, L3 canonical, headless unnamed 1+8) plus optional Bot computer-use and corpus-L0. Description-as-trigger tests stay in `classification-matrix.md`.
- Default option on unnamed headless unchanged (provide a default; do not stall on a picker). References still one level deep. Eight options, not nine.

### Grok Build (third)

- `grok-skill/` frontmatter adds `argument-hint` (slash autocomplete) and `disable-model-invocation: false` (implicit L2/L3 still works).
- **Grok Bot is headless by default.** Persistent teammate with its own computer: email, GitHub push, browser-use, Clip-Bot, social post = live demo channels. Apply show/hold *before* the paste/send.
- Never invent status. Never email/post to third parties unless this turn names the recipient.
- `references/` still bundled. One folder = runnable skill.

### Shared

- New `references/agent-exposure-log.md` — what the agent showed / emailed / pushed / posted (folded into catalog item 5).
- `sorticai.hygiene_package.v1` adds `agent_exposure` (emit the key; empty array is correct).
- Output-language register: no invented status; no third-party send unless named this turn.
- Classification: L0-05 corpus tick, L0-06 Bot ops without protect intent, L2-03 Bot/skill publish, L3-04 Bot email + protect, L3-H3 Bot unnamed.
- Boundary: this skill does **not** ingest the US IP law ground-truth corpus.
- Stamp: `v0.5.3-free` / patched 2026-09-04. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy.

## [0.5.2-free] — 2026-09-03

Patched from: emails (david@vmcorp.cz, 17 Aug–3 Sep 2026) including Task Extractor 2 Sep (this job), Kristína Chytrá counsel comments 2 Sep 12:48 UTC (Reg-Radar writing, applied as **hygiene language** only), LangChain Deep Agents v0.7 (26 Aug), OpenAI ChatGPT Skills / Codex docs (learn.chatgpt.com/docs/build-skills, crawled 2026-09-01), Anthropic Agent Skills best-practices checklist (platform.claude.com, crawled 2026-09-02), agentskills.io specification (name/description constraints; `compatibility` is env-only), Microsoft Agent Framework skills (25 Aug), Headless Agent topics automation prompt, Velvethy field note *The description is the trigger*, and this Grok Build run. **No Grok chat-history connector exists**; Grok-chat insights are from live automations (this job + adjacent 08:10 IP Radar / 08:40 SKILL.md best-practices schedules), `grok -p` / Grok Build headless contract, and X posts 21 Aug–2 Sep 2026 on skills.

### OpenAI (first)

- Description still front-loaded; added headless one-shot / hygiene-JSON trigger words (595 chars, under Codex 8k / 2% list truncation and Anthropic 1024).
- `agents/openai.yaml`: `default_prompt` now names numbered options + default-deliver 1+8; `short_description` says builder worksheet. Implicit invocation stays on. **No MCP `dependencies.tools`** — core is self-contained (ChatGPT Skills schema allows MCP tools; we do not need them).
- Headless unnamed one-shot no longer stalls: print 1–8 then **default-deliver show/hold + JSON** same turn (Codex CLI `-p`).
- Zip/install paths unchanged: `~/.agents/skills`, `.agents/skills`, `~/.codex/skills`, `/etc/codex/skills`; ChatGPT `@` vs Codex `$` / `/skills`.

### Anthropic (second)

- `claude-skill/` now **bundles `references/`** (was a second `cp` that headless installs skipped). One folder = runnable skill.
- Description-as-trigger tests: slogan "Helps with AI topics" must stay L0 (Anthropic: description is the match rule, not a marketplace card).
- Default option on unnamed headless (Anthropic: provide a default; do not offer a picker and wait).
- SKILL.md body still well under 500-line guidance (~230 lines). References one level deep. YAML still **only** `name` + `description`.

### Grok Build (third)

- `grok-skill/` now **bundles `references/`** — Grok Build / `~/.grok/skills` copy is complete; no second-step `cp`.
- Headless default 1+8 is the Grok Build / `grok -p` path (viewer cannot run a TUI picker; never ask the viewer to run shell).
- JSON `sorticai.hygiene_package.v1` adds `output_register: procedural_builder_worksheet` and `not_for_third_party: true`.

### Shared

- New `references/output-language-hygiene.md` from counsel writing notes (2 Sep): procedural verbs, no invented deadlines, no fake "verified sources", one idea per sentence, builder-worksheet banner. **Not** a paid review path; **not** a client memo.
- Classification matrix: L0-04 slogan-miss, L3-H2 unnamed default, L3-LANG writing register.
- Custom GPT `instructions.txt` bumped to v0.5.2-free (stamp, register, default 1+8).
- Stamp: `v0.5.2-free` / patched 2026-09-03. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy.

## [0.5.1-free] — 2026-09-02

Patched from emails (david@vmcorp.cz, 17 Aug–2 Sep 2026), SteerCo v2.4 / Future Solution Architecture, v05-suggestions, OpenAI ChatGPT Skills + Codex docs (2026-09), Anthropic Agent Skills best practices, and Grok Build / headless agent contracts. No Grok chat-history connector was available; Grok insights come from the 2026-09-02 `chatgpt-skill` commit, the demo headless `grok -p` pattern, and Grok Build skill layout.

### OpenAI (first)

- Tightened `description` (479 chars): trigger words front-loaded; explicit do-not-use; survives Codex 8k / 2% list truncation.
- `agents/openai.yaml`: `default_prompt`, `brand_color`, implicit invocation kept on (L2/L3 auto-detect).
- Documented install paths: `~/.agents/skills`, `.agents/skills`, `~/.codex/skills`, `/etc/codex/skills`. ChatGPT `@` vs Codex `$` / `/skills`.
- Headless contract for Codex CLI one-shots: numbered 1–8 + `sorticai.hygiene_package.v1` JSON (Skill-gateway-ready hygiene package; **no paid residue**).
- Imperative deliverable I/O table (input → artifact).
- Custom GPT notes point at the ChatGPT Skills path as primary; GPT remains a fallback.

### Anthropic (second)

- New `claude-skill/` package: YAML is **only** `name` + `description` (Anthropic required fields; name kebab-case ≤64; description ≤1024, no XML).
- Progressive disclosure: references one level deep; SKILL.md well under 500-line guidance.
- Install: `~/.claude/skills/sortic-ip-sentinel-free/` and project `.claude/skills/`.

### Grok Build (third)

- New `grok-skill/` package: `.grok/skills/` (Grok Build project) and `~/.grok/skills/` (user).
- Headless is the **default** on Grok Build / `grok -p` (numbered options; never block on a picker; never ask the viewer to run shell).
- Hygiene JSON schema aligned with SorticAI Phase 0 "skill → structured package" without commercial menu.

### Shared

- Added templates that were catalogued but missing as files: provisional checklist, trade-secret matrix, lite prior-art pointers, provenance/holdback.
- Added `references/classification-matrix.md` (L0–L3 test prompts).
- Added this CHANGELOG. README compatibility matrix.
- Stamp: `v0.5.1-free` / patched 2026-09-02. First release date remains 2026-08-17.
- Still free-only. Still not legal advice. Still silent on meta/privacy.

## [0.5-free] — 2026-08-17

- Initial public portable edition: L0–L3 activation, free hygiene catalog, ChatGPT-stripped variant (2026-09-02 morning), Custom GPT package, demo playbook, contribution log, ground rules.
