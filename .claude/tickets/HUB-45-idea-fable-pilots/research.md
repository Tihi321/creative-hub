# HUB-45 research: what Scriptorium needs to write an "idea fable"

Researched 2026-11-24, read-only. Scriptorium repo: `C:/projects/Personal/scriptorium` (master, clean; verified). Live data folder: `C:/Users/Infplane/Scriptorium` (`~/Scriptorium`). Nothing was started, built or run.

Marks: **C** = confirmed (read at the path:line given), **I** = inferred (reason given).

## Question

What does Scriptorium need so it can write one "idea fable" (a 1,500-2,000 word one-chapter English fiction story, humanized, in which a character lives through one non-fiction idea, then a sourced "What just happened" debrief, 3 multiple-choice quiz questions with explanations and a "Go deeper" list of 2-3 books with a fixed disclaimer), fed by a concept card in the brief?

## Answer

1. **The story part is config-only; the debrief, quiz and book list as machine-checked extras are not.** A new fiction format is one entry in `seed/config/formats.md` plus a hand-added copy in the live `~/Scriptorium/config/formats.md`. No code switches on a format id for pipeline behaviour (C: the only code mentions of `idea-blink` and `kids-picture-book` are a UI badge table, `src/renderer/store/bookTypes.ts:32-44`, and the picture-book migration list, `src/engine/store/migrations.ts:178`). Behaviour switches on flags (`nonfiction`, `script`, `picture_book`, `article`, `long`, `humanize`, `research`), and a plain fiction format with none of them uses the plain `draft_chapter.md` prompt (`handlers.ts:1417-1420`).
2. **Nothing in the pipeline produces extra non-story sections for fiction.** References/sources exist only for `nonfiction: true` books (`books.ts:394-399`) and the fact-checker needs the non-fiction fact base. The debrief/quiz/books therefore must be written by the writer inside the one chapter (guidance only), or by a code change (new flag + `_fable` prompts, about 6 files; section "What the plan needs").
3. **Concept card in the brief needs no code change.** `add_story {sections:[{heading,text}]}` becomes `## <heading>` blocks that reach the architect, the writer (every draft and rewrite), the humanizer and the reviewers through `storyBriefSection` (`handlers.ts:1524-1528`, `brief.ts:119-137`).
4. **ACP-only per book has no single switch.** `add_story {models}` per role puts ACP models first, but the role lists and `fallback_shared: true` (live) still put paid DeepSeek behind them. The only hard stop is the budget: ACP models are `local: true`, hence never budgeted, while paid models are refused when a cap is reached, so `daily_cap_usd: 0` (global, hot-reloaded) blocks every paid call.
5. **Starting Scriptorium resumes everything open.** No pause flag on `hub.ps1 start`, but `paused: true` in `~/Scriptorium/config/factory.md` before the start, or `only: <slug>` / `--only`, keeps the other 7 open ideas from starting.
6. Next free numbers: hub **HUB-45** (confirmed free), Scriptorium **SCP-71** (last is SCP-70).

## Path through the code

### Q1 Formats: where they live and what keys exist

- **Definition file:** `C:/projects/Personal/scriptorium/seed/config/formats.md` (465 lines; YAML frontmatter list `formats:` lines 3-441, docs below). Schema: `formatEntrySchema`, `src/shared/schemas.ts:194-270`. It is a `looseObject`, so unknown keys are tolerated (C).
- **Seeding rule:** `initDataFolder` copies the seed into the data folder but never overwrites an existing file (`COPYFILE_EXCL`, `src/engine/store/dataFolder.ts:87-93`). So an existing `~/Scriptorium/config/formats.md` does **not** get a new seed format by itself. Formats added after data folders existed get a one-off append migration: `appendSeedFormats` + `migratePictureBooks` (`migrations.ts:144-190`), registered at `dataFolder.ts:110-121`. C.
- **Live copy:** `~/Scriptorium/config/formats.md` exists, has all 24 seed ids including `idea-blink` (line 251) and `kids-picture-book` (line 416, moved to the end by the migration) and differs in small ways from the seed (the live bedtime entries have no `research: false` line, which the code treats as false for `bedtime-*` anyway, `advance.ts:17-19`). **Consequence: the new format must be added to the live file by hand (or by a new migration), in addition to the seed.** Config changes apply while running (inferred from `roles.md` text "applies at once" and the file watcher `store/watcher.ts`; not run).
- **Keys that exist** (`schemas.ts:194-270`): `id`, `name`, `enabled`, `kinds`, `juvenile`, `age_band`, `words [min,max]`, `chapters [min,max]` (default [1,1]), `read_aloud`, `long`, `research_prep`, `research` (optional bool), `nonfiction`, `script`, `screenplay`, `puzzles`, `picture_book`, `runtime`, `choices`, `humanize` (default true), `article`, `max_rounds`, `reviewers`, `guidance`. There is **no** "fiction" flag: fiction is simply `nonfiction:false, script:false`. There is no per-format "fact-check" key: the fact-checker enters through `nonfiction` (`advance.ts:10`) or by naming it in `reviewers`.
- **`idea-blink` in full** (seed lines 276-298, identical in live):

```yaml
  - id: idea-blink
    name: Ideas explainer (short read)
    enabled: true
    nonfiction: true
    humanize: true
    max_rounds: 1
    kinds: [nonfiction]
    juvenile: false
    age_band: null
    words: [2000, 4000]
    chapters: [6, 10]
    read_aloud: false
    guidance: |
      A short-read explainer on a philosophical idea for curious general readers, in the style of a book-summary app. Each chapter is one
      "blink" of 250 to 500 words that carries one key idea. Open the first blink with a hook: a vivid scene, a small story, a thought
      experiment or a puzzle the reader can feel. Every blink explains one idea or argument in plain, concrete words, defines each term when
      it first appears, names the thinker who made the argument and when, uses an everyday example or a thought experiment, and ends with a
      line that pulls into the next. Give the strongest objection to the idea its fair hearing. The last blink is a short takeaway: the whole
      argument in a few sentences, and what it can mean for an ordinary life. Where thinkers disagree or the question is still open, say so
      plainly, and keep what a thinker actually argued apart from the writer's own view. Every fact comes from the sourced notes and carries
      the number of its source in square brackets, like [2]. Never state a date, name or quote that the notes do not give, and put no words
      in a thinker's mouth that the notes do not give. No invented people; a clearly imagined scene or thought experiment that illustrates
      an idea is allowed if the text frames it as imagined.
```

  `idea-blink` is **non-fiction** (6-10 chapters of 250-500 words, sourced `[n]`). It is the wrong base for a fable. It does show how a topic of kind `nonfiction` is picked; a story that fixes the format does not need a topic.

- **`kids-picture-book` in full** (seed lines 217-239): `script: true`, `picture_book: true`, `kinds: [juvenile-visual-novel]`, `juvenile: true`, `age_band: "3-6"`, `words: [150, 900]`, `chapters: [1, 1]`, `read_aloud: true`, `research: false`, plus a long page-wise `guidance` (read it at `seed/config/formats.md:229-239`). It is a script format, so it is not the template for prose.
- **Closest short single-piece prose fiction format: `bedtime-story`** (seed lines 19-31):

```yaml
  - id: bedtime-story
    name: Bedtime story
    enabled: true
    kinds: [juvenile-fiction]
    juvenile: true
    age_band: "3-6"
    words: [600, 2000]
    chapters: [1, 1]
    read_aloud: true
    research: false
    guidance: |
      A calm read-aloud story for a child of three to six. ...
```

  Use it as the shape: `chapters: [1, 1]`, `research: false`, no `nonfiction`/`script`. Its `juvenile`/`read_aloud` keys add the child-safety and read-aloud reviewers (`advance.ts:11-12`), which a fable for adults would not want (set both false). Other single-chapter formats: `article`, `feature-article` (non-fiction, article pipeline).
- **Code that switches on format flags, relevant to a fiction fable** (all C):
  - `variant()` picks the prompt suffix: article, then `_nf`, `_sp`, `_pb`, `_vn`, else plain (`handlers.ts:1417-1420`). A new fable prompt family needs a new line here.
  - `formatsForKind(formats, null)` returns every enabled format except article/screenplay/puzzles/picture_book (`handlers.ts:157-160`). **So a new fiction format with no exclusion flag can be picked at random by the editor-in-chief for any story or topic with no topic, and a topic of a matching `kinds` value would pick it.** Mitigation in config: give it an unused kind (e.g. `kinds: [idea-fable]`) and fix the format in every `add_story`; a story that fixes `format` still finds it in `allowed` when it has no topic (`handlers.ts:531, 546-547`). For a hard guarantee, copy the `picture_book` pattern (a flag excluded in `formatsForKind` and handled at `handlers.ts:539`): code.
  - `reviewersFor` default set for fiction: continuity-checker, developmental-editor, line-editor, copy-editor, beta-reader, originality-checker (+ child-safety if `juvenile`, + read-aloud if `read_aloud`) (`advance.ts:6-14`). `must_pass` in `config/quality.md:4` is `[child-safety-reviewer, originality-checker, fact-checker]`.
  - `needsResearch(format)`: `format.research ?? !id.startsWith('bedtime-')` (`advance.ts:17-19`). Without `research: false` the architect makes a `research_plan` job (`advance.ts:344-346`) and, for a fiction format, may start web research.
  - Drafting prompt: `draft_chapter` (plain) for fiction. Writer is told it may add `[RESEARCH: ...]` markers, at most three, which become researcher jobs (`seed/prompts/writer/draft_chapter.md` last paragraph; `advance.ts:200-209`, `MAX_MARKERS_PER_CHAPTER = 3` `handlers.ts:268`). Say in the guidance "no research markers" to avoid it (I).
  - UI badge: `bookTypes.ts:30-44` lists seed ids; an unknown id falls to a regex (`bookTypes.ts:47-62`) and shows its raw id as the badge. Cosmetic, no failure (C).

### Q2 Length gate and a 1,500-2,000 word single chapter

- Gate for a short book (`advance.ts:394-411`), runs once, only at `r === 0`, before the humanizer and the reviews: `out = total < min*0.85 || total > max*1.15 || (target && (total < target*0.8 || total > target*1.2))` (`advance.ts:399`, `TARGET_BAND = 0.2` at `:257`). Out of range: stage `length-fix`, one `rewrite_chapter` job per chapter with a note to rewrite to the chapter's share; then `length_gate.status: done` (`:401-410`). One pass only, no loop. **C.**
- `target_words` is chosen at `start_book`: the editor-in-chief returns `target_words` (optional), clamped to the format's `words`, default the middle (`handlers.ts:583`), stored in book.md (`:617`). `start_book` always calls the editor-in-chief model for a fresh story (the "direct" shortcut is only for adaptations, `:553`) so the `editor-in-chief` role needs a model. C.
- Words are counted over **all chapter text** (`totalWords`), so the debrief, quiz and book list count. If the story is 1,500-2,000 words and the debrief block adds roughly 300-500, the whole chapter is about 1,800-2,500 words. Set `words` for the whole chapter, for example `[1800, 2600]` (gate window 1,530-2,990, target about 2,200, target band 1,760-2,640), or the gate will rewrite a correct draft once. Inferred sizing; the arithmetic is from `advance.ts:399`.
- Per-chapter tighten: a chapter over `TRIM_ABOVE = 1.2` of its target gets one extra "cut to target" request (`handlers.ts:255`, used by `tighten`, `:382`). With one chapter the target is the whole `target_words` (`perChapterTarget`, `handlers.ts:261-262`). A chapter 20% over target is cut, and the cut could remove debrief material. C for the rule, I for the effect.
- **1-chapter fiction passes**: `chapters: [1,1]` is exercised by `bedtime-story` and `kids-picture-book`; the outline handler only refuses fewer chapters than `chapters[0]` and truncates above `chapters[1]` (`handlers.ts:773-793`); the outline prompt says "If the number of chapters is 1, give one chapter that holds the whole story" (`seed/prompts/architect/outline.md`). No minimum chapter count anywhere else; `splitActs` only matters for `long`. The pitch has a 300-word limit with one tighten retry (`handlers.ts:250-251`), unrelated to length. C.

### Q3 Brief input over MCP (`add_story`, port 7341)

- Tool definition: `src/engine/mcp/tools.ts:562-618`. Parameters (all optional, but a title or some text is required): `title`, `premise`, `plot`, `characters[]`, `setting`, `style`, `sections[{heading,text}]`, `format`, `topic`, `genre`, `series`, `humanize`, `noLocalFallback`, `puzzles`, `byline`, `models` (role -> `provider/model` or ordered list). Returns `{slug, file, story}`. Docs `docs/mcp.md:86`. C.
- Brief shape and rendering: `src/shared/brief.ts` (`StoryBrief` 24-52, `renderBrief` 119-137): `## Premise`, `## Plot`, `## Characters` (`### Name`, `Role: ...`), `## Setting`, `## Style`, then every extra section as `## <heading>` verbatim; "Any other heading is passed to the agents as it is" (`docs/mcp.md:200`). No length limit ("There are no length limits anywhere", `brief.ts` header).
- Delivery: the story is `ideas/<slug>.md`; at book start it is copied to `books/<slug>/brief.md` (`handlers.ts:627-631`). `storyBriefSection` (`handlers.ts:1524-1528`) appends "## The owner's story brief" + the whole brief to the outline (`:732`), the chapter draft (`:924`), the rewrite (`:1225`), the humanizer (`humanizerHandlers.ts:378`) and long-book prompts. It tells the agents to "keep its title, characters, plot points and setting". The editor-in-chief also gets the brief (`:550`). Reviewers get the brief through the same section (inferred from the shared helper; I did not trace each reviewer).
- **Answer: a concept card passes as sections with no code change**, e.g. `sections: [{heading:"Concept card", text:"Name: ...\nDefinition: ...\nMechanism: ...\nMisconception: ...\nKey facts:\n1. ... [source]\n..."}, {heading:"Books for Go deeper", text:"..."}]`. Put the debrief/quiz/disclaimer instructions in `guidance` (per format, fixed) and the per-idea content in sections. Caveat: the brief section tells the agents to build the story around "its plot points"; give a `premise` and a `plot` that name the character and the lived situation, and use the card sections only as facts.
- Fiction has no fact base, so `[n]` source numbers are not validated in a fiction format, and the humanizer prompt only tells the model to keep `[n]` (the engine check `citations(original) !== citations(revised)` runs only for `nonfiction`, `humanizerHandlers.ts:337`). A debrief cited as plain text ("Source: Author, Title, year") is safer than `[n]`.

### Q4 Debrief, quiz, book list: any existing mechanism?

Nothing in the fiction path adds extra sections. Searched `src/engine/publish/*` (`epub.ts`, `sections.ts`, `xhtml.ts`, `reader.ts`) and `books.ts`, grep for references/appendix/afterword/colophon:

- References: `BookStore.references()` returns null unless `book.data.nonfiction === true` (`books.ts:394-399`), and then builds from the fact base (`buildReferences(this, new FactBase(this), slug)`). Used by the EPUB and reader (`books.ts:436, 527`). C.
- Articles have their own References section (`publish/article.ts:73-121`) but also need the fact base.
- `sections.ts` is gamebook section numbering, unrelated (C, `sections.ts:1-20`).
- The EPUB/reader render prose with `markdownToXhtml`: `## Heading` on its own line becomes `<h3>` (level = hashes + 1), `---` a scene break, `> ` a blockquote, `**bold**` and `*italic*`. **No lists** (a `- item` line becomes `<p>- item</p>`, joined with `<br/>`) (`xhtml.ts:203-224`). So a debrief written in the chapter body as headed paragraphs renders properly; write the quiz as numbered paragraphs ("1. Question ...<br>A) ...") not markdown lists, or accept `<br/>` line breaks. C for the renderer; the quiz layout advice is inferred.
- **Fact-checker on a non-fiction format:** role `fact-checker` runs task `fact_check` (`advance.ts:22`, `nonfiction.ts:193-310`): it reads the **whole book text**, the fact base digest and numbered research notes, flags unsourced/contradicted claims (prompt `seed/prompts/fact-checker/fact_check.md`), and a non-pass sends the chapters back; it is must-pass (`quality.md` `must_pass`). It cannot be applied to only the debrief: it always checks the whole book, and a fiction story has no fact base, so the coverage check marks the whole chapter "unsourced" (`nonfiction.ts:230-243`). Naming `fact-checker` in a fiction format's `reviewers` is possible (the role is generic) but it would fail every time. I did not run it; the failure is read from the code. I.
- **Humanizer and the debrief:** `humanize_chapter.md` rewrites the whole chapter, bans "a summary of what was learned" endings and "closing summary", and compares numbers/names with the original (`humanizerHandlers.ts:337-393`, prompt text). With one chapter holding story + debrief the humanizer will pass over the debrief too. A refused pass keeps the original (`seed/config/roles.md` humanizer note). Real risk: it softens or reorders the quiz or drops the disclaimer. Options: `humanize: false` for the book (`add_story {humanize:false}`), or a fable-specific humanizer prompt. The humanizer is applied after the length gate, before reviews, once per chapter (`advance.ts:447-451`).
- **Prompt conflict (config-only route):** the plain `draft_chapter.md` ends "Write only the text of the chapter, as plain prose in paragraphs. Do not write a title or chapter heading, notes, or a summary." That conflicts with a `guidance` that asks for headed debrief, quiz and list. The guidance sits above that instruction, so a model may obey the later line. The dev editor, beta reader and line editor read the whole chapter and may call the debrief a tacked-on summary (I; reviewers are generic fiction prompts). `max_rounds: 1` limits damage.

**Options to produce the extras:**

- **A. Config only (guidance holds the layout).** One chapter = story, then `## What just happened`, `## Quiz`, `## Go deeper` and the fixed disclaimer line, all inside chapter 1. No code change; the format entry in seed + live. Risks above (prompt conflict, humanizer, reviewers, length). Smallest. Quality of the debrief's citations is unchecked by any engine step.
- **B. Debrief as a second chapter (`chapters: [2, 2]`), config only.** The outline has two chapters, but all drafting prompts are per format, not per chapter, so chapter 2 is written by the same fiction `draft_chapter` prompt, and `perChapterTarget` splits the target evenly (`handlers.ts:261`), so each chapter is told about half the words. The humanizer and the reviewers still apply to chapter 2. Gains nothing over A except separate chapter files; costs an even word split. Not recommended.
- **C. Small code change (recommended if A's pilot shows the conflict).** A format flag (for example `fable: true`) with:
  1. `src/shared/schemas.ts` (flag next to `picture_book`, `:244`);
  2. `src/engine/pipeline/handlers.ts` `variant()` (`:1417-1420`: add `fmt.fable ? ${task}_fable`) and its type signature; `formatsForKind` exclusion (`:157-160`) and the "only a story that fixes the format" override (`:539`) so it is never picked at random;
  3. `src/engine/pipeline/prompts.ts` fallback regex (`:30`: add `fable`) so roles without a `_fable` prompt use the plain one;
  4. new prompts `seed/prompts/writer/draft_chapter_fable.md` and `rewrite_chapter_fable.md` (and optionally `humanizer/humanize_chapter_fable.md`, `developmental-editor/review_fable.md`) that describe the story-then-debrief layout and tell the writer not to summarize the story into the debrief; `yarn seed:hashes` (CLAUDE.md rule) regenerates `src/engine/store/seedHistory.ts`;
  5. a migration appending the seed entry to existing data folders (`src/engine/store/migrations.ts` + `dataFolder.ts:114`, the `migratePictureBooks` pattern), plus `bookTypes.ts` badge (cosmetic);
  6. tests (see Q10) and docs lines (`seed/config/formats.md` flag docs, `docs/mcp.md`, `docs/design.md` Decisions row).
  Reference implementation to copy: SCP-46 picture books, file table in `scriptorium/.claude/tickets/SCP-46-picture-books/plan.md`.
- **D. A real post-story step** (a separate job after the story that writes the debrief, fact-checks only it and appends it as a back-matter section, excluded from humanizing and from the length gate). Not present; would touch `advance.ts` (new stage and job), `pipeline.ts` (state), a new handler in `handlers.ts` or a new file, `books.ts` (`references`-style section in EPUB/reader/PDF `epub.ts`, `reader.ts`, `pdf.ts`), the schema and prompts. Large; not needed for pilots (I).

### Q5 Prompts

- `seed/prompts/_rules.md` (C, 14 lines) is added to every request: English only, original work, "Reply with the requested output only", child-suitable content for the age band. It does not forbid sections or lists.
- Writer prompts: `seed/prompts/writer/` = `draft_chapter.md`, `_article`, `_nf`, `_pb`, `_sp`, `_vn`, plus `rewrite_chapter*.md`, `research_fix.md`, `research_prep*.md` (the live folder matches). A plain fiction format (`bedtime-story`, `short-story`) uses **`writer/draft_chapter.md`** and **`writer/rewrite_chapter.md`** (`variant()` returns the bare task). Variables: `{{chapter_n}} {{chapter_count}} {{title}} {{format_name}} {{age_band}} {{target_words}} {{chapter_words}} {{guidance}} {{story_so_far}} {{chapter_title}} {{chapter_summary}}` (draft prompt, read).
- Where a `draft_fable` prompt would go: `seed/prompts/writer/draft_chapter_fable.md` (task name `draft_chapter_fable`, frontmatter `kind: prompt`, `role: writer`, `task: draft_chapter`, as the `_pb` file does, `seed/prompts/writer/draft_chapter_pb.md:1-5`); the live copy `~/Scriptorium/prompts/writer/` receives new seed files at the next start (`copyTree`), and `migrateSeedPrompts` upgrades untouched ones (`dataFolder.ts:121`, history `store/seedHistory.ts`). After editing any seed prompt run `yarn seed:hashes` or a test fails (project `CLAUDE.md`). The prompt family needs the `variant()` and `loadPrompt` changes of option C. C for the mechanism.
- Other roles reuse their plain prompts when a `_fable` one is missing, once the regex at `prompts.ts:30` is extended; the fact-checker, researcher and archivist prompts are not variant-selected.

### Q6 Models: ACP only, no paid fallback

- **Role defaults** (seed `seed/config/roles.md:1-37`): writer, architect, editor-in-chief, publisher, idea-generator `[paid, acp]`; developmental/line/copy editors, beta reader `[acp, paid]`; humanizer `[deepseek/deepseek-flash, paid]`; continuity/originality/fact/researcher `[acp/strata/..., paid]`; archivist `[acp/antigravity/gemini-4-hydrogen, acp/strata/..., paid]`. `paid` = first API row of `fallbacks` in `config/settings.md` = `deepseek/deepseek-flash`. Live `settings.md` has `fallback_shared: true` and `fallbacks: [deepseek/deepseek-flash, acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs]` (C, read), so every role also gets the paid row first-to-last. Live `roles.md` is the same lists written as YAML blocks (C).
- **Per-book models:** `add_story {models: {"writer": ["acp/claude/claude-sonnet-5"], ...}}` (`tools.ts:586`, `docs/mcp.md:86`; `set_book_model` for a running book). Order in `Router.candidates`: book models, then the agent's own model, then the role's list (`src/engine/models/router.ts:180-217`). **The role's list (with paid) is still appended**, so this is a preference, not a ban (C). Live ACP rows: `codex/gpt-5.6-luna|terra`, `codex/gpt-6-luna`, `antigravity/gemini-3.8-flash|gemini-4-argon|gemini-4-hydrogen`, `claude/claude-sonnet-5`, plus local `strata/...`, `gufo/...`, `llama/...` (live `providers.md`, read). The role must exist and each ref must be in the registry (`checkRoleModels`). Roles a fable book uses: editor-in-chief, architect, writer, humanizer, developmental-editor, line-editor, copy-editor, beta-reader, originality-checker, continuity-checker, publisher, archivist (plus researcher if research is on).
- **There is no `no_paid_fallback` flag.** `noLocalFallback` / `no_local_fallback` is the opposite (it forbids models on this machine, `router.ts:194`, `tools.ts:580`); do not set it for an ACP-only book that uses `acp/strata/...` or `acp/gufo/...`, because those count as "on device" (`registry.ts:78`, `docs/mcp.md:100`). C.
- **Budget mechanism that does stop paid calls:** `isPaidModel(m) = !m.provider.local && (priceIn>0 || priceOut>0 || priceCachedIn>0)` (`registry.ts:128-131`). The `acp` provider is `local: true` (live `providers.md:10`; seed `providers.md:123`), so ACP models are never reserved or counted (`router.ts:245-253`, `costUsd = paid ? ... : 0`). For a paid model the router calls `budget.reserve(est, book)`, and a refusal skips to the next model (`router.ts:247-257`). `check()` refuses when `day + est > daily_cap_usd` / `month + est > monthly_cap_usd` / `book spend + est > per_book_cap_usd` (`budget/spend.ts:227-245`). So `daily_cap_usd: 0` (or `monthly_cap_usd: 0`) in `~/Scriptorium/config/budget.md` refuses every paid request, for **all** books, and applies without a restart (`seed/config/budget.md` text: "the engine picks them up without a restart"). Live budget: monthly 40, daily 20, `per_book_cap_usd: null`. `per_book_cap_usd` is a single global number applied to each book, not settable per book (C), but `per_book_cap_usd: 0` has the same effect for every book. The job then goes to the next model; if none is left the job fails or waits (I: not run). Paid web search providers (`price_per_request`, `registry.ts` search kind) are another spend route: use `research: false` and no markers (I).
- Recommended combination (option): `models` for every used role set to ACP refs, `research: false`, `humanize` decided separately (the humanizer's own model is a role too), and set `daily_cap_usd: 0` for the duration of the pilot as the hard stop, restored afterwards. The cap change is a live-config edit that needs the user's yes (not a repo change).
- The quality threshold and `must_pass` come from `config/quality.md:2-5`: `threshold 7.0`, `max_rounds 2` (format `max_rounds: 1` overrides), `revise_below 7`.

### Q7 Starting Scriptorium

- `hub.ps1 start scriptorium -Force` (without `-Force` it prints the `warning` of `services.json:17` and skips, `hub.ps1:339-342`). `services.json:5-20` (C): repo `C:\projects\Personal\scriptorium`, data `~\Scriptorium`, lock `index\engine.lock`, port 7341, `start: {kind: electron, args: [".", "--headless"]}`, `requires: ["acp-proxy"]` (started first, `hub.ps1:344-350`), `default: false` (not in the plain `start` set). It needs `out/` built (`hub.ps1` electron branch). `hub.ps1` has no way to pass extra engine arguments: the `args` come from `services.json` only (C: `hub.ps1:355, 364-370`), so `--only` cannot be passed through `hub.ps1`. Requires `pwsh` 7 (`hub.ps1:5`).
- What resumes at start (C, read): `Pipeline.tick` loops every non-terminal book and advances it (`pipeline.ts:430-440`), then if not paused fills ideas (`fillIdeas` only when open ideas < `idea_low_water_mark`) and starts books for open ideas up to `max_books_in_progress` (`pipeline.ts:440-451`); the scheduler runs every queued job whose book is not paused (`scheduler.ts:360-372`). Job ids are deterministic so a restart never duplicates (`advance.ts` header comment). **Live state now (read):** 42 book folders, none in a non-terminal stage (my check printed no non-published/rejected `stage:` line), `jobs/queued` empty, 46 idea files of which **7 have `status: open`** (`peak-of-whispers`, `signal-lost`, `the-glass-horizon`, `the-gravity-garden`, `the-iron-tide`, `the-last-lighthouse-keeper`, `the-rust-runner`), `max_books_in_progress: 5`, `idea_low_water_mark: 5`. So an unguarded start would begin up to 5 of those 7 books, user ideas first, with paid models allowed (`services.json` warning). Not run; read only.
- **Ways to start without resuming other books** (all C from code):
  1. `paused: true` in `~/Scriptorium/config/factory.md` **before** the start (hand edit while the engine is down). While paused: no job launches (`scheduler.ts:360`), no idea fill or book start (`pipeline.ts:440`), but `advanceBook` still plans jobs for open books (no open book exists now). Then over MCP: `add_story`, `set_factory_only {idea: <slug>}`, `set_factory_paused {paused:false}`. Order matters: add the story and set `only` first, then un-pause.
  2. `only: <slug>` in `factory.md` before the start. The slug needs an existing `ideas/<slug>.md` (a hand-written story file is accepted: `docs/mcp.md:157-207`, "You can write one by hand; the engine picks it up"), else the engine warns "no job will run" (`engine.ts:713-723`). With `only` set, other ideas and books are ignored, no idea generation (`pipeline.ts:430-448`, `scheduler.ts` `inScope`). `--only <slug>` on the engine command line (`index.ts:27, 87-94`) would also work but `hub.ps1` cannot pass it.
  3. Combine 1 and 2 for safety. `set_factory_only` and the hand edit are both persisted in `config/factory.md` (`engine.ts:739-753`), so clear them afterwards.
- A second engine on the same data folder is refused by `index/engine.lock` (`docs/mcp.md:255`).
- Config edits to the live data folder (factory, budget, formats) are outside the repos; the project rule is to ask the user before starting Scriptorium (`creative-hub/CLAUDE.md`).

### Q8 Byline

- Per story: `add_story {byline: "Taleidea Stories"}` (`tools.ts:585, 610`) or `update_story` (`:662, 701-704`) while the story is unused; per book later: `set_book_byline` (`tools.ts:902-911`, `engine.ts:937-945`). Stored as `byline:` in the idea frontmatter (`brief.ts:172-173`), copied to `book.md` at `start_book` (`handlers.ts:596, 616`: `idea.byline || settings.byline || ''`). Shown on cover, EPUB `dc:creator`, title page, reader, PDF through `displayAuthor` (`src/shared/byline.ts`: byline, else the writer agent's pen name); the credits line still names the agent (`schemas.ts:429`, `docs/mcp.md:86`). C.
- Pen-name default lives in the live settings only: `~/Scriptorium/config/settings.md:3` `byline: "Mara Kestrel"` (C, read). The seed has `byline: ""` (`seed/config/settings.md:9`). A per-story byline wins over it (`handlers.ts:596`). Not in the hub repo (the hub files mentioning "Kestrel" are only `.claude/director/requests/REQ-0024-...md` and temp JSON).

### Q9 Tickets

- Scriptorium `ROADMAP.md` (102 lines): prose bullets under headings ("Where it stands", "Open: ...", "Models" ...), each item written `**SCP-NN (state, branch ...; plan in .claude/tickets/SCP-NN-<name>/; hub HUB-NN, REQ-NNNN): short title.** Description. Not done: ...`. Branch rule at the top: "Fix items on a ticket branch (`SCP-NN_<what>`) cut from `master`". Ticket plan folder is `.claude/tickets/SCP-NN-<name>/plan.md` (`ls` shows `SCP-70-adapt-test-race` last; branch list shows `SCP-70`, merged). **Next free: SCP-71** (highest folder and highest branch is SCP-70). Recent items SCP-65 to SCP-70 follow the same line format (ROADMAP lines ~96-102). C.
- Hub `ROADMAP.md`: a table `| # | Ticket | What | Code in | Needs | Status |` ("Tasks, in order"), last row `| 37 | HUB-44 | ... |` (line 49), `.claude/tickets/HUB-NN-<name>/plan.md` for each. `ls creative-hub/.claude/tickets` newest = `HUB-44-pending-ideas`; a grep of `HUB-4[4-9]` in ROADMAP.md finds only HUB-44. **HUB-45 is free** (and this folder `HUB-45-idea-fable-pilots` is already the one used). Row 37 text is the template for a new row (what, code in `scriptorium (SCP-71)`, needs, status). C.
- Hub rule: change a tool's code only in its own repo, on a branch named after a ticket in that repo's style, e.g. `SCP-71_idea-fable` (hub `CLAUDE.md`).

### Q10 Tests and how to run them

- Run one file: `npx vitest run <file>` (Scriptorium `CLAUDE.md`); `yarn test` runs vitest then the recovery config (`package.json:16-17`); `yarn typecheck`, `yarn lint`, `yarn seed:hashes` after seed prompt/template edits; `yarn build` (`package.json:11-23`). Node: only through fnm; if `node` is not on PATH use `fnm exec --using default <cmd>` (global rule; the project `CLAUDE.md` says to eval `fnm env`; the SCP-46 plan used `fnm exec --using=24 cmd /c "yarn test"`). Memory note: `fnm exec yarn` fails on this PC, put the fnm default alias dir on PATH. I ran none of them. Do not run the full suite (>700 tests).
- Format config / flags: `tests/pictureBook.test.ts` (13 tests: flag parsing, "is in the seed with the flags and guidance" `:41`, "never picked at random" `:66`, prompt variant `:75`, factory start with a fixed format `:137`, migration `:187-232`), `tests/noResearch.test.ts:46` (`research:false`), `tests/nonfiction.test.ts:365` (a hard-coded list of the six non-fiction format ids: **a new fiction format does not break it, a new non-fiction one would**), `tests/migrations.test.ts`, `tests/dataFolder.test.ts`, `tests/pipeline.test.ts`, `tests/story.test.ts` and `tests/mcp.test.ts` (add_story).
- Length gate: `tests/lengths.test.ts:55-82` (short-book gate incl. 23% over target and a clamped per-chapter share), `:84-128` (long), `:130-155` (tighten), `:213-241` (screenplay runtime), `:288-330` (`length_over`). Use it for a short single-chapter case.
- Pattern for a fable test set (option C): copy `tests/pictureBook.test.ts` structure (seed entry has the flags, never picked by a topic, prompt variant selected, start from a story that fixes the format, migration appends once).

## Reproduction

Not applicable (research, not a bug). Nothing was run or reproduced; every finding is from reading files, plus one `diff` of live vs seed formats/roles and `ls`/`grep` of the live data folder.

## What the plan needs

1. **Decide config-only (A) or flag + prompts (C).** A is enough for a first pilot; C is the clean answer if the prompt conflict (plain draft says "no summary/notes") or the humanizer harms the debrief. The planner should state which in one line (global scope rule).
2. **Format entry** (both `scriptorium/seed/config/formats.md` and live `~/Scriptorium/config/formats.md`): suggested keys `id: idea-fable`, `enabled: true`, `kinds: [idea-fable]` (unused kind, keeps it out of topics), `juvenile: false`, `read_aloud: false`, `age_band: null`, `chapters: [1, 1]`, `words` sized for the whole chapter with the debrief (about `[1800, 2600]`, see Q2), `research: false`, `humanize: true` (or `false` per book), `max_rounds: 1` (the fiction default is 2; a story of this size is cheap but each round is 5-6 reviews), `reviewers: [developmental-editor, line-editor, copy-editor, beta-reader, originality-checker]` (drop the continuity checker for one chapter if wanted; `reviewers` overrides the default set, `advance.ts:8`), and `guidance` holding: the story rules (1,500-2,000 words, one character living through the one idea, the idea never named in the story, the misconception shown), the layout of the three trailing sections, the quiz format (3 questions, options A-D, correct letter, a one-sentence explanation), the fixed disclaimer line verbatim, "no research markers", "cite as plain text, never `[n]`".
3. **Per story call:** `add_story {format:"idea-fable", title, premise, plot, characters, setting, style, sections:[concept card, books], byline:"Taleidea Stories", humanize?, models:{every used role -> ACP ref(s)}}`; then `wait_for_book`. Facts that must reach the writer must be in `sections` (the writer never sees web research with `research:false`).
4. **Live-data steps (need the user's go-ahead):** add the format to `~/Scriptorium/config/formats.md`; set `paused: true` or `only` in `~/Scriptorium/config/factory.md` before the start; `daily_cap_usd: 0` in `budget.md` for an ACP-only run and restore it; start with `scripts\hub.ps1 start scriptorium -Force`; stop it afterwards (`hub.ps1 stop scriptorium`). The hub's `.claude/skills/make-visual-novel` was not read in detail; it is the existing pattern for driving `add_story` + `wait_for_book`.
5. **Hub ticket row** HUB-45 in `creative-hub/ROADMAP.md` (table, row 38), plan in this folder; if code is needed, `SCP-71` on branch `SCP-71_idea-fable` in scriptorium, ROADMAP bullet in the line format above.
6. **Checks the pilots should include:** the finished chapter's word count against the gate (`book.md` `length_gate`, `get_book` `lengthGate`), the debrief block present and intact after the humanizer (compare `chapters/ch-01.md` before and after: `humanizer_result: rewritten|kept` in the chapter front matter), the disclaimer verbatim, the byline on the title page, `modelDeviations` in `get_book` empty (no shared fallback used), spend 0 in `spend/` of the month file.
7. **Quiz/debrief accuracy is unchecked by the engine.** Cited sources in the debrief are only as good as the concept card. If a fact check is wanted, do it outside the engine (director/researcher pass over `chapters/ch-01.md`), or via option D.

## Risks

- Config-only layout vs the plain draft prompt ("no summary", "plain prose"): the model may drop or compress the debrief; the humanizer prompt forbids "a closing summary" and may do the same (Q4).
- A random pick: an enabled fiction format without an exclusion flag is eligible for any no-topic story the editor-in-chief starts (Q1). With only fixed-format stories, and kind `idea-fable` matching no topic, risk is low; the 7 open ideas in the live folder might take it if the factory runs freely (they have their own formats most likely; I did not read them).
- Word-gate surprise: a 1,500-2,000 word format range would rewrite a correct 2,300-word chapter once; the tighten step may cut the debrief (Q2).
- `[RESEARCH: ...]` markers turn into researcher jobs even with `research:false` (markers are processed from the chapter text, `advance.ts:200-209`); in an ACP-only run the researcher's search providers may be priced (Q6).
- ACP-only is not enforced by `models` alone; the paid fallback needs the cap or a roles edit. A budget cap of 0 is global and affects any other book running at the same time (none now).
- Starting Scriptorium with the live folder as it is begins up to 5 of 7 open ideas on paid models (Q7). Must be guarded by `paused`/`only` first.
- Live `formats.md` is a separate copy; seed edits never reach it without a migration or a hand edit, and a migration that rewrites the live file must keep CRLF and the user's own edits (existing `appendSeedFormats` does).
- Seed prompt edits require `yarn seed:hashes` or a test fails; seeds with new hashes upgrade untouched live prompts (`migrateSeedPrompts`), so test with the live prompts folder in mind.
- `tests/nonfiction.test.ts:365` pins the non-fiction format list: if a fable is built as `nonfiction: true` (to get a fact base and references) that test and the `_nf` pipeline change. Not recommended: it would make the story a sourced explainer, research for every chapter, and no fiction prompts.
- The fixed disclaimer line must be agreed word for word; it is not in any file I read.

## Open questions

1. Is the debrief allowed to cite sources as plain text (author, title, year) instead of `[n]`? (the engine only validates `[n]` on non-fiction.)
2. Which ACP refs per role for the pilots (live list above), and whether the humanizer stays on `deepseek/deepseek-flash` (paid) or moves to an ACP model for an all-free run.
3. Should the fable be a separate flag/format (C) from the start, or pilot A first? (Planner decision.)
4. Does the format list need to be hidden from the UI for non-fable users? (Not checked: `bookTypes.ts` badges only; the Models and Library UI were not read.)
5. I did not read the editor-in-chief prompt (`seed/prompts/editor-in-chief/start_book.md`) to see how it treats a fixed format and `target_words`; I did not read each reviewer prompt, so I cannot say which of them will complain about a debrief block (inferred only).
6. Reviewer verdicts and the originality checker on a story whose facts come from a card of real books: not tested.
7. Whether `hub.ps1` should get an `-Only <slug>`/engine-args option (hub ticket scope) instead of hand-editing `factory.md`: it currently has none (`hub.ps1:355-370`).
