# Claude Code does the model work (Scriptorium SCP-08, VN Studio VNO-05)

Status: **implemented and verified by tests, 2026-10-20; uncommitted. Live runs still open.** See `changelog.md`.
Written 2026-10-20.

Checklist:
- [x] SCP-08 steps 1-16: 300 tests, typecheck and lint ok. Per-book models were added after the review.
- [x] VNO-05 steps 1-8: 557 tests, typecheck and lint ok.
- [x] BTT-09 steps 1-10: 241 tests, typecheck and lint ok.
- [x] Hub skill, ROADMAP and README.
- [x] Live runs (SCP-08 step 17, VNO-05 step 9, BTT-09 step 11), 2026-10-20 after the merge: all three passed. See changelog.md.
- [x] Commit and PRs. The user merged them. The hub fixes from the live run are uncommitted.
Branches:
- scriptorium `SCP-08_client-provider`, from origin/master 26371be
- visual-novels-orchestrator `VNO-05_client-provider`, from origin/master c67409b

The two repos are worked in parallel against the shared contract below, so the code matches.

## Goal

Let Claude Code, connected over MCP, do the model work in Scriptorium and VN Studio. Today that work can only go to LM Studio, Strata or a paid API. Book Translator already works this way (`get_translation_task` / `submit_translation`).

The trigger is `runs/the-local-patch.md`: the book was rejected after DeepSeek's round-2 rewrite repeated chapter 3 inside chapter 4, and there is no way to give a rejected book another round.

## Done when

1. Scriptorium can route any role or any single agent to a model `client/claude-code`. Its jobs then wait until Claude Code takes them over MCP and answers. The book carries on as if a model had answered, and nothing is spent.
2. Scriptorium has a tool to reopen a rejected book for one more rewrite or review round.
3. VN Studio offers the same for its model steps: analyse, art plan, music plan, stage, voice plan, edition align, art review and summary.
4. The hub skill explains the loop, and `the-local-patch` is finished this way and played/read by the user. That last part is a follow-up run, not part of these tickets.

## How it is meant to work

Both apps share the same model layer: VN Studio's `models/` and `queue/` are a fork of Scriptorium's. Every model call already goes through one point, `JobContext.chat` → `ModelRouter.chat` → `ProviderClient.chat(req)`. A request carries its messages (system + user), an optional JSON `schema`, `maxTokens` and `meta {role, task, book, agent, unit}`.

So the design is **a new provider kind, `client`**. Its `chat()` does not call a model. It puts the request in an in-memory **client task queue** on the engine and waits until an MCP client submits the answer. Everything above it is unchanged: scheduler, router, `chatJson` parsing and repair, and the handlers.

```
job handler → ctx.chat → router → ClientProvider.chat ──park──► ClientTaskQueue
                                                                  ▲        │
                         MCP: get_client_task ────────────────────┘        │
                         MCP: submit_client_task {taskId, text} ──resolve──┘
```

### Client task queue (same in both repos)

- **Task:** `{id, job, call, role, task, book, agent, unit, messages, schema?, maxTokens?, images?, createdAt, leaseUntil?}`. The id is `<job id>#<call n>`. `RequestMeta` gains `job` (the scheduler passes it at the `router.chat` call).
- **States:** waiting → leased (`get` hands it out with a lease, default 30 min) → answered. If a lease runs out, the task goes back to waiting. That lets several Claude sessions or subagents work in parallel, one task each.
- **Abort:** the provider honours `req.signal` (stop, model change, stop now). It drops the task, and a later submit gets "task gone".
- **Restart:** the queue lives in memory. On an engine restart the running job is requeued (attempts + 1, as today), and its new request makes a new task. No timeout: the 15-minute per-request timeout of the HTTP clients does not apply to `client`.
- **Usage:** in/out tokens are estimated (chars / 4) for the logs. The cost is 0. The provider counts as `local`, so it needs no API key, is never "paid" and is never budget-checked.
- **Concurrency:** set in `providers.md`, default 8. That is enough for the scheduler not to stall on `waiting-provider`.

### Provider config

`providers.md` gets:

```yaml
- id: client
  kind: client
  local: true
  concurrency: 8
  models:
    - id: claude-code
      vision: true        # VN Studio art-critic sends images
```

Choose what Claude does with the existing `set_model`:
- per role, e.g. `{role: writer, model: client/claude-code}`
- per agent: `hire_agent` a writer whose model is `client/claude-code`, then `assign_agent` it to one book. **Recommended for single books**, so the factory's own ideas keep using their models and never wait for Claude. Check during implementation that `assign_agent` pins the agent's jobs the way this needs.

### MCP tools

| Scriptorium | VN Studio | What |
|---|---|---|
| `list_client_tasks` | `vno_client_tasks` | Waiting and leased tasks, grouped by book, role and task, plus their ages |
| `get_client_task {role?, book?, task?}` | `vno_get_task {…}` | Leases the oldest matching task. Returns `{taskId, meta, system, user, schema?, maxTokens, output}`, where `output` says "one JSON object matching `schema`" or "prose only, no preamble". It returns `{none: true}` when nothing waits. VN Studio vision tasks add the images as MCP image content. |
| `submit_client_task {taskId, text}` | `vno_submit_task {…}` | When there is a schema, it checks the text and, if it fails, returns `{accepted: false, problems}` with the task still leased, so the client fixes and resubmits instead of `chatJson` spending a repair round. Otherwise it resolves the request. |
| `release_client_task {taskId}` | `vno_release_task {…}` | Gives a task back |

`factory_status` gains `clientTasks: {waiting, leased}`. `vno_status` gains the same.

## SCP-08: Scriptorium (`C:\projects\Personal\scriptorium`)

Branch: `SCP-08_client-provider`, cut from `master`. Ticket folder: `.claude/tickets/SCP-08-client-provider-reopen-book/` (`plan.md` + `changelog.md`, as in SCP-07).

**Provider**
1. `src/shared/schemas.ts:45`: add `client` to the provider kind enum.
2. New `src/engine/models/client.ts`: `ClientTaskQueue` (lease, abort, list) and `ClientProvider implements ProviderClient`.
3. `models/registry.ts`, `setupClient` (261-310): build it for `kind: client`, with no API-key requirement (280-287). Check `isPaidModel`/`groupOf` (86, 467).
4. `models/types.ts`: `RequestMeta.job`. In `queue/scheduler.ts:471`, pass the job id.
5. The engine owns one queue and passes it to the registry and to the MCP tools. The MCP server is stateless per request, so the queue must not live there.

**Tools**

6. In `mcp/tools.ts`, the four tools above, plus `clientTasks` in `factory_status`. Add any new command types to the `Command` union and to `COMMAND_TYPE_SET` (`src/shared/protocol.ts:313-376+`).
7. `summary.ts` `providerSummaries` (136-143) and `ModelsDialog.tsx:41`: show `client` as local and free, so it does not appear as "paid" or "down".

**Reopen a rejected book**

8. New `reopen_book {book, mode: 'rewrite'|'review', chapters?}` tool, backed by a `reopenBook` command and `Pipeline.reopenBook`. It works only on a `rejected` book. It:
   - sets `extra_rounds += 1` in book.md. `maxRoundsOf` (`advance.ts:210`) becomes format/quality `max_rounds` + `extra_rounds`.
   - sets the stage to `rewriting` with round r+1 and `rewrite_chapters` (given, or from the round-r reviews via `chaptersToRewrite`, `advance.ts:140`), or to `reviewing` with round r+1
   - clears the reasons and score, adds 1 back to the topic's in-progress count, emits `book.stage` and kicks the pipeline

   The new round's job ids are new (`--r{r+1}`), so the idempotent enqueue lets them through. It counts toward `max_books_in_progress` again.

**Docs and seed**

9. `docs/mcp.md` (tools list, `retry_book` vs `reopen_book`, a "Do the model work yourself" section).
10. `docs/design.md`: a Decisions row, the Model layer section (153+), the History.
11. `seed/config/providers.md`: the `client` entry (commented or `enabled: false`, so new installs don't route to it).

**Tests** (Vitest)

12. `tests/models.test.ts`: the client provider resolves, leases expire, abort drops the task, and the cost is 0.
13. `tests/scheduler.test.ts`: a job on `client` waits, is answered through the queue and completes; a schema that fails on submit leaves the task leased.
14. `tests/mcp.test.ts`: update the tool-list check (72-81); round-trip get/submit; `reopen_book` refuses non-rejected books.
15. `tests/pipeline.test.ts`: reopen after a forced reject (`:354`) runs round r+1 and publishes or rejects again.

**Checks**

16. Run `yarn test`, `yarn typecheck` and `yarn lint`, with Node through fnm.

**Live**

17. Restart the hub's Scriptorium (ask the user first; the factory resumes). Hire `claude-writer` on `client/claude-code`, add a `bedtime-story` test story and assign the writer to it. Take its tasks over MCP until it publishes. Reviewers stay on their models, which costs cents, or all roles go to `client` for $0.

## VNO-05: VN Studio (`C:\projects\Personal\visual-novels-orchestrator`)

Branch: `VNO-05_client-provider`, cut from `origin/master`. Ticket folder: `.claude/tickets/VNO-05-client-provider/`. Port SCP-08's provider and queue (same files under `src/engine/models/`, kind enum at `schemas.ts:47`, registry 265-314, scheduler `ctx.chat` 456-540), then the VN parts:

1. **Tools** `vno_client_tasks`, `vno_get_task`, `vno_submit_task`, `vno_release_task` in `mcp/tools.ts` (`def(...)`, 75-363). Add MCP image content to `callTool` (366-379) for art-critic tasks, built from the request's `{type: 'image', mime, data}` parts.
2. **`vno_wait` / `svc.waitIdle`** (`service.ts:1259-1298`): return as soon as nothing runs except jobs waiting for the client, with `clientTasks: n`. Otherwise it blocks for its whole timeout. Do the same in `vno_status`.
3. **Batching:** analyse (30 items), art plan (10) and edition align (25) make several tasks in a row from one job. That is fine, because each one goes back into the queue after the previous answer. Note it in the guide.
4. **Out of scope for v1: the Pixel Studio draw loop** (`studios/draw.ts`). It is multi-turn and bounded by `drawTimeoutS` 240. With `client` it would time out, so the guide says: keep `pixel-studio-draw` on a real model, or draw yourself with the pixel-studio MCP and `vno_asset_replace`. Add it to the ROADMAP.
5. **Side fix:** jobs that will not call the model (analyse with 0 items, stage with `byHand` cues) still wait for a model slot (`scheduler.ts:300-336`). With `client` they pass at once, so no change is needed now. Note it in the ROADMAP.
6. **Docs:** `docs/mcp-guide.md` (it is also `vn-studio://guide`), `server.ts` `INSTRUCTIONS`, README (tools, providers), `seed/config/providers.md`, and `ModelsPage.tsx` showing `client`.
7. **Tests:** `tests/models.test.ts`, `scheduler.test.ts`, `mcp-http.test.ts` and `vn-handlers.test.ts`. For handlers: art plan and stage, answered through the queue, give the same files as with the mock.
8. **Checks:** `fnm exec --using=24 cmd /c "yarn test"` (also typecheck and lint).
9. **Live:** `hub.ps1 build vn-studio`, stop and start it, reconnect. Make a two-chapter `vno_create_project`, set every role to `client/claude-code`, run `vno_run_pipeline` and take every task until build and lint pass. Images and music still come from ComfyUI and Chiptune.

## BTT-09: Book Translator (`C:\projects\Personal\book-translator`)

Added by the user on 2026-10-20, during implementation.

Branch: `BTT-09_client-provider`, from master 4364b0d (BTT-08 is merged). Ticket folder: `.claude/tickets/BTT-09-client-provider/` (plan.md + changelog.md, as in BTT-08).

**Why.** The existing `get_translation_task` / `submit_translation` cover only the translator's first pass. The glossary builder, proofreader, QA review/recheck and the QA fix always need a real model. README:105 wrongly says they can run later.

Its `src/engine/models` is a fork of Scriptorium's, with these differences:
- `RequestMeta {role, task, project, unit}`, with no `agent` field
- the router takes an explicit list of refs per agent (`settings.agentModels[agent]`)
- no budget

Every call goes through `ProjectRunner.makeCall` (`runner.ts:311-339`) → `router.complete`.

1. **Provider:** the same `client` kind and `ClientTaskQueue` / `ClientProvider` (`src/engine/models/client.ts`), with the same API.
   - Task meta is `{job, call, role, task, project, unit}`. There is no `book` or `agent`; the role is the agent.
   - The job id is `<project>--<unit>--<task>` and the task id is `<job>#<n>`.
   - Wire it in `registry.setupClient` (249-288; the mock short-circuit at 254-258 is the spot). Add the kind enum entry (`src/shared/schemas.ts:35`).
2. **Ownership:** `EngineService` owns one queue. The MCP server is stateless, a new server per POST.
3. **Tools** in `src/engine/mcp/server.ts` (via the `tool(...)` helper → `Command` union, reply map, `dispatcher.handle`):
   - `list_client_tasks`
   - `get_client_task {role?, project?, task?}`
   - `submit_client_task {taskId, text}`
   - `release_client_task {taskId}`

   Their shapes are the same as in Scriptorium, with `project` in place of `book`. Translator, proofreader and fix tasks are `<seg>` text: the `output` hint says to keep every `<seg id>` and tag. Glossary and QA tasks are JSON with a schema, checked on submit.
4. **`wait_for_progress`:** return at once when a client task is waiting, with `clientTasks: {waiting, leased}`. `get_project` shows the same counts.
5. **CLI `translate`:** refuse with a clear error when any agent model in the project is `client/*`, because nothing would answer it.
6. **Choosing the model:** `update_project_settings` `agentModels {translator|glossary|proofreader|qa: ['client/claude-code']}`. Check that this works over MCP.
7. **Keep** `prepare_chunks` / `get_translation_task` / `submit_translation` / `translate_book_yourself` as they are (the fast first-pass-only path).
8. **Docs:**
   - README: Providers, the MCP section, and fix the line-105 claim
   - `seed/config/providers.md`: kinds list plus a disabled `client` example
   - `server.ts` INSTRUCTIONS, and a second prompt `translate_with_full_pipeline` only if it is simple; update the `tests/mcp.test.ts:104` prompts assertion if one is added
   - Existing data folders do not get new seed entries: document adding the `client` provider to `~/BookTranslator/config/providers.md` by hand
9. **Tests:**
   - registry/router: the client resolves, abort drops the task, cost 0
   - pipeline: a whole project with every agent on `client`, answered by a test loop, reaches done with proofread and QA
   - mcp: the tool list (`mcp.test.ts:97-102`) and a get/submit round-trip
   - `wait_for_progress` returns with `clientTasks`
10. **Checks:** `fnm exec --using=24 cmd /c "yarn test"`, plus typecheck and lint.
11. **Live (orchestrator, later):**
    - `hub.ps1 build book-translator` and a restart
    - fix the session's 401 first: restart Claude Code so it gets `BOOK_TRANSLATOR_MCP_TOKEN`
    - translate a small text with every agent on `client`

## Hub (`creative-hub`)

- `.claude/skills/make-visual-novel/SKILL.md`: a "Do the model work yourself" section covering:
  - which roles to switch, and the per-agent pin for one book
  - the loop: `list_client_tasks` → `get_client_task` → write → `submit_client_task`, until `none`
  - running several subagents in parallel, one task each
  - not leaving roles on `client` once the run is done (the factory would wait forever)
- `ROADMAP.md`: mark the two Scriptorium gaps done when merged, and add the VN draw-loop gap.
- `README.md` table: the new tools. `services.json` and `.mcp.json` don't change.

## Order

SCP-08 first; it is the larger part and the user's book is waiting on it. Then VNO-05, ported from SCP-08's diff (the `replay-ticket` skill fits). Each one goes through the `implement` skill on its own branch, ending in a PR. Nothing is merged without the user.

## Risks

- **Jobs wait forever if no client comes.** A role left on `client` stalls every book that uses it. Mitigations: the per-agent pin; `factory_status` shows waiting tasks; the skill's reminder to switch back. A later option is `fallback_after_minutes` on the provider (not in v1).
- **Long prompts.** A book review sends the whole book (about 14k tokens for the-local-patch), which is fine for Claude. A `novel` could be 150k+ words. Keep client runs to short formats unless needed.
- **Engine restart mid-task:** the leased task is lost, and the job retries with attempts + 1. Three restarts fail the job, and then `retry_book` applies.
- **Scriptorium restart resumes the factory.** Ask the user before the live check.
