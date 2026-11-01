# HUB-24 changelog

## 2026-11-01 EGS-40..46: edu-game-studio test diet, all merged to master (303ee0f)

Outcome: `yarn test` 1928 -> 501 tests, 103 s -> 37 s, 0 skipped, no Chromium. `yarn test:e2e` 118 -> 25 tests, 1095 s -> 361 s (6 m 02).

Repo C:\projects\Personal\edu-game-studio, test-only changes (no src/ change) except config/docs.
- EGS-40 (PR #45, d2dd418): `test` / `test:e2e` / `test:all`; vitest.e2e.config.ts; guard test e2e-split; `requireChromium()` fails instead of skipping (proved with an empty PLAYWRIGHT_BROWSERS_PATH); globalSetup kept, skips when out/ is fresh; Chromium blocks moved to *.e2e.test.ts; AGENTS.md, README, ROADMAP rows.
- EGS-41 (PR #47, 70e7941): pipeline-run restart test made deterministic with a gate and `reopen()` in tests/helpers.ts (~4 s, 30/30 under load twice, fails when resume is broken); pipeline 14->9, pipeline-run 6->4, art/music/voice merged into media-pipeline (8).
- EGS-42 (PR #48, 59d8fd6): lint.test.ts one case per code with enumeration guard (111 cases, ~105 codes); edu-mcp 31->19 with a 50-tool contract; mcp-http 4, mcp-config 2, edu-cli 4.
- EGS-43 (PR #46, 55f0480): engine/schema/puzzle/player-logic trims; edu-puzzles merged into puzzles; EGS-48 and EGS-51 regression tests kept.
- EGS-44 (PR #49, 8c6cf87): live, clients, infra trims; sleeps replaced by awaited events; scheduler and stt long timeouts dropped.
- EGS-46 (PR #50, cc7eb85): German unit files trimmed, fast suite to 501, timeouts <= 15 s, timing-after.md.
- EGS-45 (direct merge into master, 303ee0f; commit f72f730): e2e trimmed; each shell keeps one perfect run; art/music/voice e2e merged into media-pipeline.e2e. Conflicts in 3 pipeline test files resolved by keeping master's (EGS-46) versions.

Deviations: user changed the process mid-run: no PRs after #50, EGS-45 merged locally and master pushed. Per-ticket worktrees under edu-wt; all removed after merge, with node_modules junctions.

Verification: final master 303ee0f: `test` 501/501 in 38 s; `test:e2e` 25/25 in 361 s (retry 1 configured). Typecheck/lint clean per worker on each branch. Not run: `yarn build`, final-master typecheck/lint by me.

Known gaps: the Scriptorium pipeline wiring test was dropped in EGS-41 with no replacement; lint has 111 cases, not ~60 (about 105 codes); MAZE_* cases stay in mindmaze-maze.test.ts; fast tests still pass `run()` ceilings of 90-150 s in a few places (edu-editions, pipeline-reading, media-pipeline), but the global testTimeout is 15 s and they pass; `waitFor` in tests/helpers.ts may still poll.
