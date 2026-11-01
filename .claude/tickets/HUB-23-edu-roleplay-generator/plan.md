# HUB-23 plan: a role-play scene generator in the Edu Studio pipeline for German courses (hr + en speakers, A1 to B2)

**Status: Approved 2026-11-01, build after the user has played deutsch-a1-pilot.**

Repo of the work: `C:\projects\Personal\edu-game-studio` (master at `60ab232`-era state, EGS-54 is the highest id in use). Paths below are relative to it unless absolute. Research: `research.md` in this folder (read it first; where this plan differs from it, this plan wins: see "Findings that change the research"). Style and rules follow `.claude/tickets/HUB-22-edu-start-screen-german/plan.md`.

Rules every worker follows (from the repo's `AGENTS.md`): branch `EGS-NN_<what>` cut from `master`, one commit per ticket, plan in `.claude/tickets/EGS-NN-<name>/plan.md` (copy the task block from here), a row in `ROADMAP.md`, `yarn typecheck && yarn lint && yarn test` green (Node via `fnm exec --using=24 yarn ...`), every interactive element has a `data-testid`, public repo (no keys, no `~/EduGames` content, no personal paths), tests use the mock provider and fakes, nothing spends money. Do not commit or push unless asked. Scratch files under `.claude/temp/`. Tests follow the global `test-discipline` skill: only the few that matter, extend existing files and tables, no near-duplicates, no per-code lint tests where a table or fixture already covers the code.

Hard rules for this ticket (user's): **client model only** (`client/claude-code`, no paid model, no key spent); **never start Scriptorium**; **voice allocation: German goes to VibeTTS**, never to Gemini (the 10 requests a day cannot cover a course); a production is done only when the user has played it.

## Scope

One line per reading, as the global rules ask.

- **Narrow reading, chosen:** a pipeline stage that **writes `shells.config.roleplay` for language courses** (taught language `de`, editions `hr` and `en`, A1 to B2), tied to each unit's CEFR level, vocabulary and verbs, with feedback on wrong replies, and enables the `roleplay` shell on the built game. The player, lint and bot are used as they are.
- **Not the full reading:** no spoken scene audio, portraits or voiced NPC lines (the section allows them; without them the shell shows initials and no play button). That is a follow-up (see "Out of scope"). No new reply kind (spoken = typed with the EGS-18 mic).

### Defaults for the open questions (the user can change any of them; each is one line to flip)

| # | Question | Default used in this plan | How to change |
|---|---|---|---|
| D1 | Reply items | **Option A**: the writer reuses existing item ids where one fits and adds new reply items otherwise (kinds mcq, typed, cloze with gap; B1+ also order). | Option B (reuse only): drop "new reply items" from EGS-55 and the `scenes_accepted` step from EGS-56. Option C (always new): set the reuse cap to 0 in the prompt. |
| D2 | Fact-checker on scenes | **Yes**: the `fact-checker` role reviews scene text (say lines, reply answers, new items) in a `scenes_check` step, one revise round. | Remove the step in EGS-56 (one `if`), the code checks stay. |
| D3 | On by default | **Roleplay is on for formats `language-a1`, `language-a2`, `language-b1`, `language-b2`** through a new format field `roleplay: true`; a brief can switch it off with `roleplay: false`. Non-language formats never run the stage. | Set the field to `false` in `seed/config/formats.md`. |
| D4 | Scenes per level | As in the research: **A1 1 per unit (4) + finale; A2 1 to 2 per unit + finale; B1 and B2 2 per unit + finale.** 8 to 12 lines, 3 to 5 replies per scene, at least one typed reply per unit. | Format fields `scenes_per_unit: [min, max]` in `formats.md`. |

## Out of scope (and why)

- **Scene audio and speaker portraits** (German VibeTTS clips for say lines, art for speakers): a follow-up. Voice for lines would be local VibeTTS only; do not couple it to this work.
- **Branching dialogue.** The walker is a single chain by design (`roleplay.ts:58-67`); the generator writes chains.
- **A spoken-reply kind and pronunciation scoring** (ROADMAP "Later").
- **Native review of the model-written German dialogue.** Not available; the plan adds mechanical checks plus the fact-checker pass and says so in the live check.
- **Courses other than language courses** (detective, quiz-only topics): the stage is skipped. Old courses are not touched until a user restarts them.
- **Changing the roleplay shell, its lint codes or the bot driver**, except the three new warnings in EGS-57.

## Findings that change the research (verified in code)

1. **EGS-39 is free.** No row in `ROADMAP.md` (grep), no branch (local or remote), no ticket folder. Highest ids in use are EGS-38 and EGS-40..54. Free: EGS-39 and EGS-55 upward. The hub ROADMAP row 17 (HUB-23) and HUB-22 `plan.md:20,362,370` already name EGS-39. So this plan uses **EGS-39 for the first ticket** (which also adds the missing `ROADMAP.md` row) and **EGS-55 to EGS-58** for the rest. (The plan lists tickets in build order, so ids are not monotonic.)
2. **The "design" prompt is not the gate.** `PIPELINE_SHELLS = ['quiz-arena','encyclopedia','mindmaze','rpg']` (`src/engine/edu/authoring.ts:~781`, comment just above says role-play and detective "need authored sections that no role writes yet"). A shell not in the list ends in `extensions.pipeline.requestedShells` and is not enabled. EGS-56 adds `roleplay` to the list **and updates that comment**, and `seed/prompts/game-designer/design.md` (the line ~17 that lists the shells "the player has today" names four; add `roleplay` for language courses).
3. **The `accepted` stage is per unit inside the unit loop** (`pipeline.ts:~685`, after `explain`, `R.language` only), so scene-written reply items miss `distractors`, `fact_check`, `explain`, `accepted` if the new stage simply comes after. The plan handles this explicitly (see EGS-56 "late items").
4. **Stage plumbing needs four places, not one:** `STAGES` (`pipeline.ts:38`), `STAGE_OF` (task name to stage, ~45-85), `STAGE_FILES` (~90), and the step list/driver near the `design` step (~491). The new task names (`scenes`, `scenes_check`, `scenes_revise`, `scenes_accepted`) must be in `STAGE_OF` or `restart from: scenes` will not find them. Old `steps.json` files lack the stage; a missing stage must read as "not run yet", never as an error.
5. **Seed refresh is the way prompts reach a data folder** (`src/engine/store/seedRefresh.ts`, `seedMigrations.ts`, ticket EGS-47). A new prompt, role, agent and the changed `formats.md` and `design.md` all need history entries, or an existing `~/EduGames` never receives them (the HUB-22 live check needed this).
6. **hr/en editions need no extra work for scene text.** `editions.ts` translates every source-catalog string and accepted list and skips keys living in the target catalog. German `text` and reply answers go in `de.json`; `translation`, `help`, titles, gloss and item prompts go in the source catalog and are translated.

## Files and modules to touch (by ticket)

### EGS-39 scene schema, checks, role, prompt (no pipeline wiring yet)
- NEW `src/engine/edu/scenes.ts`: `sceneOutputSchema` (zod; the writer's answer: `speakers[]`, `scenes[]` with `lines[]`, `newItems[]`), `checkScenes(output, ctx): Problem[]` (pure), `toRoleplaySection(...)` helper types. Reuse `walkScene` and the lint logic from `src/shared/shells/roleplay.ts` instead of copying (export what is missing there; no behaviour change).
- `src/engine/edu/authoring.ts`: the `scene-writer` entry in `ROLES`/role task table, `PROMPT_VARS` entry (`authoring.ts:~863-888`), the `askRole` check wiring helper `sceneCheck`.
- NEW `seed/prompts/scene-writer/scenes.md`; NEW `seed/agents/scene-writer-<name>.md` (follow the style of `language-coach-ines-markovic.md`); `seed/config/roles.md`; `src/renderer/ui/roles.ts`.
- `src/engine/store/seedMigrations.ts` / `seedRefresh.ts` (history entry for the new files; test already exists).
- `ROADMAP.md`: the **EGS-39 row** (absent today) and rows for EGS-55 to EGS-58 marked open; plan copied to `.claude/tickets/EGS-39-scene-schema-role/plan.md`.
- Tests: `tests/edu-authoring.test.ts` (extend: PROMPT_VARS contract and one golden round trip), NEW `tests/edu-scenes.test.ts` (the `checkScenes` table), seed-history test (extend the existing one).

### EGS-55 pipeline stage `scenes`, late items, assemble
- `src/engine/edu/pipeline.ts`: `STAGES` (insert `scenes` between `accepted` and `design`), `STAGE_OF`, `STAGE_FILES` (`scenes/*`, `reviews/scenes_check-*`), the driver step (per unit, then the finale), skip for non-language courses and for `roleplay: false`.
- `src/engine/edu/pipeline-handlers.ts`: handlers `scenes`, `scenes_check`, `scenes_revise`, `scenes_accepted`; the input builder (unit title, objectives, `scope.json` vocabulary and verbs via `unitScope`, grammar, the unit's items with canonical answers, cefr, du/Sie rule, speakers, `{{language_rules}}`); a renderer of scene text for the fact-checker (`renderSceneForReview`, next to `renderItemForReview`).
- `src/engine/edu/assemble.ts`: a roleplay branch next to the other shell branches (~232-240): merge late items into the pack with `put()` (German answers to the target catalog via the existing `it.taught && tgt` route, prompts/whys to the source catalog, `putAccepted`), write `shells.config.roleplay` (`speakers`, `scenes`, `garden`, `finale`), add `roleplay` to `shells.enabled`, record it in `extensions.pipeline`, never in `requestedShells`. Garden derived in code.
- `src/engine/edu/authoring.ts`: `PIPELINE_SHELLS += 'roleplay'` and the comment; `normalizeDesign` keeps working.
- `seed/prompts/game-designer/design.md` (shell list), `seed/config/formats.md` (`roleplay: true`, `scenes_per_unit` on the four language formats; `language-b2` exists from EGS-36), `src/shared/schemas.ts` (format fields `roleplay`, `scenes_per_unit`), `src/shared/brief.ts` (optional `roleplay: boolean`, comment fix), seed history entries for `formats.md` and `design.md`.
- Docs: `docs/mcp-guide.md` (pipeline stages, brief field), `docs/design.md` (pipeline list), `docs/player.md` (roleplay: now generated).
- Tests: `tests/pipeline-helpers.ts` (a scene-writer mock), `tests/pipeline.test.ts` (one new case).

### EGS-56 lint additions
- `src/shared/shells/roleplay.ts`: new warning codes (below), computed from data that is already in the section and the catalogs; reuse `walkScene`.
- `tests/fixtures/courses/broken-roleplay/course/...` (new rows) and `.../EXPECTED.md`; `tests/lint.test.ts` (the table-driven lint test, one row per new code only).
- `docs/player.md` (lint code list).

### EGS-57 German fixture and bot
- NEW `tests/fixtures/courses/de-roleplay-a1/` (hr + en editions, `targetLang: de`, over a small A1 unit set like `de-verbs-a1`): speakers, 2 scenes, a finale, garden, reply items reused and one new typed item.
- `scripts/bot/roleplay.mjs` only if the German fixture exposes a real gap (research expects none); `tests/bot-roleplay.e2e.test.ts` (add the fixture to the existing run list, no new file).
- `docs/player.md`, `docs/mcp-guide.md`, `ROADMAP.md` row.

### EGS-58 live-check fixes (reserved)
- Reserved id for whatever the live check finds (as EGS-53 was for HUB-22). Created only if needed; the changelog of EGS-57 says whether it is.

## Tasks for workers

### EGS-39 Scene schema, checks, role and prompt
- **Inputs:** research sections 1, 3, 4 and "Proposals"; this plan's D1 to D4.
- **Do:**
  1. `sceneOutputSchema` (strict zod, lenient only where the other schemas are lenient): `speakers: [{ id, name, learner? }]` (2 to 4 NPCs plus the learner), `scenes: [{ id, unit, title, setting, cefr, start, lines: SayLine | ReplyLine }]` with the chain rules of `roleplay.ts` (`next` explicit, `null` at the end), `newItems: [authored item]` limited to kinds `mcq`, `typed`, `cloze` (with a gap), `order` from B1; each new item carries `objective`, `prompt`, `explanation`, a `why` per wrong choice and (typed) a draft `accepted`.
  2. `checkScenes()`, pure, returns `Problem[]` so `askRole` can run its one repair round. Hard errors: dangling `next`, unknown speaker, unknown item id, unreachable line, no end, scene without a reply, say `text` or reply answers not German (the `RP_TEXT_NOT_TARGET` case made an **error** on the generator side), reply with no `help`, a say line equal to a reply answer (gives it away), mixed du/Sie inside one scene, scene `cefr` above the course, fewer than the unit's required typed replies, a verb unit whose verbs never appear in a reply (use `conjugate`/`findVerb` from `src/shared/lang/de` to accept the form), unit vocabulary coverage below a threshold (default: at least half of the unit's `vocabulary` terms appear in some scene of the unit).
  3. Role `scene-writer`: agent file, prompt `seed/prompts/scene-writer/scenes.md` that carries `{{language_rules}}` as is, the level gates (A1 du, greetings, ordering with `sein`, `haben`, `möchten`; A2 Perfekt, separable verbs, requests; B1 Präteritum, Konjunktiv II, polite requests and complaints with Sie; B2 longer turns, register shifts, Konjunktiv I only in reported speech), the scene count and length bounds from D4, and the output shape. Scenario list per level is prompt data (introductions, café order, directions, hotel, doctor, phone, complaint), chosen to fit the unit.
  4. `PROMPT_VARS` entry (variables the handler fills; the existing both-ways test must pass), roles config and UI role list, seed history entry.
  5. Add the ROADMAP rows (EGS-39 and EGS-55 to EGS-58, each one line, in the HUB-22 style).
- **Outputs:** `scenes.ts`, prompt, agent, role, tests, ROADMAP rows, changelog.
- **Contract:** `sceneOutputSchema`, `checkScenes(output, ctx)`, the role id `scene-writer`, the task names `scenes`, `scenes_check`, `scenes_revise`, `scenes_accepted` (reserved for EGS-55), prompt variable names in `PROMPT_VARS`. EGS-55 codes against these.

### EGS-55 Pipeline stage `scenes`, late items and assemble
- **Inputs:** EGS-39 contract; findings 3 to 6; `pipeline.ts` unit loop (~640-690) and the `design` step (~491).
- **Do:**
  1. Stage order: `... accepted, scenes, design ...`. The stage runs **after the per-unit loop has finished for every unit** (it needs complete items) and only when `R.language` and the format/brief allow roleplay. Per unit: `scenes` (scene-writer) -> `scenes_check` (fact-checker over the scene text and the new items, D2) -> at most one `scenes_revise` when the check says revise (the same must-pass gate pattern as `fact_check`; a second failure blocks with a note, as for items) -> `scenes_accepted` (language-coach `accepted` task for the **new typed items only**, by `ref`). Then one `scenes` call for the **finale** over the units' reply items (ids reused, no new items).
  2. **Late items (how they get checked, D1):** the writer must deliver, for each new item, the same fields the item schema requires (`explanation`, a `why` per wrong choice, a draft `accepted`). That is the explain step's output moved into the writer call; the `explainer` role is **not** re-run. The checks that replace the skipped steps: the authored-item schema (same zod as the item writer), `scenes_check` (the fact-checker sees the new items through the same `renderItemForReview`), `scenes_accepted` for typed items, and the normal `edu_lint`. New items get tag `scene`, ids `rp-<unit>-<n>`, and are stored in `scenes/<unit>.json` (not in the unit's `items` file, so a restart from `scenes` is idempotent and never rewrites earlier work).
  3. **Garden in code:** per unit, words from `scope.json` vocabulary (`term`, `gloss`) whose term appears in a scene or whose item answer equals it; `{id, text -> target key, gloss -> source key, item -> item id}`; cap 4 to 6 per unit, 13 or more per course; deterministic order.
  4. **Assemble:** per the file list. Speakers, scenes and garden strings get catalog keys exactly as the `hr-a1-greetings` fixture names them (`rp.sc.<scene>.l<n>`, `.tr`, `.help`) so the existing fixtures and the new output look the same. Lines with `text` and reply answers -> target catalog; everything else -> source catalog.
  5. `PIPELINE_SHELLS`, design prompt, formats, brief field, docs, seed history.
  6. Resume/restart: `restart: true, from: 'scenes'` reruns only the new tasks; an old run without the stage resumes without error; a non-language course records `skip` with the reason "not a language course".
- **Outputs:** pipeline code, handlers, assemble, prompt/format/seed changes, docs, tests, ROADMAP row.
- **Contract:** `shells.config.roleplay` as in `src/shared/shells/roleplay.ts`; format fields `roleplay`, `scenes_per_unit`; brief field `roleplay`; item tag `scene`.

### EGS-56 Lint additions
- **Inputs:** research "Reply checking" and the current 14 `RP_*` codes (`roleplay.ts:163-300`).
- **Do:** add **warnings only** (they never fail an existing course): `RP_REPLY_NO_HELP` (a reply with no `help`), `RP_UNIT_VOCAB_UNUSED` (a unit's scope vocabulary share used in its scenes below the threshold; threshold is a constant shared with EGS-39), `RP_SCENE_LENGTH` (outside 6 to 14 lines or 2 to 6 replies), `RP_SAY_GIVES_ANSWER` (a say line equals a reply answer), `RP_REGISTER_MIXED` (du and Sie forms in one scene, German courses only). The generator-side errors of EGS-39 already stop bad output; these catch hand-edited and imported courses.
- **Outputs:** code, fixture rows + `EXPECTED.md`, lint table rows, docs.
- **Contract:** the five codes; no change to the 14 existing codes.

### EGS-57 German fixture and bot
- **Inputs:** EGS-39, EGS-55 output shape; fixture `hr-a1-greetings` and `de-verbs-a1` as models.
- **Do:** the fixture `de-roleplay-a1` (hr + en, `targetLang: de`); bot runs on it: perfect, wrong (help lines appear, third miss shows the reply, scene ends), random, keyboard-only (umlauts via the letter buttons). Add it to the existing e2e list; touch `scripts/bot/roleplay.mjs` only if a real gap shows. Docs.
- **Outputs:** fixture, e2e rows, docs, ROADMAP row.
- **Contract:** none new.

## Order, dependencies, parallel work

```
Wave 1: EGS-39 (schema, checks, role, prompt, ROADMAP rows)
Wave 2 (after 39 merged): EGS-55 (stage + assemble)      EGS-56 (lint additions; independent of 55, may run in parallel)
Wave 3 (after 55): EGS-57 (German fixture, bot)
Then the live check (below). Fixes found there become EGS-58 (or a new id).
```
All tickets sit on separate branches cut from `master`; EGS-55 rebases on EGS-39. Merge order: 39, 56, 55, 57. Conflict hot spots: `authoring.ts` and `PROMPT_VARS` (39, 55), `pipeline.ts` STAGES (55 only), `ROADMAP.md` (all: one row each, resolve by hand), `seedMigrations.ts` (39, 55: two entries, keep both). The split 39 + 55 may merge into one ticket if the repo prefers fewer (HUB-22 used one per stage); the plan keeps them apart because 39 is pure and testable without the pipeline.

## Acceptance criteria and the tests that prove each

Only the few tests that matter. No per-code lint tests beyond the existing table and fixture rows.

| # | Criterion | Proof |
|---|---|---|
| S1 | `checkScenes` accepts a good model answer and reports each class of fault | `tests/edu-scenes.test.ts`: one golden German A1 output passes; one table of broken outputs (dangling next, unknown speaker, unknown item, no typed reply, German text missing, reply with no help, say line gives the answer, unit vocabulary never used) each gives the right Problem. Reuses `walkScene` |
| S2 | Prompt contract and seed delivery | `tests/edu-authoring.test.ts` PROMPT_VARS test (exists, extended), seed-history test (exists, extended): the `scene-writer` files, `formats.md` and `design.md` reach an existing data folder |
| P1 | The stage writes a valid German section | `tests/pipeline.test.ts` (mock provider, helpers in `pipeline-helpers.ts`): a small German course run yields `shells.config.roleplay`, `roleplay` enabled, the section passes `validateCourse` and `lintGameData` with **0 `RP_*` errors**, German in `de.json`, translations in the `hr` and `en` catalogs, new typed items have accepted lists |
| P2 | Restart and skip | same test file: restart from `scenes` is idempotent (same ids and bytes); a non-language course skips the stage; an old `steps.json` without the stage resumes |
| L1 | New lint warnings fire and nothing else changes | `tests/lint.test.ts` rows for the five new codes only; existing fixtures still lint 0 errors |
| B1 | The German section plays in the real player, all modes | `tests/bot-roleplay.e2e.test.ts` (Chromium, `yarn test:e2e`) on `de-roleplay-a1`: perfect completes, wrong shows help then the reply, random in between, keyboard-only, 0 console errors, axe 0 |
| Z | Repo health | `yarn typecheck`, `yarn lint`, `yarn test` (fast, no Chromium) on each branch; `yarn test:e2e` for EGS-57 |

Each ticket's changelog ends with the DONE / NOT DONE / UNTESTED list. UNTESTED by design until the live check: real German quality, the bot on a real generated course, a human playing.

## Live check (hub session; no paid models; never start Scriptorium)

Preconditions: `pwsh -File scripts\hub.ps1` (status). Start only Edu Studio (`pwsh -File scripts\hub.ps1 start edu-studio`). ComfyUI, Pixel Studio, Chiptune Studio, Gemini and Scriptorium are **not** needed or used (art, music and voice off; scene audio is out of scope). All model work is `model: "client/claude-code"` ($0): the session loops `edu_wait` -> `edu_get_task` -> answer -> `edu_submit_task`. Check the data folder has the new seeds first (seed refresh, finding 5). Open `runs/deutsch-roleplay-a1.md` and `runs/deutsch-roleplay-b2.md` from `runs/_template.md` and record every id, decision and check.

1. **A1 course with roleplay.** `edu_run_pipeline`, slug `deutsch-roleplay-a1`, brief `{"topic":"German for beginners","audience":"Croatian and English speaking adults starting German","sourceLang":"hr","languages":["hr","en"],"targetLang":"de","cefr":"A1","format":"language-a1","units":4,"shells":["quiz-arena"],"model":"client/claude-code","media":{"art":{"enabled":false},"music":{"enabled":false},"voice":{"provider":"auto"}}}` (the worker adjusts the media keys to the real schema). Expect `roleplay` enabled without being listed in `shells` (D3). Check: 4 unit scenes plus a finale, 8 to 12 lines each, every unit has a typed reply, garden present, `edu_lint` 0 errors (list the warnings, including the new `RP_*` ones), `languages = [hr, en]`, German in `de.json` only, the `help` and translations in hr and en.
2. **B2 course with roleplay.** Slug `deutsch-roleplay-b2`: `{"cefr":"B2","format":"language-b2","units":2,"languages":["hr","en"],"targetLang":"de","sourceLang":"hr","model":"client/claude-code","media":{"art":{"enabled":false},"music":{"enabled":false}}}` (2 units only to keep the model work short; B2 formats run the readings too). Check: 2 scenes per unit plus a finale, longer turns and register shifts, a Konjunktiv II or reported-speech reply where the unit teaches it, `edu_lint` 0 errors, the `scenes_check` verdicts are recorded.
3. **The bot passes** on both courses: `node scripts\play.mjs courses\<slug>\build --mode perfect --shell roleplay`, then `--mode wrong` and `--mode random`. Perfect completes every scene; wrong shows `help` then the reply and never dead-ends; 0 console errors. Record the run time (the bot takes about 0.9 s per answer; EGS-54).
4. **Voice rule.** `edu_voice_quota` and `edu_voice_plan` show no German request to Gemini and no scene audio planned. Nothing is generated.
5. **The user plays it.** Ask the user to play the roleplay mode of `deutsch-roleplay-a1` and one scene of `deutsch-roleplay-b2`, and to read the German of both. A production is done only when the user has played it.
6. **Not verified by anyone but the user:** the correctness and naturalness of the model-written German dialogue (no native review), the Croatian and English help and translations, whether the scenes fit their units and are fun. Mark UNTESTED until the user answers.

## Risks

- **Unreviewed German in dialogue.** Free dialogue is likelier to contain errors than item answers. Mitigation: `{{language_rules}}`, the verb-table check on verb units, the fact-checker pass (D2), the generator-side German-text error, and the explicit human-review flag in the live check.
- **Late items miss earlier steps.** Handled by writing `explanation`/`why`/`accepted` inside the writer call, the same schemas, `scenes_check` and `scenes_accepted`. If the user picks Option B this risk disappears.
- **Cost and time.** One writer call, one check, and sometimes one revise per scene unit; about 5 to 15 scene calls per course plus checks, all client-model jobs that park and need the `edu_wait` loop. A1 bot time is minutes per persona (EGS-54).
- **Wrong-language text.** A say line written in the source language: made a generator error (EGS-39), a warning in the shell lint stays for imported courses.
- **All-mcq scenes.** `RP_REPLY_NOT_PRODUCTION` is only a warning in the shell lint; the generator requires one typed reply per unit.
- **Shared code.** `authoring.ts`, `pipeline.ts` STAGES, `assemble.ts` and `PROMPT_VARS` serve every course. Inserting a stage shifts stage-based restart; keep the stage a no-op for non-language courses and tolerate old `steps.json`.
- **Prompt delivery.** A changed prompt reaches an existing data folder only through the seed refresh history (finding 5); forgetting it means the live check silently runs the old design prompt.
- **Late-bound behaviour not read.** The mid-section of `src/player/shells/roleplay/index.ts` (star thresholds, unlock rule) and `kit` mastery numbers were not read in the research; EGS-57's bot run is the first real proof. Also not read: how `brief.shells` flows into the design step beyond the notes string (`pipeline-handlers.ts:~597`); EGS-55 must confirm `roleplay: true` from the format reaches the enabled list.

## Rollback

- Everything is additive and per ticket. **Per ticket:** `git revert` the ticket's merge commit; no data migration is involved.
- **Fast off switch without a revert:** set `roleplay: false` in `seed/config/formats.md` (and in the user's `~/EduGames/config/formats.md`), or pass `roleplay: false` in a brief. The stage then records a skip and the course builds as before.
- **A bad generated course:** `edu_run_pipeline` with `restart: true, from: 'scenes'` to redo, or `edu_course_edit` to remove `shells.config.roleplay` and `roleplay` from `shells.enabled`; the items the stage added are tagged `scene` and live in `scenes/<unit>.json`, so they can be dropped without touching the unit items.
- **Old courses** are unaffected: no stage in their `steps.json`, no section in their pack.

## Hub changes (this repo, `C:\projects\Personal\creative-hub`)

- `ROADMAP.md`: update row **HUB-23** (row 17): replace "Open, no plan yet" with "Open, plan in `.claude/tickets/HUB-23-edu-roleplay-generator/plan.md`; tickets EGS-39 and EGS-55 to EGS-57 in `edu-game-studio`; live check with `deutsch-roleplay-a1` and `deutsch-roleplay-b2`"; also change the Dependencies cell from "HUB-22" to "HUB-22 (done)". Mark it done only after the live check **and** after the user has played the courses.
- `.claude/skills/make-edu-game/SKILL.md`: (a) the line near the top of the pipeline section (line ~26: "role-play and detective need authored sections ... so they are recorded and not enabled") becomes: for language courses (formats `language-a1` to `language-b2`) the pipeline writes and enables role-play scenes (stage `scenes`, roles `scene-writer` and the fact-checker; `roleplay: false` in the brief turns it off); detective still needs an authored section; (b) the language-course section: replies are course items (new typed replies get accepted lists), scene text is German in the target catalog, help and translations are translated into hr and en, and the bot is run with `--shell roleplay`; (c) the voice section: scene lines have no audio; if audio is added later, German goes to local VibeTTS and never to Gemini; (d) keep the rules about client model work and never starting Scriptorium. Delete nothing else.
- `runs/deutsch-roleplay-a1.md` and `runs/deutsch-roleplay-b2.md`: production logs, created by the live-check session from `runs/_template.md`.
- `README.md` table row for Edu Studio: mention role-play scenes for language courses only if the row lists capabilities.
- `MEMORY` (user auto-memory) update after the run: what was merged, what the live check showed.
- No change to `services.json` or `.mcp.json` (no new service); `scripts/hub.ps1` unchanged.

## Optional follow-ups (flagged, not in this plan)

- Scene audio: German VibeTTS clips per say line and speaker portraits (local voices only).
- Branching scenes (the walker is a chain today).
- A spoken-reply scene mode using the EGS-18 mic with a stricter transcript tolerance.
- Scenes for non-language courses (interviews, historical dialogue) in the same stage.

## Open questions for the user (also returned in the summary)

1. Reply items (D1): Option A as above (reuse plus new), or reuse only?
2. Fact-checker on scenes (D2): keep it (costs one more client-model job per scene unit) or code checks only?
3. Roleplay on by default for all four language formats (D3), or opt-in per brief?
4. Scene counts (D4): are 4 scenes at A1 enough, or do you want more?
5. Is the next free EGS range (EGS-39, EGS-55 to EGS-58) fine, or should another session's tickets be checked first?
