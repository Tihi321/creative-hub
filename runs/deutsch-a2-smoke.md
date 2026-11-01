# German A2 smoke course (HUB-22 live check, item 4)

Started 2026-11-01. Slug `deutsch-a2-smoke`, Edu Studio port 7463, all model work by the Claude Code session (client/claude-code, no paid model, no Scriptorium, no Gemini).

## Brief

- Idea / theme: German for elementary learners, everyday situations and the Perfekt
- Kind: language course A2, format `language-a2`, 2 units, shells quiz-arena + encyclopedia
- Languages: sourceLang hr, languages [hr, en], targetLang de
- Art: off. Music: off. Voices: not switched off in the brief (see Log)

## Ids

| Tool | Id |
|---|---|
| Edu Studio course | deutsch-a2-smoke (run 1 aborted on stale server, run 2 = final) |
| Build | C:\Users\Infplane\EduGames\courses\deutsch-a2-smoke\build |

## Log

- Run 1 failed at start: `no course format "language-a2"` (data folder had old seeds). Seeds copied from edu-game-studio\seed to ~/EduGames (backup in .claude/temp/edu-data-backup). The server was also stale (started 11:27, before the build); restarted by another session. Run 1 jobs discarded.
- Run 2 (`restart:true, from:'plan'`): 34 jobs done, 0 failed. Prompts carried {{language_rules}} and the verb-unit instruction; the `editions` step ran (en: 150 texts, 85 taught de texts left; languages hr+en).
- Fact check u2 round 1: revise (bleiben unsupported by facts, kaufen explanation wrong); items corrected; round 2 pass.
- Voice: the pipeline planned and generated 2 German listening clips with local VibeTTS (vibetts 2). Not wanted by the brief; no Gemini, no quota spent. Brief did not set media.voice off.
- Pack: 31 items, conjugation x7 (praesens x3 modals; perfekt x4: machen, gehen, aufstehen, fahren), verbUnits [u1,u2].

## Checked

- Finishes: DONE (publish step answered).
- edu_lint: 0 errors, 0 warnings (no CONJ_FORM_MISMATCH).
- Pipeline playtest: 5 simulated learners passed; playtest_report pass.
- Bot (cwd edu-game-studio, `node scripts/play.mjs <build> --mode perfect|random --shell quiz-arena`): perfect ok, random ok, no failures.

## Not verified

- German correctness is model-written, no native review; no human played it.
- Language switch hr/en in the browser, listening clip playback, encyclopedia shell, Verb drill button not looked at.

## Bugs / notes

- Review text for accessibility showed empty "answer:" lines for typed and conjugation items (taught answers live in de.json; the renderer seems to read only the edition catalog).
- Fact base has no modal-verb facts, so u1 conjugation items cite only CEFR facts.
- The prompt for the `design` task still says the player has only quiz-arena.
- No child-safety review step appeared in the run.
