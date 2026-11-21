# SorticAI Free IP Sentinel

**What it is.** Free IP Sentinel is a free skill by SorticAI (edition 0.5.81-free). It notices IP-sensitive moments and gives builder worksheets, so you can decide what to show and what to hold.

**Who it is for.** Builders who are about to show their work: an investor demo, a fundraising deck, a partner share or pre-read, a publish, or an agent that is about to show, send, push or post the work.

**Try it**

1. Pick the folder for your host in [Which folder do I install?](#which-folder-do-i-install).
2. Copy it in using that row (`cp -r`, or zip the folder when the row says zip).
3. Ask a trigger question from [Usage triggers (examples)](#usage-triggers-examples), for example "protect the IP".

Free portable IP-sensitive moment detector + hygiene sentinel (**v0.5.81-free**).
Host-read notes: [docs/host-reads.md](docs/host-reads.md).

## Claude

Upload, copy, or API. `python3 scripts/build-packs.py` writes the Claude archive as `dist/sortic-ip-sentinel-free.zip`. The only top folder in that zip is `sortic-ip-sentinel-free/`, the same as `name`, and `SKILL.md`, `references/`, `README.md`, and `LICENSE.md` sit inside it. Paste-in nudge and the install check: [claude-skill/SETUP.md](claude-skill/SETUP.md).

**claude.ai and Claude Desktop.** Upload that zip as a custom skill. Code execution must be enabled. Source: [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

**Claude Code.** Copy the pack to `~/.claude/skills/sortic-ip-sentinel-free/` or a project's `.claude/skills/sortic-ip-sentinel-free/`. Check with `/sortic-ip-sentinel-free` and ask `What skills are available?`. Source: [Extend Claude with skills](https://code.claude.com/docs/en/skills).

**API.** Follow Anthropic's Skills guide. This page does not add steps. Source: [Using Agent Skills with the API](https://docs.claude.com/en/build-with-claude/skills-guide).

**Not legal advice. No guarantees. Free only.** Outputs are builder worksheets — do not send them to third parties as legal analysis. A skill is an instruction package. This free skill stays instructions-only: no scripts in the skill, no paid paths, no secrets. Progressive disclosure: load `references/` on demand.

Packaged for ChatGPT, Claude, Cursor and Grok Bot.

Shareable one-pager: [EXEC-SUMMARY.md](EXEC-SUMMARY.md). Lunch HITL: [HITL-LUNCH.md](HITL-LUNCH.md). What landed: [CHANGELOG.md](CHANGELOG.md).

---

## Which folder do I install?

ChatGPT Skills needs a ChatGPT Business, Enterprise or Edu plan.

| Host | Folder in this repo | Install |
|------|---------------------|---------|
| **OpenAI Codex** | [`chatgpt-skill/`](chatgpt-skill/) | `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free` (also works at `~/.codex/skills/` or project `.agents/skills/`) |
| **ChatGPT Skills** | [`chatgpt-skill/`](chatgpt-skill/) | Zip that folder → Skills tab (Business / Enterprise / Edu). Invoke with `@`. |
| **Anthropic Claude** | [`claude-skill/`](claude-skill/) | Claude Code: `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free` (`references/` is bundled). claude.ai, Desktop, and the API: [Claude](#claude). |
| **Grok / Grok Build** | [`grok-skill/`](grok-skill/) | `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free` or project `.grok/skills/` |
| **Grok Bot** | [`grok-skill/`](grok-skill/) zip | Save / Plugins → **enable per-Bot**. Not `cp` to `~/.grok/skills/` (that is Build). Do not Teach-to-install. |
| **Cursor** | [`cursor-skill/`](cursor-skill/) | Cloud Agents: `cp -r cursor-skill .cursor/skills/sortic-ip-sentinel-free/`. Sync Skills = `~/.cursor/skills/` only. Custom Modes = pin skill. |
| **Grok Bot share pack** | [`grok-bot-share/`](grok-bot-share/) | Profile/skills/routines config only. **Do not publish live.** Never on the skill zip. |
| **Any agentskills.io host** | repo root | Root `SKILL.md` + `references/` |

Root `SKILL.md` is the canonical behaviour file (rich frontmatter). Platform folders tune **frontmatter and install only**. Hygiene behaviour is the same.

Custom GPT fallback: [`openai-gpt-package/`](openai-gpt-package/).

---

## Usage triggers (examples)

- L3: "protect the IP", "run IP-sensitive moment", "trade secret before investor demo", "how to protect this before we file", "NDA before sharing the protocol", "the Grok Bot will email the deck — protect the IP", "callable agent into the partner network — protect the IP".
- L2 exposure: "investor demo in 10 days", "publish the Bot and post a clip", or "board/partner weekly" → soft tip only.
- L0: privacy, telemetry, debug, config, meta on this skill, slogan "Helps with AI topics", US IP corpus ticks, and a headless, Bot-to-Bot, or computer-use mention that does not show, email, push, post, or pass the work → silent. Older zips shared outside this repository are stale; use the packs built from this repository.

Headless one-shot (Codex / Claude / grok `-p` / Grok Bot): add "Output numbered options and hygiene package JSON." If you omit that, the skill still **default-delivers show/hold + JSON** so the unattended run is not blank. By design, it tells your agent to hold a send, push or post unless that turn names the recipient and the action. Leftover drafts stay drafts, and a backup is not a publish. It is written to decline unnamed GitHub pushes, logins, payments, identity publishing and voice or phone provisioning. `--yolo` is not approval. It is not a security control: keep your host's own approval settings on. Done requires evidence. Truncated files are not originals. Workspace renewal is silent.

---

## Compatibility (v0.5.18)

| Rule | OpenAI | Anthropic | Grok Build / Bot |
|------|--------|-----------|------------------|
| Frontmatter | `name` + `description` (+ optional `license`/`metadata`); extra keys in `agents/openai.yaml` | **Only** `name` + `description`; name kebab-case ≤64 | Rich keys ok (`when-to-use`, `argument-hint`, metadata) |
| Description | Front-load triggers (list may be truncated to 8k / 2% context) | What + when + do-not-use; slogan-miss stays L0 | Same description |
| Invocation | ChatGPT `@` · Codex `$` / `/skills` · implicit | implicit + `/skill` | implicit + `.grok/skills` + slash `argument-hint` |
| Headless | Numbered 1–8; unnamed → default 1+8 JSON; leftover drafts held | Same + gotchas | Numbered 1–8 **default**; Bot = headless; approval + evidence-or-blocked |
| Progressive disclosure | Load `references/` on demand | One-level-deep; SKILL.md <500 lines; ≥3 evals | Same |
| Package | `references/` bundled | `references/` bundled | `references/` bundled |

---

**Sources (high-level)**
EPO Guidelines, USPTO 2025 AI inventorship guidance, WIPO principles.

**Disclaimer:** This is free procedural hygiene support only. **Not legal advice.** No guarantees. Consult qualified counsel.

Free for personal or internal builder use, with attribution and the disclaimer kept (see LICENSE.md). Not an OSI open-source license.
