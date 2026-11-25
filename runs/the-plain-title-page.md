# The Plain Title Page

Started 2026-11-24. Idea fable from *The Best Minds* (card `halo-effect`). Ticket HUB-45, request REQ-0033, plan `.claude/tickets/HUB-45-idea-fable-pilots/plan.md`. Pilot 2 of 3. Pre-flight record: `runs/the-second-window.md`.

## Brief

- Idea / theme: The halo effect, from *The Best Minds* (Jonathan Rosen). Story "The Plain Title Page", byline Taleidea Stories.
- Kind: linear (idea fable, one chapter, 1,500-2,000 words) · adults
- Languages: en
- Art: off · Music: off · Voices: off

### Frozen card (verbatim, as sent in `add_story`; frozen 2026-11-24 after the source check)

Common fields: `format: "idea-fable"`, `byline: "Taleidea Stories"`, `genre: "literary fiction"`, `noLocalFallback: true`, `models` map of plan 2.2. Pilot fields (title, premise, plot, characters, setting, style) as in plan 2.2 Pilot 2, unchanged.

`sections`:

**Concept card**
```
Idea: The halo effect
Definition: One impressive quality in a person makes us assume they are good at other, unrelated things too.
Mechanism: The mind prefers a simple, consistent picture, so a strong first impression leaks into judgments of other traits and of the person's mistakes. The opposite, one bad trait colouring the rest, is the horn effect. The cost falls on the person whose weaknesses go unseen and on the people overlooked beside them.
Misconception: Only shallow people fall for it, and only for good looks. It is a general feature of judgment; teachers, managers and experts show it too.
Rules: No real person. Nothing about medicine or mental illness, no violence, no prodigy who breaks down, nothing from the real case of the starting book.
```

**Key facts**
```
1. In 1920 Edward Thorndike asked two commanding officers to rate their soldiers on separate qualities and found the ratings correlated too highly and too evenly, as if one general impression coloured the rest.
2. In a 1972 study (Dion, Berscheid and Walster), people judged attractive people to have more desirable traits.
3. In a 1974 study (Efran), mock jurors were more lenient with attractive defendants.
4. Phil Rosenzweig argues that ratings of a company's leadership or culture are often shaped by its known results, such as its share price or profits.
5. The opposite, where one bad trait colours the judgment of the rest, is called the horn effect.
```

**Sources**
```
1. Thorndike, "A constant error in psychological ratings", Journal of Applied Psychology 4(1), 25-29 (1920), copy at https://zenodo.org/record/1429134 ; summary at https://en.wikipedia.org/wiki/Halo_effect
2. https://en.wikipedia.org/wiki/Halo_effect
3. https://en.wikipedia.org/wiki/Halo_effect
4. https://en.wikipedia.org/wiki/The_Halo_Effect_(book)
5. https://en.wikipedia.org/wiki/Halo_effect
```

**Go deeper**
```
*The Best Minds: A Story of Friendship, Madness, and the Tragedy of Good Intentions*, Jonathan Rosen (Penguin Press; paperback ISBN 9780143132899)
*Thinking, Fast and Slow*, Daniel Kahneman
*The Halo Effect*, Phil Rosenzweig (2007)
```

### Wikipedia marks (beside the card, not inside it)

All five key facts rest on Wikipedia: needs a better source before anything is public.
- Fact 1: the Zenodo copy of Thorndike opens (title, author, year; CC0) but is a scanned PDF the fetcher could not read, so the "too high and too even" wording rests on the Wikipedia page.
- Facts 2, 3: the primary papers (DOIs 10.1037/h0033731 for Dion et al., 10.1016/0092-6566(74)90044-0 for Efran) did not open (redirect/loading page/no abstract), so they are not cited.
- Fact 4: Wikipedia page "The Halo Effect (book)" opens and supports it.
- Fact 5: Wikipedia "Halo effect" (also called the devil effect or reverse halo effect there).

### Source check (2026-11-24, WebFetch)

- Changed vs plan draft: fact 1 said officers' "ratings were too high and too even"; the page says the *correlations* "are too high and too even" for two commanding officers rating soldiers, so the wording now says the ratings correlated too highly and too evenly. Fact 3: "mock jurors" kept (page: simulated jury task, more lenient sentencing of attractive defendants). Fact 4: reworded to the page's wording (judgments contaminated by share price or profitability).
- Nisbett and Wilson (1977) is not cited (it appears on the Wikipedia page's horn-effect references; no open source).
- Concept card: consistent with the sources; no contradiction. (Dion et al. also found attractive people were judged worse parents; the card does not claim otherwise.)
- Rosenzweig's year (2007) in Go deeper was not confirmed from a fetched page (the Wikipedia halo page lists a 2014 edition); left as drafted.

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | (after `add_story`) |
| Scriptorium book | |
| Book Translator project | n/a |
| VN Studio project | n/a |

## Log

- 2026-11-24 card frozen by the pre-flight worker. No `add_story` yet; waiting for the user's go (plan 2.0 step 6).

## Production record (HUB-45 production worker, 2026-11-25)

### 2.3 Run 1
- After pilot 1: `add_story` -> story slug `the-plain-title-page`, file `ideas/the-plain-title-page.md`; book slug `the-plain-title-page`. `set_factory_only {the-plain-title-page}`; `set_factory_paused {false}`.
- First `wait_for_book` returned `reason: client-task` after 150 s (stage reviewing): a `web_search` task (role `searcher`, client claude-code, job `search-mwvtv7cd-1`, researcher-hugo-sterne, question about bean seedling growth in four weeks), raised by a reviewer's research question. Not answered (brief: answer nothing). Second `wait_for_book` with `stop_on_client_task: false` returned `published` after 14 s; a second searcher task (`search-mwvtvg1h-2`, researcher-noor-castell) was waiting too; both stay unanswered in the engine's queue. Reported to the director as a finding: the `researcher` role map does not cover the web search, which goes to a `client` searcher.
- `set_factory_paused {true}` right after. Published 2026-11-25T07:54:40Z, score 8.33, `words` 1508, `lengthGate` {ok, 1543}. Book log: no `fable back matter:` line. Copy of run-1 chapter: `.claude/temp/HUB-45-prod/plain-title-page-run1-ch01.md`.
- Models (made.md, 11 rows, all cost 0, all acp): claude-sonnet-5 for editor-in-chief, architect, writer, humanizer, publisher; gemini-4-hydrogen for the five reviewers. Spend today 0.

### 2.4 Checks, run 1
- K1 PASS: 1508 (front matter and manual recount agree); lengthGate 1543 (info). Near the lower edge.
- K2 PASS: three bold lead-ins and `**Sources**` equal to the 5 frozen lines; no second block.
- K3 FAIL. Table:

| Debrief sentence | [n] | Key fact | Verdict |
|---|---|---|---|
| Idea 1: one impressive quality -> we assume other, unrelated strengths; first impression leaks | [1] | 1 | ok |
| Idea 2: "This shows up even among trained judges, not only casual observers" | [1] | 1 (two commanding officers rating soldiers) | not supported: "trained judges" is not in KF1 |
| Idea 3: one bad trait colours the rest: horn effect | [5] | 5 | ok |
| Where it showed up: Hana marks Milo highly, skims Agata's notebook | none | story | in story |
| Answer 1: "growth figure too large for the time span; identical repeated measurements" | [1] | none (story detail; cited to Thorndike) | FAIL: wrong citation |
| Answer 2: Thorndike ratings correlated too highly and evenly | [1] | 1 | ok |
| Answer 3: horn effect mirror image | [5] | 5 | ok |

  Also: the story states real-world plant-growth claims ("more growth than bean seedlings produced at all in that stretch at this altitude") that no key fact covers (the reviewers' research question on this was never answered); Quiz Q2 and Q3 say "the key facts" (back-matter jargon the reader does not know).
- K4 PASS: 3 questions A-D; Answers 1. B, 2. B, 3. C; exactly one right option each.
- K5 PASS: Go deeper = the 3 frozen lines; disclaimer once, last paragraph.
- K6 PASS: no Rosen, Kahneman, Thorndike, Rosenzweig, Dion, Efran, Berscheid, Walster in the story part.
- K7 PASS (all 11 rows cost 0, acp; spend today 0.00; modelDeviations []).
- K8 PASS: chapter-01.xhtml has the four headings and the disclaimer; EPUB 310,762 bytes; author "Taleidea Stories".
- K9 PASS: `humanizer_result: rewritten`.
- Side note: the chapter front-matter title is "One Quality at a Time" (get_book title is "The Plain Title Page").
- Wikipedia marks: all five key facts still rest on Wikipedia: needs a better source before anything is public.

### Retry (the one allowed, 2026-11-25)
- Because K3 failed: `add_book_note {book, chapter 1, text}` (note: no real-world plant-growth claims, suspicion only from Milo's own data; every [n] only for what that key fact says, no [1] on story details, no "trained judges"; no "key fact(s)" in the quiz; story 1,550-1,900 words) then `reopen_book {mode: rewrite, chapters: [1]}`; `set_factory_paused {false}`; one `wait_for_book` (stop_on_client_task false): published after 295 s; `set_factory_paused {true}`. made.md shows the engine itself ran a further rewrite round inside the retry (round 2, 26 rows, all cost 0, acp). Spend today 0.
- Two researcher jobs for this book (bean growth questions) still show `running` in factory_status, waiting for `client` web-search tasks that nobody answers; they do not block anything now (book published, factory paused).

### 2.4 Checks, run 2 (final; counts as the result)
- K1 PASS: 1556 (front matter `words: 1556`; manual recount 1556). lengthGate not re-read after the retry.
- K2 PASS: `**The idea.**`, `**Where it showed up.**`, `**How to use it tomorrow.**`, `**Sources**` = the 5 frozen lines; no second block.
- K3 PASS. Table:

| Debrief sentence | [n] | Key fact | Verdict |
|---|---|---|---|
| One impressive quality -> assume good at unrelated things | none | card definition | ok |
| 1972 study: attractive people judged to have more desirable traits ("across the board") | [2] | 2 | ok (writer's "across the board" is slight overstatement) |
| 1974 study: mock jurors more lenient with attractive defendants | [3] | 3 | ok |
| 1920 Thorndike: two commanding officers rating soldiers on separate qualities, ratings correlated too highly and too evenly | [1] | 1 | ok |
| A later writer argued judgments of a company's leadership or culture follow its known share price or profits | [4] | 4 | ok |
| Reverse: one bad trait colours the rest, the horn effect | [5] | 5 | ok |
| Where it showed up: Hana marks Milo highly, skims Agata's notebook | none | story | in story |
| Answer 1: Hana's sums on Milo's own data, repeated readings | none | story | story only, no citation |
| Answer 2: 1920 officers' ratings | [1] | 1 | ok |
| Answer 3: horn effect | [5] | 5 | ok |

- K4 PASS: 3 questions A-D; Answers 1. B, 2. B, 3. C; one right option each. Wording note: Q3 says "the main effect described", slightly vague.
- K5 PASS: Go deeper = the 3 frozen lines; disclaimer once, last paragraph; "key fact" no longer appears in the chapter.
- K6 PASS: no Rosen, Kahneman, Thorndike, Rosenzweig, Dion, Efran, Berscheid, Walster in the story part.
- K7 PASS: all 26 made.md rows cost 0 and acp; spend today 0.00, month 0.010392 unchanged.
- K8 PASS: chapter-01.xhtml has the four headings and the disclaimer; EPUB 311,126 bytes; author Taleidea Stories.
- K9 PASS: `humanizer_result: rewritten` (humanizer_round 2).
- Book log: no `fable back matter:` line. Score 8.42.
- Paths: reader `C:\Users\Infplane\Scriptorium\books\the-plain-title-page\out\reader`; EPUB `C:\Users\Infplane\Scriptorium\books\the-plain-title-page\out\the-plain-title-page.epub`.
- Models: claude-sonnet-5 (editor-in-chief, architect, writer, humanizer, publisher), gemini-4-hydrogen (five reviewers). Retries used: 1.

### Leftovers and restore
- 09:16 `set_book_paused {the-plain-title-page, true}` (remedy for the researcher stall seen in pilot 3); the book is still `paused: true` in book.md, and its two research jobs are in `jobs/queued/`. Do not unpause it. Restore of the factory (paused true, no only, cap 20, engine down): see `runs/the-clock-on-the-hill.md` 2.5.

## Checked

- what was looked at or played, by whom

## Left to do

- The user's go, then plan 2.1-2.5.
