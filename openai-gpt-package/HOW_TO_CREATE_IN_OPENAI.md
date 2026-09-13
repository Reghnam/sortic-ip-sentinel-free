# How to Publish the SorticAI Free IP Sentinel (v0.5.13-free) to OpenAI

Primary path in 2026 is **ChatGPT Skills + Codex SKILL.md**, not a Custom GPT.

## Path 1: Portable Skill (recommended)

Repo: https://github.com/Reghnam/sortic-ip-sentinel-free

**Codex**
```bash
git clone https://github.com/Reghnam/sortic-ip-sentinel-free.git
cp -r sortic-ip-sentinel-free/chatgpt-skill ~/.agents/skills/sortic-ip-sentinel-free
```
Fallback: `~/.codex/skills/`. Project: `.agents/skills/`. Invoke `$` or `/skills`. Description is front-loaded so implicit match survives list truncation. Astra computer-use is a live demo channel; connectors are not a vault.

**ChatGPT Skills (Business / Enterprise / Edu)**
Zip `chatgpt-skill/` with `SKILL.md` at the zip root → Skills tab. Invoke `@`. The zip is scanned — no secrets, no client facts. Agent Plugins use a different layout (`plugin.json` + `skills/<name>/SKILL.md`) — do not mix. Responses API Skills are versioned bundles; pin an integer version, not `latest` / `default_version` / omit-version. De-identified / ZDR is not a vault. API no-train ≠ ChatGPT no-train. Skills/Agents/Files/Conversations/chatkit/batches/videos/fine-tuning are ZDR-ineligible.

`agents/openai.yaml` sets display name, default prompt, brand colour, and `allow_implicit_invocation: true`.

Headless: "Output numbered options and hygiene package JSON." Backup is not publish. Owner-gated send/pay/identity/voice-provision/access-grant. Callable hops and reviewer hops are demo channels. Drafts ≠ send. `--yolo` is not approval. Scan Tools is a snapshot. Plugin-bundled hooks untrusted until reviewed — this skill has none. Scan zip again after change before plugin submit.

## Path 2: Custom GPT (fallback)

1. Create a GPT named `SorticAI Free IP Sentinel (v0.5.13-free)`.
2. Paste `instructions.txt` into Instructions.
3. Upload `knowledge/` files.
4. Starters: "IP sensitive moment on our new protocol before investor demo" / "Help me create a show/hold map".
5. Share via link. GPT Store still needs an eligible workspace + Builder Profile.

**This is free procedural hygiene only. Not legal advice. No guarantees.**
