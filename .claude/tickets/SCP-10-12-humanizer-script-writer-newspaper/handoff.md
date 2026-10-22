# Handoff: SCP-10/11/12 + BTT-10 + Croatian translation (2026-10-21)

The plan is `plan.md` in this folder; its Status section is at the bottom. The run logs are `runs/the-clockless-god.md` (book 1 and the Croatian edition). The VN, test-book and article runs get their own `runs/` logs when they start.

## What the user asked (2026-10-20)

1. A script writer panel that adapts books to visual novels.
2. A newspaper section that writes articles the way books are written.
3. A humanizer role, so books and articles do not read as AI-written.
4. Translate *The Clockless God* to Croatian with Book Translator, with Claude Code doing the model work and no outside models.

Decisions:
- The newspaper writes real, researched articles.
- The humanizer runs on every book and article, on the line editor's model chain.
- The script writer asks linear or choices for each book.
- Live runs: the humanizer on a short test book, one test article, and adapting *The Clockless God* to a VN.

## State of each repo (all committed, nothing pushed)

| Repo | Branch | Commit | State |
|---|---|---|---|
| scriptorium | `SCP-10_humanizer` | 89910c2 (from master 1e51cd9) | Done. 335 tests, test:ui, typecheck, lint and the build pass. |
| scriptorium | `SCP-11_script-writer` | f5a2e49 (on SCP-10) | Done. 348 tests, test:ui 4/4, typecheck, lint and the build pass. |
| scriptorium | `SCP-12_newspaper` (checked out) | 902564d (on SCP-11) | **WIP.** The code (plan items 1-9) is in; see "Next" below. |
| book-translator | `BTT-10_client-only` (checked out) | 323e16c (from master 89e837f) | Done. 247 tests, typecheck, lint, build:engine and build pass. |
| creative-hub | `SCP-10-12_hub` | the commit with this handoff | Ticket, run log, ROADMAP fixes and the Croatian EPUB. |

The Scriptorium branches are stacked and must be merged in order: SCP-10, then SCP-11, then SCP-12 (or merge SCP-12, which contains all three). BTT-10 and the hub branch are independent.

## Done

- **Humanizer (SCP-10).**
  - Role `humanizer`, with starter agent Iris Vane.
  - Job `humanize--chNN--rN`: for long books after the continuity fix and before the memory update; for short books after the length gate; again after each rewrite round.
  - Guards: ±10% length, research markers, `[n]` citations, VN script structure.
  - A format flag `humanize`, and a book override `humanize: false`.
  - A migration in `src/engine/store/migrations.ts` adds the role and agent to existing data folders.
- **Script writer (SCP-11).**
  - `adapt_book {book, format, title?, notes?, models?}` and an "Adapt to visual novel" panel (`ui/ScriptWriter.tsx`) on published books.
  - `source_book` on the idea and the book; the adaptation waits until its source is published.
  - `adapt.ts` gives the source digest to the pitch and outline, the mapped source chapters (`source_chapters` in outline.md) to drafts and rewrites, and the adaptation note to reviews.
  - The bible is seeded from the source. Research is skipped.
- **BTT-10.** `clientOnly: true` on `create_project` / `update_project_settings` puts all four agents on `client/claude-code` and refuses any other model ref.
- **Croatian translation.**
  - Project `the-clockless-god-hr-2945aa`: all 62 chunks done, $0, every task answered by Claude subagents (glossary, about 170 translate/proofread/QA tasks, and a final edit pass with `edit_chunk`).
  - Exported to `runs/the-clockless-god/the-clockless-god.hr.epub`: "Bezsatni bog", about 44k words.
  - The working briefs are in `.claude/temp/hr/` (`TRANSLATOR.md`, `EDITOR.md`, `bt.sh`).

## Next (in order)

1. **Finish SCP-12** on `SCP-12_newspaper`, with one implementer:
   - Update two stale seed assertions for the 2 new article formats and the 8 Newspaper topic rows:
     - `tests/nonfiction.test.ts`, "the formats, the gate and the prompt variants are in the seed";
     - `tests/pipeline.test.ts`, "the seed list has 250 to 500 rows..." (482 vs 483).
   - Re-run `tests/adapt.test.ts`, `humanizer.test.ts` and `series.test.ts` after the `start_book` fix.
   - Write the docs:
     - `docs/design.md`: Decisions row, sections, folder layout, History;
     - `docs/mcp.md`: `list_articles`, `medium`, article `add_story`.
   - Then a clean full `yarn test` (known timing flakes in scheduler/features/pipeline/recovery: rerun and compare), `yarn test:ui`, `yarn build`. Commit as `SCP-12: ...` (not WIP).
   - Deviations to record in the changelog:
     - references are built from the fact base `sources()`;
     - article pitches skip the similarity check;
     - `office/scene.ts` library-door click fix;
     - old data folders keep their `generate_ideas.md`, and the handler appends the headlines.
2. **Rebuild and restart Scriptorium** on the SCP-12 build: `hub.ps1 build scriptorium`, then `hub.ps1 start scriptorium -Force -Window`.
   - Don't pipe the start command's output in Bash (`| tail`): the engine inherits the pipe and the call never returns. Redirect it to a file instead.
   - The migrations add the humanizer, the article formats and the Newspaper topics to `~/Scriptorium`. Check `config/roles.md`, `agents/`, `config/formats.md` and `topics.md` after the start.
   - Reconnect `/mcp`, or use `hub.ps1 call`.
3. **Live runs** (plan Part E). Write the books through the client loop with `.claude/temp/ct.sh` and `next.sh` (book slug inside them: adapt them for each run):
   - **E2:** a short-story test book (`add_story {format: short-story, models: {writer: client/claude-code}}`). Check the `humanize--ch..` job, then compare `chapters/history/ch-NN-r0*.md` with the humanized chapter and record the tic counts before and after.
   - **E3:** one article (`add_story {format: article, topic: news-technology}`; switch the topic on or pass it directly). Claude writes; the app models research, humanize and review. Check `out/article.html` in the Newspaper tab. Tavily news search costs a little.
   - **E4:** adapt *The Clockless God*: `adapt_book {book: "the-clockless-god", format: <ask the user: visual-novel or choice-visual-novel>, models: {architect, writer: client/claude-code}}`. Claude writes the ~25k-word script. When published, `vn-studio vno_import` as a check. Log it in `runs/the-clockless-god-vn.md`.
4. **Finish:**
   - Write `changelog.md` in this folder.
   - Tick the plan Status lines E2-E4.
   - Update the ROADMAP with anything found.
   - Update the hub skill step 1 with "adapt an existing book" and the newspaper; update the README Scriptorium row.
   - Commit the hub branch.

## Live services right now

- Scriptorium is down (its window was closed). It still has the pre-SCP-10 build in `out/` until rebuilt.
- Book Translator is up on 47811, started by the hub with the master build from before BTT-10. Restart it after `hub.ps1 build book-translator` to get `clientOnly`.
- LM Studio is down. The app models for reviews (DeepSeek through OpenRouter, plus LM Studio) are needed for the live runs.

## Open questions for the user

- Visual-novel adaptation: linear or with choices?
- They should read the Croatian EPUB and rate book 1 (`rate_book`).
- Known slip in the English book 1, ch17: Dec raises "the hand that was not holding the pistol" after an officer has already taken it. It is fixed in Croatian. The English book is published and cannot be reopened (a ROADMAP item).
