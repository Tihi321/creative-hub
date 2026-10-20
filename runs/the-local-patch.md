# The Local Patch

Started 2026-10-20.

## Brief

- Idea / theme: user's synopsis. A physical constant (the rate of atomic decay) starts shifting inside a closed habitat (generational starship or planetary dome). Society splits between a "Programmer" simulation religion and people who see it as a natural phase change, "like a fever". A small team (Dr. Aris Thorne, Vera Lin, Kaelen Vance) has to adapt the habitat's technology before it collapses.
- Kind: prose book (no visual novel yet) · format `short-story` (3,000-10,000 words, 3-6 chapters) · adults
- Languages: English
- Art / music / voices: none for now

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | `the-local-patch` |
| Scriptorium book | `the-local-patch` (stage `published`, round 3, score 7.14) |
| Book Translator project | |
| VN Studio project | |

## Log

- 2026-10-20 Hub status: everything is up except Strata. Book Translator's MCP got a 401 in this session because Claude Code started before `BOOK_TRANSLATOR_MCP_TOKEN` was set. The token itself works (HTTP 200 when tested directly). Fix: restart Claude Code from a new terminal.
- 2026-10-20 Scriptorium was already running (not paused). Spend: $0 today (cap $5), $4.04 this month (cap $40). Only LM Studio is available (4 slots). 7 open ideas the factory generated itself are competing for slots.
- 2026-10-20 `add_story` gave story `the-local-patch` (format short-story, genre science fiction, title fixed). Plot, style and starship-or-dome were left for the editor-in-chief to decide. The pasted synopsis was cut off at "To kick off our story, whic"; the missing part was not used.
- 2026-10-20 Started `scripts/wait-book.ps1 -Story the-local-patch` in the background.

- 2026-10-20 14:00-14:12 Pitch, outline, 5 chapters drafted, 2 rewrite rounds, then **rejected**: weighted score 6.29, below the threshold of 7 (enjoyment 6, genre fit 6, continuity 6, mechanics 6, structure 6, prose 6, originality 8). Length 10,124 words against a 6,000 target. Cost $0.21: deepseek-flash, which is paid, plus the free nemotron model on OpenRouter. LM Studio was not used.
- Every round-2 reviewer gave the same main reason: the round-2 rewrite made chapter 4 tell chapter 3's events again, almost word for word (the Command Node meeting, the overshoot and filter, Aris finding the second fit). The two versions also contradict each other: in ch3 Aris buries the second fit, in ch4 he logs it; the hour count and clock times disagree. Lesser notes:
  - "a part in ten thousand ... small enough to be nothing" in the fine-structure constant is wrong physics.
  - "partial pressure" is used for an oxytocin aerosol.
  - Some refrains repeat (the "bought hours, not days" line and the "number he had written down" line).
  - "grey" vs "gray".
- Reviewers liked the ending: the coda with Sera and the Kaelen material. Setting chosen by the factory: the generation ship *Keres*.
- 2026-10-20 SCP-08 / VNO-05 / BTT-09 merged, built and restarted, with the `client` provider added to each data folder.
- 2026-10-20 Rescue:
  - `set_book_model {writer: client/claude-code}`, then `reopen_book {mode: rewrite, chapters: [3, 4]}` gave round 3.
  - Claude wrote both rewrites through `get_client_task` / `submit_client_task`.
    - Ch3 (1,256 words) keeps Vera's sandbox tests and production patch, Aris's countdown (59 h) and Kaelen's chem-bank sums.
    - Ch4 (1,899 words) holds the filter at hour 9, the harness, the second fit (found once and logged, not buried), the one Command Node meeting at hour 41 (chem-bank now 22 %), and the snap with the fine-structure physics corrected and emergency white light.
    - The refrains and the tremor repeat were dropped.
  - DeepSeek reviewed: 3 pass, 3 revise. **Published** at 7.14 (enjoyment 8, genre fit 8, structure 8, originality 8, continuity 6, mechanics 6, prose 6). EPUB, cover and reader were made.
  - Round 3 cost about $0.02, reviews only. Total about $0.23.
- `set_book_model ... null` is refused on a published book, so `role_models.writer` stays `client/claude-code`. This is harmless because a published book runs no jobs. It is in the ROADMAP.

## Checked

- Read the round-2 reviews and `log.md` in `~/Scriptorium/books/the-local-patch/`.
- Round 3: Claude read the whole book (it comes in the rewrite task) and wrote ch3 and ch4. The published EPUB has not been opened by the user yet.

## Left to do

- The user reads the EPUB (`~/Scriptorium/books/the-local-patch/out/the-local-patch.epub`) and rates it (`rate_book`).
- Optional, for a higher score: a round on ch1, ch2 and ch5. The notes left are the repeated refrains in ch1/ch2, "partial pressure" and "fission blanket" in ch2, and "winter", the slip and "grey" in ch5. `reopen_book` takes only rejected books, so a published book needs a new feature first (in the ROADMAP).
- Optional: translate it (restart Claude Code first), or turn it into a visual novel.
