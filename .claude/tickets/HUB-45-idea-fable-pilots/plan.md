---
status: approved
request: REQ-0033
repos: [C:/projects/Personal/creative-hub, C:/projects/Personal/scriptorium]
branch: HUB-45_idea-fable-pilots
updated: 2026-11-24
---

# HUB-45: idea-fable pilots

Request: `.claude/director/requests/REQ-0033-pilot-short-books.md` (requirements and acceptance criteria are binding).
Research: `research.md` (this folder). Concept cards: `concepts.md` (this folder). Scriptorium code plan:
`C:/projects/Personal/scriptorium/.claude/tickets/SCP-71-idea-fable/plan.md` (the contract for task group 1).

Branches: Scriptorium code on `SCP-71_idea-fable` in the Scriptorium repo; hub docs and run logs on `HUB-45_idea-fable-pilots` in
this repo. The pilot production itself changes no repo code.

Build reading (one line, per the global scope rule): **the full reading** - Scriptorium gets a real `fable` format (own writer
prompts, engine-checked back matter, story-only length gate and humanizer), and three published pilot stories are made with it at
$0 and handed to the user to read.

## Scope

An idea fable: one original English fiction story, one chapter, 1,500-2,000 words, humanized, in which an invented character lives
through ONE non-fiction idea; then a "What just happened" debrief (the idea in plain words, where it showed up, how to use it
tomorrow, sources), 3 multiple-choice quiz questions with answers and explanations, and a "Go deeper" list of 2-3 real books
followed by the fixed line "This story is original fiction. It is not a summary of these books and is not affiliated with or
endorsed by their authors or publishers." Byline "Taleidea Stories".

1. **Task group 1 (Scriptorium, SCP-71):** the `idea-fable` format, implemented by the `implement` skill in the Scriptorium repo
   from the SCP-71 plan.
2. **Task group 2 (production):** three pilots, one per book, with the cards the user picked:
   - *The Book of Elon* -> card `subtraction-neglect` -> story "The Second Window", slug `the-second-window`.
   - *The Best Minds* -> card `halo-effect` -> story "The Plain Title Page", slug `the-plain-title-page`.
   - *Seven Brief Lessons on Physics* -> card `gravitational-time-dilation` -> story "The Clock on the Hill", slug
     `the-clock-on-the-hill`.
   (The engine makes the slug from the fixed title with `freeSlug`; if it appends a suffix, the run log records the real slug.)
3. **Task group 3 (hub docs):** ROADMAP row, the skill note, one run log per pilot.

### Out of scope

- Audio, story packs, story-kit, Supabase, the Taleidea app, translation, a concept-bank store.
- Any change to another tool (VN Studio, Book Translator, the proxy ...), and any Scriptorium change outside SCP-71.
- Hand edits of `~/Scriptorium/config/formats.md` or `prompts/` (the SCP-71 migration and seed copy do it at start).
- Paid models, paid search, any spend above $0.
- An `-Only` option for `hub.ps1`.
- Deciding whether the ideas "click": that verdict is the user's.

## Files and modules to touch

| Group | Path |
|---|---|
| 1 | everything in the SCP-71 plan's file table (Scriptorium repo only) |
| 2 (live data, reversible, engine down) | `C:/Users/Infplane/Scriptorium/config/factory.md` (`paused`), `C:/Users/Infplane/Scriptorium/config/budget.md` (`daily_cap_usd`) |
| 2 (read only) | `C:/Users/Infplane/Scriptorium/ideas/*.md`, `books/*/book.md`, `books/<slug>/made.md`, `books/<slug>/log.md`, `jobs/queued/`, `config/providers.md` |
| 3 | `C:/projects/Personal/creative-hub/ROADMAP.md`, `C:/projects/Personal/creative-hub/.claude/skills/make-visual-novel/SKILL.md`, `C:/projects/Personal/creative-hub/runs/the-second-window.md`, `runs/the-plain-title-page.md`, `runs/the-clock-on-the-hill.md` (from `runs/_template.md`) |

## Task group 1: Scriptorium SCP-71 (code)

- Worker: the global `implement` skill, run in `C:/projects/Personal/scriptorium`, with the plan file
  `C:/projects/Personal/scriptorium/.claude/tickets/SCP-71-idea-fable/plan.md`, branch `SCP-71_idea-fable` from `master`.
- Inputs: the SCP-71 plan (contracts C1-C7). Output: the branch with the change, tests green (`yarn test`, `yarn typecheck`,
  `yarn lint`, `yarn build`), and a short changelog in the SCP-71 folder.
- Rules: no engine start, no live model call, no edit of `~/Scriptorium`. The pilots do not need SCP-71 merged: they run from the built `SCP-71_idea-fable` working tree. Commit or merge to `master` only with the user's yes.
- Interface handed to group 2 (from the SCP-71 plan):
  - format id `idea-fable` (flag `fable: true`, `words [1500, 2000]`, one chapter, `research: false`, `humanize: true`,
    `max_rounds: 1`);
  - the brief layout: `add_story {format: "idea-fable", sections: [Concept card, Key facts, Sources, Go deeper]}` (C7);
  - the chapter markup: story, then `## What just happened` with `**The idea.**`, `**Where it showed up.**`,
    `**How to use it tomorrow.**`, an engine-written `**Sources**` paragraph, `## Quiz` with `**1. ...**` + `A)`-`D)` lines x3,
    `### Answers` with `1. B. ...` x3, then the engine-written `## Go deeper` lines and the disclaimer (C4);
  - the chapter file's `words` and `get_book.lengthGate.words` count the story only; the gate window for a fable is exactly
    1,500-2,000.

## Task group 2: the pilot production

Done by one production worker that drives Scriptorium over its MCP server (`scriptorium`, `http://127.0.0.1:7341/mcp`), in this
hub. It is the only task that may start Scriptorium, and only after the user's explicit go in chat (hub `CLAUDE.md`). It keeps one
run log per pilot (`runs/<slug>.md`, from `runs/_template.md`) with every id, value and decision as it goes.

### 2.0 Pre-flight (all before any live edit or start)

1. **SCP-71 is built from its branch.** SCP-71 does not have to be merged to master for the pilots. Required: the Scriptorium working tree is on branch `SCP-71_idea-fable` (`git -C C:/projects/Personal/scriptorium branch --show-current`), the checker's PASS is recorded in REQ-0033, and `pwsh -File scripts\hub.ps1 build scriptorium` succeeds from that tree (a build is not a start). Committing or merging SCP-71 happens only when the user asks.
2. **Engine is down.** `pwsh -File scripts\hub.ps1 status` shows scriptorium down; no live owner of `~/Scriptorium/index/engine.lock`.
3. **What the factory would resume** (read only, record the lists in the first run log):
   - ideas with `status: open` in `~/Scriptorium/ideas/*.md` (research found 7: `peak-of-whispers`, `signal-lost`,
     `the-glass-horizon`, `the-gravity-garden`, `the-iron-tide`, `the-last-lighthouse-keeper`, `the-rust-runner`);
   - books whose `book.md` `stage` is not `published` or `rejected` (research found none);
   - files in `~/Scriptorium/jobs/queued/` (research found none).
   If a book is open or a job is queued, stop and tell the user: the guards below would hold it, but the user should know.
4. **ACP proxy and models.** `pwsh -File scripts\hub.ps1 status` shows `acp-proxy` up (if not, `pwsh -File scripts\hub.ps1 start acp-proxy`;
   `start scriptorium` would also start it as a requirement). `curl http://127.0.0.1:8787/v1/models` lists
   `codex/gpt-6-luna`, `codex/gpt-5.6-terra`, `claude/claude-sonnet-5` and `antigravity/gemini-4-hydrogen`; the same ids are rows
   of the `acp` provider in `~/Scriptorium/config/providers.md` (research: they are). The writer roles use the models in 2.2.
   A model the proxy does not list is replaced in the `models` map by another listed ACP cloud row, and the change is logged.
5. **Fix each card's sources.** For each of the three cards below, open every Sources URL (WebFetch or the browser pane):
   - each URL must open and support its key fact as worded; where `concepts.md` names a primary source that opens (NIST, GPS World,
     the Ole Miss lab page, the Zenodo copy of Thorndike 1920), use it instead of Wikipedia; Wikipedia is allowed for the pilots
     only where no primary or institutional source opens (decision 4); the run log marks each key fact that still rests on
     Wikipedia as "needs a better source before anything is public";
   - a fact whose source does not open is dropped, and Key facts and Sources are renumbered together (same numbers);
   - never cite Nisbett and Wilson (1977) (no open source); cite Adams et al. (2021) through the Ole Miss lab page (nature.com did
     not open); for time dilation the **higher clock runs faster** (NIST, 2010); ignore the NPR piece that has it backwards;
   - ISBNs only for Rosen (paperback 9780143132899) and Rovelli (Riverhead 9780399184413); the other books get none.
   Freeze the final card (all four sections, verbatim) in the pilot's run log under "Brief" before its `add_story`.
6. **The user's go.** Show the user: the three frozen cards, the two live-config edits below with their old and new values, the
   model map, and that Scriptorium will start with `-Force`. Wait for an explicit yes. Without it, stop here.

### 2.1 Live-config guards (engine down; record the old lines in the first run log; the budget edit is reversed at the end, the pause is kept)

| File | Line before (verify, research read it 2026-11-24) | Line during the pilots |
|---|---|---|
| `C:/Users/Infplane/Scriptorium/config/factory.md` | `paused: false` (no `only:` line) | `paused: true` |
| `C:/Users/Infplane/Scriptorium/config/budget.md` | `daily_cap_usd: 20` (`monthly_cap_usd: 40`, `per_book_cap_usd: null` unchanged) | `daily_cap_usd: 0` |

Edit only those frontmatter lines (Edit tool), nothing below them. `daily_cap_usd: 0` makes the router refuse every paid model
(ACP models are `local: true` and never budgeted, research Q6); `paused: true` stops any job and any idea start, so the 7 open
ideas do not start.

Then start: `pwsh -File scripts\hub.ps1 start scriptorium -Force`. Check at once with `factory_status`: `paused: true`, no running
jobs, no book in progress; and on disk: `~/Scriptorium/config/formats.md` contains `id: idea-fable` (the SCP-71 migration ran) and
`~/Scriptorium/prompts/writer/draft_chapter_fable.md` exists. If either is missing, `set_factory_paused` stays true, stop the engine
(`pwsh -File scripts\hub.ps1 stop scriptorium`), leave `factory.md` `paused: true` with no `only:` line, set `budget.md` `daily_cap_usd` back to 20, and report (the built `out/` is not SCP-71).

### 2.2 The `add_story` calls (exact shape; texts from the frozen cards)

Common fields of all three calls:

```json
{
  "format": "idea-fable",
  "byline": "Taleidea Stories",
  "genre": "literary fiction",
  "noLocalFallback": true,
  "models": {
    "editor-in-chief": ["acp/codex/gpt-6-luna", "acp/claude/claude-sonnet-5"],
    "architect": ["acp/claude/claude-sonnet-5", "acp/codex/gpt-6-luna"],
    "writer": ["acp/claude/claude-sonnet-5", "acp/codex/gpt-6-luna"],
    "humanizer": ["acp/claude/claude-sonnet-5", "acp/codex/gpt-6-luna"],
    "developmental-editor": ["acp/antigravity/gemini-4-hydrogen", "acp/codex/gpt-6-luna"],
    "line-editor": ["acp/antigravity/gemini-4-hydrogen", "acp/codex/gpt-6-luna"],
    "copy-editor": ["acp/codex/gpt-5.6-terra", "acp/antigravity/gemini-4-hydrogen"],
    "beta-reader": ["acp/antigravity/gemini-4-hydrogen", "acp/codex/gpt-6-luna"],
    "originality-checker": ["acp/codex/gpt-6-luna", "acp/antigravity/gemini-4-hydrogen"],
    "publisher": ["acp/codex/gpt-6-luna", "acp/claude/claude-sonnet-5"],
    "archivist": ["acp/antigravity/gemini-4-hydrogen", "acp/codex/gpt-6-luna"],
    "researcher": ["acp/antigravity/gemini-4-hydrogen", "acp/codex/gpt-6-luna"]
  }
}
```

Reviewers' research questions create `researcher` jobs for the book; without an ACP model the researcher falls to Strata (dropped by `noLocalFallback`) and then to paid (refused by the cap), and the job requeues for ever, stalling the book.

`noLocalFallback: true` keeps Strata, Gufo and Llama chat models out when the book's list runs out (so Strata does not take the GPU);
the embeddings are not a role and are not affected (risk below). The writer and the reviewers are of different families on purpose.
`humanize` is left to the format (on). `sections` always holds exactly the four headings `Concept card`, `Key facts`, `Sources`,
`Go deeper` (C7 of SCP-71); one fact or source or book per line, numbered `1.`, `2.` ... where shown.

**Pilot 1: "The Second Window" (`subtraction-neglect`, from *The Book of Elon*)**

```json
{
  "title": "The Second Window",
  "premise": "A ticket clerk at a small island ferry harbour is told the morning queue is too long and is handed money for a second window and a new booking app; on a foggy morning when the app is down she skips the steps nobody needs, and the queue is gone in minutes.",
  "plot": "Ines is blamed for the long queue at the harbour of Vessa and given a budget for a second window and an app. She plans to add both. On a foggy morning the app is down and the harbour master is away, so she must sell tickets alone; she drops the stamp, the carbon copy and the signature nobody has read in years, and the queue vanishes. Before she cuts anything else she asks why each step was there, and keeps the one that still protects someone. She tells the harbour master she does not need the second window.",
  "characters": [
    {"name": "Ines Mardal", "role": "ticket clerk at Vessa harbour, careful, used to adding a form when something goes wrong"},
    {"name": "Tomas Corrin", "role": "harbour master, kind, quick to spend money on new things"}
  ],
  "setting": "Vessa, an invented small island with one ferry harbour and one ticket office, today.",
  "style": "Close third person on Ines, warm and concrete, small physical detail, light humour.",
  "sections": [
    {"heading": "Concept card", "text": "Idea: Subtraction neglect\nDefinition: When people try to improve something, they reach for adding parts and rarely think of removing them, even when removing is better.\nMechanism: Adding ideas come to mind quickly; removing ideas take more effort and are often not thought of at all, more so when people are busy. The habit that helps is asking of every part, rule or step who asked for it and what happens if it is gone, and checking why it exists before cutting it.\nMisconception: Simplifying means cutting as much as possible. Deleting without knowing why a part is there is its own failure.\nRules: No real person or company. Do not retell or reword any engineering 'algorithm' or step list from the books. No app or brand names."},
    {"heading": "Key facts", "text": "1. In eight experiments, people asked to improve something found changes that remove parts less often than changes that add them (Adams, Converse, Hales and Klotz, Nature, 2021).\n2. They overlooked removing even more when they were not prompted to consider it, when they were busy with another task, and when they had fewer chances to notice that adding had limits.\n3. The researchers found that removing ideas were usually not thought of at all, rather than thought of and rejected.\n4. Chesterton's fence (G. K. Chesterton, The Thing, 1929): do not take away a fence until you know why it was put up.\n5. In the Toyota Production System, credited to Taiichi Ohno, muda names activity that uses resources without adding value; seven kinds of waste were listed."},
    {"heading": "Sources", "text": "1. Adams, Converse, Hales and Klotz, \"People systematically overlook subtractive changes\", Nature 592, 258-261 (2021), via https://sites.olemiss.edu/scilab/publications/people-systematically-overlook-subtractive-changes\n2. Same study, via https://sites.olemiss.edu/scilab/publications/people-systematically-overlook-subtractive-changes\n3. ScienceDaily, 7 April 2021, https://sciencedaily.com/releases/2021/04/210407135801.htm\n4. https://en.wikipedia.org/wiki/G._K._Chesterton\n5. https://en.wikipedia.org/wiki/Muda_(Japanese_term)"},
    {"heading": "Go deeper", "text": "*The Book of Elon*, Eric Jorgenson\n*Subtract: The Untapped Science of Less*, Leidy Klotz (2021)"}
  ]
}
```

**Pilot 2: "The Plain Title Page" (`halo-effect`, from *The Best Minds*)**

```json
{
  "title": "The Plain Title Page",
  "premise": "A village science teacher gives the top mark at the school fair to her most charming pupil and later finds his experiment never ran, while the quiet pupil's careful notebook, which she skimmed because its cover was plain, holds the real result.",
  "plot": "Hana judges the science fair of a small village school in an afternoon. Milo, bright and funny, presents a glossy poster and wins; Agata's notebook has a plain title page and gets a quick look. Days later Hana tries to repeat Milo's experiment for the next class and finds it could not have worked. She opens Agata's notebook properly for the first time and finds the measurements and a result that holds. She re-marks both, tells Milo kindly and Agata openly, and changes how she judges: one quality at a time, the work before the person.",
  "characters": [
    {"name": "Hana Petrak", "role": "science teacher at a village school, fair-minded, busy, fond of her pupils"},
    {"name": "Milo Fenn", "role": "pupil, eleven, charming and quick, not dishonest, careless with his experiment"},
    {"name": "Agata Sorn", "role": "pupil, eleven, shy and exact, keeps a plain notebook"}
  ],
  "setting": "An invented village school in hill country, one autumn week, today.",
  "style": "Close third person on Hana, gentle and honest, the classroom's small sounds and objects, no villain.",
  "sections": [
    {"heading": "Concept card", "text": "Idea: The halo effect\nDefinition: One impressive quality in a person makes us assume they are good at other, unrelated things too.\nMechanism: The mind prefers a simple, consistent picture, so a strong first impression leaks into judgments of other traits and of the person's mistakes. The opposite, one bad trait colouring the rest, is the horn effect. The cost falls on the person whose weaknesses go unseen and on the people overlooked beside them.\nMisconception: Only shallow people fall for it, and only for good looks. It is a general feature of judgment; teachers, managers and experts show it too.\nRules: No real person. Nothing about medicine or mental illness, no violence, no prodigy who breaks down, nothing from the real case of the starting book."},
    {"heading": "Key facts", "text": "1. In 1920 Edward Thorndike reported that officers rating soldiers on separate qualities gave ratings that were too high and too even, as if one general impression coloured the rest.\n2. In a 1972 study (Dion, Berscheid and Walster), people judged attractive people to have more desirable traits.\n3. In a 1974 study (Efran), mock jurors were more lenient with attractive defendants.\n4. Phil Rosenzweig argues that people who judge a company's leadership or culture are often swayed by its known results.\n5. The opposite, where one bad trait colours the judgment of the rest, is called the horn effect."},
    {"heading": "Sources", "text": "1. Thorndike, \"A constant error in psychological ratings\", Journal of Applied Psychology 4(1), 25-29 (1920), copy at https://zenodo.org/record/1429134\n2. https://en.wikipedia.org/wiki/Halo_effect\n3. https://en.wikipedia.org/wiki/Halo_effect\n4. https://en.wikipedia.org/wiki/The_Halo_Effect_(book)\n5. https://en.wikipedia.org/wiki/Halo_effect"},
    {"heading": "Go deeper", "text": "*The Best Minds: A Story of Friendship, Madness, and the Tragedy of Good Intentions*, Jonathan Rosen (Penguin Press; paperback ISBN 9780143132899)\n*Thinking, Fast and Slow*, Daniel Kahneman\n*The Halo Effect*, Phil Rosenzweig (2007)"}
  ]
}
```

**Pilot 3: "The Clock on the Hill" (`gravitational-time-dilation`, from *Seven Brief Lessons on Physics*)**

```json
{
  "title": "The Clock on the Hill",
  "premise": "Two sisters keep two matched precision clocks, one at a mountain observatory and one in a harbour town at sea level; when the clocks are brought together after many years they disagree by a sliver of time, and the sisters learn they have lived at very slightly different speeds.",
  "plot": "Maren runs the clock room of a mountain observatory; her sister Tove keeps the twin clock in her house by the harbour. They set them together when they are young and argue for years about whose life goes faster. When Maren retires she carries her clock down the mountain and the two are compared with an instrument: the mountain clock is ahead by a sliver far too small for any clock face to show. Maren explains why the higher clock runs faster. The sisters laugh at the tiny gap, and the story turns to what the years did with them, which no instrument measures.",
  "characters": [
    {"name": "Maren Lind", "role": "keeper of the observatory's clock room, precise, dry humour"},
    {"name": "Tove Lind", "role": "her younger sister, runs a chandlery in the harbour town, warm, sceptical of physics"}
  ],
  "setting": "An invented country: a mountain observatory high above a harbour town at sea level, across several decades up to today.",
  "style": "Close third person, alternating gently between the sisters, quiet and wry, concrete detail of clocks and the harbour.",
  "sections": [
    {"heading": "Concept card", "text": "Idea: Gravitational time dilation\nDefinition: Time passes more slowly where gravity is stronger, so a clock lower down runs slower than one higher up.\nMechanism: In general relativity the rate at which time passes depends on where you are near a mass. Everyday differences are tiny and were invisible for a long time; modern atomic clocks measure them across the height of a table, and satellite navigation must correct for them. Each person feels their own time as normal; the difference shows when the clocks are compared.\nMisconception: It only happens near black holes or close to the speed of light. It happens everywhere, even between the floors of a building.\nRules: The higher clock runs faster. Nobody can feel the difference; never suggest it makes a life noticeably longer. Give the sisters' clocks no number: the gap is a sliver seen only by an instrument. No real person or real observatory."},
    {"heading": "Key facts", "text": "1. A clock lower down, closer to a mass, runs slower than one higher up, and both observers agree which one runs slower; this is different from the time dilation caused by speed.\n2. In 1971 Hafele and Keating flew caesium clocks around the world on airliners; compared with a clock on the ground, the eastward clocks lost about 59 billionths of a second and the westward clocks gained about 273, as relativity predicted.\n3. In 2010 NIST compared two aluminium-ion atomic clocks, one raised about 33 centimetres above the other, and the higher clock ran slightly faster.\n4. NIST worked out that at that height difference the effect adds up to about 90 billionths of a second over a 79-year life.\n5. GPS satellite clocks lose about 7 millionths of a second a day from their speed and gain about 45 from the weaker gravity, a net gain of about 38 a day, so their rate is adjusted before launch."},
    {"heading": "Sources", "text": "1. https://en.wikipedia.org/wiki/Time_dilation\n2. https://en.wikipedia.org/wiki/Hafele%E2%80%93Keating_experiment\n3. NIST news, September 2010, https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal\n4. NIST news, September 2010, https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal\n5. GPS World, https://www.gpsworld.com/inside-the-box-gps-and-relativity/"},
    {"heading": "Go deeper", "text": "*Seven Brief Lessons on Physics*, Carlo Rovelli (Riverhead; ISBN 9780399184413)\n*The Order of Time*, Carlo Rovelli\n*Black Holes and Time Warps*, Kip Thorne"}
  ]
}
```

The texts above are the draft; the frozen card of 2.0 step 5 wins where the source check changed a fact or a source.

### 2.3 Per-pilot procedure (one pilot at a time, in the order 1, 2, 3)

1. `add_story { <common fields> + <pilot fields> }` -> `{slug, file, story}`. Record the story slug and file in the run log.
2. `set_factory_only { idea: <story slug> }`; `factory_status` shows `only: <story slug>`.
3. `set_factory_paused { paused: false }`.
4. Loop `wait_for_book { slug: <story slug>, timeout_seconds: 900 }` until `done`. After each return: record the stage; call
   `factory_status` and check spend today is still 0.00 USD and record `blocked`. If a job is blocked by `limitedModels`, or held back by the budget or with no usable model (for example a stuck `researcher` job), or a job of this book is still in `C:/Users/Infplane/Scriptorium/jobs/queued/` with no progress (a job skipped only because of the budget is never listed in `blocked`), for more
   than 30 minutes, fix it with `set_book_model { book, role, model: <a listed ACP cloud ref> }` and log it. A `reason: "client-task"`
   should not happen (no client models are used): if it does, log it and answer nothing; tell the user.
5. When the book is `published`, `rejected` or `failed`: `set_factory_paused { paused: true }`, then read the book log file `C:/Users/Infplane/Scriptorium/books/<slug>/log.md` (`get_book` returns no log) for a line starting `fable back matter:` (the engine logs back-matter problems it could not repair) and record it in the run log; such a line means K2/K4 need a close look. Then the checks (2.4).
6. Then the next pilot from step 1.

### 2.4 Checks on each result (record every check and its evidence in the run log)

| # | Check | How |
|---|---|---|
| K1 | Story 1,500-2,000 words | `get_book { book }` -> `words` (or the chapter front matter `words`) in 1,500-2,000; `get_book.lengthGate.words` is the count at gate time, before the humanizer and any round-1 rewrite, so it is not the figure: record it too, as information. Manual recount: `read_book_file { book, file: "chapter", chapter: 1 }` returns the raw file with its YAML front matter; strip the front matter, take the text before the line `## What just happened`, split on whitespace, count |
| K2 | Debrief complete | the back matter has `## What just happened` with `**The idea.**`, `**Where it showed up.**`, `**How to use it tomorrow.**` and a `**Sources**` paragraph equal to the frozen card's Sources lines; also fail if there is a second, model-written Sources or Go deeper block beside the engine's |
| K3 | Debrief facts trace to the card | a table in the run log: every sentence of the debrief that states a fact -> its `[n]` -> key fact n; any fact without a matching key fact fails; "Where it showed up" names only moments that are in the story |
| K4 | Quiz | exactly 3 questions, each with four options A-D; `### Answers` gives one letter per question; the worker answers each question from the story and the card and agrees that exactly one option is right |
| K5 | Go deeper and the fixed line | `## Go deeper` lines equal the frozen card's Go deeper lines; the disclaimer appears exactly once, word for word, as the last paragraph; also fail if there is a second, model-written Sources or Go deeper block beside the engine's |
| K6 | No real person depicted | read the story; also search it for the authors and people of the cards and books (Musk, Jorgenson, Klotz, Chesterton, Ohno, Rosen, Laudor, Thorndike, Kahneman, Rosenzweig, Rovelli, Einstein, Hafele, Keating, Thorne): none may appear in the story part (the back matter may name sources and books) |
| K7 | $0 | every row of `C:/Users/Infplane/Scriptorium/books/<book>/made.md` has `cost_usd: 0` and an `acp/...` model; `factory_status` spend today unchanged from before the start; `get_book.modelDeviations` empty or only ACP models (log any) |
| K8 | Byline and rendering | `get_book` shows byline `Taleidea Stories`; open the reader HTML in `paths.readerDir`: it has `<h3>What just happened</h3>`, `<h3>Quiz</h3>`, `<h4>Answers</h4>`, `<h3>Go deeper</h3>` and the disclaimer; `paths.epub` exists |
| K9 | Humanized | chapter front matter `humanizer_result` is `rewritten` (or `kept`, logged with the reason) |

**One retry rule.** At most one retry per pilot, then stop that pilot and report:
- `failed` -> `retry_book { book }`;
- `rejected` -> `reopen_book { book, mode: "rewrite" }`;
- `published` but K1-K6 or K8 fails -> `add_book_note { book, chapter: 1, text: "<what failed, concretely>" }` then
  `reopen_book { book, mode: "rewrite", chapters: [1] }`.
Unpause with `set_factory_paused { paused: false }` for the retry, wait as in 2.3, check again. A K7 failure (any paid cost) is
never retried: pause, stop the engine and report at once. "Restore" at any stop means the same: the factory is left `paused: true` with no `only:` line, and `budget.md` `daily_cap_usd` is set back to its recorded value (20) (steps of 2.5). A second failure of the same pilot goes to the user, not to a
second retry.

### 2.5 Restore (after the third pilot, or at any stop)

1. `set_factory_only { idea: null }` (removes `only:` from `factory.md`); `set_factory_paused { paused: true }`.
2. `pwsh -File scripts\hub.ps1 stop scriptorium`; `status` shows it down.
3. With the engine down, leave `factory.md` with `paused: true` and check there is no `only:` line (decision 3: the factory stays
   paused; this differs from the recorded `paused: false`); set `budget.md` back to the recorded `daily_cap_usd:` value (20).
   Record the before/after lines in the run log, including that `paused` differs from the before-state. Tell the user: they
   unpause when they want the 7 open ideas written.
4. `git status` of the Scriptorium repo is unchanged by the production (the production changes no code; it need not be clean, since SCP-71 may be uncommitted).

### 2.6 Hand-off to the user (the end of task group 2, not "done")

Give the user the three stories to read: for each, the title, the reader HTML path (`paths.readerDir`), the EPUB path, the story's
word count, and the K1-K9 results. Ask for a verdict per story: does the idea click? Record the verdict in each run log
("Checked"). The ticket is done only when the user has read all three (REQ-0033 acceptance).

## Task group 3: hub docs

- `ROADMAP.md`, "Tasks, in order", new row after row 37:
  `| 38 | HUB-45 | Idea-fable pilots: Scriptorium's idea-fable format (a story, then a debrief, a three-question quiz and a Go deeper list) and three pilot fables at $0: The Second Window, The Plain Title Page, The Clock on the Hill (.claude/tickets/HUB-45-idea-fable-pilots/plan.md, REQ-0033) | scriptorium (SCP-71) | user's go to start Scriptorium; user reads the three stories | Open |`;
  and in "Each tool's own roadmap", the Scriptorium cell gains "SCP-71 (idea-fable format) for HUB-45". Update the status cell when
  the pilots are handed over and again when the user has read them.
- `.claude/skills/make-visual-novel/SKILL.md`: a short "Idea fable (a story that teaches one idea)" note: `add_story` with
  `format: "idea-fable"`, the four sections (Concept card, Key facts, Sources, Go deeper), byline, and that the engine writes the
  sources, the book list and the disclaimer. No other skill change.
- `runs/the-second-window.md`, `runs/the-plain-title-page.md`, `runs/the-clock-on-the-hill.md`, each from `runs/_template.md`
  (Kind: idea fable; Languages: en; Art, Music, Voices: off). Each holds: the frozen card; the pre-flight results (the first log also
  the resume lists and the 2.1 before/after lines); story and book slugs; every MCP call that changed state with its time;
  `lengthGate`; K1-K9 with evidence (the K3 table); any retry; the restore lines; the user's verdict.
- The REQ file is updated by the director's scribe, not by these tasks.

## Acceptance criteria and the tests that prove them

| REQ-0033 criterion | Proof |
|---|---|
| An `idea-fable` format exists in Scriptorium and a story can be ordered through `add_story` with a concept card in the brief | SCP-71 tests (`tests/fable.test.ts` 1, 3, 4) and the three live `add_story` calls of 2.3 |
| Three published stories, 1,500-2,000 words within the format's gate, each with debrief, sources, 3 quiz questions and Go deeper | K1-K5, K8 per pilot, recorded in the run logs; SCP-71 `tests/fable.test.ts` 2 and the `tests/lengths.test.ts` case for the mechanism |
| No paid spend for the three books | K7 per pilot, `budget.md` spend summary unchanged, with `daily_cap_usd: 0` as the hard stop |
| The user has read the three stories | 2.6, the verdict in each run log |

Code tests run in the Scriptorium repo (PowerShell, from `C:\projects\Personal\scriptorium`):
`fnm env --use-on-cd | Out-String | Invoke-Expression; npx vitest run tests/fable.test.ts tests/lengths.test.ts`, then `yarn test`,
`yarn typecheck`, `yarn lint`, `yarn build`; fallback `fnm exec --using default cmd /c "<command>"`. The production has no automated
test: its proof is the checks K1-K9.

## Risks / alternatives

- **Config-only (research option A) instead of the code route**: rejected in SCP-71 (prompt conflict "no summary", humanizer over
  the quiz, back matter counted by the gate, no quiz check).
- **Starting Scriptorium resumes work**: guarded by `paused: true` before the start and `only:` per pilot; the budget cap is the
  hard stop for money. Both are global: no other book should run during the pilots (none is open today).
- **ACP cloud models have usage limits** (subscriptions behind the proxy): a limited model is set aside until its reset; the map
  gives each role two models, and 2.3 step 4 swaps a stuck one. The run may take hours; that is fine.
- **`noLocalFallback: true` and embeddings**: the flag forbids on-device chat models outside the book's list; the embeddings
  (`acp/llama/nomic-embed-text-v1.5`) are configured separately in `roles.md` and are not a role. If the engine treats them as
  forbidden for the book (not seen in the code), the memory index warns but the short book does not need search; log it. The
  alternative (flag off) lets the shared fallback start Strata on the GPU at $0.
- **Humanizer on Claude instead of DeepSeek**: the live humanizer default is paid DeepSeek (refused by the cap). Claude through ACP
  is untested as humanizer; the guards keep the original if a pass is bad (K9 records it).
- **Fact binding is partly manual**: the engine checks `[n]` ranges; K3 traces each claim by hand.
- **Wikipedia in pilot sources**: allowed only where no primary or institutional source opens (decision 4); primary sources are
  used where they open; each key fact still resting on Wikipedia is marked in the run log "needs a better source before anything
  is public".
- **The originality checker and the real books**: `FABLE_REVIEW_NOTE` tells reviewers the Go deeper list is not imitation; if a
  pilot is still rejected for it, the one retry applies and the note is tuned in a follow-up SCP ticket.
- **The factory is left paused** (decision 3): the 7 open ideas do not start at the next Scriptorium start; the restored cap
  (20) applies once the user unpauses. The run log records that `paused` differs from the before-state.

## Decisions (user, 2026-11-24)

1. Models: the role map in 2.2 is approved as written.
2. Story seeds and titles: approved as written.
3. After the pilots: leave the factory paused (`paused: true`, no `only:`); `daily_cap_usd` is restored to 20.
4. Sources: Wikipedia allowed for the pilots where no primary source opens; such facts are marked "needs a better source before anything is public".
