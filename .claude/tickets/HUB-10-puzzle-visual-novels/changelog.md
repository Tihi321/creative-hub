# HUB-10 changelog

2026-10-23. Phase 5 production (`runs/the-winter-garden-clock.md`): *The Winter Garden Clock*, a Hartley and Varga case in the format `mystery-puzzle-visual-novel` (4 chapters, 6,303 words, score 7.36, $0.06): Murdle `winter_garden` and Knights and Knaves `belfry`, both proved and read back by a separate reader (`textChecked: true`); 66 Flow images (switched from ComfyUI by the user's choice), lint clean (344 dialogue blocks). No testimony puzzle (the generator repeated itself: VNO-25). Found: VNO-25, 26, 29, 30, 31, 28; SCP-30 to 33. Open: the user plays it (solve both, a wrong answer first).

2026-10-22. Tool work: VN Studio VNO-12 to VNO-15 (branch `VNO-10-19_hub-roadmap`) and Scriptorium SCP-18 (PR #10, merged).

- Phase 1, VNO-12: the puzzle proof of concept (a 3x3 Murdle generator and solver, the Ren'Py grid screen, `scripts/puzzle-poc.ts`).
- Phase 2, VNO-13: puzzle beats, the `vno_puzzle_*` tools, the flavour read-back check and the puzzle build. The core's shape is in `puzzle-core.md`.
- Phase 3, VNO-14: more kinds (a 4x4 Murdle with a motive, Knights and Knaves, testimony, logic grids).
- Phase 4: Scriptorium SCP-18 (format `mystery-puzzle-visual-novel`, `bible/puzzles.md`, the planting check); VN Studio VNO-15 (the script lines read at import); hub: the "Mystery with puzzles" steps in the make-visual-novel skill.

Verified: the VN Studio tests, the Ren'Py self-tests of the PoC, and the Scriptorium tests.
Not verified: the user playing the PoC (`npx tsx scripts/puzzle-poc.ts --play` in VN Studio); phase 5, the first puzzle VN. It runs after the VN Studio PR is merged.
