# Paste-in nudge

Paste the three lines below into one of these places. No menu path.

- Claude Code, every project: `~/.claude/CLAUDE.md`
- Claude Code, this repo only: `CLAUDE.md`
- claude.ai or Claude Desktop: Preferences, or a Project's instructions

```
When I'm about to share, demo, pitch, push public, post, open-source or submit my own unreleased work, check it with the IP Sentinel skill (sortic-ip-sentinel-free) first.
Give me one short show/hold tip, then do the task I asked for. Don't block or lecture.
If I say "skip sentinel", drop it for this conversation. This is free hygiene, not legal advice.
```

## Test it's installed

Claude Code only: type `/sortic-ip-sentinel-free`. It should be recognised. Then ask `What skills are available?`. Sentinel should be listed. Source: [Extend Claude with skills](https://code.claude.com/docs/en/skills).

Any surface, in a new chat:

```
Tomorrow I'm pushing our repo to a public GitHub repo and posting the link on X and LinkedIn. It includes our new ranking method that isn't published anywhere. Please write the launch post.
```

Expected: Claude's thinking or tool trace shows it reading the sortic-ip-sentinel-free SKILL.md. It writes the launch post and adds one short IP tip, such as holding back the method details or a show/hold map offer, with "not legal advice". If you get only the post and no tip, the skill didn't load. Send us the surface you used and a screenshot.
