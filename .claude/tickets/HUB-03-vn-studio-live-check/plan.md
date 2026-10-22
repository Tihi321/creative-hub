# HUB-03: VN Studio live check (VNO-08)

## Goal

Prove on the hub's running VN Studio that what VNO-08 added works in a real game the user plays: CGs, inserts, SFX, ambience, scene music, a CJK edition, an RTL edition and the translated game menus. No code change is planned. A failure becomes a new VNO item in `C:\projects\Personal\visual-novels-orchestrator\ROADMAP.md`.

## Background

- VNO-08 (merged, master 7ff8a2d): media cues and asset kinds, UI strings for 36 languages, a font per language and `vno_fonts_fetch`, RTL layout (`vno_rtl.rpy`), `turns` in `vno_get_task`, scheduler and import fixes. 717 tests pass, Ren'Py lint clean on 9 integration cases. Changelog: `visual-novels-orchestrator/.claude/tickets/VNO-08-roadmap-fixes/changelog.md`. How to use the tools: its `docs/mcp-guide.md` ("Pictures and sounds", "Languages").
- The hub's engine (`out/`) was built on 2026-10-20, before VNO-05 to VNO-08.
- The Ren'Py lint cannot check layout, so RTL and fonts need a look in the game.

## Decisions

- Inferred: use a small new test project made with `vno_create_project` (one chapter, two scenes, about 12 beats, two characters), so the check is quick and does not touch the played Clockless God projects. Slug `vno-media-test`.
- Inferred: images with ComfyUI (default provider); music and ambience with the music engine; the editions' text written by Claude with `vno_edition_set`.
- Made (2026-10-22): the SFX file comes from Chiptune Studio's `compose_sfx` (MDI-05), imported with `vno_asset_import`. HUB-13 (VNO-19) later lets VN Studio call it itself (`sound.sfxEngine: "chiptune"`).
- Made: which UI-string languages the user can check: The user reads Croatian; other languages are only checked to show up, not for wording.

## Steps

- [x] 1. `hub.ps1 start` (default set: ComfyUI, comfy-mcp, Pixel Studio, Chiptune Studio, VibeTTS, LM Studio), then `hub.ps1 build vn-studio`, `stop vn-studio`, `start vn-studio`, `/mcp` reconnect. `hub.ps1 check vn-studio` shows the new tool count (`vno_image_set`, `vno_sound_set`, `vno_fonts_fetch`, `vno_asset_import`, `vno_voice_import`, `vno_clear_queue` present).
- [x] 2. Seed migration: the engine log shows what `store/seedMigrations.ts` added to `~\VisualNovels`; the user's edits are unchanged.
  Result 2026-10-22: engine log: 0 seed files copied, 1 folder created (`fonts/`), 7 unedited seeded files updated at an earlier start, providers.md (user edits) kept.
- [x] 3. `vno_create_project` with a short English story: `images` with one full CG and one insert, `sounds` with one sfx and one ambience, a beat with `image`, a beat with `sfx`, a scene with `ambience` and `music`, a beat that hides the image (`null`).
  Result 2026-10-22: `vno-media-test` created: 1 chapter, 2 scenes, 13 beats, 2 characters, insert + full CG, sfx + ambience, scene music/ambience, hide beats (`null`).
- [x] 4. `vno_run_pipeline {slug, wait: true}` (or with `vno_wait`). If a project model uses the client provider, check one `vno_get_task`: `turns: "single"` has `system` + `user`, no `messages`.
  Result 2026-10-22: pipeline run 2 finished (voices off by default, left off; LM Studio did the model steps, `client` not used so the `turns` check was not applicable). `music_01` hung after a ComfyUI native crash; `vno_stop_now` + `vno_resume_all` recovered it.
- [x] 5. Import the SFX file with `vno_asset_import`. `vno_build` lists no placeholder for `cg_`, `sfx_`, `amb_`. `vno_lint` clean.
  Result 2026-10-22: sfx from Chiptune `compose_sfx` (door, nes, seed 7), imported as `sfx_door_creak`; `vno_build` ok, placeholders [], `vno_lint` ok, no messages.
- [x] 6. Editions: `vno_edition_set` for `ja` (CJK) and `ar` (RTL), and `hr` for the UI strings. `vno_fonts_fetch {script: "kana"}` for Japanese. Build and lint again; the build has no missing-font warning.
  Result 2026-10-22: ja, ar, hr set (`missing` empty); `vno_fonts_fetch kana` ok (`fonts/kana.otf`); rebuilt: no warnings (Arabic uses DejaVuSans), lint clean on en+ja+ar+hr.
- [ ] 7. The user plays it (`renpy` launch command in the build result): CG shows and hides, insert shows, SFX plays once, ambience loops under the scene and stops, music changes at the scene; Japanese text renders (no boxes); Arabic reads right to left with the name box, dialogue and navigation mirrored; Croatian menus are Croatian and read well.
- [x] 8. Log it in `runs/vno-media-test.md` (copy `runs/_template.md`). Mark the VNO-08 live checks done in `ROADMAP.md`; any problem goes to VN Studio's `ROADMAP.md`.
  Result 2026-10-22: `runs/vno-media-test.md` written. ROADMAP.md not yet touched: the VNO-08 live checks wait for the user's play (step 7).

## Acceptance

- Build and lint clean with all media assets present.
- The user played the English, Japanese and Arabic versions and saw each cue work.
- The user checked the Croatian menus.

## Not in scope

- Native-speaker review of the other 33 languages' UI strings (stays open in the hub roadmap until someone can read them).
- The Croatian Clockless God edition from HUB-02 can be built and played here too, as a bonus.
