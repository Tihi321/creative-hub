# The Hour That Happens Twice

Started 2026-10-21. Book 2 of the series *The Hartley & Varga Mysteries*, after *The Clockless God* (`runs/the-clockless-god.md`).

## Brief

- Idea / theme: the user asked for book 2, picking up the Nine, the Keeper of the Last Hour and the HUIT parcel. Claude pitched it and the user said "Yes, go".
  - HUIT is the Eighth of the Nine, whose seal is the mouth: Dagmar Vaňková, the voice of the Czech speaking clock. She wants out and is Stopped before Dec and Inès reach her.
  - The trail runs from Paris (Père-Lachaise, a grave dated to the second 2:30) to Prague: the Astronomical Clock, the Jewish Town Hall clock, a bell foundry, a clearing house.
  - The Fifth of the Nine, Renata Hollerová (the Bell), plans the "Collection of the Doubled Hour" on the night the clocks go back: a rite at the Orloj, and a theft that makes every payment in the repeated hour twice.
  - Vaulmont (VII) comes back as a voice on the telephone. Pichon is in Prague "for a Europol conference". There is a step toward the Keeper of the Last Hour (I, the key) and a hint of the Ninth (IX, the crown).
- Kind: prose book, format `novella`, aiming at about 45k words in about 18 chapters · adults · English.
- Art / music / voices: none ("just do the books part").
- Who writes: as in book 1. Claude does the editor-in-chief, architect and writer work through the `client` provider; Scriptorium's models do the research, the reviews, the archivist and the humanizer (DeepSeek chain).
- The brief JSON is in `.claude/temp/story-hour-twice.json`.

## Ids

| Tool | Id |
|---|---|
| Scriptorium series | `the-hartley-varga-mysteries` |
| Scriptorium story | `the-hour-that-happens-twice` (series_index 2) |
| Scriptorium book | `the-hour-that-happens-twice` (published, round 1, score 7.61) |

## Log

- 2026-10-21 Scriptorium was started with `-Force -Window` on branch SCP-13_client-search (5c93340), with the user's OK. Factory: no open stories outside inactive topics, spend $0.73 today, $5.58 this month.
- 2026-10-21 `add_story` made `the-hour-that-happens-twice`: novella, series index 2, with editor-in-chief, architect and writer on `client/claude-code`.

- 2026-10-21 The editor-in-chief's `start_book` was stuck in `waiting-provider`: its default, the free OpenRouter model, had used up its daily limit, and the scheduler waits instead of falling back (ROADMAP). Worked around by setting the agent to `client/claude-code` for that one job, then back to `null`. Claude answered start_book: novella, 45000.
- 2026-10-21 Claude wrote the pitch and the research plan (4 questions).
  - The research ran through the client search provider, done by two Claude subagents: the Orloj and summer time, Old Czech time, the Czech speaking clock, and the Jewish Town Hall clock.
  - **Finding that changed the plot:** the Orloj keeps Central European winter time all year (since 1912) and is never set back. It strikes two only at the second 02:00, and that is now the cue for the rite.
- 2026-10-21 Outline: 18 chapters in three acts (Paris 1-5, Prague 6-12, the doubled hour 13-18), 13 characters, 14 places, 11 threads.
  - The solution: Jan Vaněk's stop phrase "Gong oznámí dvacet pět hodin, nula minut, nula sekund", twenty-five o'clock on the one day with 25 hours.
  - The clues: the grave's "la seconde fois", the diary line "Jak židovské hodiny. Ten delší den.", the backwards tape, and the backwards bell line with its number chiselled off.
  - The builder script is `.claude/temp/hour/outline.py`.
- 2026-10-21 Outline review (DeepSeek): pass, structure 8. Its two notes are in `.claude/temp/hour/WRITER.md`: ch10 ends on a discovery rather than a third trap, and the ch11 bell line is printed with its tail and the gap.
- 2026-10-21 The ch1 draft failed three times with ECONNREFUSED. LM Studio was closed after the VN production, and drafting most likely needs its embeddings (nomic); not verified. `hub.ps1 start lmstudio`, then `retry_book`, and drafting resumed.
- 2026-10-21 Drafting. One Claude writer subagent per 3 chapters, a relay working the task loop. Instructions: `.claude/temp/hour/AGENT.md`; shared notes: `hour/NOTES.md`; chapters: `hour/chNN.md`.
- 2026-10-21 Chapters 1-3 drafted and accepted: 2,887, 2,887 and 2,752 words. The humanizer (DeepSeek) then trimmed each by about 30-60 words, with no em dashes and no canon changes seen. It still breaks some sentences into verbless fragments ("Not young.", "Eighty-four years old, widow of a judge, second floor..."), the ROADMAP finding from the earlier runs. It was left on, as the user asked for every book.
- 2026-10-21 Chapters 4-6 drafted and accepted, at about 2,950-3,000 words each. The continuity check asked for a ch5 rewrite (the train-or-bus argument, the departure time, whose phone got the nine calls, the Orloj's own hour); it was rewritten and accepted.
  - Canon set while drafting: Dagmar's flat is on the fourth floor; Maître Carrère is Kessler's lawyer; Dagmar remembers sending the parcel in April and lost only Thursday 15 October.
  - Act one now ends with the twins at the door and at the balcony at the same instant.
- 2026-10-21 Chapters 7-9 drafted and accepted (2,850-2,980 words); the check asked for a ch7 rewrite, which was accepted.
  - The archivist misread ch7 and recorded the twins as Hollerová's brothers. Ch8 corrects it in the text, and thread t45 in `bible/threads.md` was fixed by hand.
  - The bible also has duplicate character entries (three for the twins; dec / declan-hartley), the alias problem already in the ROADMAP.
- 2026-10-21 Act 1 review (chapters 1-6, DeepSeek): pass, structure 8. Its notes are in `hour/WRITER.md`:
  - pay off ZWEI cleanly;
  - vary the synchronised arrivals;
  - no third drugged drink;
  - make Božena felt (a ch13 scene);
  - fewer explanatory monologues.
- 2026-10-21 Chapters 10-12 drafted and accepted (2,858, 2,890 and 2,729 words). Ch10 ends on a discovery; ch11 prints the bell line and pays off ZWEI; ch12 has the escapes, the plan folder and the backwards reading. Jan's bell is melted down in ch12, so the line survives only in Inès's photos and notebook.
  - The archivist's ch11 summary called the day "Sunday 24 October"; it was fixed by hand to Saturday.
  - The check asked for a ch12 rewrite, which the next writer agent takes first.
- 2026-10-21 The ch12 rewrite was accepted. The checker's notes promised "three concrete fixes below" but listed none, so the writer fixed what its summary named: the bell is not melted, nothing pours before 18:00, and the missing number is a real problem (ROADMAP).
- 2026-10-21 Chapters 13-15 drafted and accepted (2,895, 2,829 and 2,665 words).
  - Božena's scene at the Domov Na Vrchu care home is in ch13. Pichon acts on his own authority there (Ferrand picked up in Paris; the invented night walk).
  - **Timeline fixed by the writer:** the Orloj strikes two at the very instant 03:00 summer time becomes 02:00, so the whole race happens inside one real hour. The outline's "an hour later" was wrong; WRITER.md now has the timeline.
- 2026-10-21 Act 2 review (chapters 7-12, DeepSeek): pass, structure 8. Its notes for act 3 are in WRITER.md: no fourth synchronised entrance, the number not the method, Pichon or Kroupová acting on their own authority, and varied scene shapes. The check asked for a ch15 rewrite.
- 2026-10-21 Chapters 16-18 drafted and accepted (2,706, 2,609 and 2,741 words); the ch15 and ch16 check rewrites were also accepted.
  - The ch16 checker claimed ch14 had Šťastný dead, which is wrong; the text now says plainly he is "only Stopped".
  - Ch18 closes the threads. The Keeper's bell is the Pummerin of St Stephen's in Vienna (from the writer's own knowledge, not researched), and the crown-sealed letter of the Ninth leaves the hook for book 3.
  - All 18 chapters are in, about 50k words. The book went to `reviewing` (round 0).
- 2026-10-21 **Round 0 review of the whole book** (all DeepSeek):
  - pass: beta reader (enjoyment 8/9/9, genre fit 8/9/9), developmental editor (structure 8 in all three acts), originality (9/8/9), line editor acts 1 and 3 (8);
  - revise: continuity (6 in all three acts), copy editor (6 in all three), line editor act 2 (6: the "the way a man who..." simile and "said nothing at all" tics) and the thread check (6: the token, and the woman on the train).
  - The engine asked for rewrites of ch3, 5-13 and 16-18.
- 2026-10-21 Claude sorted the notes in `.claude/temp/hour/ROUND1.md`. Several were reviewer errors, kept out of the rewrite:
  - the Jura clove tea is book 1 canon;
  - 10 and 25 October 2026 are a Saturday and a Sunday;
  - thirty-two years since 1994 is right in 2026;
  - the +420 number has the right length.
- The real fixes:
  - tense, comma and pronoun slips; time notation; the older bell in the shed for "three hundred years";
  - the train woman, who had Vaulmont's voice, now has her own and is a quiet Madame Ardouin hook;
  - the token thread closed in ch18;
  - a line pass on the tics and the humanizer's fragments.
  - Five Claude subagents revise the chapters in parallel into `hour/r1/`, and `hour/rw.sh` submits them as the rewrite tasks come.
- 2026-10-21 Round 1: all 13 rewrites were submitted by `hour/rw.sh` and accepted. Before submitting, Claude fixed the ch18 *Mami* line: Božena (born 1953) is the elder sister, and she calls whoever wears their mother's coat *Mami*.
- 2026-10-21 **Published** in round 1 at **7.61** (book 1: 7.73). Round 1 scores:
  - enjoyment 9/8/9, genre fit 9;
  - structure 8, originality 9/8/8;
  - prose 8/8/7, mechanics 8/6/6;
  - continuity 6 and threads 6, both still marked revise.
- What is left in the published text: small slips the round 1 checkers found that the engine does not send back for another round (a published book cannot be reopened; ROADMAP):
  - ch5, a bootlace "still knotted round his finger" after both laces stayed in the hold;
  - ch7, Šťastný's "in forty years I give eight" against the 1996 token;
  - ch18, the crown letter is signed "IX", which a checker reads as too explicit.
  - The woman on the night train is left open on purpose, as the series hook (pearls and grey cardigan, like Madame Ardouin in ch1); the thread check counts that as unclosed.
- About 51.4k words in 18 chapters, over the 45k target and slightly over the novella's 50k (book 1 was 50.7k).
- Cost: $0.87 in all (reviews, checks, archivist, researcher and humanizer on DeepSeek). Claude's work on the client provider cost nothing. Spend today $1.62 of the $5 cap.
- `get_series` lists both books: 1 published at 7.73, 2 published at 7.61.
- Outputs: `~/Scriptorium/books/the-hour-that-happens-twice/out/the-hour-that-happens-twice.epub`, `cover.png` (type-only cover) and `reader/`.

## Checked

- Claude planned every chapter. Writer subagents wrote them, and Claude read the agents' reports, every review and the humanizer's changes (spot-checked in ch1).
- The cover was looked at (type only, title and author right). The EPUB and the reader exist.
- Not checked by Claude: the EPUB in a reader app, and the book in the Scriptorium window. The user has not read it yet.

## Left to do

- The user reads it and rates it (`rate_book`).
- Optional: a translation (Book Translator, `clientOnly: true`) or a VN adaptation (`adapt_book`), as for book 1.
- Book 3: the Keeper of the Last Hour (the Pummerin, Vienna), the Ninth (the crown), and the woman on the train.
- LM Studio and Scriptorium are still running.
