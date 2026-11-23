# Research: what a Scriptorium start does in its first two minutes (HUB-44 live check)

Date of reading: 2026-11-23. Read-only. Scriptorium was NOT started; nothing was built or called. Paths: engine = `C:\projects\Personal\scriptorium\src\engine`, data = `C:\Users\Infplane\Scriptorium` (`~\Scriptorium`).

## Question

If `pwsh -File scripts\hub.ps1 start scriptorium -Force` runs now and Scriptorium is stopped about two minutes later, does anything call a paid or cloud model, and what makes that provably impossible?

## Answer

- Verdict: **SAFE AS IS**, today, on the live data. No pause is needed. The factory has nothing to run and nothing it may start. (Confirmed by reading code and data, not by running it.)
- Why (four facts): (1) `jobs\queued` and `jobs\running` are both empty (0 files); (2) all 42 books are `stage: published` and published is a terminal stage, so the pipeline never advances them; (3) the only way the factory enqueues a book start is `pickNext`, and it finds nothing: all 7 open ideas are `source: generated` and their topics (`fic-action-and-adventure`, `vn-science-fiction`) are `active: no`, and the only active topic is full (`target 1, done 1`); (4) idea generation needs fewer than 5 open ideas (`idea_low_water_mark: 5`), and 7 are open.
- The queue is **not paused** now (`config\factory.md`: `paused: false`), and a start would not change that. It does not need to be paused, because nothing is runnable.
- The guarantee is only as good as those facts. They must be re-checked right before the start (script in section 5). If any one fails (a `source: user` open idea, another active topic with room, fewer than 5 open ideas, a queued job), the verdict becomes SAFE WITH `paused: true` in `config\factory.md` (option c).

## Path through the code

All **confirmed** by reading unless marked inferred.

### Launch (hub.ps1, services.json)
- `services.json:5-19`: scriptorium `managed: true`, `start: {kind: electron, args: [".", "--headless"]}`, `requires: ["acp-proxy"]`, `lock: index\engine.lock`, `port 7341`, and the warning "Starting the engine resumes the book factory ... may use paid models".
- `scripts\hub.ps1:339-342`: without `-Force`, a service with a `warning` is skipped. `-Force` only skips that gate. It adds no other behaviour for start. (`-Force` also means "stop non-managed" in `stop`, `hub.ps1:515`; irrelevant here.)
- `hub.ps1:343-349`: starts `requires` first. acp-proxy already listens on 8787 (pid 9248, `Get-NetTCPConnection` just now), so it prints "already up" (Start-Service1 returns at `hub.ps1:330`).
- `hub.ps1:392-393`: for a managed service it calls `Clear-StaleLock -AtStart` before launch, then `Start-Detached`, output appended to `C:\projects\Personal\creative-hub\logs\scriptorium.out.log` / `.err.log` (`hub.ps1:414`). Those logs are appended, so the old content (last line dated 2026-11-16) stays. Note the byte size before the start.
- Headless Electron: `scriptorium\src\main\index.ts:31,41` forwards `--mcp` to the engine process. `hub.ps1` passes no pause, only, or concurrency argument, and `services.json` args are fixed, so a flag cannot be added without editing services.json.

### The stale lock (answer to part of Q5)
- `index\engine.lock` = `{"pid":19260,"started":"2026-11-21T20:30:48.246Z"}` (cat).
- pid 19260 is not running (`Get-Process -Id 19260` returned nothing). Last boot was 2026-11-22 12:22 (CIM `LastBootUpTime`), after the lock's time.
- `hub.ps1:453-457`: pid not running, so `Clear-StaleLock` removes it and prints `scriptorium: removed its stale lock (pid 19260)`.
- Even if hub.ps1 had left it, the engine would replace it: `store\dataFolder.ts:154-165` treats a lock started before the last boot, or one whose pid is dead, as stale and overwrites it.
- The engine then writes a new lock `{"pid":<new>,"started":...}` (`dataFolder.ts:165`).

### Engine `main()` (`index.ts`)
Order, from `index.ts:39-137`:
1. `initDataFolder` (seed copy of missing files, migrations, `index.ts:69-72`). Logs `[engine] data folder: ...`, `[engine] seed: copied N file(s), kept M existing...`, optional `[engine] migration: ...`.
2. `acquireEngineLock` (`:78`).
3. `new Engine(...)` (`:86`). No `--only` flag is passed.
4. `await engine.start()` (`:98`), detailed below.
5. `watchDataFolder` (`:99`). A change event calls `handleWatch` (`engine.ts:983-1024`): it reloads config and kicks the scheduler and pipeline. No job is created by a watch event.
6. `startMcpServer` on 127.0.0.1:7341 (`:106-109`; `config\mcp.md`: `enabled: true`, port 7341). Logs `mcp: listening on http://127.0.0.1:7341/mcp (no token set)` (`mcp\server.ts:144`).
7. Heartbeat every 3000 ms (`:116-119`).

### `engine.start()` (`engine.ts:237-263`), in order
1. `loadFactory` reads `config\factory.md` (`:439-446`; `paused`, limits, `only`).
2. `loadQualityAndFormats`, `loadSettings` (`config\settings.md`), `registry.load()` (providers.md, roles.md, models.md). A parse error is logged as `config/<name>.md: <message>`, and only for errors (`:444,457,1036`); a successful read logs nothing.
3. `void discoverModels()` (`:244`, `:466-476`): for providers with `discover: true` that are enabled and available, a `GET /models` listing (`registry.ts:408-448`). Only `acp` qualifies (`providers.md`: `acp` discover true; `strata`, `lmstudio`, `ollama` are `enabled: false`). Logs `models: acp serves ...` or `models: acp N found`. This lists models; it is not a completion request.
4. `syncSlots` now and every 10 s (`SLOT_SYNC_MS = 10_000`, `engine.ts:62,247-248`): `syncProxyHealth` does `GET /healthz` to loopback providers (the proxy, `:310-350`). No model request.
5. `budget.load()`, seeding the daily request counters (`:250-252`).
6. `jobs.recoverRunning()` (`:253`): running jobs go back to queued. There are 0 running, so it does nothing.
7. `agents.loadAll`, then `scheduler.start()` (`:259`): polls every 1000 ms (`scheduler.ts:168-173`, `pollMs ?? 1000`), first tick immediately.
8. `pipeline.start()` (`pipeline.ts:66-71`): `scanCovers` (under Electron the cover renderer exists; it only acts on a published book whose `cover_png` is `pending`/`requested`, `:582-588`; all 41 books with the key are `cover_png: done`, so nothing), then `kick()` at once and every 5000 ms (`tickMs ?? 5000`).
9. `budget.writeSummary()` (`:261`): rewrites the "Spend summary" below the marker in `config\budget.md`. The numbers stay the same; the "Updated" stamp changes. That is the only expected change in budget.md.

### What the scheduler would do (`scheduler.ts:346-461`)
- If `factory.paused` it does nothing (`:360`). It is `false` now.
- Otherwise it lists `jobs\queued`. Queue is empty, so the loop body never runs. No agent is given a job, and no model is chosen.

### What the pipeline factory tick does (`pipeline.ts:429-447`)
- Walks all books; `TERMINAL_STAGES = published, rejected, failed` (`pipeline\advance.ts:137`) are skipped (`:436`). 42 of 42 books are `stage: published` (grep of `books\*\book.md`).
- `factory.paused` false, so continues: `fillIdeas()` then `startBooks()`.
- `fillIdeas` (`:497-516`): active topics exist (eligible), but `open.length (7) >= idea_low_water_mark (5)` returns (`:508`). No `generate_ideas` job.
- `startBooks` (`:518-558`): `room`: 0 books in progress < `max_books_in_progress 5` (factory.md) so room is true. `pickNext` (`pipeline\handlers.ts:187-214`):
  - user ideas first (`:202-205`) ignore topic activity: **there are no open user ideas** (all 30 `source: user` ideas are `status: used`; the 7 open ideas are all `source: generated`).
  - generated ideas need `topic.active && hasRoom(topic)` (`:206-209`): the 7 open ideas are `fic-action-and-adventure` (3: peak-of-whispers, the-last-lighthouse-keeper, the-rust-runner; `topics.md:22` `active: no`) and `vn-science-fiction` (4: signal-lost, the-glass-horizon, the-gravity-garden, the-iron-tide; `topics.md:595` `active: no`).
  - fresh topic (`:210-213`): only one topic is `active` in `topics.md`: `my-after-petra-thrown-soother-...` (`topics.md:639`, `juvenile-visual-novel`, `yes`, `target 1`, `done 1`). `hasRoom` = `done + inProgress < target` = false (`handlers.ts:216`).
  - returns null, so no `eic--start--` job. The engine logs once `warning: no new book starts: every active topic has reached its target ...` (`pipeline.ts:539-541`, via `warnOnce`).
- No other loops create jobs. A grep of `setInterval|setTimeout` over the engine finds only: budget summary, log flush, MCP/clientSearch timers, slot sync, heartbeat, scheduler poll, pipeline tick, watcher debounce. There is no auto-idea or auto-book loop apart from the pipeline tick above.

### Embeddings / index work at start
- None at start. `MemoryService` opens `index\library.sqlite` lazily on first `getIndex()` (`memory\service.ts:5-30`). Callers of `getIndex()`/`reindexAll` are job handlers (`handlers.ts:325,1383`, `longHandlers.ts:199`, `researchHandlers.ts:339`, `research\context.ts:33`) and the CLI `reindex` (`cli.ts:87`). With no job there is no call. (confirmed by grep; inferred that no MCP call is made unprompted.)
- Model if it ever ran: `config\roles.md` front matter `embeddings: acp/llama/nomic-embed-text-v1.5`, a local model through the proxy (`providers.md` marks it `embedding: true`). Fine. `discover_skip: [ qwen-image, nomic-embed ]` hides it from discovery only.

### Pause mechanisms that survive a start
- `config\factory.md` `paused: true` is the one saved pause: "the saved state of pause all" (factory.md body), written by `setPaused` (`engine.ts:756-768`), read at start by `loadFactory` (`:238`, `:439`). While true the scheduler starts no job (`scheduler.ts:360`), and the pipeline tick returns before `fillIdeas`/`startBooks` (`pipeline.ts:440`). Running jobs are not touched by it. The factory is `paused: false` now.
- Per-book `paused: true` in `book.md` (`pipeline.ts:434`, `scheduler.ts:370`): not useful here.
- Per-agent `paused` in `agents\<agent>.md` (`scheduler.ts:487`): 27 agent files; not a clean switch.
- `only:` in `config\factory.md` or `--only <idea>` (`engine.ts:717-737`, `index.ts:87-96`): runs one idea. With `only` set to an unknown slug nothing runs, but `--only` makes the engine exit 1 and hub cannot pass it. Not a good pause.
- `pause_all` MCP tool (`mcp\tools.ts:1082` calls `handleCommand pauseAll`, `engine.ts:1360`): stored in the same `factory.md`. It exists only after the engine is up and the MCP server listens (`index.ts:106-109`), which is after the first pipeline tick (`engine.start()` runs `pipeline.start` kick first, `:98`). So it cannot pause before the first tick. There is no tool that writes the pause while the engine is down (no CLI for it in `index.ts` USAGE: only `probe`, `reindex`, `rebuild-reader`, `key-set`).
- Budget: `config\budget.md` caps are 20 USD/day, 40 USD/month (not zero). They block a paid model once reached (`scheduler.ts:399`), but today's spend is tiny, so they are not a pause. Setting `daily_cap_usd: 0` would be another switch (the failed jobs show it blocked paid models in the past: "daily cap 0 USD reached"), but it is a less clean way than `paused`.
- Concurrency in `providers.md` (e.g. `deepseek` concurrency 8) is not a pause.

### How a job would pick its model (for the jobs that exist NOW: none)
- `scheduler.ts:376-446`: agent chosen, then `router.candidates(role, {agentModel, bookModels, noLocalFallback})`, then the first model not limited, not over budget, usable and with capacity. A paid model is skipped only when over a cap (`:399`).
- Role lists (`config\roles.md` front matter, `fallback_shared: true` and `fallbacks` in `settings.md`: `deepseek/deepseek-flash`, then `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`):
  - Paid first (`paid` = `deepseek/deepseek-flash`, PAID) then `acp`: editor-in-chief, idea-generator, architect, writer, publisher.
  - `acp` first then paid: developmental-editor, line-editor, copy-editor, beta-reader, child-safety-reviewer, read-aloud-reviewer.
  - Local strata first (`acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, LOCAL) then paid: continuity-checker, originality-checker, fact-checker, researcher.
  - archivist: `acp/antigravity/gemini-4-hydrogen` (CLOUD through the proxy, no USD cost) then local strata, then paid.
  - humanizer: `deepseek/deepseek-flash` (PAID) then paid.
- Which are local here: only `acp/strata/...`, `acp/llama/...`, `acp/gufo/...` (`providers.md` comments). `acp/antigravity/*`, `acp/claude/*`, `acp/codex/*` are cloud models reached over the proxy (budget shows them at 0 USD, but they are cloud); `deepseek`, `openrouter`, `anthropic`, `gemini` are paid cloud. `client/claude-code` is a task parked for a Claude Code session (nothing is sent anywhere).
- `role_models` in a book's `book.md` is read through `getBookModel` (`scheduler.ts:379`) and goes in front of the list. Only jobs with that book would use it; none exist.
- Provider keys: envs `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `TAVILY_API_KEY` are not set as user/machine/process variables in this shell. The engine can also take keys from the Windows credential store (not checked here). `budget.md` shows `deepseek/deepseek-flash` spent 0.0104 USD this month, so a DeepSeek key has been usable. Treat deepseek as having a key. Enabled providers (`providers.md`): `acp`, `client`, `deepseek`, `openrouter`, `anthropic`, `gemini`, `tavily`, `wikipedia`, `client-search`; disabled: `lmstudio`, `strata`, `ollama`, `brave`, `serpapi`, `serphouse`, `duckduckgo`. ("A provider whose key can't be found is skipped", `providers.md:257`.)

## Live data (read-only)

- `jobs\queued`: 0; `jobs\running`: 0; `jobs\done`: 4054; `jobs\failed`: 4 (all `task: research`, role researcher; books `the-one-way-street-why-time-only-runs` x3 and `the-salt-line` x1; failures: ECONNREFUSED/HTTP 400 on `acp/antigravity/gemini-3.8-flash`, one LM Studio load error). Failed jobs are never retried by a start (`recoverRunning` handles only `running`; retry needs the `retryBook` command, and the books are published, not failed). No queued/running jobs to list (0).
- Is the queue paused now? No: `config\factory.md` `paused: false`. There is no other state file for pause (`jobs\` has no state file; only the four folders).
- `config\factory.md`: `paused: false, max_books_in_progress: 5, idea_low_water_mark: 5, research_limit_per_book: 10, max_attempts: 3`, no `only`; `max_articles_in_progress` not in the file (schema default 3, `shared\schemas.ts:163`).
- `config\settings.md`: no auto/factory switch. Keys: `byline`, mail settings, `fallbacks` (deepseek-flash, then strata), `fallback_shared: true`, `last_resort_model: ""`, `lmstudio_*`. `last_resort_model` empty, so no extra last resort.
- `config\budget.md`: `monthly_cap_usd 40`, `daily_cap_usd 20`, `per_book_cap_usd null`. Month so far 0.0104 USD; today (2026-11-21 last entry) 0.
- `config\mcp.md`: enabled, 127.0.0.1:7341, `token_env SCRIPTORIUM_MCP_TOKEN` (no token noted in the lock check; engine logs "no token set" if unset).
- Books: 42, all `stage: published`; 41 have `cover_png: done`.
- Ideas: 46 files; 39 `status: used`, 7 `open`, listed above; open ones carry no `role_models`/`models`/`no_local_fallback` keys.
- Spend ledger: `logs\spend\2026-11.md` last row is 2026-11-21T21:43:10 `probe` role (`cli`), 235569 bytes, mtime Nov 21 21:43. `logs\app.log` last line 2026-11-02 ("another Scriptorium is running ... quits").

## Reproduction

Not applicable (not a bug). Not reproduced: Scriptorium was not started, by instruction. All findings are from reading the code, the services registry and the data folder. The built engine `out\engine\index.js` (mtime 2026-11-23 10:26) postdates `src\engine\engine.ts` (Nov 16) and `pipeline.ts` (Nov 14), so it should contain the code read (inferred; the built file was not read).

## What the plan needs (the live check)

### 1. Before start: record a baseline and re-check the preconditions (read-only)
Re-run just before `hub.ps1 start`; every line must hold:
- `jobs\queued` and `jobs\running` have 0 files.
- `config\factory.md`: `paused: false` is fine, no `only` key; if you prefer to be safe, see option (c).
- No open idea with `source: user`:
  `grep -l '^status: open' ~/Scriptorium/ideas/*.md | xargs grep -L '^source: generated'` prints nothing.
- Active topics: `grep -nEi '\|\s*(y|x|yes)\s*\|' ~/Scriptorium/topics.md` shows only the one full row (line 639, target 1, done 1). Any other active row with room (or target empty or 0) would start a book.
- Open ideas count >= 5 (it is 7); if fewer than 5 and an eligible topic exists, `generate_ideas` (idea-generator role, `paid` first) would be enqueued.
- All books are `stage: published` (`grep -h -m1 '^stage:' ~/Scriptorium/books/*/book.md | sort | uniq -c` shows only `42 stage: published`).
- Baseline to compare later: `jobs\done` = 4054, `jobs\failed` = 4, byte size and mtime of `logs\spend\2026-11.md` (235569, Nov 21 21:43), mtimes of files in `logs\agents\`, byte size of `C:\projects\Personal\creative-hub\logs\scriptorium.out.log` and `.err.log`.

### 2. Option ranking for the "free of paid calls" guarantee
- **(a) Nothing needed: applies today.** No job can run (queue empty, all books terminal, `pickNext` returns null, ideas above the low-water mark). The brief's "Scriptorium resumes its whole book factory" is true only when ideas, topics and books give it work. Here it has none.
- **(b) An existing pause that survives the start without editing a file by hand: none exists.** `paused: true` in `factory.md` survives, but the only tools that write it (`pause_all` over MCP, or the UI button) need a running engine, and the engine's first pipeline tick runs before the MCP server listens (`index.ts:98-110`). No CLI command writes it while the engine is down. State it plainly: not possible without touching the file.
- **(c) Reversible one-key edit (optional belt and braces).**
  - File: `C:\Users\Infplane\Scriptorium\config\factory.md`, key `paused`.
  - Before: `paused: false` (front matter line 3). After: `paused: true`.
  - Backup first: copy to `C:\projects\Personal\creative-hub\.claude\temp\factory.md.bak-HUB-44` (temp folder per the global rules).
  - Read at start by `loadFactory` (`engine.ts:238`). While running the engine re-reads the file when it changes (`handleWatch` → `loadFactory`, `engine.ts:1007-1010`).
  - Effect: `scheduler.ts:360` and `pipeline.ts:440` stop everything that enqueues or starts a job. The engine would still read config, discover models, serve MCP and heartbeat.
  - Revert: write `paused: false` back (or copy the backup over), or call the `resume_all` MCP tool once the engine is up. The check must restore this key before leaving, or the user's factory stays paused.
  - Cost: it is an edit of a live file, and the user said not to edit live files by hand unless needed. Since (a) holds, it is not needed. Use it only if a precondition in step 1 fails or the user wants a proof that does not depend on those facts.
- **(d) Not needed.** (`only: <nonexistent slug>` in factory.md would also stop all jobs, with a warning, but is a worse switch than `paused`.)

### 3. What to look at during the run (about 2 minutes)
- hub.ps1 output, in order: `scriptorium: requires acp-proxy`, `acp-proxy: already up on 8787`, `scriptorium: removed its stale lock (pid 19260)`, `scriptorium: started (launcher pid N), waiting for port 7341...`, then `scriptorium: up at http://127.0.0.1:7341/mcp (pid N)` (`hub.ps1:330,347,456,415,425`). `startTimeout` is not set in services.json, so the wait is `max(WaitSeconds, 0)`.
- Right after: `index\engine.lock` has a new pid and a fresh `started`.
- Logs: `C:\projects\Personal\creative-hub\logs\scriptorium.out.log` (new lines after the recorded offset; use `hub.ps1 logs scriptorium`). Expected lines:
  - `[engine] data folder: C:\Users\Infplane\Scriptorium`
  - `[engine] seed: copied 0 file(s), kept N existing...` (a nonzero `copied` or a `migration:` line would mean the app changed files; note it)
  - `[engine] models: acp serves ...` or `models: acp N found` (discovery of the proxy)
  - `[engine] warning: no new book starts: every active topic has reached its target (books in progress count toward it, and they go on). Raise a target in topics.md or switch on another topic.` (`pipeline.ts:540`; this is positive proof that the first pipeline tick ran and `startBooks` had no pick)
  - `[engine] mcp: listening on http://127.0.0.1:7341/mcp (no token set)` and the main process heartbeat relays.
- "Read roles/providers/settings without an error": the engine does not print a success line for config files (`engine.ts:444,457,1036`); it prints `config/<name>.md: <message>` only on error. So proof = those lines are absent, plus the `models: acp ...` line (providers.md parsed, `registry.load` ok) and `models:` / `aliases` warnings absent (`warnAliases`, `engine.ts:243,1041+`; a `roles.md` alias with no matching `fallbacks` row is logged once). Also grep `.err.log` for `fatal`, `invalid agent file`, `could not reload`.
- Optional, MCP (read-only): `factory_status` (`mcp\tools.ts:145`) shows paused flag, queue, blocked jobs. Call it only if useful; it calls no model.

### 4. After: prove no model job ran and no paid model was called (from Scriptorium's own files)
- `jobs\queued` and `jobs\running` still 0, `jobs\done` still 4054, `jobs\failed` still 4. A started job would have appeared in `running` and then `done`/`failed` (`scheduler.ts:447,774`).
- `logs\spend\2026-11.md` unchanged (size 235569, mtime Nov 21 21:43; every model request, even a local one, appends a row, `budget\spend.ts`). No new row = no request of any kind. A paid request would also move the "Today" and "This month" lines in `config\budget.md` (today 0.0000, month 0.0104 USD, 1 deepseek request).
- `config\budget.md`: only the "Updated ..." stamp may change (`writeSummary` at start, `engine.ts:261`); the spend numbers and the per-model, per-role list stay exactly as they are above (e.g. `deepseek/deepseek-flash: 0.0104 USD ... 1 requests`).
- `logs\agents\*.md` (per-agent job logs, `scheduler.ts:605-618` writes `## <time> job` there): no mtime newer than the start; none created.
- Engine log: no `job.started`-style line; there is no job log line, no `every model of ... is unusable`, no `DEVIATION:`, no `recovery:` line (the last would mean running jobs existed).
- Also the proxy side: `C:\projects\Personal\creative-hub\logs\acp-proxy.out.log` should show only `GET /v1/models` and `/healthz`, no `chat/completions` request in the window (inferred about its log format; not read).
- Stop: `pwsh -File ...\hub.ps1 stop scriptorium` (taskkill runs no shutdown code, so hub removes the lock itself, `hub.ps1:432-456`; the engine's own SIGTERM path `index.ts:122-133` is not used). Confirm `index\engine.lock` is gone or stale-and-removed.

## Risks

- The proof depends on five data facts (queue empty; no open user idea; only the full topic active; open ideas >= 5; all books terminal). The user or another session could change any of them (an idea file edit, a topic tick in the UI, `add_story` over MCP) between this reading and the start. The scan at step 1 closes that. A user idea becomes startable at once even if its topic is inactive (`handlers.ts:202-205`), and `start_book` goes to `editor-in-chief` whose first model is the PAID `deepseek/deepseek-flash` (`roles.md`), so this is the one path that would spend.
- MCP is on at 127.0.0.1:7341 with no bearer token set (engine logs "no token set" when `SCRIPTORIUM_MCP_TOKEN` is unset; whether it is set was not checked). Any local MCP client during the window could call `add_story` and so on; only if something does, jobs appear. Keep other agents from calling it during the window (or use the `paused` option).
- Cloud-through-proxy models are not "paid" in the budget file (cost 0.0000) but are cloud: `acp/antigravity/*`, `acp/claude/*`, `acp/codex/*`. The archivist's first model is `acp/antigravity/gemini-4-hydrogen`, and the researcher, checkers and editors fall back to `deepseek/deepseek-flash`. The proof above covers all of them, because it shows no job (hence no request) ran.
- A start rewrites `config\budget.md` (stamp), `index\engine.lock`, and may seed missing files from `seed\` (`index.ts:69-72`). `index\library.sqlite` is opened lazily, so it should not change; its backup `library.sqlite.bak-HUB-44` exists from the earlier re-chunk.
- If the log shows `recovery: N running job(s) back to queued`, running jobs existed after all (a changed fact); stop at once.
- The built `out\engine\index.js` was not read; behaviour read from `src\`.
- hub.ps1 needs pwsh 7 (HUB-44 earlier change); the brief's command uses `pwsh`, fine.

## Open questions

- Are the Windows credential-store keys set for DeepSeek/OpenRouter/Anthropic/Gemini/Tavily? Not checked (env vars are unset; the store was not queried). Not needed for the verdict, since no job runs.
- Is `SCRIPTORIUM_MCP_TOKEN` set? If not, MCP accepts any local caller during the window.
- Does the acp-proxy log every request line? Not read; the spend ledger and job folders are the primary evidence.
- Does the `seed:` line copy anything at start (a newer seed than the data folder)? Unknown until the log shows it; the settings reading showed nothing that needs seeding.
