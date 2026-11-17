# Content-only host reads

Future content-only daily host reads go in this file. It is not part of a shipped pack or zip.

The single latest read for the current edition stays in CHANGELOG.md. The next content-only daily read is appended below this note.

## 2026-11-17 (same edition, content-only)

A content-only host read. No edition bump. No pin restamp. Not a shipped pack. **No client / product / infra names.**

### OpenAI (first)

- GitHub releases Latest this read is still **0.169.0** (13 Nov, not a prerelease). A later non-prerelease tag is the stable CLI.
- **New:** the first row of the releases list is a prerelease published 17 Nov. That row is not the Latest badge. A second row is also a prerelease published 17 Nov. Prerelease rows dated 16 Nov are in this list and are not the Latest badge. An alpha is not the stable CLI. No stable tag dated 16 Nov. No stable tag dated 17 Nov. Do not copy the alpha tag. Do not copy a commit count. Do not copy a model name. Do not copy the release bullets.
- The 16 Nov sentence that no row is dated 16 Nov, and that the first row is a 15 Nov prerelease, is that day's read. It is not this read.
- Codex implicit invocation stays `allow_implicit_invocation` in `agents/openai.yaml` (this pack stays true). Claude `disable-model-invocation` is a different flag. Do not treat that flag as the Codex switch. This skill still ships **no hooks**.
- The description stays the router. The body stays the procedure. Depth stays in `references/`, one level deep from `SKILL.md`. Do not add a second skill format.

### Anthropic (second)

- **New:** raw CHANGELOG.md this read leads with `## 2.1.326` and has no date on that heading. The next headings are `## 2.1.325`, then `## 2.1.323`, then `## 2.1.322`, then `## 2.1.321`. There is no `## 2.1.324`. A missing number is not a wipe.
- GitHub releases Latest is **v2.1.326** (16 Nov, not a prerelease). No release dated 17 Nov. A 17 Nov read of a 16 Nov release is not a 17 Nov binary.
- The 16 Nov sentence that the raw lead is still **2.1.325**, and that no release is dated 16 Nov, is that day's read. Do not invent a date on the raw heading. Do not invent a 17 Nov heading. Do not copy the bullets. Do not copy a model name.
- Claude YAML stays name + description only. The checker body stays 499 lines. Do not claim the body is under 200. Do not claim the body is under 500. Do not claim that 499 is a rewrite.

### Grok Build (third)

- This curl of the public changelog returned **403**. Do not replace the recorded public line **v1.0.77** (5 Nov). Another 403 is not a new binary.
- A search result of the public page still leads with **v1.0.77** (5 Nov). A search result is not this curl. A product page is not the public changelog line. Do not copy a model name.
- **New:** a vendor changelog file numbered above the page lead returned **200**. Its last-modified date is 17 Nov. The next number returned **404**. That file is not the public page. Do not copy that number. Do not copy the bullets. The 16 Nov sentence that the file last-modified date is 14 Nov is that day's read. A 17 Nov file date is not a new public line.

### Shared

- **Latest this read is still 0.169.0 (13 Nov).** The first row of the releases list is a 17 Nov prerelease and is not the Latest badge. A second 17 Nov prerelease row is not the badge either. No stable tag dated 17 Nov.
- **The raw lead is 2.1.326 and has no date.** GitHub Latest is **v2.1.326** (16 Nov). No release dated 17 Nov. There is no **2.1.324**. The 16 Nov sentence that the raw lead is still **2.1.325** is that day's read.
- **This curl returned 403.** Do not replace **v1.0.77**. A vendor file last-modified 17 Nov is not the public line.
- Evals stay **281**. HITL F1–F28 + T1–T69 required. This read adds T70 (still 0.169.0 + a 17 Nov prerelease that is not Latest + raw lead 2.1.326 with no date + another 403 and a 17 Nov file that is not the public line). No new eval heading.
- A content-only observation does not bump the edition. Content notes go through a pull request. Rebase-merge that pull request. Do not push them directly to main.
- Still free-only. Still not legal advice. No secrets.
