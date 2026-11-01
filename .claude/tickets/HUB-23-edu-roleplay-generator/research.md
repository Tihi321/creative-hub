# HUB-23 / EGS-39 research: role-play scene generator

## Question
How can the Edu Studio pipeline write `shells.config.roleplay` scenes itself for German courses (A1 to B2, hr and en editions), tied to each unit's CEFR level, vocabulary and verbs, with feedback on wrong replies? What exists, what is missing, how to check replies and the bot, risks, and a ticket split.

## Answer
- The shell, the lint (14 `RP_*` codes), the player and the bot driver are generic and need no change for German. Replies are ordinary course items (`reply: <itemId>`), so matching, accepted lists and the hr/en editions already work through the item machinery.
- Everything on the authoring side is missing: no role, prompt, schema, pipeline step or assemble code writes a `roleplay` section. `PIPELINE_SHELLS` excludes it (`src/engine/edu/authoring.ts:781`; comment at 777-780 says so) and the design prompt never offers it (`seed/prompts/game-designer/design.md:17`). A requested `roleplay` is only recorded in `extensions.pipeline.requestedShells` (`assemble.ts:218`). EGS-39 is not yet a row in the edu-game-studio ROADMAP.md (grep found none); only HUB-22 `plan.md:20,362,370` and hub ROADMAP row 17 name it.
- Recommended shape: a `scene-writer` role and a pipeline stage `scenes` after `accepted`, before `design`. It writes scenes and the reply items they need. A code step builds the garden, speakers and finale. Assemble writes the section and the catalogs. The existing lint is the gate, plus a few new generator-side checks.
- Not run: nothing was executed, only read.

## Path through the code

### 1. Scene data model (confirmed, `src/shared/shells/roleplay.ts`)
- Section `shells.config.roleplay` = `{speakers[], scenes[], garden[], finale?, theme?}` (79-87). Required section (`requiresSection: true`, 304).
- Speaker: `{id, name(key), learner?, portrait?}` (22-30).
- Scene: `{id, unit?, title, setting?, cefr?, start, lines[]}` (58-67). Finale has no `unit`.
- Lines are a single chain, no branches: `next` id or `null` (explicit). Two kinds:
  - say: `{id, say(speaker), text(target-catalog key), translation?, audio?, listen, next}` (32-43).
  - reply: `{id, reply(itemId), help?, youSay?, next}` (45-54). `help` is the speaker's hint after a miss (edition key). `youSay` is the bubble text when the item answer is not the whole sentence.
- Reply kinds are whatever item the reply points at; the shell asks it through the shared question screen. "Choose" = mcq (and the other choice kinds). "Typed" = typed, cloze gap without bank, listening mode `type`, crossword (`isProduction`, 143-157). "Spoken": there is no spoken reply kind. EGS-18 is a mic button that fills the typed input (ROADMAP.md:56), so spoken = typed with STT. Listening items give audio input (confirmed by reading; mic not run).
- Scoring (`src/player/shells/roleplay/dialogue.ts:1-60`): up to `MAX_TRIES = 3` answers; a miss makes the speaker repeat with `help` (log kind `help`), the turn is asked again; after the third miss the right reply is shown (`shown`) and the scene goes on, never a dead end. Only the FIRST answer counts for stars (score 0..1, partial credit); the item stays in the review queue until right. Unit unlock/stars come from the kit (`ShellSession`, 2 stars = mastered per the bot header, `scripts/bot/roleplay.mjs:1-20`).
- Garden (`garden.ts:1-30`, 91-98): stages `seed | sprout | bud | bloom | wilted`. Stage comes from `stageOf(card, queued)` over `mastery(card)` of the word's item: sprout = fewer than 3 right in a row, bloom = next review 21 days or more, wilted = missed and queued. Garden word = `{id, text(target key), gloss(edition key), item}` (69-77); `water` practises due words.
- Lint (`roleplay.ts:163-300`): `RP_UNIT_NO_SCENE`, `RP_SCENE_UNIT_MISSING`, `RP_START_MISSING`, `RP_NEXT_MISSING`, `RP_NO_END`, `RP_LINE_UNREACHABLE`, `RP_SPEAKER_MISSING`, `RP_REPLY_ITEM_MISSING`, `RP_SCENE_NO_REPLY`, `RP_GARDEN_ITEM_MISSING`, `RP_FINALE_MISSING` (errors); `RP_TEXT_NOT_TARGET`, `RP_REPLY_NOT_PRODUCTION`, `RP_CEFR_ABOVE_COURSE` (warnings). `validate` blocks duplicate ids (221-237). `textRefs` makes the generic lint check every key in every edition (`(in en)`).

### 2. Fixture `hr-a1-greetings` (confirmed by loading the pack)
- hr taught, en edition, A1. 3 units, one scene per unit (cafe 11 lines/4 replies, school 12/4, hotel 9/4) plus a `final` scene (13 lines/6 replies), 5 speakers (4 NPCs + learner `you`), 13 garden words. Each reply points at an existing item (`g-hello-mcq`, `g-name-typed`, ...). Mix of mcq and typed. `help` on every reply.
- Text keys: say `text` in the target catalog (`rp.sc.cafe.l1`), `translation` (`.tr`) and `help` in the edition catalog.

### 3. Pipeline (confirmed)
- `STAGES` (`pipeline.ts:38`): plan, research, factbase, curriculum, scope, articles, items, distractors, fact_check, explain, accepted, design, story, art, music, assemble, review, harvest, voice, editions, build, lint, playtest, publish. Stage-to-file mapping at 45-103 (a new stage needs entries in `STAGE_OF`, `STAGE_FILES`, and the step list near 535).
- `scope` step (`pipeline-handlers.ts:278-292`) writes `scope.json`: per unit `vocabulary[{term,gloss}]`, `verbs[{inf,tense,level}]`, `grammar[]`. Read by `unitScope` (207). This is the vocabulary/verbs source for scenes. Verb units are flagged by the curriculum (`verb: true`; `extensions.language.verbUnits`, `assemble.ts:229-231`).
- `design` step (576-604) offers `PIPELINE_SHELLS`; `normalizeDesign` puts unknown shells in `requested` (`authoring.ts:806-821`). `story` is a frame only for `rpg`.
- `assemble` (`assemble.ts:232-240`) builds `shells.config` from the design: quiz-arena, rpg story, encyclopedia glossary. No roleplay branch. `put(cat,key,value)` writes catalog strings; `it.taught && tgt` routes answers to the target catalog (45, 104); `putAccepted` writes accepted lists.
- `editions` step (`editions.ts:1-30`) translates every source-catalog string and accepted list except keys living in the target catalog. So `translation`, `help`, titles, gloss, item prompts written to the source catalog get hr/en for free. Taught text goes in the target catalog and is never translated.
- Role plumbing: `askRole` with a zod schema and a `check` returning `Problem[]`; one repair round, then a thrown error (`authoring.ts:79-89`). `PROMPT_VARS` (`authoring.ts:863-888`) is the contract between handler and template, tested both ways. A new role touches ROLES, `src/renderer/ui/roles.ts`, `seed/config/roles.md`, a seeded agent, a prompt, and the seed refresh history (EGS-47; EGS-32 did the same for `translator`, `.claude/tickets/EGS-32-editions-step/plan.md`).
- `playtest` stage runs the bot with 5 personas (perfect, wrong, strong 0.9, average 0.75, struggling 0.55) (`playtest.ts:28-34`). The bot driver is chosen by the shell the game runs (`scripts/bot/index.mjs`). Chromium is needed, so this is `yarn test:e2e` territory (HUB-24).

### 4. German rules and matching (confirmed)
- `languageRulesText` (`src/shared/lang/index.ts`) is the `{{language_rules}}` text: articles with nouns, level-gated cases, du vs Sie "never mix in one item", ä ö ü ß canonical, answers without pronoun are wrong, accepted-list rules (`rules.ts:6-39`). Reusable as is in a scene prompt; it already says "A dialogue item says which one it uses". B2 adds `rules-b2.ts`.
- `matchAnswer` (`src/shared/edu/match.ts:137`) with `lang: 'de'`: ae/oe/ue/ss are accepted as alternates and never cost a grade, a missing umlaut is wrong (strict default, 189-194), a lowercase noun is accepted with a `caps` note, typo tolerance is on for typed and off for conjugation and word-bank gaps (`checkers.ts:79-148`). The reply therefore needs no new matcher; the accepted list is the only lever.
- Accepted lists come from the `language-coach/accepted` task (`seed/prompts/language-coach/accepted.md`), which takes typed items by `ref`. Items the scene-writer adds after that step would miss it unless the stage runs earlier or the accepted step is re-run for them.
- `verbTable` (`findVerb`, `conjugate`, `tenseForCefr`) can check a verb form in a scene line; today it is used only by the conjugation lint (`lint-conjugation.ts`) and `GRAMMAR_*` (`lint-grammar.ts`). There is no German lint of free dialogue lines.

## What is generic and what is missing
| Part | Status |
|---|---|
| Schema, walker, lint (14 codes), broken fixture + EXPECTED.md, player, garden, i18n (de/hr/en UI), bot driver | generic, done (EGS-13, EGS-34) |
| Editions of scene text | generic via `editions` |
| German matching of typed replies | generic |
| Prompt, role, agent, `PROMPT_VARS`, zod `sceneSchema` for model output (ids, line chain, speakers) | missing |
| Repair `check`: model output to Problem[] (dangling next, unknown speaker/item, no reply, text language) | missing; reuse `walkScene` and the lint logic as a pure `checkScenes()` instead of copying |
| Pipeline stage `scenes`, STAGE_OF/STAGE_FILES, resume/restart | missing |
| Reply items: scenes need items with `objective`, `prompt`, wrong-choice `why`, accepted lists | missing: decide reuse vs new (below) |
| Garden words (text, gloss, item) | missing; derive in code from scope vocabulary + item answers |
| Assemble: write section, `put` keys into target vs edition catalogs, enable `roleplay` in `shells.enabled`, `PIPELINE_SHELLS` entry, design prompt text | missing |
| Brief: `shells` already a list on the brief (`design` notes mention `h.R.brief.shells`); format switch so only language formats opt in | missing |
| Lint: unit vocabulary used, level, verbs, scene length, feedback present, speaker count | partly (CEFR only), see below |

## Proposals

### Tie to units, scenes per level
- Input per scene call: unit title, objectives, `scope.json` vocabulary (`term`, `gloss`), verbs (`inf`, `tense`, `level`), grammar notes, the unit's existing items (id, kind, prompt, canonical answer), `cefr`, du/Sie rule, speakers, `{{language_rules}}`.
- Reply items: Option A (recommended) the writer reuses existing item ids where one fits and may add new reply items (kinds mcq, typed, cloze with gap; B1+ also order) for the rest; new items pass the same item schema, each wrong choice gets a `why`, typed ones go through the accepted step. Option B only reuse existing items: simpler, but replies then read as quiz questions, not conversation. Option C replies are always new items: a clean conversation, more cost, and a bigger lint surface.
- Scene counts (proposal, matches `config/formats.md`: A1 4 units, A2 5, B1 6, B2 6): 1 scene per unit at A1 (4 plus the finale), 1 to 2 at A2, 2 at B1 and B2, plus one finale. Per scene 8 to 12 lines, 3 to 5 replies, at least one typed reply per unit (avoids `RP_REPLY_NOT_PRODUCTION`). Level gates: A1 du/greetings/ordering with `sein`, `haben`, `möchten`; A2 Perfekt and separable verbs, requests; B1 Präteritum/Konjunktiv II, complaints and polite requests with Sie; B2 longer turns, register shifts, Konjunktiv I only in reported speech. Verb units must use the unit's verbs in at least one reply.
- Scenario list per level is prompt data (introductions, café order, complaint about an order, directions, hotel, doctor, phone), chosen to match the unit, not fixed in code.
- Feedback on wrong replies: `help` is required on every reply (the speaker repeats in simpler German with a hint in the edition language); item `why` per wrong option and `explanation` (already required by the item writer) cover the rest. A lint warning for a reply with no `help` is cheap to add.

### Reply checking
- mcq: wrong options come from a plausible-mistake set (Croatian/English misconceptions in `rules.ts` Misconceptions list). Typed: accepted list from the language-coach with du/Sie both allowed only when the prompt allows both; the matcher handles ae/oe/ue/ss, case, typos.
- Add a generator-side check (pure, in `authoring.ts` or a new `scenes.ts`): `say.text` and reply answers are German (target catalog), every unit vocabulary term appears in some scene of the unit at least once (threshold, not all), the verbs of a verb unit appear in a form `conjugate` accepts, no say line equals a reply's answer (the fixture changelog says "no spoken line gives its own answer away"), register consistent per scene (du vs Sie), `cefr` of scene <= course cefr (already `RP_CEFR_ABOVE_COURSE`).
- hr and en: only the instruction side differs. German lines and answers are shared; `translation`, `help`, `gloss`, titles, settings and item prompts are source-edition strings the `editions` step translates. Check that `editions` covers the new keys (it does: it takes every non-taught key).

### Bot and playtest
- No bot change expected: `scripts/bot/roleplay.mjs` reads the section generically (`sectionOf`, `maxSteps` from turn counts). Run it perfect/wrong/random on a generated German A1 course and on the changed fixture set. The playtest stage already runs the 5 personas. Add one German fixture with a roleplay section (a small scene set over `de-verbs-a1`, hr target is `de`): use it for a bot e2e (Chromium, `yarn test:e2e`).
- Wrong-mode check: help lines appear, third miss shows the reply, scene ends. Keyboard-only mode types umlauts via special-letter keys (EGS-13 changelog).

### Tests that matter (few)
1. Pure `checkScenes` / schema unit test: one golden model output passes; a table of broken outputs (dangling next, unknown speaker, unknown item, no typed reply, German text missing, unit vocab never used) each gives the right Problem. Reuse `walkScene`.
2. Assemble test: a mock-provider run of the `scenes` stage on a small German course yields a section that the validator and `lintGameData` accept with 0 `RP_*` errors, the target catalog holds the German, the edition catalog holds translations (extend `pipeline.test.ts` helpers, no Chromium).
3. PROMPT_VARS contract test (exists; needs the new entry) and the seed refresh history test (exists).
4. One e2e bot run on a German generated or fixture course (perfect + wrong), in the e2e config only.
Do not add per-code lint tests: the `broken-roleplay` fixture already covers the 14 codes; add rows only for new codes.

## Ticket split (EGS numbers to be assigned after EGS-54)
1. **EGS-39a Scene schema, checks, prompt, role.** Model output schema (`sceneSchema` for the writer: scenes, new reply items, speakers), pure `checkScenes()` (the bullets above), `scene-writer` role, agent, prompt `scene-writer/scenes.md`, `PROMPT_VARS`, roles config and seed history. Done when: unit tests (1) and (3) pass; a mock model answer round-trips; `yarn typecheck`, `yarn lint`, `yarn test` clean.
2. **EGS-39b Pipeline stage `scenes` and assemble.** Stage after `accepted` (plus `STAGE_OF`, `STAGE_FILES`, restart/resume), reuse-or-add reply items, accepted step for new typed items, garden derivation, `PIPELINE_SHELLS += roleplay`, design prompt text, assemble writes the section and catalogs (target vs edition), enables the shell, only for language formats. Done when: test (2) passes; a restart from `scenes` is idempotent; the stage is skipped for non-language courses.
3. **EGS-39c Lint additions.** New warnings: `RP_REPLY_NO_HELP`, `RP_UNIT_VOCAB_UNUSED`, scene length/turn-count bounds, say line echoes a reply answer, du/Sie mixed. Rows in `broken-roleplay` + `EXPECTED.md`. Done when: `tests/lint.test.ts` rows pass and existing fixtures still lint 0 errors.
4. **EGS-39d German fixture and bot.** A German A1 roleplay fixture (hr + en), bot perfect/wrong/random/keyboard on it, `docs/player.md`/`mcp-guide.md`/ROADMAP row. Done when: e2e bot passes in all modes with 0 console errors and axe 0 violations.
5. **EGS-39e Live run (hub).** Run `edu_run_pipeline` with the client model for A1 first (`deutsch-a1-*`), then A2 to B2 smoke; log under `runs/`. Done when: published, lint 0 errors, bot ok, run log written; the user plays it (a production is done only when played). Records German not natively reviewed.
Split 1 and 2 may merge if the repo prefers fewer tickets (the HUB-22 pattern had one ticket per stage).

## Risks
- Model-written German is not natively reviewed (HUB-22 changelog line 20): grammar errors in dialogue are likelier than in item answers. Mitigate with the verb-table check, the rules text, the fact-checker pass on scenes (not currently run on a shell section), and a human review flag.
- Reply items added late miss earlier steps (distractors, explain, accepted, fact_check). Either run those on them or write their `why`/`explanation`/accepted inside the scene-writer output and validate with the same schemas.
- Cost and time: one call per scene (about 5 to 15 calls per course); client-model jobs park and need a loop. The A1 pilot already costs minutes of bot time per persona (EGS-54, about 0.9 s per answer).
- Two languages of text: a say line in the source catalog by mistake fires `RP_TEXT_NOT_TARGET` (warning only, easy to miss). Make it a generator error.
- `isProduction` counts only typed-like replies; a model may produce all-mcq scenes (warning only).
- Existing courses: `roleplay` becomes enabled only on rerun/restart; resuming old runs must not break (stage absent in old `steps.json`).
- Shared code: `authoring.ts`, `pipeline.ts` STAGES order, `assemble.ts`, `PROMPT_VARS` are used by every course; changes to STAGES shift stage-based restart. Prompt changes reach data folders only through the seed refresh history.
- Speakers' portraits and line audio: the section allows both, and without them the shell falls back to initials and no play button. Voice for scene lines (German clips, local voices only) is a follow-up; do not couple it.

## Open questions
1. Reuse existing items, add new reply items, or both (Option A)? Needs a decision before 39a.
2. Should the fact-checker review scenes (cost) or only the code checks?
3. Roleplay on by default for every language format, or opt-in through `brief.shells`? Not read: how `brief.shells` flows into the design step beyond the notes string (`pipeline-handlers.ts:597`).
4. Scene counts above are a proposal; the user may want more at A1.
5. Not read in detail: `player/shells/roleplay/index.ts` mid-section (scene-done star thresholds, unlock rule) and `kit` mastery thresholds; the player-side numbers above come from file headers and the changelog.
6. EGS-39 needs a ROADMAP.md row in edu-game-studio (it is absent).
