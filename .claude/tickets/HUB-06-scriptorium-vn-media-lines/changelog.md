# HUB-06 changelog

2026-10-22, branch `HUB-02-13_roadmap-tasks`. Tool work: Scriptorium SCP-16 (PR #10, merged) and VN Studio VNO-16 (branch `VNO-10-19_hub-roadmap`).

- H1 (commit 71ddd75): a hand-made book in the SCP-16 format (`runs/hub-06-media-lines/book/`) imports into VN Studio with every cue line (`CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, `END CG`) and every `Aliases:` sentence. Run log: `runs/hub-06-media-lines.md`.
- VNO-16: CG and insert images get their characters from the cue text, and the `Aliases:` sentence is taken out of the character's looks (H1 found it there).
- Skill and README (commit 170ee2e): the cue lines and the aliases.

Verified: the H1 import into VN Studio and the VNO-16 tests.
Not verified: H2, a real Scriptorium adaptation (`the-lighthouse-that-kept-lists` to a VN) on the merged builds. It runs after the VN Studio PR is merged.
