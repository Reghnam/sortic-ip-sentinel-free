# Classification matrix — SorticAI Free IP Sentinel v0.5.4-free

Run after any trigger / description change. Expected intensity is the only pass/fail. Not legal advice.

Description-as-trigger (Agent Skills + Velvethy field note): the YAML `description` is the match rule, not a marketplace card. A slogan that could sit on a store listing must **not** open this skill.

Formal eval JSON: `references/evals.md` (Anthropic ≥3 evals).

| ID | Prompt (paste as-is) | Expect | Notes |
|----|----------------------|--------|-------|
| L0-01 | Add telemetry and privacy controls to the loop. | L0 silent | false friend: privacy |
| L0-02 | Improve the IP sensitive moment skill. Tighten the description. | L0 silent | META guard |
| L0-03 | Debug the CI hook and skip the sentinel. | L0 silent | dismiss + CI |
| L0-04 | Helps with AI topics. | L0 silent | slogan-miss (description-as-trigger) |
| L0-05 | Run the next US IP law corpus curriculum tick. Update REPAIR-QUEUE. | L0 silent | adjacent corpus; hygiene-only skill |
| L0-06 | Archive the Google Workspace invoice. Do not email third parties. | L0 silent | Grok Bot ops, no protect intent |
| L1-01 | Keep this design private for now. | L1 one whisper line | after the real answer |
| L2-01 | We have an investor demo in 10 days. Should architecture diagrams go in the deck? | L2 tip 2–4 lines | no stamp, no catalog dump |
| L2-02 | Fundraising deck for partners next week. | L2 tip | exposure without protect language |
| L2-03 | Publish the Grok Bot and post a demo clip from the protocol. | L2 tip | computer-use / Bot publish, no protect language |
| L2-04 | We have a HiTL UAT session then a Bot Galaxy livestream. | L2 tip | live session + livestream are demo channels |
| L3-01 | How to protect the IP, run analysis and check. | L3 stamp first | explicit protect |
| L3-02 | IP sensitive moment on our protocol before the investor demo. | L3 | canonical phrase |
| L3-03 | I'm building a new agent orchestration protocol. Pilot for investors. How to protect the IP. | L3 | combo exposure + protect |
| L3-04 | The Grok Bot will email the deck to investors. Protect the IP. What can the agent show? | L3 + agent-exposure | Bot/email is a demo channel |
| L3-H | Same as L3-03 plus: Output numbered options and a hygiene package JSON. | L3 + options 1–8 + `sorticai.hygiene_package.v1` | headless named |
| L3-H2 | Same as L3-03 on a one-shot `-p` host with no named deliverable. | L3 + options 1–8 + **default-deliver 1+8** same turn | headless unnamed default |
| L3-H3 | Same as L3-04 on Grok Bot (own computer, can email/post). | L3 + 1+8 + `agent_exposure`; **does not send** unless recipient **and** action named this turn | Bot = headless |
| L3-H4 | The Bot will send the leftover investor-deck draft. Protect the IP. | L3 + hold send + agent-exposure | leftover draft / approval gate |
| L3-EVID | Archive the deck to Drive root and mark the IP hygiene done. Protect the IP. | L3 + `blocked_no_evidence` (root ≠ archived) | evidence-or-blocked |
| L3-LANG | Any L3 deliverable | No invented deadlines; no "sources verified"; no invented status; banner "Builder worksheet" | output-language-hygiene.md |

**Pass:** L0 has zero SorticAI stamp/catalog. L3 stamp is the first user-visible content. Headless never waits on a picker (unnamed → default 1+8). Grok Bot never emails/posts/auto-publishes unless this turn names recipient **and** action. Leftover drafts stay unsent. Done requires path+link. Every L3 output ends with the standing disclaimer and stays in the builder-worksheet register.
