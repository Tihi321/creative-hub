# The Umbrella Conductor

Started 2026-10-22. Made for HUB-04 (Scriptorium live check, `wait_for_book`). Claude did the model work.

## Brief

- Idea / theme: a Zagreb tram conductor (Ana Horvat, number 12 tram) who keeps forgotten umbrellas finds the owner (Mr Kovac) of the yellow duck-handled one.
- Kind: linear, one chapter, format `bedtime-story` (600-2000 words, age 3-6; the cheapest format) · children
- Languages: English
- Art: none · Music: none · Voices: off (book only, no VN made)

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | the-umbrella-conductor |
| Scriptorium book | the-umbrella-conductor (same slug; the published title became "The Yellow Umbrella") |
| Book Translator project | none |
| VN Studio project | none |

Book folder: `C:\Users\Infplane\Scriptorium\books\the-umbrella-conductor`, EPUB in `out\`.

## Log

- 2026-10-22 18:2x `add_story {format: bedtime-story, models: {editor-in-chief, architect, writer: client/claude-code}}`. The editor-in-chief's `start_book` came as a client task, so `add_story {models}` now reaches `start_book` (SCP-14 fix confirmed).
- Client tasks answered by Claude: start_book, pitch, research_plan (no research), outline, research_prep (none), draft_chapter (1840 words), rewrite round 1 and 2 (rewrite_chapter). Reviewers, humanizer and publisher ran on Scriptorium's own models (deepseek-flash; read-aloud-reviewer on lmstudio/nail-qwen3.6-35b-a3b-mtp).
- Round 0 review: line-editor "revise" (repeated "tap, tap, tap", repeated phrases) and read-aloud-reviewer "revise" (it said "story is set in 1989" and called "three winters" a contradiction with the 1989 ticket; wrong). Added `add_book_note` that the story is set in the present and 1989 is only the ticket year. Round 1 and 2 fixed the prose; published at round 2, score 8.53 (read_aloud 8, prose 8, structure 8, others 9).
- `wait_for_book` returned `client-task` each time a request waited, `timeout` while reviewers ran, and `done: true, reason: published` at the end.
- Cost today: $0.044 (all DeepSeek reviewers/humanizer), nothing for Claude's tasks.

## Checked

- The text was read by Claude only. Not played, not read by the user.
- Cover state `done`, EPUB exists.

## Left to do

- The user reads it. Title changed from the fixed "The Umbrella Conductor" to "The Yellow Umbrella" (see HUB-04 report); restored with `rename_book` on 2026-10-22 (cover, EPUB and reader remade).
