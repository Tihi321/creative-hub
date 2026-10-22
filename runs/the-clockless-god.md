# The Clockless God

Started 2026-10-20. Book 1 of the series *The Hartley & Varga Mysteries*.

## Brief

- Idea / theme: user's request. A book in the style of Broken Sword:
  - a man and a woman who investigate, detective-style, with humour;
  - a powerful secret society with an invented deity, a dogma and a strange curse, which plans something bad.
  - It should be a medium-size book and the first entry of a series.
- The user wants to watch Scriptorium in its window.
- Kind: prose book (no visual novel yet) · format `novella` (20-50k words, 10-25 chapters), aiming at about 45k words in about 18 chapters · adults
- Languages: English
- Art / music / voices: none for now
- Who writes: Claude does the editor-in-chief, architect and writer work through the `client` provider. Scriptorium's models (DeepSeek, LM Studio) do the reviews and the archivist.
- Setting: present-day Europe, starting in Paris. The leads and the society were invented by Claude.

## Ids

| Tool | Id |
|---|---|
| Scriptorium series | `the-hartley-varga-mysteries` |
| Scriptorium story | `the-clockless-god` (series_index 1) |
| Scriptorium book | `the-clockless-god` (stage `published`, round 1, score 7.73) |
| Book Translator project | `the-clockless-god-hr-2945aa` (Croatian, done, all agents `client/claude-code`, $0) |
| VN Studio project | |

## Log

- 2026-10-20 Built the series feature in Scriptorium: ticket SCP-09, branch `SCP-09_series`, commit 33c224b, not merged.
  - What it adds: series files, an order gate, earlier books in the prompts, bible carry-over, the MCP tools `list_series` / `get_series` / `add_series` / `update_series`, and a Series panel in the Library.
  - Checks: typecheck, lint, vitest (312 tests) and the Playwright renderer tests all pass, and so does the build.
  - The full vitest run has a timing flake that master has too: 3 failures in 10 runs on master, 1 in 17 on the branch.
- 2026-10-20 Hub: `hub.ps1 start <electron app> -Window` (branch `SCP-09_series-hub`, commit 4c474a4). Scriptorium was started with `-Force -Window` and opened its window, and `check` reported 37 tools. The `start` command itself did not return, though the engine was up; see Left to do.
- 2026-10-20 Factory state at start: nothing running, spend $0.23 today and $4.27 this month. The 7 open ideas the factory generated belong to inactive topics, so they do not start. The user chose "only our book".
- 2026-10-20 `add_series`, then `add_story`:
  - series `the-hartley-varga-mysteries`;
  - story `the-clockless-god`, format novella, series index 1;
  - models: editor-in-chief, architect and writer set to `client/claude-code`.
  - The brief JSON is in `.claude/temp/`; the brief text is in `~/Scriptorium/ideas/the-clockless-god.md`.

- 2026-10-20 Book `the-clockless-god` started at once, with target_words 45000.
  - The editor-in-chief's start_book ran on nemotron (free), not on the client: `add_story {models}` does not reach start_book. This is in the ROADMAP.
  - Claude wrote the pitch, the research plan and the outline: 18 chapters, three acts, a bible of 10 characters and 8 places.
  - The research (4 questions) ran on Scriptorium's researcher. It established that ALS162 at Allouis drives public clocks, traffic lights and the SNCF, and that the Panthéon pendulum is a copy.
  - Outline review (DeepSeek): pass, structure 8. Its notes are applied in the chapters; see `.claude/temp/clock/WRITER.md`.
- 2026-10-20 Drafting. Claude writes every chapter itself, one at a time, because the long-book pipeline drafts in order (draft, check, archivist, next).
  - The working files are in `.claude/temp/clock/`: `chNN.md`, the outline (`outline.py`), the writer brief (`WRITER.md`), and the helpers `ct.sh` / `next.sh` for the client tasks.
  - Chapters 1-9 have been submitted. The continuity checks are all pass, at 8-9.
  - Act 1 review: pass, structure 8. Notes applied: a station clock test is shown early (ch7), and the Jura chapters have no third chase.
  - Act 2 review: pass, structure 8. Its notes shaped act 3:
    - the word itself is the climax, because Roux's copy of the lock is too precise to pick;
    - Inès's fear of heights pays off on the dome stair;
    - the "not partners" running joke is transformed in ch18.
  - The checker asked for rewrites of ch11, ch12, ch15 and ch17. All of them were rewritten and accepted.
    - The ch12 rewrite went in with the old text by mistake (a script error). The fixed text is in `clock/ch12.md`.
    - Later fixes to ch3, ch9, ch13, ch16 and ch17 are applied in the files and listed in `clock/FIXES.md`, to resubmit in the review round.
- 2026-10-20 All 18 chapters drafted, about 50.7k words: slightly over the novella range of 20-50k and the 45k target. Spend so far today is $0.43, all on reviews and the archivist.

- 2026-10-20 Chapter checks led to rewrites of ch11, ch12, ch15, ch17 and ch18. All were accepted.
- 2026-10-20 Round 0 review of the whole book. Pass: beta reader (enjoyment 9 and genre fit 9 in all three acts), developmental editor (structure 8), originality checker (8). Revise: continuity (acts 1-2, 6), copy editor (acts 1-2, 6), line editor (act 3, 6) and the thread check (6, because the seized notebook, board and ledger were never accounted for).
  - The engine asked for rewrites of ch2, 3, 6, 7, 8, 9, 10, 12, 13, 17 and 18.
  - The fixes were collected in `.claude/temp/clock/ROUND1.md`. Four subagents revised the chapter files in parallel: the verbal tics, the weekday arithmetic, the chapel head count, the ledger note in a modern hand, the bell's Latin spelling, Vaulmont's "each other's time", the shorter ch17 lecture, the evidence thread in ch18, and the trimmed "not partners" exchange.
  - Claude submitted all 11 rewrites; all were accepted.
- 2026-10-20 **Published** in round 1 at 7.73. Round 1 scores:
  - enjoyment 8/8/9, genre fit 9;
  - structure 8, originality 8, threads 8;
  - act 3: continuity 8, mechanics 8, prose 8;
  - acts 1-2: continuity 6 and mechanics 6, both still marked revise. The open points are small: the chapel head count against the Nine, and Roux's ledger entry, which should mark a refusal.
  - The total cost was $0.58, all on reviews, the archivist, the researcher and the free editor-in-chief start. Claude's writing cost nothing.
- `set_book_model ... null` was refused on the published book, as already listed in the ROADMAP.
- `get_series` lists book 1 as published, at 7.73.

- 2026-10-20 **Croatian translation** with Book Translator. Every model task was done by Claude through the client provider; the outside-model spend was $0. Steps:
  - Project `the-clockless-god-hr-2945aa`: hr, with all four agents (glossary, translator, proofreader, qa) on `client/claude-code`. BTT-10 adds a `clientOnly` switch for this, merged later; this run predates it, so the four agents were set by hand. A Croatian brief went in with `set_brief`.
  - Glossary: 14 passes, answered by Claude. The series terms are Bratovština Devetog sata, Bezsatni, Zaustavljeni sat, Siva pričest, Devetorica, Sedmi, Sat duga, sat bez kazaljki, slovna brava, "pribor za jelo" and Bdijenje pomrčine.
  - 62 chunks, worked in parallel by 6 translator, 3 proofreader and 2 QA subagents (about 170 tasks). Book Translator releases the tasks in waves, so the first stop rule (stop after 2 idle minutes) was too short and was changed to "stop when the project leaves translating".
  - QA flagged French, Latin and Hungarian text as "untranslated" several times. These were false alarms, and the brief now says so.
  - 6 chunks were left flagged at the end.
  - A final editorial pass by 3 editor subagents with `edit_chunk` touched about 140 segments:
    - one tense (the perfect, no aorist dialogue tags);
    - the address rules (Dec and Inès use "ti" from chapter 4);
    - the same word for each object and term (kalauz, leptirić, usadna brava, urezi, procjep, sajla...);
    - the twist kept: the Brotherhood's "Naš je restaurator" is masculine, because a feminine form would give away early that they mean Morel;
    - the real QA findings fixed;
    - the contents page matched to the chapter headings.

    All 62 chunks are done.
  - Exported to `runs/the-clockless-god/the-clockless-god.hr.epub`: about 44k words, `dc:language hr`, title "Bezsatni bog".
- Found during the translation: the English ch17 has Dec lift "the hand that was not holding the pistol" after an officer has already taken it. It is fixed in Croatian (d19.71). The English book is published and cannot be reopened, so the English slip stays.

## Checked

- Claude wrote and reread every chapter, and read every check and every review.
- The EPUB, cover and reader exist: `~/Scriptorium/books/the-clockless-god/out/the-clockless-god.epub`.
- The series file `~/Scriptorium/series/the-hartley-varga-mysteries.md` lists the book, and `get_series` shows its stage and score.
- The series section of the prompts was seen in the pitch, outline and chapter tasks.
- Not checked by Claude: the Series panel in the Scriptorium window, which only the user can see. The book has not been read by the user yet.

## Left to do

- The user reads the EPUB and rates it (`rate_book`).
- Optional: one more round on the act 1-2 notes. That needs a published book to be reopenable, which is a ROADMAP item.
- Croatian EPUB: the user reads it.
- Visual novel: the SCP-11 adaptation (`runs/the-clockless-god-vn.md`).
- Book 2 of the series: `add_story {series: "the-hartley-varga-mysteries", ...}`. It gets book 1's summaries, the cast's end state and the open threads (the Nine, the Keeper of the Last Hour, Vey's ledger, HUIT).
- `hub.ps1 start -Window` started the app but never returned or printed anything. Find out why.
- Merge `SCP-09_series` (scriptorium) and `SCP-09_series-hub` (hub) when the user is happy.
