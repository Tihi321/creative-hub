# deutsch-b2-smoke (HUB-22 live check item 5)

Started 2026-11-01. Copy this file to `runs/<slug>.md` for each production.

## Brief

- Idea / theme:
- Kind: linear | choices · adults | children
- Languages:
- Art: illustrated | pixel · Music: comfy | chiptune (<chip>) · Voices: off | on

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | |
| Scriptorium book | |
| Book Translator project | |
| VN Studio project | |

## Video (only for a short film or cartoon, skill make-video)

- Format: short-film | cartoon | kids-cartoon · Aspect: 16:9 | 9:16 · Runtime (s):
- Screenplay: story / book slug, `runs/<slug>/video/screenplay.json`
- Video model: omni-720p | omni-360p | veo-lite · Budget (Flow credits): 150 · Spent:
- Flow project: · Credits before / after (`flow_status`):
- Plan: `runs/<slug>/video/plan.json` (shot ids, keyframe media ids, clip files, voices)
- Animatic OK from the user (date) · Songs asked and made · Final MP4:

## Log

- <YYYY-MM-DD HH:MM> what was done, result

## Checked

- what was looked at or played, by whom

## Left to do

-

- 2026-11-01 first run_pipeline failed: data folder formats.md had no language-b2 (seed not refreshed); retried after refresh, created, run 1.
- 2026-11-01 INVALID (old code): the running Edu Studio was pre-HUB-22 (editions step said "skipped ... Book Translator later"; scope prompt had an empty "Language rules" block). Run 1 got through plan, research (4 web searches answered), factbase (31 facts), curriculum (2 units, 6 objectives), scope; stopped at articles. Stopped on request of another session; nothing after this was run. Redo after restart from master.
- 2026-11-01 restarted studio from master; run 2 started (restart from plan). Run 1 results above are void.
- 2026-11-01 run 2: {{language_rules}} filled incl. B2 reading rules (confirmed in scope/articles/items prompts); verb unit = 1 (u2, Passiv/Konjunktiv II). plan..items done: 4 readings (a-u1-1, a-u1-2, a-u2-1, a-u2-2), 43 items. Now distractors.
- 2026-11-01 run 2 state at stop: all steps done through harvest (63 glossary cards), voice_plan (0 clips), voice_generate (0). `editions` step in progress: translator batches submitted up to call 8 (batches 3-7 were answered by a helper agent that hit the usage limit; unverified). 106 items (67 flashcards = 63 harvested + 4 self-check). Readings: a-u1-1, a-u1-2, a-u2-1, a-u2-2 (~330-420 words each by estimate, NOT counted by script). Fact-check pass x2 (accuracy 8), accessibility pass.
- 2026-11-01 edu-studio MCP disconnected after submitting editions batch 8 (edu_wait: "connection closed"); status unreachable. Not resumed. Remaining: finish editions, review/build/lint/playtest, then all item-5 checks (word counts, lint, bots, gloss screenshot, en edition).
- Observations: (1) first server was pre-HUB-22 (restarted). (2) The design prompt says "shells the player has today: quiz-arena" although encyclopedia was asked; I returned both, unverified whether the encyclopedia shell is in the built pack. (3) Fact base is thin on unit 2 hours (years of Destatis values unknown).
- 2026-11-01 run 2 finished through build/lint/playtest (5 learners passed); editions: en 440 texts, 272 taught de texts untouched; languages [hr,en]. playtest_report job queued (not a client task).
- Checks: reading words (no headings/citations) a-u1-1 424, a-u1-2 412, a-u2-1 399, a-u2-2 394; mean sentence ~14 words. Glossary entries 16/16/15/16 (63 harvested cards), hr+en glosses present for all 63. edu_lint: 0 errors, 4 warnings, all CONJ_VERB_UNKNOWN (erheben, fördern, unterstützen, verkürzen not in the verb table). Bots (play.mjs, seed 1): quiz-arena perfect 34/34 ok, random 32/44 ok; encyclopedia perfect ok (reader: 4 chapters, 4 taps, 4 read, deck 1, practice 18 answers, passages opened 24/24), random ok (passages 30/30). Screenshots: .claude/temp/b2-gloss-popover-en.png, b2-title-en.png.
- BUG (edu-game-studio, reader view): the article body is shown with literal "## " heading markers (drop cap lands on "##") and citations as literal "[1]". Seen at 1280x800 in encyclopedia reader chapter 1.
- Not verified: German realism; self-check card back shown in a real screen (bot flashcards only); the 4 Passiv verbs are unknown to the verb table so their forms were NOT mechanically checked.
