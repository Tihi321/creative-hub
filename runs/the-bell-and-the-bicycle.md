# The Bell and the Bicycle (picture book)

Started 2026-10-25. HUB-17 live production (VNO-47 + SCP-46). Croatian edition hand-written by the Lead from the English pack catalog.

## Brief

- Idea / theme: Lana gets a red bicycle bell; it pops off in the park; Kiki the dog finds it. Ages 3-6, 12 pages.
- Kind: linear · children
- Languages: English source (Scriptorium), Croatian edition
- Art: illustrated (Google Flow if signed in, else ComfyUI) · Music: chiptune (SNES) · Voices: on, Croatian Supertonic narrator

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | `the-bell-and-the-bicycle` |
| Scriptorium book | `the-bell-and-the-bicycle` (expected) |
| Book Translator project | not used (catalog translated by hand) |
| VN Studio project | `the-bell-and-the-bicycle` (expected) |

## Log

- 2026-10-25 17:00 Scriptorium started headless with the factory paused and `max_books_in_progress: 1` (`config/factory.md`, original saved in `.claude/temp/factory.md.backup`); the SCP-46 migration added `kids-picture-book` to `config/formats.md` and the `_pb` prompts arrived.
- 2026-10-25 17:02 `add_story` (format `kids-picture-book`, all roles `client/claude-code`), factory resumed: the editor-in-chief task waits for the client. Writer teammate `pb-book-writer` works the task loop.
- Hub fix found on the way: this session exports `ELECTRON_RUN_AS_NODE=1`, which made `hub.ps1 start scriptorium` run `out/main/index.js` under Node and crash; `Start-Detached` now drops that variable for Electron apps (`scripts/hub.ps1`).
- 2026-10-25 17:11 Book published on the first round: 1 chapter, 12 pages, 586 words, score 8.89, all eight reviewers pass; `vn/pack.json` and `vn/text/en.json` written. Factory paused immediately, Scriptorium stopped, `config/factory.md` restored.
- 2026-10-25 17:13 VN Studio import: format `kids-picture-book`, presentation `picture-book`, 12 scenes, no warnings; settings Flow art, chiptune SNES music, VibeTTS Croatian narrator; pipeline run 1.
- 2026-10-25 17:19 **Live bug:** the writer used semicolons in `ON SCREEN:`, `castOf` split only commas, so the pack had cast `[lana]` on all 12 pages and VN Studio planned one sheet. Pipeline stopped (3 images made). SCP-46 fixed `castOf` (`,` and `;`) and the `settleScenePlaces` comma truncation; 703 tests, typecheck, lint, build green.
- 2026-10-25 17:24 Pack rebuilt (`packHash sha256:e6065d69…`, 46 beats, cast 2-4 per page), project deleted and re-imported: 12 page assets + 4 sheets + cover. Croatian edition added from `runs/the-bell-and-the-bicycle/vn-text-hr.json`. Pipeline run 2 started.
- 2026-10-25 17:32 Art plan by the client (17 prompts: 12 pages, 4 sheets, cover), music by the composer (`music_01`, snes, 75 bpm, C, 102 s).
- 2026-10-25 17:55 Pages generated one by one by Google Flow (free), sheets before pages so the page refs exist.
- 2026-10-25 16:58Z (18:58 local) Pipeline done: cover v1, 34 voice clips per language (en and hr), stage, build (0 placeholders, 0 warnings, 1 translation) and lint clean (12 pages). Game opened in the browser.
- Scriptorium stopped and `config/factory.md` restored (`paused: false`, `max_books_in_progress: 10`); hub `logs/` untouched otherwise.

## Checked

- Images read: sheets lana/tomo/kiki (likeness matches the bible), pages s01 (Mama gives the bell), s03 (park gate with Tomo and Kiki), s05 (the bell pops off over the root), s07 (Kiki digs in the leaves by the red bench), s11 (yellow door, four characters), s12 (bedtime, bell on the nightstand). Style is consistent watercolour; all 12 pages exist, no placeholders.
- `game-data.json`: `presentation: "picture-book"`, 12 scenes, `bgPath` per scene, editions `en` + `hr`, Croatian title `Zvonce i bicikl`, Croatian beats and 34+34 voice entries.
- Build/lint: `build` 0 placeholders / 0 warnings / 1 translation; `lint` clean (12 pages). Full test suites of both repos green (VN Studio 1087; Scriptorium 703), typecheck and lint clean.

## Left to do

- The user plays the book (page turns, Croatian switch, read-aloud replay, Load on the last page) and says whether it works; write the verdict here.
- No commits or pushes; the three branches are ready for the user's decision.

