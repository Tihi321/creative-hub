# HUB-15 changelog

## 2026-10-23 evening: C1 and C3

- **C1 (VN adaptation):** `the-local-patch-2` from `the-local-patch`, published at round 2, score 7.36, 11,342 words, imported into VN Studio (preview). Verified: SCP-28, SCP-35, SCP-36, the SCP-37 target, and SCP-34 for bare weekdays. Found: SCP-38 to SCP-42 in Scriptorium's `ROADMAP.md`. Run log `runs/the-local-patch-2.md`.
- **C3 (puzzle mystery, run in a fork):** `the-trap-room-at-the-lanterna`, published at round 0, score 8.36, 4 chapters, 6,244 words, imported with the art and music plan (no images). Verified: SCP-30, SCP-31, SCP-33, VNO-26, VNO-29 (separate `claude -p` reader), VNO-30 (in the project data). SCP-32 not exercised. VNO-25 and VNO-31 partly fixed: VNO-36, VNO-37 (and VNO-38, the harmless `END CG` "dropped" warning) are in VN Studio's `ROADMAP.md`. Run log `runs/the-trap-room-at-the-lanterna.md`.
- The tool roadmap edits are uncommitted on each tool's `master`.
- Still open (then): C2 (screenplay), C4 (Flow and ComfyUI side by side), C5 (after the Gemini quota resets, about 09:00 on 2026-10-24), C6 (the user's verdicts).


## 2026-10-23 evening: C2

- **C2 (screenplay, SCP-29):** `the-local-patch-3` from `the-local-patch` as a `short-film`. Published at round 2 with score 7.09: 2 sequences, 9 scenes, 18 shots, runtime 120 s in [60, 180]. The SCENE places match the bible. SCP-29 verified: the writer prompts ask for seconds, not words. The length gate read `ok, seconds: 120` against a `target_words: 1200`. No length rewrite ran. Reviewer spend was $0.023. Run log `runs/the-local-patch-3.md`, screenplay `runs/the-local-patch-3/screenplay.json`.
- Notes (not filed, for the user to decide):
  - Round 1 scored 6.73 and was rejected, because `short-film` has `max_rounds: 1` like the other short formats. The worker reopened it with `reopen_book {mode: "rewrite"}`.
  - `book.md` still carries a word target (`target_words: 1200`) that nothing uses for screenplays.
- Still open: C4 (Flow and ComfyUI side by side), C5 (after the Gemini quota resets, about 09:00 on 2026-10-24), C6 (the user's verdicts).
