# Headless Hygiene Package — `sorticai.hygiene_package.v1`

**Free only · Not legal advice · No guarantees**

Use when the host is non-interactive (Codex CLI, Claude `-p`, `grok -p`, Grok Build, **Grok Bot**, MCP/A2A, computer-use, CI) or the user asks for JSON / export / package.

This is a **hygiene package**, not a commercial case file. No prices, no counsel names, no protectability rulings, no "you should file". Aligns with SorticAI Phase 0 "skill → structured package" **without** paid residue.

## When to emit

- User says export, JSON, package, headless, "for my agent", "structured summary".
- Host has no picker (including Grok Bot / computer-use).
- Option **8** from the numbered list.
- **Default on unnamed headless L3:** emit this JSON together with a show/hold map (option 1) in the same turn.

Emit **after** the stamp + snapshot. Repeat the disclaimer inside the JSON. Apply `output-language-hygiene.md` (procedural verbs; no invented deadlines; no invented status; no "verified").

## Schema (emit exactly these keys)

```json
{
  "schema": "sorticai.hygiene_package.v1",
  "edition": "0.5.3-free",
  "activation_level": "L3",
  "output_register": "procedural_builder_worksheet",
  "not_for_third_party": true,
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
  "agent_exposure": [
    {"runtime": "grok-bot | codex-p | claude-p | computer-use | other", "channel": "browser | email | github | social | file | none", "what": "redacted one line", "audience_named": false, "action": "hold | ok | not_sent"}
  ],
  "next_hygiene_step": "one practical sentence a builder can do today",
  "disclaimer": "Builder worksheet. Do not send these tables to third parties as legal analysis. SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is not legal advice and carries no guarantees. Consult qualified IP counsel.",
  "sources_note": "High-level summaries only: EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles. Public URLs located are not 'verified sources'."
}
```

## Rules

- `exposure_risk_signal` is a **rough hygiene signal**, not a legal opinion.
- Prefer empty arrays over invented facts. Prefer `"channel": "none"` over fake rows.
- If context is thin, set `deliverables` to `offered` and still return the envelope.
- Markdown above the JSON is allowed (stamp + snapshot). Do not wrap JSON in a story.
- Never invent a deadline. Never claim links were "verified" unless you state the exact check.
- Never invent status. Never email/post the JSON or the work to third parties unless this turn names the recipient (`not_for_third_party`).
- `agent_exposure` is optional-looking but **emit the key**. Empty array is correct when the agent did not show/send anything this turn.

**Disclaimer:** SorticAI IP Sentinel (free edition) v0.5.3-free is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
