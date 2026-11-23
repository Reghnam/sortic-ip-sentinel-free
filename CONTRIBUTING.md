# Contributing — SorticAI Free IP Sentinel

Hygiene only. Not legal advice. Free edition only.

## Edition bumps

Bump the edition only for a functional change, an activation change, an eval change, or a hard-stop change.

A content-only CLI or ecosystem observation tip must not bump the edition. Record a functional observation under the current CHANGELOG tip. Do not open a new edition heading for it, and do not restamp the public edition pins (SKILL.md, LICENSE, README, EXEC-SUMMARY, LAUNCH, `grok-bot-share/bot-template.json`, and the other stamps the hygiene check pins) for it.

A content-only daily host read goes in `docs/host-reads/ROLLING.md` only. That file is outside every shipped pack and zip. Do not record a host read in CHANGELOG.md.

The CHANGELOG top edition heading is the current edition. A later commit may edit that tip. Do not rewrite git history to change an older heading.

## How notes land

Content notes and changelog notes go through a pull request. The maintainer rebase-merges that pull request. Do not push them directly to main.
