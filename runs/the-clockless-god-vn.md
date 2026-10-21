# The Clockless God: visual novel adaptations

Started 2026-10-21.

## Brief

- Source: *The Clockless God* (`the-clockless-god`, published at 7.73), adapted with the new script writer (SCP-11).
- The user asked for two versions:
  - **with choices**: `choice-visual-novel`, with meaningful detective choices, the book ending as the canon true ending, and 2-3 short alternative endings;
  - **linear**: `visual-novel`, faithful.
- Who writes: Claude does the editor-in-chief, architect and writer work through the client provider, with subagents per book. The reviewers and the humanizer run on Scriptorium models.
- Art, music and voices: a later production in VN Studio.

## Ids

| Tool | Id |
|---|---|
| Scriptorium book (choices) | `the-clockless-god-2` (published, 7.57) |
| Scriptorium book (linear) | `the-clockless-god-3` (published, 7.5) |
| VN Studio project (linear) | `the-clockless-god-3` (built, lint clean, 0 placeholders) |
| VN Studio project (choices) | `the-clockless-god-2` (built, lint clean, 0 placeholders) |

## Log

- 2026-10-21 Scriptorium was restarted on the SCP-12 build (SCP-10/11/12) with `-Window`. The migrations added the humanizer role and agent, the article formats and the Newspaper topics. MCP reports 39 tools.
- 2026-10-21 `adapt_book {book: the-clockless-god, format: choice-visual-novel, notes, models}` made `the-clockless-god-2`; then, at the user's request, `format: visual-novel` made `the-clockless-god-3`. Both are at the pitch stage.

- 2026-10-21 Writing: one Claude subagent per book, each handing over to a fresh agent after 6 tasks. Notes for each successor are in `.claude/temp/live/the-clockless-god-{2,3}-notes.md`.
- **Linear (`the-clockless-god-3`): published at 7.5** after 2 rounds: enjoyment 8, genre fit 8, structure 8, originality 9, prose 7, continuity 6, mechanics 6.
  - 9 chapters, each adapting 2 source chapters, about 2,000-2,500 words each (over the 1,667 target; never flagged).
  - The REMITTERE decode is on screen in ch7; the HUIT hook and "Get your coat." are in ch9.
  - The humanizer, round 2 on the SCP-13 build: ch3 was kept humanized. The guards refused ch1, ch5 and ch7 (length more than 10% off, or a "new name"). One refusal was a **false positive**: "Hz" counted as a new name.
  - Before SCP-13 the humanizer had chopped some chapters into fragments (ch6, ch8). The rewrites restored them.
  - ch2 has 13 speech lines without an expression. That is valid script grammar (the expression is optional).
- 2026-10-21 VN Studio started. `vno_import {source: the-clockless-god-3}` worked: 9 chapters, 21 characters, 22 places, linear, en.
  - Warnings: the speaker VOICE (the hooded Vaulmont in ch3) has no sprite, which is right for a hidden voice; **24 scenes have a place that matches no bible place**.
  - Before generating art: line up the scene places with the bible's places (`vno_scene_update`), or improve the adapter so it reuses bible place names (ROADMAP).


- 2026-10-21 **Choices (`the-clockless-god-2`): published at 7.57** after 2 rewrite rounds: enjoyment 8, genre fit 9, prose 8, originality 9, continuity 6, mechanics 6, structure 6. It has 16 chapters (about 26k words) and 6 writer agents worked on it. The choice map is in `.claude/temp/live/the-clockless-god-2-notes.md`:
  - 3 choice points: ch4 (lamps), ch7 (the tea), ch9 (Pichon);
  - the true ending is ch13;
  - the alternative endings are ch14 "Caught by the Brotherhood" (the face is seen, then lost on the bridge), ch15 "Dec Stopped" and ch16 "The Miracle at None" (the bank calls in the atelier's loan).
- From the 2nd round on, the humanizer ran on `deepseek/deepseek-flash` with the SCP-13 prompts (switched at the user's request; see the ROADMAP).
- **Defect fixed by hand after publication:** `chapters/ch-09.md` ended with 3 paragraphs of leaked task instructions ("Write the improved chapter. ..."). A writer agent's answer file still held them, and Scriptorium accepted the submission.
  - They were removed from `ch-09.md`, from `out/the-clockless-god-2.epub` (chapter-09.xhtml patched, `mimetype` kept first) and from the reader (`node out/engine/index.js rebuild-reader`).
  - The originals are in `.claude/temp/scp-backup/`.
- Still open in the published text:
  - ch12, the "Already on R" detail;
  - ch13, quai des Orfèvres against rue du Bastion;
  - some speaker lines without an expression (valid; VN Studio uses neutral);
  - one em dash in the blurb.
- 2026-10-21 `vno_import {source: the-clockless-god-2}` worked: choice, 16 chapters, 21 characters, 24 places. Warnings: speakers RADIO, VOICE and HOODS have no sprite (on purpose); **58 scenes have a place that matches no bible place** (line them up before the art).

- 2026-10-21 Scriptorium was reloaded on the latest SCP-13 build (5c93340). All repos are clean; Book Translator BTT-10 was merged by the user.
- 2026-10-21 **Bible places lined up** (`.claude/temp/vn/places.py`, one `vno_story_edit` per project):
  - **Linear:** 24 scenes repointed and 9 new places with full looks: rue des Gravilliers, the old railway tunnel, the room at Le Balancier, the track to Combe-Noire, the cheese cellar, the holding cell, a serious restaurant, the Debt Clock chamber and the Clockmaker's Cell.
  - **Choices:** 58 scenes repointed and 8 new places, which add a school courtyard and the valley road at night; the crypt and the Debt Clock chamber already existed.
  - Both projects now have **0 unmatched scenes**. The only warnings left are the voice-only speakers VOICE, RADIO and HOODS, which have no sprite on purpose.
- 2026-10-21 User's choices for the VN production: **illustrated art** (ComfyUI qwen-image 2.1; BiRefNet cut-outs), **ACE-Step music** (5 tracks), **voices off**.
  - The VN Studio text roles of both projects (script-analyst, composer, stage-director) are set to `deepseek/deepseek-flash` by `vno_update_settings {models}`. Strata is down, and the local LM Studio model would compete with ComfyUI.
  - LM Studio's models were unloaded (`lms unload --all`); they reload on demand. ComfyUI and comfy-mcp were started; the GPU has about 108 GB free.
- 2026-10-21 `vno_run_pipeline {slug: the-clockless-god-3}` (run 1). The linear VN goes first; its characters and the places they share are to be reused for the choice VN.

- 2026-10-21 **Art direction changed** after the first sheet came out gritty watercolour, muddy and torn.
  - The user chose **clean hand-drawn**, like the classic 1990s point-and-click adventures: `art.stylePrompt` on both projects.
  - 49 planned prompts were restyled by `vno_asset_set` (`.claude/temp/vn/restyle.py`).
  - The 7 old-style sheets were regenerated through comfy-mcp and set with `vno_asset_replace` before any sprite was made (`gen_sheets.py`). VN Studio runs jobs oldest first, so a regen job would have run after the sprites.
  - La Taupe's prompt now says "young woman"; her first sheet read as male.
- 2026-10-21 Scriptorium was stopped and LM Studio's models unloaded, to free memory. ComfyUI ran qwen-image 2.1 at about 1-2 minutes per image on the AMD 8060S (about 108 GB of GPU memory).
- 2026-10-21 **Linear VN built.** 132 jobs, 0 failed:
  - assets: 14 sheets, 60 backgrounds, 67 sprites, cover, 5 ACE-Step tracks;
  - staging, build, and Ren'Py lint ok (1,221 dialogue blocks, about 17k words), 0 placeholders.
  - Fixed by hand (comfy-mcp, then `vno_asset_replace` and `vno_asset_lock`):
    - the cover: Inès had brown curly hair in a bun, and the cover was portrait, which the menu crops. It is now a **landscape** key art of Dec and Inès at Roux's clock window under the eclipse;
    - `bg_pont_de_sully_day` had a stray figure.
  - Rebuilt; lint clean.
  - The build only notes VOICE (the hidden speaker, no sprite, on purpose).
- 2026-10-21 Choice VN:
  - The alias characters `the_bald_man` (60 cast lines), `the_young_man_in_grey` (6) and `declan_hartley` (1) were remapped to Kessler, Fabien and Dec, and the aliases removed (`vno_story_edit`).
  - Reused from the linear VN (`copy_assets.py`): 13 sheets, 61 sprites, the cover, 5 music tracks, and 28 backgrounds mapped by place.
  - Only the choice VN's own art is generated: Vey, Lassalle, Zoltán, the old lady in the fur hat, Madame Ferré, a few extra expressions, Pichon's office, the priory, the school courtyard.
  - Its analysis ran on strata, with an LM Studio fallback (gemma), not on the DeepSeek models set for the project: check `vno_update_settings {models}` against the run.

- 2026-10-21 **Choice VN built.** 64 jobs, 0 failed. Lint ok: 1,257 dialogue blocks, about 19k words, **12 choice menus**. 0 placeholders. The build notes RADIO, VOICE and HOODS as ad hoc characters with no sprite, on purpose.
- Spot check: the old lady in the fur hat is good. Brother Anselm Vey came out as a young man in a waistcoat, which showed the real fault, a **wrong cast**:
  - In ch4 s5 (the chapel), the names Inès reads in the ledger had become cast beats, putting Kessler, Roux, Vey and then Lassalle on screen.
  - In ch14 s3, "the silver-haired man" (Vaulmont) was cast as Zoltán, with 4 people on screen.
  - Fixed: the ledger beats keep Inès, Dec and La Taupe on screen; the extra cast beats were removed; ch14 now shows Dec, Vaulmont and Inès. Vey, Lassalle and Zoltán no longer appear (their assets are orphaned). Rebuilt; lint clean.
  - The linear VN was checked too: those characters are never on screen there.
- 2026-10-21 The user played the **linear VN: "clockless god works"**.

Play:
- Linear: `& "C:\projects\Localenpyenpy-8.5.3-sdkenpy.exe" "$env:USERPROFILE\VisualNovels\projects	he-clockless-god-3\game"`
- Choices: `& "C:\projects\Localenpyenpy-8.5.3-sdkenpy.exe" "$env:USERPROFILE\VisualNovels\projects	he-clockless-god-2\game"`

## Checked

- what was looked at or played, by whom

## Left to do

- The user plays the **choice VN** (all 4 endings) and says how it plays.
- Optional: Croatian VN editions (the Croatian book exists; a VN edition needs the script translated, see skill step 2), Android builds, voices.

-
