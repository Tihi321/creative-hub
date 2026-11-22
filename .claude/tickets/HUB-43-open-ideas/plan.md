---
status: done
request: REQ-0030
repos: [creative-hub, api-acp-proxy, visual-novels-orchestrator, cartoon-studio, pixel-art-generator]
branch: HUB-43_open-ideas
updated: 2026-11-22
---

# HUB-43 The open ideas of REQ-0030, built before one round of rebuilds and live checks

The user said on 2026-11-22, word for word: "Ok build open idea first" (before the pending rebuilds and live checks of HUB-42, so that one rebuild and one round of checks covers everything). Reading (the director's): every extra idea still marked pending is triaged and, where valid and buildable at a sane size, built with the director's recommended choice; then one merged list of rebuilds and live checks.

Every item was checked on 2026-11-22 against master: creative-hub a2e0788, api-acp-proxy 23cf725, pixel-art-generator 9429022, visual-novels-orchestrator fe42e25, cartoon-studio d80ab09 (edu-game-studio 7d93579 and scriptorium 980e415 have no item). Strata on 8080 and the embedding llama-server on 8083 were read with GETs only; no model was called; nothing was started or stopped. The live data folders were only read.

## Triage (in the order of `## Extra ideas` in `.claude/director/requests/REQ-0030-acp-for-all.md`, the nine `decision: pending` lines, then the findings the director named)

| # | idea (short) | verdict | ticket | reason (verified 2026-11-22) |
|---|---|---|---|---|
| 1a | Monitor: sparklines | BUILD | AAP-49 | Strata `/metrics` `history`: ten series of 60 points, one a second (`D:\Strata\terminal\serve\telemetry.py:27,1806-1809`); drawn as inline SVG with attributes (the page's CSP is `style-src 'self'`, `src/renderer/settings.html:5`) on the six Strata tiles |
| 1b | Monitor: reasoning tokens per request | BUILD | AAP-49 | `traceUsage` (`src/server.ts:54-59`) already computes `openAiUsage().reasoning` for every provider that reports thought tokens, and an estimate otherwise, and drops it; it goes into `ActivityEntry`, the Requests page and a Monitor column |
| 1c | Monitor: `--metrics` for llama-server | TOO LARGE for this cut | next proxy ticket | it pushes AAP-49 to 15 files. Sketch: `buildLlamaArgs` adds `--metrics` (no setting; the embedding server's args and its restart key are untouched, `src/llama-args.ts:54-76`, and the key is compared only within one settings save, `src/electron/main.ts:317-323`, so an upgrade restarts nothing); a whitelist mapper for `llamacpp:tokens_predicted_total`, `tokens_predicted_seconds_total`, `prompt_tokens_total`, `prompt_seconds_total` (llama.cpp `tools/server/README.md:1122-1146`); Llama's Decode and Prefill tiles. Smallest useful cut: exactly that, 6 files, with a live read of `8082/metrics` on Inkling. The facts are in AAP-49's "Next cut" |
| 1d | Monitor: Gufo status | NEEDS A RUNNING SERVICE | probe P1 | no endpoint known (the proxy probes only `/v1/models`, `src/settings.ts:15`; no docs in `D:\Gufo\v0.35.0`; Gufo not running) |
| 1e | Monitor: a local server started outside the app | BUILD for Strata and Llama; Gufo NEEDS A RUNNING SERVICE | AAP-49; K5 | the Monitor shows "No local model loaded" while the proxy sends requests to an outside server (`src/local-models.ts:180-181`); `fetchEngine` can read Strata and Llama on their configured ports (`src/local-monitor.ts:111-125`) |
| 2a | Strata `/v1/telemetry` and `/v1/status` as Monitor sources | NO CHANGE | - | both shapes recorded in AAP-49's plan; every number a tile would use is already in `/metrics` (`last_timings` repeats the newest request, `machine` repeats `hardware`, `devices` and `recent` repeat `hardware` and `requests`); `dialects` are Strata's own, not the proxy's |
| 2b | Strata's conversation-cache numbers | BUILD (one tile) | AAP-49 | `/metrics` `conversation_cache` `{enabled, budget_mib, slots, parked, bytes, evictions, parks, restores, requests, requests_reused, reused_tokens, ...}`, same answer, no new request |
| 3a | Monitor: a distinct state after a render error | BUILD | AAP-49 | `tick()` swallows a render error and keeps the old numbers silently (`src/renderer/monitor-view.ts:74-75`) |
| 3b | Monitor: cache `apiKeyNeeded` | BUILD | AAP-49 | each 2 s poll calls `proxy.getSettings()` (`main.ts:530`), which re-resolves the config (`src/controller.ts:135-139`), only for `server.apiKey` |
| 4 | `architecture.input_modalities` for Gufo and Llama profiles | NO CHANGE (Llama); NEEDS A RUNNING SERVICE (Gufo) | probe P1 | llama-server b12613 does send it (`8083/v1/models`: `architecture.input_modalities: ["text"]`), but a Llama profile's `vision` and its `--mmproj` come from the same profile fields (`src/llama-args.ts:40`, `src/providers/local-openai.ts:41`), so they cannot disagree while the server runs; Gufo's `/v1/models` shape is unknown |
| 5 | typecheck config for `tests/` | BUILD | AAP-48 | no config includes `tests/` (`tsconfig.json` `include: ["src"]`); a trial on 2026-11-22 found 29 errors in 7 test files, all fixable without weakening an assertion |
| 6 | `completion_tokens`/`total_tokens` not guarded | BUILD | AAP-48 | `src/providers/local-openai.ts:235-237` (`?? 0`, `?? sum`), while prompt and cached go through `finiteOrZero` |
| 7 | "does not keep a cancelled turn" is flaky | BUILD (de-flake, assertions unchanged) | AAP-48 | the race: the test aborts after a fixed 250 ms (`tests/acp-provider.test.ts:191`); under load the abort lands while `generate` awaits the agent start (`src/acp-provider.ts:864-865`), before any session exists, so no `session/delete` is sent and the count is 0. Fix: abort once the fake agent logged `session/prompt` |
| 8 | Cartoon `kind-switch.ts` keeps its own free call and a stale comment | BUILD | CTS-58 | `src/engine/comfy/kind-switch.ts:18-22` copies `POST /free`; `freeMemory` (`client.ts:175-183`) is fixed since CTS-57 |
| 9a | VN: cap the `wait:` option of the other tools at 240 s | BUILD | VNO-72 | three `settle`s wait `opts.waitTimeoutMs ?? 10 * 60_000` (`src/engine/mcp/tools.ts:75-81`, `tools-import.ts:12-16`, `tools-plan.ts:17-21`) |
| 9b | VN: widen `stripTextNegations` | BUILD | VNO-72 | `src/engine/assets/derive.ts:37-47` splits on commas only; adds "without any text", "No text.", "no text and no signs", newline and `;` clauses; "no people", "no borders", "a shop sign with no text" stay (anchored pattern); "no text on the walls" left out on purpose |
| 9c | VN: `SLUG_RE` allows `--` | BUILD | VNO-72 | job ids are `<slug>--<task>--<scope>--r<n>`; `deleteProject` removes by the prefix `${slug}--` (`src/engine/vn/service.ts:801-811`), so deleting the non-existent `foo--vn.analyse` removes project `foo`'s analyse job files. No real slug has `--` (`asciiSlug`, `src/engine/vn/ids.ts:40-52`); the regex refuses it |
| 10 | the rest of the Strata sections of the live Scriptorium and VN `providers.md` | BUILD (live data step) | hub L1, L2 | diffs (read only, 2026-11-22): Scriptorium live `## Strata` (line 263) differs from the seed's (`seed/config/providers.md:255`) in 6 lines (pre-HUB-38 "Scriptorium only connects to it", old `D:\Strata\run-*.bat` paths); VN live (`:240`) from its seed (`:238`) in 5 lines. Both live files also lack whole seed sections (Scriptorium: "The ACP proxy", "OpenRouter", "DeepSeek", "Client provider"; VN: "Client", "ACP proxy"): question 1 |
| 11a | Pixel: New chat aborts a running MCP run | NO CHANGE (question 3) | - | real and by design: `chat.ts:133-141`, documented in the README (line 50); a change of what a button does is the user's call |
| 11b | Pixel: `openChat` races an MCP run | BUILD | PAR-24 | `agent.ts:179-181`: check, `await load`, set: a start during the load runs in the old chat |
| 11c | Pixel: `model: ""` ignores the chat's selection | BUILD | PAR-24 | `agentMcp.ts:299`; `checkAgentModel`/`resolveModel` use `??` (`llm.ts:400, 408-425`) |
| 11d | Pixel: local paths in MCP results | NO CHANGE | - | localhost server with a Host/Origin check (`src/main/mcp.ts:103,155-175`); export and save tools already return paths, which clients need |
| 11e | Pixel: `stoppedBy`/`timedOut` on a `completed` run | BUILD | PAR-24 | `agentMcp.ts:116-125, 177-185`: the flags are never cleared by a `completed` done |
| 11f | Pixel: stale turn-stack entry after a nested rollback | NO CHANGE (not reachable) | - | only `AgentRunner` begins and ends turns, once per run, one run at a time (`agent.ts:243,267,285`) |
| 11g | Pixel: back-to-back runs, `whenIdle()` during run 1's save | DONE ALREADY | PAR-23 | `agent.ts:195-201, 287-296`, test `tests/main/agent.test.ts:274` |
| 11h | Pixel: `before-quit` does not wait for the chat save | NO CHANGE | - | real only for a window closed mid-run (that run's chat is lost; the drawing is kept); window-only, needs Electron to test; headless already waits (`headless.ts:127`) |
| 11i | Pixel: `send()` assigns `current` after `execute` | NO CHANGE (not reachable) | - | `execute`'s first `await` (`agent.ts:233`) comes before anything could re-enter |
| 11j | Pixel: duplicate `turnError` line in a test | DONE ALREADY | - | one left (`tests/main/agent.test.ts:40`) |
| 12 | Pixel: slimmer tool list for JSON-action mode | TOO LARGE (unchanged); a small optional cut exists (question 2) | - | 71 tools, `jsonModeInstructions` 99,843 chars plus a 20,041-char guide that names 69 of them; every cut contradicts the guide. Optional cut: `agentToolSet: 'all' \| 'no-files'` in `config/app.json`, default `all` (`readAppSettings` fills defaults, `src/main/appSettings.ts:21`), dropping 12 file/export tools: 17,349 chars, about 4.3k tokens a step (14%). Whether that matters depends on Strata's prompt reuse, which K4 measures |
| 13 | Hub: stale locks cleared only after a kill; pid reuse | BUILD | hub H1 | every app already treats a dead pid as stale; what blocks is a live reused pid. The lock's own time decides it: VN's running engine started 14:38:13 UTC and wrote its lock at 14:38:16; a process that started after the lock's time cannot have written it. Today's locks (Edu 25460, Cartoon 10856, Pixel 32952, Scriptorium 19260) all have dead pids (last boot 11:22 UTC) |
| 14 | other pending lines | none | - | the nine `decision: pending` lines are 1-10 above; the older lines without a decision word were triaged in HUB-40 to HUB-42 (HUB-42 plan, row "older") |

## Tickets (ids checked 2026-11-22 in each `ROADMAP.md`, `.claude/tickets` and `git branch -a`)

| ticket | repo | branch | plan | order |
|---|---|---|---|---|
| AAP-48 | api-acp-proxy | `AAP-48_small-fixes` | `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-48-small-fixes\plan.md` | merge first |
| AAP-49 | api-acp-proxy | `AAP-49_monitor-second-cut` | `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-49-monitor-second-cut\plan.md` | cut from AAP-48's head, merged after it |
| VNO-72 | visual-novels-orchestrator | `VNO-72_negations-waits-slugs` | `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-72-negations-waits-slugs\plan.md` | any |
| CTS-58 | cartoon-studio | `CTS-58_kind-switch-free` | `C:\projects\Personal\cartoon-studio\.claude\tickets\CTS-58-kind-switch-free\plan.md` | any |
| PAR-24 | pixel-art-generator | `PAR-24_agent-run-edges` | `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-24-agent-run-edges\plan.md` | any |
| HUB-43 | creative-hub | `HUB-43_open-ideas` | this file | live steps and checks after all merges |

Last ids used before this plan: HUB-42, AAP-47, PAR-23, VNO-71, CTS-57. No item for Edu, Scriptorium, Book Translator, MIDI or Chiptune.

Notes every worker gets: the desktop proxy runs from api-acp-proxy's `dist/` and VN Studio from its repo's `out/`; both are RUNNING: no build on a branch in those repos, tests, typecheck and lint only. Pixel and Cartoon also run from `out/` (down today): no build on a branch either. The api-acp-proxy tree has two uncommitted AAP-43 files: leave them out of every commit. `%APPDATA%\api-acp-proxy\settings.json` is never edited by a build; no ticket adds a setting.

## Out of scope

- 1c (next proxy ticket), 1d and 4-Gufo (probe P1), 2a, 11a, 11d, 11f, 11h, 11i, 12 (question 2).
- Anything for "no text on the walls"; progress events for long waits; Pixel seed or live changes that make Strata Pixel's vision model (only if K3 passes, as its own ticket).
- Starting Scriptorium; any paid or cloud model; any book's `models:` map.

## Hub tasks (branch `HUB-43_open-ideas`)

The hub has no test suite. Line numbers are from master a2e0788; find each place by its text.

**H1 `scripts/hub.ps1`: a start clears a lock whose pid is gone or now belongs to another process (item 13).**
- `Clear-StaleLock($s)` (line 431) becomes `Clear-StaleLock($s, [switch]$AtStart)`:
  - Read the lock as JSON into `$lock`; `$lockPid = $lock.pid` (unreadable or non-numeric: the existing message, return). `$stamp = if ($lock.startedAt) { $lock.startedAt } elseif ($lock.started) { $lock.started }` (Scriptorium writes `started`, the others `startedAt`).
  - `Start-Sleep -Milliseconds 500` only when not `$AtStart` (after a kill, as today).
  - No process with that pid: remove and print `"$($s.id): removed its stale lock (pid $lockPid)"` (as today).
  - A process exists and `$AtStart`: `try { $began = $p.StartTime.ToUniversalTime() } catch { $began = $null }`; `$t = $null; if ($stamp) { try { $t = ([datetime]::Parse($stamp, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind)).ToUniversalTime() } catch { } }`. When both are known and `$began -gt $t.AddSeconds(5)`: remove and print `"$($s.id): removed its stale lock (pid $lockPid is now $($p.ProcessName), started after the lock)"`. Otherwise print `"$($s.id): lock $path held by running pid $lockPid ($($p.ProcessName)), left"`.
  - A process exists and not `$AtStart`: the existing "still held ... left" message.
  - It never removes a lock whose process started before the lock was written, so a running window app keeps its lock; a lock left by a shutdown or by a killed engine whose pid Windows gave to another program is removed.
- `Start-Service1`: inside `if ($s.managed) {` (line 390), before `New-Item -ItemType Directory -Force $logs`, add `Clear-StaleLock $s -AtStart`. The port check above it has already returned for a service that answers, so this runs only when the app is about to be started.
- `status` is unchanged (read-only).
- Header comment line 7 (`#   pwsh -File scripts\hub.ps1 start ...`): append "; a start first deletes the app's `lock` file when its pid is gone or started after the lock".
- `services.json` `_about`: after the `lock` sentence added in HUB-42, add "`hub.ps1 start` also deletes it before starting the app when its pid is gone or the process with that pid started after the lock's time (pid reuse)."
- Check: parse check `pwsh -NoProfile -Command "$null = [System.Management.Automation.Language.Parser]::ParseFile('scripts/hub.ps1', [ref]$null, [ref]$e); $e"` prints nothing; `node -e "JSON.parse(require('fs').readFileSync('services.json','utf8'))"`. Dry run that touches no app: copy the script to `.claude/temp/hub43/scripts/hub.ps1`; write `.claude/temp/hub43/server.js` (`require('http').createServer((q,r)=>r.end('ok')).listen(65014)`) and `.claude/temp/hub43/services.json` with one service `{ "id": "fake", "port": 65014, "managed": true, "repo": "<abs .claude/temp/hub43>", "data": "<abs .claude/temp/hub43/data>", "lock": "engine.lock", "start": { "kind": "exe", "path": "<abs path of node.exe from fnm>", "args": ["<abs server.js>"] } }` (copy any other top-level keys the script reads from the real file). Three runs of `pwsh -File .claude/temp/hub43/scripts/hub.ps1 start fake`, each followed by `... stop fake`: (a) `data\engine.lock` = `{"pid": 999999, "startedAt": "2026-11-22T00:00:00Z"}` -> "removed its stale lock (pid 999999)"; (b) start a background `node -e "setTimeout(()=>{},120000)"`, lock = `{"pid": <its pid>, "startedAt": "2026-01-01T00:00:00Z"}` -> "removed its stale lock (pid N is now node, started after the lock)"; (c) the same pid with `"startedAt"` = now plus one minute (ISO, UTC) -> "held by running pid N (node), left" and the file stays. Kill the background node; delete `.claude/temp/hub43`.

**H2 `ROADMAP.md`.** Row 36 after row 35 (line 47), same columns:
`| 36 | HUB-43 | The open ideas of REQ-0030 (proxy: tests typechecked, local usage guarded, a flaky test fixed, Monitor second cut with 60-second lines, thinking tokens, Strata's conversation cache and an outside server; VN: wider text-negation stripping, 240 s waits, no -- in slugs; Cartoon: kind switch uses freeMemory; Pixel: empty model, stop flags, openChat race; hub start clears stale and reused-pid locks; live Strata prose) (.claude/tickets/HUB-43-open-ideas/plan.md, REQ-0030) | api-acp-proxy (AAP-48, AAP-49), visual-novels-orchestrator (VNO-72), cartoon-studio (CTS-58), pixel-art-generator (PAR-24), hub | one round of rebuilds and live checks with HUB-42's, each with the user's go-ahead | Planned |`
The repo table's ACP proxy row (line 127): replace "AAP-46, AAP-47 for HUB-42" with "AAP-46, AAP-47 for HUB-42; AAP-48, AAP-49 for HUB-43".

Check for H1-H2: `git diff` shows only `scripts/hub.ps1`, `services.json`, `ROADMAP.md`; the H1 checks above.

## Live data steps (after the HUB-42 live worker has finished its L1-L5; each needs the user's go-ahead at run time; the hub does them)

Rules (as HUB-42): copy the file to `<file>.bak-HUB-43` first (older backups stay); prose only, found by its text; front matter untouched (SHA-256 of everything up to and including the second `---` line, same before and after); keep line endings and encoding (bytes as UTF-8, CR as the live file has it); a script that refuses unless the old text matches exactly once; verify with `git diff --no-index -U0 <file>.bak-HUB-43 <file>`. Record each step in `runs/hub-43-open-ideas.md`. Recompute every diff at run time (the HUB-42 worker edits these files today).

**L1 Scriptorium live `providers.md` (item 10).** Scriptorium down (`pwsh -File scripts\hub.ps1 status`; never start it). In `C:\Users\Infplane\Scriptorium\config\providers.md` (front matter ends at line 244 today) replace the `## Strata` section (from the line `## Strata` to the line before the next `## ` heading) with the seed's `## Strata` section of `C:\projects\Personal\scriptorium\seed\config\providers.md` copied as it is. On the user's yes to question 1 instead: the whole prose after the second `---` becomes the seed's prose. Verify: the changed region equals the seed's (CR stripped); show the diff in the run log.

**L2 VN live `providers.md` (item 10).** VN Studio may run (it reads the file on start; prose only). Same in `C:\Users\Infplane\VisualNovels\config\providers.md` (front matter ends at line 219) with `C:\projects\Personal\visual-novels-orchestrator\seed\config\providers.md`'s `## Strata` section, or the whole prose (question 1).

## Rebuilds and live checks, one merged list (after every repo ticket of HUB-42 and HUB-43 is merged; in this order; each step needs the user's go-ahead at run time)

GPU = loads a model; SVC = starts, stops or restarts a service. Local models only; no paid or cloud model, no Flow, no ElevenLabs, no Gemini. Record ids, times, tokens and results in `runs/hub-43-open-ideas.md` (HUB-42's K results also go there, with a line in `runs/hub-42-pending-ideas.md` pointing to it).

**R1 + K1 The proxy (HUB-42 K1, plus AAP-48 and AAP-49). SVC, GPU.** No local request in flight (`curl -s http://127.0.0.1:8787/healthz`: every provider `active` 0) and no app job running (VN `jobs\running` empty). SHA-256 of `%APPDATA%\api-acp-proxy\settings.json` first.
1. `cd C:\projects\Personal\api-acp-proxy` and `yarn build` (Bash: fnm PATH first). Brings AAP-44 to AAP-49 into the running app.
2. Restart: `pwsh -File scripts\hub.ps1 stop acp-proxy`, then `pwsh -File scripts\hub.ps1 start acp-proxy`. A Strata the proxy started stops with it; a Strata started outside the app keeps running and then shows as "started outside the app" (AAP-49): record which.
3. One local request (HUB-42 K1 step 3): `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, "Reply with the word OK.", `max_tokens` 50, `reasoning_effort` "none".
4. A person (or the worker with a screenshot) reads Monitor and About against AAP-47's list (HUB-42 K1 step 4: model ready, engine 0.1.52, context 131,072, images on, GPU, CPU, RAM, GPU load/VRAM/temperature/power, the engine request with prompt and reused tokens, the proxy request, base URL `http://127.0.0.1:8787/v1`, no key value) and AAP-49's: a line under GPU load, VRAM, GPU temp, Power, Disk read and Decode that moves between two screenshots 10 s apart; the Conversation cache tile shows numbers (or "off"); the Requests page and the Monitor's proxy table have a Thinking value for step 5's request.
5. One request with thinking: as step 3 with `reasoning_effort` "low" and `max_tokens` 300; record `usage.completion_tokens_details.reasoning_tokens` from the answer and the Thinking value shown.
6. Polling stops when hidden: not measurable from outside (HUB-42 K1 step 5); recorded as not measured.
7. An image to Strata (HUB-42 K1 step 6, AAP-46): a 64x64 PNG data URL; passes on HTTP 200.
Passes when every tile shows a value or an honest dash, the lines move, step 5 shows a Thinking count, step 7 is 200, and the settings file's SHA-256 is unchanged.

**R2 + K2 VN Studio (HUB-42 K2, plus VNO-72). SVC, GPU.** `pwsh -File scripts\hub.ps1 build vn-studio`; restart VN (stop, start) when no job runs. Then HUB-42 K2 unchanged in substance (throwaway project `hub42-signs-check`, market-street background with review on, `vno_asset_generate {only: [<bg id>], force: true}`, `vno_wait {timeoutSeconds: 240}`, read every regenerated prompt and look at each image, `vno_comfy_free {}`). Before the delete, VNO-72: `vno_delete_project {slug: "hub42-signs-check--vn.analyse", confirm: true}` returns an "invalid project slug" error and `VisualNovels\jobs\done` still holds the project's `hub42-signs-check--vn.*` files; then the real delete and the HUB-42 check that no `hub42-signs-check--*` job file is left. Passes when no regenerated prompt contains "no text", "no letters", "no signs", "no captions", "without any text" or a "No text." sentence, the bad slug is refused, and the job files are gone after the real delete.

**R3 + K3 + K4 Pixel (HUB-42 K3 and K4, plus PAR-24). SVC, GPU.** `pwsh -File scripts\hub.ps1 build pixel-studio` (brings PAR-23 and PAR-24). Then HUB-42 K3 unchanged (temp data folder `.claude\temp\hub42-pixel`, `vision: true` on the Strata row of the copy, a second headless Pixel on 7467, one artist run, record usage per step, stop and delete the temp folder) and HUB-42 K4 unchanged (two artist runs back to back, Pixel's `usage.cached` and Strata's `/metrics` `requests[].reused` per step, the Monitor's engine table). PAR-24: start K4's second run with `model: ""` and record that its result's `model` equals `list_models`' `selectedModel` (or `defaultModel` when none is selected).

**R4 Edu and Cartoon builds. No SVC.** `pwsh -File scripts\hub.ps1 build edu-studio cartoon-studio` (both down; brings EGS-75, CTS-57, CTS-58 into `out/`). No live check (UNTESTED until their next real ComfyUI job). Their next `hub.ps1 start` also exercises H1 on their dead-pid locks (Edu pid 25460, Cartoon 10856).

**K5 (optional, question 5) A Strata started outside the app (AAP-49). SVC, GPU.** After K4. On the proxy's Strata page press Stop and confirm the Monitor says "No local model loaded"; then `pwsh -File scripts\hub.ps1 start strata` (the proxy now holds no local model, so this follows the CLAUDE.md rule), wait for `curl http://127.0.0.1:8080/health` `loaded: true`; the Monitor shows Strata ready with "started outside the app" and its numbers; one request as K1 step 3 still answers. Leave Strata running.

**Probe P1 (NEEDS A RUNNING SERVICE, no go-ahead asked now): Gufo.** The next time the user loads a Gufo model through the proxy, read with GETs only: `curl -s -o - -w " %{http_code}" http://127.0.0.1:8081/health`, `/metrics`, `/v1/status`, `/props`, `/slots`, `/v1/models`; record each status code and JSON keys (and whether `/v1/models` has `architecture.input_modalities`). That decides 1d, 1e-Gufo and 4-Gufo.

## Acceptance criteria

| # | criterion | proof |
|---|---|---|
| H-1 | a hub start removes a lock whose pid is gone or reused, never a live writer's | H1 parse check and dry run (a), (b), (c) |
| H-2 | ROADMAP row 36 and the proxy repo row | `git diff ROADMAP.md` |
| H-3 | each repo ticket meets its own plan | the five repo plans |
| H-4 | L1 and L2 change only the listed prose | the `git diff --no-index` checks and the front-matter hashes |
| H-5 | the proxy's pages, old and new tiles, show honest values; thinking counts reach the lists; images reach Strata | R1 + K1 |
| H-6 | VN: no text negations in regenerated prompts; a `--` slug is refused; a deleted project leaves no job files | R2 + K2 |
| H-7 | Strata as Pixel's vision model and its prompt reuse, measured; an empty model uses the selection | R3 + K3 + K4 |
| H-8 | an outside Strata shows as such | K5 (optional) |

## UNTESTED (until the checks run)

- R1-R4 and K1-K5, each until the user says go; the proxy window (no Electron harness) until K1.
- H1 with a real app: the dry run uses a fake service; pid reuse cannot be produced on purpose with a real app.
- Cartoon's and Edu's `freeMemory` paths against a real ComfyUI (no check planned).
- 1c, 1d, 4-Gufo (next ticket, probe P1).

## Questions for the user (recommended answer first)

1. Live `providers.md` of Scriptorium and VN (L1, L2): only the `## Strata` section equal to the seed, or the whole prose equal to the seed? Recommended: the whole prose (front matter untouched, backups kept): the seed's Strata text points to "The ACP proxy" section that the live Scriptorium file lacks, and VN's live file also lacks the seed's Client and ACP proxy sections. Alternative: the Strata section only (the literal idea).
2. Pixel's slimmer tool list: wait for K4's prompt-reuse numbers? Recommended: wait; if K4 shows little reuse across steps, build the off-by-default `agentToolSet: 'no-files'` setting (about 4.3k tokens a step less) as its own ticket.
3. The Pixel window's New chat button stops a running MCP run (documented). Leave it? Recommended: leave it. Alternative: disable the button while a run goes (a one-line UI change).
4. llama-server `--metrics` (Llama speed on the Monitor): its own small proxy ticket after AAP-49? Recommended: yes (keeps AAP-49 at 13 files). Alternative: fold it into AAP-49 (15 files).
5. K5 (an outside Strata, one extra Strata reload of 1-3 minutes): run it at the end? Recommended: yes.
