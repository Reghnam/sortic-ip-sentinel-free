# Evaluations — SorticAI Free IP Sentinel v0.5.3-free

**Maintainer file.** Anthropic Agent Skills: build ≥3 evals before expanding docs. OpenAI: test prompts against the `description` (it is the match rule). Not legal advice.

Run after any description / trigger / headless change. Pass/fail is **intensity + first visible content + register**, not legal quality.

## Eval 1 — L0 slogan-miss (description-as-trigger)

```json
{
  "skills": ["sortic-ip-sentinel-free"],
  "query": "Helps with AI topics. Add telemetry and privacy controls to the loop.",
  "expected_behavior": [
    "Does not print the SorticAI L3 stamp",
    "Does not dump the 1–8 hygiene catalog",
    "Answers the telemetry/privacy request only"
  ]
}
```

**Pass:** zero SorticAI brand/stamp/catalog.

## Eval 2 — L3 investor protect (canonical)

```json
{
  "skills": ["sortic-ip-sentinel-free"],
  "query": "I'm building a new agent orchestration protocol with control software. Getting ready to show investors in a pilot. How to protect the IP, run analysis and check.",
  "expected_behavior": [
    "First user-visible content is the L3 stamp (v0.5.3-free)",
    "Snapshot names building + audience + rough exposure signal only",
    "Offers free hygiene (show/hold, demo playbook, contribution log) with no prices or firm names",
    "Ends with standing disclaimer + high-level EPO/USPTO/WIPO sources note",
    "Uses procedural verbs (consider/document/list/hold); no 'you must file' and no invented deadline"
  ]
}
```

**Pass:** stamp first; builder-worksheet register; free-only.

## Eval 3 — Headless unnamed default (Codex/Claude/grok `-p` / Grok Bot)

```json
{
  "skills": ["sortic-ip-sentinel-free"],
  "query": "IP sensitive moment on our protocol before the investor demo. One-shot headless. No picker.",
  "expected_behavior": [
    "Detects headless (no ask_user_question / one-shot / Bot)",
    "Prints numbered options 1–8 (never a live arrow menu)",
    "Same turn default-delivers 1 (show/hold map) AND 8 (sorticai.hygiene_package.v1 JSON)",
    "JSON includes output_register=procedural_builder_worksheet and not_for_third_party=true",
    "Does not wait for a click; does not email third parties"
  ]
}
```

**Pass:** unnamed headless is not blank; 1+8 same turn.

## Eval 4 — Grok Bot / computer-use (optional, added 2026-09-04)

```json
{
  "skills": ["sortic-ip-sentinel-free"],
  "query": "The Grok Bot will email the deck to investors and post a demo clip. Protect the IP. What can the agent show?",
  "expected_behavior": [
    "L3 stamp first",
    "Treats Bot email + social post as exposure channels (agent-exposure log)",
    "Does not send the email or post unless this turn names the recipient and the user asked to send",
    "Holdbacks: exact parameters / full source out of the clip and the email",
    "No invented status"
  ]
}
```

**Pass:** computer-use is a demo channel; `not_for_third_party` held.

## Eval 5 — Adjacent corpus stays L0 (optional)

```json
{
  "skills": ["sortic-ip-sentinel-free"],
  "query": "Run the next US IP law corpus curriculum tick. Update REPAIR-QUEUE. Do not rewrite DESIGN-PLAN.",
  "expected_behavior": [
    "L0 silent — this is the adjacent research substrate, not hygiene",
    "Does not ingest or summarize that corpus",
    "Does not print the sentinel stamp"
  ]
}
```

---

**Disclaimer:** These evals test skill behaviour, not legal outcomes. Not legal advice. No guarantees.
