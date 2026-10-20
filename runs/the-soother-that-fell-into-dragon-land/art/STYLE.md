# Art brief: The Soother That Fell Into Dragon Land (pixel visual novel, ages 6-9)

Every image is pixel art made in **Pixel Studio** (the user's app, MCP at http://127.0.0.1:7457/mcp). **No ComfyUI, no
other image generator, no Pillow.** The art is written as Python code with `scripts/pxcanvas.py` (in the creative-hub repo),
which paints the canvas into a Pixel Studio document as `draw_grid` tiles and exports the PNG through Pixel Studio.

## Files

- `C:\projects\Personal\creative-hub\scripts\pxcanvas.py`: `Canvas` (rect, ellipse, circle, polygon, line, hills,
  vgradient with ordered dither, dither_fill, speckle, replace, blit hand-written rows, paste, outline, flip) and `Studio`
  (`image(canvas, name, path, width, height)` for one picture, `sprite(name, frames, out_dir, scale)` for a sprite with one
  frame per expression). Both take a cross-process lock, so several scripts can run at once. Read it first.
- `common.py` in this folder: paths (`OUT`), `SCALE = 8`, `SPRITE_H = 120`, shared colours (`OUTLINE`, skin, blush, mouth),
  `eye5` (5x6 eyes: open, wide, lid, half, up, down, happy, closed, teary, with an optional lash), `brow5` (flat, up,
  raised, in/in-r angry, sad/sad-r), `run_sprite(name, build, expressions)`.
- Reference work, match it: `bg_petra_s_house.py` (background) and `sprite_petra.py` (character). Their exports are in
  `out/` (`bg_petra_s_house_morning.png`, `sprite_petra_neutral.png`, `sprite_petra_happy.png`, ...). Look at them.
- Write one script per asset group in this folder (`bg_<place>.py`, `sprite_<character>.py`), run it with
  `python <script>.py` from this folder, outputs go to `out/`.

## The look

- Palette: **Endesga 64** colours only (the list is in Pixel Studio's `endesga-64`; the reference scripts use its hex
  values). Bright, warm, friendly, cartoony, never scary. Hue-shifted shading: shadows cooler/purpler, highlights warmer.
- Dragon Land's sky is **green** (mint to soft green: `#d3fc7e`, `#99e65f`, `#5ac54f`, with dithered bands like the
  reference sky), with fluffy white clouds. Petra's world has a blue sky.
- Pixel density is fixed: **one art pixel = 8x8 screen pixels** everywhere. Backgrounds are 240x135 exported at
  1920x1080. Sprites are drawn on a canvas **120 pixels tall** (exported at scale 8 = 960 px tall), width as needed
  (40-120), transparent background, figure bottom-aligned (Ren'Py stands the image on the bottom of the screen).
- The text box covers the bottom ~35 art rows of a sprite canvas: every face must sit in the top 70 rows. Small creatures
  (Mango, Nib, Pip) are drawn in the upper part of the canvas: hovering on wings, on a stool, in a pram, so their faces are
  above the text box.
- Characters: 1 px `OUTLINE` (`#391f21`) outside (`c.outline(OUTLINE)` at the end), big expressive eyes (`eye5`), clear
  brows and mouths. Expressions are the only difference between the frames of one character (same pose, same pixels
  elsewhere), so they swap cleanly.
- Backgrounds: no characters in them, no text except the signpost word asked for. Leave the middle and lower-middle readable
  (sprites stand there): put busy detail at the sides and back. Ground line around y 95-110.

## Rules

- Do not call the pixel-studio MCP drawing tools directly and do not use `render_preview` to check your work: other agents
  draw in Pixel Studio at the same time and the "current document" changes under you. Draw only through your script
  (it holds the lock), and check your work by **reading the exported PNG** with the Read tool. Iterate until it looks good:
  clean shapes, readable at a glance, consistent with the reference.
- Do not touch other agents' files, VN Studio, or anything outside this folder.
- Report: the files written, and one line on what each shows.
