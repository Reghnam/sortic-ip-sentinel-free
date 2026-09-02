# Headless Hygiene Package — `sorticai.hygiene_package.v1`

**Free only · Not legal advice · No guarantees**

Use when the host is non-interactive (Codex CLI, Claude `-p`, `grok -p`, Grok Build, MCP/A2A, CI) or the user asks for JSON / export / package.

This is a **hygiene package**, not a commercial case file. No prices, no counsel names, no protectability rulings, no "you should file". Aligns with SorticAI Phase 0 "skill → structured package" **without** paid residue.

## When to emit

- User says export, JSON, package, headless, "for my agent", "structured summary".
- Host has no picker.
- Option **8** from the numbered list.

Emit **after** the stamp + snapshot. Repeat the disclaimer inside the JSON.

## Schema (emit exactly these keys)

```json
{
  "schema": "sorticai.hygiene_package.v1",
  "edition": "0.5.1-free",
  "activation_level": "L3",
  "noticed": "one plain sentence",
  "snapshot": {
    "building": "user's words, one line",
    "audience": "investors | partners | customers | pilot | public | other",
    "exposure_risk_signal": "low | medium | high"
  },
  "show_hold": [
    {"item": "high-level architecture", "action": "show", "note": "block diagram only"}
  ],
  "deliverables": [
    {"id": 1, "name": "show_hold_map", "status": "included | offered"}
  ],
  "holdbacks": ["exact parameters", "full source", "production data"],
  "contribution_log_started": false,
  "next_hygiene_step": "one practical sentence",
  "disclaimer": "SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is not legal advice and carries no guarantees. Consult qualified IP counsel.",
  "sources_note": "High-level summaries only: EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles."
}
```

## Rules

- `exposure_risk_signal` is a **rough hygiene signal**, not a legal opinion.
- Prefer empty arrays over invented facts.
- If context is thin, set `deliverables` to `offered` and still return the envelope.
- Markdown above the JSON is allowed (stamp + snapshot). Do not wrap JSON in a story.

**Disclaimer:** SorticAI IP Sentinel (free edition) v0.5.1-free is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
