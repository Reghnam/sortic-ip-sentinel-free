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
  "edition": "0.5.15-free",
  "activation_level": "L3",
  "output_register": "procedural_builder_worksheet",
  "not_for_third_party": true,
  "owner_gated": true,
  "noticed": "one plain sentence",
  "snapshot": {
    "building": "user's words, one line",
    "audience": "investors | partners | customers | pilot | public | board | other",
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
    {"runtime": "grok-bot | grok-build | codex-p | claude-p | computer-use | other", "channel": "browser | email | github | social | livestream | hitl | board | backup | export | local-computer | callable | voice | voice-screen | routine | file | bot-share | marketplace | grok-share | reviewer | mailbox | iam-screenshot | access-grant | legal-draft | webhook | bot-duplicate | lifecycle-hook | astra-computer | console-shot | ci-apply | sites | async-board | repo-skill | fan-out | hooks-trust | remote-mac | workspace-plugin | responses-api | hosted-skill | counsel-release | livestream | claude-plugin | demo-skill | meet-notes | judge-model | deid-train | default-version | shared-bot-session | job-skill | cross-surface | protected-lane | skill-zdr | bot-dm | bot-screen | api-vs-chat | capdir | app-builder | vercel-deploy | claude-sync | astra-complete | grok-discover | desktop-egress | ownership-pass | videos-zdr | allowed-tools | legacy-privacy | none", "what": "redacted one line", "audience_named": false, "action_named": false, "evidence": "", "action": "hold | ok | not_sent | blocked_no_evidence | declined"}
  ],
  "approval_required": true,
  "evidence_or_blocked": "done requires path+link; promises and inbox-root dumps are not done",
  "stop_or_decline": "ask | stop | decline | none",
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
- Never invent status. Do not invent, replace, or reroll a result. Never email/post/auto-publish/pay the JSON or the work unless this turn names the recipient **and** the action (`not_for_third_party`, `approval_required`, `owner_gated`). Leftover drafts and partner pre-reads stay unsent.
- Claimed send needs message-id + recipients, else `not_sent`.
- `evidence_or_blocked`: write blocked when there is no path+link. Inbox-root dumps are not done.
- `stop_or_decline`: `ask` (incomplete input), `stop` (leftover draft / truncated-as-original / clock-limited overshare / backup-tree growth / image-only invented figures / holdbacks in a shareable Bot / public Grok-share of internals / IAM paste / console-shot mail of internals / ZDR-as-vault paste / API-as-ChatGPT-vault / holdbacks on a shared Bot computer / Bot-to-Bot dump), `decline` (unsupported login, unnamed public auto-push, client facts into public repo, partner send, pay, identity/live-copy, backup-as-publish, access grant, mailbox MCP, production hooks, webhook secret, voice clone, voice/phone provision, CI auto-apply, Sites public publish, project-repo skill commit, untrusted project hooks, unnamed remote-Mac register, unnamed workspace plugin, unnamed Responses API open catalog / pin-latest / default_version / omit-version, unnamed Claude-plugin submit, unnamed public livestream, unnamed demonstration-to-skill, unnamed counsel-unreviewed client send, unnamed marketplace job-taking skill, unnamed cross-surface Claude install, unnamed Bot-to-Bot dump, treating Skills/Files/Conversations as ZDR-covered, exploit/PoC), or `none`.
- `owner_gated`: always `true` on this edition. Send / publish / pay / identity / live title-copy stay declined unless this turn names recipient **and** action. IP L3 is not write-privilege.
- Truncated/junk files are not originals. Do not emit them as work product.
- Do not dump client/product facts into a public skill repo. ChatGPT/Codex skill zips are scanned — no secrets in the zip.
- Backup ≠ publish. Project export is owner-desk.
- Callable hops are demo channels. Do not dump internals into the callable surface.
- `--yolo` / `--always-approve` is not owner approval. Voice/phone provision is declined unless named.
- Placeholders and MCP-size-blocked files are not originals.
- Fit-note / adjacent-demand analysis is not a send.
- Disabled jobs stay disabled. Do not rewrite live prompts.
- Bot share / marketplace clone is a demo channel. Do not park holdbacks in a shareable Bot.
- Image-only decks are not numbered facts.
- Require Approval wins Always Allow. 2FA/CAPTCHA computer-takeover → decline login.
- Reviewer hop is a disclosure hop. Mailbox connectors are MCP. Public Grok/Bot share URLs are cloneable config.
- Access grant is owner-gated. IAM / webhook screenshots are holdbacks. Legal drafts ≠ send.
- Voice screen-share sees the browser. Voice clone is identity publish. Astra computer-use / write-across-apps is a live demo channel. Connectors are not a vault. Console-shot partner mail is a demo. CI auto-apply is a production change.
- Plugin-bundled hooks are untrusted until reviewed. This skill has none. Pin `latest` is a live production channel.
- Stale schedule metadata ≠ "didn't run".
- If source data is unavailable, report failure — do not reuse stale data.
- `agent_exposure` **must be emitted**. Empty array is correct when the agent did not show/send anything this turn.

**Disclaimer:** SorticAI IP Sentinel (free edition) v0.5.15-free is automated / skill-assisted procedural hygiene help only. It is **not legal advice** and carries **no guarantees**. Consult qualified IP counsel. Sources referenced (high-level summaries only): EPO Guidelines G-II 3.3.1, USPTO 2025 AI inventorship guidance, WIPO principles.
- Sites deploy URL is production. Save-without-deploy to review. Default owner+admins. Workspace/public publish is a demo. Sites env/secrets are holdbacks.
- User instructions this turn beat skill guidelines. Named recipient AND action is the override. On L3 decline, quote SKILL.md. No unsolicited L0/L1 hypothetical-risk checklists.
- Async board packet without the room is a demo. Project-repo skill commit is a publish. Workflow fan-out is a disclosure multiplier. Project `.grok/hooks/` needs `/hooks-trust`.
- Responses API Skills are versioned bundles. Pin an integer version; `latest` / `default_version` / omit-version are live channels. Do not expose this public repo as an open end-user catalog. Three zip layouts; do not mix. Subagents do not inherit unless listed.
- Remote Mac / phone-driven desktop is computer-use. Live `isEnabled` is evidence. Workspace-shared plugin / Copilot `.github/skills/` is a publish.
- De-identified / ZDR-claimed training is still a disclosure. Opt-out is not a rewind. Shared Bot computer is account-wide (files, sessions, logins). Marketplace job-taking is access grant + send. claude.ai enablement syncs to Cowork/cloud; local ~/.claude/skills/ still does not auto-sync; API is a separate publish.

- Counsel-release is a send. "Waiting for legal review" is an internal hold. A judge-model is not counsel. Meet auto-notes of an IP/AI session are a demo.
- Three zip layouts; do not mix. Unnamed Claude-plugin submit is a publish. Public livestream of internals is a demo; attending is L0. Demonstration-to-skill is a publish (screen recorded).
- App Builder live preview is a demo; Vercel deploy is a publish. claude.ai sync / CLAUDE_CODE_SYNC_SKILLS=1 is a publish. Define L3 completion so Astra does not stop after the stamp. Grok discovers ~/.agents/skills/ with zero config.

- Desktop-egress is a CDN, not a vault (update computer first). Ownership-pass is access grant + hop. Videos 48h+30d / Eyes Off still retain. No Legacy Privacy Mode. Do not add allowed-tools write grants.
