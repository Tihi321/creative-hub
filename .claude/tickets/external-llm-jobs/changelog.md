# Changelog: Claude Code does the model work

## 2026-10-20 (later): live verification after the merge

**Outcome:** the user merged all three PRs. All three apps were built from `master` and restarted, and each one ran a real job end to end with Claude Code answering every model call. All three work.

**Setup**
- `yarn build` (Scriptorium) and `yarn build:engine` (VN Studio, Book Translator) all exited 0.
- A `client` provider entry was added to `~/Scriptorium`, `~/VisualNovels` and `~/BookTranslator` `config/providers.md`: local, concurrency 8, model `claude-code` with `vision: true` and `context: 200000`. Backups are in `.claude/temp/providers-backup/`.
- Scriptorium was idle, with no running jobs, when it was restarted.
- `hub.ps1 check`: scriptorium 33 tools, vn-studio 66, book-translator 26. `list_models` shows `client/claude-code` in each app.

**Book Translator.** Project `the-keeper-hr-cb2b62`, a short English text translated into Croatian, with every agent on `client/claude-code`.
- The tasks came in order: glossary (JSON), translate (`<seg>`), proofread (`<seg>`), QA review (JSON). `wait_for_progress` returned at once each time a task waited.
- A QA answer without `segId` was refused (`issues[0].segId: missing (required)`), and the task stayed leased. The fixed answer was accepted.
- The project reached `done` with 1 of 1 chunks at $0. The export has correct Croatian diacritics, „…” quotes and **bold**.

**VN Studio.** Project `quarter-tone-test`: 2 chapters, 2 characters, 1 place, illustrated art, NES chiptune. Every role was on `client/claude-code` through `vno_update_settings {models}`.
- Claude answered 6 tasks: the art plan in 2 batches (10 assets + the cover), the music plan, staging (one task per chapter) and the run summary.
- The music plan was submitted without the defaulted fields `prompt` and `seconds`, and was accepted. That is the defaults fix working live.
- ComfyUI generated 12 assets in about 29 minutes, the slow part.
- The game built with 0 placeholders and 0 warnings. Ren'Py lint is clean (7 dialogue blocks). 21 jobs done, 0 failed.
- Claude looked at both sheets, one sprite and the cover, and they match the prompts. The game itself was not played.

**Scriptorium.** The rejected book `the-local-patch` was rescued.
- `set_book_model {writer: client/claude-code}`, then `reopen_book {rewrite, [3, 4]}`.
- Claude wrote ch3 (1,256 words) and ch4 (1,899 words) from the rewrite tasks. A rewrite task carries the whole book, every review note and the research (98k characters).
- The DeepSeek reviewers passed it, and it was **published** at 7.14, up from 6.29 rejected. EPUB, cover and reader were made. Round 3 cost about $0.02 (reviews only).

**Found and fixed in the hub (uncommitted)**
- `scripts/hub.ps1`: `call` printed through the console code page, so `š` became `s` and „” became quotes that broke the JSON. It now prints UTF-8. The data stored in the apps was always correct.
- `scripts/hub.ps1`: `stop` killed only the process listening on the port. That is a child of Electron apps such as Scriptorium, so the main process lived on. `stop` now walks up to the top process of the same program and kills its tree. Checked as a dry run against the running Scriptorium (listener 31712 → main 16884 `--headless`).
- The skill: `vno_wait` timeout lowered to 240 s, because Claude Code aborts an MCP call that is silent for 300 s. This was seen live.

**Found, written in ROADMAP.md (not fixed)**
- Every client task sends the prompt twice (`messages` alongside `system`/`user`).
- `set_book_model {model: null}` is refused on a published book.
- A published book can't be reopened.
- Book Translator does not reload `providers.md` while running.
- A client model without `context` defaults to 8,192 tokens.

**Not checked**
- Nobody played the VN, and the user has not read the EPUB.
- Not tried: VN Studio's art-critic image tasks (art review was off), Scriptorium writing from a new story (`add_story {models}`), and parallel subagents taking tasks.

## 2026-10-20: SCP-08, VNO-05, BTT-09

**Outcome:** Scriptorium, VN Studio and Book Translator each have a model provider `client` (model `client/claude-code`). A model request sent to it waits in an in-memory queue until Claude Code takes it over MCP and answers it, and nothing is spent. Each app can choose it per book or per project. Scriptorium can also reopen a rejected book. Everything is uncommitted on ticket branches, and nothing has been tried against the running apps.

### The design shared by all three repos

The new file `src/engine/models/client.ts` holds:
- `ClientTaskQueue`, with `add`, `list`, `lease`, `submit`, `release`, `cancel` and `counts`
- `ClientProvider`
- `checkAgainstSchema`, a built-in JSON-schema check with no new dependency; a field that has a `default` may be left out
- the constants `GONE` and `DEFAULT_LEASE_MS` (30 min)

How tasks behave:
- A task id is `<job>#<call n>`.
- A lease runs out lazily (checked on access), and the task goes back to waiting.
- An abort (stop, model change, pause) drops the task with an `AbortError`, so the job is requeued without counting an attempt.
- Cost is 0, the provider counts as `local`, there is no timeout, and the provider is never marked down.

Wiring:
- The engine (or service) owns one queue and passes it to the registry and the MCP tools.
- `RequestMeta.job` carries the job id.
- Under `model_order`, client refs are sorted first.

### scriptorium, branch `SCP-08_client-provider` (from origin/master 26371be)

24 files changed, plus the new `src/engine/models/client.ts` and the ticket folder.

- **Provider:** `src/shared/schemas.ts` (kind `client`, `vision`, book `extra_rounds` and `role_models`), `models/types.ts`, `models/registry.ts` (builds the client provider, client refs first), `models/router.ts` (`candidates` puts the book model first, before the agent model), `queue/scheduler.ts` (passes the job id, `getBookModel`, `bookModelChanged`, `changeModel` by book), `engine.ts` (owns the queue, caches the book model, `reopenBook` and `setBookModel` commands).
- **Per-book models:**
  - `add_story` and `update_story` take `models`. They are stored as `role_models` in the idea and copied into book.md when the book starts (`store/ideas.ts`, `shared/brief.ts`, `pipeline/handlers.ts`).
  - New tool `set_book_model {book, role, model|null}`. It works on books in progress and rejected ones, and refuses published and failed books.
  - book.md uses `role_models` because `models` already holds the job counts per model.
- **Reopen:** `reopen_book {book, mode: rewrite|review, chapters?}` runs one more round on a rejected book (`pipeline/pipeline.ts`, and `advance.ts` reads `max_rounds + extra_rounds`).
- **MCP** (`mcp/tools.ts`): `list_client_tasks`, `get_client_task`, `submit_client_task`, `release_client_task`, `reopen_book`, `set_book_model`; `factory_status.clientTasks`.
- **UI:** `summary.ts` and `ModelsDialog.tsx` show client as local and free.
- **Docs:** `docs/mcp.md` gains a "Do the model work yourself" section. `docs/design.md` gains three Decisions rows, a Model layer change and a History entry. `seed/config/providers.md` has a disabled `client` entry.
- **Tests:** `models`, `scheduler`, `mcp`, `pipeline`, `features` and `helpers` (12 new tests in the first round, 6 in the second).

### visual-novels-orchestrator, branch `VNO-05_client-provider` (from origin/master c67409b)

27 files changed, plus the new `src/engine/models/client.ts`, `src/engine/mcp/tools-client.ts` and the ticket folder.

- **Provider:** `shared/schemas.ts`, `models/types.ts`, `models/registry.ts`, `models/router.ts` (project model first), `queue/scheduler.ts` (job id, `projectModel` hook), `engine.ts` (queue to the registry, the MCP controller and stdio).
- **Per-project models:** `shared/vn.ts` (settings `models`); `vn/service.ts` (`updateSettings` checks the role and the ref; `null` clears it); `vn/project.ts` (models cache).
- **MCP:** `tools-client.ts` adds `vno_client_tasks`, `vno_get_task` (art-critic images as MCP image content), `vno_submit_task` and `vno_release_task`. In `tools.ts`, `callTool` can return image blocks, `vno_status` and `vno_wait` gain `clientTasks`, and `vno_update_settings` takes `models`.
- **`waitIdle`** (`vn/service.ts`): it returns when running jobs are only waiting on the client, with `clientTasks` and a hint. `vncli.ts` exits 1 with a message in that case.
- **UI:** `ModelsPage.tsx` shows client as local and free.
- **Docs:** `docs/mcp-guide.md` gains "Do the model work yourself", covering the roles, batching (30/10/25), per-project models and the draw loop being out of scope. Also updated: the tools table, the `INSTRUCTIONS` in `server.ts`, the README, and a commented example in `seed/config/providers.md`.
- **Tests:** `models`, `scheduler`, `mcp-http`, `vn-handlers` (the art plan and staging answered through the queue give the same files as the mock), plus the helpers.

### book-translator, branch `BTT-09_client-provider` (from origin/master 4364b0d)

12 files changed, plus the new `src/engine/models/client.ts`, `tests/client.test.ts` and the ticket folder.

- **Provider:** `shared/schemas.ts`, `models/types.ts`, `models/registry.ts` (`setClientQueue`, because the registry is built before the service), `service.ts` (owns the queue), `pipeline/runner.ts` (job id `<project>--<unit>--<task>`).
- **MCP:**
  - `server.ts` adds four tools: `list_client_tasks`, `get_client_task`, `submit_client_task` and `release_client_task`.
  - `wait_for_progress` returns at once when a task waits; it polls the queue every 500 ms, because a new task sends no event.
  - `get_project` shows `clientTasks`.
  - A new prompt, `translate_with_full_pipeline`, and the third mode in INSTRUCTIONS.
  - Supporting changes in `dispatcher.ts` and `shared/protocol.ts`.
- **CLI:** `cli.ts` `translate` exits 2 when an agent model is a client model.
- **Docs:** README has the client provider section, the YAML to add by hand, and the corrected claim that QA and the proofreader could run later. `seed/config/providers.md` has a disabled entry.
- **Tests:** `tests/client.test.ts` (8, including a whole project with every agent on client) and the tool and prompt lists in `tests/mcp.test.ts`.

### creative-hub (master, uncommitted)

- `.claude/skills/make-visual-novel/SKILL.md`:
  - New section "Doing the model work yourself": setup, per-book and per-project choice, roles, the loop table for the three apps, rules for answering, and `reopen_book`.
  - Step 0.5 asks who does the model work.
  - The `wait-book` line mentions `reopen_book`.
- `ROADMAP.md`: the Scriptorium, VN Studio and Book Translator gaps are marked done on their branches. New gaps: a pin is not exclusive; existing data folders need the provider added by hand; the VN draw loop times out with client; a parked job holds its agent; no-op model jobs still wait for a model slot.
- `README.md`: the LLM line and a short paragraph on the client provider.
- `runs/the-local-patch.md`: the rejected book, the reasons, and that it is on hold.

### Deviations from the plan

- **Book Translator added mid-run** at the user's request (2026-10-20).
- **Per-book and per-project models added** (Scriptorium `role_models` / `set_book_model` / `add_story {models}`, VN Studio settings `models`). The review found that an `assign_agent` pin is not exclusive: other writers take the book's jobs after about 20 s while the client agent waits.
- **book.md field named `role_models`**, not `models`, which was already taken.
- **No `set_model` MCP tool in VN Studio.** The global choice stays in `config/roles.md`; per-project `models` covers the use case.
- **Schema check:** not switched to `io: 'input'`, because OpenAI strict `json_schema` needs every key required. The check skips defaulted keys instead.
- **Book Translator's `wait_for_progress` polls** every 500 ms.

### Verification

- **Final run by the orchestrator** after every change (Node 24 via fnm):

  | Repo | `yarn test` | `yarn typecheck` | `yarn lint` |
  |---|---|---|---|
  | scriptorium | 20 files, 300 tests passed | ok | ok |
  | visual-novels-orchestrator | 45 files, 557 tests passed | ok | ok |
  | book-translator | 22 files, 241 tests passed | ok | ok |

- **One Scriptorium test failed once** while the three suites ran in parallel (299/300). It passed in two more runs, one of them under the same load. It was not reproduced, and which test it was is not known.
- **Not run:**
  - No live run against the running apps (each needs a build and restart; Scriptorium's restart resumes the factory; this session's Book Translator MCP has the 401).
  - The UI changes were not looked at in a window.
  - No end-to-end book, VN or translation was made with Claude answering.

### Follow-ups

1. Live check per app: `hub.ps1 build <id>`, restart (ask before Scriptorium), add the `client` provider to `~/Scriptorium`, `~/VisualNovels` and `~/BookTranslator` `config/providers.md`, reconnect, then do a small run in each.
2. Rescue `the-local-patch`: `set_book_model {writer: client/claude-code}`, then `reopen_book {mode: rewrite, chapters: [3, 4]}`.
3. Commit and open PRs per repo when the user asks.
4. ROADMAP gaps: the VN draw loop with client, parked jobs holding their agent, no-op model jobs waiting for a slot.

**Commit status:** uncommitted in all four repos.
