# deutsch-a1-pilot (HUB-22 live check items 2 and 3)

Status: RESTARTED 2026-11-01 after Edu Studio was restarted from fresh master build (run 1 on old code discarded; run 2 = restart from plan).

- Run 1 started via edu_run_pipeline (client/claude-code). Answered with real work: plan, 4 research searches (+repair rounds), curriculum, scope. Fact base 26 facts, 4 units, 12 objectives. Articles jobs (u1-u4) were queued when stopped.
- Evidence of stale engine: PIDs 19544 and 22772 (`node out/engine/index.js`, started 11:27 / 11:32). `out/engine/index.js` was rebuilt 17:53 (HEAD of edu-game-studio master 289bc7b, 17:52) and contains `language_rules`; the running process behaves like pre-EGS-29/30/32 code:
  - editions step skipped with the old message "the editions en come from Book Translator later (EGS-18)" (string no longer in src or out): course would be hr only.
  - scope prompt shows an empty "Language rules" block and "a verb unit: see above" with nothing above; curriculum prompt had no verb-unit note and schema without `verb`.
- Not verified: everything in items 2 and 3 (lint, bot, verb drill, matcher, language switch, voices).

## Run 2 (fresh master build), progress log
- Restart: edu_run_pipeline {slug, restart:true, from:'plan'} -> run 2. Research and fact base (26 facts, 6 sources) kept from run 1.
- Confirmed in the first prompts: {{language_rules}} filled (German rules block); curriculum prompt carries the verb-unit note ("mark exactly 1 unit(s) with verb:true"); scope prompt asks "verbs" for [VERB UNIT]. Editions step: not yet visible in `steps` through the items stage (check after assemble; NOT confirmed).
- Answered by the worker (client/claude-code): plan, curriculum (u2 = verb unit), scope (6 verbs: sein, haben, machen, wohnen, lernen, heißen, praesens, A1), 4 articles, items u1-u4 (u2 has 5 conjugation items: machen, haben, sein, wohnen; first submission of u1/u3/u4 used true-false/order, rejected by the A1 format kinds, resubmitted as accepted).
- Pending when the worker stopped (context budget): distractors u1-u4, fact-check, explain, accepted, design, assemble, editions, review, voice, build, lint, playtest.
- NOT verified yet: everything in live-check items 2 (lint, bot, verb drill, matcher, language switch) and 3 (voices).

## Worker 2 (continuing run 2)
- Answered: distractors u1-u4, items u1 (repair rounds), fact_check u1-u4 (all pass), explain u1-u4, accepted u1-u4. Next: whatever edu_get_task gives (design, assemble, review, voice, ...).
- Known content nit (unfixed): u3-q1 option b why says "francuski i hrvatski" have two genders; Croatian has three (wrong claim). Fix with edu_item_update after the run.
- Worker 2: also answered design (4 shells, round 8/boss 12), review_accessibility r1 (revise, 2 texts, both fixed via polish; I flagged my own false claim in u3-q1 opt b why), r2 pass. Next: child-safety review, assemble, editions, voice, build, lint, playtest (use edu_wait + edu_get_task book:'deutsch-a1-pilot'). Worker 2 context is nearly full; prompts are ~15k tokens each.

## Worker 3 (run 2 to the end)
- Answered: voice_plan (narration off, 8 German listening items, no gemini), editions (5 chunks, en), playtest_report (revise), summarize.
- Engine: voice_generate done by the engine itself (vibetts 8 clips, de: vibetts). Editions: en 276 texts, 123 taught de texts left as they are; course has hr, en. Build: 13 files. Lint: 0 errors, 13 warnings (CONJ_FORM_DUPLICATE_AMBIGUOUS macht er/ihr; READING_LENGTH 141 and 139 words vs 300-800; READING_SENTENCE_LENGTH; READING_ITEM_COUNT 0 items per reading; others not shown).
- Playtest: perfect/wrong/strong/average pass; struggling FAILED on u2-q8 (cloze): expected wrong but game says right; wrong-answer feedback has no feedback-answer; missed item not in review queue.
- Pipeline end state: BLOCKED at publish (hard gate: playtest). Not published.
- Possible code bug (not confirmed, not investigated): u2-q8 cloze behaviour; may be a content issue (accepted list too wide, e.g. macht/machst after widening) or an engine issue with the cloze/conjugation kind.
- Left for successor: fix u2-q8 (edu_get_course / edu_item_update, check accepted list), rerun edu_run_pipeline {slug, restart:true, from:'build'}; then verification checks and voice checks (not done by me). Also unfixed: u3-q1 opt b why Croatian-gender claim.

## Worker 4
- ENGINE BUG found: u2-q8 content was fine (key machst, bank machst/macht/machen). checkCloze applied the 1-letter typo rule to banked gaps, so picking macht (distance 1) scored right. Fixed: EGS-49, PR 39 (merged), cloze gaps with a bank get no typo tolerance; test in tests/edu-checkers.test.ts. Studio restarted by parent 21:33.
- Lint bug: A1 articles with a glossary were linted as B2 readings (band 300-800 words, 4 items) because readingBand falls back to the B2 band when no extensions.language.reading is recorded (language-a1 records none). Fixed: EGS-50, PR 40 (merged, out/ rebuilt in main checkout; the studio needs another restart for this to apply).
- Content: u3-q1 opt b why already correct (three genders, polished earlier). u2-q1 ihr set given:true (er/ihr macht ambiguity). Lint run 3: 0 errors, 12 warnings (before EGS-50 restart: still READING_* x10-ish, ENC_ANSWER_NOT_IN_ARTICLE u1-q1 and u3-q1 hunts).
- Run 3 (restart from build): build done 13 files, lint clean (12 warnings), playtest running at the time of writing.
- Run 3 playtest: perfect, wrong, strong, average pass. struggling (random, seed 5, accuracy 0.55) FAILED differently: "the bot printed no result (exit 1)" (no u2-q8 message any more). Rerunning by hand: `node scripts/play.mjs <build> --mode random --seed 5 --accuracy 0.55 --shell quiz-arena` runs >2 min with no output (still running at time of writing, background task brcdrfa5i). Possible hang/step-bound problem in review loop; not yet diagnosed. playtest_report model task queued (pipeline waits on it).
- Voice: gemini down (flow-music-mcp not running), quota used 0/10; VibeTTS up, de voice supertonic:M2. 8 German mp3 clips exist in course/assets/voice-de-*/v1.mp3 (made by the engine in run 2, not wav). No extra clip generated.
- NOT done by worker 4 so far: live checks (editions/catalog listing, verb drill button + drill round, matcher Maedchen/Strasse/Madchen, hr<->en switch), perfect/wrong/random as separate manual runs (pipeline runs of perfect/wrong/strong/average passed).

## Worker 5
- Answered playtest_report r3 (revise: struggling bot gave no result, honest) and summarize. Pipeline end state: BLOCKED at publish (hard gate: playtest struggling "printed no result (exit 1)"). Not published.
- Cause: src/engine/edu/playtest.ts:151 timeoutMs default 300_000; by hand random seed 5 accuracy 0.55 took 422 s (368 steps, 201 right/167 wrong, finished, 0 console errors, ok). Needs the timeout fix, then edu_run_pipeline {restart:true, from:'playtest'} (build/lint need not rerun).
- Lint (rebuild, studio now has EGS-50): 0 errors, 2 warnings, both ENC_ANSWER_NOT_IN_ARTICLE (hunts u1-q1, u3-q1, "in en"). Decision: ACCEPT. The en answer is a full English sentence (e.g. "Three: masculine, feminine and neuter") and the article is German taught text, so the heuristic cannot match; hunt still points to the right article. No content change.
- Bot by hand: perfect ok (48/48, finished), wrong ok (0/24, review reached), random seed 5 ok. Verb drill step (quiz-arena.mjs: button present iff verb units, round kind 'verbs', played to summary) ran inside perfect/random with no failure.
- Editions: languages [hr,en], game-data catalogs de(123)/en(275)/hr(275), defaultLang hr; verb unit u2 (extensions.language.verbUnits), 4 conjugation items; taught forms exist only in the de catalog (u2-q1 ich accepted ["mache"]), so hr<->en cannot change German answers. Playwright: lang-picker Hrvatski/English switches the title (checked title only).
- Matcher (match.ts, lang de, policy strict): Maedchen and Strasse correct+translit note; Madchen wrong (diacritics); Strase typo accepted; mädchen caps note.
- Voice: status 8/8 clips made (vibetts), 0 placeholders, de provider vibetts; gemini down, quota 0/10; no clip made, no plan rerun.
