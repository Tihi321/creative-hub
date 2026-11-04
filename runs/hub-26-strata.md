# HUB-26 Strata model discovery: live check L2 (DeepSeek)

Started 2026-11-04. Ticket: `.claude/tickets/HUB-26-strata-model-discovery/plan.md`. Branch `HUB-26_strata-model-discovery`.

## Setup

- Strata variant: deepseek (`D:\Strata\run-deepseek-v4.1-flash-ist-das-2.00bpw.bat`), started by the user. Not stopped, restarted or reconfigured by this check.
- `/health`: `{"model":"deepseek-v4.1-flash","loaded":true,"max_context":131072}`.

## L2: `node scripts/strata-probe.mjs` (verbatim)

```
Strata probe against http://127.0.0.1:8080
PASS  GET /health - model=deepseek-v4.1-flash loaded=true
PASS  GET /v1/status - model=deepseek-v4.1-flash concurrency.serving=1
PASS  GET /v1/models - id=deepseek-v4.1-flash n_ctx=131072
PASS  (a) stream, include_usage, reasoning_effort none - answer="The sea is a vast, restless expanse of water that shapes the..." reasoning_chars=0 usage=yes
PASS  (b) stream, reasoning_effort low - answer="The sea is vast and ever-changing." reasoning_chars=63
PASS  (c) JSON-shaped answer without response_format - answer="{\"colour\": \"red\", \"count\": 3}"
PASS  (d) tool call, one function, reasoning_effort none - tool_calls="draw_rect{\"x\":1,\"y\":2,\"size\":3,\"colour\":\"red\"}"
PASS  (e) response_format json_schema (informational) - answer="{\"colour\":\"red\",\"count\":3}"

All required checks passed
```

Result: (a)-(d) PASS, (e) accepted (informational: the `deepseek-v4.1-flash` profile may set `json_schema: true`; not decided here).
Step 2 of the check (finding another `extra_body`) was not needed: (a) returned no reasoning text with `reasoning_effort: none` and (b) answered, with 63 reasoning characters as expected for `low`. No seed was edited; the profile needs no extra `extra_body`.

## hub.ps1

`pwsh -NoProfile -File scripts\hub.ps1 status`: `strata  up  8080  Idle  http://127.0.0.1:8080/health  deepseek-v4.1-flash` (Model column filled; every other service down). AC-H2 status part: PASS. The Pid column shows 0 for strata (the process id is not resolved; cosmetic, not checked further).

`pwsh -NoProfile -File scripts\hub.ps1 start strata`: printed `strata: already up on 8080`, started nothing, then the status table. AC-H1b: PASS.

AC-H2 start part: PASS. The director ran `hub.ps1 start strata deepseek` in a terminal at 12:08 and it opened `cmd /k run-deepseek-v4.1-flash-ist-das-2.00bpw.bat` (verified by the process list).

## Verified

- AC-H2 start part (see above).
- Probe (a)-(e) against DeepSeek v4.1 flash; `hub.ps1 status` shows the loaded model; `hub.ps1 start strata` with Strata up starts nothing.

## Not verified

- L5 (live switch to Qwen), L6 (Scriptorium): not run. L3 and L4 are under "Apps (L3-L4)" below.
- Probe re-run with the Qwen IQ3_S Strata (regression check): pending, needs the user to restart Strata.
- User-data migration (T8) and use of the apps on the DeepSeek Strata by the user: pending. The ticket is done only when the user has used the apps.

## Apps (L3-L4)

Run 2026-11-04 12:15-12:35 against the DeepSeek Strata (`/health` model `deepseek-v4.1-flash`, not stopped or restarted; ComfyUI and Scriptorium never started). Each app was built from its ticket branch (VNO-60, EGS-60, BTT-24, PAR-17, MDI-12 `*_strata-model-discovery`, all trees clean before and after; `yarn build:engine` for VN, Edu, BT; `yarn build` for Pixel, Chiptune: all exit 0). Backups of the five `config` folders (and VN/Edu `.seed-hashes.json`; the BT/Pixel/Chiptune `seed-state.json` sit inside `config`) are in `.claude/temp/HUB-26-backup/<app>/`, hash-verified identical to the originals before any start. No app was running at the start (the `engine.lock` files were stale: dead pids).

Method notes:
- `hub.ps1 start <id>` starts every app but then reports "not listening after 60 s" and `hub.ps1 stop` says "not running": from this agent session `Get-NetTCPConnection` only shows 6 listeners (Strata's among them), so `Get-Listener` cannot see the apps' ports although the MCP endpoints answered on them. I verified with HTTP instead and stopped each app by the pid from its lock file (`Stop-Process`), then checked the port was closed. Run from a normal terminal this is probably fine; not investigated.
- `VNO_AUTOSTART=0` / `EDU_AUTOSTART=0` were set in the environment for VN and Edu (no config file change), so ComfyUI, Pixel and Chiptune were not started by them.
- "Served model" evidence comes from the engine log (`models: strata now serves deepseek-v4.1-flash`), the `engine probe` / `engine models` CLI, and a throwaway tsx script (deleted) that builds the app's own `ModelRegistry` / `createLlm` on the live data folder and prints `getModel(ref)` (`servedId`, `family`, `context`, `extraBody`). The Models page / picker labels were not looked at (no window was opened).

### VN Studio (VNO-60), data `~\VisualNovels`
- Migration: `strata-loaded-v1` plus the two follow-ups `strata-loaded-roles-v1`, `strata-loaded-settings-v1` recorded in `.seed-hashes.json`. providers.md: strata `discover: true`; rows `default` and `default-low` (`loaded: true`, aliases `qwen3.8-flash-next` / `-low`, context 131072, `reasoning_effort` none / low); profiles `qwen3.8-flash-next` (qwen) and `deepseek-v4.1-flash` (deepseek); old rows removed; `concurrency: auto` kept. roles.md line 17 `strata/default-low`; settings.md fallback `strata/default`. `budget.md` also changed (the engine's daily spend rollover, unrelated). Nothing else changed. OK.
- Served: log `models: strata now serves deepseek-v4.1-flash`, later `strata serves ...`. Registry: `strata/default` and `strata/default-low` servedId `deepseek-v4.1-flash`, family `deepseek`, context 131072, extra_body none / low, jsonSchema false; legacy ref `strata/qwen3.8-flash-next-low` resolves to `strata/default-low`.
- Request: `engine probe --model strata/default` answered (12 in / 17 out), `strata/default-low` answered (38 / 57), legacy `strata/qwen3.8-flash-next` answered; cost 0 (local); spend rows written with provider strata, model default / default-low.
- VERIFIED (engine, config, request). NOT VERIFIED: Models page label, a `vn.analyse` job (not run).

### Edu Studio (EGS-60), data `~\EduGames`
- Migration: same three ids; same strata block, roles.md lines 37 and 39 `strata/default-low`, settings.md `strata/default`. The seeded roles.md rationale (line 79) was also updated by the seed update (DeepSeek note). Side effect to know: this app rewrote the whole providers.md YAML, so comment alignment and flow lists changed (`[ content-safety ]`, `discover_skip: [ dflash ]`, `search_order: [ client-search, wikipedia ]`, spacing before `#`); values unchanged. VN did not do this. `budget.md` changed by the daily rollover.
- Served: log `models: strata now serves deepseek-v4.1-flash`; registry output identical to VN (deepseek, 131072, none / low).
- Request: `engine probe --model strata/default` answered (12 in / 22 out), `strata/default-low` answered; cost 0.
- The engine moved a stale `running` job (`deutsch-a1-pilot--summarize--all--r4`, model `client/claude-code`, parked for a Claude client) back to queued on start ("recovery"); nothing ran, no spend.
- VERIFIED (engine, config, request). NOT VERIFIED: Models page label.

### Book Translator (BTT-24), data `~\BookTranslator`
- Migration: `strata-loaded-v1` added to `config/seed-state.json`. providers.md: `concurrency: 1` became `auto`, `discover: true`, loaded rows and profiles as above (comment spacing on one line changed: `local: true # Claude Code ...`). defaults.json: `strata/qwen3.8-flash-next` became `strata/default` at lines 4, 9, 13, 16, 156 (agentModels, fallbacks, groupDefaults). Nothing else changed. OK.
- Served: `engine models` prints `discovery strata: serves deepseek-v4.1-flash`; log `models: strata now serves deepseek-v4.1-flash`; registry: servedId `deepseek-v4.1-flash`, family deepseek, context 131072, none / low. Gap: the MCP `list_models` tool does not show it, because `trimModels` in `src/engine/mcp/server.ts:64-66` keeps only ref, available, local, context and prices (the dispatcher's UI summary does carry `served`, `dispatcher.ts:209`). It lists `strata/default` and `strata/default-low` (available, context 131072, free).
- Request: `ModelRouter.complete` on `strata/default` (12 in / 21 out) and `strata/default-low` (38 / 53) answered, cost 0. No glossary job on a test project was run.
- VERIFIED (migration, models, request). NOT VERIFIED: UI label, a translation job.
- Security note: `logs/book-translator.err.log` holds the MCP token in plain text (`[headless] token (shown once): ...`, one line per start). Existing behaviour, not caused by HUB-26.

### Pixel Studio (PAR-17), data `~\PixelStudio`
- The headless `--mcp-only` engine starts and serves MCP but never creates the LLM layer (`LlmService.get()` is lazy, used by the window's chat; Pixel has no MCP chat tool), so the app's start alone did not migrate anything (config unchanged after start; confirmed by diff). I then ran `createLlm({ configDir: ~/PixelStudio/config, seedDir: <repo>/seed/config })`, the exact call the app makes on first chat use, via a throwaway tsx script (deleted).
- Migration (by that call): `strata-loaded-v1` in `seed-state.json`; providers.md strata block as C1 (rows keep `tools: true`; `discover: true`; profiles incl. deepseek); roles.md `aliases.strata: strata/default`; models.md `shown` `strata/default`; app.json `selectedModel` `strata/default`. This writer also re-aligned comment spacing across providers.md (`# ...` after one space, `[ content-safety ]`); values unchanged. OK.
- Served: registry `strata/default` and `-low`: servedId `deepseek-v4.1-flash`, family deepseek, context 131072, tools true, vision false, extra_body none / low; `-low` `shown: false` (so it stays out of the picker); legacy ref resolves to `strata/default`.
- Request: tool-call chat through `strata/default` with one `draw_rect` function answered with tool call `draw_rect {"x":1,"y":2,"size":3,"colour":"red"}` (finish `tool_calls`); `strata/default-low` plain chat answered.
- VERIFIED (migration, registry, tool-call chat via the app's llm layer). NOT CHECKABLE headless: the chat picker label and the agent chat itself (needs the desktop window; no MCP chat tool).

### Chiptune Studio (MDI-12), data `~\ChiptuneStudio`
- Same as Pixel (headless engine has no LLM layer; no `engine.lock` is written by this app). Migration by `createLlm`: `strata-loaded-v1`; providers.md as C1 (same comment re-alignment); roles.md `strata: strata/default`; models.md `shown` lines 11-12 `strata/default`, `strata/default-low`; app.json `selectedModel` `strata/default`. OK.
- Served: registry `strata/default` and `-low`: servedId `deepseek-v4.1-flash`, family deepseek, context 131072, tools true, vision false, none / low, both `shown`.
- Request: tool-call chat through `strata/default` with one `add_note` function answered with tool call `add_note {"pitch":60,"start":0,"length":4}`; `strata/default-low` plain chat answered.
- VERIFIED (migration, registry, tool-call chat). NOT CHECKABLE headless: picker label and the composer chat in the window.

### After the run
All five apps stopped (ports 7459, 7463, 47811, 7457, 7458 closed); Strata still `loaded: true`; five repos clean on their branches; nothing committed. Config folders keep the migrated files (backups in `.claude/temp/HUB-26-backup/`). `.seed-hashes.json` / `seed-state.json` now list `strata-loaded-v1`, so a restore must restore those too (they are in the backup).

## Switch to Qwen (L5) and Qwen probe (L2)

Run 2026-11-04 by a sub-agent for the director. Nothing started, stopped or restarted; nothing committed.

### Detection (L5)
- The DeepSeek console was closed by the user. Strata was then started by the director with `hub.ps1 start strata` (iq3_s, about 13:2x local). Strata `/health`: model `qwen3.8-flash-next-iq3_s`, loaded true.
- VN Studio (port 7459, VNO-60 build) noticed the new model on its status poll. `logs/vn-studio.out.log`, last lines:
  - `[engine] models: strata serves deepseek-v4.1-flash`
  - `[engine] models: strata is down (http://127.0.0.1:8080/v1 does not answer, or has no model loaded), jobs use the next model in their role`
  - `[engine] models: strata now serves qwen3.8-flash-next-iq3_s (was deepseek-v4.1-flash)` (13:27:25)
  - `[engine] models: strata answers again`
- Result: VN followed the model change with no restart. VERIFIED.

### Strata probe (L2) verbatim, `node scripts/strata-probe.mjs`
```
Strata probe against http://127.0.0.1:8080
PASS  GET /health - model=qwen3.8-flash-next-iq3_s loaded=true
PASS  GET /v1/status - model=qwen3.8-flash-next-iq3_s concurrency.serving=1
PASS  GET /v1/models - id=qwen3.8-flash-next-iq3_s n_ctx=131072
PASS  (a) stream, include_usage, reasoning_effort none - answer="The sea stretches endlessly to the horizon, whispering secre..." reasoning_chars=0 usage=yes
PASS  (b) stream, reasoning_effort low - answer="The sea stretches endlessly beneath a wide, quiet sky." reasoning_chars=94
PASS  (c) JSON-shaped answer without response_format - answer="{\"colour\": \"red\", \"count\": 3}"
PASS  (d) tool call, one function, reasoning_effort none - tool_calls="draw_rect{\"x\":1,\"y\":2,\"size\":3,\"colour\":\"red\"}"
PASS  (e) response_format json_schema (informational) - answer="{\"colour\":\"red\",\"count\":3}"

All required checks passed
```
(a) has reasoning_chars=0 with reasoning_effort none, as required for Qwen.

### VN served / family
The VN MCP (http://127.0.0.1:7459/mcp) has no model-status tool (tools/list: none for models; initialize and tools/list worked, no auth). Evidence instead from the VN repo's own registry code (`ModelRegistry.load()` + `discover()` against `~\VisualNovels`, run with tsx from a scratchpad script, a separate read-only process, not a second engine):
- discovery strata: served `qwen3.8-flash-next-iq3_s`
- `strata/default`: servedId `qwen3.8-flash-next-iq3_s`, family `qwen`, context 131072, extra_body `reasoning_effort: none`, available true
- `strata/default-low`: servedId `qwen3.8-flash-next-iq3_s`, family `qwen`, context 131072, extra_body `reasoning_effort: low`, available true

### Request through VN's router
`node out/engine/index.js probe --model <ref>` (loads the registry and calls ModelRouter; does not start the engine, so no lock conflict):
- `strata/default`: answered "Libraries are quiet sanctuaries that nurture curiosity and community." tokens in/cached/out 20/0/14, cost 0.
- `strata/default-low`: answered "Libraries remain one of the most valuable free resources in any community." 48/0/35, cost 0.

### Status
- VERIFIED: probe (a)-(e) all PASS on Qwen; VN log shows the live switch; registry served/family qwen on both profiles; both requests answered.
- NOT VERIFIED: the served/family were read from a fresh registry in a separate process (same code and config), not from the running engine's memory (no MCP tool exposes it; the running engine's view is evidenced only by its log line); VN Models page label; a real VN job on Qwen.

## Scriptorium (L6, CLI only) and user data

Date 2026-11-04. Scriptorium repo `C:\projects\Personal\scriptorium` on `SCP-52_strata-model-discovery` (96042eb), clean before and after. Strata served `qwen3.8-flash-next-iq3_s` on :8080 (not touched). The app, engine server, MCP and factory were not started.

### Safety check
- `src/engine/index.ts`: `argv[0] === 'probe'` calls `probe()` and returns before the engine lock, the Engine (queue/scheduler/factory) and the MCP server (`startMcpServer`).
- `src/engine/cli.ts` `probe()`: `initDataFolder` (seed copy of missing files + migrations, incl. `migrateStrataLoaded` and `migrateSeedPrompts`), `registry.load()`, `registry.discover()` (GET /models on providers with `discover`), then `router.chat([model])` with only the `--model` ref (no fallbacks added, `retries: 0`), then one embedding with `roles.md` `embeddings` = `lmstudio/text-embedding-nomic-embed-text-v1.5` (local, free), `budget.flush()`. No paid model in the path.
- No Scriptorium process was running; `~\Scriptorium\index\engine.lock` named pid 43680 (dead, from before the last boot: stale). `probe` does not take the lock anyway. Port 7341 not listening.

### Backup
`C:\projects\Personal\creative-hub\.claude\temp\HUB-26-backup\scriptorium\` = `config`, `prompts`, `templates`, `agents`, `topics.md` (the folders the seed copy and migrations can touch; there is no separate migration state file). Verified with `diff -rq` / `cmp` before the run.

### Probe output (`yarn build:engine`, then `node out/engine/index.js probe --model <ref>`)
- discovery: acp failed (not running), lmstudio failed (not running), strata 0 model(s) (loaded rows: discovery only notes the served model).
- `strata/default`: "Libraries are vital community hubs that provide free access to information and foster lifelong learning." tokens in/cached/out 20/13/18, cost 0 (local).
- `strata/default-low`: "Libraries are quiet spaces where knowledge is freely available to everyone." 48/43/35, cost 0 (local).
- Both: embedding failed (LM Studio not running at :1234), which made the second run exit 1; the model requests themselves succeeded.

### Config diff against the backup
- `providers.md`: strata provider is the C1 shape: rows `default` (`loaded: true`, aliases `[qwen3.8-flash-next]`, context 131072, `reasoning_effort: none`) and `default-low` (`loaded: true`, aliases `[qwen3.8-flash-next-low]`, `reasoning_effort: low`), `profiles` `qwen3.8-flash-next` (qwen) and `deepseek-v4.1-flash` (deepseek), `discover: true`; the two old rows gone. Side effect of the YAML rewrite: inline comment alignment collapsed to one space, `[dflash]` -> `[ dflash ]`, `search_order: [ ... ]` spacing, one top-level comment before `client-search` indented; values unchanged. The strata `discover: true` line kept its old comment ("fixed ids keep roles.md the same"), now stale.
- `roles.md`: the five `strata/qwen3.8-flash-next-low` refs (continuity-checker, originality-checker, fact-checker, researcher, archivist) -> `strata/default-low`. Nothing else.
- `settings.md`: no change from the migration (no old ref; `last_resort_model` is "").
- `budget.md`: only the engine-kept spend summary (date, two probe rows of 0 USD).
- `prompts`, `templates`, `agents`, `topics.md`, other config files: unchanged.

### Fallbacks edit (manual, user-approved)
`settings.md` `fallbacks` is now `deepseek/deepseek-flash`, `strata/default`, `lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic` (LF, same indentation). No CLI command lists roles, so a read-only tsx script (`.claude\temp\HUB-26-backup\resolve-check.mts`, `ModelRegistry.load()` only, no discovery or requests) checked it: `strata` -> `strata/default`; `strata/qwen3.8-flash-next` -> `strata/default`; unresolved aliases: none; architect = deepseek-flash, strata/default, lmstudio gemma; continuity-checker = strata/default-low, lmstudio gemma, deepseek-flash.

### Status
- VERIFIED: probe path cannot start the factory or call a paid model (code read); migration produced the C1 strata shape and renamed refs; both Strata rows answered through Scriptorium's router at 0 cost; `strata` alias resolves to `strata/default` after the fallbacks edit.
- NOT VERIFIED: the app's Models dialog and status bar (app not opened); a real Scriptorium job on Strata; embeddings (LM Studio was not running).
