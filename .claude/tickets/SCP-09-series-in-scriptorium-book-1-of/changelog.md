# Changelog: SCP-09

## 2026-10-20: Series in Scriptorium, hub windowed start, book 1 published

Scriptorium can now group books into a series that continue each other. The hub can start Electron apps with their window. Book 1 of *The Hartley & Varga Mysteries*, "The Clockless God", was written through the client provider and published.

### scriptorium: branch `SCP-09_series` (from origin/master dd7ea80), commit 33c224b, not pushed or merged

- **Series store.** `src/engine/store/series.ts` (new) keeps `series/<slug>.md` files with frontmatter `kind, title, genre, format, books, created` and a brief body. It handles create, update, addBook and list, and gives the order-gate helpers `bookRefs`, `waitingStories` and `nextSeriesIndex`.
- **Series prompts.** `src/engine/pipeline/series.ts` (new) provides:
  - `seriesSection`: the series premise, cast, setting and style, plus each earlier book's title, stage, blurb, act and chapter summaries, the cast's end state from its bible, and its open threads, capped at about 7k characters per book and 28k in total;
  - `withSeriesBible`: carries the bible over to a later book;
  - `earlierSeriesBooks`.
- **Schemas.** `src/shared/schemas.ts` and `src/shared/brief.ts`: ideas, books and briefs have optional `series` and `series_index`.
- **Pipeline.**
  - `src/engine/pipeline/handlers.ts`:
    - `pickNext` skips a series story while an earlier book of its series is not published, or an earlier story is still open;
    - `start_book` copies the series fields into the book and adds the book to the series;
    - the series section is added to the pitch, outline, draft, rewrite, review and check prompts;
    - the outline handler seeds the bible from the earlier books.
  - `longHandlers.ts` and `pipeline.ts` follow these changes.
- **Draft context.** `src/engine/memory/context.ts`: the draft context of a long book adds RAG passages from the earlier books of its series.
- **MCP.** `src/engine/mcp/tools.ts` adds `list_series`, `get_series`, `add_series` and `update_series`, and a `series` parameter on `add_story` and `update_story`.
- **Engine.** `src/engine/engine.ts`, `summary.ts`, `store/ideas.ts`, `store/dataFolder.ts` and `store/watcher.ts`:
  - series commands and `series.updated` events;
  - series in the snapshot;
  - `series/` in the data layout and in the folder watcher;
  - `series_index` numbered automatically.
- **UI.**
  - `src/shared/protocol.ts`, `src/renderer/store/store.ts`, `renderer/demo/fake.ts`: the protocol, reducer and demo engine handle series.
  - `ui/Series.tsx` (new) is a panel in the Library with the books in order, a New series form, Edit, and Next book.
  - `ui/StoryForm.tsx` has a Series select, and `ui/SideTools.tsx` and `ui/Library.tsx` are wired to them. `styles.css` styles the panel.
- **Docs.** `docs/design.md` has a Decisions row, the UI row, the folder layout, the Later list and History. `docs/mcp.md` covers the series tools.
- **Tests.**
  - `tests/series.test.ts` (new, 11 tests) and `tests/renderer/series.spec.ts` (new);
  - `tests/mcp.test.ts` has the tool list and a series flow;
  - `tests/renderer/store.test.ts` is updated.

### creative-hub: branch `SCP-09_series-hub` (from origin/master 9c4d547)

- `scripts/hub.ps1`: a `-Window` switch. An Electron service drops `--headless` and `--mcp-only`, adds `--mcp`, and starts without `WindowStyle Hidden`. Other kinds print a note. (commit 4c474a4)
- `README.md`: the `-Window` usage, and series in the Scriptorium row. (4c474a4)
- `.claude/skills/make-visual-novel/SKILL.md`: a Series bullet in step 1A. (4c474a4)
- `ROADMAP.md`:
  - the Series item marked done, with notes from the live use;
  - new Scriptorium items: `add_story {models}` does not reach `start_book`; check notes reach the writer as a summary only; an odd word target in check rewrites;
  - the `-Window` live result: the window and MCP work, but the start command hangs. (uncommitted)
- `runs/the-clockless-god.md`: the run log of the production. (uncommitted)

### Deviations from the plan

- The plan's parallel chapter agents were not used for drafting. Scriptorium's long-book pipeline drafts one chapter at a time (draft, check, archivist, then the next), so Claude wrote the chapters itself, in order, in one voice.
- Subagents were used for the round 1 rewrite: four agents revised 11 chapters in parallel from one fix list.
- The editor-in-chief's start job ran on a free model, not the client, because `add_story {models}` does not reach `start_book`. It is in the ROADMAP.
- The factory's 7 generated ideas were left alone after the user chose "only our book". Their topics were already inactive, so nothing else started.
- The ch12 check rewrite was submitted once with the old text by mistake (a script error). The fixed text went in with the round 1 rewrite.

### Verification

- **Run:**
  - Scriptorium: `yarn typecheck`, `yarn lint` and `yarn build` pass. `yarn test` gives 312 passing, with a timing flake that also occurs on master: 3 failures in 10 runs there, 1 in 17 on the branch, all hook timeouts in other tests. `yarn test:ui` passes 3/3.
  - The hub: the parser check on `hub.ps1` reports 0 errors, and the status command runs.
- **Run live:**
  - `hub.ps1 start scriptorium -Force -Window` opened the window, and `hub.ps1 check scriptorium` reported OK with 37 tools.
  - `add_series`, `add_story {series, models}`, the series section in the pitch, outline and chapter prompts, and `get_series` with the published book all worked.
  - The book went through 18 drafts, chapter checks, three act reviews, a full review, and one rewrite round, and was published at 7.73.
- **Not run:**
  - `yarn test:electron` and `test:packaged`;
  - the Series panel seen in the real window;
  - book 2 of a series run live (the gate and the bible carry-over in the real factory);
  - the user reading the book.

### Follow-ups

- The user reads and rates the book.
- Merge both branches when the user is happy.
- Find out why `hub.ps1 start -Window` hangs its caller.
- The ROADMAP items above.

### Commit status

- scriptorium 33c224b and hub 4c474a4 are committed locally, not pushed.
- The hub ROADMAP, run log and this ticket are committed after 4c474a4 on the same branch.
