# HUB-24 edu-game-studio test diet: plan

Source: `research.md` (same folder), spot-checked against edu-game-studio master 893d382, and the user's `test-discipline` skill (one test per behaviour a caller relies on, one regression test per fixed bug, table-driven over near-identical cases, one e2e happy path per feature, no sleeps, slow tests marked separately).

Work lands in the edu repo (`C:\projects\Personal\edu-game-studio`), one branch per EGS ticket named in that repo's style (`EGS-40_test-split`). This hub ticket only holds the plan.

## Scope
- Cut the edu repo from ~1900 effective tests (111 files, 1447 literal `it(`) to a default `yarn test` of at most ~500 tests with no Chromium, and a separate `yarn test:e2e` of at most ~45 tests.
- Add the `test` / `test:e2e` split, fix the flaky pipeline-run restart test, make e2e fail (not skip) without a browser.
- Update `AGENTS.md` (line 10: "yarn typecheck, yarn lint and yarn test") and `README.md` (line 67 table) with the new commands and the rule "whoever changes a shell runs `yarn test:e2e`".
- Per the skill, every deleted test is listed in the ticket report with the criterion it used to cover.

## Out of scope
- Any change to product code under `src/` (except a test seam for the gate in the pipeline-run fix, only if unavoidable; then say so).
- New features, new CI. Checked: the edu repo has no `.github/`; no hub script, `services.json`, README or ROADMAP calls `yarn test`/`vitest` (grep of `scripts/`, `.github`, `services.json`, `README.md`, `ROADMAP.md` in the hub is empty). So nothing outside the edu repo depends on the command, and EGS-20 (packaging, "CI") is the only future consumer: note in its row that CI runs `test` and, separately, `test:e2e`.
- Other tools' test suites.
- Trimming German files before HUB-22 lands.

## Step 0: measure (EGS-40, first action)
1. After HUB-22's pending merges (EGS-36 #35, EGS-38 #30, EGS-34) are on master, run once: `yarn vitest run --reporter=json --outputFile=.claude/temp/timing.json` on the current config (run it with the machine otherwise idle; the research could not, the cache was empty).
2. From the JSON produce `.claude/temp/timing.md`: per file, tests (real count, loops expanded), wall seconds, sorted by seconds. Also record `globalSetup` build time of `out/player`.
3. Recount the real totals and write them into the EGS-40 report as the "before" numbers. If a file's measured cost disagrees with the "Cost" guess below (H/M/L), the measurement wins; adjust the verdict, not the target.
4. Re-run the same command at the end (EGS-46) as the "after" numbers.

## Files and modules: verdicts
Counts are literal `it(` (loops make real counts higher). "e2e" = moved to `tests/*.e2e.test.ts`, run only by `test:e2e`. Verdicts for files in A-H come from research.md; all trims are "trim to N" meaning the end state has at most N cases, chosen by the skill's rule (boundaries plus one typical). German-touching files are in the last table.

### A. Bot / Playwright (all e2e; trim to one `perfect` run per shell plus one keyboard/axe)
| file | now | verdict | reason |
|---|---|---|---|
| bot.e2e | 5x+1 | trim to 4: 1 fixture x (perfect, keyboard+axe), 2nd fixture perfect, "not a build" exit-code case | modes `wrong`/`random` re-walk the same screens; logic covered by player-round and player-*-logic |
| bot-rpg.e2e | 1+loop | trim to 1 perfect, phone viewport merged in | |
| bot-detective.e2e | 8 | trim to 1 (perfect + axe, one CASE) | |
| bot-mindmaze.e2e | ~5x | trim to 2 (perfect, keyboard+axe) | |
| bot-roleplay.e2e | 5x | trim to 2 | |
| bot-encyclopedia.e2e | ~12+ | trim to 3 (explorer perfect+axe, reader perfect+axe) | most expensive file (11 timeouts) |
| bot-conjugation.e2e | 4 | trim to 1 perfect | German: edit after HUB-22 |
| classroom.e2e | 2 | trim to 1 | |
| live-quiz.e2e | 1 | keep (the single live-quiz end to end) | |
| android-mobile.e2e | 2 | trim to 1 | |
| audio-shells.e2e | 2 | trim to 1 | |
| player-shell-picker.e2e | 3 | trim to 1 | |
| speaking.e2e | 10 | trim to 2 (record/replay, permission denied) | player-speaking.test covers logic |
Result ~25 cases. Each shell keeps exactly one `perfect` bot run (the net's item 1).

### B. Pipeline
| file | now | verdict | reason |
|---|---|---|---|
| pipeline.test | 14 | trim to 8 (happy path, failure, retry, ...) | core net |
| pipeline-run.test | 7 | trim to 3 (restart-resume FIXED, retry after failure, restart-from-stage) + 1 client-loop; the "refuses what it cannot run" test (`:74`) moves into edu-mcp; the last test (`:234`, Chromium playtest) moves to `pipeline.e2e.test.ts` | |
| art-pipeline, music-pipeline, voice-pipeline (15+17+11) | 43 | merge into `media-pipeline.test.ts`, ~8 cases (happy path, provider down, placeholder when comfy is down, ids stable, composer unusable, credit opt-in); their Chromium blocks (music `:514`, art, voice) become one `media-pipeline.e2e.test.ts` case or are deleted if bot e2e already plays a media course | they share `makePipelineEnv` and walk near-identical runs; delete the MCP-guide string test (music `:386-392`, greps doc text) |
| edu-playtest | ? | measure; keep 1 fast case, Chromium case to e2e | uses `skipIf` |

### C. Engine / schema / lint / match
| file(s) | now | verdict | reason |
|---|---|---|---|
| edu-course, course-model, edu-build, edu-assemble, edu-editions | 33x+5+15+13+12 | keep schema/validate and build; each invalid class once; trim edu-course/course-model/authoring to ~40 combined | core net 2 |
| edu-authoring | 32 | merge into the ~40 above | many one-field-per-test |
| edu-lint, detective-lint, encyclopedia-lint, mindmaze-lint, roleplay-lint, rpg-lint, edu-checkers | 121 | merge into table-driven `lint.test.ts`: exactly one case per lint code (list the codes from the guide; a script asserts every code in `src/` appears once); ~60 | core net 3; before dropping a case run `git log -S` (see rule below) |
| edu-match | 21 | keep | core net 5 |
| translit | 14 | trim to 6 | |
| edu-srs, scoring | 13, 11 | keep | |
| edu-adaptive | 10 | trim to 5 | |
| puzzles + edu-puzzles | 25+15 | merge, ~15 | |
| mindmaze-maze | 30 | trim to 8 (generator invariants) | |
| detective-case | 16x | trim to 6 | |
| design-tokens | 22 (25 loops) | trim to 2 (palette contrast, all themes load) | snapshots of static data |
| themes-load, seed-files, main-files, studio-files | 8,3,8,2 | delete if they only assert file existence (read each first) | existence checks; typecheck/build catch missing files |
| seed-migrations | 9 | keep | real migrations |
| seed-refresh | 7 | trim to 3 | |
| languages | 15 | trim to 5 | |

### D. Player logic (cheap; count only)
player-round 15, progress 11, shell-kit 15, audio 14, feedback 10, speaking 13, classroom 16, detective-model 8, encyclopedia-logic 28, reader-logic 10, roleplay-logic 24, rpg-logic 26, mindmaze-walk 11 (~200). Verdict: keep player-round and progress; trim each `*-logic` / `*-walk` file to 8-10 cases with one full walk per shell (this is the fast playthrough net now that bots are cut); audio, feedback, shell-kit, speaking to ~3 each. Target ~90.

### E. MCP / CLI
edu-mcp 18, mcp-http 12, mcp-config 4, classroom-mcp 7, live-mcp 4, ui-mcp 2, edu-cli 11. Verdict: edu-mcp is the contract file: tool list, schema, one call per tool, one refusal; fold classroom-mcp, live-mcp, ui-mcp into it; mcp-http trim to 4 (auth, session, call, bad request; real listen); mcp-config 2; edu-cli 4. ~60 to ~30. Contract: a test asserts the registered tool-name list equals the documented list, so a tool cannot be added or removed unnoticed, plus one call per tool (the net's item 6).

### F. Live quiz
live-room 19 to ~8 (pure state); live-server 20 to 4 (join, answer, scoreboard, disconnect; replace `setTimeout` waits by awaiting the event). ~45 to ~12.

### G. Provider, plan and generate clients
voice-allocate 19 to ~8 (keep the quota rule: 10 Gemini requests/day, Croatian first, English falls to VibeTTS), voice-catalog 10, voice-generate 19, voice-plan 17; art-plan 20, art-tools 8, assets-generate 24 to 8, assets-import 5, assets-postprocess 10; music-generate 24 to 6, music-plan 17, chip-plan 4; comfy-client 33 to 8, comfy-custom 11, comfy-tts-engines 16 to 4, studios-clients 15, studios-flow-client 9, studios-generate 5, studio-commands 10, studio-lib 15, flow-generate 10, stt 11 (60 s timeout; drop it), vision 5, models 51 (real http server, 1147 lines) to 12. Rule per kind: one plan + one generate happy path + one failure; the remaining files each to at most 4. ~370 to ~110.

### H. Infra
autostart 31 to 6 (replace real child processes and sleeps with a fake spawner); scheduler 35 to 12 (12 sleeps to fake timers, drop the 20 s timeout); engine-lock 5 to 3; roles-config 13 to 5; custom-providers 12 to 4; clientsearch 7 to 3; research 28 to 8; factbase 10 to 4; fact-check 6 to 3; scriptorium 6 to 2; android 12 to 4; ui-course + ui-store 16 to 6. ~200 to ~70.

### I. German (HUB-22) files: planned last, after EGS-34/36/38 are on master
| file | verdict |
|---|---|
| conjugation 19, de-grammar 15 (13 loops), de-verbs 12 (11 loops) | trim to ~5 each, table-driven: one regular, one irregular/separable, one B2 form (passiv-prat, connector word order), the boundary of tolerant matching. Keep any case whose name or `git log -S` shows a bug fix |
| bot-conjugation.e2e, bot fixtures de-b2-reading | one perfect run each (already in A) |
| any new German tests from EGS-34/36/38 | review under the same budget: one test per behaviour; merge into the files above |
| editions (EGS-32) | already in C (edu-editions) |

## Tasks (tickets in the edu repo; ids: highest in ROADMAP is EGS-37, EGS-36/38/34 are in flight and EGS-39 is reserved by the user, so use EGS-40 onward; the worker confirms the ids are still free before the first commit)

### EGS-40 test split, timing and the e2e guard (first; contract for the others)
- Inputs: master after HUB-22 merges.
- Does: Step 0 timing; `vitest.config.ts` gets `exclude: ['**/*.e2e.test.ts']`; new `vitest.e2e.config.ts` (`include tests/**/*.e2e.test.ts`, `fileParallelism` capped at 2, `retry: 1`, long timeouts local to this config, `globalSetup` = player bundle); package.json: `"test": "vitest run"`, `"test:e2e": "vitest run -c vitest.e2e.config.ts"`, `"test:all": "yarn test && yarn test:e2e"`; AGENTS.md and README updated.
- Contract (others rely on it): any file named `*.e2e.test.ts` never runs in `yarn test`; any other `*.test.ts` never launches Chromium. A tiny guard test (in `test`) fails if a non-e2e test file imports `playwright` or `bot-helpers`.
- globalSetup: decide with data. Run `yarn test` with the player-bundle `globalSetup` removed; if tests fail for lack of `out/player`, keep the setup but make it skip when `out/player` is newer than `src/player` (stat check). Report which.
- E2E guard: replace every `describe.skipIf(!!unavailable)` and the `console.warn SKIPPED` (e.g. `bot.e2e.test.ts:32-33,80`, plus the other `unavailable` users listed by grep) with a shared `requireChromium()` in `bot-helpers.ts` that throws in a `beforeAll` with "run yarn playwright install chromium". Done when `test:e2e` on a machine without Chromium exits non-zero (prove by pointing `PLAYWRIGHT_BROWSERS_PATH` at an empty folder).
- Moves (no trimming yet): the Chromium blocks of pipeline-run (`:234`), art/music/voice pipelines and edu-playtest into `tests/*.e2e.test.ts`.
- Output: `.claude/temp/timing.md` (before), the config, a list of moved tests.

### EGS-41 pipeline-run restart fix (deterministic gate), then pipeline trims
- Input: EGS-40 merged.
- Fix `tests/pipeline-run.test.ts:12-44` (cause per research, reading only, not reproduced: stop lands after `curriculum:all` is done while the next job is in flight; hand-copied `Engine` config at `:21-30`; exact `author.count` assertions). Make it deterministic: the mock model for the stage after curriculum blocks on a gate promise; the test waits until that call has started, calls `engine.stop()`, then releases the gate. Build the second engine from a factory exported by `makePipelineEnv` (no hand-copied config). Assert the contract, not the counts: steps `done` before the stop keep their job ids and are not run again (`plan_brief` and `curriculum` author counts stay 1 across the restart), and the run publishes. No `waitFor` poll with long timeouts; target under 5 s.
- Acceptance: the test passes 30 times in a row (`vitest run --repeat`-style loop) under CPU load (run two copies in parallel); it fails if the resume logic is broken (temporarily make resume redo curriculum and see it fail; record it in the report).
- Also in this ticket: trim pipeline.test to ~8, pipeline-run to 3+1, merge art/music/voice into `media-pipeline.test.ts` (~8).

### EGS-42 lint and MCP contract consolidation
- Merge shell lints into `lint.test.ts` (one case per code, plus a guard that enumerates the codes in `src/` and fails if one has no case). Fold classroom-mcp, live-mcp, ui-mcp and the `:74` refusal test into edu-mcp, with the tool-list contract; trim mcp-http, mcp-config, edu-cli.
- Before deleting a lint edge case: see the bug rule below.

### EGS-43 engine, schema, player-logic and puzzle trims
- Sections C (minus German) and D. Merge puzzles + edu-puzzles; delete the snapshot files listed; per-shell logic files down to the walk plus round/progress.
- Output: one `walk` test per non-German shell still exists in the fast suite (name them in the report).

### EGS-44 clients, live quiz and infra trims
- Sections E-live, F, G, H. Replace sleeps with fake timers or awaited events (autostart, scheduler, live-server, clientsearch, voice-generate, research); no `setTimeout`-based waits left in `tests/` except in the e2e files. Drop `stt`'s 60 s timeout.

### EGS-45 e2e trims (A)
- Trim each bot file as the table says; keep `live-quiz.e2e`. Output: the per-shell perfect-run list and the measured e2e wall time.

### EGS-46 German files and final recount (last, after EGS-34/36/38 merged)
- Section I, then the "after" timing run, the acceptance table below filled in with numbers, and the ROADMAP rows for EGS-40..46 moved to Done.

Dependencies: 40 first; 41-45 can run in parallel on separate branches after 40 (they touch different files: 41 pipeline files, 42 lint+mcp, 43 core+player, 44 clients+infra, 45 bot e2e); 46 last. Merge order: 40, 41, then the rest, then 46, to keep rebases small.

## Rule: bug-fix edge cases (applies to every delete or trim)
Before removing a case that is not an obvious duplicate, run `git log -S"<distinctive string of the case>" --oneline -- tests/<file>` (and `git blame` on its lines). If the introducing commit message names a bug, fix, regression or a review finding, the case stays (or is merged into the table as one row) and is listed in the report under "kept: regression for ...". Deleted cases go in a table in the ticket report: file, case, why redundant (the criterion and the layer that still covers it).

## Acceptance criteria (measured with the JSON reporter, before and after)
1. `yarn test`: at most ~500 tests (real, loops expanded), no Chromium launched, wall time at most 2 min on this machine (target 60-90 s; if Step 0 shows the unit tests alone exceed that, find the slow files and fix them before trimming further). `globalSetup` cost reported.
2. `yarn test:e2e`: at most ~45 tests, wall time at most 10 min (budget to confirm, see questions).
3. Every shell (quiz, rpg, detective, mindmaze, roleplay, encyclopedia, conjugation) has one bot `perfect` run in e2e and one logic `walk` test in the fast suite; listed in the final report.
4. `lint.test.ts` has exactly one case per lint code, enforced by the enumeration guard.
5. Every MCP tool has a contract case in edu-mcp; the tool-name list is asserted.
6. The restart test passes 30 consecutive runs under load and is under 5 s.
7. `test:e2e` without Chromium fails with a clear message (not skip); `yarn test` has no skipped tests (`grep skipIf tests/` only in e2e files).
8. No `sleep`/`setTimeout` waits and no test timeout above 15 s in the fast suite.
9. `yarn typecheck`, `yarn lint`, `yarn build` pass; AGENTS.md and README show the new commands.
10. The report lists tests removed and the criterion or bug each remaining one covers (test-discipline's report rule).

## Order
HUB-22 merges first (EGS-36 #35, EGS-38 #30, EGS-34) -> EGS-40 (Step 0 timing, split, guard) -> EGS-41..45 -> EGS-46 (German, recount). If HUB-22 stalls, EGS-40..45 may start on master but must not touch the Section I files, and EGS-40's timing is rerun at EGS-46.

## Risks
- Default `test` no longer catches shell regressions: mitigated by the `walk` tests and the AGENTS.md rule.
- Hand-reading ~110 files is large; workers should work from the timing table, slowest and most redundant first, and stop a file once it meets its target.
- Counts in research.md are literal declarations and file-level; real numbers come from Step 0.

## Open questions
1. E2E time budget: is about 10 minutes acceptable, or should it be shorter (for example 5 minutes, which means dropping the keyboard/axe runs)?
2. Should `test:e2e` run automatically before a PR/merge (a hook or a roadmap rule), or only when a shell changes?
3. EGS ids: the plan uses EGS-40..46 because EGS-39 is reserved; confirm no other ticket claims them.
4. Is `retry: 1` on e2e acceptable (it can hide a flaky bot), or should e2e fail on first failure?
5. May `src/` get a small test seam (engine factory export) for the gate in EGS-41 if `makePipelineEnv` cannot provide it?
