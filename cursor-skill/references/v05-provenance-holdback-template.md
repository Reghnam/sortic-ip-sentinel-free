# Code / Output Provenance + Holdback Audit — Template (v0.5.4-free)

**Purpose:** Know what a model or **agent** saw, and what a demo / Bot / computer-use session must not leak. Hygiene only.

## What was shown to a model (redact secrets in this table)

| Date | Tool / model | What was pasted or uploaded | Still secret? | Action |
|------|----------------|-----------------------------|---------------|--------|
|      |                |                             |               |        |

## What an agent showed, emailed, pushed, or posted

If the runtime has a computer (Grok Bot, browser-use, MCP, GitHub push, social scheduler), also fill `references/agent-exposure-log.md`. Summary row:

| When | Runtime | Channel | What left the workspace | Audience named this turn? | Hold or ok? |
|------|---------|---------|-------------------------|---------------------------|-------------|
|      |         |         |                         |                           |             |

## Demo / deck / repo / Bot holdbacks

- [ ] Exact parameters / weights / recipes out of the deck **and** out of any agent paste.
- [ ] Full source not in the leave-behind, public repo, or Clip-Bot export.
- [ ] Production data / customer names masked.
- [ ] AI-generated sections labelled in the contribution log (human vs runtime).
- [ ] Recordings: off, or logged if the other side insisted.
- [ ] No third-party email or social post unless this turn named the recipient.

**Disclaimer:** This is a builder hygiene template. **Not legal advice.** No guarantees. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
