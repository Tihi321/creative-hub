# HUB-06 changelog

2026-10-23. H2 live run (`runs/the-lighthouse-that-kept-lists-vn.md`): Scriptorium adapted *The Lighthouse That Kept Lists* into a 6-chapter VN script (13,710 words, score 7.79, Claude as architect/writer/humanizer, deepseek reviewers, $0.17) with CG/INSERT/SFX/AMBIENCE lines inside the limits and `Aliases:` before `Voice:`; VN Studio imported 11 CGs, 11 inserts, 25 sounds, aliases on their characters; 99 assets (ComfyUI art, chiptune SFX/ambience), build 0 placeholders, lint clean (995 dialogue blocks). Hand edits: 3 CG `characters` (VNO-32). Blocked first by Scriptorium's retired fallback model (user fixed the config; SCP-26 to 28). Found: SCP-34 to 37, VNO-32 to 35. Open: the user plays it.

2026-10-22, branch `HUB-02-13_roadmap-tasks`. Tool work: Scriptorium SCP-16 (PR #10, merged) and VN Studio VNO-16 (branch `VNO-10-19_hub-roadmap`).

- H1 (commit 71ddd75): a hand-made book in the SCP-16 format (`runs/hub-06-media-lines/book/`) imports into VN Studio with every cue line (`CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, `END CG`) and every `Aliases:` sentence. Run log: `runs/hub-06-media-lines.md`.
- VNO-16: CG and insert images get their characters from the cue text, and the `Aliases:` sentence is taken out of the character's looks (H1 found it there).
- Skill and README (commit 170ee2e): the cue lines and the aliases.

Verified: the H1 import into VN Studio and the VNO-16 tests.
Not verified: H2, a real Scriptorium adaptation (`the-lighthouse-that-kept-lists` to a VN) on the merged builds. It runs after the VN Studio PR is merged.
