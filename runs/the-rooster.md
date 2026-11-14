# The Rooster

Started 2026-11-14. Book only (the user said no visual novel).

## Brief

- Idea / theme: "The Predictable Author" seeds (does predictability disprove free will; Peter's denial, Gethsemane, Oedipus). Source chat: https://claude.ai/share/49afbbfe-6ab6-46a9-8278-69f88e4f3553 (not fetched; the pasted seeds were used).
- Kind: novella, adults, literary fiction · Language: English
- Ending: (b) the model predicts even her last act and she finds peace in it.
- Art / music / voices: none (book only)
- Brief file: `.claude/temp/rooster-story.json`; drafts as submitted: `.claude/temp/rooster/ch01.txt` … `ch14.txt`

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | the-rooster |
| Scriptorium book | the-rooster (published, score 8.56, 26,419 words, 14 chapters) |
| Book Translator project (hr) | the-rooster-hr-1c4fee (clientOnly, translator only; glossary/proofreader/QA off; brief + 37-term glossary set by hand: `.claude/temp/rooster/hr-brief.json`, `hr-gloss.json`) |

## Output

- EPUB: `C:\Users\Infplane\Scriptorium\books\the-rooster\out\the-rooster.epub`
- Cover: `...\out\cover.png` (byline "Culo", the writer persona's name in Scriptorium)
- Reader: `...\out\reader\`

## Log

- 2026-11-14 Started Scriptorium (`-Force`, user chose "Scriptorium + you write"). `add_story` with every role on `client/claude-code`; `set_factory_only the-rooster`.
- Main session did editor-in-chief, architect (pitch, outline, no research) and writer. A background subagent did the reviewer, humanizer and archivist roles.
- LM Studio's process was up but its API server was down, so chapter indexing waited on embeddings. Fixed with `lms server start` and `lms load text-embedding-nomic-embed-text-v1.5`. `hub.ps1 status` reported lmstudio "up" all along, which it gets from the process, not the API.
- Rewrites from review: ch03 (notebook count, Ruth as sealing witness), ch02 (the rooster is new this spring, so the notebooks mention "a rooster", not Bishop), ch13 (word count, "only the last sentence differs"), ch14 (Low Water notebook, last envelope). The queen move became "sixteenth" in review, consistently.
- Published. Cleanup: book models set to null, `only` cleared, factory unpaused in config, Scriptorium stopped (it was down before the run).

## Checked

- Final chapter files: chess move numbers are consistent; the cover renders.
- Not checked: the EPUB opened in a reader app. The user has not read it yet.

## Left to do

- The user reads the EPUB.
- Known leftovers in the published text: typo "in Agnes's hand's reach" (ch11); soft points not revised: divorce timing (ch1 vs ch6), two dice over 36 names (ch5), Calvin passage reads as lecture (ch10), thesis stated more than once (ch11, ch14), some repeated tics. Fixing needs Scriptorium restarted and a republish.
- Hub gap: `hub.ps1` status checks the LM Studio process, not `http://127.0.0.1:1234/v1/models`.

## Croatian translation (2026-11-14)

- Book Translator project `the-rooster-hr-1c4fee`, clientOnly, translator only (no glossary/proofreader/QA agents); brief and 37-term glossary written by hand.
- 34 chunks were translated by 4 parallel agents; all were accepted. A consistency pass followed: "deset do pet" (one range had "pet do pet"), Halvorsen is "trajektaš", the crow is "kukurikati" (the chapter title keeps "Prije nego pijetao zapjeva"), and chunks 1-17 were converted from „…” dialogue to the en-dash dialogue that 18-34 used.
- Export: `C:\Users\Infplane\Scriptorium\books\the-rooster\out\Pijetao.hr.epub` (cover: text title page). Spot check: 23,934 words, no English left, key lines present, no „ left.
- Not done: proofreading by a second reader; the user has not read it. Book Translator stopped again (it was down before).

## Tool fixes and byline (2026-11-14)

- Merged and pushed: HUB-34 (hub status/start check the http URL), BTT-30 (typography rule, dialogue-style check, previous-passage note), SCP-60 (byline) plus SCP-60_byline-fix (the whitespace regex dropped every "s").
- Byline: pen name "Mara Kestrel", set as the default in `~/Scriptorium/config/settings.md` (`byline:`) and on this book with `set_book_byline`. Cover PNG, EPUB dc:creator and title page now show it; the credits still name the AI writer (Culo). Croatian EPUB re-exported with the same author; Book Translator's new check says its dialogue style is consistent (dash).
- Cost note: the publish step ran on `deepseek/deepseek-flash` (the publisher role was not set to client), $0.0104. Everything else was $0.
