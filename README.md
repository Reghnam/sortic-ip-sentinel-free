# SorticAI Free IP Sentinel

**The skill that quietly protects your IP at the exact moment you need it.**

Free portable IP-sensitive moment detector + hygiene sentinel (v0.5-free).  
Detects “protect the IP”, investor demos, pilot showcases, fundraising decks… and delivers only free procedural hygiene:

- Show / hold maps  
- Staged disclosure ladders  
- Investor & partner demo hygiene playbook  
- AI / human contribution logs (USPTO 2025 aligned)  
- Provisional readiness checklists  
- Provenance & holdback audits  

**Not legal advice. No guarantees. Free only.**

Works on **Codex**, **Claude Code**, **Grok**, **ChatGPT Skills**, Cursor and any agentskills.io runtime.

---

**Usage triggers (examples)**
- "protect the IP", "IP sensitive moment", "trade secret before investor demo", "how to protect this before we file", "NDA before sharing the protocol".
- L2 exposure: "investor demo in 10 days" → soft tip only.
- L0: privacy, config, meta on this skill → silent.

**Contents**
- SKILL.md (the skill definition)
- references/ (playbook, catalog, templates, ground rules)

**Distribution**
This is the public seed for the GitHub repo. Clone, use, contribute hygiene improvements.

**Weekly updates**
This skill is kept current by an autonomous research loop (see scheduler in main SorticAI skill).

**Sources (high-level)**
EPO Guidelines, USPTO 2025 AI inventorship guidance, WIPO principles.

See SKILL.md for full disclaimers and guardrails.

Free hygiene at the moment of creation. File before you expose when it matters.

**Sources referenced (high-level summaries only):** EPO Guidelines G-II 3.3.1 (AI/ML technical effect), USPTO 2025 AI inventorship guidance (human conception), WIPO principles.

**Disclaimer:** This is free procedural hygiene support only. **Not legal advice.** No guarantees. Consult qualified counsel.

This public hub seed was produced through two autonomous iterations (implementation + review + fix) using sub-agents for rigor. See weekly research loop for ongoing updates.

---

## ChatGPT / Codex Compatible Variant

For strict ChatGPT Skills and Codex compatibility, we provide a minimal-frontmatter variant inside this repo:

**Location inside this repo:** `chatgpt-skill/`

**Quick Install**

**OpenAI Codex**
```bash
# Recommended: clone the main repo and copy the subfolder
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.codex/skills/sortic-ip-sentinel-free
```

**ChatGPT Skills (Business/Enterprise/Edu)**
1. Go to the folder on GitHub and click **"Download ZIP"** (top right when viewing the folder):
   https://github.com/Reghnam/sortic-ip-sentinel-free/tree/main/chatgpt-skill
2. Upload the zip in the Skills tab.

This variant strips OpenAI-unsupported frontmatter keys and uses `agents/openai.yaml` for display + invocation policy.

All behaviour, references, disclaimers, and licence text are identical to the canonical version.

See `chatgpt-skill/README.md` inside the folder for the short install guide.

The rich `SKILL.md` (root of this repo) is still the recommended version for Claude Code, Grok, Cursor, and other full agentskills.io runtimes.
