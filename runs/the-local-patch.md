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
| Scriptorium book | `the-local-patch` (stage `rejected`) |
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

## Checked

- Read the round-2 reviews and `log.md` in `~/Scriptorium/books/the-local-patch/`. The chapters themselves have not been read yet.

## Left to do

- **On hold (user, 2026-10-20)** until two features exist: Scriptorium jobs that Claude Code can take over MCP, and the same for VN Studio's model work. Plan: `.claude/tickets/external-llm-jobs/plan.md`. After that, rescue or rewrite this book (fix ch3/ch4 by hand, or start over with Claude writing it), then publish, read it and `rate_book`.
- Optional: translate it (restart Claude Code first), or turn it into a visual novel.
