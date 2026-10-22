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
- Open (ask the user): where the SFX file comes from. Options: a free sound the user picks, a short sound made with comfy-mcp's audio, or `sound.sfxEngine` if one fits. Recommendation: one free CC0 file, imported with `vno_asset_import`.
- Open: which UI-string languages the user can check. The user reads Croatian; other languages are only checked to show up, not for wording.

## Steps

- [ ] 1. `hub.ps1 start` (default set: ComfyUI, comfy-mcp, Pixel Studio, Chiptune Studio, VibeTTS, LM Studio), then `hub.ps1 build vn-studio`, `stop vn-studio`, `start vn-studio`, `/mcp` reconnect. `hub.ps1 check vn-studio` shows the new tool count (`vno_image_set`, `vno_sound_set`, `vno_fonts_fetch`, `vno_asset_import`, `vno_voice_import`, `vno_clear_queue` present).
- [ ] 2. Seed migration: the engine log shows what `store/seedMigrations.ts` added to `~\VisualNovels`; the user's edits are unchanged.
- [ ] 3. `vno_create_project` with a short English story: `images` with one full CG and one insert, `sounds` with one sfx and one ambience, a beat with `image`, a beat with `sfx`, a scene with `ambience` and `music`, a beat that hides the image (`null`).
- [ ] 4. `vno_run_pipeline {slug, wait: true}` (or with `vno_wait`). If a project model uses the client provider, check one `vno_get_task`: `turns: "single"` has `system` + `user`, no `messages`.
- [ ] 5. Import the SFX file with `vno_asset_import`. `vno_build` lists no placeholder for `cg_`, `sfx_`, `amb_`. `vno_lint` clean.
- [ ] 6. Editions: `vno_edition_set` for `ja` (CJK) and `ar` (RTL), and `hr` for the UI strings. `vno_fonts_fetch {script: "kana"}` for Japanese. Build and lint again; the build has no missing-font warning.
- [ ] 7. The user plays it (`renpy` launch command in the build result): CG shows and hides, insert shows, SFX plays once, ambience loops under the scene and stops, music changes at the scene; Japanese text renders (no boxes); Arabic reads right to left with the name box, dialogue and navigation mirrored; Croatian menus are Croatian and read well.
- [ ] 8. Log it in `runs/vno-media-test.md` (copy `runs/_template.md`). Mark the VNO-08 live checks done in `ROADMAP.md`; any problem goes to VN Studio's `ROADMAP.md`.

## Acceptance

- Build and lint clean with all media assets present.
- The user played the English, Japanese and Arabic versions and saw each cue work.
- The user checked the Croatian menus.

## Not in scope

- Native-speaker review of the other 33 languages' UI strings (stays open in the hub roadmap until someone can read them).
- The Croatian Clockless God edition from HUB-02 can be built and played here too, as a bonus.
