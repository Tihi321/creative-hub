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
| Book Translator project | `the-hour-that-happens-twice-hr-9af646` (Croatian, HUB-05, clientOnly) |

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

### 2026-10-22 HUB-05 Croatian (setup, plan steps 1-3 and the glossary of step 4)

- Step 1: `hub.ps1 status`: book-translator up (pid 29084, port 47811) on master 2a21970 (BTT-11 to BTT-14 merged, `out/engine/index.js` built 17:53).
- Step 2: book 1's glossary (project `the-clockless-god-hr-2945aa`, 44 terms) plus the HUB-02 VN project's extra terms (`the-clockless-god-3-hr-ac0756`, 150 more, all edited to agree with book 1) plus the HUB-02 editorial words (atelijer, nacrti, kućište, kotačići, prstenovi, posuđen / na zajam): 202 rows in `.claude/temp/hub05/hv-glossary-hr.json` and the readable `hv-glossary-hr.md`. Book 1's stored brief turned out to be the English-headed one the glossary pass wrote, not the Croatian one.
- Step 3: `create_project {sourcePath: the EPUB, targetLanguage: hr, clientOnly: true}` made **`the-hour-that-happens-twice-hr-9af646`** (format epub, as book 1; the README keeps book folders for VN scripts only). All four agents on `client/claude-code`. Croatian brief from `.claude/temp/hub05/brief.txt`: title "Sat koji se dogodi dvaput", perfekt only, Dec and Inès "ti" throughout, Pichon and the Prague cast "vi", one word per term, Czech/French/Latin/German/Hungarian kept and not flagged, the Croatian place forms, book 1's series terms, "Naš je restaurator" masculine if it recurs, the cast (Maître Carrère is a woman).
- Glossary seed (`update_glossary`, 37 rows, `.claude/temp/hub05/setup/seed.json`): only book 1 / HUB-02 terms that occur in book 2 as whole words, checked in context. Left out as false or harmful matches: "None" (English "none"), "Stopped" (69 of 70 hits are the verb; the term is in the brief instead), "the word", "aisle", "pick", "gates", "the Rule", "grille", "service stair".
- Step 4 (glossary): 14 passes, all answered by Claude as role `glossary` (answers in `.claude/temp/hub05/gl/ans1..14.json`). 244 terms. Choices: Prag, Staromjestski trg, Staromjestska vijećnica, Orloj (praški astronomski sat), Stari grad, Židovska vijećnica, Karlov most, Praški dvorac, Vltava, Nürnberg, Beč; Czech districts, streets and names kept with diacritics (Vinohrady, Žižkov, Holešovice, Pankrác, Josefov, Kožná, Liliová, Domov Na Vrchu, U Tří kohoutů, paní); žeton, govorni sat, čuvar (Orloja, groblja), kostur / Smrt, Naplata udvostručenog sata, fraza za zaustavljanje, dan koji je dulji od ostalih, ljevaonica zvona Holler, plašt / jezgra / lažno zvono, poluge, terca; chapter titles in Croatian ("Pichon jede knedlíky" keeps the Czech word); the backwards bell line and all Czech/Latin/French lines kept letter for letter.
- After the passes: 69 chunks of up to 1500 tokens. The glossary pass had overwritten the brief again (runner.ts:174, known); restored with `set_brief` from `brief.txt` plus a section of the new book-2 terms (6,339 chars). The first ~8 chunks were already leased under the overwritten brief (still Croatian, with the tense, address and foreign-text rules). Then `update_glossary` (242 rows, `.claude/temp/hub05/setup/glossary_fix.json`) fixed substring traps the passes had added: "pension" (would hit "pensions") became "pension in Liliová" = pansion u Liliovoj plus "pensions" = mirovine; "lever" (hits "clever") became "levers"; "Old Town" (inside "Old Town Square") and "Cover" (inside "discover") removed.
- QA (role `qa`, same agent; translators and proofreaders were other workers): 79 QA tasks answered (69 reviews, one per chunk, and 10 rechecks). Translation quality is high; tense, address (Dec/Inès "ti", Pichon and the Prague cast "vi") and the series terms held. Real findings raised: 3 major (d5.3 the clock face taken out of the recess, d19.9 "mostić" for the clockwork-room gangway, d19.36 "ljepljiva traka" for the magnetic tape), all fixed by the pipeline; 18 minor ones (consistency: "u prva dva sata" for "the first two o'clock", "kućište" reused for paddle boxes and a case clock, mapa/fascikl, inženjer/tehničar, and a few grammar slips). Minor issues do not trigger fix tasks, so all 18 are still in the text: list with suggestions in `.claude/temp/hub05/qa/open-findings.txt` for the step-5 editorial pass.
- 2026-10-22 Project status `done`, 69/69 chunks: 62 done, 7 flagged (5, 7, 8, 23, 41, 46, 50). Every flag is the automatic "untranslated" check on lines kept on purpose (the phonetic GONG line, 2 H 30 LA SECONDE FOIS, VOX TEMPORIS NON MENTITVR, the Czech diary line, the backwards bell line twice, the Gong oznámí . . . line), as in HUB-02. Brief intact at the end (6,339 chars). Spend $0. Not done yet: plan step 5 (editorial pass), 6 (export), 7 (log), 8 (the user reads it).

### 2026-10-22 HUB-05 Croatian (steps 5-7: editorial pass, sweep, export)

- Step 5, editorial pass: three editor subagents read every segment of their range and fixed it with `edit_chunk` (rules in `.claude/temp/hub05/EDITOR.md`): e1 changed **45 segments** in chunks 1-23, e2 **56** in 24-46, e3 **65** in 47-69 (166 in all). Tense (perfekt only), address (Dec/Inès "ti", Pichon and the Prague cast "vi", Šťastný and Dagmar "ti" to each other), one word per object, the 18 open QA findings, the contents page. The term choices each agreed are in `.claude/temp/hub05/e1|e2|e3/terms.md`; translator notes in `WORKER-NOTES.md`.
- Whole-book sweep (one more agent, after the editors): all 69 chunks dumped to `.claude/temp/hub05/final/book.txt` (1,740 segments) and grepped for the decided terms. No leftovers: kapuljača, trench, fascikl, ekran, lowercase "monsieur Hartley", "s kapljicom" (d19.4 already reads "prostorija u kojoj je kapalo", as d16.79), stolice for the nine chairs (stolac/stolci throughout; the other stolice are plastic or gilt chairs), ubrus, Kroupové, -yjev- forms of Šťastný, šalica for the stone cups (the remaining šalice are tea and coffee cups), himna, "u prva/druga dva sata", Staro Mjesto, Općina, kačket, Plink/Pljus, baguette, a declined "Madame Vargu/Varge", "ormar" for the bronze cabinet, sob (the reindeer is "irvas" in d17.9, d18.18, d18.38). No aorist or imperfect anywhere (also not as dialogue tags; 529 rekao/rekla). Kept after checking the context: d4.45 "list upijača" (a sheet of blotting paper, not the desk blotter), d8.30-32 "Pristajao je?" (the referent is the brojčanik, masculine, as in d4.31), Dec's "ti" + "Viléme" in d16.23 and d17.5 (asides to Šťastný when he is not there; to his face Dec says "vi", d11.83). Contents page d21.3-d21.20 matches all 18 chapter headings (dN.t / dN.1) word for word.
- Sweep fixes: no text changed. Five chunks still carried the automatic glossary check's minor flag, all false (the term is there, declined or shortened): 15 d6.36 "kartici sa sivom skalom", 19 d7.35 "iz pribora za jelo", 32 d10.89 "na kotačnom parobrodu", 43 d13.94 "crtaonici"/"jamu", 69 d21.11 "Vltavi". Each was re-saved unchanged with `edit_chunk` to clear it (text compared before/after: identical). Project: `done`, 69/69 done, 0 flagged, 0 client tasks waiting, $0, glossary 242 rows.
- Step 6: `export_project` wrote `~/BookTranslator/projects/the-hour-that-happens-twice-hr-9af646/output/the-hour-that-happens-twice.hr.epub`, copied to **`runs/the-hour-that-happens-twice/the-hour-that-happens-twice.hr.epub`** (373,034 bytes, sha256 5a72d24a…7fe97). Checked: zip valid, `mimetype` first and stored; all XHTML/OPF/SVG parse; every manifest file present; `dc:language` hr; `dc:title` "Sat koji se dogodi dvaput", also the `<h1>` of the title page and every page `<title>`; nav "Sadržaj" with the 18 Croatian chapter titles; cover present (`images/cover.png`, `properties="cover-image"`, cover.xhtml first in the spine). Words: **45,525** in Croatian vs **51,565** in the English EPUB by the same count (88%; book 1: 43,744).
- What the export lacks (as in book 1's EPUB): the cover is the English image, with "The Hour That Happens Twice", "COMIC MYSTERY ADVENTURE" and "AI-written · 2026" baked into the PNG, and its alt text stays English ("Cover of The Hour That Happens Twice"). Book Translator copies the source cover and does not translate image text or the alt attribute. The title page's credit line is in Croatian.
- Book 1 check (read only): `runs/the-clockless-god/the-clockless-god.hr.epub` has **0** "reče" and no aorist dialogue tags (0 upita/odgovori/doda/viknu/… after a closing quote; 361 rekao/rekla). The "reče Dec" a translator saw is in project `the-clockless-god-hr-2945aa` chunk 4's `translation` and `proofread` fields (7 "reče" in d3.6-d3.x); its `final` field, which the export uses, has none. Book 1 is fine; nothing was edited.

## Checked

- Claude planned every chapter. Writer subagents wrote them, and Claude read the agents' reports, every review and the humanizer's changes (spot-checked in ch1).
- The cover was looked at (type only, title and author right). The EPUB and the reader exist.
- Not checked by Claude: the EPUB in a reader app, and the book in the Scriptorium window. The user has not read it yet.

## Left to do

- The user reads it and rates it (`rate_book`).
- Croatian EPUB (HUB-05): the user reads `runs/the-hour-that-happens-twice/the-hour-that-happens-twice.hr.epub` (plan step 8). Book Translator gap to put in its own ROADMAP.md: a translated cover (the image's title text and the alt attribute stay English).
- Optional: a VN adaptation (`adapt_book`), as for book 1.
- Book 3: the Keeper of the Last Hour (the Pummerin, Vienna), the Ninth (the crown), and the woman on the train.
- LM Studio and Scriptorium are still running.
