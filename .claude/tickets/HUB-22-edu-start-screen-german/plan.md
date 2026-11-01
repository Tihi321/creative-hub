# HUB-22 plan: one start screen for every Edu Studio mode, and a German course (hr + en speakers, A1 to B2, with verb conjugation and graded reading)

Repo of the work: `C:\projects\Personal\edu-game-studio` (master at `6c53e22`, EGS-24 merged; next free ticket id is **EGS-25**). Paths below are relative to it unless absolute. Research: `research.md` in this folder (read it first; where this plan differs from it, this plan wins: see "Findings that change the research").

Rules every worker follows (from the repo's `AGENTS.md`): branch `EGS-NN_<what>` cut from `master`, one commit per ticket, plan in `.claude/tickets/EGS-NN-<name>/plan.md` (copy the task block from here), a row in `ROADMAP.md`, `yarn typecheck && yarn lint && yarn test` green (Node via `fnm exec --using=24 yarn ...`), every interactive element has a `data-testid`, public repo (no keys, no `~/EduGames` content, no personal paths), tests use the mock provider and fakes, nothing spends money. Do not commit or push unless asked. Scratch files under `.claude/temp/`.

## Scope

One line per reading, as the global rules ask.

- Start screen: **the title screen and the mode picker only**. One shared component in one style (a new `menu` theme) for all six shells; each shell keeps its own theme in every in-game screen. Quiz arena's private copy of the title screen is deleted and uses the shared component. The modes stay (they are the feature); the picker becomes a card grid of modes.
- German: **one course for Croatian speakers and English speakers** (editions `hr` and `en`, taught language `de`), levels **A1, A2, B1 and B2**. A1 to B1 are interactive and played in the shells the pipeline already enables (quiz arena, encyclopedia, MindMaze, RPG). **B2 is book-like**: graded long-form reading in a reader view of the encyclopedia shell with tap-to-gloss vocabulary and per-text glossaries, comprehension and grammar items on the texts, vocabulary SRS harvested from the texts, optional German listening passages (see "B2 design"). Voices are real (listening clips in German), not export-only.
- Verbs: a new item kind **`conjugation`** (verb x person x tense table, typed answers) plus **verb-focused units** and a **verb drill round with spaced repetition**, plus a deterministic German paradigm table that the lint uses to catch wrong forms the model wrote.
- Must-haves: German grammar rules in the writer prompts; umlaut / ss / capitalisation matching; German voice check and allocation; German UI strings.
- The en edition is made inside the pipeline (a translation step with the client model), so one pipeline run yields both editions.

## Out of scope (and why)

- **C1 and C2, and any auto-grading of free writing or free speaking.** B2 is IN scope, designed around what the system can check deterministically ("B2 design"). Free writing and speaking at B2 exist only as a **self-check with a model answer** (a flashcard; the learner compares and grades themselves); there is no scorer and no native reviewer, so nothing is auto-graded. C1 and C2 stay out: they need unabridged authentic texts and a native reviewer for register and idiom, and the verb and grammar tables stop at B2.
- **Role-play scene generator** (no role writes `roleplay` scenes, `authoring.ts:653-659`): not built in HUB-22. It is recorded as an open follow-up roadmap item (EGS-39 in the Edu Studio `ROADMAP.md`, HUB-23 in the hub `ROADMAP.md`), planned after these tickets (see "Hub changes").
- Pronunciation scoring (ROADMAP "Later"); speaking stays "speech becomes the typed answer".
- German-speaking learners (a `de` edition of the UI is added for strings completeness in EGS-34, but no course is built for German speakers).
- Changing the in-game look of any shell, a course-level theme setting in the Game tab, and the "Later" items of the ROADMAP.
- Native-speaker review of the model-written German content and tables: not available; the plan adds mechanical checks instead (EGS-28) and says so in the live check.

## Findings that change the research (verified in code)

1. **hr + en editions of one German course are supported by the data model.** `coursePackSchema` has `languages: [hr, en]` and `targetLang: de`; `makeTextResolver(catalogs, lang, targetLang)` (`src/shared/edu/text.ts:24`) looks a key up in the edition catalog first and then in the **target-language catalog** (`text/de.json`), and `validateCourse` requires a catalog for every edition plus the target (`validate.ts:72-74`). Taught phrases (items with `taught: true`) therefore live once in `de.json` and prompts, explanations, hints and whys live per edition (`assemble.ts:15-24`). **What is missing is the pipeline**: `assembleCourse` writes `languages: [sourceLang]` only (`assemble.ts:210`) and the step `editions` is skipped (`pipeline.ts:464`, "come from Book Translator later"). EGS-32 closes that.
2. **`match.ts` already folds `ß -> ss`** (`foldDiacritics`, `match.ts:50-66`) **and strips umlauts (ä -> a) like any accent**. So today: "Madchen" for "Mädchen" is accepted silently (policy `ignore`), which is wrong in German (Bruder / Brüder, schon / schön are different words); "Maedchen" is only a distance-1 *typo* under `ignore` and a miss under `strict`. And a typo (distance 1) is accepted for words of 4+ letters, so "seid" is accepted for "sein" and "geht" for "gehe": fatal for a conjugation drill. EGS-26 and EGS-27 fix both.
3. **Player strings:** Croatian exists (`src/player/i18n.ts`, table `HR`, `TABLES = { hr: HR }` at :326; shell strings have `en` + `hr`, `src/player/kit/strings.ts:8`); German letters for the on-screen letter buttons **already exist** (`SPECIAL_LETTERS.de`, `i18n.ts:344`). Only the `de` UI table is missing.
4. **Check context is built in six places** (`session.ts:172,232`, `quiz-arena.ts:131,167`, `lint.ts:159`, `live/questions.ts:75`) plus the bot. A new matching input must go through one helper (EGS-26) or the six drift.
5. **Quiz arena does not extend `ShellSession`** (it is its own class, `quiz-arena.ts:84`, own `mount()` that sets the theme at ~:147 and its own `title` markup at ~:387-420), so "use the shared title" needs a small host interface, not a call to `titleScreen(session, ...)`.
6. EGS-18 appears twice in `ROADMAP.md` (placeholder "editions" in Phase 7 and the done "speaking practice"). The editions placeholder is therefore not a ticket anyone can pick up; EGS-32 here replaces it. Update that row.

## Files and modules to touch (by ticket)

### EGS-25 shared start screen
- `src/player/kit/screens.ts:34-48` `shellPicker`, `:61-216` `titleScreen` (becomes a thin wrapper that calls the new component; keep the export so shells compile until they are moved).
- NEW `src/player/kit/start.ts` (the component), NEW `src/player/kit/mode-icons.ts` (one inline-SVG pictogram per shell id: quiz-arena, encyclopedia, mindmaze, rpg, roleplay, detective).
- `src/player/kit/kit.css:7-21` (picker styles move to a mode-card grid), `src/player/kit/index.ts` (exports).
- `src/player/kit/session.ts:176-182` `mount`, `:498` `render` (theme per screen), `:172,:232` untouched here.
- `src/player/shells/quiz-arena.ts` constructor/`mount` ~:131-150 and the title markup ~:387-420 (delete it; call the component through a `StartHost` adapter); `src/player/style/arena.css:109-130` (remove title-specific rules).
- Shell title callers: `rpg/index.ts:348`, `mindmaze/index.ts:231`, `roleplay/index.ts:310`, `detective/index.ts:261`, `encyclopedia/app.ts:279` (pass options to the component; drop `art`/`tagline` options, see contract).
- `src/design/themes/index.ts` (register theme `menu`; `ThemeInfo.shell = 'menu'`), NEW `src/design/themes/menu.css`, `src/design/tokens.css` only if a slot is missing (do not add slots).
- Theme dressing that hit the old title: `.title-screen` / `.eyebrow` rules in `chalkboard.css:134`, `parchment.css:79`, `postcard.css:123`, `castle.css:116`, `noir.css:105` (remove the title-only ones; in-game rules stay).
- `src/player/engine.ts:84` (error screen keeps `chalkboard`), `src/player/i18n.ts` (keys `start.*`, `mode.<id>.name|blurb`), `src/player/kit/strings.ts` consumers (per-shell `shell.<id>` names move to the common table).
- Tests: `tests/player-shell-kit.test.ts`, `tests/player-shell-picker.e2e.test.ts`, `tests/design-tokens.test.ts` (iterates the registry, so `menu` is contrast-checked automatically; confirm), `tests/themes-load.test.ts`, bot title steps in `scripts/bot/*.mjs`, `scripts/play.mjs`, `scripts/theme-previews.mjs`, `docs/player.md`, `docs/design.md` (Look: add the `menu` row, state the rule "title and mode picker use `menu`, play uses the shell's theme").

### EGS-26 German-aware matching
- `src/shared/edu/match.ts`: `MatchOptions` (:25), `MatchResult` (:33), `matchAnswer` (:105), `resolveDiacritics` (:151).
- `src/shared/edu/registry.ts:13` `CheckContext` (+ `lang`), NEW helper `makeCheckContext(pack, text, targetLang)` in `src/shared/edu/index.ts`; replace the six hand-built contexts (list in finding 4).
- `src/shared/edu/checkers.ts:75` `textResult` (pass `lang`, carry the new flags into `CheckResult`), `checkTyped:87`, `checkCloze:92`, `checkListening:178`.
- `src/player/feedback.ts` (notes for `translit` and `caps`), `src/player/i18n.ts` (keys `fb.note.translit`, `fb.note.caps`, `fb.note.umlaut`), `docs/player.md` / `docs/design.md` (matching policy paragraph).
- Tests: `tests/edu-match.test.ts` (extend), `tests/edu-checkers.test.ts`.

### EGS-27 conjugation item kind
- `src/shared/course.ts:~246` (add `conjugationSchema`, add to `itemKindsBuiltin` :34-48 and `builtinItemSchema` :~215), `src/shared/edu/kinds.ts` (a `def({kind:'conjugation', ...})` next to `cloze`), `src/shared/edu/checkers.ts` (`checkConjugation`), `src/shared/edu/registry.ts` (nothing, unless `ItemKindDef` needs `drill`), `src/shared/schemas.ts:155` `AUTHORED_ITEM_KINDS` (+ `conjugation`).
- Authoring: `src/engine/edu/authoring.ts:~399-416` (`conjugationItem` zod + add to `authoredItemSchema`), `src/engine/edu/assemble.ts` (item to pack + catalog keys; default pronoun labels), `src/engine/edu/pipeline-handlers.ts:~100-115` (`renderItemForReview` case), `src/engine/mcp/tools-course.ts` (`edu_item_add` shape + description), `docs/mcp-guide.md`.
- Lint: `src/engine/edu/lint.ts` (kind-specific problems through `validate` of the kind def; new codes below), `lint.ts:~62-78` code list.
- Player: NEW `src/player/items/conjugation.ts`, register in `src/player/items/index.ts`; `src/player/feedback.ts:55-150` (per-person marking, `fb.detail.forms`), `src/player/debug.ts:46` (bot solver exposure), `src/player/round.ts:214-228` (`gradeOf`, `timerApplies`).
- Bot: `scripts/play.mjs:438,511,554` (perfect / wrong / random answers for the new kind), `scripts/bot/generic.mjs`.
- Studio editor: `src/renderer/ui/course/ItemEditor.tsx:~303` (a form editor), `src/renderer/lib/items.ts`.
- Live quiz: `src/shared/live/questions.ts` (explicitly **excluded** from live questions; add a test that it is skipped, not crashed).
- Fixture + tests: NEW `tests/fixtures/courses/de-verbs-a1/` (hr + en editions, `targetLang: de`), `tests/edu-checkers.test.ts`, `tests/edu-lint.test.ts`, `tests/edu-authoring.test.ts`, `tests/bot.e2e.test.ts` (new fixture runs perfect / wrong / random), `tests/edu-course.test.ts`.

### EGS-28 German verb paradigm table
- NEW `src/shared/lang/de/verbs.ts` (data + `conjugate`, pure, bundled nowhere in the player unless EGS-31 needs it), NEW `src/shared/lang/de/pronouns.ts`, NEW `src/shared/lang/index.ts` (language-rule registry: `rulesFor(lang)`), lint hook in `src/engine/edu/lint.ts` (only calls the table when `pack.targetLang === 'de'`), tests `tests/de-verbs.test.ts`, `tests/edu-lint.test.ts`.

### EGS-29 formats A1/A2/B1, brief, verb units
- `seed/config/formats.md:31-41` (edit `language-a1`; add `language-a2`, `language-b1`), `src/shared/brief.ts:80` (default format from `cefr`: `language-<cefr lower>` when present), `src/shared/brief.ts:18` (fix the stale "only quiz-arena" comment), `src/shared/schemas.ts:155-173` (format schema: new optional `verb_units`, `verbs_per_unit`), `src/engine/edu/pipeline-handlers.ts:271` (curriculum + scope pass the verb-unit info), `seed/prompts/curriculum-designer/*.md`, `seed/prompts/language-coach/scope.md`, `src/engine/edu/assemble.ts` (write `pack.extensions.language = { verbUnits: [unitId], verbsPerUnit }`), docs `docs/mcp-guide.md`, tests `tests/edu-formats.test.ts` (new or existing), `tests/edu-brief.test.ts`.
- Seed sync gotcha: seeds are copied to `~/EduGames` only when absent (ROADMAP "Later": "Starter agents ... not copied when `~/EduGames/agents` already exists"). The worker must find out how `config/formats.md` and `prompts/` reach an existing data folder and either fix it (copy missing files without overwriting, warn about changed ones) or document the manual step, because the live check depends on it.

### EGS-30 German grammar rules in the writer prompts
- `seed/prompts/language-coach/scope.md`, `language-coach/accepted.md`, `seed/prompts/item-writer/items.md` (the `conjugation` shape, German rules), `seed/prompts/misconception-designer/*.md` (German misconceptions list), `seed/prompts/explainer/*.md`, `seed/prompts/fact-checker/*.md` (language items: what counts as a source), `seed/agents/language-coach-ines-markovic.md`, new shared include or a `seed/config/language-rules/de.md` loaded into the prompt variable `{{language_rules}}`: add the variable in `authoring.ts:745-760` (the allowed-variables table) and fill it in `pipeline-handlers.ts:271,346,459,513` from `src/shared/lang/index.ts` (`rulesFor(targetLang).promptRules`, empty string for languages without rules). Tests `tests/edu-authoring.test.ts` (prompt renders with the rules, unknown variable check still passes).

### EGS-31 verb drill round (spaced repetition)
- `src/player/round.ts:79-143` (`startPool`/`startRound`: new `RoundKind` `'verbs'`), `:151-186` `pickNext` (due-first order), `src/player/shells/quiz-arena.ts` map screen ~:560-600 and `:586` (button `verb-drill`), `src/shared/edu/srs.ts` (no change expected; `dueCards` is used), `src/player/progress.ts` (nothing unless per-person weakness is stored), `src/player/i18n.ts` keys, `tests/player-round.test.ts` (or the existing round test file), `tests/bot.e2e.test.ts`.

### EGS-32 editions step (hr + en from one run)
- `src/engine/edu/pipeline.ts:42,464` (the `editions` step becomes real: depends on `assemble`, runs before `build`), `src/engine/edu/pipeline-handlers.ts` (handler `editions`), `src/engine/edu/assemble.ts:210` (`languages: [sourceLang, ...editions]`), `src/shared/edu/validate.ts:72-74` (unchanged, used as the check), NEW prompt `seed/prompts/translator/edition.md` and role/agent `translator` in `seed/agents` + `seed/config/roles.md`, `src/engine/edu/authoring.ts:745-760` (variables), `src/shared/brief.ts:16` (comment), `docs/mcp-guide.md`, `docs/design.md` Architecture line "other editions come from Book Translator later".
- Tests: `tests/edu-pipeline*.test.ts` (mock provider: a course with `languages: [hr, en]`, `targetLang: de` yields three catalogs, validate and lint clean), `tests/edu-lint.test.ts` (an edition missing a key is `TEXT_MISSING (in en)`).

### EGS-33 German voices
- `src/engine/voice/allocate.ts:8-12,38` (comments say "Croatian"; order rule stays, see contract), `src/engine/voice/catalog.ts:113` (`voiceLangsOf` includes `targetLang`), `src/engine/edu/voice.ts:87-258` (taught phrases are spoken in the target language; style `fallbackStyle`), `seed/prompts/voice-director/plan.md`, `seed/config/voice.md` (a `de` line; `localVoices.de`), `src/engine/mcp/tools-voice*.ts` (`edu_voice_status` reports `de` readiness per provider), `docs/mcp-guide.md` (Voice), tests `tests/voice-allocate.test.ts`, `tests/voice-plan.test.ts`.

### EGS-34 German UI strings (and the new keys in hr and en)
- `src/player/i18n.ts` (add table `DE`, `TABLES = { hr, de }`, `UI_LANGUAGES`), `src/player/kit/strings.ts` consumers: every `src/player/shells/*/strings.ts` gets a `de` table, `src/shared/ui-strings.ts` (add `de`), `seed/config/languages.md:~7` text, test `tests/player-i18n.test.ts` (every `UiKey` and every shell key has an `hr` and a `de` entry; no key missing).

### EGS-35 reader, glossary, passage items (B2)
- `src/shared/shells/encyclopedia.ts` (schema, lint), `src/player/shells/encyclopedia/{view-article.ts,app.ts,articles.ts,data.ts,strings.ts,encyclopedia.css}`, NEW `view-reader.ts`, `src/player/items/common.ts` (passage panel), `src/player/progress.ts`, `src/player/i18n.ts`, `scripts/bot/encyclopedia.mjs`, `tests/encyclopedia-lint.test.ts`, `tests/bot-encyclopedia.e2e.test.ts`, NEW fixture `tests/fixtures/courses/de-b2-reading/`.

### EGS-36 B2 format, readings, harvest, self-check
- `seed/config/formats.md`, `src/shared/schemas.ts:155-173` (format fields), `src/shared/brief.ts`, NEW `seed/prompts/subject-expert/reading.md`, `seed/prompts/item-writer/items.md`, `src/engine/edu/authoring.ts` (authored `passage`, tags), `src/engine/edu/assemble.ts`, `src/engine/edu/pipeline.ts:42` (step `harvest`), `pipeline-handlers.ts`, `lint.ts`, NEW `seed/config/language-rules/de-b2.md`, tests `edu-brief`, `edu-pipeline*`, `edu-lint`.

### EGS-37 B2 grammar
- NEW `src/shared/lang/de/grammar.ts`; `src/shared/lang/de/verbs.ts` (tenses); `lint.ts`; `seed/config/language-rules/de.md`; tests `tests/de-grammar.test.ts`, `tests/de-verbs.test.ts`.

### EGS-38 listening passages (optional)
- `src/engine/edu/voice.ts`, `voice-service.ts`, `src/shared/media.ts` (voice settings), `seed/prompts/voice-director/plan.md`, `view-reader.ts`, `tests/voice-plan.test.ts`.

## Tasks for workers

Order and parallelism are in the next section. All tickets are `EGS-NN`; "contract" is what other tickets code against, so a worker may start before the other ticket merges.

### EGS-25 Shared start screen (title + mode picker)
- **Inputs:** this section; `research.md` section "1. Start screen"; decision 1 (start screen only; modes are good).
- **Do:**
  1. New theme `menu` (`src/design/themes/menu.css`, registry entry `{ id: 'menu', shell: 'menu', ... }`): fills **every** `--edu-*` slot, bundled fonts only (reuse Young Serif + Atkinson Hyperlegible Next, already bundled: no bundle growth), AA contrast (the registry-driven contrast test must pass), motion behind `prefers-reduced-motion` using the existing motion tokens. Direction: a calm "game lobby" that none of the six shells already looks like (so no mode appears to be the default); invoke the `frontend-design` skill for it. Mode identity comes from each card's pictogram and one accent dot, not from re-theming the page.
  2. New `startScreen(host: StartHost, opts: StartOptions, redraw, state)` in `kit/start.ts`. `StartHost` is a small interface (`pack`, `ui`, `shellId`, `shells`, `switchShell`, `courseTitle()`, `unitTitle()`, classroom host, `store.persistent`, `started`, `progress`, lang switch, sound/speak setting builders). `ShellSession` and `QuizArena` both implement it (quiz arena through an adapter object; do not make it extend `ShellSession`).
  3. Layout, same for every shell: header (course title h1, subject, audience), language picker, **mode cards** (`role="group"`, one `button` per playable shell: pictogram, name, one-line blurb, `aria-pressed` on the current one), then settings, the big **Start** button, export / import / reset, messages. The eyebrow line is the current mode's blurb (the per-shell tagline option goes away). A shell's `art` option on the title is dropped (it was part of the mixed look); a shell may show its art on its first in-game screen, not on the title.
  4. Theme per screen: `ShellSession.render(screen, ...)` (`session.ts:498`) and the quiz arena's render set `data-edu-theme` to `menu` when `screen === 'title'` and to the shell's theme otherwise, through one exported helper `applyScreenTheme(root, screen, shellTheme)`. `mount()` must not leave the previous shell's theme on the root while the title shows (no flash on `switchShell`).
  5. Delete the quiz arena's own title markup and the title-only theme CSS (list above); keep the quiz-specific "timed questions" toggle as `opts.settings`.
  6. Keep every existing testid: `course-title`, `course-subject`, `lang-picker`, `lang-<code>`, `shell-picker`, `shell-<id>`, `setting-sound`, `start`, `export`, `import`, `import-file`, `reset`, `reset-confirm`, `reset-cancel`, `title-message`, `storage-warning`. New: `mode-card-<id>` is NOT added; the card IS `shell-<id>` so the bot and tests are unchanged. A course with one shell shows no cards (as now: `shellPicker` returns null for fewer than 2).
  7. New UI keys (en + hr; de comes in EGS-34): `start.choose`, `mode.<id>.name`, `mode.<id>.blurb` for the six shells.
- **Outputs:** `kit/start.ts`, `kit/mode-icons.ts`, `menu.css`, deletions, tests, docs, ROADMAP row, changelog.
- **Contract with others:** `StartOptions.settings?: Child` (extra checkboxes); `applyScreenTheme(root, screen, themeId)` exported from `kit/index.ts`; testids above are frozen (the bot in EGS-27/31 and the live check rely on them); the `data-edu-theme` of `#edu-root` is `menu` on the title screen and the shell's theme everywhere else.

### EGS-26 German-aware matching (umlaut, ss, capitals) and one check-context helper
- **Inputs:** `match.ts` policy comment (lines 1-23), research open question "does match.ts fold ä/ö/ü/ß" (answer: it folds all of them as plain accents; see Finding 2).
- **Proposed rules** (language `de` only, selected by `MatchOptions.lang`, which is the language of the *answer text*: `pack.targetLang` for taught items, else the edition language). Order of evaluation, first hit wins:
  1. **Exact** (normalised, case-insensitive, accents kept): correct.
  2. **Transliteration**: the input equals one of three alternate spellings of an accepted answer: all of ä/ö/ü/ß written as ae/oe/ue/ss; only ß written ss; only ä/ö/ü written ae/oe/ue. Result: **correct, `translit: true`**, note "Accepted. The umlaut is written ä / ö / ü and ß; ae / oe / ue / ss is the keyboard spelling." The input is never converted back (ae -> ä would break words like "Aerosol"); the *accepted* side is expanded. Never costs a grade step.
  3. **Missing umlaut** (input equals the accepted answer only after folding ä->a, ö->o, ü->u): **wrong**, `diacritics: true`, note "Almost: check the umlaut" (default for `de` = `strict`, because Bruder / Brüder, schon / schön, Mutter / Mütter differ in meaning). An item with `strictDiacritics: false` still gets the lenient `ignore`. Implemented by `resolveDiacritics(itemStrict, courseDefault, lang)` returning `strict` for `de` when the item says nothing and the course default is `ignore`; a course default of `warn` or `strict` wins.
  4. **Capitalisation** (German nouns): if the accepted answer has a capitalised token that is not its first token (or the answer is a single capitalised token) and the input has it in lower case, **correct, `caps: true`**, note "Accepted. German nouns start with a capital letter." First tokens of multi-word answers are ignored (sentence start is ambiguous).
  5. Typos as today (distance 1, 4+ letters), but **never for conjugation forms** (EGS-27 passes `typos: false`).
  Other languages: unchanged behaviour (no `lang`, or `lang !== 'de'`).
- **Do:** implement in `match.ts` (pure, no node), add `translit` and `caps` to `MatchResult` and `CheckResult`; add `lang` to `MatchOptions` and `CheckContext`; add `makeCheckContext({ pack, text, targetLang })` and replace the six hand-built contexts and the bot's; feedback notes; docs.
- **Outputs:** code, tests (table-driven: Mädchen / Maedchen / Madchen / mädchen, Straße / Strasse / Strase, Bruder vs Brüder, Feuer typed Feuer, Haus / haus, sentence "Ich heiße Anna" / "ich heisse anna", typo still accepted for "Wasser"), docs.
- **Contract:** `matchAnswer(input, accepted, { lang?: string, diacritics?, typos?, minTypoLength? }): MatchResult & { translit?: boolean, caps?: boolean }`; `CheckContext.lang?: string`; `CheckResult.translit?/caps?`; `makeCheckContext` from `src/shared/edu/index.ts`. EGS-27 builds on these names.

### EGS-27 `conjugation` item kind
- **Inputs:** EGS-26 contract; decision 3.
- **Schema** (`course.ts`, strict, in the pack; all strings are catalog keys):
  ```
  kind: 'conjugation'
  ...itemBaseShape                      // id, objective, prompt, explanation, hint?, difficulty, tags, extensions
  verb: keySchema                       // the infinitive, shown ("gehen"); taught catalog when taught
  tense: idSchema                       // metadata: 'praesens' | 'perfekt' | 'praeteritum' | 'futur1' | 'imperativ' | 'konjunktiv2' (free id for other languages)
  forms: [{ person: idSchema,           // 'ich','du','er','wir','ihr','sie','Sie' for de; any id for other languages
            label: keySchema,           // pronoun shown beside the input ("er / sie / es"); assemble fills it for de
            answer: keySchema,          // accepted list per language, first = canonical, WITHOUT the pronoun (see rules)
            given: boolean = false }]   // shown filled in, not asked
         .min(2).max(7)
  ask: int >= 1 optional               // how many of the non-given forms are asked per presentation (a drill); missing = all
  strictDiacritics: boolean optional
  ```
  Catalog keys (assemble): `item.<id>.verb`, `item.<id>.form.<person>` (strings + `accepted`), `item.<id>.form.<person>.label`; with `taught: true` the verb, forms and labels go to the target-language catalog, prompt / explanation / hint / why stay in the edition catalogs.
- **Answer shape** `{ [person]: string }` for the asked persons only. **Check** = per form `matchAnswer` with `typos: false`, `lang` from the context, policy from EGS-26; `score = right / asked`, `correct` only when all asked forms are right, `detail = { [person]: boolean }`, `expected = { [person]: canonical }` (all forms, so feedback can show the full table), `partial` when some are right; `translit`/`caps` true if any form used them.
- **Writing rules** (also in the EGS-30 prompts): the answer is the verb form without the pronoun ("gehe"); compound tenses and separable verbs include every word the learner types ("bin gegangen", "werde gehen", "würde gehen", "stehe auf"); imperativ persons are only `du`, `ihr`, `Sie` (`Sie` form includes the pronoun: "gehen Sie"); `er` covers er / sie / es, `sie` is the plural, `Sie` the formal; alternate correct forms go in `accepted` (du: "arbeitest"; Präteritum "wurde"; imperative du: "Geh", "Gehe"); an irregular verb must show at least one irregular form asked.
- **Grade:** `gradeOf` (`round.ts:214`): all right -> `good` (the `translit` / `caps` notes never cost a grade, EGS-26; `gradeOf` must not treat them like `typo`); some right (score >= 0.5) -> `hard`; else `again`. `timerApplies`: false (typing).
- **Lint codes (errors unless noted):** `CONJ_PERSON_DUPLICATE`, `CONJ_ASK_TOO_MANY` (`ask` > asked forms), `CONJ_IMPERATIVE_PERSON` (tense `imperativ` with a person outside du / ihr / Sie, only when `targetLang` is `de`), `CONJ_FORM_DUPLICATE_AMBIGUOUS` (two persons with the same canonical form in an item that asks both without a `given`: allowed, but **warning** because the learner cannot tell them apart: wir/sie/Sie in Präsens). EGS-28 adds `CONJ_FORM_MISMATCH` and `CONJ_VERB_UNKNOWN` to the same list.
- **Player:** `items/conjugation.ts`: the verb as a heading, the tense as a badge, one labelled input per asked form in a table (given forms are read-only rows), on-screen letter buttons ä ö ü ß (`SPECIAL_LETTERS`), speech button on each input if speaking is on (`speak.ts`), `Check` button; feedback marks each person, shows the full table afterwards (right forms in the table, wrong ones with the expected form). Testids: `conj-<person>` (input), `conj-<person>-result`, `check`. Keyboard: Enter in an input moves to the next, Enter on the last submits.
- **Other consumers (each must handle or explicitly skip):** studio ItemEditor (a table editor), `edu_item_add` shape, `renderItemForReview` (fact-checker sees `verb/tense/forms`), bot (`play.mjs` perfect = canonical forms, wrong = reversed forms, random = random persons right), live quiz (skip, tested), crossword / word search builders do not take it.
- **Outputs:** code, fixture `de-verbs-a1` (editions hr + en, `de.json` target; one unit "Verben", items for sein, haben, gehen, machen in Präsens; a Perfekt item; an Imperativ item; one with `ask: 3`; one `given` form), tests, docs (`docs/player.md` item table, `docs/mcp-guide.md`), ROADMAP row.
- **Contract:** the schema above is final; EGS-28 / 30 / 31 / 32 / 34 code against it. Pack extension used by 29 / 31: `pack.extensions.language = { verbUnits: string[], verbsPerUnit?: number }`.

### EGS-28 German verb paradigm table and form lint
- **Inputs:** EGS-27 schema (the lint hook is wired after 27 merges; the data module has no dependency).
- **Do:** `src/shared/lang/de/verbs.ts`: `interface DeVerb { inf; aux: 'haben'|'sein'; partizip2; praet3: string; presOverrides?: { du?; er? }; sep?: string; modal?: boolean; reflexive?: boolean; level: 'A1'|'A2'|'B1' }`, `findVerb(inf)`, `conjugate(verb, tense, person): string[]` (accepted forms, compound tenses spelled out, separable prefix at the end, Konjunktiv II as `würde + inf` for all verbs plus the special forms of sein, haben, werden, the modals, gehen, kommen), `tenseForCefr`. At least **120 verbs**: every verb a learner meets at A1 (sein, haben, werden, the six modals, ~25 everyday), A2 (separable and reflexive verbs, Perfekt with sein, Präteritum of sein / haben / modals) and B1 (Präteritum of the common strong verbs, Konjunktiv II). `pronouns.ts`: `PRONOUN_LABELS.de` (`er` -> "er / sie / es" ...). `src/shared/lang/index.ts`: `rulesFor(lang): { promptRules: string; verbTable?: ...; matching?: ... } | undefined`, registered for `de`; `promptRules` is the German rules text EGS-30 loads.
  Lint (`lint.ts`, only when `pack.targetLang === 'de'` and the item is a conjugation item): `CONJ_FORM_MISMATCH` (**error**) when the verb is in the table and an item's canonical form is not one of `conjugate()`'s forms for that person and tense; `CONJ_VERB_UNKNOWN` (**warning**, "not in the verb table, check the forms by hand"); `CONJ_TENSE_LEVEL` (**warning**) when the tense is above the course CEFR (Konjunktiv II or Futur in an A1 course, Präteritum of a non-modal strong verb below B1).
- **Honesty:** the table is model-written and not natively reviewed; its tests are spot checks (>= 40 verb x tense x person golden forms I can verify by rule: regular -en verbs, stem -t/-d verbs with -est/-et, -s/-ß/-z stems with `du gehst/reist`, e/i changes, a/ä changes, sein / haben / werden, modals, separable, sein-Perfekt) plus invariants (regular verbs equal what the rule generator gives; every `partizip2` of a separable verb contains `ge` in the right place). The changelog says so.
- **Outputs:** data, functions, lint codes, tests, docs. **Contract:** `findVerb`, `conjugate`, `rulesFor('de')`, `PRONOUN_LABELS` as above; 27's assemble uses `PRONOUN_LABELS`, 30 uses `rulesFor(...).promptRules`.

### EGS-29 Formats A1 / A2 / B1, brief defaults, verb-focused units
- **Inputs:** `seed/config/formats.md` (current `language-a1`), `brief.ts:80`, decision 2 and 3.
- **Formats** (all `language: true`, kinds exclude hotspot / crossword / word-search as today):
  | id | cefr | units | objectives / unit | items / objective | articles / unit | research q / unit | verb units | kinds |
  |---|---|---|---|---|---|---|---|---|
  | `language-a1` (edit) | A1 | 4 | 3 | 3 | 1 | 1 | 1 | mcq, cloze, typed, match-pairs, flashcard, sort-groups, **conjugation** |
  | `language-a2` (new) | A2 | 5 | 3 | 4 | 1 | 1 | 2 | the A1 kinds + true-false, order, multi-select |
  | `language-b1` (new) | B1 | 6 | 3 | 4 | 2 | 2 | 2 | all of A2; articles are short reading texts (B1 reading comprehension = article + items that cite it) |
  `verb_units` / `verbs_per_unit` are new optional format fields (default 0): the number of units that are **verb units** (a unit whose objectives are all about one verb group: A1 sein / haben / regular Präsens / modals; A2 Perfekt, separable, reflexive, Präteritum of sein / haben / modals; B1 Präteritum, Konjunktiv II, Futur I) and verbs per verb unit (default 6). Item mix inside a verb unit: at least 40 % `conjugation`, the rest cloze (verb in a sentence), typed, mcq, sort-groups (regular / irregular, haben / sein).
- **Brief:** `resolveBrief` chooses `language-<cefr>` when `cefr` is given and `targetLang` is set and no `format` (A1 stays the default for `targetLang` alone); B2 selects `language-b2` once EGS-36 has merged (until then it fails with "no format for B2 yet"); C1 and C2 without a format fail with "out of scope (HUB-22)". `brief.cefr` already exists.
- **Curriculum:** the curriculum-designer prompt receives `verb_units` and must mark that many units as verb units (a convention in the unit title and objectives; the assembled pack gets `extensions.language.verbUnits`). `language-coach/scope` returns, for a verb unit, `verbs: [{ inf, tense, level }]` (instead of / besides `vocabulary`) and the item-writer receives them in `{{scope}}`.
- **Outputs:** formats, schema, brief, prompts for curriculum / scope (the German rules text is EGS-30), seed-sync fix or documented step, tests (`resolveBrief` per CEFR; a mock-provider pipeline run on `language-a2` gives verb units in `extensions.language`), docs, ROADMAP row.
- **Contract:** format ids `language-a1|a2|b1`; `FormatEntry.verb_units`, `.verbs_per_unit`; `pack.extensions.language.verbUnits: string[]` (unit ids).

### EGS-30 German grammar rules in the writer prompts
- **Inputs:** `rulesFor('de').promptRules` slot (EGS-28; until it merges write the text in `seed/config/language-rules/de.md` and let EGS-28 read it, or the reverse: whichever lands first owns the file, the other imports; the worker records the choice in the changelog).
- **The rules text** (concise, imperative, at most about 60 lines; the roles get it as `{{language_rules}}` when `targetLang` is `de`, empty otherwise):
  - **Gender and articles:** every noun is taught with its article and gender (der / die / das), in the base form and in the plural ("das Haus, die Häuser"); the article is part of the accepted answer for a noun item and is asked on its own in a sort-groups (der / die / das) item; never teach a noun without its article; indefinite article only after the definite one is known (A1 unit 2 onwards).
  - **Plural:** the plural form is taught with the noun; typed plural items accept only the right plural, with umlaut (the matcher is strict about it).
  - **Cases:** A1 nominative and accusative of the definite / indefinite articles and the personal pronouns (ich / mich / mir only as phrases), A2 dative after mit / bei / zu and the two-way prepositions in or an stated rule by rule, B1 genitive only as fixed phrases (wegen, trotz) and relative pronouns; never teach a case that is above the level.
  - **Verbs:** conjugation items per the EGS-27 writing rules; verb position (second place in the main clause, at the end after a conjunction `weil`, `dass`, `ob`; separable prefix at the end; Perfekt as auxiliary + participle at the end); stem-changing verbs flagged `irregular` in `tags`; reflexive verbs from A2; modal verb + infinitive from A1.
  - **Word order and sentences:** cloze and order items; `order` items for sentence building (words in the correct order) are encouraged from A2 (verb second, time-manner-place at B1).
  - **Spelling:** write ä ö ü ß exactly (never ae / oe / ue / ss in canonical answers; those are alternates the matcher accepts); nouns capitalised; `ß` after long vowels and diphthongs, `ss` after short vowels (Swiss "ss" is only an alternate); numbers and times as the level needs.
  - **Register:** `du` for peers / children and `Sie` for strangers: every dialogue-style item says which; do not mix inside one item.
  - **Accepted answers (language-coach/accepted):** synonyms and optional words (pronoun drop is NOT optional in German except imperatives), both `Sie` / `du` only if the prompt allows it; never add a wrong case or gender as an alternative.
  - **Misconceptions (misconception-designer):** a list of the typical mistakes of Croatian speakers (no articles in Croatian; word order; sein / haben in Perfekt; der / die / das by natural gender; `du` / `Sie`) and of English speakers (verb second; capitals; false friends: *bekommen* = get; plural forms; `ich bin kalt`), used to write the `why` of each wrong choice.
  - **Facts / sources:** grammar facts name their source (Duden, Wiktionary page, a CEFR vocabulary list such as Goethe-Institut Wortliste for the level) in the fact's `source` field; the fact-checker checks forms against them and, for conjugation items, against the lint's verb table result (a `CONJ_FORM_MISMATCH` is a fail).
- **Do:** write the rules, add the `{{language_rules}}` variable to the allowed variables (`authoring.ts:745-760`) and fill it in the four handlers, add the `conjugation` shape to `item-writer/items.md` and the review renderer, extend `language-coach/scope` and `accepted` prompts with the rules and the verb scope, extend the fact-checker / misconception / explainer prompts to mention the rules.
- **Outputs:** prompts, variables, tests (rendered prompt for `targetLang: de` contains the rules and the `conjugation` shape; for `targetLang: hr` contains neither; prompt-variable test still passes), docs.
- **Contract:** `{{language_rules}}`; authored `conjugation` item shape (item-writer output, one JSON object): `{ "kind": "conjugation", "id", "objective", "taught": true, "verb": "gehen", "tense": "praesens", "prompt", "explanation", "facts": ["f3"], "forms": [{ "person": "ich", "accepted": ["gehe"] }, { "person": "du", "accepted": ["gehst"] }], "given": ["wir"]?, "ask": 3? }`; `authoring.ts` turns it into the pack shape of EGS-27.

### EGS-31 Verb drill round with spaced repetition
- **Inputs:** EGS-27 (kind), EGS-29 (`extensions.language.verbUnits`), `srs.ts` (SM-2 per item, `dueCards`), `round.ts`.
- **Do:** a new round kind `'verbs'`: the pool is every `conjugation` item of the verb units that is **due** (`dueCards`) first, then new ones, then the weakest (lowest ease), at most `DEFAULT_ROUND_LENGTH`; for an item with `ask`, which persons are asked is chosen by the seeded rng (`rngFor`) with a bias to persons missed before (kept in `progress` per item: `weak: string[]`, only if it fits `progress.ts` without a schema bump; otherwise random). A miss re-queues the item in the session like any other (`retryGap`). The quiz arena's map screen shows a **Verb drill (n due)** button (`verb-drill`) when a course has verb units and at least one conjugation card exists; it is hidden otherwise. Result: the item's SM-2 card is scheduled with `gradeOf`. Other shells play conjugation items through the generic item renderer as they do any kind (no new shell work); the roleplay and detective shells are checked and, if they filter kinds, documented.
- **Outputs:** code, tests (the round picks due before new; a missed form comes back; hidden when no verb units; deterministic with a seed), bot driver step `verb-drill` in `scripts/bot/quiz-arena.mjs`, docs.
- **Contract:** testid `verb-drill`; `RoundKind` gains `'verbs'`; no change to the pack schema.

### EGS-32 Editions in the pipeline (hr + en from one run)
- **Inputs:** Finding 1; brief fields `sourceLang`, `languages`.
- **Do:** make the `editions` step real. After `assemble`, for each edition language other than `sourceLang`, a `translator` role (model from `course.md`, `client/claude-code` in the live check) translates **only** the source-edition catalog: every string of `text/<sourceLang>.json`, **excluding** keys that live in the target-language catalog (the taught phrases are not translated: `lang !== targetLang` and the key is not in `text/<targetLang>.json`), keeping `{{gap}}` markers, `{placeholders}` and keys; `accepted` lists of non-taught keys are translated too. The output is validated (`validateCourse`), the missing keys are re-asked once (repair round), and `pack.languages = [sourceLang, ...editions]`. The player's language picker then offers hr and en. Book Translator stays a manual alternative (documented); the step does not call it. The `editions` step is skipped when `languages.length === 1`, as now.
- **Outputs:** step, handler, prompt, role, docs, tests with the mock provider (hr -> en for the fixture; validate and lint clean; the taught `de.json` is byte-identical before and after; a run with a missing key repairs), ROADMAP row (also fix the duplicate EGS-18 placeholder row).
- **Contract:** `pack.languages` lists the editions; `text/<lang>.json` exists for each edition and for `targetLang`; lint reports a missing key per edition with `(in en)`.

### EGS-33 German voices
- **Inputs:** `voice.md`, `allocate.ts`, `edu_voice_status`, `edu_voice_quota`; research (Kokoro cannot read German; Supertonic 31 languages, Higgs ~100, OmniVoice 600+, Chatterbox lists `de`).
- **Do:**
  1. Check, with the real services in the live check (not in unit tests): `edu_voice_status` must show which providers read `de`. In code: `reads('de')` for VibeTTS must come from `list_voices` language codes (a probe, not a hard-coded list), and German must not be sent to Kokoro.
  2. Allocation for a language course, stated as a proposal: the clips that need speaking in a language course are the **German listening clips** (and optional narration in the edition language). The hub order is kept (Croatian first, then English, then others, `orderLanguages`): if the course needs Croatian narration clips and they fit the remaining free Gemini quota, they go to Gemini first; **German then goes to Gemini only if its clip count still fits the quota left (10 requests a day, so in practice never for a course: it goes to local VibeTTS)**. Because a whole-language rule makes German local, narration for a language course defaults to **off** (`media.voice` narration flag; the worker finds the real setting name) so the free quota is not spent on Croatian narration that nobody asked for; the brief can turn it on. German local order: VibeTTS (Supertonic or Higgs voice) then ComfyUI TTS (OmniVoice / Chatterbox). `voice.localVoices.de` default is empty (VibeTTS picks); the voice-director may name `supertonic:F1`-style ids only from `list_voices`.
  3. Style for taught German: `fallbackStyle` already says "clear, natural and a little slow"; add a `de` line to the voice-director prompt (standard German, Hochdeutsch, no dialect, one phrase per clip, the article spoken with the noun).
  4. Fix the stale comments (`allocate.ts:11`).
  5. `edu_voice_status` output includes `readsDe` per provider; the course gets a warning (not a failure) when no provider reads German: clips become silent placeholders as the rule says.
- **Outputs:** code, tests with fakes (German: Kokoro-only availability -> placeholders + warning; Supertonic available -> VibeTTS; quota 10 left and 4 hr + 40 de clips -> hr Gemini, de local; no narration default for language courses), docs, ROADMAP row.
- **Contract:** `VoiceAvailability.vibetts.reads('de')` is a probe; `media.voice` narration default false when `targetLang` is set.

### EGS-34 German UI strings (and the `de` table for all keys)
- **Inputs:** all UI keys after EGS-25, 26, 27, 31 have merged (or a rebase onto them).
- **Do:** table `DE` in `i18n.ts` for every `UiKey`, `de` tables for every shell's strings, `UI_STRINGS.de`; keep the "written by a language model, not native" note; test that every key exists in `en`, `hr` and `de` (a missing `hr` key found by the test is fixed here too). A German-speaking learner is not a target of the course; the table makes `languages: ['de']` editions of other courses work and the new `fb.note.*` / `mode.*` strings complete.
- **Outputs:** tables, test, docs, ROADMAP row.

### B2 design (what the system can check)

B2 reuses shells and items; only the glue is new. Principle: every B2 activity must have an answer key the engine can check, or be an explicit self-check.

| B2 activity | Built from | New? |
|---|---|---|
| Graded long reading (chapters) | encyclopedia articles (one per chapter, unit-ordered, cross-linked) shown in a **reader view** of the encyclopedia shell | reader view, EGS-35 |
| Tap-to-gloss vocabulary, per-text glossary | `shells.config.encyclopedia.glossary` (data below), tappable spans in the article body and a glossary panel per text; glosses in the edition catalogs (hr / en), terms in the target catalog | EGS-35 |
| Comprehension: multiple choice | `mcq` | no |
| Comprehension: true / false / not given | `mcq` with three fixed options `t`, `f`, `ng` (`shuffle: false`, tag `tfng`); lint `TFNG_OPTIONS` | convention + lint, EGS-36 |
| Comprehension: ordering of events | `order` | no |
| Matching headings to paragraphs | `match-pairs` (left = paragraph opening, right = heading) | no |
| Cloze on the text | `cloze` (text = a passage excerpt) | no |
| Vocabulary SRS harvested from the texts | `flashcard` items **derived** from the glossary by a deterministic pipeline step `harvest` (ids `<articleId>-gl-<n>`, `taught: true`, tag `gloss`) | EGS-36 |
| Grammar: connectors, Konjunktiv II (also past), Passiv, relative clauses | `cloze` with bank, `order` (sentence building), `sort-groups` (verb-final vs inversion), `conjugation` (new tense ids `passiv-praesens`, `passiv-praeteritum`, `perfekt-passiv`, `konjunktiv2-vergangenheit`), `typed` (transformation with an accepted list) | grammar tables + lint, EGS-37 |
| Listening passages (optional) | German VibeTTS clips per paragraph of a reading, played in the reader | EGS-38 |
| Writing, speaking | **Self-check only**: `flashcard` tagged `self-check`, prompt = the task, back = a model answer; the learner compares and grades themselves with the existing SM-2 buttons. **No auto-grading** (out of scope) | convention + lint `SELFCHECK_NO_MODEL`, EGS-36 |

**Passage link.** A comprehension or cloze item names its text with `extensions.passage = { article: "<articleId>", paragraphs?: [from, to] }`. In every shell that plays items, the item screen shows a collapsible "Read the text" panel (article body or paragraph range, with tap-to-gloss); the encyclopedia reader jumps to it from the feedback. Owned by EGS-35.

**Glossary data (contract, EGS-35).** `shells.config.encyclopedia.glossary: { [articleId]: GlossEntry[] }`, `GlossEntry = { id, term: key, lemma?: key, gloss: key, pos?: 'n'|'v'|'adj'|'adv'|'prep'|'conj'|'phrase', note?: key }`. `term` is the exact surface form in the article body (target catalog, taught); `lemma` the dictionary form (nouns with article and plural: "die Entscheidung, -en"); `gloss` and `note` are edition strings (hr, en). Keys: `art.<articleId>.gl.<id>.term|lemma|gloss|note`.

**Text-writing rules for B2 (into the prompts, EGS-36).** Reading length 350 to 700 words per text (lint band 300 to 800), three to eight paragraphs of 3 to 6 sentences, a heading per paragraph; register: informative non-fiction, a news report, an opinion piece with a stated position, a short biography or a report on a social topic; the first sentence of a paragraph carries its point; 10 to 20 glossary entries per text, from words above B1 (no names, no cognates the learner already knows), no word glossed twice; sentences average 14 to 24 words, none over 40; connectors (obwohl, während, sodass, deshalb, trotzdem, indem, falls), Passiv, relative clauses, Konjunktiv II and nominal phrases at a density that makes the text B2; standard German, no dialect; the text rests on the fact base (facts cited as for any article), sources named; no invented quotes from real people.

**B2 lint codes** (`lint.ts`, run when `pack.cefr` is B2 or an article has a glossary; error unless noted): `READING_LENGTH` (warning outside 300 to 800 words), `READING_SENTENCE_LENGTH` (warning if mean sentence length is outside 12 to 26 words or any sentence has more than 45), `GLOSS_TERM_NOT_IN_TEXT` (error: the `term` is not a substring of the article body), `GLOSS_DUPLICATE` (error: same term twice in one text), `GLOSS_COVERAGE` (warning: fewer than 8 entries in a reading of 300+ words), `READING_ITEM_NO_PASSAGE` (error: an item tagged `reading` without `extensions.passage`, or the article / paragraph range does not exist), `READING_ITEM_COUNT` (warning: a reading with fewer than 4 items), `TFNG_OPTIONS` (error: a `tfng` item whose options are not `t`, `f`, `ng` in that order with `shuffle: false`), `SELFCHECK_NO_MODEL` (error: a `self-check` flashcard whose back has fewer than 25 words), `GRAMMAR_FORM_MISMATCH` (error, EGS-37), `GRAMMAR_CONNECTOR_CLASS` (error, EGS-37), `GRAMMAR_TRANSFORM_ONE_ANSWER` (warning, EGS-37).

**Honesty about B2.** Texts and glosses are model-written and not natively reviewed. Length, sentence length, term-in-text, option and form checks are mechanical; whether a text is really B2 is a judgement the lint cannot make (sentence statistics and connector / Passiv counts are only a proxy). The live check says so and asks the user to read one text.

### EGS-35 Reader view, glossary and passage-linked items
- **Inputs:** B2 design above; `src/player/shells/encyclopedia/` (`view-article.ts:27-109` article spread, `articles.ts`, `data.ts`, `app.ts`, `strings.ts`), `src/shared/shells/encyclopedia.ts` (section schema + lint; `theme: 'parchment'` at :431).
- **Do:**
  1. `encyclopedia` section schema gets optional `glossary` (contract above) and `reader: boolean` (default false; true makes the reader the first screen after Start). The shell lint checks every key (`TEXT_MISSING` per edition) and `GLOSS_TERM_NOT_IN_TEXT`, `GLOSS_DUPLICATE`, `GLOSS_COVERAGE`.
  2. **Reader view** (screen `reader`; testids `reader`, `reader-chapter-<articleId>`, `reader-prev`, `reader-next`, `reader-progress`): unit-ordered articles as chapters with a table of contents; remembers chapter and scroll position in the progress store (`progress.shells.encyclopedia.reader`); marks a chapter read at its last paragraph; arrow keys change chapter. Reuses the parchment theme and article layout with larger type in a reading-width column.
  3. **Tap-to-gloss:** every glossary `term` in the body is a `button.gloss` (`gloss-<id>`) that opens a popover (lemma, gloss, note); a per-text glossary panel (`glossary-panel`) lists all entries with an "in my deck" toggle (on by default; stored as `progress.shells.encyclopedia.glossOff: string[]` and honoured by EGS-36's harvested cards). Screen readers get the gloss through `aria-describedby`.
  4. **Passage panel** for items: `extensions.passage` rendered by a shared helper in `src/player/items/common.ts` (`passage-toggle`, `passage-panel`), closed by default in a quiz round and open in the reader; works in every shell that uses `getItemRenderer`, with no per-shell code.
  5. New UI keys en + hr (de in EGS-34): `reader.*`, `gloss.*`, `passage.*`.
- **Outputs:** code, fixture `de-b2-reading` (hr + en editions, `targetLang: de`, 2 chapters of about 400 words, 12 glosses each, one item of every comprehension form with passage links), tests, bot steps in `scripts/bot/encyclopedia.mjs` (open reader, tap a gloss, read to the end), docs (`docs/player.md`), ROADMAP row.
- **Contract:** the glossary data, `extensions.passage`, the `reader` flag and the testids above (frozen for EGS-36 / 38).

### EGS-36 B2 format, reading prompts, glossary harvest, self-check
- **Inputs:** EGS-29 (formats, `verb_units`), EGS-30 (rules slot), EGS-35 (contract).
- **Do:**
  1. Format `language-b2` in `seed/config/formats.md`: `cefr: B2`, 6 units, 3 objectives per unit, 5 items per objective, `articles_per_unit: 2` (the readings), `research_questions_per_unit: 2`, `verb_units: 1`; new optional format fields `reading: boolean`, `reading_words: [min, max]` (350, 700), `glossary_per_text: [min, max]` (10, 20); kinds: mcq, true-false, multi-select, cloze, typed, match-pairs, order, sort-groups, flashcard, conjugation. `language-b1` gets `reading: true`, `reading_words: [200, 400]`, glossary 6 to 12 (B1 reads too, shorter). `resolveBrief`: `cefr: B2` selects `language-b2`; C1 / C2 without a format still errors ("out of scope, HUB-22").
  2. **Readings:** a prompt `seed/prompts/subject-expert/reading.md`, used instead of the article prompt when the format has `reading: true` in a language course. It carries the B2 text-writing rules and outputs `{ articles: [{ id, title, unit, body (paragraphs separated by blank lines, `## ` headings), citations, glossary: [{ term, lemma, pos, gloss, note }] }] }` with `gloss` and `note` in the source language. Assemble writes the glossary into `shells.config.encyclopedia.glossary` (terms and lemmas to the target catalog, glosses to the edition catalogs), sets `reader: true` and enables the encyclopedia shell. The editions step (EGS-32) translates the glosses to `en`.
  3. **Comprehension items:** the item-writer prompt gets a reading mode: per reading at least 4 items (one `mcq`, one `tfng`, one `order` or heading match, one `cloze` on the text), each with `extensions.passage`; the authored item schema gets `passage` and `tags`, mapped by assemble; the `tfng` and `self-check` conventions are described in the prompt.
  4. **Pipeline step `harvest`** (deterministic, after `assemble`, before `editions`): one flashcard per glossary entry, id `<articleId>-gl-<n>`, front = the term in its sentence (term marked), back = lemma + gloss, `taught: true`, tags `['gloss']`, attached to the reading's objective; idempotent (stable ids, existing ones kept). This is the vocabulary SRS.
  5. **Self-check tasks:** per unit the item-writer may write one writing task and one speaking task as `flashcard` tagged `self-check` (prompt = task with register and word count; back = a model answer of 80 to 180 words). The card shows "Compare with the model answer" (`selfcheck.hint`); nothing is graded by the engine.
  6. Lint: `READING_*`, `TFNG_OPTIONS`, `SELFCHECK_NO_MODEL` (EGS-35 owns the `GLOSS_*` codes). B2 rules text in `seed/config/language-rules/de-b2.md`, appended to `{{language_rules}}` when `cefr` is B2.
- **Outputs:** format, prompts, `harvest` handler, lint, tests (a mock-provider run on `language-b2` gives readings inside the band, glossaries, harvested flashcards with stable ids and a clean `edu_lint`; every lint code has a failing fixture), docs, ROADMAP row.
- **Contract:** format id `language-b2` and the three format fields; item tags `reading`, `tfng`, `self-check`, `gloss`; flashcard id scheme `<articleId>-gl-<n>`.

### EGS-37 B2 grammar tables and items
- **Inputs:** EGS-27 (kind), EGS-28 (verb table).
- **Do:** `src/shared/lang/de/grammar.ts`: (a) **connectors** `{ word, class: 'verb-final' | 'inversion' | 'coordinating', meaning, level }` (verb-final: weil, dass, obwohl, während, sodass, indem, falls, ob, damit, nachdem, bevor; inversion: deshalb, trotzdem, deswegen, außerdem, dennoch, folglich; coordinating: und, aber, denn, oder, sondern); (b) the **relative pronoun table** by gender, number and case (with preposition); (c) extend EGS-28's `conjugate` with tenses `passiv-praesens`, `passiv-praeteritum`, `perfekt-passiv`, `konjunktiv2-vergangenheit` for the whole verb table (Konjunktiv I only as a stretch, only if its golden tests pass; else documented as left out); (d) B2 grammar rules text in `rulesFor('de')`. Item patterns (in the prompts, checked by lint where deterministic): connector cloze with a bank of both classes; `order` for word order after a connector; `sort-groups` verb-final vs inversion from the table; relative-pronoun cloze with `extensions.grammar = { kind: 'relative', gender, case }` (answer checked against the table); Passiv and Konjunktiv II past as `conjugation` items; `typed` transformations ("Man baut das Haus." -> Passiv) only with `extensions.grammar.kind = 'transform'` and an accepted list of two or more variants.
  Lint: `GRAMMAR_FORM_MISMATCH` (error), `GRAMMAR_CONNECTOR_CLASS` (error), `GRAMMAR_TRANSFORM_ONE_ANSWER` (warning); `CONJ_TENSE_LEVEL` knows the B2 tenses.
- **Outputs:** tables, lint, tests (golden: 20 Passiv and 20 Konjunktiv II past forms, the full relative-pronoun table, every connector class), prompt text, docs, ROADMAP row. Same honesty note as EGS-28.
- **Contract:** `extensions.grammar`; the four new tense ids; `rulesFor('de').promptRules` including B2.

### EGS-38 Listening passages (optional; build last)
- **Inputs:** EGS-33 (German routing), EGS-35 (reader), `src/engine/edu/voice.ts` (narration cut at `narrationMaxChars` 600).
- **Do:** voice option `media.voice.passages` (default **false**): one clip **per paragraph** of each reading (longer paragraphs split at a sentence), German, **local chain only (never Gemini)**, asset ids `art-<articleId>-p<n>`; the reader shows a play button per paragraph (`reader-play-<n>`) and "play all"; a missing clip is a silent placeholder with the usual lint warning. `edu_voice_plan` shows clips and characters before anything is generated. Deterministic plan, no new role.
- **Outputs:** code, tests with fakes (plan counts, local routing, placeholders, hash index skips unchanged paragraphs), docs, ROADMAP row.
- **Contract:** `media.voice.passages`, the asset id scheme, the testids above.

## Order, dependencies, parallel work

```
Wave 1 (parallel, no shared files except i18n.ts keys, resolved by each ticket adding its keys in its own block):
  EGS-25 start screen       (player/kit, design/themes)
  EGS-26 matching           (shared/edu match + context helper)   -> must merge before 27
  EGS-28 verb table         (shared/lang, new files only)
  EGS-29 formats + brief    (seed/config, brief.ts, schemas.ts)
  EGS-32 editions step      (pipeline)
  EGS-33 German voices      (engine/voice)
Wave 2 (after 26 merged; 28 and 29 preferably merged):
  EGS-27 conjugation kind   (stacks on 26; lint hook for 28 added here if 28 has merged, else 28 adds it)
Wave 3 (after 27, 28, 29):
  EGS-30 prompts            (needs the authored shape of 27, rules of 28)
  EGS-31 verb drill         (needs 27, 29)
Wave 4 (B2; EGS-35 can start in wave 1, it only touches the encyclopedia shell):
  EGS-35 reader + glossary  (independent; parallel with wave 1)
  EGS-36 B2 format, readings, harvest, self-check  (after 29, 30, 35)
  EGS-37 B2 grammar tables  (after 27, 28; parallel with 36)
  EGS-38 listening passages, optional  (after 33, 35; last)
Wave 5:
  EGS-34 German UI strings  (after 25, 26, 27, 31, 35, 36 and 38 so all keys exist)
Then the live check (below), by a session with the studio running; fixes found there become new EGS tickets.
```
Merge order to avoid conflicts: 26, 25, 28, 29, 32, 33, 35, 27, 30, 31, 37, 36, 38, 34. Conflict hot spots: `i18n.ts` (25, 26, 27, 31, 34), `checkers.ts` (26, 27), `pipeline-handlers.ts` (29, 30, 32, 36), `lint.ts` (27, 28, 35, 36, 37), `round.ts` (27, 31), `ROADMAP.md` (all: one row each, resolve by hand).

## Acceptance criteria and the tests that prove each

| # | Criterion | Proof |
|---|---|---|
| A1 | The title screen of all six shells has identical structure and the `menu` theme; the in-game screens keep their own theme | NEW assertions in `tests/player-shell-picker.e2e.test.ts`: for each enabled shell of the `european-capitals` fixture plus `hr-a1-greetings` (roleplay) the title DOM skeleton (tag + class + testid tree, texts removed) is equal across shells; `data-edu-theme === 'menu'` on `data-screen=title`, equals the shell theme after `start` |
| A2 | Only one title implementation exists | unit test in `tests/player-shell-kit.test.ts`: `class: 'title-screen'` appears in exactly one source file (`kit/start.ts`) |
| A3 | Picking a mode keeps the progress and the language, and does not flash the old theme | e2e: switch shell on the title, `data-edu-theme` stays `menu`, progress export before and after equal |
| A4 | `menu` theme passes contrast, fonts, motion, reduced-motion | `tests/design-tokens.test.ts` and `tests/themes-load.test.ts` (iterate the registry), bot `--axe` 0 violations on the title in every shell, `--keyboard` run completes |
| A5 | Title looks right at 1280x800 and 390x844 (no overflow, cards wrap) | bot/Playwright screenshots of the title in every shell (`scripts/theme-previews.mjs` extended); reviewed by eye by the worker and again in the live check |
| A6 | The bot's testids still work | `tests/bot*.e2e.test.ts` all green (perfect / wrong / random, each shell) |
| B1 | `ä/ö/ü/ß` rules as specified | `tests/edu-match.test.ts` table: Maedchen, Madchen (wrong, "umlaut" note), Strasse, Strase (wrong or typo per distance), Bruder vs Brüder wrong, Feuer exact, haus accepted with `caps`, "ich heisse anna" accepted; other languages unchanged (hr "cuvar" still `ignore`) |
| B2 | One check context for the player, quiz arena, lint, live quiz, bot | grep test: no remaining `{ text: ..., diacritics: ..., typos: ... }` literals; `tests/edu-checkers.test.ts` for `lang` flowing into typed / cloze / listening |
| C1 | A conjugation item validates, lints, builds, plays and is solved by the bot | `tests/edu-checkers.test.ts` (right, partial, all wrong, `ask`, `given`, a one-letter slip on `gehst` is wrong because typos are off, `Maedchen`-style transliteration in a form is right), `tests/edu-lint.test.ts` (each CONJ code, one test per code), `tests/bot.e2e.test.ts` on `de-verbs-a1` (perfect = all correct, wrong = 0, random in between, 0 console errors, keyboard-only, axe 0) |
| C2 | Authoring: item-writer output with `conjugation` assembles into catalogs (taught forms in `de.json`) | `tests/edu-authoring.test.ts`, `tests/edu-assemble.test.ts` |
| C3 | Live quiz skips the kind; studio editor edits it | `tests/live-questions.test.ts` (skip), renderer test for ItemEditor form (existing renderer test style) |
| D1 | Wrong German forms are caught mechanically | `tests/de-verbs.test.ts` >= 40 golden forms; `tests/edu-lint.test.ts`: a fixture item with "gehst" for `er` gives `CONJ_FORM_MISMATCH`; unknown verb gives `CONJ_VERB_UNKNOWN` warning only |
| E1 | Formats and brief | `tests/edu-brief.test.ts`: `cefr: A2` -> `language-a2`; `B2` without a format -> clear error; verb-unit numbers present; mock pipeline run on `language-a2` has `extensions.language.verbUnits` of the right length |
| E2 | Prompts carry the German rules for `de` only | `tests/edu-authoring.test.ts` rendered-prompt tests for the item-writer, language-coach, misconception-designer, fact-checker prompts |
| F1 | Verb drill picks due items first and is hidden without verb units | `tests/player-round.test.ts` + bot step `verb-drill` |
| G1 | One run makes both editions | `tests/edu-pipeline*.test.ts` with the mock provider: `languages = [hr, en]`, three catalogs, `validateCourse` and `edu_lint` clean, `de.json` unchanged by the step, the language picker offers hr and en (bot) |
| H1 | German voice routing | `tests/voice-allocate.test.ts` cases listed in EGS-33; `edu_voice_status` shows `readsDe` (live check) |
| I1 | UI tables complete | `tests/player-i18n.test.ts`: every key in en, hr, de |
| R1 | Reader, tap-to-gloss and the passage panel work in the encyclopedia and in the quiz arena | `tests/bot-encyclopedia.e2e.test.ts` on `de-b2-reading` (open reader, tap a gloss, read to the end, passage panel from a quiz item, keyboard-only, axe 0), `tests/encyclopedia-lint.test.ts` (one failing fixture per `GLOSS_*`) |
| R2 | B2 course shape and lint codes | `tests/edu-brief.test.ts` (`cefr: B2` -> `language-b2`; C1 errors), `tests/edu-pipeline*.test.ts` (mock run: readings 300 to 800 words, glossaries, harvested flashcards with stable ids, clean lint), `tests/edu-lint.test.ts` (a failing fixture for each of `READING_LENGTH`, `READING_SENTENCE_LENGTH`, `READING_ITEM_NO_PASSAGE`, `READING_ITEM_COUNT`, `TFNG_OPTIONS`, `SELFCHECK_NO_MODEL`) |
| R3 | B2 grammar is checked mechanically | `tests/de-grammar.test.ts` (goldens), `tests/edu-lint.test.ts` (`GRAMMAR_*`) |
| R4 | Harvest is idempotent and respects the learner's "in my deck" switch | unit test: run twice, same ids; a hidden entry is not queued |
| R5 | Self-check cards are never graded by the engine | unit test: a `self-check` flashcard result comes only from the learner's own grade |
| R6 | Passage clips (optional) | `tests/voice-plan.test.ts` (EGS-38 cases) |
| Z | Repo health | `yarn typecheck`, `yarn lint`, `yarn test`, `yarn build` all pass on each ticket branch |

Each ticket's own changelog ends with the DONE / NOT DONE / UNTESTED list. UNTESTED by design until the live check: real audio, real VibeTTS German, a human playing.

## Live check (hub session; no paid models; never start Scriptorium)

Preconditions: `pwsh -File scripts\hub.ps1` (status). Start only Edu Studio (`pwsh -File scripts\hub.ps1 start edu-studio`); ComfyUI, Pixel Studio and Chiptune Studio are **not** needed (art and music off). VibeTTS is a tray app that is never started by the studio: ask the user to have it running if the voice step should be checked; Gemini (flow-music-mcp) is not used for German; check `edu_voice_quota` before any voice generation and do not spend quota on Croatian narration. All model work is `model: "client/claude-code"` ($0): the session loops `edu_wait` -> `edu_get_task` -> answer -> `edu_submit_task`. Open `runs/deutsch-a1-pilot.md` (copy of `runs/_template.md`) and record every id, decision and check. Make sure the data folder has the new seeds (see EGS-29's seed-sync note) before the first run.

1. **Start screen on the existing pilot.** `edu_build {slug: "suncev-sustav"}`. Open `C:\Users\Infplane\EduGames\courses\suncev-sustav\build\index.html`. For every mode the course enables, click its card and check: same layout, same theme (menu), the mode name and blurb change, Start leads into that mode's own theme. Screenshots at 1280x800 and 390x844 for each shell title and for one in-game screen per shell (proof that the in-game look is unchanged). Run the bot: `node scripts\play.mjs courses\suncev-sustav\build --mode perfect --shell <id>` for each shell. Record: DONE only for what was seen; the user's opinion of the look is **not** verified until the user looks at it.
2. **A1 pilot with a verbs unit.** `edu_run_pipeline` with this brief (slug `deutsch-a1-pilot`):
   `{"topic":"German for beginners","audience":"Croatian and English speaking adults starting German","sourceLang":"hr","languages":["hr","en"],"targetLang":"de","cefr":"A1","format":"language-a1","units":4,"shells":["quiz-arena","encyclopedia","mindmaze","rpg"],"story":"none","model":"client/claude-code","media":{"art":{"enabled":false},"music":{"enabled":false},"voice":{"provider":"auto"}}}`
   (the worker adjusts the media keys to the real schema). Check: 4 units of which at least 1 is a verb unit (`extensions.language.verbUnits`), conjugation items for sein, haben and one regular verb in Präsens, `languages = [hr, en]`, `edu_lint` 0 errors (list warnings), the bot passes perfect / wrong / random in the quiz arena, the **Verb drill** button shows and a drill round runs, typing "Maedchen" or "Strasse" is accepted with a note, typing "Madchen" is not. Switch the player language hr <-> en: prompts change, the German answers do not.
3. **Voices.** `edu_voice_status`: which providers read `de` (record it); `edu_voice_plan` (no generation yet) and `edu_voice_quota`; if VibeTTS is up and reads German, generate **one** listening clip (a single-clip batch) and play it. If nothing reads German, record the placeholders and the warning. No Gemini request for German.
4. **A2 and B1 smoke courses.** Two small runs (`units: 2`, formats `language-a2` and `language-b1`, same media off, `languages: ["hr","en"]`, slugs `deutsch-a2-smoke` and `deutsch-b1-smoke`): they must finish, lint with 0 errors, include Perfekt (A2) and Präteritum / Konjunktiv II (B1) conjugation items that pass `CONJ_FORM_MISMATCH`, and pass the bot (perfect and random, quiz arena). These prove the formats and the machinery, not the quality of the German.
5. **B2 smoke course.** `deutsch-b2-smoke`: `{"cefr":"B2","format":"language-b2","units":2,"languages":["hr","en"],"targetLang":"de","sourceLang":"hr","shells":["encyclopedia","quiz-arena"],"story":"none","model":"client/claude-code","media":{"art":{"enabled":false},"music":{"enabled":false}}}` (voice passages off; if VibeTTS is running and the user wants it, `edu_voice_plan` with `passages: true` only plans, and one paragraph clip is generated). Check: 2 units with 2 readings each in the 300 to 800 word band, glossaries, tap-to-gloss works in the built game (screenshot of a popover), a glossary-harvested flashcard appears in the deck, a comprehension item opens its passage panel, an item of each form (mcq, tfng, order, headings match, cloze), a Passiv / Konjunktiv II conjugation item passes `GRAMMAR_FORM_MISMATCH`, a `self-check` card shows the model answer, `edu_lint` 0 errors, bot perfect and random in the quiz arena and the reader walkthrough in the encyclopedia. The `en` edition shows English glosses with German texts.
6. **Not verified by anyone but the user:** whether the B2 texts are really B2 (ask the user to read one), the correctness and naturalness of the German, the Croatian and English prompts, real listening, and that the course is fun. Mark UNTESTED; ask the user to play `deutsch-a1-pilot` (a production is done only when the user has played it).

## Hub changes (this repo, `C:\projects\Personal\creative-hub`)

- `ROADMAP.md`: add the row **HUB-22** (next to HUB-19 at line 25, same table format): "Edu Studio: one start screen for every game mode, and a German course (hr + en speakers, A1 to B1) with verb conjugation; tickets EGS-25 to EGS-34 in `edu-game-studio`; live check with the pilot `deutsch-a1-pilot`", status open; plan in `.claude/tickets/HUB-22-edu-start-screen-german/plan.md`. Mark it done only after the live check and the user has played the pilot.
- `.claude/skills/make-edu-game/SKILL.md`: (a) section 0.4 and 1: language courses use `format: language-a1|a2|b1|b2` (chosen from `cefr`), `languages: ["hr","en"]` for two editions made in one run, `targetLang: "de"` and the verb units / `conjugation` items (typed with umlaut / ss tolerance, no typo tolerance for forms); C1 and C2 are not available; B2 is a reading course (reader view, tap-to-gloss, harvested vocabulary cards, self-check writing and speaking with a model answer, no auto-grading); (b) section 0.5 voices: for German the listening clips go to local VibeTTS (Gemini's 10 requests cannot cover a course) and narration is off by default for language courses; run `edu_voice_status` first; (c) section 2: the start screen is one shared menu, and a rebuilt course shows it (rebuild old courses with `edu_build`); (d) delete nothing else. Keep the rules about client model work and never starting Scriptorium.
- `ROADMAP.md` (hub): also add an open row **HUB-23** "Edu Studio: role-play scene generator for language courses (follow-up of HUB-22)", no plan yet. In the Edu Studio repo the same item is `EGS-39` under the ROADMAP "Later" list (open, planned after EGS-25 to EGS-38).
- `README.md` table row for Edu Studio: mention language courses A1-B1 (only if the row lists capabilities).
- `runs/deutsch-a1-pilot.md` (+ `-a2-smoke`, `-b1-smoke`, `-b2-smoke`): production logs, created by the live-check session from `runs/_template.md`.
- `MEMORY` (user auto-memory) update after the run: what was merged, what the live check showed.
- No change to `services.json` or `.mcp.json` (no new service); `scripts/hub.ps1` unchanged.

## Optional follow-ups (flagged, not in this plan)

- **Role-play scene generator** (EGS-39, open roadmap item, not built here): a `scene-writer` role (language-coach + narrative-designer) that writes `shells.config.roleplay` dialogue scenes with translations and vocabulary for the course's taught words, reuses the `broken-roleplay` lint, adds `roleplay` to `PIPELINE_SHELLS`.
- **Pronunciation scoring** (ROADMAP Later).
- **A course-level theme choice** in the Game tab (ROADMAP Later) now that titles are unified.

## Open questions for the user (also returned in the summary)

1. Is a German-capable engine (Supertonic or Higgs) installed in your VibeTTS? (`edu_voice_status` in the live check shows it; without one, German clips are silent placeholders.)
2. B2 listening passages (EGS-38) are optional and built last: include them in HUB-22 or leave them for later?
3. Konjunktiv I (indirect speech) is a stretch inside EGS-37, only if its golden tests pass. Acceptable, or must it be in?
