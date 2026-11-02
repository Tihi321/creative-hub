# HUB-23 changelog

## 2026-11-02 - HUB-23: role-play scene generator built in Edu Studio (uncommitted, live check pending)

Built on the user's decision without first playing `deutsch-a1-pilot`. Plan defaults D1-D4 used (reuse + new reply items, fact-checker on scenes, on by default for `language-a1`..`language-b2`, D4 scene counts).

### edu-game-studio - branch `EGS-39_roleplay-generator` (from `origin/master` 303ee0f), uncommitted

All four tickets sit on one branch because commits were not authorised; each ticket has its own `.claude/tickets/EGS-NN-*/plan.md` and `changelog.md` in that repo so the work can be split into one commit per ticket later.

- **EGS-39** (scene schema, checks, role, prompt)
  - NEW `src/engine/edu/scenes.ts`: `sceneOutputSchema`, pure `checkScenes(out, ctx)` (dangling next, unknown speaker/item, unreachable lines, no end, no reply, non-German text, reply without help, say line giving the answer, mixed du/Sie, cefr above course, too few typed replies, unit verbs unused, vocabulary coverage < 0.5, rules for new items), `sceneCheck(ctx)` for `askRole`, `toRoleplaySection`.
  - NEW `src/shared/lang/de/register.ts` (du/Sie detection).
  - NEW `seed/prompts/scene-writer/scenes.md`, `seed/agents/scene-writer-nina-hartmann.md`; role `scene-writer` in `seed/config/roles.md`, `src/shared/schemas.ts` ROLES, `src/renderer/ui/roles.ts`; `PROMPT_VARS['scene-writer/scenes']` in `authoring.ts` (`ident` exported).
  - `seedRefresh.ts`: pre-change `roles.md` hash in SEED_HISTORY.
- **EGS-56** (lint) - `src/shared/shells/roleplay.ts`: five new warnings `RP_REPLY_NO_HELP`, `RP_UNIT_VOCAB_UNUSED`, `RP_SCENE_LENGTH`, `RP_SAY_GIVES_ANSWER` (skips `listen` dictation lines), `RP_REGISTER_MIXED` (German only); shared `ROLEPLAY_VOCAB_COVERAGE = 0.5`; existing 14 codes unchanged. Fixture `broken-roleplay` rows + `EXPECTED.md`, one `lint.test.ts` row, `docs/player.md`.
- **EGS-55** (pipeline stage)
  - `pipeline.ts`: stage `scenes` between `accepted` and `design`, in STAGES/STAGE_OF/STAGE_FILES; runs after all units; per unit `scenes` -> `scenes_check` (fact-checker) -> at most one `scenes_revise` -> `scenes_accepted` (language-coach, new typed items); then the finale (also checked). Skips with a reason for non-language courses, for `roleplay: false`, and for target languages other than `de`. Old `steps.json` without the stage resumes.
  - NEW `src/engine/edu/scenes-stage.ts` (pure helpers, garden derivation, cap 6 per unit), handlers in `pipeline-handlers.ts`, NEW prompt `seed/prompts/scene-writer/scenes_revise.md`.
  - `assemble.ts`: writes `shells.config.roleplay`, enables `roleplay`, late items (tag `scene`, ids `rp-<unit>-<n>`, stored in `scenes/<unit>.json`) merged with German to `de.json`, the rest to the source catalog.
  - `authoring.ts`: `PIPELINE_SHELLS` includes `roleplay`; `design.md` shell list; `formats.md` `roleplay: true` + `scenes_per_unit` on the four language formats; `schemas.ts` format fields; `brief.ts` optional `roleplay`; seed history for `formats.md`/`design.md`; seed migration `roles-scene-writer-v1` (adds the role to an edited roles.md once).
  - Docs: `docs/mcp-guide.md`, `docs/design.md`, `docs/player.md`.
- **EGS-57** (fixture and bot) - NEW `tests/fixtures/courses/de-roleplay-a1/` (hr + en, target de, 2 units, 2 scenes + finale, 7 reused items + 1 new typed `rp-u-cafe-1`, 12 garden words, umlauts/ß in typed answers); `tests/bot-roleplay.e2e.test.ts` table extended (German fixture: perfect, keyboard+axe, wrong, random); `tests/lint.test.ts` golden list; fixtures README; docs. `scripts/bot/roleplay.mjs` unchanged.
- `ROADMAP.md`: rows EGS-39, EGS-55, EGS-56, EGS-57 (implemented, uncommitted), EGS-58 (reserved, not needed so far).

### creative-hub (master, uncommitted)
- `ROADMAP.md` HUB-23 row: status and dependency "HUB-22 (done)".
- This changelog; status line in `plan.md`.

### Deviations
- One branch for all tickets (no commits allowed), not one branch per ticket.
- Stage runs only for target language `de` (prompt gates, register check and verb tables are German).
- Finale also goes through `scenes_check`/`scenes_revise`; extra prompt `scenes_revise.md`; roles.md seed migration added.
- `sceneCheck` lives in `scenes.ts`, not `authoring.ts` (import cycle).
- `RP_UNIT_VOCAB_UNUSED` measures garden words (the pack has no unit scope); the generator check uses `scope.json`.
- Garden: cap 6 per unit; "13 or more per course" not enforced (fixture has 12).
- E2E: wrong and random modes run only on the German fixture (respecting the EGS-45 trim); perfect/keyboard timeouts raised 120 s -> 240 s.
- Bot types umlauts with the keyboard; the `letter-<char>` buttons are not pressed by any mode.
- Mock language-coach second accepted variant changed to `<answer> ja`.
- Hub `SKILL.md` change not made: it would describe behaviour that is not on edu-game-studio master yet; do it when the branch merges.

### Verification
- `yarn typecheck`: pass. `yarn lint`: pass. `yarn test`: 91 files, 518 tests pass (orchestrator rerun). Workers saw occasional 15 s timeouts in `tests/pipeline-run.test.ts` under full parallel load (the client-loop case takes ~11.7 s alone); reruns green.
- `yarn test:e2e tests/bot-roleplay.e2e.test.ts`: 6/6 pass (~160 s).
- Not run: full `yarn test:e2e`, `yarn build`, the live check (no Edu Studio started, no model calls), a real old data-folder upgrade, any human play.

### Follow-ups / known limits
- Live check per plan (`deutsch-roleplay-a1`, `deutsch-roleplay-b2`), then the user plays; EGS-58 for its fixes.
- Hub `.claude/skills/make-edu-game/SKILL.md` update after merge.
- German quality of generated scenes UNTESTED (no native review).

### Commit status
Uncommitted in both repos.

## Polish

- Speaker clash fixed (`src/engine/edu/pipeline-handlers.ts`, `sceneCall`): a unit's scene-writer call now gets the speakers of the units before it (the prompt and `checkScenes` already make it reuse them or pick new ids), so two units can no longer both define `anna` and show unit 2's character under unit 1's name.
- Garden minimums: `gardenWarnings` in `src/engine/edu/scenes-stage.ts` (4 words per unit, 13 per course); the assemble step adds a "warning: ..." to its note when they are not met. Not an error; the 6-word cap is unchanged.
- Regression test: in `tests/pipeline.test.ts` (the German A1 role-play case) unit 1 and unit 2 scenes must not share a speaker id; the fake scene-writer in `tests/pipeline-helpers.ts` now brings a new character under a new id when earlier speakers are given. Confirmed failing (`['anna']` shared) with the fix disabled, passing with it.
- Checks: `yarn typecheck`, `yarn lint`, `yarn test` (91 files, 518 tests) all pass.

## Merged 2026-11-02

- edu-game-studio master `0f78fb8` (EGS-39, EGS-55, EGS-56, EGS-57).
- Hub step done: `make-edu-game` skill updated for German role-play. Live check and the user playing the courses are still pending.
