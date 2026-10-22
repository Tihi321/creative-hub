# ALS162 explainer (newspaper test)

Started 2026-10-21.

## Brief

- A test of the SCP-12 newspaper live: one `article` (600-1,800 words) in the technology section (topic `news-technology`). The subject is the ALS162 long-wave time signal from Allouis and who depends on it.
- Who writes: Claude writes it (the writer role on the client). The architect, the research (Tavily news), the humanizer and the reviewers run on Scriptorium models.
- To check: `out/article.html` with references, no cover or EPUB, and the article shown in the Newspaper tab.

## Ids

| Tool | Id |
|---|---|
| Scriptorium book | `france-s-atomic-clock-on-air-the-als162-signal-t` (published round 3, 7.27, `out/article.html`) |

## Log

- 2026-10-21 `add_story {format: article, topic: news-technology, models: {writer: client/claude-code}}`. With no title given, the story slug came from the premise (long). The editor-in-chief's headline then gave the book slug `france-s-atomic-clock-on-air-the-als162-signal-t`, which is cut short. Stage: pitch.

- 2026-10-21 Pipeline ran end to end as an article: pitch, research plan, research, outline (one chapter), research prep (Claude asked 3 questions), draft (Claude, 1,493 words with [n] citations), humanizer, reviews, rewrite (Claude, 1,132 words), humanizer, reviews.
  - Headline set by Scriptorium: "France's ALS162 Signal Keeps 300,000 Clocks in Step".
- 2026-10-21 **Rejected** at 6.27 (accuracy 7; enjoyment, genre fit, mechanics and prose 6). The fact-checker (must pass) said revise because of "negative claims about absence of public records that lack citations". No `out/article.html`, as expected for a rejected book.
  - Root cause: **no web search**. `TAVILY_API_KEY` is not set, so every Tavily search returned nothing ("no search provider gave results ..."), and the other search engines except Wikipedia are stubs. All the research notes came from English Wikipedia pages, so the questions on ANSSI, funding, the 2022 cable theft and the TDF plans had no answers, and the article had to keep saying "not on record".
- Humanizer, seen live:
  - Round 0: the free model (`openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, which the line-editor chain fell back to) cut the text from 1,493 to 1,277 words, more than 10%. The guard kept the original.
  - Round 1: it ran and was saved (`humanized: 1`); the history has `ch-01-r0-humanized.md`.
- The user chose to have **Claude Code do the web research**: SCP-13 adds a client search provider. When it is built: rerun the research with Claude answering, `reopen_book {mode: rewrite}`, check the published `article.html`.

- 2026-10-21 Scriptorium was restarted on SCP-13. The migration added the `client-search` provider (`search_order: [tavily, client-search, wikipedia, ...]`).
  - Four `ask_researcher` questions for the article (operator and guarantee, outages, spoofing and jamming, alternatives) became 4 `searcher/web_search` client tasks. A researcher subagent answered them with WebSearch and WebFetch, using real pages and verbatim excerpts, and all 4 were accepted.
  - Sources: France Horlogerie and Presse Agence (2026: extended to end 2034 under ANFR), Telesatellite (power cut to 675 kW from 31 Mar 2026; ANFR report on after 2034 due end 2027), LNE-SYRTE / LNE-OP bulletins H 667/668/705 (the 2023 faults and outages), the ANFR-DGITM jamming guide (2024), the ANFR 2016 press release, and Next 2024.
  - The task asked for news from the last 7 days. Nothing that fresh exists for this subject, so the researcher returned the newest official sources with their real dates.
- 2026-10-21 `reopen_book {mode: rewrite}`: round 2 (extra round). Claude rewrites it on the new research.

- 2026-10-21 Round 2: Claude rewrote it (about 1,050 words). **Rejected again** at 6.91: accuracy 9 and mechanics 9, but enjoyment 6, genre fit 5 and prose 6. The fact-checker flagged one claim that was cited only from a research note.
  - Root cause, a **pipeline gap**: the 4 new notes never reached the fact base (`factbase/sources.md` and `facts.md` were unchanged), and the rewrite prompt showed only the old Wikipedia sources and notes. The writer had no [n] numbers for the 2034 extension, the 675 kW change, the jamming guide and so on, so it had to leave them out.
  - Also: the researcher's notes on disk do not hold every fact the searcher returned. The 2023 faults and the 2027 report were in the search results, not in the summarised notes.
- The fix is SCP-13 Part G (late research reaches the fact base). After it: build, restart, `reopen_book`, and Claude rewrites again with all the sources numbered.

- 2026-10-21 SCP-13 Part G was built and Scriptorium restarted. `reopen_book` gave round 3. The live refresh job `factbase--refresh--r3` merged 13 notes, and `sources.md` now numbers [7]-[15]:
  - [7] LNE-OP Bulletin H 705
  - [8] Telesatellite 2026
  - [9] France Horlogerie 2026
  - [10] Presse Agence
  - [11] LNE-SYRTE 2019
  - [12] Next 2024
  - [13] LNE-SYRTE RNT
  - [14] ANFR-DGITM jamming guide 2024
  - [15] ANFR 2016
- Claude rewrote it (about 1,240 words):
  - It opens on the five Tuesday maintenance pauses of September 2026 [7], with the users and this year's news (the cut to 675 kW and the extension to end 2034).
  - It goes through history, how the time is made, power, the sovereignty and jamming case, and the alternatives.
  - It closes on "Eight years to choose".
  - Each figure appears once. The humanizer left it unchanged.
- **Published at 7.27**: accuracy 10 (fact-checker pass), enjoyment 7, genre fit 6, prose 6, mechanics 6. `out/article.html` and `out/article.md` were written; there is no cover or EPUB, as designed.
- **Bug found live in Part G:**
  - The refresh logged "83 new key fact(s)", but `facts.md` kept the old 20 (the 14+6 per-chapter cap kept the old facts and dropped the new ones).
  - The writer's numbered sources come from the kept facts, so the prompt listed only [1]-[6].
  - The writer cited [7]-[15] from `sources.md`, which the fact-checker's prompt did list, and it passed at 10.
  - The fix (fresh facts win the cap, and the sources of fresh notes are always listed) was sent back to the Part G implementer.
- Remaining editor notes, which a published article cannot take (a ROADMAP item):
  - the opening and closing read as an outage, not maintenance;
  - the power sequence is muddled;
  - "government" should be lower case;
  - "the every decade" subhead;
  - "The results are tight".

## Checked

- what was looked at or played, by whom

## Left to do

-
