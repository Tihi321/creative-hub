# HUB-22 research: Edu Studio start screen, topic templates, German course

Repo: C:\projects\Personal\edu-game-studio (paths below relative to it unless absolute).

## Question
(1) How is the player's start / mode-select screen built and styled, and why is it mixed? (2) Is a course template-based, so a new topic is just a new pipeline brief? (3) Can a German course (for Croatian or English speakers) be made now, and what is missing?

## Answer
1. The mode cards are not cards: they are a row of `chip` buttons (`shell-picker`) inside each shell's own title screen. The "mixed" look is because switching a mode remounts a different shell that sets its own `data-edu-theme` on the root, so the whole title screen (colours, fonts, ornament, art, tagline) changes per mode. The mode picker is therefore dressed differently on every mode. A unified style = fix one theme for the title/menu layer (or style the picker outside the per-shell theme).
2. Yes, template-based. Shells, items, themes and the player are shared code; a new topic is a new `edu_run_pipeline {brief}`. Only content (facts, text, art prompts) is topic-specific. Cost is model work (client/claude-code = free but you answer ~15 job types) plus ComfyUI art/Chiptune music; the pilot log is 1305 lines.
3. German is possible only partly now: quiz arena, encyclopedia, MindMaze and RPG shells work through the pipeline with `targetLang: de`; the language role-play shell exists but the pipeline does not switch it on (needs hand-authored scenes). Voices/STT likely work but unverified for German. No German-specific grammar/conjugation tooling exists.

## Path through the code

### 1. Start screen
- Built `index.html` is only `<div id="edu-root">` plus `player.css`, `game-data.js`, `player.js` (C:\Users\Infplane\EduGames\courses\suncev-sustav\build\index.html:10-14). All markup is made at runtime, so I read the source, not rendered markup. **Not rendered** (no browser run). Confirmed.
- Shared title: `titleScreen()` in `src/player/kit/screens.ts:61-` returns `section.title-screen.shell-title.shell-title-<shellId>` with eyebrow tagline, h1 `course-title`, subject, audience, optional shell `art`, classroom block, language picker, `shellPicker(...)`, settings, big Start button, export/import/reset (screens.ts:188-216). Confirmed.
- Mode picker: `shellPicker` (screens.ts:34-48): `div.shell-picker` with one `button.chip` per `host.shells` (`shell-<id>`, `aria-pressed`), returns null if fewer than 2 shells. Click calls `host.switchShell(id)`. Styling `src/player/kit/kit.css:7-21` is flex-wrap only; colours come from the active theme's `.chip`. Confirmed.
- Quiz arena does NOT use the kit title: it has its own copy in `src/player/shells/quiz-arena.ts:387-` (same classes, plus a timer toggle) and calls the same `shellPicker`. So there are two title implementations. Confirmed. The other four shells (rpg index.ts:348, mindmaze:231, roleplay:310, detective:261, encyclopedia app.ts:279) use `titleScreen`.
- Theming: each shell has a theme id (`ShellSession` opts `theme: THEME_ID`, e.g. mindmaze/index.ts:58) and mount sets `root.setAttribute('data-edu-theme', this.theme)` (`src/player/kit/session.ts:177-182`); quiz arena does the same (quiz-arena.ts:145-147; engine.ts:84-85 sets chalkboard). Registry `src/design/themes/index.ts` (`THEMES`, `themeForShell` at :116, `DEFAULT_THEME` chalkboard :112); a course may override per shell via `shells.config[shell].theme` (confirmed index.ts:116-119). Seven theme CSS files: castle, chalkboard, noir, parchment, pixel, postcard (src/design/themes/). The pilot `player.css` contains all six (selector counts: castle 12, chalkboard 7, noir 5, parchment 5, pixel 9, postcard 9). Confirmed.
- Theme dressing that hits the title: `.title-screen .screen-title::after` in chalkboard.css:134, parchment.css:79, postcard.css:123; castle/noir restyle `.eyebrow`, `.btn`, `.chip` (castle.css:116, noir.css:105); shell `art` slot differs per shell. Design doc: themes fill the `--edu-*` slots and "a shell never defines colours of its own" (docs/design.md, Look section). Confirmed.
- Existing hook: `shells.config[shell].theme` override already works, so the lowest-effort unification is every shell using one theme id; but themes are also tied to shell art/motion (castle doors, pixel `steps()`), so a pure override flattens the in-game look too. The ROADMAP "Later" list has "Save a course's theme from the Game tab once a second shell can play another look" (ROADMAP.md, Later), so a course-level theme choice is a known gap. Confirmed.

### 2. Templates / new topic
- Pipeline: brief -> research -> curriculum -> articles -> items -> distractors -> fact-check -> explain -> design -> story -> art -> music -> assemble -> reviews -> voice -> build -> lint -> playtest -> publish (docs/design.md Architecture; MCP guide: `edu_run_pipeline {brief:{topic,audience,age?,sourceLang,units?,model?,story?}}`). The pilot's brief is in C:\Users\Infplane\EduGames\courses\suncev-sustav\course.md:3-30 (topic, audience, sourceLang hr, languages hr+en, shells list, format quick, units 3, media art/music on, voice off). Confirmed.
- Shared: shells, item kinds (13, src/shared/course.ts:100-239), themes, player runtime, lint, bot. Topic-specific: fact base, articles, items, art prompts and generated art (pilot art plan in log.md:439-455), music, voices.
- Shells the pipeline enables by itself: `PIPELINE_SHELLS = ['quiz-arena','encyclopedia','mindmaze','rpg']` (src/engine/edu/authoring.ts:660). Role-play and detective "need authored sections (dialogues, cases) that no role writes yet", so they are only recorded as `requestedShells` (authoring.ts:653-659). Confirmed.
- Art limits: RPG tiles/sprites go to Pixel Studio, others to ComfyUI; failures become labelled placeholders (lint `PLACEHOLDER_ASSET` warning), not failures (docs/design.md Media). A new topic needs ComfyUI up for pictures; this was not re-measured. Time per topic: not measured here (pilot log has no timings; open question).
- Note stale comment: src/shared/brief.ts:18 says "the player has only quiz-arena today".

### 3. German learning
What exists (all confirmed by reading):
- Language table has `de` German/Deutsch (src/shared/languages.ts:59). Player UI strings exist only for `hr` (src/shared/ui-strings.ts:9); other languages show English menus (seed/config/languages.md). So Croatian speakers: fine; English speakers: fine; German-menu UI would need a table.
- Brief fields `targetLang` and `cefr` (A1..C2) (src/shared/brief.ts:14-17,33-37; course.ts:37,356-359). Format `language-a1`: 4 units, 3 objectives x 3 items, kinds `mcq, cloze, typed, match-pairs, flashcard, sort-groups` (seed/config/formats.md:31-41); default when `targetLang` set (brief.ts:80). Only an A1 format exists.
- language-coach role picks vocabulary/grammar by CEFR and writes accepted answers (seed/agents/language-coach-ines-markovic.md; pipeline-handlers.ts:271,346,459,513 pass `cefr` and `target_language` into prompts).
- Typed/cloze accepted lists per language live in the text catalog `accepted` (course.ts:47-48,134,148). Tolerant matching of case, diacritics, typos (docs/design.md; `pack.matching`). German umlauts/ß handled by diacritics policy: inferred, not read in `src/shared/edu/match.ts` (open question).
- Listening items + derived `<item>-listen` clips from taught phrases (EGS-17, docs/design.md voice-director row). Flashcards use SM-2 (src/shared/edu/srs.ts). Vocabulary garden in role-play shell.
- Speaking: mic button on typed/cloze/listening-typed; recogniser language = `targetLang`; Web Speech or local whisper.cpp (docs/speaking.md). Matching is by shared matcher, no pronunciation scoring. German with whisper: multilingual models handle `de` (inferred); Web Speech `de-DE` (inferred).
- Voice allocation (seed/config/voice.md): Gemini free 10 req/day, Croatian first; local = VibeTTS (Kokoro: English, Spanish, French, Hindi, Italian, Portuguese; Supertonic 31 langs; Higgs ~100) else ComfyUI TTS (OmniVoice 600+ langs default; Chatterbox lists `de`, seed/workflows/chatterbox-multilingual.map.yaml:18). Kokoro does NOT read German. German via Supertonic/Higgs/OmniVoice/Gemini: inferred from the language counts, not confirmed; `edu_voice_status` would show it (not run, services not started). Note `src/engine/voice/allocate.ts:11` comment still says Supertonic/Higgs: Croatian.
- Role-play shell: dialogue scenes with choose/type replies, translations, CEFR badge, vocabulary garden (src/shared/shells/roleplay.ts, src/player/shells/roleplay/). Fixture: Croatian A1 greetings (`tests/fixtures`, `.claude/temp/fixtures/roleplay/hr-a1-greetings.json`; golden in EGS-02). The pipeline does not generate its scenes (authoring.ts:653-659).

## Reproduction
Not a bug. Not run: no browser rendering of the start screen, no pipeline run, no edu_voice_status (no services started, read-only).

## What the plan needs

### (a) Unified start-screen ticket (proposal, options)
Files: `src/player/kit/screens.ts` (titleScreen, shellPicker), `src/player/shells/quiz-arena.ts:387-` (duplicate title), `src/player/kit/kit.css`, `src/player/style/arena.css:109-130`, theme CSS `.title-screen`/`.eyebrow` rules in the six themes, `src/design/themes/index.ts`, `src/player/kit/session.ts:177-182`, `src/player/engine.ts:84`, tests `tests/design-tokens.test.ts`, bot `scripts/bot/` testids (`shell-picker`, `shell-<id>`, `start`).
- Option 1 (smallest): one neutral "menu" theme applied only on `screen = title` (all shells); in-game screens keep the shell theme. Needs a way to swap `data-edu-theme` between title and play, and the title must be identical across modes (picker, buttons, tagline layout).
- Option 2: make mode selection a proper card grid (icon/art + name + one line per mode) rendered by one shared component, in the unified style; also move quiz-arena onto `titleScreen` so there is one implementation.
- Option 3 (cheapest, loses identity): force one `shells.config[*].theme` for all shells.
- Decide with the user: does "single style" mean only the title/menu, or all in-game screens? The user's words say the start screen only, "game modes ... awesome" (modes stay).
- Verification: bot screenshots of the title in every shell at 1280x800 and 390x844, axe, contrast tests; the pilot course must be rebuilt (`edu_build`) to see it.

### (b) German course (proposal)
Works now: `edu_run_pipeline` with `sourceLang: hr` (or `en`), `targetLang: de`, `cefr: A1`, `format: language-a1`, shells quiz-arena + encyclopedia + mindmaze + rpg; typed/cloze/mcq/match-pairs/flashcard/sort-groups; listening items and clips once a voice provider reads German; speaking button; SM-2 review; Croatian menus.
Gaps, ranked:
- Must have: (1) role-play shell not auto-generated: no role writes scenes/vocab for it (authoring.ts:653-659), yet it is the language-learning mode. Needs a role/prompt (narrative or language-coach) producing the `roleplay` section plus lint, or hand authoring. (2) Verify German voice: run `edu_voice_status`; confirm Gemini/Supertonic/Higgs/OmniVoice read `de` and the voice-director picks a German voice (`voice.localVoices.de`); Kokoro cannot. (3) German-specific content rules in the language-coach prompt: gender/articles (der/die/das), plural, verb conjugation, case, word order; items need a "grammar" form (cloze with a bank covers most; sort-groups for gender). Prompt work, no engine code. (4) A pilot run + user playtest (rule: done only when played). Also confirm umlaut/ß matching in `match.ts`.
- Should have: formats `language-a2`/`b1` (only `language-a1` exists); fact-checker for language items (facts source for vocabulary: curated word lists, not web); `de` UI strings if German-speaking learners are wanted.
- Nice: pronunciation scoring (ROADMAP Later), conjugation-table or sentence-building item kind, per-course vocabulary SRS deck view beyond role-play garden, a theme for a language course (postcard exists for role-play).

## Risks
- Changing the shared title/theme touches every shell and the bot testids; the player.css bundle size (about 200 KB per docs) grows with themes.
- Theme/shell coupling: art and motion are tied to the shell theme; overriding it can break contrast (tested per theme, tests/design-tokens.test.ts).
- A German course rests on an LLM writing the language content; no native check. The built-in `hr` UI strings were written by a model too (languages.md).
- Free Gemini quota 10/day: a full A1 course needs many clips; local voice quality for German unknown.

## Open questions
- Which languages the user's VibeTTS actually reports (Supertonic/Higgs installed?) and whether the ComfyUI TTS suite is installed.
- Does `match.ts` fold ä/ö/ü/ß (ae/oe/ue/ss) as accepted variants?
- Is the whole menu/screen style meant to unify, or only the title? Should Croatian or English be the source language for German?
- Pipeline time and token cost for the pilot: not recorded in log.md.
- Whether the git state of edu-game-studio master has EGS branches merged (ROADMAP says stacked, not merged; the brief says master fb26927+). Not checked.
