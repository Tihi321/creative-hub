# PRs of the hub roadmap run (2026-10-22)

`gh` is not installed here, so the branches are pushed and each PR is opened from its compare link. Title and description below each link.

## scriptorium: SCP-16-18_hub-roadmap

https://github.com/Tihi321/scriptorium/compare/master...SCP-16-18_hub-roadmap?expand=1

**Title:** SCP-16 to SCP-18: VN media lines, screenplay writer, mystery with puzzles (+ SCP-20 to SCP-25 roadmap)

**Description:**

Hub tickets HUB-06, HUB-11 (phase 1) and HUB-10 (phase 4), from the creative hub's roadmap run.

- **SCP-16, VN media lines and bible aliases (HUB-06).** VN scripts carry `CG:`, `INSERT:`, `SFX:`, `AMBIENCE:` (and Croatian keywords), copied from VN Studio's importer; the bible writes an `Aliases:` sentence before `Voice:`; `get_script` returns `cue` beats; the EPUB and reader show cues as small notes; the humanizer keeps cue lines. Checked against VN Studio master: a hand-made book in this format imports with every cue and alias (hub H1).
- **SCP-17, the screenplay writer (HUB-11 phase 1).** Formats `short-film`, `cartoon`, `kids-cartoon` (`screenplay: true`, humanizer off, never picked for a topic-less idea), `_sp` prompts, `SHOT`/`MUSIC`/`TITLE` lines, `get_screenplay` (shots with seconds, lines, music cues, runtime), `adapt_book` to a screenplay. Contract in `docs/screenplay.md`.
- **SCP-18, mystery with puzzles (HUB-10 phase 4).** Format `mystery-puzzle-visual-novel`; `add_story {puzzles}` takes VN Studio's puzzle cores, kept as `bible/puzzles.md`; the outline places puzzles, the writer plants `CLUE:` / `EVIDENCE:` lines before `PUZZLE:`, `TESTIMONY:` blocks; the continuity review checks the planting; `get_script` returns clue, evidence, puzzle and testimony beats. Contract in `docs/visual-novel.md` "Puzzles".
- **SCP-20 to SCP-25 (roadmap only):** findings from the HUB-04 live check (`title_fixed` ignored at publish, story year guessed from the text, interleaved `log.md`, pitch length, research for bedtime stories, silent second instance).

Tests: 571 vitest, recovery test, typecheck, lint, `yarn seed:hashes` clean. Not run: a real model writing these formats (hub live runs after merge), `yarn test:electron`.

Merging and restarting Scriptorium resumes its factory; the hub asks before that. New seed migrations: `migrateScreenplay`, `migratePuzzles` (formats appended), prompt upgrades for unedited prompts.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## flow-music-mcp: FMM-11-12_hub-roadmap

https://github.com/Tihi321/flow-music-mcp/compare/master...FMM-11-12_hub-roadmap?expand=1

**Title:** FMM-11, FMM-12: voice hooks for VN Studio; flow_assemble timeline

**Description:**

Hub tickets HUB-07 (phase 2) and HUB-11 (phase 2a).

- **FMM-11:** `flow_narrate` gets `format` (mp3, wav, ogg, m4a; default m4a), text up to 4000 characters for gemini and windows (400 for flow); `flow_voices` returns Gemini voices with gender, the Gemini TTS model in use (default `gemini-3.8-flash-tts`, `FLOW_MUSIC_MCP_GEMINI_TTS` overrides) and every Windows voice with culture and gender; a 429 says "rate limited". Live: an English and a Croatian Gemini mp3; Windows voices in four formats.
- **FMM-12:** `flow_assemble` clips may be `{file, from?, to?}` trims or `{image, seconds, zoom?}` stills; `music_cues` with windows and fades; `duck` (sidechain on the voice); a `timeline` in the result. Live with synthetic media: an 11 s film with stills, a trim, two cues and ducking.

Tests: 146 vitest, `yarn build`. Not run: real Flow clips, Croatian by ear, `engine: flow` (credits).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## book-translator: BTT-15-20_hub-findings

https://github.com/Tihi321/book-translator/compare/master...BTT-15-20_hub-findings?expand=1

**Title:** BTT-15 to BTT-20: Roadmap: findings from the hub's Croatian translations

**Description:**

Roadmap only. Found while Claude translated *The Clockless God* VN script (HUB-02) and *The Hour That Happens Twice* (HUB-05) into Croatian through the client provider on master 2a21970: false "untranslated" QA flags on VN lines (BTT-15), the glossary pass overwriting the brief (BTT-16), substring glossary matching (BTT-17), the English cover in translated EPUBs (BTT-18), a stale lock with a reused pid (BTT-19), client-loop ergonomics (BTT-20).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## midi-generator: MDI-06_vn-sfx-done

https://github.com/Tihi321/midi-generator/compare/master...MDI-06_vn-sfx-done?expand=1

**Title:** MDI-06: Roadmap: compose_sfx is now called by VN Studio

**Description:**

Roadmap only. The last open item (VN Studio calling `compose_sfx`) is done in VN Studio as VNO-19 (hub ticket HUB-13): `sound.sfxEngine` / `sound.ambienceEngine: "chiptune"`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## visual-novels-orchestrator: VNO-10-19_hub-roadmap

https://github.com/Tihi321/visual-novels-orchestrator/compare/master...VNO-10-19_hub-roadmap?expand=1

**Title:** VNO-10 to VNO-19: cue characters, chiptune SFX, studio autostart, Flow provider, puzzle visual novels

**Description:**

Hub tickets HUB-06, HUB-13, HUB-08, HUB-07 and HUB-10, from the creative hub's roadmap run.

- **VNO-16 (HUB-06):** CG and insert images get their characters from the cue text; the bible's `Aliases:` sentence is taken out of a character's looks.
- **VNO-19 (HUB-13):** `sound.sfxEngine` / `sound.ambienceEngine: "chiptune"` make `sfx_` and `amb_` sounds with Chiptune Studio's `compose_sfx`.
- **VNO-11 (HUB-08):** VN Studio starts Pixel Studio, Chiptune Studio and ComfyUI when a job needs them (`seed/config/autostart.md`).
- **VNO-10 (HUB-07):** a flow-music-mcp client with session renewal; `art.provider`, `voice.provider` and `music.provider` `flow`.
- **VNO-12 to VNO-14 (HUB-10 phases 1 to 3):** puzzles made and proved by code (Python `vno_puzzles`, run with the Ren'Py SDK's Python): Murdle (3x3, 4x4 with motive), Knights and Knaves, testimony (cross-examination with a court record), logic grids. Puzzle beats, `vno_puzzle_*` tools, the flavour read-back check, Ren'Py screens.
- **VNO-15 (HUB-10 phase 4):** `CLUE:`, `EVIDENCE:`, `PUZZLE:`, `TESTIMONY:` … `END TESTIMONY` lines (and Croatian keywords) and `bible/puzzles.md` read at import, as in Scriptorium's `docs/visual-novel.md`; cores proved at import; warnings name the chapter; editions aligned by clue id.
- **ROADMAP:** VNO-20 (lost ComfyUI prompt leaves a job running), VNO-21 (hr UI strings on older projects).

Tests: 903 vitest (67 files), typecheck, lint; Python tests per kind; the Ren'Py PoC self-test (5 cases); `renpy lint` clean on the new integration cases. Not run: a Flow job with real credits, autostart against real studios, a book written by Scriptorium in the puzzle format, the puzzle screens looked at or played by the user.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## creative-hub: HUB-02-13_roadmap-tasks

https://github.com/Tihi321/creative-hub/compare/master...HUB-02-13_roadmap-tasks?expand=1

**Title:** HUB-02 to HUB-13: the hub roadmap run (live checks, Croatian editions, skills for the new tool features)

**Description:**

- **HUB-12:** `hub.ps1 start` returns when piped (WMI detached start); deep `call` arguments survive; logs append.
- **HUB-02:** Book Translator live check; the Croatian VN edition of *The Clockless God*, aligned 1221/0/0 in VN Studio.
- **HUB-03:** VN Studio live check: `vno-media-test` with CG, insert, SFX, ambience, scene music; ja, ar, hr editions.
- **HUB-04:** Scriptorium live check; the skill waits with `wait_for_book`.
- **HUB-05:** *The Hour That Happens Twice* in Croatian (EPUB), all model work by Claude, $0.
- **HUB-06 H1:** a hand-made SCP-16 book imports into VN Studio with every cue line and alias.
- **HUB-11:** `make-video` skill and `scripts/video-plan.mjs` (14 tests).
- **HUB-06/07/08/10/13:** skill, README, CLAUDE.md, `services.json` and ROADMAP for the new tool features; the "mystery with puzzles" steps; HUB-13 ticket; a changelog per ticket; `followups.md` and `handoff.md`.

Not done yet (after the VN Studio PR is merged and the tools rebuilt): HUB-06 H2, the live checks of HUB-07, 08 and 13, HUB-10 phase 5 and HUB-11 phase 3. Every production waits for the user to play or read it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
