# HUB-13: VN Studio makes sound effects and ambience with Chiptune Studio

Opened 2026-10-22 during the hub roadmap run (umbrella plan `.claude/tickets/HUB-02-13-roadmap-tasks/plan.md`, section "HUB-13"). Origin: the only open item of midi-generator's `ROADMAP.md`: VN Studio did not call Chiptune Studio's `compose_sfx` (MDI-05), so every `sfx_` sound needed an imported file.

## Goal

`sound.sfxEngine: "chiptune"` makes `sfx_` sounds and `sound.ambienceEngine: "chiptune"` makes `amb_` ambience loops with `compose_sfx`, so a VN needs no hand-imported sound files.

## Decisions

- Made: both engines stay explicit, also for pixel/chiptune books (a default would change existing projects and call a studio that may not run).
- Made: no new setting for ambience; `ambienceEngine` already existed.

## Steps

- [x] VN Studio `VNO-19` (branch `VNO-10-19_hub-roadmap`, commit 98e81d0): engine value, `composeSfx` client call, sound-name picker with a `blip` / `drone` fallback and a warning, `vno_update_settings {sound}`, docs, 10 tests (752 pass).
- [x] midi-generator `MDI-06_vn-sfx-done`: its roadmap item closed (docs only).
- [x] Hub: the skill says how to set the engines (make-visual-novel step 3).
- [x] Live check (2026-10-23, `hub08-13-autostart`): a small project with `sfxEngine` and `ambienceEngine` set to `chiptune`; the build has no `sfx_`/`amb_` placeholder; the user hears them in the game (open: the user has not listened yet).

## Acceptance

- A VN with SFX and ambience builds with no imported sound file, and the user has heard them.
