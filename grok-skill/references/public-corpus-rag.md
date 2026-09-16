# Private US-IP corpus — sidecar / offline RAG (v0.5.25-free)

**Hygiene only. Not legal advice. Not a prior-art search. Not FTO. Not a second regulatory radar.**

`Reghnam/us-ip-law-ground-truth` is **PRIVATE**. It is the source of truth for hourly US-IP curriculum. This free skill must **never** ship that tree.

This skill may **retrieve** limited citation/snippet answers through a SorticAI-controlled **sidecar** on L3. The user **never downloads the KB**. It must never **ingest** client secrets, work-product, holdbacks, or private facts into that corpus. Curriculum ticks / DESIGN-PLAN / REPAIR-QUEUE stay L0 (Eval 5).

## Never bundle / never Bot disk

Do **not** copy, zip, upload, or park `us-ip-law-ground-truth` (or any private law dump) into:

- this public free skill zip (`chatgpt-skill/`, `claude-skill/`, `grok-skill/`, `cursor-skill/`)
- a Grok Bot disk / Computer / share template
- a Drive free pack (Sep-2 Drive zips are **stale** lunch sources — use this PR branch)
- ChatGPT / Claude / Cursor uploads
- marketplace Bot templates

Unknown sidecar → **offline** public-safe fixtures only. **Do not invent a corpus URL** or hosting endpoint.

## When to load this file

L3 and the user asks for prior-art pointers, public-source hygiene, or "use the hourly US IP corpus". Also when offer 6 (lite prior-art pointers) is chosen.

## Expected interface (sidecar first; path may be unknown)

Probe, in order, then stop. Do not invent a private client path or a live API host.

1. Environment variable `SORTICAI_US_IP_SIDECAR` (retrieve-only HTTPS endpoint controlled by SorticAI). Request/response contract: `references/sidecar-retrieve.stub.json`.
2. **Do not** treat a sibling `us-ip-law-ground-truth/` inside this skill tree as mounted — that would mean the corpus was bundled. If a maintainer sidecar mount exists **outside** the skill zip, it is still retrieve-only; never copy it in.
3. If neither resolves, use **offline fallback**.

### Sidecar request (retrieve-only)

POST limited keywords the **user already typed**. `max_snippets` ≤ 3. No bulk export. No `download_kb`. No `list_all`.

```json
{"q": "user keywords only", "max_snippets": 3}
```

### Allowed operations

- RETRIEVE limited citations/snippets via the sidecar
- CITE at **high level** ("public URL located", title match)
- State `as_of` when the sidecar returned it
- Offline: `references/v05-lite-prior-art-pointers.md` + the fixtures below

### Forbidden operations

- WRITE / UPDATE / DELETE corpus files
- INGEST client secrets, protocols, decks, holdbacks, IAM, names, valuations
- DOWNLOAD or zip the knowledge base
- RUN curriculum ticks, DESIGN-PLAN, REPAIR-QUEUE (those stay L0 here)
- Claim holdings, validity, FTO, or patentability
- Build a second regulatory-radar product from this skill
- Copy the corpus into the skill zip, Bot disk, Drive free pack, or ChatGPT/Claude upload
- Invent a corpus URL, API host, or "hourly feed" link when none was returned

## Offline fallback (sidecar unknown or unreadable)

1. One line: "Private US-IP sidecar not configured — offline pointers only."
2. Use `references/v05-lite-prior-art-pointers.md` (USPTO / Google Patents / Espacenet / PATENTSCOPE / Lens.org).
3. Public-safe distilled fixtures only (no private law corpus):

| Fixture | Public pointer |
|---------|----------------|
| USPTO AI inventorship (2025) | https://www.uspto.gov/sites/default/files/documents/ai-inventorship-guidance.pdf |
| EPO G-II 3.3.1 (AI/ML technical effect) | https://www.epo.org/en/legal/guidelines-epc |
| WIPO conversation on IP and AI | https://www.wipo.int/about-ip/en/artificial_intelligence/ |

4. Keep the standing high-level sources note (EPO G-II 3.3.1, USPTO 2025 AI inventorship, WIPO).
5. Do not invent cases, holdings, corpus rows, or a corpus URL.
6. JSON: `agent_exposure.channel` = `corpus-offline`.

## If the user asks to ingest / train / write / zip / park on Bot disk

**Decline.** Channel `corpus-ingest`. Writing client work into the private corpus, or bundling that corpus into a public zip / Bot disk / Drive pack, is owner-gated and out of this free skill.

## JSON

`agent_exposure.channel` may be `private-corpus-sidecar | corpus-offline | corpus-ingest`.

## Reminder

Hourly corpus **maintenance** is a different job. This file is only the **use** contract for hygiene lookups. The free skill is an **offline / sidecar interface**, not a corpus distribution.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
