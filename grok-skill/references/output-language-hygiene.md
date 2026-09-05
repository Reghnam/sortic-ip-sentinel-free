# Output language hygiene — SorticAI Free IP Sentinel

**Free only · Not legal advice · No guarantees**

Load this file when drafting any L3 deliverable (maps, checklists, JSON, slides).
These rules come from counsel review of adjacent SorticAI writing (2 Sep 2026), Task Extractor / Grok Bot operating notes 1–4 Sep 2026 (do not invent status; do not email third parties unless the item names recipient **and** action; evidence-or-blocked), OpenAI plugins/skills 2026-09-05 (do not invent, replace, or reroll; state what the model must not infer), and Grok Bot skill anatomy (what requires approval; report failure instead of stale data). They are **writing rules**, not legal opinions.

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
| Not found / not in this turn. | Invented status ("filed", "cleared", "sent").
| Blocked — no path+link. | "Done" with no artifact, or inbox-root dump as archived. |
| Hold leftover draft. | Auto-publish / resend / empty signature reply. |

## Hard rules

1. **Verbs.** consider / document / list / hold / mark / log. Never "you must file", "implement to comply", "this is a trade secret".
2. **No invented deadlines.** Do not write "within 48 hours" or similar unless the *user* stated the date. Arbitrary clocks look like legal/compliance advice.
3. **No fake verification.** Never "externí adresy ověřeny jako platné" / "sources verified". Write what you actually did: "public URL located" + what was checked (title, HTTP reachable) — or omit.
4. **No invented status.** Unknown stays unknown. Do not invent, replace, or reroll a result. Do not claim sent / filed / approved without evidence in this turn.
5. **Approval gate.** Do not email, post, auto-publish, push, or send leftover drafts unless this turn names the recipient **and** the action. Empty signature replies stay unsent. Claimed send needs message-id + recipients.
5b. **Evidence-or-blocked.** Do not mark done without folder path + link. Inbox-root dumps are not archived. If source data is unavailable, report failure — do not reuse stale data.
6. **One idea per sentence.** Do not stack jargon ("data origin, legal basis, minimisation, filtering…") without saying *of what*. Write for a builder, not an IP specialist.
7. **Every recommended step has a next action** the reader can do today, or drop the step. Factual observations without a next action are empty.
8. **Priority ≠ impact.** If you rank items, say *why* this one is first (time-to-exposure, irreversibility), not a naked "P1".
9. **Do not mix "a lawyer reviewed this" with "not legal advice".** This free skill never claims counsel review. If a later paid product does, that is a different document.
10. **Plain labels.** Avoid internal codes (L0–L3, T0–T3) in user-visible text except this file and maintainer notes.

## Headless / JSON / Grok Bot

Set `"output_register": "procedural_builder_worksheet"`, `"not_for_third_party": true`, `"approval_required": true` on `sorticai.hygiene_package.v1`. Repeat the banner inside `disclaimer`. Emit `agent_exposure` (empty array is fine) and `evidence_or_blocked`. Computer-use / livestream / HiTL is a demo channel — see `agent-exposure-log.md`.

## Check before you send (30 seconds)

- [ ] Would a non-lawyer read this as "do this to be legally safe"? If yes, rewrite.
- [ ] Any deadline you invented? Remove it.
- [ ] Any "verified / valid / compliant"? Replace with what you actually checked.
- [ ] Any status you invented? Replace with "not found" / "not in this turn".
- [ ] About to email, post, or auto-publish? Recipient **and** action named this turn? Not a leftover draft?
- [ ] Claiming sent? Message-id + recipients written?
- [ ] Claiming done? Path + link, not inbox-root?
- [ ] Banner + standing disclaimer present.

**Disclaimer:** SorticAI IP Sentinel (free edition) is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
