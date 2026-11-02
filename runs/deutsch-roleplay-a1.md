# deutsch-roleplay-a1 (HUB-23 live check item 1)

Started 2026-11-02. Edu Studio master 0f78fb8 (EGS-39, EGS-55, EGS-56, EGS-57), built with `hub.ps1 build edu-studio` and started with `hub.ps1 start edu-studio`.

## Brief

- Topic: German for beginners; audience: Croatian and English speaking adults starting German
- Course slug: `deutsch-roleplay-a1`; format `language-a1`, 4 units, cefr A1, targetLang de, sourceLang hr, languages [hr, en]
- Shells asked: quiz-arena (roleplay expected to be enabled by the scenes stage, D3)
- Art off, music off, voice provider auto (German listening clips local; no scene audio, out of scope)
- Model: client/claude-code for every role ($0)

## Ids

| Tool | Id |
|---|---|
| Edu Studio course | deutsch-roleplay-a1 |
| Pipeline run | 1 |

## Log

- 2026-11-02 Seeds checked: `~/EduGames/prompts/scene-writer/{scenes,scenes_revise}.md` present, `config/formats.md` has `roleplay: true` on the four language formats.
- 2026-11-02 Voice quota before the run: 0/10 used (day 2026-11-02, America/Los_Angeles).
- 2026-11-02 First edu_run_pipeline call put `slug` inside `brief` (ignored), which made course `german-for-beginners`; its job was dropped (`edu_stop_now {drop, slug}` then `edu_resume_all`) and the folder deleted. Run restarted with top-level `slug`.
- 2026-11-02 Unrelated: `deutsch-a1-pilot--summarize--all--r4` client task left waiting from an earlier session; not touched.
- 2026-11-02 Plan, 4 web searches (worker, 13 pages), 4 research notes (47 facts), curriculum (u2 = verb unit), scope (u2 verbs sein, haben, wohnen, kommen, lernen, heißen; praesens A1) answered by the session; articles, items, distractors, fact_check (all pass, accuracy 9), explain, accepted for u1-u4 answered by two worker subagents (one rejected submit: u1-q7 options Sie/sie read the same, fixed to ihr).
- 2026-11-02 **BUG (EGS-58 candidate): the `scenes` jobs stayed `queued` forever.** The data folder had no `scene-writer` agent: `initDataFolder` copies `seed/agents/` only when `agents/` does not exist yet (`src/engine/store/dataFolder.ts`), and no seed migration adds the new starter agent `scene-writer-nina-hartmann.md` to an existing data folder. Workaround for this live check: copied `seed/agents/scene-writer-nina-hartmann.md` into `~/EduGames/agents/` by hand; the four scenes jobs started within 20 s. No code changed.

- 2026-11-02 Scenes (session): u1-hotel (Sie, Frau Weber, evening check-in then breakfast), u2-sprachcafe (du, Pablo), u3-cafe (Sie, waiter Jonas, Vienna), u4-foto (du, Mia's family photo), finale (du, Mia's birthday, new speaker Paul). New reply items rp-u1-1, rp-u1-2, rp-u2-1..3, rp-u3-1..2, rp-u4-1..2. Generator refusals (repair rounds): u2 used 1 of 7 vocabulary terms (needs 4), rewritten (Pablo from Spain instead of Lukas); u3 used 6 of 14 (needs 7), Tee/Wasser/Bitte schön added. 4 parallel scene calls each saw "(none)" speakers and each listed the learner `you`; the merge kept one, no error.
- 2026-11-02 scenes_check verdicts (session as fact-checker): u1 pass 9, u2 pass 9, u3 pass 8 (Was kostet das? is vocabulary, not a fact), u4 pass 8 (eine Schwester / meine Eltern from scope grammar, not a fact), finale pass 9. scenes_accepted: rp-u1-2 + "Guten Morgen, Frau Weber"; rp-u2-1 + "Ich lebe in Zagreb."; rp-u4-1 + "Ich habe eine Schwester.", "Ja, eine Schwester.".
- 2026-11-02 Design: shells quiz-arena + encyclopedia (roleplay deliberately NOT named, to test D3), round 8, boss 12, timer 40 s. Assemble enabled roleplay anyway: pack shells = quiz-arena, encyclopedia, roleplay (D3 confirmed). Assemble note: garden 10 words, fewer than 4 for u2, u3, u4 (fewer than 13 overall).
- 2026-11-02 review_accessibility r1 revise (6 texts: u4-q7 whys, u3-q2 hint "-ßig", u2-q5 expl, two articles), polish-k2, r2 pass 9/8. Voice plan: narration off, 8 German listening items derived (u1-q2, rp-u1-1, rp-u2-3, rp-u2-1, u3-q6, rp-u3-1, u4-q2, rp-u4-2); voice_generate "8 clip(s) spoken (vibetts 8), de: vibetts" (VibeTTS answered even though `hub.ps1` status listed it down; hub status also showed edu-studio down while it served calls). Gemini: 0 requests, quota still 0/10 used after the run.
- 2026-11-02 Editions (worker): 7 translator chunks, en 398 texts, 189 taught de texts kept. Build 13 files, lint clean (1 warning), pipeline playtest 5 personas all passed, playtest_report pass, publish (score 8.64), summarize. **Pipeline stage: published.**
- 2026-11-02 Fixes after publish (session, data folder only): u2-q7 conjugation (wohnen) asked er and ihr (both wohnt): ihr now given, Sie asked (CONJ_FORM_DUPLICATE_AMBIGUOUS gone). Paul (Mia's brother, u4 l3) was 20 with a 4-year-old daughter in the finale: now "Er ist dreißig" (de, hr, en). **Item-writer issue:** u1-q3, u1-q6, u1-q9 cloze texts and u1-q5 group g2 were Croatian sentences stored in the German catalog (`de.json`), so the en edition would have shown Croatian; moved to hr.json and en.json (English written by the session) and removed from de.json. Rebuilt: lint 0 errors, 0 warnings.

## Checked

- Pack: languages [hr, en], targetLang de; shells quiz-arena, encyclopedia, roleplay; 5 scenes: u1-hotel, u2-sprachcafe, u3-cafe, u4-foto 10 lines / 4 replies each, finale 14 lines / 6 replies, no unit; every unit has a typed reply (rp-u1-2, rp-u2-1, u3-q1, rp-u4-1); garden present (10 words); 56 items in the pack (39 unit items, 9 rp items, 8 listening items).
- Catalogs: German say lines only in de.json (e.g. rp.sc.u1-hotel.l1); translations and help in hr.json and en.json; build game-data catalogs de 185, hr 402, en 402.
- edu_lint after fixes: 0 errors, 0 warnings (no RP_* warning).
- Bot (play.mjs, roleplay): perfect ok, 24 steps, 24 right, finished, 5 scenes, garden 10 plants, 0 console errors, 95 s; wrong ok, 24 wrong, help shown 8 times (recovery), whys 15, explanations 24, scene-done reached, never dead-ended, 0 console errors, 48 s (finished false is expected for always-wrong); random ok, 6 scene plays, recovery 7, garden 10, 0 console errors, 128 s. Quiz arena perfect rerun after fixes: 47/47, finished, 0 errors, 58 s. Pipeline playtest (before fixes): perfect, wrong, strong, average, struggling all passed.
- Voice: quota 0/10 used before and after; no Gemini request; no scene audio planned or made (bot: roleplay clips 0); 8 German listening clips by VibeTTS.

## Not verified

- The German dialogue, the Croatian help and the English translations: model-written, no native review.
- Real audio of the 8 clips (files exist; nobody listened), touch, a human playing. The user has not played it.

## Left to do

- The user plays the role-play mode (build: `~/EduGames/courses/deutsch-roleplay-a1/build/index.html`).
- EGS-58 in edu-game-studio: the scene-writer starter agent never reaches an existing data folder (fix in `initDataFolder` or a seed migration that adds missing starter agents for new roles); the item-writer put Croatian cloze texts in the German catalog (`taught` set on items whose text is in the course language).
