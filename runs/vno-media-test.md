# The Lantern Door (vno-media-test)

Started 2026-10-22. HUB-03 live check of VN Studio VNO-08 (media cues, fonts, RTL, translated menus). Plan: `.claude/tickets/HUB-03-vn-studio-live-check/plan.md`.

## Brief

- Idea / theme: two children find a key and a lit lighthouse; a test story that uses every VNO-08 cue.
- Kind: linear · children's mystery, short
- Languages: en (primary) + ja, ar, hr editions (text written by Claude)
- Art: illustrated (ComfyUI qwen-image-2.1) · Music: comfy (ace-step-v1-instrumental, 3 tracks) · Voices: off (project default)

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | none (written straight into VN Studio) |
| Scriptorium book | none |
| Book Translator project | none (editions written with `vno_edition_set`) |
| VN Studio project | `vno-media-test` (data `C:\Users\Infplane\VisualNovels\projects\vno-media-test`) |

Story ids: chapter 1; scenes `ch01.s01` (lighthouse_door, dusk, music_02, ambience `waves`), `ch01.s02` (lamp_room, night, music_03, ambience stopped); 13 beats (`ch01.s01.b001`-`b007`, `ch01.s02.b001`-`b006`).
Cues: insert `old_key` (asset `cg_old_key`) shown at `ch01.s01.b004`, hidden (`null`) at `b005`; sfx `door_creak` (`sfx_door_creak`) at `ch01.s01.b006`; ambience `waves` (`amb_waves`) starts with scene 1, `ambience: null` on scene 2; full CG `lamp_glow` (`cg_lamp_glow`) shown at `ch01.s02.b002`, hidden at `b005`.
Chiptune songId `song_mvjq3j608i7ts`, `compose_sfx {kind: sfx, sound: door, chip: nes, seed: 7}` -> `.claude/temp/hub03/sfx_door.ogg` (1.10 s), imported with `vno_asset_import` as `sfx_door_creak` (locked, custom).

## Log

- 2026-10-22 17:50 Step 2: engine log `logs/vn-studio.out.log`: at this start "seed: copied 0 file(s), kept 32 existing, created 1 folder(s)" and "update available for 1 seeded file(s) you edited (yours are kept): config/providers.md". An earlier start of the same log shows "updated 7 seeded file(s) you had not changed: config/languages.md, studios.md, voice.md, prompts/art-director/plan_art.md, composer/plan_music.md, script-analyst/resolve_uncertain.md, stage-director/stage_chapter.md". The user's edited providers.md was kept. New folder = `fonts/`.
- 17:55 sfx made with Chiptune `compose_sfx`; 17:56 created project, imported sfx, started pipeline run 2 (LM Studio did the model steps; nothing used `client`, so the `turns` check of step 4 was not applicable).
- 17:57-18:05 `vno_edition_set` ja, ar, hr (11 beats each, `missing` empty). `vno_fonts_fetch {script: "kana"}` -> `fonts/kana.otf` (Noto Sans CJK JP, 16.5 MB, OFL).
- generate ran about 50 min after the pipeline started at 15:56 UTC (19 assets; ComfyUI one at a time). ComfyUI crashed natively while `music_01` was running; the job stayed "running" forever with ComfyUI idle. `vno_stop_now` + `vno_resume_all` made it run again and it finished, then the pipeline went on (stage, build, lint).
- 18:49 `vno_build`: ok, 0 placeholders, translated arabic/croatian/japanese, no warnings. `vno_lint`: ok, no messages (11 dialogue blocks in each of the 4 languages).

## Checked

- Generated files (read as images): `cg_lamp_glow` (both children, lamp, dark sea; fine), `cg_old_key` (key with tag on a table; opaque square, no transparent background, sits in the middle as an insert), `sheet_mara` (fine), sprite `tom thinking` (cut out cleanly), background `lighthouse_door_dusk` (a stout white tower with the arched door; not tall like a lighthouse, but acceptable).
- Game script read: `ch01.rpy` has `play music` at the chapter and `if_changed` at scene 2, `play ambience "audio/amb_waves.mp3"` at scene 1 and `stop ambience fadeout 1.5` at scene 2, `show cg old_key as vn_cg at vn_insert` / `hide vn_cg`, `play sound "audio/sfx_door_creak.ogg"`, `show cg lamp_glow as vn_cg` / `hide vn_cg`. `vno_media.rpy` registers the `ambience` channel (loop). `vno_fonts.rpy`: Japanese -> `fonts/lang/kana.otf`, Arabic -> DejaVuSans.ttf. `vno_rtl.rpy`: `config.rtl = True` with Arabic-only mirroring.
- NOT checked: anything that needs the game running (layout, hearing, Japanese glyphs, Arabic mirroring, Croatian menus). That is step 7, for the user.

## Play (PowerShell)

English:
```
& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\vno-media-test\game"
```
The Ren'Py project folder is `...\vno-media-test\game` (the game files are in its `game\game`). A window titled "The Lantern Door" means it started.
Other languages: the same game. Main menu -> Preferences -> the Language column -> Japanese / Arabic / Croatian (the editions' names are shown in their own language), then Start. To test the Croatian menus look at the main menu, Preferences, Load/Save and History after switching.

What to look for:
- English: scene 1 has the sea ambience from the first line (loops); at Tom's "Look at the tag" the key insert appears in the middle and goes at Mara's "Then that is us."; at "The door groaned" the creak plays once; scene 2: the ambience fades out, the music changes, the lamp CG covers the scene at "At the top, the great lens" and goes at "The light moved on".
- Japanese: the text must be letters, not boxes (Noto Sans CJK JP), menus in Japanese.
- Arabic: the text reads right to left; the name box, dialogue and navigation buttons are mirrored; the other languages keep the normal layout.
- Croatian: menus in Croatian and natural; story text is mine (also to be judged).

## Left to do

- Step 7: the user plays English, Japanese, Arabic and checks the Croatian menus; write the answer here.
- Mark the VNO-08 live checks in `ROADMAP.md` only after that.
