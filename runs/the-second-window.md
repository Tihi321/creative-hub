# The Second Window

Started 2026-11-24. Idea fable from *The Book of Elon* (card `subtraction-neglect`). Ticket HUB-45, request REQ-0033, plan `.claude/tickets/HUB-45-idea-fable-pilots/plan.md`. Pilot 1 of 3 (the others: `runs/the-plain-title-page.md`, `runs/the-clock-on-the-hill.md`).

## Brief

- Idea / theme: Subtraction neglect (question the requirement, delete the step), from *The Book of Elon* (Eric Jorgenson). Story "The Second Window", byline Taleidea Stories.
- Kind: linear (idea fable, one chapter, 1,500-2,000 words) · adults
- Languages: en
- Art: off · Music: off · Voices: off

### Frozen card (verbatim, as sent in `add_story`; frozen 2026-11-24 after the source check)

Common fields: `format: "idea-fable"`, `byline: "Taleidea Stories"`, `genre: "literary fiction"`, `noLocalFallback: true`, `models` map of plan 2.2. Pilot fields (title, premise, plot, characters, setting, style) as in plan 2.2 Pilot 1, unchanged.

`sections`:

**Concept card**
```
Idea: Subtraction neglect
Definition: When people try to improve something, they reach for adding parts and rarely think of removing them, even when removing is better.
Mechanism: Adding ideas come to mind quickly; removing ideas take more effort and are often not thought of at all, more so when people are busy. The habit that helps is asking of every part, rule or step who asked for it and what happens if it is gone, and checking why it exists before cutting it.
Misconception: Simplifying means cutting as much as possible. Deleting without knowing why a part is there is its own failure.
Rules: No real person or company. Do not retell or reword any engineering 'algorithm' or step list from the books. No app or brand names.
```

**Key facts**
```
1. In eight experiments, people asked to improve something found changes that remove parts less often than changes that add them (Adams, Converse, Hales and Klotz, Nature, 2021).
2. They overlooked removing even more when the task did not prompt them to consider it, when they were under a higher mental load, and when they had only one chance, rather than several, to notice that adding had limits.
3. The research team tested whether people reject removing ideas or overlook them altogether, and focused on the second: removing ideas take more mental effort, and people who move fast settle for the first adding idea that comes to mind.
4. Chesterton's fence (G. K. Chesterton, The Thing, 1929, chapter "The Drift from Domesticity"): a reformer who sees no use for a fence across a road should find out why it was built before taking it away.
5. In the Toyota Production System, Taiichi Ohno categorized seven major kinds of waste found in mass production, among them overproduction, waiting and unneeded processing.
```

**Sources**
```
1. Adams, Converse, Hales and Klotz, "People systematically overlook subtractive changes", Nature 592, 258-261 (2021), via https://sites.olemiss.edu/scilab/publications/people-systematically-overlook-subtractive-changes
2. Same study, via https://sites.olemiss.edu/scilab/publications/people-systematically-overlook-subtractive-changes
3. ScienceDaily, 7 April 2021, https://sciencedaily.com/releases/2021/04/210407135801.htm
4. https://en.wikipedia.org/wiki/Wikipedia:Chesterton%27s_fence
5. Lean Enterprise Institute, "7 Wastes", https://www.lean.org/lexicon-terms/seven-wastes/
```

**Go deeper**
```
*The Book of Elon*, Eric Jorgenson
*Subtract: The Untapped Science of Less*, Leidy Klotz (2021)
```

### Wikipedia marks (beside the card, not inside it)

- Key fact 4 (Chesterton's fence) rests on Wikipedia only: needs a better source before anything is public. (chesterton.org returned 403 to the fetcher; Gutenberg text of *The Thing* not found; the G._K._Chesterton article did not show the passage, so the Wikipedia fence page is used.)
- Key facts 1, 2, 3, 5 rest on non-Wikipedia sources (Ole Miss lab page, ScienceDaily, Lean Enterprise Institute).

### Source check (2026-11-24, WebFetch)

- 1, 2: Ole Miss page opens; abstract: "Across eight experiments", less likely to identify subtractive changes "when the task did not (versus did) cue them", "under a higher (versus lower) cognitive load", "only one opportunity (versus several) to recognize the shortcomings of an additive search strategy".
- 3: ScienceDaily opens; the team "focused on the latter" (overlook altogether, not discard); "subtractive ideas require more cognitive effort"; fast movers accept additive solutions. Plan draft said "usually not thought of at all, rather than thought of and rejected": softened to what the page says.
- 5: draft cited Wikipedia "Muda"; that page opens and supports it, but the Lean Enterprise Institute page (opens) states Ohno's seven wastes directly, so the fact now uses it and no longer says "muda". Unneeded processing = LEI "Processing: doing unneeded or incorrect work".
- Concept card: "often not thought of at all" is a little stronger than the sources (the study did not directly test it); the card is left as drafted. Noted for the director.

## Ids

| Tool | Id |
|---|---|
| Scriptorium story | (after `add_story`) |
| Scriptorium book | |
| Book Translator project | n/a |
| VN Studio project | n/a |

## Log

- 2026-11-24 pre-flight steps 1-5 done by the pre-flight worker (record below). No `add_story` yet; waiting for the user's go (plan 2.0 step 6).

## Pre-flight record (steps 1-4, 2026-11-24)

1. **SCP-71 build.** `C:/projects/Personal/scriptorium` is on branch `SCP-71_idea-fable`; the SCP-71 changes are in the working tree, uncommitted (modified: ROADMAP.md, docs/design.md, docs/mcp.md, seed/config/formats.md, src/engine/pipeline/{advance,books,handlers,humanizerHandlers,prompts}.ts, src/engine/store/{dataFolder,migrations,seedHistory}.ts, src/renderer/store/bookTypes.ts, src/shared/schemas.ts, tests/{lengths,puzzles}.test.ts; added: seed/prompts/writer/{draft,rewrite}_chapter_fable.md, src/engine/pipeline/fable.ts, tests/fable.test.ts; untracked: `.claude/tickets/SCP-71-idea-fable/`). Checker PASS recorded by the director (re-check 3 PASS, 2026-11-24; assumed, not re-run). `pwsh -File scripts\hub.ps1 build scriptorium`: exit 0, ends with "built in 6.20s" (renderer out/ written).
2. **Engine down.** `hub.ps1 status`: scriptorium down (7341). Others: book-translator, vn-studio, edu-studio, cartoon-studio, pixel-studio, chiptune-studio, comfyui, comfy-mcp, lmstudio, strata, flow-music-mcp down; vibetts up (7723, pid 14328); acp-proxy down. `C:/Users/Infplane/Scriptorium/index/engine.lock` does not exist.
3. **What the factory would resume (read only).**
   - Ideas with `status: open` (7): `peak-of-whispers`, `signal-lost`, `the-glass-horizon`, `the-gravity-garden`, `the-iron-tide`, `the-last-lighthouse-keeper`, `the-rust-runner`. All other idea files are `status: used`.
   - Books whose `book.md` stage is not published/rejected: none (every book is `published`).
   - Files in `jobs/queued/`: none.
   - Before-values (frontmatter): `config/factory.md`: `paused: false` (line 3); no `only:` line. `config/budget.md`: `monthly_cap_usd: 40`, `daily_cap_usd: 20`, `per_book_cap_usd: null`.
4. **ACP proxy.** `acp-proxy` is DOWN (8787), so `/v1/models` was not queried and nothing was started. Instead checked `config/providers.md` (the `acp` provider rows): `codex/gpt-6-luna` (line 21), `codex/gpt-5.6-terra` (line 19), `claude/claude-sonnet-5` (line 32), `antigravity/gemini-4-hydrogen` (line 29): all four present. The proxy must be started before the pilots (`start scriptorium` starts it as a requirement), then re-check `/v1/models`.

## Production record (HUB-45 production worker, 2026-11-25)

User's go given 2026-11-25 ("Go").

### 2.1 Guards and start
- Scriptorium repo `git status --short` before (saved in `.claude/temp/HUB-45-prod/scp-status-before.txt`): branch `SCP-71_idea-fable`; M ROADMAP.md docs/design.md docs/mcp.md seed/config/formats.md src/engine/pipeline/{advance,books,handlers,humanizerHandlers,prompts}.ts src/engine/store/{dataFolder,migrations,seedHistory}.ts src/renderer/store/bookTypes.ts src/shared/schemas.ts tests/{lengths,puzzles}.test.ts; A seed/prompts/writer/{draft,rewrite}_chapter_fable.md src/engine/pipeline/fable.ts tests/fable.test.ts; ?? .claude/tickets/SCP-71-idea-fable/.
- Before: factory.md line 3 `paused: false`, no `only:`; budget.md `daily_cap_usd: 20` (monthly 40, per_book null). After edit: `paused: true`, `daily_cap_usd: 0`.
- `hub.ps1 start scriptorium -Force`: acp-proxy started (pid 30868), scriptorium up (pid 1836, 7341).
- `/v1/models` lists codex/gpt-6-luna, codex/gpt-5.6-terra, claude/claude-sonnet-5, antigravity/gemini-4-hydrogen: all four, no model replaced.
- Disk: `config/formats.md` has `id: idea-fable` (1 match); `prompts/writer/draft_chapter_fable.md` exists.
- `factory_status`: paused true, only null, running [], 42 books all published, spend today 0, month 0.010392, dailyCap 0.
- Decision by the director: in the Concept card Mechanism line, "are often not thought of at all" is replaced by "are often overlooked" (the rest unchanged). The text sent is therefore: "Adding ideas come to mind quickly; removing ideas take more effort and are often overlooked, more so when people are busy. ..." (the frozen card above keeps the old words; this line wins).

### 2.3 Run (2026-11-25)
- `add_story` -> story slug `the-second-window`, file `ideas/the-second-window.md` (slug as planned, no suffix). Book slug `the-second-window`.
- `set_factory_only {the-second-window}` ok (factory.md `only:` written); `set_factory_paused {false}`; one `wait_for_book` (900 s): returned `published` after 242 s. `set_factory_paused {true}` straight after. No retry used.
- factory_status after: spend today 0, month 0.010392 (unchanged from before the start). Side note: `limitedModels` shows codex (`gpt-6-luna`, `gpt-5.6-luna`, `gpt-5.6-terra`) set aside until 2026-11-29T10:07Z (Codex usage limit); the book finished on the other models of its map; `modelDeviations` empty.
- Stage published, score 8.33, `words` 1578, `lengthGate` {status ok, words 1611} (gate-time count, before humanizer; information only). Published 2026-11-25T07:50:58Z.
- Book log `log.md`: no `fable back matter:` line.
- Paths: reader `C:\Users\Infplane\Scriptorium\books\the-second-window\out\reader` (index.html, chapter-01.xhtml); EPUB `C:\Users\Infplane\Scriptorium\books\the-second-window\out\the-second-window.epub` (174,932 bytes); cover.png done.
- Models used (made.md): editor-in-chief, architect, writer, humanizer, publisher = acp/claude/claude-sonnet-5; developmental-editor, line-editor, beta-reader, copy-editor, originality-checker = acp/antigravity/gemini-4-hydrogen (codex rows were set aside by the usage limit). Cost 0 on every row.

### 2.4 Checks
- K1 PASS: story words 1578 (chapter front matter `words: 1578`; manual recount of text before `## What just happened`, front matter stripped, `wc -w` = 1578). lengthGate.words 1611 (info).
- K2 PASS: `## What just happened` has `**The idea.**`, `**Where it showed up.**`, `**How to use it tomorrow.**` and `**Sources**` with the 5 frozen Sources lines verbatim; no second Sources / Go deeper block.
- K3 PASS with two notes. Table (debrief sentence -> [n] -> key fact):

| Debrief sentence | [n] | Key fact | Verdict |
|---|---|---|---|
| The idea 1: first instinct is to add (window, app, rule); hardly anyone asks whether removing would work better | [1] | 1 | ok |
| The idea 2: people reached for additions far more often than removals, especially when busy, not prompted, one chance | [2] | 2 | ok ("far more often" is stronger than "less often" in KF1; note) |
| The idea 3: not because removing is judged bad; it takes more effort to think of, rushed mind settles for first adding idea | [3] | 3 | ok |
| The idea 4: before you remove a part find out why it is there; a fence across a road was usually built for a reason | [4] | 4 | ok ("usually" is the writer's) |
| The idea 5: some steps still do a job, "the way a factory floor has real waste to cut but also real work that must stay" | [5] | 5 (only: Ohno listed seven wastes) | weak: "real work that must stay" is not in KF5; a truism hung on [5]; flagged, not treated as a fail |
| Where it showed up: Ines and Tomas reach for a second window and app; Ines drops stamp, carbon, signature under pressure; traces each step, keeps the boarding tally for lifeboats | none | story only | all moments are in the story |
| Answer 1: additive changes found far more than subtractive | [1] | 1 | ok |
| Answer 2: removing ideas take more effort to notice; busy mind settles for first adding idea | [3] | 3 | ok |
| Answer 3: find out why it was built; may still be protecting someone, as Ines kept the tally | [4] | 4 | ok |

- K4 PASS: 3 questions, A-D each; `### Answers` 1. B, 2. A, 3. B; read against story and card, exactly one option is right in each (Q1 B; Q2 A; Q3 B).
- K5 PASS: `## Go deeper` = the 2 frozen lines; disclaimer once, word for word, last paragraph (grep count 1); no extra block.
- K6 PASS: story part has none of Musk, Jorgenson, Klotz, Chesterton, Ohno, Toyota, Adams, Tesla, SpaceX (grep on text before `## What just happened`); invented names only. (The cover blurb in log.md names Chesterton's fence; blurb not story.)
- K7 PASS: 11 made.md rows, all cost_usd 0 and acp/...; spend today 0.00 unchanged; modelDeviations [].
- K8 PASS: `get_book.author` "Taleidea Stories"; chapter-01.xhtml contains `<h3>What just happened`, `<h3>Quiz`, `<h4>Answers`, `<h3>Go deeper` and the disclaimer; EPUB exists.
- K9 PASS: `humanizer_result: rewritten`.
- Wikipedia marks: key fact 4 (Chesterton's fence) still rests on Wikipedia only: needs a better source before anything is public.
- Retries used: 0.

### 2.5 Restore (2026-11-25, about 09:45, after pilot 3)
- Engine stopped (down, lock removed); acp-proxy still up (pid 30868). factory.md `paused: true`, no `only:`; budget.md `daily_cap_usd: 20`. Scriptorium repo git status identical to the "before" list above. Details and the pilot-2 leftovers: `runs/the-clock-on-the-hill.md` (2.5).
- Pilot 1 was written while codex was set aside (usage limit until 2026-11-29 11:07 local); all rows acp, cost 0.

## Checked

- what was looked at or played, by whom

## Left to do

- The user's go (plan 2.0 step 6), then plan 2.1-2.5.

## Text fixes after the check (2026-11-25)

- Before (chapters/ch-01.md, `**The idea.**`): "...a fence across a road was usually built for a reason [4], and not every part is dead weight — some steps genuinely still do a job, the way a factory floor has real waste to cut but also real work that must stay [5]."
- After: "...a fence across a road was usually built for a reason [4], and it helps to name what counts as waste before cutting: in the Toyota Production System, Taiichi Ohno categorized seven kinds of waste in mass production, among them overproduction, waiting and unneeded processing [5]." ([5] now says what key fact 5 says.)
- Front matter `words` stays 1578 (the change is in the back matter). `book.md` `length_gate.words: 1611` untouched.
- Outputs rebuilt without the engine: throwaway script `.claude/temp/HUB-45-fix/rebuild.mts` calling Scriptorium's own `BookStore.buildEpubFile` (EPUB, then `out/reader/`) with tsx; no service started, no model called. Backups in `.claude/temp/HUB-45-fix/backup/`. EPUB file list identical to the backup.

## Audio (REQ-0035, 2026-11-25)

- Voice: bf_emma (Emma, British English, female), engine Kokoro (VibeTTS, local, $0).
- Narration scope: title, "a Taleidea story", the story, then "What just happened" and the debrief paragraphs. Quiz, Sources, Go deeper and the disclaimer left out; no front matter, markdown marks or citation marks. Narration text: .claude/temp/REQ-0035-audio/the-second-window.txt
- Words narrated: 1914
- MP3: C:/Users/Infplane/Scriptorium/books/the-second-window/out/audio/the-second-window.mp3
- Size: 4602775 bytes. Duration: 575 s (9:35) (ffprobe).
- Not verified: nobody has listened to it.

## Sources and audio update (HUB-47, 2026-11-26)

- Debrief sentence [1]: "When something is slow or broken, people's first instinct is almost always to add something - a window, an app, a rule - and hardly anyone stops to ask whether taking something away would work better" -> "When something is slow or broken, people tend to default to searching for things to add (a window, an app, a rule) and so overlook the option of taking something away"
- [2]: "Studies that gave people a thing to fix found they reached for additions far more often than removals, especially when they were busy, hadn't been prompted ..., or only had one chance to notice the problem" -> "Across eight experiments, people were less likely to spot helpful removals when the task did not prompt them to consider removing, when they had only one chance to see that adding falls short, or when they were under heavier mental load"
- [3]: "This isn't because people think removing is a bad idea ... so a rushed mind settles for the first thing it can add" -> "The researchers' account is that people overlook removing rather than reject it: removing ideas take more mental effort to come to mind, so people moving fast settle for the first adding idea"
- [4], [5]: wording kept (source swapped for [4]: Chesterton, The Thing, 1929; [5] Lean Enterprise Institute kept).
- Quiz 1 option B and answer 1: "far more often" -> "more often".
- Sources applied: 1 Adams et al., Nature 592 (2021), doi 10.1038/s41586-021-03380-y; 2 same study; 3 McManamay, UVA Engineering, April 2021; 4 Chesterton, The Thing (1929), archive.org scan; 5 Lean Enterprise Institute, 7 Wastes. Full list as in `.claude/tickets/HUB-47-filters-fable-and-audiobooks/sources.md`.
- Rebuild evidence: outputs rebuilt without the engine (throwaway `.claude/temp/HUB-47-pilots/rebuild.mts`, `BookStore.buildEpubFile`, tsx; no service touched, no MCP call). It rewrites `out/<slug>.epub` and `out/reader/` only; `out/audio/` was checked afterwards and is intact. The new sentence and a new source are present in both `out/reader/chapter-01.xhtml` and the EPUB's `OEBPS/chapter-01.xhtml`. Checks: story part identical to the backup (diff before `## What just happened`), Go deeper and disclaimer identical, [1]-[5] in the debrief match Sources 1-5, quiz still 3 questions. Backup: `.claude/temp/HUB-47-pilots/backup/<slug>-ch-01.md`.
- New audio: DONE (2026-11-26). Voice bf_emma (Kokoro); speed 1.0 for title and story, 0.87 for the debrief (speed had effect with a `path` input); pauses 1.5 s after the title and 2 s before the debrief; durations: title 3.1 s, story 467.7 s (202 wpm), debrief 112.9 s (170 wpm), total 587.3 s; path `books/the-second-window/out/audio/the-second-window.mp3` (+ one-line `the-second-window.m3u`), 44.1 kHz mono 128 kbps. Not verified: nobody has listened.
- Not verified: nobody has listened.
