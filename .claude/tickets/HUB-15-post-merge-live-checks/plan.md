# HUB-15: live checks of the 2026-10-23 fixes, now merged

Written 2026-10-23. Every fix found by the 2026-10-23 productions is merged to master (Scriptorium PR #11, Book Translator PR #13, VN Studio PR #12, flow-music-mcp PR #6, hub PR #8), tested (Scriptorium 629 + recovery, Book Translator 313, VN Studio 930, flow-music-mcp 154, hub planner 15), and the running services were rebuilt and restarted from master. Most fixes were only unit-tested. This ticket runs them for real.

Branch: `HUB-15_post-merge-live-checks` (hub; run logs, this plan, the changelog). No tool code is planned; a bug found goes into that tool's `ROADMAP.md` and is fixed there on its own branch, one commit per ticket (the user's rule, 2026-10-23).

## Decisions already made (user, 2026-10-23)

- Scriptorium may be started; Claude does architect, writer, humanizer and editor-in-chief work through `client/claude-code`; reviewers run on Scriptorium's models (deepseek-flash, cents). Daily cap $5.
- Flow images are the default image provider (`make-visual-novel` skill). Flow credits: agreed budgets, may go over when needed.
- Scriptorium's fallback list starts with `deepseek/deepseek-flash` (the retired `:free` minimax was replaced in `~/Scriptorium/config/settings.md`).

## Checks

### C1. Scriptorium VN adaptation (SCP-28, 34, 35, 36, 37)

- [x] Pick a short published book (`list_books`; not the lighthouse one, which already has two adaptations). Write the brief so some `SCENE:` lines carry a weekday.
- [x] `adapt_book {book, format: "visual-novel", models: {architect, writer, humanizer: "client/claude-code"}}`. Answer client tasks for that book only.
- [x] SCP-28: the start job makes no model call (job log), the book has the source's title and genre.
- [x] SCP-37: `book.md` has `target_words` about 1.7 x the source words (clamped to the VN range, min 8,000) and `target_from_source_words`; no "grow every chapter" length rewrites. **Target verified; a grow rewrite still ran (drafts at 77%): SCP-42.**
- [x] SCP-34: a `SCENE: Place, Weekday, time` line keeps its weekday after drafting and humanizing. **Bare weekdays verified; other day words cut: SCP-38, SCP-39.**
- [x] SCP-35: no cue line is the last line of a scene (log shows a move if one was); VN Studio's `vno_import` gives no "dropped cue" warning.
- [x] SCP-36: the book's repetition report lists no `scene ...`, `on screen ...`, `ambience ...` phrases.
- [x] Stop at the published book plus `vno_import` (preview only); no images needed.

### C2. Scriptorium screenplay (SCP-29)

- [x] `adapt_book {book: <same book>, format: "short-film", models: {architect, writer: "client/claude-code"}}`. **`the-local-patch-3`, published at round 2, score 7.09. Round 1 was rejected at 6.73 under `max_rounds: 1` and reopened with `reopen_book {mode: "rewrite"}`.**
- [x] No word-count length requests; any length request is in seconds / shots; `get_screenplay` runtime inside the format's range. **Verified: the prompts ask for "about 60 seconds ... count seconds, not words". Length gate `ok, seconds: 120`; no `--len` rewrite; runtime 120 s in [60, 180], 18 shots.**
- [x] Stop at the published screenplay (no Flow video).

### C3. Puzzle mystery (SCP-30, 31, 32, 33; VNO-25, 26, 29, 30, 31)

- [x] `vno_puzzle_generate` a Murdle and a Knights and Knaves core (and a testimony core: VNO-25 should no longer repeat; check `repeats()` is empty), then `add_story {format: "mystery-puzzle-visual-novel", puzzles}` with full names in the brief and short names used in the outline (as *The Winter Garden Clock* did).
- [x] SCP-33: one bible entry per person, the short name as an alias.
- [x] SCP-30: the knights statements are planted only in the puzzle chapter.
- [x] SCP-31: no hint of the knights answer before `PUZZLE:`; later chapters agree with it.
- [x] SCP-32: no review round asks to change a `CLUE:` line (dropped requests are logged). **Not exercised (no such request came).**
- [x] VN Studio import: VNO-26 every knights speaker has a statement; VNO-29 the read-back includes the intro rule and passes (separate reader subagent); VNO-30 evidence pictures are shown on their lines; VNO-31 the art plan's place descriptions are complete. **VNO-26, 29 verified; VNO-30 verified in data only; VNO-25 and VNO-31 partly (VNO-36, VNO-37).**
- [x] Optional: build it with Flow images and give it to the user to play. **Done during C4: 63 assets generated (42 Flow images, 13 ACE-Step music/ambience tracks), game cleanly built and linted.**

### C4. Flow and ComfyUI side by side (VNO-28)

- [x] Two small VN projects at once, one `art.provider: flow`, one ComfyUI; `vno_status` shows an image job of each running at the same time. (C3's build can be the Flow one.) **Verified: Flow image jobs (`sheet_luka_bencic`, `sheet_bruno_orsini`, `sheet_mira_valenti`) and ComfyUI image jobs (`bg_harbour_night`, `cover`) captured running simultaneously across 19 polling samples. Run log `runs/hub15-c4-parallel.md`.**

### C5. Gemini daily quota (VNO-24, FMM-15)

- [x] After the quota resets (about 09:00 on 2026-10-24): `vno_run_pipeline {slug: "hub07-flow-test", from: "voice"}` makes the 6 missing Croatian clips (transcribe two with `flow_transcribe {language: "hr"}`). **Verified: all 6 clips generated cleanly (9/9 Croatian clips in game); transcribed `ch01.s01.b004` and `ch01.s01.b006` with 100% exact match.**
- [x] If the quota runs out again: the job stops at once with one "daily quota, resets at ..." message (VNO-24) and `flow_narrate`'s error says "daily" (FMM-15). **Quota did not run out on rerun (all clips succeeded); daily quota detection already verified in initial run.**

### C6. The user's verdicts (closes HUB-06, 07, 08, 10, 11, 13)

- [ ] Ask the user to play or watch, and write their notes in each run log: the film (`runs/the-lighthouse-that-kept-lists-2/video/out/final.mp4`), *The Winter Garden Clock*, *The Lighthouse That Kept Lists (VN)*, `hub07-flow-test`, `hub08-13-autostart`. Bugs they find go to the right tool's `ROADMAP.md`.

## Not in scope (optional backlog, only if the user asks)

VN Studio "Later" (start buttons, VibeTTS auto-start, "Open in" lock clash, hard kill leaves services, Flow extras, help strings for 35 more languages); flow-music-mcp Studio panel, Scenes/Library automation, rename, and its stale "Later" lines (VN Studio as a client and screenplay to video are done); comfy-mcp bypassed subgraphs and more TTS engines; HUB-09 (on hold); a native-speaker menu check.

## Done when

C1 to C5 are checked with results in run logs (`runs/<slug>.md`) and a `changelog.md` here, every bug found is in its tool's roadmap or fixed, and C6 has the user's verdicts.
