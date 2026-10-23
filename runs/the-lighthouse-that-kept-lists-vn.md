# The Lighthouse That Kept Lists (VN)

Started 2026-10-23. HUB-06 step H2: live run of Scriptorium's VN media lines (`CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, bible `Aliases:`) into VN Studio. Ticket plan: `.claude/tickets/HUB-06-scriptorium-vn-media-lines/plan.md`; contract check (H1): `runs/hub-06-media-lines.md`.

## Brief

- Idea / theme: adapt the published book `the-lighthouse-that-kept-lists` (Tobias Wren, short story, 4 chapters) into a visual novel script.
- Kind: linear · adults
- Languages: en
- Art: illustrated (ComfyUI) · Music: project default · Voices: off · SFX and ambience: chiptune engines (`sound.sfxEngine`/`ambienceEngine: chiptune`), no hand-made files

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | `the-lighthouse-that-kept-lists-vn` |
| Scriptorium book | `the-lighthouse-that-kept-lists-vn` (published, score 7.79) |
| Book Translator project | none |
| VN Studio project | `the-lighthouse-that-kept-lists-vn` |

## Log

- 2026-10-23 12:19 Services already running from master builds (Scriptorium 7341, VN Studio 7459, ComfyUI 8188, Chiptune, Pixel Studio, flow-music-mcp); MCP links down, every call via `scripts/hub.ps1 call`. Scriptorium `factory_status`: idle, spend today $0, month $6.52 (caps $5/day, $40/month), LM Studio and Strata down.
- 2026-10-23 12:19 `adapt_book {book: the-lighthouse-that-kept-lists, format: visual-novel, title: "The Lighthouse That Kept Lists (VN)", models: {architect, writer, humanizer: client/claude-code}}` -> story `the-lighthouse-that-kept-lists-vn`. Reviewers on Scriptorium's own models.
- 2026-10-23 12:20-12:29 `wait_for_book {slug: the-lighthouse-that-kept-lists-vn, timeout_seconds: 540}` -> `reason: timeout`, `book: null`, no client tasks. `factory_status`: nothing running, `clientTasks 0/0`, spend unchanged ($0 today).
- 2026-10-23 12:30 Cause: three `start_book` jobs for this story failed in `~/Scriptorium/jobs/failed/` (`eic--start--n22--r0`, `n23`, `n24`, created 12:24:51 to 12:25:09, 3 attempts each, model `openrouter/minimax/minimax-m3.1-flash:free`). Failure text: `HTTP 404: The free launch period for MiniMax M3.1 Flash ended on Oct 22, 2026. The :free variant has been retired; use minimax/minimax-m3.1-flash (list price $0.15/M in, $0.60/M out)`. After 3 failed start jobs the factory stops starting any book (`startBooks` in `src/engine/pipeline/pipeline.ts`: "starting a book failed 3 times. Not trying again until the failed jobs in jobs/failed/ are removed").
- 2026-10-23 12:32 Stopped here (blocked for real; a fix needs a Scriptorium config change and removing files from its data folder, which this run may not do). No book, no VN Studio project.
- 2026-10-23 ~12:35 Unblocked by the coordinator with the user's choice: the retired fallback row in `~/Scriptorium/config/settings.md` is now `deepseek/deepseek-flash`; the three failed start jobs were moved to the hub's `.claude/temp/scp-failed-starts/`. The start ran on deepseek.
- 2026-10-23 12:38 Book `the-lighthouse-that-kept-lists-vn` (stage pitch, target 18,000 words). Client loop (Claude as architect and writer), tasks leased only with `book: the-lighthouse-that-kept-lists-vn`:
  - pitch (`--pitch--book--r0#1`) accepted;
  - outline (`--outline--book--r0#1`, JSON) accepted: 6 chapters, source chapters [1],[1],[2],[2],[3],[4]; characters Mara, Dino (`aliases: the harbour master`), Ivka (`teta Ivka`), Luka, Crewman (`the older man`); 9 places; Ante and Katica left out on purpose (never on screen);
  - drafts ch01..ch06 (`--draft--chNN--r0#1`) accepted, 1,779 / 1,540 / 1,420 / 1,433 / 1,897 / 2,175 words (about 10,200, under the 18,000 target, inside the format's 8,000 to 25,000). Cue lines written per chapter: CG 2/2/1/2/2/2, INSERT 2/2/2/2/2/1, SFX 3/3/2/3/2/2, AMBIENCE in most scenes, END CG after most CGs; ch06 uses the alias `THE OLDER MAN` as a speaker and `the older man (...)` in `ON SCREEN`.
  - length fix (`--rewrite--chNN--len#1`, "too short, about 3000 words each"): all six expanded (ch01 2,669, ch02 2,263, ch03 1,929, ch04 1,958, ch05 2,424, ch06 2,465; ch06 gained a Friday-morning harbour office scene from the source's narration). Cues kept.
  - humanize r0 ch01..06: small edits only (the counter's "rows of three" and "a long moment"); every cue line kept word for word; all accepted, no refusals.
  - review round 1 (deepseek reviewers) -> rewrite r1 ch01 (inventory "seven this morning", the doorway sentence, the raincoat sequence) and ch06 (Friday in the ferry ramp heading, the reply list numbering, the crew leaving without the pole); humanize r1 ch01, ch06.
  - review round 2 -> rewrite r2 ch01 (planted the Split agent and his jacuzzi plans for Ante's list item 1; the chicken man's reported speech), ch02 (wording), ch03 (wording), ch04, ch05 unchanged (the continuity note on 35 + 15 = 50 years of lemons was wrong: it matches the source and the "fifty years" of good lemons), ch06 (blotting simile); humanize r2 ch01..06 (small edits or none).
- 2026-10-23 12:55 Book **published**, score 7.79, round 2, 6 chapters, 13,710 words. Scriptorium spend: today $0.168 (month $6.69); the book's reviewers on deepseek about $0.15 in all, Claude's roles (architect 2 jobs, writer 20, humanizer 14) $0.
- 2026-10-23 12:55 Book checks (`get_script`, `read_book_file bible`, chapter grep): see "Checked" below. One SFX cue is the last beat of its scene (ch02 s02, the padlock): my own writing mistake as the client writer (the `SFX:` line sat just before a `---` break); nothing in Scriptorium caught it.
- 2026-10-23 12:55 `vno_import {source: the-lighthouse-that-kept-lists-vn}` -> VN project `the-lighthouse-that-kept-lists-vn`. Preview: 6 chapters, 7 characters, 9 places, `uncertain: 161`, language en (0.892), one warning: `chapter 2: a SFX line at the end of a scene has no beat after it in its scene: dropped` (the padlock, as above). Story: 11 full images, 11 inserts, 25 sounds (12 sfx, 13 ambience). Aliases kept: Dino `[the harbour master]`, Ivka `[teta Ivka]`, Crewman `[the older man]`; speaker `THE OLDER MAN` -> `speakerKey crewman`, label kept (4 lines); cast entry `the older man` -> crewman. No alias-merge report. Title imported as "The Lighthouse That Kept Lists" (the "(VN)" suffix dropped).
- 2026-10-23 12:56 Hand edits in VN Studio (not to the script or bible), `vno_image_set`: `mara_dino_dark_alley` characters `[mara, dino, ivka]` -> `[mara, dino]` (Ivka is only in "behind Ivka's shop"); inserts `teleprinter_sheet_headed_ivka` `[ivka]` -> `[]` and `long_teleprinter_sheet_headed` `[mara]` -> `[]` (a paper sheet, the name is only in its heading).
- 2026-10-23 12:56 `vno_update_settings`: `sound {sfxEngine: chiptune, ambienceEngine: chiptune}`, `models` art-director, script-analyst, composer, stage-director = `client/claude-code`. Art illustrated (qwen-image-2.1, the default), music ace-step 3 tracks (default), voice off.
- 2026-10-23 12:56 `vno_run_pipeline {slug}` run 1. Client tasks answered (only `book: the-lighthouse-that-kept-lists-vn`): analyse `vn.analyse--all--r1#1..#6` (161 items: free-form expressions mapped to the 8 standard ones, scene times from the SCENE text, the three "alias" pairs Ivka/Dino, Crewman/Dino, Crewman/Luka answered as different people); art plan `vn.art.plan--all--r1#1..#7` (17 backgrounds, 5 sheets, 23 sprites, 11 CGs, 11 inserts, cover; no text in any prompt); music plan `vn.music.plan--all--r1#1` (3 tracks: menu accordion waltz, chapter theme guitar and clarinet, night piano and cello; ch1, 2, 4 -> music_02, ch3, 5 -> music_03, ch6 -> music_01).
- 2026-10-23 12:59-17:37 Generate: 99 assets (17 backgrounds, 5 sheets, 23 sprites, 11 CGs, 11 inserts, cover, 3 music tracks, 11 sfx, 13 ambience; Ante and Katica got no sheet or sprite). 0 failed. From 15:22 to about 17:05 no job of this project ran: another production's tool-requested run took the shared queue (see Found). Chiptune fell back to a stock sound for 5 sounds (log warnings): `ferry_deep_horn_sounding`, `handheld_receiver_shrieking_two`, `heavy_wooden_crate_thumping`, `teleprinter_paper_tearing_cleanly` -> `blip`; ambience `two_warbling_radio_tones` -> `drone`.
- 2026-10-23 17:37 Stage director client tasks `vn.stage--all--r1#1..#6` (one per chapter): slots (one on screen center, two left/right, three left/center/right, kept while they stay), `fade` for the first scene and after a `---` break, `dissolve` otherwise, no pauses, music left to the plan, no extra cues except one: the padlock SFX that the import dropped, put back on `ch02.s03.b001`.
- 2026-10-23 17:38 Build: `game` folder written, theme classic-dark, 0 placeholder images, 1 warning: `ch02.s03.b001: sound effect heavy_padlock_snapping_open has no file yet: skipped` (the dropped cue has no asset; `vno_asset_generate {only: [sfx_heavy_padlock_snapping_open]}` -> "No asset matches", `vno_sound_set` again added none). Lint: **clean** (995 dialogue blocks). Pipeline summary (director on deepseek): built cleanly, nothing failed.
- 2026-10-23 17:39-17:44 `vno_asset_regen {id: cg_mara_reading_teleprinter_sheet, seed: 4242}` (v1 drew Mara as a second Ivka): v2 has the same fault; kept v2 (selected and rebuilt by the regen). No other regen, to spare the shared ComfyUI.

## Checked

- Source book `the-lighthouse-that-kept-lists` is published, 4 chapters (read in full, for the client writing).
- `get_script {book}` (copy in `.claude/temp/hub06-h2/script.json`), cues with a picture or sound per chapter (END CG and `AMBIENCE: none` not counted):

  | ch | CG | INSERT | SFX | AMBIENCE | END CG | AMBIENCE none | scenes |
  |---|---|---|---|---|---|---|---|
  | 1 | 2 | 2 | 2 | 4 | 2 | 1 | 6 |
  | 2 | 2 | 2 | 3 | 5 | 2 | 0 | 6 |
  | 3 | 1 | 2 | 2 | 2 | 1 | 1 | 5 |
  | 4 | 2 | 2 | 3 | 3 | 1 | 0 | 5 |
  | 5 | 2 | 2 | 2 | 5 | 2 | 0 | 6 |
  | 6 | 2 | 1 | 2 | 7 | 2 | 0 | 9 |

  All inside the limits (CG at most 2, INSERT at most 2, SFX at most 4). No line beat with speaker CG, SFX, INSERT or AMBIENCE (speakers: Mara 357, Dino 153, Ivka 116, Crewman as `the older man` 4, Luka 3). One cue is the last beat of its scene: ch02 s02 SFX (padlock), followed only by a `break` beat.
- `read_book_file {file: bible}`: every character is one bullet; `Aliases:` comes before `Voice:` for Dino (`the harbour master`), Ivka (`teta Ivka`), Crewman (`the older man`); no alias names another character. Mara and Luka have none. The engine added two source characters with no looks of their own, `Ante Bašić` and `Katica Bašić` (from the source bible; never on screen; VN Studio made no sheet or sprite for them).
- `ON SCREEN` lines in the six chapter files: only Mara, Dino, Ivka, Luka and `the older man`; no prop.
- VN Studio import and story JSON: see the Log (images and sounds, aliases, CG characters, one dropped-cue warning).
- Looked at (Read tool): `sheet_mara` (yellow raincoat, grey jumper, dongle on lanyard, laptop bag: on-model, a little androgynous, the "oil on fingertips" drawn as smudges on the face too), `sheet_dino` (navy jacket, tie, clipboard, moustache: good), `sheet_ivka` (black cardigan, white bun, chain: good, glasses worn rather than on the chain).
- Looked at after the build: CGs `cg_dino_filling_mara_doorway` (Dino right; Mara in raincoat and pyjamas but with a brown bun, off-model), `cg_mara_half_risen_crate` (Mara on-model, red and green lamps glowing; the crate drawn as a big box she stands in), `cg_ivka_kitchen_chair_beside` (all three right, back room right), `cg_mara_ivka_dino_walking` (Ivka drawn as an old man), `cg_mara_typing_teleprinter_keyboard` (Dino twice), `cg_mara_reading_teleprinter_sheet` v1 and v2 (two Ivkas); insert `cg_two_scraps_old_masking` (clean receiver face, one tape strip above the lamps, no text); sprites `sprite_mara_happy`, `sprite_dino_sad` (consistent with the sheets, clean cut-out); background `bg_service_room_night` (no roof); `cover` (lighthouse, causeway, small yellow coat, beam: very good, left third calm).
- Build and lint: built, lint clean (995 dialogue blocks), 0 placeholder images, 1 build warning (the padlock SFX).
- Not checked: the game was not launched or played by me; no sound or music was listened to (chiptune SFX and ambience, ACE-Step tracks); the other 7 CGs, 10 inserts and most backgrounds and sprites were not looked at; the CG `characters` hand edit was not compared on screen.

## Play

```powershell
& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\the-lighthouse-that-kept-lists-vn\game"
```

## Found

- **Scriptorium: the editor-in-chief has no model of its own, and the first fallback model is retired.** `agents/editor-in-chief-edith-marlowe.md` has `model: null`; `config/settings.md` `fallbacks` is `openrouter/minimax/minimax-m3.1-flash:free`, `strata/qwen3.8-flash-next`, `lmstudio/...`. The `:free` variant answers 404 since 2026-10-22, and Strata and LM Studio are down, so every `start_book` fails. The `config/models.md` entry (line 47, `minimax/minimax-m3.1-flash:free`) is the same retired id. Agents whose `model:` is empty or a list may also rely on the fallbacks (architect, archivist-ruth-calder, fact-checker, humanizer, idea-generator, read-aloud-reviewer: not checked one by one).
- **Scriptorium: `adapt_book {models}` does not cover the editor-in-chief's `start_book`.** The story's `role_models` name architect, writer and humanizer only, so `start_book` used the editor-in-chief's own model (the retired fallback). The docs say the start is a client task only "when the story's models name one" for that role; an adaptation needs no editorial choice, so the start could skip the model, or `adapt_book` could say that `editor-in-chief` belongs in `models`.
- **Scriptorium: a 404 "model retired" was retried 3 times on the same model per job, and 3 jobs in a row** (9 calls in 18 s), then the factory blocks every book start until a person deletes the failed job files. One user story with a dead model blocks every other story's start too (the other agent's `the-lighthouse-that-kept-lists-2` short film, and the factory's own ideas).
- **Scriptorium: the SCENE place fixer drops the weekday.** A SCENE line `Place, Weekday, time` loses its weekday: `SCENE: Ferry deck, Monday, late afternoon` was written as `SCENE: Ferry deck, late afternoon`. Evidence: `~/Scriptorium/books/the-lighthouse-that-kept-lists-vn/log.md`, draft ch01 job: `SCENE place "Ferry deck, Monday" written as the bible's "Ferry deck"` (also `The riva, Monday`, `Ante's kitchen, Tuesday` twice), and the chapter files keep only the time. The continuity checker then flagged the missing "Friday" on the ferry ramp scene. A weekday at the end (`a quarter to five on Friday`) survives. The fixer seems to take `<place>, <weekday>` as the place name when it does not match the bible.
- **Scriptorium: nothing catches a cue as the last line of a scene.** The ch02 padlock `SFX:` sat right before `---`; the humanizer guard, the line editor and the reviewers passed it, and `get_script` shows it as a `cue` beat followed by a `break` beat (so a check of "last beat is a cue" must skip `break`). VN Studio drops it with a warning (as designed). The plan's Risk list foresaw this; an engine-side move of a trailing cue before the scene's last beat would fix it.
- **Scriptorium: the humanizer counter flags cue lines it also says to keep word for word.** Its "repeated phrase" list counts `AMBIENCE:` texts, `SCENE:` places and `ON SCREEN:` looks (`ambience wind pushing at`, `scene the back room`, `on screen mara raincoat`), which the same prompt forbids changing. The ambience repeats on purpose (the same key replays the same loop).
- **Scriptorium: the length fix asks every chapter of a short adaptation to grow.** The VN format target (18,000 words) is applied to an adaptation of a 5,900-word short story, so all six chapters went through a length rewrite (10,212 -> about 13,600 words). Not wrong, but an adaptation's target could follow the source's length.
- **VN Studio: CG and insert `characters` (VNO-16) match a name inside a possessive or a heading.** `mara_dino_dark_alley` ("...behind Ivka's shop") got `ivka`; the inserts `teleprinter_sheet_headed_ivka` ("FOR IVKA") and `long_teleprinter_sheet_headed` ("FOR MARA") got `ivka` / `mara`. Fixed by hand with `vno_image_set`. Inserts might not need characters at all.
- **VN Studio: one shared art queue, no fairness between projects.** From 15:22 my generate jobs (41 queued, 62 of 99 done) stopped while `the-winter-garden-clock` run 3 generated one asset after another (`jobs/running`: its sprites, created 13:22). Jobs asked for with a tool have priority 1 over a pipeline's chain (priority 0), so a second project's regen run starves a running pipeline until it is empty. Not a bug by the doc ("Order" in `docs/mcp-guide.md`), but with three productions at once it stalls the others for hours.
- **VN Studio: a dropped cue's sound stays in the catalogue with no asset, and the stage director may still use it.** `heavy_padlock_snapping_open` is listed in `sounds` and offered to the stage director, but the asset list is derived from the beats only, so no `sfx_` asset exists; a stage-plan cue on it is skipped at build with a warning, and neither `vno_asset_generate {only}` nor `vno_sound_set` creates it.
- **VN Studio art: a CG with two character sheets can merge them.** `cg_mara_reading_teleprinter_sheet` (Mara and Ivka) drew two Ivkas, twice (v1, and v2 with seed 4242); `cg_mara_typing_teleprinter_keyboard` (Mara, Ivka, Dino) drew Dino twice and Mara off-model; `cg_mara_ivka_dino_walking` drew Ivka as an old man with a moustache. `cg_ivka_kitchen_chair_beside` (the same three) came out right. Single-character CGs and the cover are good.
- **VN Studio art: the teleprinter is drawn as a typewriter everywhere**, and `bg_service_room_night` has no roof (an open ruin under the night sky). Prompt wording (mine, as art director) could be firmer.
- **VN Studio: the import drops "(VN)" from the title** ("The Lighthouse That Kept Lists"); fine for the game, but the project title then equals the source book's.
- **Fix options given at 12:32 for the start block (the user chose 2 and 3, applied by the coordinator):**
  1. `set_model {role: "editor-in-chief", model: "deepseek/deepseek-flash"}` (as most reviewers use), or `update_story {story: the-lighthouse-that-kept-lists-vn, models: {editor-in-chief: client/claude-code, architect: client/claude-code, writer: client/claude-code, humanizer: client/claude-code}}` (the story has no book yet, so it may be edited);
  2. replace the fallback row `openrouter/minimax/minimax-m3.1-flash:free` in `config/settings.md` (paid `minimax/minimax-m3.1-flash`, or deepseek);
  3. delete `~/Scriptorium/jobs/failed/eic--start--n22--r0.md`, `n23`, `n24` so the factory starts books again.

## Left to do

- The user plays it (the production is done only then). Ask about the CGs, inserts, ambience and SFX, and write the answer here.
- Optional art fixes, each a `vno_asset_regen` (or `vno_image_set` with one character, then regen): `cg_mara_reading_teleprinter_sheet` (two Ivkas), `cg_mara_typing_teleprinter_keyboard` (two Dinos), `cg_mara_ivka_dino_walking` (Ivka as a man), `cg_dino_filling_mara_doorway` (Mara's hair), `bg_service_room_night` (no roof).
- Optional sounds: import real files (`vno_asset_import`) for the five chiptune fallbacks and the padlock.
- HUB-06 H3 docs; tool tickets for the findings above (Scriptorium: SCENE weekday, trailing cue, humanizer counter, adaptation length; VN Studio: CG characters, dropped-cue sound, two-sheet CG merge, queue fairness).
