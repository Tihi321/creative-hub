# HUB-10 changelog

2026-10-22. Tool work: VN Studio VNO-12 to VNO-15 (branch `VNO-10-19_hub-roadmap`) and Scriptorium SCP-18 (PR #10, merged).

- Phase 1, VNO-12: the puzzle proof of concept (a 3x3 Murdle generator and solver, the Ren'Py grid screen, `scripts/puzzle-poc.ts`).
- Phase 2, VNO-13: puzzle beats, the `vno_puzzle_*` tools, the flavour read-back check and the puzzle build. The core's shape is in `puzzle-core.md`.
- Phase 3, VNO-14: more kinds (a 4x4 Murdle with a motive, Knights and Knaves, testimony, logic grids).
- Phase 4: Scriptorium SCP-18 (format `mystery-puzzle-visual-novel`, `bible/puzzles.md`, the planting check); VN Studio VNO-15 (the script lines read at import); hub: the "Mystery with puzzles" steps in the make-visual-novel skill.

Verified: the VN Studio tests, the Ren'Py self-tests of the PoC, and the Scriptorium tests.
Not verified: the user playing the PoC (`npx tsx scripts/puzzle-poc.ts --play` in VN Studio); phase 5, the first puzzle VN. It runs after the VN Studio PR is merged.
