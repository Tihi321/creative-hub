# HUB-22 changelog

Status 2026-11-01: code merged, live check run with the client model ($0). Not played by the user.

## Merged in `Tihi321/edu-game-studio` (PR / merge order)
- EGS-26 German matching (#26), EGS-25 shared start screen (#27), EGS-28 German verb table (#28), EGS-32 editions step (#29), EGS-29 language formats and brief (#23), EGS-33 German voices (#25), EGS-35 reader, glossary, passage panel (#24), EGS-27 conjugation kind (#31), EGS-30 German writer prompts (#32), EGS-31 verb drill (#33), EGS-37 B2 grammar incl. Konjunktiv I (#34), EGS-36 B2 format, readings, harvest, self-check (#35), EGS-38 listening passages (#30), EGS-34 German UI (#36).
- Found and fixed during the live check: EGS-47 seed history (#37), EGS-48 stale UI test (#38), EGS-49 word-bank cloze no typo (#39), EGS-50 no reading lint on A1 (#40), EGS-51 reader markup (#41), EGS-52 playtest bot timeout 300 s to 900 s with a clear message (#42), EGS-53 verb table variants, lint fixes, design prompt, four verbs (#43), EGS-54 roadmap row for the slow bot (#44).
- Hub: ROADMAP rows HUB-22 and HUB-23, make-edu-game skill, run logs (this PR).

## Live check results (details in `runs/deutsch-*.md`)
- Start screen: `suncev-sustav` rebuilt; bot perfect OK in quiz-arena, encyclopedia, mindmaze, rpg; title is the shared `menu` look, in-game screens keep their themes (seen at 1280x800 for mindmaze). 390x844 NOT looked at.
- `deutsch-a1-pilot` (hr+en, de, 4 units, verb unit u2 with sein/haben/machen/wohnen): published, score 7.89; editions [hr,en] with three catalogs; bot perfect/wrong/random(seed 5) OK; verb drill ran; matcher checked at module level (Maedchen/Strasse accepted with note, Madchen wrong); 8 German clips made by VibeTTS supertonic:M2 (0 Gemini). Lint 0 errors, 2 warnings (ENC_ANSWER_NOT_IN_ARTICLE, accepted: hunt answers are English sentences).
- `deutsch-a2-smoke`: published, lint 0/0, perfect/random bots OK (2 local voice clips by mistake: voice was left on).
- `deutsch-b1-smoke`: published, lint 0/0, 4 Praeteritum + 2 Konjunktiv II conjugation items, bots OK.
- `deutsch-b2-smoke`: published (score 8), 4 readings 394-424 words, 63 harvested cards, 16 glosses per text, lint 0 errors / 4 CONJ_VERB_UNKNOWN (verbs now in the table, EGS-53), bots OK, reader fixed (EGS-51).
- Full suite on master before the live fixes: 2022/2024 (two stale tests, fixed by EGS-47/48), pipeline-run restart test excluded (times out on clean master, pre-existing; HUB-24 owns it). Engine/electron/player/live builds OK.

## DONE / NOT DONE / UNTESTED
- DONE: all fourteen tickets EGS-25..38 merged; hr+en editions in one run; verb units, conjugation kind, verb drill; B2 reader, glossary, harvest, self-check, B2 grammar (Konjunktiv I included); German voices (local VibeTTS), listening passages code; UI strings de; seed history; hub skill and ROADMAP rows.
- NOT DONE: role-play generator (HUB-23 / EGS-39, planned follow-up only); C1/C2 (out of scope); native review of any German.
- UNTESTED: the user playing `deutsch-a1-pilot` (a production is done only when played); look of the start screen at 390x844; matcher notes on screen in the browser; hr<->en prompt change inside a round in the browser; listening passages (EGS-38) with real audio; self-check card on screen; B2 realism of the texts; Passiv forms for verbs outside the verb table; EGS-53 item (c) only seen indirectly (the playtest report prompt showed the fresh lint, 2 warnings, not the 12 the lint step reported).

## Plan correction
The conjugation contract example put `given` outside `forms`; the real schema has it inside (plan fixed).

## Follow-ups (not built)
HUB-23 role-play generator; EGS-54 bot speed (about 0.9 s per answer); accessibility review renders empty answers for typed/conjugation items (reads only the edition catalog); no child-safety review step ran; no modal-verb facts in the fact base; clients tasks reset on restart are re-leased (FYI); HUB-24 test diet (EGS-40..46).
