# Audiobooks, English, 2026-11

Goal: English audiobooks, Kokoro voices through VibeTTS (port 7723), $0, for published prose books in `C:/Users/Infplane/Scriptorium/books/`. Updated after every book. Generated from `.claude/temp/audiobooks/results.json` (work folder: scripts prep.mjs, assemble.mjs, mklog.mjs).

## Decisions

- Output folder: `books/<slug>/out/audio/` (`<slug>-chNN.mp3` plus `<slug>.m3u`). Why: Scriptorium's rebuild never clears `out/` as a whole. Code check in scriptorium/src: books.ts writes only article.html/md, cover.png/html, `<slug>.epub`, `-gamebook.epub/pdf`; `writeReaderDir` removes only `out/reader` and `out/draft`; pipeline.ts removes only `out/cover.png`. No code lists or empties `out/`.
- Text: chapters `ch-NN.md` in order; front matter, markdown marks, HTML comments, [n] citation marks, SCENE/ON SCREEN lines (picture books) removed. Read: "<Title>. By <byline>." (byline from book.md, else the author name the book shows), then "Chapter N. Title." (Blink N for blinks) per chapter, then text. Single-chapter books (picture books, bedtime story, article) get no chapter heading.
- Pauses: 1.5 s silence (ffmpeg anullsrc) after the book title, after each chapter heading and at the end of each chapter. Paragraphs: the engine itself leaves about 0.6-0.9 s between paragraphs and about 0.4 s between sentences (measured with silencedetect), so no extra paragraph silence was added.
- Speed: 1.0 for stories; 0.9 for kids' books, blinks and the article. Output MP3 re-encoded 44.1 kHz mono 64 kbps.
- Duration check: expected = words / (185 wpm x speed); flag outside 60-160% of expected (body audio only).
- I cannot listen. Only file existence, ffprobe durations and the duration ratio were checked.
- Voice never uses bf_emma, af_heart or bm_george.

## Book list

| slug | format | words (chapters) | status |
|---|---|---|---|
| circuit-breaker | novella | 35303 (10) | DONE |
| circuit-breaker-2 | visual-novel | 22957 (10) | SKIPPED: format visual-novel is an adaptation script |
| echoes-in-the-deep | novella | 36335 (10) | DONE |
| echoes-in-the-deep-2 | visual-novel | 25043 (10) | SKIPPED: format visual-novel is an adaptation script |
| fifty-minutes-of-common-sense | linked-collection | 45379 (15) | DONE |
| france-s-atomic-clock-on-air-the-als162-signal-t | article | 1243 (1) | DONE |
| rust-and-ruin | novella | 33345 (11) | DONE |
| the-automaton-who-confessed | novella | 32392 (15) | DONE |
| the-bell-and-the-bicycle | kids-picture-book | 588 (1) | DONE |
| the-clock-on-the-hill | idea-fable | 2315 (1) | SKIPPED: sources being replaced (director) |
| the-clockless-god | novella | 50770 (18) | DONE |
| the-clockless-god-2 | choice-visual-novel | 25778 (16) | SKIPPED: not prose (see Notes) |
| the-clockless-god-3 | visual-novel | 20739 (9) | SKIPPED: format visual-novel is an adaptation script |
| the-clockwork-compass | novella | 47453 (13) | DONE |
| the-cold-furnace | novella | 29241 (19) | DONE |
| the-echo-between-stars | choice-visual-novel | 21583 (12) | SKIPPED: not prose (see Notes) |
| the-egg-that-wasnt | kids-choice-visual-story | 4359 (10) | SKIPPED: not prose (see Notes) |
| the-glass-horizon | choice-visual-novel | 23909 (9) | SKIPPED: not prose (see Notes) |
| the-gravity-garden | choice-visual-novel | 22555 (11) | SKIPPED: not prose (see Notes) |
| the-hour-that-happens-twice | novella | 51403 (18) | DONE |
| the-iron-root | novella | 52570 (14) | DONE |
| the-light-at-worlds-end | novella | 32417 (11) | DONE |
| the-lighthouse-that-kept-lists | short-story | 5782 (4) | DONE |
| the-lighthouse-that-kept-lists-2 | short-film | 1031 (2) | SKIPPED: format short-film is an adaptation script |
| the-lighthouse-that-kept-lists-vn | visual-novel | 13691 (6) | SKIPPED: format visual-novel is an adaptation script |
| the-local-patch | short-story | 7721 (5) | DONE |
| the-local-patch-2 | visual-novel | 11335 (5) | SKIPPED: format visual-novel is an adaptation script |
| the-local-patch-3 | short-film | 1052 (2) | SKIPPED: format short-film is an adaptation script |
| the-one-way-street-why-time-only-runs | science-blink | 3558 (9) | DONE |
| the-perfect-alibi | novella | 31380 (20) | DONE |
| the-plain-title-page | idea-fable | 2176 (1) | SKIPPED: sources being replaced (director) |
| the-poisoned-well-of-harrowdale | novella | 35252 (18) | DONE |
| the-rooster | novella | 26396 (14) | DONE |
| the-salt-line | novella | 34454 (11) | DONE |
| the-salt-line-2 | visual-novel | 23018 (9) | SKIPPED: format visual-novel is an adaptation script |
| the-saltwater-spy | novella | 41573 (10) | DONE |
| the-sand-courier | novella | 34999 (11) | DONE |
| the-second-window | idea-fable | 2277 (1) | SKIPPED: sources being replaced (director) |
| the-silence-above-the-snowline | novella | 34527 (10) | DONE |
| the-silent-signal | novella | 25435 (10) | DONE |
| the-silent-signal-2 | visual-novel | 21284 (10) | SKIPPED: format visual-novel is an adaptation script |
| the-silent-summit | novella | 32068 (10) | DONE |
| the-silent-summit-2 | visual-novel | 21048 (8) | SKIPPED: format visual-novel is an adaptation script |
| the-snail-and-the-salad | kids-picture-book | 618 (1) | DONE |
| the-soother-in-the-mountains | kids-choice-visual-story | 5753 (10) | SKIPPED: not prose (see Notes) |
| the-soother-stone | kids-choice-visual-story | 5122 (7) | SKIPPED: not prose (see Notes) |
| the-soother-that-fell-into-dragon-land | kids-choice-visual-story | 5793 (7) | SKIPPED: not prose (see Notes) |
| the-soothers-long-way-home | kids-choice-visual-story | 5522 (8) | SKIPPED: not prose (see Notes) |
| the-storm-chaser-s-secret | novella | 33305 (10) | DONE |
| the-tide-table | short-story | 7622 (5) | DONE |
| the-trap-room-at-the-lanterna | mystery-puzzle-visual-novel | 6236 (4) | SKIPPED: not prose (see Notes) |
| the-umbrella-conductor | bedtime-story | 1755 (1) | DONE |
| the-winter-garden-clock | mystery-puzzle-visual-novel | 6294 (4) | SKIPPED: not prose (see Notes) |
| what-fate-decides-luck-will-and-the-life | idea-blink | 3738 (8) | DONE |
| where-the-soother-went | kids-choice-visual-story | 3355 (9) | SKIPPED: not prose (see Notes) |
| windward-drift | novella | 35771 (10) | DONE |

## Voice map

| slug | voice | speed |
|---|---|---|
| the-bell-and-the-bicycle | af_sky | 0.9 |
| the-snail-and-the-salad | am_puck | 0.9 |
| the-umbrella-conductor | bf_lily | 0.9 |
| the-one-way-street-why-time-only-runs | af_alloy | 0.9 |
| what-fate-decides-luck-will-and-the-life | bm_daniel | 0.9 |
| france-s-atomic-clock-on-air-the-als162-signal-t | af_jessica | 0.9 |
| the-lighthouse-that-kept-lists | bf_alice | 1 |
| the-local-patch | am_liam | 1 |
| the-tide-table | bf_isabella | 1 |
| fifty-minutes-of-common-sense | bm_lewis | 1 |
| the-rooster | bf_isabella | 1 |
| circuit-breaker | af_nova | 1 |
| echoes-in-the-deep | am_fenrir | 1 |
| rust-and-ruin | af_river | 1 |
| the-automaton-who-confessed | bm_daniel | 1 |
| the-clockless-god | bm_fable | 1 |
| the-hour-that-happens-twice | bm_fable | 1 |
| the-clockwork-compass | af_aoede | 1 |
| the-cold-furnace | am_adam | 1 |
| the-iron-root | af_bella | 1 |
| the-light-at-worlds-end | am_michael | 1 |
| the-perfect-alibi | am_echo | 1 |
| the-poisoned-well-of-harrowdale | am_eric | 1 |
| the-salt-line | af_nicole | 1 |
| the-saltwater-spy | af_kore | 1 |
| the-sand-courier | af_sky | 1 |
| the-silence-above-the-snowline | am_onyx | 1 |
| the-silent-signal | am_adam | 1 |
| the-silent-summit | af_nicole | 1 |
| the-storm-chaser-s-secret | af_jessica | 1 |
| windward-drift | am_puck | 1 |

Shared voices: the-clockless-god and the-hour-that-happens-twice share bm_fable (same detective, Dec Hartley). Other voice repeats are deliberate (31 books, 24 voices left after the three pilots). The six soother books are skipped (see Notes), so their single voice was not needed (reserved: bf_lily is used by the umbrella bedtime story).

## Results

| slug | format | voice | speed | chapters | duration | size | path | problems |
|---|---|---|---|---|---|---|---|---|
| the-bell-and-the-bicycle | kids-picture-book | af_sky | 0.9 | 1/1 | 1.8 min | 0.8 MB | books/the-bell-and-the-bicycle/out/audio/ | none |
| the-snail-and-the-salad | kids-picture-book | am_puck | 0.9 | 1/1 | 1.5 min | 0.7 MB | books/the-snail-and-the-salad/out/audio/ | none |
| the-umbrella-conductor | bedtime-story | bf_lily | 0.9 | 1/1 | 10.4 min | 4.7 MB | books/the-umbrella-conductor/out/audio/ | none |
| the-one-way-street-why-time-only-runs | science-blink | af_alloy | 0.9 | 9/9 | 23.5 min | 10.8 MB | books/the-one-way-street-why-time-only-runs/out/audio/ | none |
| what-fate-decides-luck-will-and-the-life | idea-blink | bm_daniel | 0.9 | 8/8 | 22.5 min | 10.3 MB | books/what-fate-decides-luck-will-and-the-life/out/audio/ | none |
| france-s-atomic-clock-on-air-the-als162-signal-t | article | af_jessica | 0.9 | 1/1 | 8.2 min | 3.8 MB | books/france-s-atomic-clock-on-air-the-als162-signal-t/out/audio/ | none |
| the-lighthouse-that-kept-lists | short-story | bf_alice | 1 | 4/4 | 34.6 min | 15.8 MB | books/the-lighthouse-that-kept-lists/out/audio/ | none |
| the-local-patch | short-story | am_liam | 1 | 5/5 | 40.3 min | 18.5 MB | books/the-local-patch/out/audio/ | none |
| the-tide-table | short-story | bf_isabella | 1 | 5/5 | 38 min | 17.4 MB | books/the-tide-table/out/audio/ | none |
| fifty-minutes-of-common-sense | linked-collection | bm_lewis | 1 | 15/15 | 259.8 min | 118.9 MB | books/fifty-minutes-of-common-sense/out/audio/ | none |
| the-rooster | novella | bf_isabella | 1 | 14/14 | 133.6 min | 61.2 MB | books/the-rooster/out/audio/ | none |
| circuit-breaker | novella | af_nova | 1 | 10/10 | 176.6 min | 80.8 MB | books/circuit-breaker/out/audio/ | none |
| echoes-in-the-deep | novella | am_fenrir | 1 | 10/10 | 187.1 min | 85.7 MB | books/echoes-in-the-deep/out/audio/ | none |
| rust-and-ruin | novella | af_river | 1 | 11/11 | 150 min | 68.7 MB | books/rust-and-ruin/out/audio/ | none |
| the-automaton-who-confessed | novella | bm_daniel | 1 | 15/15 | 164.1 min | 75.1 MB | books/the-automaton-who-confessed/out/audio/ | none |
| the-clockless-god | novella | bm_fable | 1 | 18/18 | 283.9 min | 130 MB | books/the-clockless-god/out/audio/ | none |
| the-hour-that-happens-twice | novella | bm_fable | 1 | 18/18 | 294.9 min | 135 MB | books/the-hour-that-happens-twice/out/audio/ | none |
| the-clockwork-compass | novella | af_aoede | 1 | 13/13 | 217.5 min | 99.6 MB | books/the-clockwork-compass/out/audio/ | none |
| the-cold-furnace | novella | am_adam | 1 | 19/19 | 151.8 min | 69.5 MB | books/the-cold-furnace/out/audio/ | none |
| the-iron-root | novella | af_bella | 1 | 14/14 | 262.2 min | 120 MB | books/the-iron-root/out/audio/ | none |
| the-light-at-worlds-end | novella | am_michael | 1 | 11/11 | 176.4 min | 80.8 MB | books/the-light-at-worlds-end/out/audio/ | ch02, ch04, ch10, ch11 re-rendered after the cancelled export; ch10 had a stale .part file |
| the-perfect-alibi | novella | am_echo | 1 | 20/20 | 168.3 min | 77.1 MB | books/the-perfect-alibi/out/audio/ | none |
| the-poisoned-well-of-harrowdale | novella | am_eric | 1 | 18/18 | 171.7 min | 78.6 MB | books/the-poisoned-well-of-harrowdale/out/audio/ | none |
| the-salt-line | novella | af_nicole | 1 | 11/11 | 257.5 min | 117.9 MB | books/the-salt-line/out/audio/ | af_nicole reads slowly (about 126 wpm, ratio 1.4-1.5 of the 185 wpm norm), under the 1.6 flag |
| the-saltwater-spy | novella | af_kore | 1 | 10/10 | 211.3 min | 96.7 MB | books/the-saltwater-spy/out/audio/ | none |
| the-sand-courier | novella | af_sky | 1 | 11/11 | 170.2 min | 77.9 MB | books/the-sand-courier/out/audio/ | voice map had af_sarah, which is reserved for Orvane, Again; used af_sky instead |
| the-silence-above-the-snowline | novella | am_onyx | 1 | 10/10 | 182.2 min | 83.4 MB | books/the-silence-above-the-snowline/out/audio/ | none |
| the-silent-signal | novella | am_adam | 1 | 10/10 | 124.6 min | 57.1 MB | books/the-silent-signal/out/audio/ | none |
| the-silent-summit | novella | af_nicole | 1 | 10/10 | 239.9 min | 109.8 MB | books/the-silent-summit/out/audio/ | af_nicole reads slowly (about 126-135 wpm), under the 1.6 flag |
| the-storm-chaser-s-secret | novella | af_jessica | 1 | 10/10 | 155.9 min | 71.4 MB | books/the-storm-chaser-s-secret/out/audio/ | none |
| windward-drift | novella | am_puck | 1 | 10/10 | 171 min | 78.3 MB | books/windward-drift/out/audio/ | none |

Totals so far: 31 books, 323 chapter files, 74.86 h, 2056 MB.

## Notes

- Skipped: the 13 script-format books. choice-visual-novel (the-clockless-god-2, the-echo-between-stars, the-glass-horizon, the-gravity-garden), kids-choice-visual-story (the six soother books) and mystery-puzzle-visual-novel (the-trap-room-at-the-lanterna, the-winter-garden-clock). I read ch-02 of the-glass-horizon, the-trap-room-at-the-lanterna and the-soother-stone. All three are screenplays: every chapter is made of SCENE:, AMBIENCE:, ON SCREEN:, SFX:, CG:, INSERT: lines and speaker-labelled dialogue (ILA: ..., Narration: ...). They are not readable prose, and I found no 'turn to chapter' choice lines in the chapters I read. Reading them aloud would read the labels, or, with labels stripped, give unattributed dialogue. Director decision needed: either skip, or write a narrated prose version first.
- Picture books (the-bell-and-the-bicycle, the-snail-and-the-salad) are scripted too, but after dropping the SCENE and ON SCREEN lines what is left is clean narration, so they were done.
- Title line: the byline read is the book's own byline (book.md), else the hub default pen name Mara Kestrel; a writer agent name is never read (coordinator correction). Books first rendered with an agent name and fixed afterwards (title segment re-rendered, book rebuilt from the same segments): the-bell-and-the-bicycle, the-snail-and-the-salad, the-umbrella-conductor, the-one-way-street-why-time-only-runs, what-fate-decides-luck-will-and-the-life, france-s-atomic-clock-on-air-the-als162-signal-t, the-lighthouse-that-kept-lists, the-local-patch, the-tide-table, fifty-minutes-of-common-sense.
- HUB-47 pilots re-narrated (coordinator request): the-second-window (bf_emma, 587 s), the-plain-title-page (af_heart, 601 s), the-clock-on-the-hill (bm_george, 718 s). One MP3 each in books/<slug>/out/audio/<slug>.mp3 plus a one-line .m3u; title 1.5 s pause, 2 s pause before the debrief, debrief at 0.87. Details in runs/<slug>.md. join.sh in .claude/temp/HUB-47-pilots had a path bug (list entries wav/... resolved relative to wav/); I ran a corrected copy join2.sh, join.sh itself is unchanged. Not verified: nobody has listened.
- orvane-again (coordinator request): one MP3 books/orvane-again/out/audio/orvane-again.mp3 (+ .m3u), 855 s, voice af_sarah (Marit and Teodor series voice; first take in am_santa was replaced at the coordinator's request), story 1.0, debrief 0.87, 1.5 s / 2 s pauses. Story 173 wpm, debrief 135 wpm. Section in runs/orvane-again.md. Not verified: nobody has listened.
- Skipped, same reason as the other soother books (screenplay: SCENE/AMBIENCE/ON SCREEN/SFX lines and speaker-labelled dialogue like PETRA (happy): ...): the-dragon-song-soother, dragons-dont-do-bedtime, the-soothed-mountain, the-littlest-dragons-lullaby (kids-visual-story; I read ch-02 of the-dragon-song-soother) and embers-borrowed-moon (kids-choice-visual-story, same script format).
- RESUME (for another session): work folder C:/projects/Personal/creative-hub/.claude/temp/audiobooks (junction C:/ab). Per book: node prep.mjs <slug...> writes <slug>/chNN-body.txt + plan.json and prints the batch items for title and chapter headings (inline text, mcp__vibetts__synthesize_batch, outputs C:/ab/<slug>/title.mp3 and chNN-head.mp3); then one mcp__vibetts__synthesize_to_file per chapter (path C:/ab/<slug>/chNN-body.txt, output C:/ab/<slug>/chNN-body.mp3, voice and speed from the voice map, overwrite true). The call times out on the tool side after about a minute while the export continues: wait with wf.sh <file> (use timeout 170000; repeat the wf call for chapters over 4000 words) before the next call, because a second call while one runs answers Another export is running. Finally node assemble.mjs <slug> then node record.mjs <that json>, then node mklog.mjs. Books not in the Results table are not done. The Bash tool backgrounds any command running more than 180 s.
- the-iron-tide-2 (exception to the no-screenplay rule, user's explicit request via coordinator): multi-voice audio drama, one MP3 per chapter in books/the-iron-tide-2/out/audio/ (the-iron-tide-2-chNN.mp3 = track NN, the-iron-tide-2-title.mp3, the-iron-tide-2.m3u), 16 files, 125 min in all. Cast to voice: narrator bm_lewis, Mara af_nova, Idris am_onyx, Sable af_river, Director Okonkwo bf_isabella, Renn am_fenrir, Pell af_sky (youngest-sounding available), Arike (minor, 2 lines in ch11) af_bella. Dropped: frontmatter, AMBIENCE, ON SCREEN, SFX, CG, INSERT, END CG, --- rules. SCENE lines read by the narrator as place and hour ("Lower Inspection Catwalk. Hour eleven."; ch09 has one "Twenty minutes."). Dialogue labels and parentheticals dropped. Choices read at the end of ch1-7 from outline.md (yaml choices block, not a "- Choices:" line): "If you choose to <text>, play track N. If you choose to <text>, play track M." Ch8-15 end with "The end." Pauses: 0.4 s between segments, 1.5 s around SCENE changes and before the choice or end line; speed 1.0; consecutive narrator paragraphs rendered as one segment. Lines rendered by calling VibeTTS's MCP endpoint (synthesize_batch) from a script, one batch at a time; work files in .claude/temp/audiobooks/iron/. Unattributed lines: none. Not verified: nobody has listened; the 12-year-old Pell is only a lighter adult-sounding voice. Per-chapter minutes: title 0.2, ch1 9, ch2 9.1, ch3 9.2, ch4 8.9, ch5 6.7, ch6 8.8, ch7 7.9, ch8 8.6, ch9 8.9, ch10 8.9, ch11 7.6, ch12 7.7, ch13 8.2, ch14 8, ch15 7.6.
