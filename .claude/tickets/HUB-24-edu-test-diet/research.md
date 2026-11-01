# HUB-24 edu-game-studio test diet: research

## Question
Which of the ~1900 tests in edu-game-studio (111 `*.test.ts` files plus helpers) should be kept, merged, trimmed or deleted, what is the minimal true safety net, and what should the fast `test` vs `test:e2e` split be?

## Answer
- Base: master at 893d382. HUB-22 (German courses) is merging concurrently, so counts will drift; re-run the file inventory before cutting. **Confirmed**: 111 test files; a grep of literal `it(`/`test(` gives 1447 declarations. The real total is ~1900 (brief) because `for` loops and `.each` tables multiply cases (bot e2e loops over fixtures/cases; design-tokens, de-grammar, de-verbs, detective-case, edu-course use loops).
- **No timing data**: `node_modules/.vite/vitest/*/results.json` is empty and I did not run the suite. All "cost" below is **inferred** from code (Playwright, 300 s timeouts, spawned processes, sleeps), not measured. Step 0 of the plan: one `vitest run --reporter=json --outputFile=...` to get real per-file durations.
- Slowness is concentrated: ~18 files launch Chromium (the 11 `*.e2e.test.ts` files, 4 pipeline files with an "autoplay bot" block, edu-playtest, pipeline-run last test). Moving those out fixes most wall time; trimming the unit tests mostly fixes count.
- Proposed target: default `yarn test` <= ~550 tests, no Chromium, ~1-2 min (inferred); `yarn test:e2e` ~45 tests, Chromium, ~10 min (inferred). Total ~600 vs ~1900 (-68%).

## Path through the code (config, confirmed)
- `vitest.config.ts`: `include: tests/**/*.test.ts`, `globalSetup tests/setup/player-bundle.ts` (builds out/player once; every run pays it), `testTimeout 15000`, `EDU_AUTOSTART=0`. `package.json` has only `"test": "vitest run"`: no e2e split.
- E2E files are already named `*.e2e.test.ts` (13 files incl. the bot ones), so a split is an `exclude` or a second config. Helpers: `tests/bot-helpers.ts`, `tests/pipeline-helpers.ts`.
- Bot files use `describe.skipIf(!!unavailable)` and `it.concurrent` with `{ timeout: 300_000 }`; each case spawns `scripts/play.mjs` via `execFile` (`tests/bot.e2e.test.ts:55`, 280 s limit) with `--mode perfect|wrong|random`, `--keyboard`, `--axe`, `--viewport`. `bot.e2e` and `bot-detective` loop a `describe` over fixtures/CASES (`bot.e2e.test.ts:80-82`, `bot-detective.e2e.test.ts:37-38`).

## Inventory and verdicts
Counts = literal `it(` count; `x` = multiplied by loops, real count higher. Cost: H = Chromium / 300 s, M = real HTTP, spawn or sleeps, L = in-memory.

### A. Bot / Playwright e2e (all go to `test:e2e`, then trim)
| file | n | cost | verdict |
|---|---|---|---|
| bot.e2e.test.ts (quiz, loop over FIXTURES x 5 modes, +1 error case) | 5x+1 | H | keep; per fixture run perfect + one keyboard/axe; drop `random` and `wrong` duplicates -> 1 fixture x 3 modes, second fixture perfect only; keep the "not a build" exit-code case (cheap) |
| bot-rpg.e2e | 1 (+loop) | H | keep perfect; merge phone viewport check into it |
| bot-detective.e2e (2 CASES x 4) | 8 | H | keep perfect on 1 case; drop random, wrong; merge `--axe` into perfect |
| bot-mindmaze.e2e | ~5x | H | keep perfect + keyboard/axe; drop random, one of the two wrong runs |
| bot-roleplay.e2e | 5x | H | perfect + keyboard/axe |
| bot-encyclopedia.e2e (CASES x 6, plus reader describe x 6) | ~12+ | H | most expensive (11 timeouts); perfect + axe for explorer and for reader; drop phone/random/wrong repeats |
| bot-conjugation.e2e | 4 | H | keep perfect only |
| classroom.e2e | 2 | H | keep 1 |
| live-quiz.e2e | 1 (8 steps, 21 timeouts) | H | keep as the single live-quiz end-to-end |
| android-mobile.e2e | 2 | H | keep 1 |
| audio-shells.e2e | 2 | H | keep 1 |
| player-shell-picker.e2e | 3 | H | trim to 1 |
| speaking.e2e | 10 | H | trim to 2 (record/replay, permission denied); player-speaking.test.ts covers the logic |
Reason: the per-shell mode matrix (perfect/wrong/random/keyboard/axe/phone) re-walks the same screens, and each mode costs a Chromium launch plus a full playthrough. "wrong" and "random" are covered by the player logic unit tests (player-round, player-*-logic). Target: ~120 cases -> ~25.

### B. Pipeline (engine happy path + resume)
| file | n | cost | verdict |
|---|---|---|---|
| pipeline.test.ts | 14 | L/M | keep happy path + failure/retry, trim to ~8 |
| pipeline-run.test.ts | 7 | M; last test runs Chromium (`:234-235`, 200 s playtest) | keep 3: resume after restart, retry after failure, restart-from-stage; move the bot/playtest test to e2e; the client-loop test (`:101`) keep as 1; fold the "refuses what it cannot run" test (`:74`) into edu-mcp |
| art-pipeline.test.ts | 15 | M + Chromium block | trim to 3 (happy path, placeholder when comfy is down, ids stable); real-bot block to e2e or delete |
| music-pipeline.test.ts (592 lines) | 17 | M + Chromium block (`:514`) | trim to 4 (happy, composer unusable, provider down, credit opt-in); delete the MCP-guide string test (`:386-392`, greps doc text) |
| voice-pipeline.test.ts (480 lines) | 11 | M + Chromium | trim to 3 |
Merge art/music/voice pipeline files into one `media-pipeline.test.ts` (~8 cases): they share the `makePipelineEnv` scaffolding and walk near-identical full runs.

### C. Engine / schema / lint / match (core net, mostly keep, trim)
- edu-course 33x, course-model 5, edu-authoring 32, edu-build 15, edu-assemble 13, edu-editions 12: keep schema/validate and build (valid builds; each invalid class rejected once); authoring/course trim to ~40 combined (many one-field-per-test).
- edu-lint 40, detective-lint 8, encyclopedia-lint 15, mindmaze-lint 3, roleplay-lint 6, rpg-lint 17, edu-checkers 32: **one case per lint error code** is the contract. Merge shell lints into one table-driven `lint.test.ts`. ~120 -> ~60.
- edu-match 21, translit 14: matching rules are a stated net; keep edu-match, trim translit to ~6.
- edu-srs 13, scoring 11, edu-adaptive 10: keep SRS and scoring, adaptive to 5. puzzles 25 + edu-puzzles 15: merge, ~15. mindmaze-maze 30 -> 8 (generator invariants). detective-case 16x -> 6.
- conjugation 19, de-grammar 15 (13 loops), de-verbs 12 (11 loops): language tables with near-identical cases / data snapshots; trim to ~5 each. HUB-22 changes these concurrently, so cut them last.
- design-tokens 22 (25 loops), themes-load 8, seed-files 3, main-files 8, studio-files 2: snapshots of static data. Delete design-tokens except 2 (palette contrast, all themes load); delete seed-files, main-files, studio-files if they only check file existence (not read in detail, **inferred**). Keep seed-migrations 9 (real migrations), seed-refresh 7 trim to 3.
- languages 15 -> 5.

### D. Player logic (cheap, count only)
player-round 15, progress 11, feedback 10, shell-kit 15, audio 14, speaking 13 (16k/48k tables), classroom 16, detective-model 8, encyclopedia-logic 28, reader-logic 10, roleplay-logic 24, rpg-logic 26, mindmaze-walk 11 = ~200. Keep round, progress and one "walk" per shell (this is the shell-playthrough net once most bots are cut): ~8-10 per shell logic file; audio/feedback/shell-kit/speaking to ~3 each (implementation detail). Target ~90.

### E. MCP
edu-mcp 18, mcp-http 12, mcp-config 4, classroom-mcp 7, live-mcp 4, ui-mcp 2, edu-cli 11. One test per tool contract. Keep edu-mcp as the contract file (tool list + schema + one call per tool + one refusal); fold classroom-mcp, live-mcp, ui-mcp into it (13 -> ~6); mcp-http keep 4 (real server listen: auth, session, call, bad request); mcp-config 2; edu-cli 4. ~60 -> ~30.

### F. Live quiz
live-server 20 (real http, `setTimeout`), live-room 19. Keep live-room (pure state) ~8; live-server trim to 4 (join, answer, scoreboard, disconnect); live-quiz e2e covers the rest. ~45 -> ~14.

### G. Voice / art / music / provider clients (mock HTTP, mostly wire tests)
voice-allocate 19, voice-catalog 10, voice-generate 19 (1 sleep), voice-plan 17; art-plan 20, art-tools 8, assets-generate 24, assets-import 5, assets-postprocess 10; music-generate 24, music-plan 17, chip-plan 4; comfy-client 33, comfy-custom 11, comfy-tts-engines 16 (7 loops), studios-clients 15, studios-flow-client 9, studios-generate 5, studio-commands 10, studio-lib 15, flow-generate 10, stt 11 (60 s timeout), vision 5, models 51 (1147 lines, real http server). ~370 tests.
Verdict: third-party wire tests. Keep per kind: one plan + one generate happy path + one failure. Keep voice-allocate quota rule (~8; matches the hub rule of 10 requests/day Gemini). Targets: comfy-client 33 -> 8, comfy-tts-engines -> 4, models 51 -> 12, music-generate 24 -> 6, assets-generate 24 -> 8. Total ~110.

### H. Infra
autostart 31 (29 spawns, 2 sleeps, real child processes) -> 6; scheduler 35 (734 lines, 12 sleeps, a 20 s timeout) -> replace sleeps with fake timers, 12; engine-lock 5 -> 3; roles-config 13 -> 5; custom-providers 12 -> 4; clientsearch 7 (2 sleeps) -> 3; research 28 -> 8; factbase 10 -> 4; fact-check 6 -> 3; scriptorium 6 -> 2; android 12 -> 4; ui-course + ui-store 16 -> 6. ~200 -> ~70.

## Tally (inferred)
| area | now | proposed |
|---|---|---|
| bot/Playwright e2e | ~120 | ~25 (e2e) |
| pipelines (engine + media) | ~65 | ~25 (+ ~5 e2e) |
| engine/schema/lint/match/SRS/puzzles/language | ~420 | ~170 |
| player logic | ~200 | ~90 |
| MCP + CLI | ~60 | ~30 |
| live quiz | ~45 | ~14 (+1 e2e) |
| voice/art/music/provider/models | ~370 | ~110 |
| infra | ~200 | ~70 |
Fast default ~510; e2e ~45. Rows do not sum to 1900 because loop multiplication is estimated.

## The true safety net (keep whatever else goes)
1. Shell playthrough: one bot `perfect` run per shell (quiz, rpg, detective, mindmaze, roleplay, encyclopedia, conjugation) in e2e, plus the `player-*-logic` walk test per shell in the fast suite.
2. Course schema/validate: edu-course, course-model, edu-build.
3. Lint error codes: one case per code, merged table.
4. Pipeline happy path + resume: pipeline.test.ts, pipeline-run restart/retry/restart-from-stage.
5. Matching rules: edu-match, translit core, conjugation core.
6. Each MCP tool contract: edu-mcp, mcp-http.
7. SRS, scoring, round, seed-migrations, voice-allocate quota rule.

## pipeline-run.test.ts restart test (flaky/slow)
- Test `a restarted engine on the same folder finishes the run`, `tests/pipeline-run.test.ts:12-44`, 90 s timeout. **Confirmed by reading**: it waits only for `curriculum:all` to be `done` (`:19`), then `engine.stop()` (`:20`), so the stop lands while the next job is in flight, and the point is nondeterministic. It builds a second `Engine` with a hand-copied config (`:21-30`) that can drift from `makePipelineEnv`, then waits up to 60 s for `published` (`:35`). Exact counts `author.count(...) === 1` (`:36-38`) fail if a job was started but not yet recorded when the stop hit, or if a loaded box makes it slow. The flakiness cause is **inferred**; not reproduced (suite not run, machine loaded).
- It is the only test of resume after a crash, so it belongs in the net. Recommendation: **fix, do not delete**. (a) Make the stop deterministic: a mock model that blocks on a gate promise at the stage after curriculum, stop while it waits. (b) Assert the real contract: stages `done` before the stop keep their job ids and are not redone, instead of exact call counts. (c) Reuse the engine factory from `makePipelineEnv`. If timeboxed: keep it in the e2e/slow config with `retry: 1`. Do not delete without a replacement.
- The last test in that file (`:234`, 200 s playtest with Chromium) moves to e2e.

## Proposed split
- `test`: `vitest run` with `exclude: **/*.e2e.test.ts` (and the Chromium describe blocks of the pipeline files moved into `tests/*.e2e.test.ts`). Check that no fast test needs `out/player` before making `globalSetup` e2e-only (inferred: tests that "assemble a game folder" need it, per the comment in `vitest.config.ts`); if some do, keep the build but make it skip when `out/player` is current.
- `test:e2e`: `vitest.e2e.config.ts`, `include tests/**/*.e2e.test.ts`, `fileParallelism` capped at 2, `retry: 1`, `unavailable` browser = fail, not skip.
- Optional `test:all` runs both.

## What the plan needs
- Real timings first (JSON reporter) once the other run is done; cut by cost x value.
- Order: config split -> move Chromium blocks -> merge lint/MCP/media pipelines -> trim tables -> fix pipeline-run restart -> German/language tables last (after HUB-22).
- Update `AGENTS.md`/README test commands. No `.github/workflows` was checked by file listing (inferred: none; verify). Check hub scripts that call `yarn test`.
- For each deleted case, `git log -S` / blame to see if it was added for a bug; keep those.

## Risks
- HUB-22 touches de-grammar, de-verbs, conjugation, bot fixtures (de-b2-reading): conflicts if trimmed before it merges.
- Counts are literal-declaration based; loops undercount, so the real saving is bigger than file-level counts suggest.
- Default `test` no longer catches shell regressions; whoever changes a shell must run `test:e2e`.
- One case per lint code can lose edge cases added for bugs.
- Removing `globalSetup` from the default run can break tests needing `out/player`.
- Bot suites skip silently when Playwright is `unavailable` (`describe.skipIf`): a green run may mean nothing ran.

## Open questions
- Real per-file durations (cache empty).
- Exact real counts and size of the bot FIXTURES/CASES lists.
- Whether CI exists and who calls `yarn test`.
- Accepted e2e budget (assumed ~10 min).
