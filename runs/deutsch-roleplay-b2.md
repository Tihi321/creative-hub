# deutsch-roleplay-b2 (HUB-23 live check item 2)

Started 2026-11-02, after `deutsch-roleplay-a1` was published. Same Edu Studio process (master 0f78fb8) and the same hand-copied `scene-writer` agent (see the A1 log, EGS-58 candidate).

## Brief

- Topic: German at B2: work, media and society; audience: Croatian and English speaking adults at upper-intermediate (B2) level
- Course slug: `deutsch-roleplay-b2`; format `language-b2`, 2 units, cefr B2, targetLang de, sourceLang hr, languages [hr, en]
- Shells asked: quiz-arena; art off, music off, voice provider auto; story none
- Model: client/claude-code for every role ($0)

## Ids

| Tool | Id |
|---|---|
| Edu Studio course | deutsch-roleplay-b2 |
| Pipeline run | 1 |

## Log

- 2026-11-02 Plan (session): u1 "Radni svijet" (holiday law, Working Hours Act, polite requests and complaints with Konjunktiv II), u2 "Konjunktiv I: neupravni govor u vijestima" (verb unit). 2 web searches (worker): gesetze-im-internet.de BUrlG §1, §3, ArbZG; de.wikipedia Konjunktiv, Indirekte Rede; mein-deutschbuch.de. 18 facts. Note: the ArbZG excerpt did not carry § 3 (8-hour day), so the course states no daily limit.
- 2026-11-02 Curriculum (session): u2 = verb unit. Scope: u2 verbs sein, haben, werden, können, sagen, kommen (konjunktiv1, B2).
- 2026-11-02 Unit content (articles/readings, items, distractors, fact_check, explain, accepted) handed to two worker subagents.
- 2026-11-02 Run 1: articles (2 readings per unit, about 400 words), items (u1 32, u2 29), distractors, fact_check u1 revise then pass (k2), u2 revise twice -> **blocked at `fact_check-k2:u2`** (the second revise was only a Croatian typo "treće osoba" in u2-q29). The two background workers then stopped (rate limit). Fix: typo corrected in `pipeline/units/u2/items.json` ("treća osoba"), `edu_run_pipeline {restart, from: fact_check}` -> run 2.
- 2026-11-02 Run 2: fact_check u1 and u2 pass 9 (session); explain u1/u2 and accepted u1 (foreground worker); accepted u2 (session; a stale lease from the dead worker released by hand).
- 2026-11-02 Scenes (session), 2 per unit: u1-urlaubsantrag (Sie, Frau Krämer, holiday request with Konjunktiv II and the legal claim), u1-ueberstunden (du, colleague Jana, advice with Konjunktiv II, Arbeitszeitgesetz), u2-redaktion (Sie, editor Herr Brandt, reported speech: sei, habe, hätten), u2-bahnhof (du, Tobias, komme, könne, sei, hätten); finale (Sie, Herr Brandt, mixes both units, 13 lines, 6 replies). New reply items rp-u1-1..4, rp-u2-1..4. Generator refusal: u1-ueberstunden mixed du and Sie (Jana quoted "Hätten Sie kurz Zeit?", option "An Ihrer Stelle") -> rewritten. scenes_check: u1 pass 8, u2 pass 9, finale pass 9. scenes_accepted: rp-u1-1 g2 könnten/würden; others canonical only.
- 2026-11-02 Design (session): quiz-arena + encyclopedia (roleplay not named), round 8, boss 12, timer 60 s. Assemble: 61 items, 4 articles; garden 4 words, none for u2. Harvest: 51 vocabulary cards. review_accessibility (foreground worker) r1 revise (8 texts incl. u1-q6 typo "Paru", u2-q23 answer given away), polish, r2 pass 9/9. Voice plan (session): narration off, 6 German listening items; voice_generate "6 clip(s) spoken (vibetts 6)". Editions (foreground worker): 11 chunks, en 640 texts, 357 taught de texts kept.
- 2026-11-02 Run 2 lint: **1 error DISTRACTOR_DUPLICATE** u2-q14 word bank: "waren" and "wären" count as the same word (umlaut folding); bank word changed to "seien" (`edu_text_set de`), restart from build -> run 3: lint clean (1 warning READING_SENTENCE_LENGTH a-u1-2, 11.7 words average vs 12-26), pipeline playtest 5 personas passed, playtest_report pass, publish, summarize. **Stage: published.**
- 2026-11-02 **Role-play bot perfect FAILED** after publish: "scene u2-redaktion / u2-bahnhof: the scene-done screen lists no planted words". Cause: the garden derived in code had no word for u2 (its scope vocabulary is phrases like "Er sagte, er sei ..." that no reply answers). Fix in the data folder: 3 garden words added for u2 (`sei` <- u2-q4, `habe` <- rp-u2-1, `komme` <- rp-u2-3, glosses in hr and en) with `edu_course_edit` + `edu_text_set`; rebuilt. **Generator gap (EGS-58 candidate):** a unit whose vocabulary is phrases gets an empty garden, and the bot then fails every perfect scene of that unit.

## Checked

- Pack: languages [hr, en], targetLang de; shells quiz-arena, encyclopedia, roleplay (D3 again); scenes u1-urlaubsantrag 10 lines / 4 replies, u1-ueberstunden 9 / 3, u2-redaktion 10 / 3, u2-bahnhof 10 / 4, finale 13 / 6 (no unit); typed replies per unit: rp-u1-1, rp-u1-3 (cloze, no bank), rp-u2-1, rp-u2-3 (cloze, no bank); Konjunktiv II replies (u1-q12, u1-q15, rp-u1-1..3) and reported-speech replies (u2-q4, u2-q6, u2-q18, rp-u2-1..4); garden 7 words; 126 items in the pack (61 unit items, 8 rp items, 51 cards, 6 listening).
- edu_lint final: 0 errors, 1 warning (READING_SENTENCE_LENGTH a-u1-2).
- Bot (play.mjs, roleplay, after the garden fix): perfect ok, 20/20, finished, 5 scenes, 7 plants, 0 console errors, 70 s; wrong ok, 30 wrong, help shown 14 times, never dead-ended, 0 console errors, 65 s; random ok, 27 right / 4 wrong, finished, 0 console errors, 104 s. Quiz arena perfect: 30 steps, finished, 0 errors. Pipeline playtest (run 3): perfect, wrong, strong, average, struggling all passed.
- Voice: Gemini quota 0/10 used after the run; no Gemini request; no scene audio; 6 German clips by VibeTTS.

## Not verified

- The German readings and dialogue, the Croatian help and the English edition: model-written, no native review.
- Real audio, touch, a human playing. The user has not played it.

## Left to do

- The user plays one scene (build: `~/EduGames/courses/deutsch-roleplay-b2/build/index.html`).
- EGS-58: empty garden for phrase vocabulary; umlaut-folded word-bank duplicates (wären/waren, würden/wurden) that writers cannot see coming; the scene-writer agent missing from existing data folders (A1 log).
