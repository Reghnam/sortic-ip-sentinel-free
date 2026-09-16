# Public US-IP corpus — read-only RAG (v0.5.18-free)

**Hygiene only. Not legal advice. Not a prior-art search. Not FTO. Not a second regulatory radar.**

This skill may **use** a mounted hourly **US-IP public** corpus during L3 hygiene. It must never **ingest** client secrets, work-product, holdbacks, or private facts into that corpus. Curriculum ticks / DESIGN-PLAN / REPAIR-QUEUE stay L0 (Eval 5).

## When to load this file

L3 and the user asks for prior-art pointers, public-source hygiene, or "use the hourly US IP corpus". Also when offer 6 (lite prior-art pointers) is chosen and a corpus might be mounted.

## Expected interface (path may be unknown)

Do not invent a private client path. Probe, in order, then stop:

1. Environment variable `US_IP_PUBLIC_CORPUS` (absolute directory).
2. Sibling directories **outside** this skill zip:
   - `us-ip-law-ground-truth/`
   - `us-ip-public-corpus/`
3. Optional index inside that directory: `INDEX.md` or `manifest.json`.

If none of those resolve, use **offline fallback**. Do not guess a Dropbox / client / Lorenc / vault path.

### Manifest (`manifest.json` or a leading `INDEX.md` block)

Expected keys (ignore extras; do not invent missing ones):

```json
{
  "name": "us-ip-public-corpus",
  "visibility": "public",
  "as_of": "ISO-8601 timestamp of last hourly tick",
  "sources": [{"title": "string", "url": "https://..."}],
  "query": "keyword lookup over public citations only"
}
```

A usable lookup is: read the index → match high-level keywords the **user already typed** → return public title + URL. Do not paste secret embodiments into a public search box.

### Allowed operations

- READ / LIST / LOOKUP public citations
- CITE at **high level** ("public URL located", title match)
- State `as_of` when the manifest has it

### Forbidden operations

- WRITE / UPDATE / DELETE corpus files
- INGEST client secrets, protocols, decks, holdbacks, IAM, names, valuations
- RUN curriculum ticks, DESIGN-PLAN, REPAIR-QUEUE (those stay L0 here)
- Claim holdings, validity, FTO, or patentability
- Build a second regulatory-radar product from this skill
- Copy the corpus into the skill zip or ChatGPT/Claude upload

## Offline fallback (path unknown or unreadable)

1. One line: "Public US-IP corpus not mounted — offline pointers only."
2. Use `references/v05-lite-prior-art-pointers.md` (USPTO / Google Patents / Espacenet / PATENTSCOPE / Lens.org).
3. Keep the standing high-level sources note (EPO G-II 3.3.1, USPTO 2025 AI inventorship, WIPO).
4. Do not invent cases, holdings, or corpus rows.
5. JSON: `agent_exposure.channel` = `corpus-offline`.

## If the user asks to ingest / train / write

**Decline.** Channel `corpus-ingest`. Writing client work into a public hourly corpus is owner-gated and out of this free skill.

## JSON

`agent_exposure.channel` may be `public-corpus-rag | corpus-offline | corpus-ingest`.

## Reminder

Hourly corpus **maintenance** is a different job. This file is only the **use** contract for hygiene lookups.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
