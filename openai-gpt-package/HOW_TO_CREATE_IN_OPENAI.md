# How to Publish the SorticAI Free IP Sentinel (v0.5-free) to OpenAI

This package makes it easy to bring the free portable IP hygiene skill into OpenAI's ecosystem (2026).

## Two Recommended Paths

### Path 1: Portable Skill (SKILL.md) — Best for portability & developers (Recommended starting point)
OpenAI supports the open agentskills.io standard in Codex and ChatGPT.

**Steps:**
1. Push this entire folder to a public GitHub repo (e.g. `Reghnam/sortic-ip-sentinel-free`).
2. Install in Codex:
   ```
   $skill-installer https://github.com/Reghnam/sortic-ip-sentinel-free
   ```
   Or manually copy the folder to `~/.codex/skills/sortic-ip-sentinel-free/`.

3. In ChatGPT (Business/Enterprise/Edu):
   - Skills tab → Upload zip of the folder or use "Create with chat" + GitHub link.

See the root `LAUNCH.md` and `README.md` for the full executive checklist and install commands.

### Path 2: Custom GPT (for hosted use + GPT Store)
Use this package for a ready-to-paste GPT.

**Steps (requires eligible workspace for full Store publishing):**

1. Go to ChatGPT → Create a new GPT (or edit one).

2. **Name:** SorticAI Free IP Sentinel (v0.5-free)

3. **Description:** Free portable skill that detects IP-sensitive moments and delivers practical hygiene help (show/hold maps, contribution logs, demo hygiene, disclaimers). Not legal advice.

4. **Instructions:** Paste the entire content of `instructions.txt` (in this folder).

5. **Knowledge files** — Upload these from the `knowledge/` folder (recommended order):
   - free-catalog.md
   - demo-hygiene-playbook.md
   - contribution-log.md
   - ground-rules.md
   (Optionally add more from the main references if you want extras.)

6. **Conversation starters** (suggested):
   - "IP sensitive moment on our new protocol before investor demo"
   - "Help me create a show/hold map for this architecture"
   - "We have a pilot showcase next month — what should I be careful sharing?"

7. **Capabilities:** Turn on "Code interpreter" if you want it to help generate tables/docs.

8. Test in Preview:
   - Trigger L3: "How do I protect the IP before we share details with partners?"
   - Check L0 silence on privacy/config questions.
   - Verify disclaimers appear.

9. Share:
   - "Anyone with the link" for easy distribution.
   - Or publish to GPT Store (if your workspace allows — complete Builder Profile first with verified domain).

**Important 2026 notes:**
- New GPT creation/publishing to the Store is restricted to Business, Enterprise, or Edu workspaces.
- Personal accounts can often still create private/shared GPTs and use links.
- Always keep the strong disclaimers.

## After Publishing
- Update knowledge files when the main skill improves (copy from the root references/).
- The skill is kept fresh by the autonomous weekly research loop.

**This is free procedural hygiene only. Not legal advice. No guarantees.**

For the full SorticAI IP Checkpoint (with paid options), see the main skill.

Sources: agentskills.io standard, OpenAI Help Center (publishing GPTs, skills in ChatGPT), 2026 ecosystem reports.
