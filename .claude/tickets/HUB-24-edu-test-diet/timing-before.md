# EGS-40 timing, before the diet (master ace4bb6 + the EGS-40 split)

Machine: this Windows box, other agents' processes also running (not idle). Real test counts, loops expanded, from vitest's JSON reporter.

## Summary
| run | files | tests (real) | failed | wall |
|---|---|---|---|---|
| `yarn test` (fast, e2e excluded) | 102 | 1928 | 1 | 103 s (1 m 43) |
| `yarn test:e2e` (2 workers, retry 1) | 18 | 118 | 0 | 1095 s (18 m 15) |

Whole suite before the split, as one `vitest run` (first attempt, not reliable): 7 m 36 s, Chromium bots in parallel, several workers died with
"JavaScript heap out of memory" and 51 tests failed (OOM, "spawn UNKNOWN"), so its counts (1955 total) undercount. Real total before the diet: 2045 tests (1927 fast + 118 e2e; the split adds 1 guard test, so 2046 now).

## globalSetup (tests/setup/player-bundle.ts: out/player + out/live)
- Build cost: 2.1 to 3.1 s (cold, `out/` removed; measured by calling the setup alone).
- Experiment: `yarn test` with the globalSetup removed and `out/` deleted: 1928 tests, 72 FAILED in 12 files (among them art-pipeline, music-pipeline, voice-pipeline, pipeline, pipeline-run, pipeline-reading, edu-editions, art-tools, live-server, live-mcp: "player bundle not found" / out/live/live.js ENOENT), wall 1 m 30. So the setup is needed.
- Decision: KEEP it, and skip it when out/player and out/live are newer than src/player, src/live-client, src/shared, src/design, themes, the two vite configs, package.json and yarn.lock (a warm run now costs about 9 ms instead of about 2.5 s).

## Fast suite: slowest files (`yarn test`)
| file | tests | failed | file s |
|---|---|---|---|
| pipeline-run.test.ts | 6 | 1 | 99.7 |
| music-pipeline.test.ts | 15 | 0 | 70.3 |
| art-pipeline.test.ts | 14 | 0 | 70.2 |
| pipeline.test.ts | 14 | 0 | 47.5 |
| voice-pipeline.test.ts | 10 | 0 | 43.8 |
| scheduler.test.ts | 35 | 0 | 30.7 |
| edu-editions.test.ts | 12 | 0 | 29.3 |
| models.test.ts | 51 | 0 | 24.5 |
| pipeline-reading.test.ts | 3 | 0 | 23.6 |
| detective-case.test.ts | 19 | 0 | 18.9 |
| mcp-http.test.ts | 12 | 0 | 14.4 |
| seed-migrations.test.ts | 9 | 0 | 11.4 |
| puzzles.test.ts | 25 | 0 | 11.3 |
| custom-providers.test.ts | 12 | 0 | 11.2 |
| research.test.ts | 28 | 0 | 11.0 |
| art-tools.test.ts | 8 | 0 | 11.0 |
| course-model.test.ts | 5 | 0 | 8.3 |
| art-plan.test.ts | 20 | 0 | 7.0 |
| voice-generate.test.ts | 19 | 0 | 6.7 |
| mcp-config.test.ts | 4 | 0 | 4.9 |
| android.test.ts | 12 | 0 | 4.6 |
| assets-generate.test.ts | 24 | 0 | 4.1 |
| edu-authoring.test.ts | 32 | 0 | 3.7 |
| edu-lint.test.ts | 50 | 0 | 3.6 |
| edu-playtest.test.ts | 8 | 0 | 3.6 |

Note: pipeline-run.test.ts "a restarted engine on the same folder finishes the run" fails every time (3 of 3 here, and on a pristine master checkout too) after a 30 s waitFor; it is the flaky test EGS-41 fixes. The 99 s of that file is mostly this wait.

## E2E files (`yarn test:e2e`, all 118 passed)
| file | tests | failed | file s |
|---|---|---|---|
| bot-detective.e2e.test.ts | 8 | 0 | 350.8 |
| bot.e2e.test.ts | 16 | 0 | 294.3 |
| bot-mindmaze.e2e.test.ts | 15 | 0 | 282.8 |
| bot-rpg.e2e.test.ts | 17 | 0 | 270.6 |
| bot-encyclopedia.e2e.test.ts | 21 | 0 | 242.0 |
| bot-roleplay.e2e.test.ts | 5 | 0 | 155.8 |
| music-pipeline.e2e.test.ts | 2 | 0 | 100.2 |
| audio-shells.e2e.test.ts | 7 | 0 | 95.8 |
| voice-pipeline.e2e.test.ts | 1 | 0 | 91.6 |
| art-pipeline.e2e.test.ts | 1 | 0 | 90.1 |
| pipeline-run.e2e.test.ts | 1 | 0 | 42.6 |
| edu-playtest.e2e.test.ts | 1 | 0 | 38.0 |
| speaking.e2e.test.ts | 10 | 0 | 30.4 |
| bot-conjugation.e2e.test.ts | 4 | 0 | 18.7 |
| classroom.e2e.test.ts | 3 | 0 | 14.2 |
| player-shell-picker.e2e.test.ts | 3 | 0 | 11.3 |
| live-quiz.e2e.test.ts | 1 | 0 | 3.8 |
| android-mobile.e2e.test.ts | 2 | 0 | 3.1 |

File seconds overlap (parallel workers); the wall time is the figure above.

## All fast files
| file | tests | file s |
|---|---|---|
| pipeline-run.test.ts | 6 | 99.7 |
| music-pipeline.test.ts | 15 | 70.3 |
| art-pipeline.test.ts | 14 | 70.2 |
| pipeline.test.ts | 14 | 47.5 |
| voice-pipeline.test.ts | 10 | 43.8 |
| scheduler.test.ts | 35 | 30.7 |
| edu-editions.test.ts | 12 | 29.3 |
| models.test.ts | 51 | 24.5 |
| pipeline-reading.test.ts | 3 | 23.6 |
| detective-case.test.ts | 19 | 18.9 |
| mcp-http.test.ts | 12 | 14.4 |
| seed-migrations.test.ts | 9 | 11.4 |
| puzzles.test.ts | 25 | 11.3 |
| custom-providers.test.ts | 12 | 11.2 |
| research.test.ts | 28 | 11.0 |
| art-tools.test.ts | 8 | 11.0 |
| course-model.test.ts | 5 | 8.3 |
| art-plan.test.ts | 20 | 7.0 |
| voice-generate.test.ts | 19 | 6.7 |
| mcp-config.test.ts | 4 | 4.9 |
| android.test.ts | 12 | 4.6 |
| assets-generate.test.ts | 24 | 4.1 |
| edu-authoring.test.ts | 32 | 3.7 |
| edu-lint.test.ts | 50 | 3.6 |
| edu-playtest.test.ts | 8 | 3.6 |
| live-server.test.ts | 20 | 3.3 |
| roles-config.test.ts | 13 | 3.3 |
| scriptorium.test.ts | 6 | 2.7 |
| clientsearch.test.ts | 7 | 2.5 |
| encyclopedia-lint.test.ts | 16 | 2.5 |
| fact-check.test.ts | 6 | 2.4 |
| player-rpg-logic.test.ts | 28 | 1.9 |
| edu-mcp.test.ts | 18 | 1.8 |
| edu-cli.test.ts | 11 | 1.7 |
| scoring.test.ts | 11 | 1.7 |
| flow-generate.test.ts | 10 | 1.7 |
| studios-flow-client.test.ts | 9 | 1.4 |
| comfy-tts-engines.test.ts | 16 | 1.4 |
| factbase.test.ts | 10 | 1.3 |
| edu-build.test.ts | 16 | 1.3 |
| studio-commands.test.ts | 10 | 1.1 |
| stt.test.ts | 11 | 0.9 |
| autostart.test.ts | 31 | 0.9 |
| studios-generate.test.ts | 5 | 0.9 |
| edu-course.test.ts | 41 | 0.7 |
| mindmaze-maze.test.ts | 35 | 0.7 |
| roleplay-lint.test.ts | 6 | 0.7 |
| detective-lint.test.ts | 9 | 0.5 |
| live-mcp.test.ts | 4 | 0.5 |
| music-generate.test.ts | 24 | 0.5 |
| edu-assemble.test.ts | 13 | 0.5 |
| comfy-client.test.ts | 33 | 0.4 |
| seed-files.test.ts | 3 | 0.4 |
| rpg-lint.test.ts | 19 | 0.4 |
| classroom-mcp.test.ts | 7 | 0.4 |
| mindmaze-lint.test.ts | 4 | 0.4 |
| studios-clients.test.ts | 15 | 0.4 |
| edu-puzzles.test.ts | 15 | 0.3 |
| player-round.test.ts | 15 | 0.3 |
| player-mindmaze-walk.test.ts | 11 | 0.3 |
| engine-lock.test.ts | 5 | 0.3 |
| edu-reading.test.ts | 15 | 0.3 |
| studio-lib.test.ts | 15 | 0.3 |
| assets-postprocess.test.ts | 10 | 0.3 |
| player-reader-logic.test.ts | 12 | 0.2 |
| player-encyclopedia-logic.test.ts | 30 | 0.2 |
| live-room.test.ts | 19 | 0.2 |
| voice-allocate.test.ts | 19 | 0.2 |
| player-progress.test.ts | 11 | 0.2 |
| assets-import.test.ts | 5 | 0.2 |
| player-feedback.test.ts | 10 | 0.2 |
| seed-refresh.test.ts | 7 | 0.2 |
| de-verbs.test.ts | 101 | 0.1 |
| player-shell-kit.test.ts | 15 | 0.1 |
| player-audio.test.ts | 14 | 0.1 |
| comfy-custom.test.ts | 11 | 0.1 |
| player-speaking.test.ts | 13 | 0.1 |
| languages.test.ts | 15 | 0.1 |
| themes-load.test.ts | 8 | 0.1 |
| edu-checkers.test.ts | 32 | 0.1 |
| design-tokens.test.ts | 273 | 0.1 |
| conjugation.test.ts | 19 | 0.1 |
| music-plan.test.ts | 17 | 0.0 |
| player-detective-model.test.ts | 8 | 0.0 |
| e2e-split.test.ts | 1 | 0.0 |
| vision.test.ts | 5 | 0.0 |
| main-files.test.ts | 8 | 0.0 |
| edu-srs.test.ts | 13 | 0.0 |
| voice-plan.test.ts | 23 | 0.0 |
| edu-match.test.ts | 37 | 0.0 |
| player-roleplay-logic.test.ts | 24 | 0.0 |
| player-classroom.test.ts | 16 | 0.0 |
| de-grammar.test.ts | 91 | 0.0 |
| voice-catalog.test.ts | 10 | 0.0 |
| translit.test.ts | 14 | 0.0 |
| edu-adaptive.test.ts | 10 | 0.0 |
| chip-plan.test.ts | 4 | 0.0 |
| ui-course.test.ts | 10 | 0.0 |
| ui-store.test.ts | 6 | 0.0 |
| player-i18n.test.ts | 13 | 0.0 |
| studio-files.test.ts | 2 | 0.0 |
| ui-mcp.test.ts | 2 | 0.0 |
