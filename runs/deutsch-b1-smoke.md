# deutsch-b1-smoke (HUB-22 live check item 4, B1 half)

## Brief
topic "German for intermediate learners: opinions, plans and stories (Praeteritum and Konjunktiv II)"; audience hr+en adults; sourceLang hr; languages [hr,en]; targetLang de; cefr B1; format language-b1; units 2; shells quiz-arena + encyclopedia; story none; model client/claude-code (all model tasks answered by the client model Claude); media: art off, music off, voice `{enabled:false}` (the real key). No Gemini, no paid model, no voice generated, Scriptorium not touched.

## Ids
Course dir `~/EduGames/courses/deutsch-b1-smoke`. Run 1 jobs `deutsch-b1-smoke--<step>--...--r1`; run 2 (restart from lint) `deutsch-b1-smoke--lint--all--r2`, `--playtest--all--r2`. Fact base 26 facts / 4 sources (de.wikipedia Praeteritum, Konjunktiv; de.wiktionary Flexion:sein, Flexion:haben). 2 units (both verb:true), 6 objectives, 4 readings, 43 questions + 34 glossary flashcards.

## Decisions
- Both units are verb units; verbs chosen: sein, haben, gehen, kommen, machen, sehen (praeteritum) and sein, haben, kommen, gehen, koennen, machen (konjunktiv2).
- Fact check: I passed both units with accuracy 8 and listed minor gaps in the notes (kommen du/wir/ihr forms, two example sentences, two interpretive sentences in the readings are not in a fact).
- Lint of run 1 found 12 CONJ_FORM_MISMATCH: (a) "wärst" for du (table has only "wärest"), (b) "würde sein"/"würde haben" as konjunktiv2 forms (table accepts only wäre/hätte). Worked around by hand: u2-q7, u2-q8 removed; u2-q6 du set to [wärest, wärst] via edu_item_update. Then lint (rebuild) = 0 errors, 0 warnings.
- Run 1 publish stayed blocked on the stale lint snapshot, so I restarted from `lint` (run 2).

## Checks done
- Lint after fix: 0 errors, 0 warnings. Conjugation items: u1 praeteritum (4), u2 konjunktiv2 (2); no CONJ_FORM_MISMATCH. pack languages [hr,en], targetLang de, extensions.language.verbUnits [u1,u2].
- Autoplay bot, quiz-arena, from edu-game-studio: `--mode perfect` ok (34/34 right, finished, 0 console errors); `--mode random` ok (failures []).
- Engine playtest r1: 5 bots passed (perfect, wrong, strong, average, struggling 151 steps).

## Not verified
German not natively reviewed (model-written; fact base thin: no haben/modal Praeteritum, no haben Konjunktiv II hätte). Encyclopedia shell/reader not played. Run 2 playtest and publish result not seen (edu-studio MCP disconnected). No human played it.

## Odd things
Item-writer prompt demands würde+inf and the conjugation kind allows it, but the verb table rejects würde+sein/haben; table lacks wärst. Design prompt says only quiz-arena exists though the encyclopedia shell was requested. Research/repair rounds flag a wiki oldid number as a missing fact. Pipeline summarize/playtest report run before the manual fix (stale lint); fact_check for tfng options requires a `why` on the wrong `t`.
