# Changelog: SCP-10 to SCP-13, BTT-10

## 2026-10-21: Humanizer, script writer, newspaper, client web search, Claude-only translation

Scriptorium can now:
- humanize every chapter;
- adapt a published book into a visual novel, linear or with choices;
- write researched newspaper articles;
- have Claude Code do its web research.

Book Translator can lock a project to Claude Code. *The Clockless God* was translated into Croatian with no outside models. Live runs published a test story, a test article and the linear VN adaptation.

### scriptorium (stacked branches, committed, not pushed or merged; merge in order)

**`SCP-10_humanizer`, 89910c2 (from master 1e51cd9)**
- New role `humanizer`: starter agent Iris Vane, seed chain, office desk.
- `pipeline/humanizerHandlers.ts`: a `humanize--chNN--rN` job:
  - long books: after the continuity fix;
  - short books: after the length gate;
  - again after each rewrite round.
- Its input: the bible, the end of the previous chapter, and a tic report from `analyzeRepetition` plus checks for machine-prose habits.
- Guards: ±10% length, research markers, `[n]` citations, VN script structure.
- `store/migrations.ts` adds the role and agent to existing data folders.
- `humanize` is a format flag; a book can override it, and the MCP has an option for it.

**`SCP-11_script-writer`, f5a2e49**
- `adapt_book` (MCP), the `adaptBook` command and `ui/ScriptWriter.tsx` ("Adapt to visual novel" on a published book, linear or with choices).
- `source_book` on ideas and books; a story waits until its source is published.
- `pipeline/adapt.ts`:
  - the source digest goes to the pitch and outline;
  - `source_chapters` per outline chapter, and the mapped source chapters go to drafts and rewrites;
  - reviews get the authorised-adaptation note;
  - the bible is seeded from the source;
  - research is skipped;
  - pitch similarity ignores the source;
  - with choices, the source's ending stays one canon path.

**`SCP-12_newspaper`, 902564d (WIP) + d6c57a1 + 465680a**
- Formats `article` and `feature-article` (one chapter, non-fiction, humanized, fact-checked).
- Topic kind `article`, and a `## Newspaper` section of 8 inactive topics.
- `_article` prompts.
- The idea generator gets recent headlines from a news search.
- News-aware research (Tavily `topic: news`, 7 days) and notes kept per article.
- Publishes `out/article.html` and `article.md` instead of a cover and EPUB.
- `max_articles_in_progress`.
- `list_articles` and a `list_books {medium}` filter.
- A Newspaper tab: front page, viewer, write-an-article form.
- Migrations for the formats and topics.
- 465680a: the dark side panel was unreadable and is fixed; on the whiteboard, pitch, research, rewriting and length-fix now go to Idea, Outline and Editing.

**`SCP-13_client-search`, 8a4cea7 + dbff630 + 5c93340**
- Search provider `client-search` (`research/clientSearch.ts`). A query becomes a `searcher/web_search` client task that the MCP client answers with real pages and verbatim excerpts. It times out after `wait_minutes` and the next provider is used. The migration puts it after tavily.
- Humanizer guards: em dashes, numbers, new names. The prompts keep facts and each speaker's register. The seed chain starts with a capable model.
- Late research reaches the fact base: a deterministic `factbase--refresh--rN` before a rewrite or review round (`factbase/merged.md`). The writer's context puts fresh notes first, with their numbers, and the fact-checker reads the same sources.
- 5c93340: fresh facts win the per-chapter cap, "the pages do not state" lines are not facts, and the merge round is recorded.

### book-translator: `BTT-10_client-only`, 323e16c (from master 89e837f)
- `clientOnly: true` on `create_project` / `update_project_settings` puts all four agents on `client/claude-code`. A setting merge cannot undo it, and `makeCall` refuses any other model ref.
- The seed client provider is enabled with a 200k context.

### creative-hub: `SCP-10-12_hub`
- b89d3b5: this ticket, the handoff, the Croatian EPUB `runs/the-clockless-god/the-clockless-god.hr.epub`, and ROADMAP fixes.
- Later (this commit):
  - README and the skill cover adapt, the humanizer, the newspaper and `clientOnly`;
  - run logs `the-clockless-god-vn.md`, `the-lighthouse-that-kept-lists.md`, `france-als162-article.md`;
  - the ROADMAP findings from the live runs.

### Deviations and decisions
- Parts F and G (SCP-13) were not in the first plan. They came from the live runs:
  - the user chose Claude Code research over a Tavily key;
  - the humanizer's live faults;
  - late research not reaching the fact base, and the cap bug.
- The user asked for a second, linear adaptation as well as the choice one.
- `client-search` is the provider id, because `client` was taken.
- The fact-base refresh makes no model call; it uses the note lines as facts.

### Verification
- Scriptorium, per branch: typecheck, lint, the full `yarn test` (390/390 at 5c93340; known timing flakes on master and under load passed when rerun alone), `test:ui` (5/5 at SCP-12/13) and `yarn build` all pass.
- Book Translator: 247 tests, typecheck, lint and both builds pass.
- Live:
  - Croatian translation `the-clockless-god-hr-2945aa`: 62/62 chunks, $0, exported.
  - Test story: published at 9; the humanizer measured.
  - Test article: rejected twice, then published at 7.27 (accuracy 10) after 4 client web searches and the Part G refresh.
  - Linear VN `the-clockless-god-3`: published at 7.5 and imported into VN Studio (9 chapters, 21 characters, 22 places, warnings logged).
  - Choice VN `the-clockless-god-2`: in round 2 at the time of writing.
- **Not run:**
  - the Electron specs (`test:electron`, `test:packaged`);
  - the Part G cap fix live (covered by a regression test built from the live data);
  - VN Studio generation (art, music, build) for either adaptation.
- **For the user:** read the Croatian EPUB, the story, the article and the VN scripts, and check the new panels in the window.

### Follow-ups
- The ROADMAP's Scriptorium section lists them: humanizer fragmenting, researcher notes dropping searched facts, article slugs, news mode for explainers, adaptation place names, choice wording, word targets, reopening published books.
