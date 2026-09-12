# SorticAI Free IP Sentinel

**The skill that quietly protects your IP at the exact moment you need it.**

Free portable IP-sensitive moment detector + hygiene sentinel (**v0.5.11-free**).
Detects “protect the IP”, investor demos, pilot showcases, fundraising decks, **and headless/Grok Bot/computer-use/HiTL/livestream exposure**… and delivers only free procedural hygiene:

- Show / hold maps
- Staged disclosure ladders
- Investor & partner demo hygiene playbook
- AI / human contribution logs (USPTO 2025 aligned)
- Agent / computer-use exposure logs (what the Bot showed, emailed, pushed, posted, livestreamed)
- Approval gate (recipient AND action named this turn; leftover drafts unsent)
- Owner-gated even at IP L3 (send / publish / pay / identity / live-copy)
- Backup ≠ publish; project export is owner-desk
- Evidence-or-blocked (done requires path+link)
- Ask / stop / decline (incomplete → ask; leftover/truncated/backup-tree → stop; login/unnamed public push/partner send/pay/identity → decline)
- Shared Bot computer is not a secrecy boundary; local-computer execution is not a vault; subagents do not inherit this skill
- Bot egress IP is not sticky — registrar new-device alerts → decline login
- Provisional readiness checklists
- Provenance & holdback audits
- Callable / headless chain is a disclosure ladder (show/hold at every hop)
- Voice/phone provision: consult ≠ provision (owner-gated decline)
- `--yolo` / `--always-approve` is not owner approval; disabled jobs stay disabled
- Fit-note / adjacent-demand analysis is not a send
- Placeholders and MCP-size-blocked files are not originals
- Headless hygiene package JSON (`sorticai.hygiene_package.v1`)
- Builder-worksheet language register (procedural, not advisory)
- Reviewer hop is a disclosure hop; mailbox connector is MCP (this skill has none)
- Public Grok share / `x.ai/bot/…` is cloneable config; access grant is owner-gated
- Legal drafts ≠ send; voice screen-share sees the browser; voice clone is identity
- Plugin-bundled hooks untrusted until reviewed; pin `latest` is a live production channel
- GPT-6 Astra computer+browser use is a live demo channel (model pick stays L0); connectors are not a vault
- Console screenshots in a partner mail are a demo; CI auto-apply is a production change
- One focused skill — do not merge with correspondence/persona skills
- Sites deploy URL is production (save-without-deploy to review; env/secrets are holdbacks)
- User instructions this turn beat skill guidelines; named recipient AND action is the override
- Async board packet without the room is a demo; project-repo skill commit is a publish
- Workflow fan-out is a disclosure multiplier; project `.grok/hooks/` needs `/hooks-trust`
- Remote Mac / phone-driven desktop is computer-use; Messages/Mail typing is a send
- Live `isEnabled` is evidence — do not invent disabled from a prior brief
- Workspace-shared plugin / Copilot `.github/skills/` is a publish
- Responses API Skills are versioned bundles — pin an integer version, not `latest`
- Three zip layouts (Skills tab = `SKILL.md` at zip root; Agent Plugins = `plugin.json` + `skills/<name>/SKILL.md`; Claude archive = `.claude-plugin/plugin.json` + `skills/<name>/SKILL.md`)
- Counsel-release is a send; "waiting for legal review" is an internal hold
- Public Bot livestream of internals is a demo; attending is L0
- Demonstration-to-skill is a publish (Teach-by-demonstration records the screen)

**Not legal advice. No guarantees. Free only.** Outputs are builder worksheets — do not send them to third parties as legal analysis.

Works on **Codex**, **ChatGPT Skills**, **Claude Code**, **Grok / Grok Build / Grok Bot**, Cursor, Microsoft Agent Framework, and any [agentskills.io](https://agentskills.io) runtime.

Shareable one-pager: [EXEC-SUMMARY.md](EXEC-SUMMARY.md). What landed: [CHANGELOG.md](CHANGELOG.md).

---

## Which folder do I install?

| Host | Folder in this repo | Install |
|------|---------------------|---------|
| **OpenAI Codex** | [`chatgpt-skill/`](chatgpt-skill/) | `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free` (also works at `~/.codex/skills/` or project `.agents/skills/`) |
| **ChatGPT Skills** | [`chatgpt-skill/`](chatgpt-skill/) | Zip that folder → Skills tab (Business / Enterprise / Edu). Invoke with `@`. |
| **Anthropic Claude Code** | [`claude-skill/`](claude-skill/) | `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free` (`references/` is bundled) |
| **Grok / Grok Build / Grok Bot** | [`grok-skill/`](grok-skill/) | `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free` or project `.grok/skills/` (`references/` is bundled) |
| **Any agentskills.io host** | repo root | Root `SKILL.md` + `references/` |

Root `SKILL.md` is the canonical behaviour file (rich frontmatter). Platform folders tune **frontmatter and install only**. Hygiene behaviour is the same.

Custom GPT fallback: [`openai-gpt-package/`](openai-gpt-package/).

---

## Usage triggers (examples)

- L3: "protect the IP", "IP sensitive moment", "trade secret before investor demo", "how to protect this before we file", "NDA before sharing the protocol", "the Grok Bot will email the deck — protect the IP", "callable agent into the partner network — protect the IP".
- L2 exposure: "investor demo in 10 days", "publish the Bot and post a clip", or "board/partner weekly" → soft tip only.
- L0: privacy, config, meta on this skill, slogan "Helps with AI topics", US IP corpus ticks → silent.

Headless one-shot (Codex / Claude / grok `-p` / Grok Bot): add "Output numbered options and hygiene package JSON." If you omit that, the skill still **default-delivers show/hold + JSON** so the unattended run is not blank. It will **not** email/post leftover drafts, partner pre-reads, or treat a backup as publish unless this turn names the recipient **and** the action. Unnamed GitHub auto-push, registrar/DNS/dashboard logins, pay, identity publish, voice/phone provision, disabled-job re-enable, live-prompt rewrite, and fit-note send are **declined**. `--yolo` is not approval. Done requires evidence. Truncated files are not originals. Workspace renewal is silent.

---

## Compatibility (v0.5.11)

| Rule | OpenAI | Anthropic | Grok Build / Bot |
|------|--------|-----------|------------------|
| Frontmatter | `name` + `description` (+ optional `license`/`metadata`); extra keys in `agents/openai.yaml` | **Only** `name` + `description`; name kebab-case ≤64; description ≤1024 | Rich keys ok (`when-to-use`, `argument-hint`, metadata) |
| Description | Front-load triggers (list may be truncated to 8k / 2% context) | What + when + do-not-use; slogan-miss stays L0 | Same description |
| Invocation | ChatGPT `@` · Codex `$` / `/skills` · implicit | implicit + `/skill` | implicit + `.grok/skills` + slash `argument-hint` |
| Headless | Numbered 1–8; unnamed → default 1+8 JSON; leftover drafts held | Same + gotchas | Numbered 1–8 **default**; Bot = headless; approval + evidence-or-blocked |
| Progressive disclosure | Load `references/` on demand | One-level-deep; SKILL.md <500 lines; ≥3 evals | Same |
| Package | `references/` bundled | `references/` bundled | `references/` bundled |

---

**Weekly updates**
This skill is kept current by a research loop (agentskills.io, USPTO/EPO high-level guidance, host skill specs, Headless/Bot topics). Changelog every patch.

**Sources (high-level)**
EPO Guidelines, USPTO 2025 AI inventorship guidance, WIPO principles.

**Disclaimer:** This is free procedural hygiene support only. **Not legal advice.** No guarantees. Consult qualified counsel.
