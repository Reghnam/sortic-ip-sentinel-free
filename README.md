# SorticAI Free IP Sentinel

**The skill that quietly protects your IP at the exact moment you need it.**

Free portable IP-sensitive moment detector + hygiene sentinel (**v0.5.2-free**).
Detects “protect the IP”, investor demos, pilot showcases, fundraising decks… and delivers only free procedural hygiene:

- Show / hold maps
- Staged disclosure ladders
- Investor & partner demo hygiene playbook
- AI / human contribution logs (USPTO 2025 aligned)
- Provisional readiness checklists
- Provenance & holdback audits
- Headless hygiene package JSON (`sorticai.hygiene_package.v1`)
- Builder-worksheet language register (procedural, not advisory)

**Not legal advice. No guarantees. Free only.** Outputs are builder worksheets — do not send them to third parties as legal analysis.

Works on **Codex**, **ChatGPT Skills**, **Claude Code**, **Grok / Grok Build**, Cursor, Microsoft Agent Framework, and any [agentskills.io](https://agentskills.io) runtime.

See [CHANGELOG.md](CHANGELOG.md) for what landed in v0.5.2.

---

## Which folder do I install?

| Host | Folder in this repo | Install |
|------|---------------------|---------|
| **OpenAI Codex** | [`chatgpt-skill/`](chatgpt-skill/) | `cp -r chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free` (also works at `~/.codex/skills/` or project `.agents/skills/`) |
| **ChatGPT Skills** | [`chatgpt-skill/`](chatgpt-skill/) | Zip that folder → Skills tab (Business / Enterprise / Edu). Invoke with `@`. |
| **Anthropic Claude Code** | [`claude-skill/`](claude-skill/) | `cp -r claude-skill ~/.claude/skills/sortic-ip-sentinel-free` (`references/` is bundled) |
| **Grok / Grok Build** | [`grok-skill/`](grok-skill/) | `cp -r grok-skill ~/.grok/skills/sortic-ip-sentinel-free` or project `.grok/skills/` (`references/` is bundled) |
| **Any agentskills.io host** | repo root | Root `SKILL.md` + `references/` |

Root `SKILL.md` is the canonical behaviour file (rich frontmatter). Platform folders tune **frontmatter and install only**. Hygiene behaviour is the same.

Custom GPT fallback: [`openai-gpt-package/`](openai-gpt-package/).

---

## Usage triggers (examples)

- L3: "protect the IP", "IP sensitive moment", "trade secret before investor demo", "how to protect this before we file", "NDA before sharing the protocol".
- L2 exposure: "investor demo in 10 days" → soft tip only.
- L0: privacy, config, meta on this skill, slogan "Helps with AI topics" → silent.

Headless one-shot (Codex / Claude / grok `-p`): add "Output numbered options and hygiene package JSON." If you omit that, the skill still **default-delivers show/hold + JSON** so the unattended run is not blank.

---

## Compatibility (v0.5.2)

| Rule | OpenAI | Anthropic | Grok Build |
|------|--------|-----------|------------|
| Frontmatter | `name` + `description` (+ optional `license`/`metadata`); extra keys in `agents/openai.yaml` | **Only** `name` + `description`; name kebab-case ≤64; description ≤1024 | Rich keys ok (`when-to-use`, metadata) |
| Description | Front-load triggers (list may be truncated to 8k / 2% context) | What + when + do-not-use; slogan-miss stays L0 | Same description |
| Invocation | ChatGPT `@` · Codex `$` / `/skills` · implicit | implicit + `/skill` | implicit + `.grok/skills` |
| Headless | Numbered 1–8; unnamed → default 1+8 JSON | Same | Numbered 1–8 **default** |
| Progressive disclosure | Load `references/` on demand | One-level-deep; SKILL.md <500 lines | Same |
| Package | `references/` bundled | `references/` bundled (v0.5.2) | `references/` bundled (v0.5.2) |

---

**Weekly updates**
This skill is kept current by a research loop (agentskills.io, USPTO/EPO high-level guidance, host skill specs). Changelog every patch.

**Sources (high-level)**
EPO Guidelines, USPTO 2025 AI inventorship guidance, WIPO principles.

**Disclaimer:** This is free procedural hygiene support only. **Not legal advice.** No guarantees. Consult qualified counsel.
