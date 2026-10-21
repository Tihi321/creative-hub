# The Lighthouse That Kept Lists (humanizer test)

Started 2026-10-21.

## Brief

- A test of the SCP-10 humanizer live: a short story (`short-story`, 4 chapters, about 5-6k words). It is a warm literary comedy on a Dalmatian island.
- Who writes: Claude does the architect and writer work through the client. The humanizer and the reviewers run on Scriptorium models.
- To check: the `humanize--chNN` job runs after drafting; compare `chapters/history/` with the humanized chapter; tic counts before and after.

## Ids

| Tool | Id |
|---|---|
| Scriptorium book | `the-lighthouse-that-kept-lists` |

## Log

- 2026-10-21 `add_story` with format short-story and models architect and writer set to client/claude-code. Started; stage pitch.

- 2026-10-21 Claude wrote the pitch, research plan, outline (4 chapters) and drafts (1,694 + 1,482 + 1,431 + 1,364, about 5,970 words), then the round-1 rewrites of ch1 and ch3. A successor agent is finishing (the ch4 rewrite).
- **Humanizer, seen live** (from the rewrite prompts, which carry the current, humanized text). It ran after each draft, but on the free fallback model it:
  - added many **em dashes**, against the house rule;
  - broke a **continuity fact**: the key "under the third flowerpot" became "a cracked flowerpot by the keeper's porch";
  - added contractions to Dino's deliberately formal speech;
  - used "drunk" similes twice and turned sentences into fragments ("Told herself...", "Didn't mention it.").
  - Some of its edits were good ("clucked disagreement", "like a clock with a grudge").

  The rewrites put the canon back and took the dashes out. Fix in SCP-13: an em-dash guard, a numbers guard, a new-names guard, a register rule in the prompt, and a capable model first in its chain.

- 2026-10-21 The successor agent rewrote ch4 (round 1): "SPARES FOUND. FOUR. NOT THE BUTTONS.", the run-on sentence split, Dino formal again, the key back under the third flowerpot.
- 2026-10-21 **Published at 9**: enjoyment, genre fit, continuity, mechanics, structure, prose and originality all 9, in 1 round. EPUB, cover and reader are in `~/Scriptorium/books/the-lighthouse-that-kept-lists/out/`.
- **Humanizer measured** (draft `ch-NN-r0.md` against `ch-NN-r0-humanized.md`, pre-SCP-13 build, free fallback model):

  | Chapter | Words | Em dashes | "It was" openers |
  |---|---|---|---|
  | ch01 | 1694 → 1548 | 0 → 8 | 3 → 0 |
  | ch03 | 1431 → 1315 | 0 → 7 | 1 → 0 |
  | ch04 | 1364 → 1364 | 0 → 0 | 2 → 2 (unchanged) |

  The pass removed the stacked "It was" openers and tightened the text by about 9%. It also added em dashes and changed canon facts. SCP-13's guards (em dashes, numbers, new names) refuse exactly those changes now.
- The copy editor left one small slip in the published text: ch3 says Ante's list praised "FIFTY YEARS" of lemons, while Ivka says fifty-five. A published book can't be reopened (a ROADMAP item).

## Checked

- what was looked at or played, by whom

## Left to do

-
