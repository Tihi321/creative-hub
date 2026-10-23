# The Local Patch (short film adaptation): HUB-15 check C2

Started 2026-10-23 19:54, published 20:11. HUB-15 C2: Scriptorium's screenplay length handling fixes (SCP-29), live check.

## Ids

- Source: Scriptorium book `the-local-patch` (short story, 5 chapters, 7,723 words).
- Story / book: `the-local-patch-3`, format `short-film`, `C:\Users\Infplane\Scriptorium\books\the-local-patch-3`.
- Models: architect, writer = `client/claude-code` (this session); reviewers and publisher on `deepseek/deepseek-flash`.
- Screenplay: `runs/the-local-patch-3/screenplay.json` (published, score 7.09, 2 sequences, 9 scenes, 18 shots, runtime 120s).

## Decisions

- Target runtime 120 seconds (exactly 2 minutes, inside `runtimeRange` [60, 180] seconds) across 2 sequences (chapters): Chapter 1 "The Drift Interval" (~60s), Chapter 2 "The Living Patch" (~60s).
- 18 shots total (1 title card + 17 live-action shots), matching brief adapter note ("About 2 minutes, 15-20 shots, live action").
- Cast kept strictly from source and bible: Aris Thorne, Vera Lin, Kaelen Vance.
- All scene places match the story bible exactly: `Observation Core`, `Main Concourse`, `Bio-Integration Lab`, `Reactor Control Deck`.
- Round 1 scored 6.73 against threshold 7.00 with `max_rounds: 1`, resulting in `stage: rejected`. Book reopened via `reopen_book {mode: "rewrite"}` to execute round 2, incorporating reviewer feedback on dialogue timing, continuity ("climbed" vs "dropped"), and intercutting the climax. Published in round 2 at score 7.09.

## Timeline

- 19:54 `adapt_book` -> `the-local-patch-3`; start job `eic--start--n27--r0` had no model call and took 151 ms; title and genre taken from source.
- Pitch: 286 words (under 300 words limit), 2-sequence plan.
- Outline: 2 chapters, 3 characters, 4 places, style, thesis, terms, matching schema.
- Drafts: ch01 (10 shots including title card, 60s) and ch02 (9 shots, 60s); total runtime 120s.
- Length gate: passed cleanly (`status: ok, seconds: 120`), no length rewrites triggered.
- Reviews r0: 4 reviewer jobs on `deepseek/deepseek-flash` ($0.0076).
- Rewrites r1: ch01 (60s) and ch02 (60s) addressing scene compression, dialogue density, and climax staging.
- Reviews r1: 4 reviewer jobs on `deepseek/deepseek-flash` ($0.0072). Beta reader passed (8/8); continuity, developmental, line editor asked minor revisions (scores 6). Overall weighted score 6.73, below threshold 7.00. Because `short-film` format config specifies `max_rounds: 1`, the publisher rejected at round 1.
- Reopened: `reopen_book {book: "the-local-patch-3", mode: "rewrite"}` gave round 2.
- Rewrites r2: ch01 (Aris dialogue trimmed to 18 words and changed "dropped" to "climbed"; Vera aphorism made clipped; developmental pushback added; 60s) and ch02 (Kaelen line changed to life-support draw transient; Vera line made concrete "Now"; concourse surge intercut added; 60s).
- Reviews r2: 4 reviewer jobs on `deepseek/deepseek-flash` ($0.0068). Developmental editor upgraded structure to 8. Overall score 7.09.
- 20:11 **Published at round 2: score 7.09**, runtime 120s, screenplay JSON exported to `runs/the-local-patch-3/screenplay.json`. Total run spend: $0.0227.

## Checks

| Check | Result | Evidence |
|---|---|---|
| SCP-29: Writer prompts name seconds/shots, never words | **verified** | `draft_chapter`: *"Format: Short film. Age band: general readers. The whole film runs 60 to 180 seconds. This chapter is one sequence of it. The chapter should run about 60 seconds: its length is the sum of its shot lengths, so count seconds, not words. Add or cut shots to fit."*<br>`rewrite_chapter`: *"Format: Short film. Age band: general readers. Keep the chapter at about 60 seconds of film: its length is the sum of its shot lengths, and the words do not count (the whole film runs 60 to 180 seconds)."* Zero word-count length requests in writer tasks. |
| SCP-29: Length gate measures runtime, not words | **verified** | `book.md`: `length_gate: { status: ok, words: 1004, seconds: 120 }`. Although word target was 1200 and drafts totaled 1004 words, no cut/grow rewrite was scheduled because `seconds: 120` was inside `runtimeRange: [60, 180]`. |
| SCP-29: No unnecessary length rewrites ran | **verified** | `made.md`: No length rewrite jobs (`--len`) ran. Only review-driven editorial rewrites ran. |
| `get_screenplay`: runtime inside `runtimeRange` | **verified** | `runs/the-local-patch-3/screenplay.json`: `runtimeSeconds: 120` is inside `runtimeRange: [60, 180]`. |
| `get_screenplay`: shots, scenes, places | **verified** | 18 shots (1 title card + 17 live-action shots), 9 scenes across 2 chapters. Every scene place (`Observation Core`, `Main Concourse`, `Bio-Integration Lab`, `Reactor Control Deck`) is an exact match to the story bible. |
| Stop at published screenplay | **done** | Stopped at `get_screenplay` output saved to `runs/the-local-patch-3/screenplay.json`. No Flow video made. |

## Bugs found (Scriptorium backlog / observations)

1. **`short-film` format `max_rounds: 1` causes premature rejection:** In `seed/config/formats.md`, `short-film` defines `max_rounds: 1`. Screenplays undergo rigorous reviews from 4 distinct editors (continuity, line, developmental, beta). If round 1 lands at 6.73 due to minor dialogue polish and a single continuity word ("dropped" vs "climbed"), it rejects immediately rather than offering a standard round 2 revision pass like other formats (`max_rounds: 2`). Calling `reopen_book {mode: "rewrite"}` enabled round 2 and achieved 7.09 publication.
2. **`target_words: 1200` remains on `book.md`:** While the length gate correctly evaluates `seconds: 120` under SCP-29, `book.md` and `brief.md` still initialize with `target_words: 1200` derived from word-count defaults rather than runtime seconds.

## Not verified

- Video generation (Flow video pipeline not run, as instructed).
- Client models (`role_models: {architect: client/claude-code, writer: client/claude-code}`) remain in `book.md` as published history.
