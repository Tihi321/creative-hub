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
| VN Studio project (linear) | `the-clockless-god-3` (imported, not yet generated) |
| VN Studio project (choices) | `the-clockless-god-2` (imported, not yet generated) |

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

## Checked

- what was looked at or played, by whom

## Left to do

-
