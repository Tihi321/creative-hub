# The Local Patch (VN adaptation): HUB-15 check C1

Started 2026-10-23 19:26, published 19:45. HUB-15 C1: Scriptorium's VN adaptation fixes SCP-28, 34, 35, 36, 37, live.

## Ids

- Source: Scriptorium book `the-local-patch` (short story, 5 chapters, 7,723 words).
- Story / book: `the-local-patch-2`, format `visual-novel`, `C:\Users\Infplane\Scriptorium\books\the-local-patch-2`.
- Models: architect, writer, humanizer = `client/claude-code` (this session); reviewers and publisher on `deepseek/deepseek-flash`.
- VN Studio project: `the-local-patch-2` (import preview only; no plan, no images, no build).

## Decisions

- Adapter notes ask for weekdays in several SCENE lines (SCP-34).
- Outline: 5 chapters, one per source chapter; `story_year: null` (ship time). Minor speakers (WATCH OFFICER, WOMAN IN LINE, VOICE(S) IN THE CROWD) left unnamed; Sera and the technician Osei come from the source.
- After the round-0 reviews the chapter 5 epilogue was re-dated so the days run forward ("Thursday, before dawn a week later", ...). That wording works around SCP-38.

## Timeline

- 19:26 `adapt_book` -> `the-local-patch-2`; start job `eic--start--n25--r0` had no model and took 124 ms; title and genre were taken from the source.
- Pitch (one cut to under 300 words), outline, 5 drafts (10,134 words).
- Length fix: every chapter got a grow rewrite ("too short ... add ... repetition"), 10,134 -> 11,270 words.
- Humanizer r0, reviews r0 (revise: chapter 5 chronology, chapter 3 meeting, reservoir and countdown arithmetic, vapour line), rewrites of chapters 3, 4 and 5, humanizer r1.
- Reviews r1 (revise: the stripped chapter 5 headings, primes vs maintenance cycle), rewrites of chapters 3, 4 and 5, humanizer r2.
- Published at round 2: score 7.36, 11,342 words, EPUB `out/the-local-patch-2.epub`.
- `vno_import {source: "the-local-patch-2"}`: 5 chapters, 3 characters, 6 places, 140 uncertain. Warnings: "chapter 2: a CG line at the end of a scene has no beat after it ... dropped" (that is `END CG` before `---`, the harmless case already filed as VNO-38), and "speakers not in the bible (no sprite): WATCH OFFICER, WOMAN IN LINE, VOICE IN THE CROWD, VOICES IN THE CROWD, SERA".

## Checks

| Check | Result | Evidence |
|---|---|---|
| SCP-28 start makes no model call | **verified** | `made.md`: `start_book` row with no model, 124 ms; book has the source's title and genre `science fiction`. |
| SCP-37 target from source words | **verified** (target) | `book.md`: `target_words: 13129`, `target_from_source_words: 7723` (= 1.7 x). The length fix still ran (see SCP-42). |
| SCP-37 no "grow every chapter" rewrites | **failed as worded** | The drafts came to 77% of the target (my drafts ran short, at about 2,000 words a chapter against 2,626 asked), so every chapter got a `--len` grow rewrite. The gate did what it is built to do, but the note asks a script for "repetition": SCP-42. |
| SCP-34 weekday kept after drafting and humanizing | **verified for `Place, Weekday, time`** | All 18 `Place, Weekday, time` headings (chapters 1 to 4 and chapter 5's first) survived every draft, rewrite and humanizer pass. **Failed for other day words:** `the ninth day` and `the following Thursday` were cut (SCP-38). The humanizer then refused to put "Saturday" back (SCP-39). |
| SCP-35 no cue as a scene's last line | **verified** | No CG, INSERT, SFX or AMBIENCE line ends a scene. The only scene-final cue is `END CG` (ch2), which gives VN Studio's harmless "dropped" warning (VNO-38). No move was needed, so `moveTrailingCues` was not exercised. |
| SCP-36 repetition report has no control-line phrases | **verified** | `analyzeRepetition` run by hand on the published chapters (the engine writes the report only for long books): no `scene`, `on screen` or `ambience` phrases. Speaker labels still count: "watch officer" is flagged 41 times as an opener (SCP-41). |
| Stop at book + `vno_import` | done | Preview import only. |

## Bugs found (Scriptorium `ROADMAP.md`, uncommitted on master)

SCP-38 (place fixer drops non-weekday time segments), SCP-39 (humanizer name guard counts weekdays), SCP-40 (a new speaker such as Sera gets no bible entry or sprite), SCP-41 (repetition counts speaker labels), SCP-42 (length-fix note for scripts, and whether to grow an adaptation that is inside its range).

## Not verified

- Not played, not built, no art. The user's verdict is not needed for C1 (stop at the book plus import).
- The book's `role_models` still name `client/claude-code`. It is published, so no further jobs are expected.
