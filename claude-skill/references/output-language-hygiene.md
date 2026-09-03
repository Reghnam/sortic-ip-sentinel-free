# Output language hygiene — SorticAI Free IP Sentinel

**Free only · Not legal advice · No guarantees**

Load this file when drafting any L3 deliverable (maps, checklists, JSON, slides).
These rules come from counsel review of adjacent SorticAI writing (2 Sep 2026) plus Agent Skills authoring practice (Anthropic: no voodoo constants; OpenAI: plain I/O). They are **writing rules**, not legal opinions.

## Banner (put on every export)

> **Builder worksheet.** Procedural hygiene for the people making the thing. **Do not send these tables to third parties as legal analysis.** Not legal advice. No guarantees.

## Register: procedural, not advisory

If a paragraph looks like a lawyer's instruction, the standing disclaimer becomes confusing. Stay in the builder register.

| Do | Do not |
|----|--------|
| Consider documenting who framed the problem. | You must file a provisional within 48 hours. |
| List what is safe to show vs hold. | This invention is protectable / patentable. |
| Hold exact parameters until NDA. | To comply with USPTO/EPO you should… |
| Public URL located (title match). | Sources verified / links validated. |
| One next action a builder can do today. | Empty "practical signal" with no action. |

## Hard rules

1. **Verbs.** consider / document / list / hold / mark / log. Never "you must file", "implement to comply", "this is a trade secret".
2. **No invented deadlines.** Do not write "within 48 hours" or similar unless the *user* stated the date. Arbitrary clocks look like legal/compliance advice.
3. **No fake verification.** Never "externí adresy ověřeny jako platné" / "sources verified". Write what you actually did: "public URL located" + what was checked (title, HTTP reachable) — or omit.
4. **One idea per sentence.** Do not stack jargon ("data origin, legal basis, minimisation, filtering…") without saying *of what*. Write for a builder, not an IP specialist.
5. **Every recommended step has a next action** the reader can do today, or drop the step. Factual observations without a next action are empty.
6. **Priority ≠ impact.** If you rank items, say *why* this one is first (time-to-exposure, irreversibility), not a naked "P1".
7. **Do not mix "a lawyer reviewed this" with "not legal advice".** This free skill never claims counsel review. If a later paid product does, that is a different document.
8. **Plain labels.** Avoid internal codes (L0–L3, T0–T3) in user-visible text except this file and maintainer notes.

## Headless / JSON

Set `"output_register": "procedural_builder_worksheet"` and `"not_for_third_party": true` on `sorticai.hygiene_package.v1`. Repeat the banner inside `disclaimer`.

## Check before you send (30 seconds)

- [ ] Would a non-lawyer read this as "do this to be legally safe"? If yes, rewrite.
- [ ] Any deadline you invented? Remove it.
- [ ] Any "verified / valid / compliant"? Replace with what you actually checked.
- [ ] Banner + standing disclaimer present.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
