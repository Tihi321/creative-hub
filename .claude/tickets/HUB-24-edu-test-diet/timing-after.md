# EGS-46 timing, after the diet (EGS-40..46 merged)

Machine: this Windows box, vitest 5 JSON reporter, loops expanded, `node node_modules/vitest/vitest.mjs run`. EGS-45 e2e work in parallel, so not an idle machine.

## Summary
| run | files | tests (real) | failed | skipped | wall |
|---|---|---|---|---|---|
| `yarn test` at EGS-40 (before the diet) | 102 | 1928 | 1 | 0 | 103 s |
| `yarn test` after EGS-44 (start of EGS-46) | 90 | 988 | 0 | 0 | 49 s |
| `yarn test` after EGS-46 | 90 | 501 | 0 | 0 | 36.5 s |

globalSetup (out/player + out/live): skipped when the bundles are newer than the sources (about 9 ms warm; 2.1-3.1 s cold).

## Files whose test count changed in EGS-46 (after EGS-44 -> after EGS-46)
| file | tests before | tests after |
|---|---|---|
| de-verbs.test.ts | 101 | 6 |
| lint.test.ts | 111 | 18 |
| de-grammar.test.ts | 91 | 7 |
| edu-match.test.ts | 37 | 13 |
| mindmaze-maze.test.ts | 28 | 8 |
| edu-course.test.ts | 30 | 12 |
| design-tokens.test.ts | 14 | 2 |
| player-i18n.test.ts | 13 | 1 |
| edu-build.test.ts | 16 | 5 |
| edu-reading.test.ts | 15 | 4 |
| player-classroom.test.ts | 16 | 5 |
| conjugation.test.ts | 19 | 9 |
| edu-srs.test.ts | 13 | 3 |
| edu-assemble.test.ts | 13 | 5 |
| edu-mcp.test.ts | 20 | 13 |
| puzzles.test.ts | 19 | 12 |
| edu-authoring.test.ts | 18 | 12 |
| player-detective-model.test.ts | 8 | 2 |
| player-progress.test.ts | 11 | 5 |
| main-files.test.ts | 8 | 3 |
| scoring.test.ts | 11 | 6 |
| player-round.test.ts | 15 | 11 |
| translit.test.ts | 6 | 2 |
| live-room.test.ts | 8 | 5 |
| player-mindmaze-walk.test.ts | 9 | 6 |
| player-reader-logic.test.ts | 9 | 6 |
| themes-load.test.ts | 5 | 2 |
| voice-allocate.test.ts | 8 | 5 |
| player-rpg-logic.test.ts | 12 | 10 |
| studio-files.test.ts | 2 | 1 |

## Slowest files now (seconds in the vitest worker, includes import)
| file | tests | s |
|---|---|---|
| media-pipeline.test.ts | 8 | 33.8 |
| pipeline-run.test.ts | 4 | 26.3 |
| pipeline.test.ts | 9 | 24.6 |
| pipeline-reading.test.ts | 3 | 18.1 |
| edu-editions.test.ts | 12 | 17.3 |
| scheduler.test.ts | 12 | 7.9 |
| models.test.ts | 12 | 7.0 |
| art-tools.test.ts | 4 | 6.0 |
| edu-mcp.test.ts | 13 | 5.4 |
| mcp-http.test.ts | 4 | 5.4 |
| seed-migrations.test.ts | 9 | 5.4 |
| detective-case.test.ts | 9 | 5.4 |

Longest single test now: 10488 ms (the client loop: with model client/claude-code in the brief every role). No test sets a timeout above the 15 s default of vitest.config.ts.
