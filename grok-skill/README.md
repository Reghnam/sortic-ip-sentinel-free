# SorticAI Free IP Sentinel — Grok / Grok Build / Grok Bot (v0.5.32-free)

Grok-native package. Headless numbered options are the **default** (Grok Build viewers cannot run a TUI picker; `grok -p` is one-shot; **Grok Bot is unattended**). Unnamed L3 **default-delivers 1 (show/hold) + 8 (JSON)** so an unattended run is not blank.

`references/` is **bundled**. One copy is a complete skill.

Frontmatter extras vs other hosts: `when-to-use`, `argument-hint` (slash autocomplete), `disable-model-invocation: false`.

## Install

User-level:
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/grok-skill ~/.grok/skills/sortic-ip-sentinel-free
```

Grok Build / project: `.grok/skills/sortic-ip-sentinel-free/` (already includes `references/`). **This `cp` is Grok Build / CLI — not Grok Bot.**

Grok Bot: **Save / Plugins → enable per-Bot.** Do not `cp` to `~/.grok/skills/` (project: `.grok/skills/` — Grok Build does not scan `.agents/skills/`). Do not use Teach-by-demonstration as the install path (publish). **Scan before ship** — third-party marketplace skills are untrusted. Treat email / GitHub push / browser-use / Clip-Bot / social post / board rooms / callable hops / reviewer hops / voice demos / voice screen-share / public Grok or Bot share URLs as **live demo channels**. Apply show/hold before the paste/send. Never invent status. Never email leftover drafts or partner pre-reads unless this turn names recipient AND action. Backup is not publish. Bot egress IP is not sticky — decline registrar login on new-device alerts. Shared Bot computer is account-wide (files, browser sessions, app logins) — not a vault. Screens ≠ security boundary. Bot-to-Bot DM is a hop. Delete Bot ≠ wipe computer; Enterprise terminate-computer keeps the durable disk. Dedicated user for isolated credentials. Cloud computer ≠ desktop-egress ≠ local-computer execution (Ask every time default; laptop closed continues cloud work, stops egress routing and local-exec). Auto Review rules are desktop-local; Update Agent Computer preserves durable state; Reset drops unsynced work. Marketplace job-taking is access grant + send. `--always-approve` / `--yolo` is not owner approval. Consult ≠ voice/phone provision. Voice clone is identity publish. Disabled jobs stay disabled. Fit-note is not a send. Drafts ≠ send. Access grant is owner-gated. Done requires path+link. Project-repo skill commit is a publish. Project `.grok/hooks/` needs `/hooks-trust`. Async board packet without the room is a demo. Workflow fan-out is a disclosure multiplier. Remote Mac / phone-driven desktop is computer-use. Live isEnabled is evidence. Copilot `.github/skills/` is a publish. De-identified / ZDR is not a vault. API no-train ≠ ChatGPT no-train. Galaxy / role livestream calendar add is L0 attend. Grok Bot computers run in the United States today (not on-prem, not BYO). Auto Review does not review memory writes or most settings changes.

## Behaviour notes
- Match L0–L3. Meta work on this skill stays L0. US IP corpus ticks stay L0. Private-corpus RAG on L3 is sidecar/offline (`references/public-corpus-rag.md`). Never bundle / never Bot disk. Do not invent a corpus URL. Share pack `grok-bot-share/` is config only — do not publish live.
- Grok `allowed-tools` does not grant or restrict. Keep the Anthropic one-turn hygiene text; do not invent a Grok tool lock.
- Never ask the Grok viewer to open localhost, run shell, or paste logs.
- Headless contract: stamp → snapshot → options 1–8 → default 1+8 if unnamed → disclaimer. JSON schema `sorticai.hygiene_package.v1` (`output_register`, `not_for_third_party`, `agent_exposure`).
- This is the free Phase-0 shape (skill → structured hygiene package). No paid menu.
- Builder worksheet: not legal advice; do not send outputs as legal analysis.

**Not legal advice. No guarantees. Free only.**
