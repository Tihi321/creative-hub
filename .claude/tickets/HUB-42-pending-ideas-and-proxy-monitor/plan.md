---
status: done
request: REQ-0030
repos: [creative-hub, api-acp-proxy, pixel-art-generator, visual-novels-orchestrator, edu-game-studio, cartoon-studio, scriptorium]
branch: HUB-42_pending-ideas-and-proxy-monitor
updated: 2026-11-22
---

# HUB-42 The pending extra ideas of REQ-0030, and a Monitor and About page in the ACP proxy app

The user said on 2026-11-22, word for word: "implemetn all pending ideas, and addd to scp proxy some of these strata pages, seems usefull to have some of these information" (two screenshots of Strata's own Monitor and About pages; "scp proxy" is the ACP proxy desktop app, repo `C:\projects\Personal\api-acp-proxy`).

Readings. Part A, the full one: every `decision: pending` line of `## Extra ideas` in `.claude/director/requests/REQ-0030-acp-for-all.md` (lines 185-202), the findings the director named (stale `engine.lock`, `vno_wait`, `vno_delete_project`) and the older lines, each checked against today's master. Part B, the narrow one (decided by the director): a read-only Monitor page and an About page for whichever local model the proxy holds; no chat; a tile only where an honest data source exists.

Every item was checked on 2026-11-22 against: creative-hub 457b735, api-acp-proxy ce7817f, pixel-art-generator 2e0d3fc, visual-novels-orchestrator 0f360c3, edu-game-studio be16f1b, cartoon-studio master, scriptorium b6071c9, and the live data folders (read only). Strata on 8080 and the embedding llama-server on 8083 were read with GETs only; no model was called.

## Triage (every pending idea, in file order)

P = REQ-0030 line 185-202 in order; E = a finding the director named; "older" = lines 137-184.

| # | idea (short) | verdict | ticket | reason (verified 2026-11-22) |
|---|---|---|---|---|
| P1 | Pixel seed `providers.md` "about 8000 tokens" | BUILD | PAR-23; hub L4 (live copy) | the sentence is at `seed/config/providers.md:296` (not 295) and in the live `PixelStudio\config\providers.md:307`; K1 of HUB-41 measured 34,292 tokens, more than the sentence's own "at least 32768" context |
| P2 | slimmer tool list for the JSON-action prompt | TOO LARGE | - | no switch exists: the agent gets the whole registry (`src/main/agent.ts:43`, `src/main/headless.ts:77`), and `jsonModeInstructions` (`src/llm/agent.ts:103-117`) prints every schema. Sketch: a per-task tool subset (drawing core: `draw_grid`, `set_pixels`, `fill`, `render_preview`, `read_grid`, palette tools) chosen by a setting `agent.tools: core | all`, with a `more_tools` action that loads the rest on demand; needs a tool catalogue, the prompt guide rewritten for the subset and a live quality check. Smallest useful cut: a fixed `core` list behind a setting, default `all`, and one K1-style run on `core` comparing steps and tokens |
| P3 | the agent never drops old preview images | NO CHANGE | - | previews are attached only for a `vision` model (`src/main/agent.ts:244`; otherwise `IMAGE_OMITTED` text, `src/llm/agent.ts:136-149`); Pixel has no vision model today, so no image is ever in the history. It matters only if K3 passes, and then belongs to that follow-up |
| P4 | Edu `freeMemory` empty-body bug; Cartoon unchecked | BUILD | EGS-75, CTS-57 | Edu `src/engine/comfy/client.ts:174-182` and Cartoon `src/engine/comfy/client.ts:175-181` both parse ComfyUI's empty 200 with `fetchJson`; VN's fix (VNO-70, `client.ts:174-183`) is copied as it is |
| P5 | live Scriptorium `roles.md` lines 79, 82-85 pre-HUB-38 | BUILD | hub L1 | the live prose differs from the seed in lines 79, 81-85 and 88 only (diff of the prose after the second `---`); the live front matter already says `paid`, `acp`, the archivist on Hydrogen, the humanizer on DeepSeek, so the seed's prose is the right text |
| P6 | live `providers.md` of VN, Edu, Pixel, Chiptune keep the nomic/LM Studio sentence | BUILD (VN, Edu); NO CHANGE (Pixel, Chiptune) | hub L3 | VN live `:247` and Edu live `:300` carry it; Pixel's and Chiptune's live files have no such sentence (grep "nomic" finds only `discover_skip`). VN and Edu will not refresh the file themselves: its hash differs from `.seed-hashes.json`, so the seed refresh keeps it |
| P7 | proxy `applyFix` leaves `hf.mmproj` / `hf.draft` stale | BUILD | AAP-46 | `src/renderer/llama-models.ts:72-80`; no code reads `hf.mmproj`/`hf.draft` today (only `repo`, `revision`, `quant`, `llama-view.ts:396-398`), so the effect is cosmetic, but the fix is three lines and turns AAP-45's code-read check P2 into an assertion |
| P8 | HUB-38 `changelog.md` omits piece 31's checks | BUILD | hub H1 | REQ-0030 `## Pieces` row 31 (line 68): VN, Cartoon, Edu probes PASS; Book Translator chunk PASS (17 s, cost 0); model lists PASS; Scriptorium probe and Pixel artist UNTESTED there (the probe passed later, Log line 236; the Pixel artist passed in HUB-41 K1) |
| P9 | `reindexLibrary` could print which files it re-embedded | BUILD | SCP-68 | `src/engine/cli.ts:78-92` prints counts only; `reindex()` (`src/engine/memory/index.ts:316-333`) knows each file |
| P10 | stale `Scriptorium\index\engine.lock` (pid 19260) | NO CHANGE in Scriptorium; BUILD hub H2 | hub H2 | written only by the long-running engine (`src/engine/index.ts:78`); a dead pid and a lock from before the last boot are already stale at the next start (`src/engine/store/dataFolder.ts:154-165`, tested in `tests/mcp.test.ts:322-336`); harmless. It was left by the PC shutdown. H2 removes such locks after a hub stop |
| P11 | live Scriptorium `providers.md:86` says embeddings come from LM Studio | BUILD (line 270, not 86) | hub L2 | live line 86 is a model row; the stale sentence is live `:270` "keep only the nomic embedding model loaded in LM Studio"; the seed's `:262` replaces it one to one |
| P12 | Pixel: permanent test "busy while a run is saving" | BUILD | PAR-23 | no test exists (`tests/main/agentMcp.test.ts` has 3 tests); the risk is real: a second `start_agent_run` during the save would reset the chat under a pending save (`src/main/agent.ts:283-284`, guard `agentMcp.ts:278-282`) |
| P13 | Pixel: headless shutdown also waits for the last run's chat save and `done` | BUILD | PAR-23 | `stopAgent` (`src/main/headless.ts:129-134`) awaits `whenIdle()`, which ends when `current` is null, set before `await this.save(convo)` (`agent.ts:283`): a stop can end the process before the chat is saved. A real bug, not only a test gap |
| P14 | Pixel: node test of the window view sync with a fake `window.pixelStudio` | BUILD | PAR-23 | `src/renderer/state/chat.ts:186,195-198` has no test and no other check reaches it (the window was UNTESTED in HUB-41) |
| P15 | Pixel: test of the second busy check after the model check | NO CHANGE (dropped by test-discipline) | - | the same guard family as P12 (a run must not start while another holds the chat); the race needs a slow `checkAgentModel` and another send in between; P12 already pins the guard's behaviour |
| P16 | Strata as Pixel's vision model | NEEDS A RUNNING SERVICE (K3), after AAP-46 | AAP-46, hub K3 | a config flip would fail today: the proxy refuses images for Strata, because Strata has no profile and `prepareModel` accepts images only for a vision profile (`src/providers/local-openai.ts:149`; `acceptsImages` `:127`). Strata says it takes images (`/health` `images: true`; `/v1/models` `architecture.input_modalities: ["text","image"]`). AAP-46 reads that flag; K3 then runs one artist run with `vision: true` in a temp data folder. The seed/live change follows only if K3 passes, as its own ticket |
| P17 | Pixel's JSON-action prompt resends about 34k uncached tokens per step | BUILD (the proxy part); measure (K3/K4) | AAP-46, hub K4 | "0 cached" is at least partly the proxy's doing: Strata reports `usage.prompt_tokens_details.cached_tokens` (its `terminal/serve/server.py:6184` sets it from `reused`), but the proxy keeps only `prompt_tokens`, `completion_tokens` and reasoning (`local-openai.ts:221,232`), so Pixel always sees 0. Pixel's own order is stable inside a run (the system string is built once, `src/main/agent.ts:232`); across runs the `## Current document` block sits before the tool list (`agent.ts:324-348`, `llm/agent.ts:307`), which breaks a shared prefix. The reorder waits for K4's numbers (Question 4) |
| P18 | VN: the regenerated background keeps drawing lettered signs | BUILD | VNO-71; hub K2 | the critic's `revisedPrompt` replaces the positive prompt unchanged (`src/engine/vn/handlers.ts:596-598`), and the critic writes "no text, no letters, no signs" into it, which names the thing to Qwen-Image. Backgrounds already get a negative "text, letters, words, ..." (`src/engine/assets/derive.ts:34,318-321`), but qwen-image-2.1 runs at cfg 1 (`src/engine/comfy/graphs.ts:392`), where ComfyUI ignores the negative |
| E1 | stale `engine.lock` after a headless stop (Pixel, Edu; also Cartoon) | BUILD (hub); NO CHANGE (apps) | hub H2 | cause per app is the same: `hub.ps1 stop` ends with `taskkill /T /F` (`scripts/hub.ps1:463`), so no SIGTERM, `before-quit` or release runs. Every app already treats a dead pid as stale (Pixel `src/main/engineLock.ts:42-45`; VN, Edu, Cartoon `src/engine/store/lock.ts:38-45,87-92`). The real hazard is pid reuse (VN `ROADMAP.md` records a lock whose pid Windows gave to `msedgewebview2`). H2 deletes the lock right after the kill when its pid is dead |
| E2 | `vno_wait` cut at 300 s by the MCP idle limit | BUILD | VNO-71 | `src/engine/mcp/tools.ts:341-349`, default 600 s, no maximum, no progress support anywhere (`mcp/server.ts:34` drops `extra`). Smallest: clamp to 240 s and say so; progress events are a larger change |
| E3 | `vno_delete_project` leaves job files | BUILD | VNO-71 | `src/engine/vn/service.ts:800-807` removes only `queued` jobs of the slug |
| older 183 | one review built to be rejected | DONE ALREADY | HUB-41 K2 | three rejections on Inkling, notes in English (`runs/hub-41-pixel-agent.md`) |
| older 137-184 | the HUB-38-era lines and the HUB-39/40/41 "decision: build" lines | DONE ALREADY or closed | HUB-40, HUB-41 | HUB-40 triaged lines 137-170 (27 built; 9, 15, 28, 29 NO CHANGE); its NEEDS USER items were closed since: 16 by PAR-22, 26 by N2 (plain re-index), 34 by N3, 32 (Pixel) by PAR-21. Lines 171-184 were built in HUB-40/HUB-41 and checked PASS |

## Tickets (ids checked 2026-11-22 in each `ROADMAP.md`, `.claude/tickets`, `git branch -a`)

| ticket | repo | branch | plan | depends on |
|---|---|---|---|---|
| AAP-46 | api-acp-proxy | `AAP-46_strata-vision-and-cache` | `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-46-strata-vision-and-cache\plan.md` | none |
| AAP-47 | api-acp-proxy | `AAP-47_monitor-about` | `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-47-monitor-about\plan.md` | AAP-46 merged first (both add a ROADMAP and README line) |
| PAR-23 | pixel-art-generator | `PAR-23_agent-tests-and-prose` | `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-23-agent-tests-and-prose\plan.md` | none |
| VNO-71 | visual-novels-orchestrator | `VNO-71_signs-wait-delete` | `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-71-signs-wait-delete\plan.md` | none |
| EGS-75 | edu-game-studio | `EGS-75_comfy-free` | `C:\projects\Personal\edu-game-studio\.claude\tickets\EGS-75-comfy-free\plan.md` | none |
| CTS-57 | cartoon-studio | `CTS-57_comfy-free` | `C:\projects\Personal\cartoon-studio\.claude\tickets\CTS-57-comfy-free\plan.md` | none |
| SCP-68 | scriptorium | `SCP-68_reindex-files` | `C:\projects\Personal\scriptorium\.claude\tickets\SCP-68-reindex-files\plan.md` | none (never start Scriptorium) |
| HUB-42 | creative-hub | `HUB-42_pending-ideas-and-proxy-monitor` | this file | L and K: the repo tickets merged |

Last ids used before this plan: HUB-41, AAP-45, PAR-22, VNO-70, EGS-74, CTS-56, SCP-67 (no Book Translator or Chiptune item). The proxy's working tree has two uncommitted files of AAP-43 (`events.jsonl`, `plan.md`): leave them out of every commit.

The desktop proxy the hub starts runs from api-acp-proxy's `dist/` and is running now. AAP-46 and AAP-47 workers run `yarn test` and `yarn typecheck` only; `yarn build` (which writes `dist/`) runs in K1 after the merge, with the user's go-ahead.

## Out of scope

- P2 (TOO LARGE), P3, P15; any Pixel seed or live change that makes Strata Pixel's vision model (a follow-up ticket only if K3 passes); Pixel's prompt reorder (Question 4).
- Progress notifications for `vno_wait`; a stricter lock check (process start time) in the apps.
- Reasoning tokens in the activity log, sparklines and history, llama-server `--metrics`, Gufo engine status (AAP-47's second cut, listed there).
- `%APPDATA%\api-acp-proxy\settings.json`, any book's `models:` map, starting Scriptorium, any paid or cloud model.

## Hub tasks (branch `HUB-42_pending-ideas-and-proxy-monitor`)

The hub has no test suite. Line numbers are from master 457b735; find each place by its text.

**H1 `.claude/tickets/HUB-38-acp-for-all/changelog.md` (P8), facts only.** After the four bullets under "Verification recorded as passed in the Log:" (after the line starting "- Test counts of the repo workers:") add:
```
- REQ-0030 piece 31 (app-level live checks, `## Pieces` row 31): VN, Cartoon and Edu probes PASS; Book Translator chunk PASS (17 s, cost 0); model lists PASS. In that piece the Scriptorium probe was UNTESTED (the worker session's permission check denied the command) and passed later (the Scriptorium CLI probe above, Log 2026-11-21 21:00); the Pixel artist request was UNTESTED (reachable only from the window chat then) and passed in HUB-41 K1 over MCP (`runs/hub-41-pixel-agent.md`).
```
And the UNTESTED line: old "UNTESTED: every live check the Log does not mark as passed (the Log states "every live check is UNTESTED" on 2026-11-21 and then records only C1, C4, C9 and the Scriptorium probe as passed)." new "UNTESTED: every live check the Log and piece 31 do not mark as passed (the Log states "every live check is UNTESTED" on 2026-11-21 and then records C1, C4, C9 and the Scriptorium probe as passed; piece 31 adds the VN, Cartoon and Edu probes, the Book Translator chunk and the model lists)."

**H2 `scripts/hub.ps1` and `services.json`: a hub stop removes a lock it left (E1, P10).**
- `services.json`: add `"lock": "<path relative to data>"` to five entries, after `"data"`: `scriptorium` `"index\\engine.lock"`, `vn-studio` `"engine.lock"`, `edu-studio` `"engine.lock"`, `cartoon-studio` `"state\\engine.lock"`, `pixel-studio` `"engine.lock"`. Extend `_about` (line 2): after "To add a tool: ..." add "`lock` (optional) is the app's engine lock file under `data`; `hub.ps1 stop` deletes it after the kill when its pid is no longer running."
- `scripts/hub.ps1` `Stop-Service1` (line 429): after `Write-Host "$($s.id): stopped (pid $rootId)"` (line 464) call a new function `Clear-StaleLock $s`, defined above `Stop-Service1`:
  - no `$s.lock` or no `$s.data`: return; path = `Join-Path (Expand $s.data) $s.lock` (`Expand`, `scripts/hub.ps1:41`, replaces a leading `~` with `$HOME`).
  - file missing: return. Read it as JSON; no numeric `pid`: print `"$($s.id): lock $path unreadable, left"` and return.
  - `Start-Sleep -Milliseconds 500`, then if `Get-Process -Id $pid -ErrorAction SilentlyContinue` finds nothing: `Remove-Item $path` and print `"$($s.id): removed its stale lock (pid $pid)"`; else print `"$($s.id): lock $path still held by pid $pid, left"`.
  - It never deletes a lock whose pid runs, so a window app that took over is safe.
- Header comment line 13 (`#   pwsh -File scripts\hub.ps1 stop [ids|all] ...`): append "; deletes the app's `lock` file (services.json) when its pid is gone".
- Check: parse check `pwsh -NoProfile -Command "$null = [System.Management.Automation.Language.Parser]::ParseFile('scripts/hub.ps1', [ref]$null, [ref]$e); $e"` prints nothing; `node -e "JSON.parse(require('fs').readFileSync('services.json','utf8'))"` (Bash: `export PATH="/c/Users/Infplane/AppData/Roaming/fnm/aliases/default:$PATH"` first). Dry run that touches no app: copy the script to `.claude/temp/hub42/scripts/hub.ps1`, write `.claude/temp/hub42/services.json` with one managed service `{ "id": "fake", "port": 65013, "managed": true, "data": "C:\\projects\\Personal\\creative-hub\\.claude\\temp\\hub42\\data", "lock": "engine.lock", "start": { "kind": "none" } }`; start a listener on 65013 with `node -e "require('http').createServer((q,r)=>r.end('ok')).listen(65013)"` (background), write `data\engine.lock` as `{"pid": <that node pid>}`, run `pwsh -File .claude/temp/hub42/scripts/hub.ps1 stop fake`. Expected: "fake: stopped (pid N)", then "fake: removed its stale lock (pid N)", and the file is gone. Delete `.claude/temp/hub42` afterwards.

**H3 `ROADMAP.md`: row 35** after row 34 (line 46), same columns:
`| 35 | HUB-42 | The pending extra ideas of REQ-0030 (proxy takes images and reports cached tokens for Strata, Pixel agent tests and shutdown, VN background signs, vno_wait cap, vno_delete_project job files, ComfyUI free in Edu and Cartoon, reindex file list, hub stop clears stale locks, live prose) and a Monitor and About page in the ACP proxy app (.claude/tickets/HUB-42-pending-ideas-and-proxy-monitor/plan.md, REQ-0030) | api-acp-proxy (AAP-46, AAP-47), pixel-art-generator (PAR-23), visual-novels-orchestrator (VNO-71), edu-game-studio (EGS-75), cartoon-studio (CTS-57), scriptorium (SCP-68), hub | GPU checks and the proxy restart with the user's go-ahead | Planned |`
Also the repo table's ACP proxy row (`ROADMAP.md` about line 125, "AAP-42, AAP-43 for HUB-38; local-model follow-ups ..."): replace "AAP-42, AAP-43 for HUB-38" with "AAP-42, AAP-43 for HUB-38; AAP-44, AAP-45 for HUB-40/41; AAP-46, AAP-47 for HUB-42".

**H4 `README.md:46`, the `acp-proxy` row of the tools table**: in its second cell, after "per-provider cap (AAP-25): codex 4, antigravity 3" add "; its desktop app has a Monitor and an About page for the loaded local model (AAP-47)". Only after AAP-47 is merged.

Check for H1-H4: `git diff` shows only these files; `services.json` parses; the H2 dry run output as above.

## Live data steps (after the repo tickets merge; each needs the user's go-ahead at run time; the hub does them)

Rules for all: copy the file to `<file>.bak-HUB-42` first (older `.bak-HUB-*` stay); change only the listed prose; find each place by its text; front matter untouched (SHA-256 of everything up to and including the second `---` line, same before and after); keep line endings and encoding (read and write bytes as UTF-8, as `runs/hub-41-pixel-agent.md` L1-L3 did with a script that refuses unless exactly one line matches); verify with `git diff --no-index -U0 <file>.bak-HUB-42 <file>`. Record each step in `runs/hub-42-pending-ideas.md`.

**L1 Scriptorium live `roles.md` prose (P5).** Scriptorium down (`pwsh -File scripts\hub.ps1 status`; never start it) and no worker using `C:\Users\Infplane\Scriptorium`. In `C:\Users\Infplane\Scriptorium\config\roles.md` replace, each by the matching text of `C:\projects\Personal\scriptorium\seed\config\roles.md` copied as it is:
- line 79 "The aliases `paid`, `strata` and `lmstudio` stand for ..." by seed line 44 "The aliases `paid` and `acp` stand for ...";
- lines 81-85 (from "Starting choices, all of them first guesses to be tuned in the model picker:" to the line starting "- Archivist (2026-11-13): Gemini 4 Hydrogen ...") by seed lines 46-50 (from "Starting choices, ... Since HUB-38 every local model is reached through the ACP proxy; ..." to the line starting "- Researcher and the checks ...");
- line 88 "Reviewer jobs prefer a model family ... Changing a default here applies from the next job. ..." by the seed's matching line ("... applies at once: a running job asks its current request again on the new model. `fallback_shared` ...").
Verify: the prose after the second `---` (CR stripped) equals the seed's; the diff touches lines 79-88 only. This drops the live line about the archivist's 2026-11-13 Hydrogen trial (its measurement stays in the `.bak-HUB-42`); see Question 1.

**L2 Scriptorium live `providers.md:270` (P11).** Same preconditions as L1. Old: "- Strata takes most of the GPU memory with any model: keep only the nomic embedding model loaded in LM Studio while it runs." New (seed `providers.md:262`): "- Strata takes most of the GPU memory with any of these models: no ComfyUI while it runs. The proxy's small nomic embedding server (port 8083) runs beside it." Verify: `@@ -270 +270 @@` only. The rest of that live Strata section is older than the seed; it is left (not asked).

**L3 VN and Edu live `providers.md` (P6).** VN Studio and Edu Studio may run (they read `providers.md` on start; prose only). `C:\Users\Infplane\VisualNovels\config\providers.md:247`, old "- Strata takes most of the GPU memory with any model: keep only the nomic embedding model loaded in LM Studio while it runs." new (VN seed `:245`) "- Strata takes most of the GPU memory with any of these models: no ComfyUI while it runs. Only one local model is on the GPU at a time (gufo, strata and llama through the proxy included)." `C:\Users\Infplane\EduGames\config\providers.md:300`, the same old line, new (Edu seed `:296`) "- Strata takes most of the GPU memory with any of these models: no ComfyUI while it runs." Verify: one changed line in each file.

**L4 Pixel live `providers.md:307` (P1), after PAR-23 is merged.** Pixel Studio down (if it runs, stopping it is a service stop: go-ahead). In `C:\Users\Infplane\PixelStudio\config\providers.md` the line starting "Tool calling works best with models that were trained for it" becomes PAR-23's new seed line (`seed/config/providers.md:296` after the merge), copied as it is. Verify: one changed line, equal to the seed's.

**L5 (only on the user's yes to Question 2) Scriptorium live `settings.md` prose.** Same preconditions as L1. The live prose (after the second `---`) differs from `C:\projects\Personal\scriptorium\seed\config\settings.md` in: file lines 31 (`fallbacks` is the list ... "API, API, LM Studio, API" ... "(`strata`, `lmstudio`, `client` ...)"), 33 (kinds "`strata` the first Strata row, `lmstudio-2` the second LM Studio row"), 35 ("the three below"), 36 (`fallback_shared`: "the checks name Strata's `-low` model"), the example row `  - lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic   # lmstudio` (line 42) and 48 (`last_resort_model`: "a Strata that is not running"); the seed also has a `## Byline` section the live file lacks and one blank line fewer after the H1. Replace the prose after the second `---` with the seed's prose (byte for byte, CR as the live file has it). Verify: front matter hash unchanged; prose (CR stripped) equals the seed's.

## Live checks (each needs the user's go-ahead; local models only; no paid or cloud model, no Flow, no ElevenLabs, no Gemini)

GPU = loads a model; SVC = starts, stops or restarts a service. Record ids, times, tokens and results in `runs/hub-42-pending-ideas.md`.

**K1 The proxy's Monitor and About pages (AAP-46, AAP-47). SVC, GPU.** After both are merged. No local request may be in flight (`curl -s http://127.0.0.1:8787/healthz`: every provider `active` 0) and no app job running (VN `jobs\running` empty).
1. `cd C:\projects\Personal\api-acp-proxy` and `yarn build` (Bash: fnm PATH first). This also brings in AAP-44 and AAP-45, which the running proxy does not have yet.
2. Restart the desktop proxy: `pwsh -File scripts\hub.ps1 stop acp-proxy`, then `pwsh -File scripts\hub.ps1 start acp-proxy` (Strata stops with it; the first local request loads it again, about 60 s).
3. One local request: `curl -s http://127.0.0.1:8787/v1/chat/completions -H "content-type: application/json" -d "{\"model\":\"strata/qwen3.8-flash-next-unsloth-ud-iq4_xs\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the word OK.\"}],\"max_tokens\":50,\"reasoning_effort\":\"none\"}"` (add the bearer header only if `server.apiKey` is set).
4. The user (or the worker with a screenshot of the window) opens Monitor and About and reads each tile against AAP-47's acceptance list: model `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` ready, engine 0.1.52, context 131,072, images on, GPU name, CPU, RAM, GPU load/VRAM/temperature/power numbers, the engine request with prompt and reused tokens, the proxy request in the recent list, OpenAI base URL `http://127.0.0.1:8787/v1`, no key value anywhere.
5. Polling stops while the page is hidden: no outside evidence exists (Strata does not log `/metrics` reads and AAP-47 logs none), so this stays proven by AAP-47's code and its review only; record it as not measured.
6. Repeat 3 with an image (AAP-46): a 64x64 PNG in a data URL; passes when the answer is HTTP 200 (before AAP-46 it was 400 `unsupported_content`).
Passes when every tile in step 4 shows a value or an honest dash, step 6 is 200 and `%APPDATA%\api-acp-proxy\settings.json` has the same SHA-256 before and after.

**K2 VN background without lettered signs (P18, VNO-71). GPU, SVC.** After VNO-71 is merged and `pwsh -File scripts\hub.ps1 build vn-studio` ran; VN restarted (go-ahead) when no job runs. Like HUB-41 K2: a throwaway project `hub42-signs-check` (`vno_create_project`, one place "Market street", looks "a narrow street of old shop fronts with awnings", `settings.art.review: true`), `vno_asset_set` the background prompt "A narrow market street with old shop fronts and awnings at noon, anime visual novel background", `vno_asset_generate {only: [<bg id>], force: true}`, then `vno_wait {timeoutSeconds: 240}` until done. Read the review job log, every regenerated prompt in `assets.json` (`prompt` after each rejection) and look at each image. `vno_comfy_free {}`; delete the project (`vno_delete_project {slug, confirm: true}`) and check that `VisualNovels\jobs\{queued,running,done,failed}` hold no `hub42-signs-check--*` file (VNO-71's delete fix). Passes when: no regenerated prompt contains "no text", "no letters", "no signs" or "no captions" (the sanitiser), and the job files are gone. Record (not pass/fail) how many images had lettering and the verdicts; Inkling may still reject for other reasons.

**K3 Strata as Pixel's vision model, one run (P16). GPU, SVC.** After AAP-46 is merged and K1 ran (the proxy now passes images to Strata). Pixel's real data folder is not touched.
1. Make a temp data folder: copy `C:\Users\Infplane\PixelStudio\config` to `C:\projects\Personal\creative-hub\.claude\temp\hub42-pixel\config`. In the copy's `providers.md`, on the `acp` row `id: strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` (live line 155-159), add `vision: true`.
2. If PAR-23 was merged since the last Pixel build, `pwsh -File scripts\hub.ps1 build pixel-studio` first. Start a second headless Pixel on another port with that folder: in `C:\projects\Personal\pixel-art-generator`, PowerShell `$env:PIXEL_STUDIO_HOME='C:\projects\Personal\creative-hub\.claude\temp\hub42-pixel'; $env:PIXEL_STUDIO_MCP_PORT='7467'; npx electron . --mcp-only` (background; the real Pixel on 7457 stays down). Check that 7467 answers.
3. Over MCP on `http://127.0.0.1:7467/mcp` (the session's `pixel-studio` server points at 7457, so use JSON-RPC over HTTP: `initialize`, then `tools/call`; the same tools as HUB-41 K1): `list_models` (the Strata model shows `vision: true`), `new_document {16,16,"hub42-vision","pico-8"}`, `start_agent_run` with HUB-41 K1's mushroom text, `get_agent_run` every 60 s until done.
4. Record: state, steps, wall time, per-step `usage` (input, cached, output), whether the step after a drawing tool grew by an image's worth of tokens (the sign that the preview reached the model; HUB-41 K1 grew by only 126 tokens), whether the model's reply refers to what it saw, cost 0. Compare with HUB-41 K1 (4 steps, 87.5 s, 138,782 tokens in).
5. Stop the temp Pixel (kill the process started in 2), delete `.claude\temp\hub42-pixel`.
Passes when the run ends `completed` with at least one preview image in the model's input and no 4xx. Only then: write a follow-up idea "Pixel's Strata row `vision: true` in seed and live, with a migration" (not built here). Fails or too slow (more than three times K1's wall time): record it; Pixel stays without a vision model.

**K4 Prompt reuse on Strata (P17). GPU.** Run together with K3 (same session) and once more with `vision` false (the copy's row without `vision: true`, or the real Pixel): two artist runs back to back with the same text. Record per step Pixel's `usage.cached` (now passed through by AAP-46) and Strata's own `GET http://127.0.0.1:8080/metrics` `requests[].reused` and `prompt_tokens`, and the Monitor's engine table (K1). Result decides Question 4: inside a run, steps 2+ should reuse most of the prompt; across runs, the first step's reuse shows whether the `## Current document` block breaks the shared prefix.

## Acceptance criteria

| # | criterion | proof |
|---|---|---|
| H-1 | HUB-38 changelog records piece 31 | `git diff .claude/tickets/HUB-38-acp-for-all/changelog.md` against REQ-0030 line 68 and Log 236 |
| H-2 | a hub stop deletes the app's lock when its pid is gone, never a live one | H2 parse check and dry run |
| H-3 | ROADMAP row 35 and the proxy repo row; README row after AAP-47 | `git diff ROADMAP.md README.md` |
| H-4 | each repo ticket meets its own plan | the seven repo plans |
| H-5 | L1-L4 (L5 if asked) change only the listed prose | the `git diff --no-index` checks |
| H-6 | the Monitor and About pages show the loaded model honestly; images reach Strata | K1 |
| H-7 | VN no longer writes "no signs" into a regenerated prompt; a deleted project leaves no job files | K2 |
| H-8 | whether Strata can be Pixel's vision model, measured | K3 |
| H-9 | whether Strata reuses Pixel's prompt, measured | K4 |

## UNTESTED (until the checks run)

- K1-K4, each until the user says go. The proxy pages are UNTESTED until K1 (no Electron test harness exists).
- L1-L5 in the running apps (Scriptorium is not started by this plan).
- E1 with a real app: H2's dry run uses a fake service; the first real `hub.ps1 stop` of Pixel, Edu, VN or Cartoon proves it.
- Edu's and Cartoon's `freeMemory` against a real ComfyUI (only VN's was live-checked, HUB-41 K2).

## Questions for the user (recommended answer first)

1. Scriptorium's live `roles.md` prose (L1): make it equal to the seed, which drops the live line about the archivist's 2026-11-13 Hydrogen trial (the line is kept in the `.bak-HUB-42`)? Recommended: yes, equal to the seed (the seed's line already says the archivist tries Hydrogen first). Alternative: keep that line and only change its "then Strata low, LM Studio, paid" to "then the local Strata model, then paid".
2. Scriptorium's live `settings.md` has the same stale prose (`strata` / `lmstudio` kinds, Strata's `-low` model) that HUB-41 L3 fixed in Edu: add it as L5? Recommended: yes (same rules, prose only).
3. K3 runs Pixel's artist on Strata with images through the proxy (after AAP-46) in a temp data folder on port 7467. Recommended: yes, through the proxy. Alternative: point the temp copy straight at Strata's 8080 without AAP-46: not recommended, it bypasses the proxy's one-model-at-a-time coordinator.
4. Pixel's prompt order (the document block before the tool list breaks a shared prefix across runs): wait for K4's numbers before changing it? Recommended: wait; build the reorder only if K4 shows good reuse inside a run and little across runs.
5. The proxy rebuild and restart in K1 (which also brings AAP-44 and AAP-45 into the running app): done by the hub worker with your go-ahead when no local request runs? Recommended: yes. Alternative: you rebuild and restart it yourself.
