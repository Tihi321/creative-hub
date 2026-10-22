# HUB-06 contract check: media lines and aliases (H1)

Started 2026-10-22. Hand-made book, no Scriptorium run. Ticket plan: `.claude/tickets/HUB-06-scriptorium-vn-media-lines/plan.md`.

## Brief

- Idea / theme: a tiny script book written the way Scriptorium SCP-16 (branch `SCP-16-18_hub-roadmap`, worktree `C:\projects\Personal\scriptorium-wt`, not merged) writes one, to check that VN Studio reads it.
- Kind: linear · adults
- Languages: en
- Art: not run · Music: not run · Voices: off (import and inspect only; no pipeline, no build)

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | none (hand-made) |
| Scriptorium book | none; folder `runs/hub-06-media-lines/book/` |
| Book Translator project | none |
| VN Studio project | `hub-06-media-lines` |

## Log

- 2026-10-22 hub.ps1 status: vn-studio up on 7459 (master 81abb9e with VNO-08 importer). Scriptorium and strata down, left down.
- 2026-10-22 Wrote `runs/hub-06-media-lines/book/` (`book.md` with `script: true`, `format: visual-novel`; `outline.md`; `bible/bible.md`; `chapters/ch-01.md`). Layout and front matter copied from `~/Scriptorium/books/the-clockless-god-3` (read only); bible and chapter lines from `scriptorium-wt/docs/visual-novel.md` and `scriptBible.ts` (`scriptBibleLine`: `Aliases:` sentence before `Voice:`).
  - Bible: Mara; Kessler with `Aliases: the bald man, Brother Kessler.` before `Voice:`; 2 places.
  - Chapter: scene 1 has `AMBIENCE:`, `SFX:`, `INSERT:`, `CG:`, `END CG`, speaker `THE BALD MAN` (alias) and cast `the bald man`; the torn page is an `INSERT:`, never `ON SCREEN:`; scene 2 starts with `AMBIENCE: none`. Every cue is followed by a beat in its scene. `CG: none` was not used (END CG covers the stop); only one CG, so only one full image.
- 2026-10-22 `vno_import {source: C:/projects/Personal/creative-hub/runs/hub-06-media-lines/book}` -> slug `hub-06-media-lines`. Preview: 1 chapter, 2 characters, 2 places, `uncertain: 2`, `warnings: []`, `run: null` (language en, confidence 0.871).
- 2026-10-22 `vno_get_story {slug: hub-06-media-lines}` (saved copy `.claude/temp/hub06-story.json`):
  - images: `torn_logbook_page_ink` (display insert), `mara_bald_man_pier` (display full). Neither has a `characters` field (VNO-16 is not in master: expected).
  - sounds: `waves_stone_far_foghorn` (ambience), `boots_running_wet_stone` (sfx).
  - Cues landed on the next beat: ambience on ch01.s01.b001; sfx on b004; insert image on b007 (`I found this on the rocks.`); full image on b008; `image: null` on b009 (END CG); `ambience: null` on ch01.s02.b001 (AMBIENCE: none).
  - Kessler has `aliases: ["the bald man", "Brother Kessler"]`. Speaker `THE BALD MAN` (2 lines) maps to `speakerKey: kessler`, `speakerLabel: THE BALD MAN` (alias kept as name tag). Cast entry `the bald man` maps to `charKey: kessler`. `KESSLER` in scene 2 maps to kessler too.
  - No speaker named CG, SFX, INSERT or AMBIENCE; speaker labels are only MARA (3), THE BALD MAN (2), KESSLER (1).
  - `warnings: []`: no "has no beat after it", no "dropped", no alias-merge report.

## Checked

- By the hub agent, from the import preview and `vno_get_story` JSON only. Nothing built, linted or played.
- Not checked: what `uncertain: 2` holds (the preview gives only a count, and the story JSON does not list them; they go to the script-analyst if the pipeline runs); the real SCP-16 output (needs H2); build of CG, insert, ambience and SFX assets.

## Findings

- Contract holds: all five cue kinds are read, attached to the next beat, and cause no warnings; the alias speaker and cast entry map to the character.
- The `Aliases: ...` sentence stays inside the character's `looks` text (`"Sixty, bald and broad, ... The lighthouse's old engineer. Aliases: the bald man, Brother Kessler."`) as well as in `aliases`. So the sprite prompt will carry that sentence. Harmless but noisy; candidate VN Studio tweak (strip the sentence from looks). Not changed.
- CG has no `characters` (VNO-16 not in master): the faces of a CG would not use the character sheets. H2 needs VNO-16 or a hand `vno_image_set`.

## Left to do

- H2 live run with Scriptorium (needs the user's go-ahead), H3 docs.
- Delete the throwaway project `hub-06-media-lines` from VN Studio when done, or keep it for the next check (ask the user).
