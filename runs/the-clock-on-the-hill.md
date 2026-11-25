# The Clock on the Hill

Started 2026-11-24. Idea fable from *Seven Brief Lessons on Physics* (card `gravitational-time-dilation`). Ticket HUB-45, request REQ-0033, plan `.claude/tickets/HUB-45-idea-fable-pilots/plan.md`. Pilot 3 of 3. Pre-flight record: `runs/the-second-window.md`.

## Brief

- Idea / theme: Gravitational time dilation, from *Seven Brief Lessons on Physics* (Carlo Rovelli). Story "The Clock on the Hill", byline Taleidea Stories.
- Kind: linear (idea fable, one chapter, 1,500-2,000 words) · adults
- Languages: en
- Art: off · Music: off · Voices: off

### Frozen card (verbatim, as sent in `add_story`; frozen 2026-11-24 after the source check)

Common fields: `format: "idea-fable"`, `byline: "Taleidea Stories"`, `genre: "literary fiction"`, `noLocalFallback: true`, `models` map of plan 2.2. Pilot fields (title, premise, plot, characters, setting, style) as in plan 2.2 Pilot 3, unchanged.

`sections`:

**Concept card**
```
Idea: Gravitational time dilation
Definition: Time passes more slowly where gravity is stronger, so a clock lower down runs slower than one higher up.
Mechanism: In general relativity the rate at which time passes depends on where you are near a mass. Everyday differences are tiny and were invisible for a long time; modern atomic clocks measure them across the height of a table, and satellite navigation must correct for them. Each person feels their own time as normal; the difference shows when the clocks are compared.
Misconception: It only happens near black holes or close to the speed of light. It happens everywhere, even between the floors of a building.
Rules: The higher clock runs faster. Nobody can feel the difference; never suggest it makes a life noticeably longer. Give the sisters' clocks no number: the gap is a sliver seen only by an instrument. No real person or real observatory.
```

**Key facts**
```
1. A clock lower down, closer to a mass, runs slower than one higher up, and both observers agree which one runs slower; this is different from the time dilation caused by speed.
2. In 1971 Hafele and Keating flew four caesium clocks around the world on commercial airliners; the eastward clocks lost about 59 billionths of a second and the westward clocks gained about 273, as relativity predicted.
3. In 2010 NIST compared two aluminium-ion atomic clocks, one raised about 33 centimetres (about a foot) above the other, and the higher clock ran slightly faster.
4. NIST worked out that at that height difference the effect adds up to about 90 billionths of a second over a 79-year lifetime.
5. GPS satellite clocks lose about 7 millionths of a second a day from their speed and gain about 45 from the weaker gravity, a net gain of about 38 a day, so their frequency is set lower before launch.
```

**Sources**
```
1. https://en.wikipedia.org/wiki/Time_dilation
2. https://en.wikipedia.org/wiki/Hafele%E2%80%93Keating_experiment
3. NIST news, 23 September 2010, https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal
4. NIST news, 23 September 2010, https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal
5. GPS World, https://www.gpsworld.com/inside-the-box-gps-and-relativity/
```

**Go deeper**
```
*Seven Brief Lessons on Physics*, Carlo Rovelli (Riverhead; ISBN 9780399184413)
*The Order of Time*, Carlo Rovelli
*Black Holes and Time Warps*, Kip Thorne
```

### Wikipedia marks (beside the card, not inside it)

- Key fact 1 rests on Wikipedia "Time dilation" (the non-reciprocity sentence carries a "citation needed" tag there): needs a better source before anything is public.
- Key fact 2 rests on Wikipedia "Hafele-Keating experiment": needs a better source before anything is public. (The primary Science papers, DOIs 10.1126/science.177.4044.166 and .168, returned 403; the archived PDFs were blocked by the fetcher.)
- Key facts 3, 4 (NIST) and 5 (GPS World) rest on institutional sources.

### Source check (2026-11-24, WebFetch)

- NIST page opens (dated 23 September 2010): "33 centimeters, or about 1 foot"; "the higher clock ran at a slightly faster rate"; "approximately 90 billionths of a second over a 79-year lifetime". Direction confirmed: higher clock faster. The page mentions neither Hafele-Keating nor GPS.
- GPS World opens: "lose about 7 microseconds per day" (speed), "gain about 45 microseconds per day" (gravity), "net ... about 38 microseconds per day", "factory offset" lowering the satellite clock frequency. Draft "adjusted before launch" reworded to "frequency is set lower before launch" (the page says factory offset, not literally "before launch").
- Wikipedia Hafele-Keating: flights in 1971, four caesium-beam clocks on commercial airliners; measured totals eastward -59 +/- 10 ns, westward +273 +/- 7 ns. Numbers match the draft. The page text read did not show the predicted values; "as relativity predicted" rests on the general statement that the results agreed with prediction and was not re-checked here. The reference clock ("a clock on the ground" in the draft) was dropped from fact 2 because the page read did not state it.
- Wikipedia Time dilation: "both observers agree that the clock nearer the center of the gravitational field is slower", velocity dilation reciprocal. Matches fact 1.
- Concept card: no contradiction with the sources. NPR's backwards claim is not used. The card says "modern atomic clocks measure them across the height of a table" (NIST: 33 cm, a foot; Chou et al. 2010 abstract says under 1 m): consistent.
- Go deeper books other than Rovelli's *Seven Brief Lessons* were not opened (no ISBNs given, as required).

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

### 2.3 Run
- After pilots 1 and 2: `add_story` -> story slug `the-clock-on-the-hill`, file `ideas/the-clock-on-the-hill.md`; book slug `the-clock-on-the-hill`. `set_factory_only {the-clock-on-the-hill}`; `set_factory_paused {false}` (about 09:00 local).
- Draft, humanizer and reviews done by 09:05 (stage reviewing, 1549 words at that point). Stall: the developmental editor's research question (job `research--the-clock-on-the-hill--5739b49ea8--r0`, pendulum clocks at altitude) sat in `jobs/queued/` from 09:05 because both `researcher` agents (hugo-sterne, noor-castell) were busy with pilot 2's two research jobs, which loop on `web_search` tasks routed to a `client` searcher (claude-code) that nobody answers (answer nothing, per brief). `set_book_model` with role `searcher` is refused ("unknown role").
- Remedies tried, in order, all logged: (1) 09:16 `set_book_paused {the-plain-title-page, true}` (book flag; pilot 2's book.md now has `paused: true`; it did not release the running jobs); (2) 09:19 `set_factory_paused {true}`, `hub.ps1 stop scriptorium`, `hub.ps1 start scriptorium -Force` (acp-proxy was already up, the same one, pid 30868; the new engine pid 22628), confirmed factory.md `paused: true`, `only: the-clock-on-the-hill`, budget `daily_cap_usd: 0`; the two running pilot-2 jobs went back to `jobs/queued/` and stay there (book paused); then `set_factory_paused {false}` about 09:21.
- 09:22: the clock book's own research job now runs on researcher hugo-sterne and waits for a client `web_search` (task `search-mwvusi1l-1`), not answered.

- 09:23-09:34: the research search timed out by itself after a few minutes (still unanswered, no client task answered at any time), the book went to `rewriting` (engine round 1) and was `published` at about 09:34 after the third 280 s wait. `set_factory_paused {true}` straight after. Score 8.58, words 1664. Book log: no `fable back matter:` line.
- Copy of run-1 chapter: `.claude/temp/HUB-45-prod/` (see below, made before the retry).

### 2.4 Checks, run 1
- K1 PASS: 1664 (front matter; manual recount 1664).
- K2 PASS (structure): three bold lead-ins and `**Sources**` = the 5 frozen lines; no second block. Note: the debrief cites only [1]; sources 2-5 are listed but never cited.
- K3 FAIL. Table:

| Debrief sentence | [n] | Key fact | Verdict |
|---|---|---|---|
| The idea: lower clock runs slower than a higher one; both observers agree which; separate from speed effect | [1] | 1 | ok |
| Where it showed up: Otho Pell's instrument, mountain clock ahead; gap unseen on the faces | none | story | in story |
| How to use it tomorrow | none | none | advice |
| Quiz Q2 option B (the correct one) ends "even added up over decades [1]" | [1] | 1 does not say the gap is tiny | FAIL: a citation inside a quiz option (also marks the right answer) |
| Answer 1: higher clock runs faster, which Pell's instrument found | [1] | 1 | ok |
| Answer 2: gap too small for any clock face | [1] | 1 does not say this (KF3/4 are about tiny effects, not cited) | FAIL: wrong citation |
| Answer 3: grandchildren, grief, years immeasurable | [1] | none (story theme) | FAIL: story theme cited to a key fact |

- K4 FAIL (judgment): 3 questions A-D, Answers 1. B, 2. B, 3. C; Q1 and Q2 have one right option; Q3 is about the story's theme, and options B ("lives unchanged in length") and C are both defensible.
- K5 PASS: Go deeper = the 3 frozen lines; disclaimer once, last paragraph.
- K6 PASS: no Rovelli, Thorne, Einstein, Hafele, Keating, NIST in the story part (the story invents Otho Pell, Saltmere, Maren and Tove Lind).
- K7 PASS: 20 made.md rows (incl. one `research` row on acp/antigravity/gemini-4-hydrogen), all cost 0, all acp; spend today 0.00, month 0.010392 unchanged; modelDeviations not re-read.
- K8 PASS: chapter-01.xhtml has the four headings and the disclaimer; EPUB 168,086 bytes; author Taleidea Stories (get_book not re-read).
- K9 PASS: `humanizer_result: rewritten`.
- Concept-card rules: the story says the higher clock runs faster, gives the clocks no number, suggests no longer life. ok.
- Wikipedia marks: key facts 1 and 2 still rest on Wikipedia: needs a better source before anything is public.
- Decision: one retry (published but K3/K4 fail): note + `reopen_book rewrite chapters [1]`.

### Retry (the one allowed)
- `add_book_note` (no [n] inside quiz questions or options; cite only what each key fact says; use key facts 2-5 in "The idea"; quiz about the idea, one clearly right option; story kept, 1,550-1,900 words) then `reopen_book rewrite [1]` (about 09:35); `set_factory_paused {false}`; published after one 254 s wait (about 09:39); `set_factory_paused {true}`; `set_factory_only {null}`. Score 8.75, words 1588. Run-1 chapter kept at `.claude/temp/HUB-45-prod/clock-run1-ch01.md`. Spend today 0.00. Retries used: 1.

### 2.4 Checks, run 2 (final)
- K1 PASS: 1588 (front matter; manual recount 1588).
- K2 PASS: three bold lead-ins, `**Sources**` = 5 frozen lines, no second block. "The idea" now cites [1] to [5].
- K3 PASS. Table:

| Debrief sentence | [n] | Key fact | Verdict |
|---|---|---|---|
| Lower clock slower than higher; observers agree which; separate from speed effect | [1] | 1 | ok |
| 1971 four caesium clocks on airliners; eastward -59, westward +273 billionths | [2] | 2 | ok ("changed exactly as the idea predicted" = "as relativity predicted") |
| 2010 two aluminium-ion clocks ~33 cm apart, higher ticks slightly faster | [3] | 3 | ok |
| 79-year lifetime at that height difference, about 90 billionths | [4] | 4 | ok |
| GPS: -7 speed, +45 gravity, net +38 a day, frequency set low before launch | [5] | 5 | ok |
| Where it showed up: Otho Pell's instrument, mountain clock ahead, gap invisible on the faces | none | story | in story (story has Otho Pell, the instrument, fifty years) |
| How to use it tomorrow | none | none | advice |
| Answer 1: higher clock runs faster | [1] | 1 | ok |
| Answer 2: 2010 comparison, higher clock slightly faster | [3] | 3 | ok |
| Answer 3: GPS net gain, frequency set low before launch | [5] | 5 | ok |

- K4 PASS: 3 questions A-D, about the idea (higher clock; 2010 NIST result; GPS correction); Answers 1. B, 2. C, 3. C; one right option each; no [n] inside questions or options.
- K5 PASS: Go deeper = the 3 frozen lines; disclaimer once, last paragraph.
- K6 PASS: no Rovelli, Thorne, Einstein, Hafele, Keating, NIST, GPS in the story part.
- K7 PASS: every made.md row cost 0 and acp (writer/architect/humanizer/publisher/editor-in-chief claude-sonnet-5; reviewers and researcher gemini-4-hydrogen); spend today 0.00, month 0.010392 unchanged.
- K8 PASS: chapter-01.xhtml has the four headings and the disclaimer; EPUB 168,254 bytes; author Taleidea Stories.
- K9 PASS: `humanizer_result: rewritten` (humanizer_round 2).
- Book log: no `fable back matter:` line.
- Paths: reader `C:\Users\Infplane\Scriptorium\books\the-clock-on-the-hill\out\reader`; EPUB `C:\Users\Infplane\Scriptorium\books\the-clock-on-the-hill\out\the-clock-on-the-hill.epub`.

### 2.5 Restore (2026-11-25, about 09:45)
- `set_factory_only {null}`, `set_factory_paused {true}`; `hub.ps1 stop scriptorium` (down, lock removed); acp-proxy left up (pid 30868, as hub.ps1 leaves it).
- factory.md line 3 `paused: true`, no `only:` line (before the production: `paused: false`, so it DIFFERS from the before-state; decision 3: the user unpauses when they want the 7 open ideas written). budget.md `daily_cap_usd: 20` (was 20 before; set to 0 during the pilots), monthly 40, per_book null.
- Scriptorium repo `git status --short` after = before (identical; branch `SCP-71_idea-fable`).
- Left behind: `the-plain-title-page` has `paused: true` in book.md (set at 09:16 as a remedy; the engine was already down at restore, so it was not reversed), and two pilot-2 research jobs sit in `jobs/queued/` (`research--the-plain-title-page--9439dd1ede--r0.md`, `...--eb6ce588f5--r0.md`). Do not unpause that book; they would loop on client web searches and block the researchers.

## Checked

- what was looked at or played, by whom

## Left to do

- The user's go, then plan 2.1-2.5.

## Text fixes after the check (2026-11-25)

- Before (chapters/ch-01.md line 29, Tove's letter): *My clock has outlived two husbands' worth of us hanging storm shutters on it by accident,* ...
- After: *My clock has survived years of us hanging storm shutters on it by accident,* ... (rest of the sentence unchanged).
- Front matter `words`: 1588 -> 1586 (story part only, split on whitespace). `book.md` `length_gate.words: 1569` is the count from the gate at the time and was left as it is. Old sentence still sits in log.md, chapters/history/, reviews/ and out/draft/ (history, not touched).
- Outputs rebuilt without the engine: a throwaway script (`.claude/temp/HUB-45-fix/rebuild.mts`) called Scriptorium's own `BookStore.buildEpubFile` (which writes the EPUB and then `out/reader/`) with tsx; no service started, no model called. Backups in `.claude/temp/HUB-45-fix/backup/`. EPUB file list identical to the backup; `modified` date of the EPUB is new.
