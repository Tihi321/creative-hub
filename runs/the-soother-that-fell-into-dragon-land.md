# The Soother That Fell Into Dragon Land

Started 2026-10-20.

## Brief

- Idea / theme: the existing Scriptorium book (published, round 2): Petra throws baby Pip's soother over the mountains into Dragon Land and has to trade for it back.
- Kind: choices (7 chapters, 3 endings: ch5, ch6, ch7) · children (6-9)
- Languages: English
- Art: pixel, drawn by hand in Pixel Studio, **no ComfyUI** (user's request) · Music: chiptune (NES) via Chiptune Studio · Voices: off

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | (not needed, book already published) |
| Scriptorium book | `the-soother-that-fell-into-dragon-land` |
| Book Translator project | |
| VN Studio project | `the-soother-that-fell-into-dragon-land` |

## Decisions

- Every VN Studio pixel mode (`pixelProvider: pixel-studio`, `provider: pixel-studio-draw`) starts from a ComfyUI render: backgrounds, sheets and sprite references all call `ctx.comfy.generate`. To keep ComfyUI out, every image asset is drawn by Claude with the pixel-studio MCP and set with `vno_asset_replace` (custom + locked) **before** the pipeline's generate step runs, so generate only makes the chiptune music.
- Pixel grid 240x135, scaled 8x to 1920x1080. Sprites use the same 8x density, bottom-aligned, with heights by character size (Petra ~72 px grid, Grumble ~120, Pip/Mango ~40).
- Theme `pixel-retro`. Music: 4 NES tracks.
- Model roles done by Claude (`client/claude-code`) for this project only: script-analyst, composer, stage-director, director, art-director. Art review off.

## Log

- 2026-10-20 `vno_import` gave project `the-soother-that-fell-into-dragon-land` (choice book, 7 chapters, 433 beats). Import warnings fixed with `vno_story_edit`:
  - added characters `pink_dragon`, `blue_dragon`, `splash`, `mama` (they spoke but were not in the bible);
  - added place `dragon_path` for ch02.s01, set ch03.s01 to `singing_dragons_chorus`;
  - ch5's ending text was the placeholder "an ending": now "happy: Petra trades a song for a sparkly stone, wins back the soother, and brings a new friend home".
- Assets: 10 backgrounds, 9 sheets, 27 sprites, cover, 4 music tracks.
- Cast beats added/changed so the speakers who had none appear on stage: ch03.s01.b014 (pink, nib, blue), new ch03.s01.b056 (pink, petra, blue), ch05.s01.b006/b014/b022/b029 (Splash), ch06.s03.b003 (3 max), new ch06.s03.b043 (Mama), b032 (Mama), new b044. That added `sprite_splash_neutral` (29 sprites).
- Art pipeline: `scripts/pxcanvas.py` (new hub helper) composes each image in Python and paints it into Pixel Studio as `draw_grid` tiles, then Pixel Studio exports the PNG (8x). Art scripts and exports in `runs/the-soother-that-fell-into-dragon-land/art/` (`STYLE.md` is the brief). Claude drew `bg_petra_s_house_{morning,evening}` and `sprite_petra_*` (6 expressions) as the style reference; 7 subagents drew the rest in parallel (a lock file serialises Pixel Studio).
- Music by Claude in Chiptune Studio (NES, strict, analyse clean), projects + ogg in `runs/.../music/`: music_01 "Petra's Garden" (C major 104), music_02 "Dragon Land" (F major 132), music_03 "The Golden Cave" (D minor 80), music_04 "Singing Hill" (G major 3/4 112). Set with `vno_asset_replace`; plan by hand: menu 01; ch1 01, ch2 02, ch3 04, ch4 03, ch5 02, ch6 01, ch7 01.
- VN Studio change: ticket VNO-07 committed on branch `VNO-07_hand-drawn-art` (22851d2, not pushed/merged): `art.provider: hand` (no ComfyUI for images, art plan skipped, sheets optional) and nearest-neighbour resizes for pixel builds; 567 tests, typecheck and lint pass. **Not live**: the build + restart of the running engine was blocked by the auto-mode permission check, so this production runs on the old engine (all images replaced before generate).
- Sprites drawn by the agents, checked by Claude from the PNGs: pip (pram), mama (thigh-up), mango (hovering), nib (on ledgers and a stool), grumble (head and chest, gold coin), pink_dragon / blue_dragon (on standing stones), splash (mid-bounce). 29 sprites + 9 sheets (= the neutral sprite) + the 2 house backgrounds set with `vno_asset_replace` (custom, locked).

- All 10 backgrounds and the cover set (the cover is 240x135 and becomes the main menu: Mango, Petra and a peeking Grumble, the soother over the green sky; script `art/cover.py` pastes the real sprite builds). 53/53 assets custom and locked.
- 2026-10-20 15:40 Pipeline run 2 from analyse. Claude answered the script-analyst (2 batches, 54 items: only expressions that have sprites, place/time kept so no background id changes; queue paused before the last batch to check that no asset was added), the composer (plan as set by hand), chapter 1 of the stage-director, and the director summary; a subagent answered stage chapters 2-7. Generate: "every asset already has a file" (no ComfyUI call). Build: 0 placeholders, 0 warnings. Lint clean, 381 dialogue blocks, 4 menus.
- The build writes lossy WebP (quality 88), which smears pixel art. Rebuilt with the global `imageFormat: png` (config/renpy.md) and set it back to `webp` right after; the game now has 38 PNG images. Code fix done as VNO-07 item 8 (c23bfb3, lossless WebP for pixel projects; 568 tests, typecheck and lint pass; not live until the engine is rebuilt).
- Project `models` cleared after the run.

## Checked

- Claude read every exported PNG (backgrounds, all sprite expressions of each character, cover) and the build/lint results. Stage cues by the subagent: 3 cast beats listed 4 characters and were cut to 3 (ch05.s03.b001 without Mango, ch06.s03.b003 without Mama, ch06.s03.b021 without Mama and Grumble).
- **Not checked yet:** how the sprites sit in the running game over the backgrounds and under the text box; the user has not played it.

## Left to do

- The user plays it (all three endings: ch5 mud puddles → stone, ch6 red boot, ch7 button then boot) and says how it plays; write the answer here.
- Merge VNO-07 (`VNO-07_hand-drawn-art`) after review, then `hub.ps1 build vn-studio` + restart (blocked in this session by the permission check), and set this project's `art.provider: hand`.
