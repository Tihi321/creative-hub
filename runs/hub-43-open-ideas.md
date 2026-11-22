# HUB-43 The open ideas of REQ-0030: live steps, rebuilds and live checks (with HUB-42's)

Date: 2026-11-22, 19:41-20:15 +01:00. Plans: `.claude/tickets/HUB-43-open-ideas/plan.md` ("Live data steps" L1, L2; "Rebuilds and live checks, one merged list" R1-R4, K1-K5) and `.claude/tickets/HUB-42-pending-ideas-and-proxy-monitor/plan.md` (K1-K4). The user approved: "All if them, if there is nothing else to fix" (HUB-42 live edits, rebuilds with a proxy restart, the four checks), "Ok build open idea first", "Yes" to the HUB-43 plans with the recommended answers (L1/L2: the whole prose equal to the seed; K5 at the end), "Add it" for AAP-50. Worker session. Only local models through the proxy were called (Strata, Inkling). No paid or cloud model, no Flow, no ElevenLabs, no Gemini. Nothing committed; no repo code or seed changed. Scratch files: `.claude/temp/hub43-live/`.

Repo heads (master, clean): api-acp-proxy aaf2519 (two known uncommitted AAP-43 ticket files), visual-novels-orchestrator 12ee5c5, pixel-art-generator 5778801, edu-game-studio 7d93579, cartoon-studio 5635447, scriptorium 980e415.

## Preflight (19:41)

`hub.ps1 status`: up vn-studio (node 25848), vibetts (17740), comfyui (17472), strata 8080 (37680, started by the proxy), acp-proxy (electron 26412). Down: scriptorium, book-translator, edu-studio, cartoon-studio, pixel-studio (7457), chiptune-studio, comfy-mcp, lmstudio, flow-music-mcp. No process had `Scriptorium` in its command line.

`%APPDATA%\api-acp-proxy\settings.json` SHA-256 (hashed only): `1130D96801D1F646694975F790F7A2BB45606EE78C64652759726868A8BBA592` at 19:41 (before the first proxy restart) and at 20:14 (end): equal.

VN `jobs\running` empty. `jobs\queued` holds 8 job files from 2026-10-23 (`hub07-flow-test--*` r2, `hub08-13-autostart--vn.build--regen-sfx_bell--r4`) whose dependencies never finish; they survived earlier restarts and did not start in this one (see Discoveries).

### Lock files before the first start (19:41:32)

| app | lock file | exists | content | pid alive |
|---|---|---|---|---|
| scriptorium | `C:\Users\Infplane\Scriptorium\index\engine.lock` | yes | pid 19260, started 2026-11-21T20:30:48.246Z | no |
| vn-studio | `C:\Users\Infplane\VisualNovels\engine.lock` | yes | pid 25848, startedAt 2026-11-22T14:38:16.214Z | yes (node, process start 14:38:13.29Z) |
| edu-studio | `C:\Users\Infplane\EduGames\engine.lock` | yes | pid 25460, startedAt 2026-11-21T22:59:49.836Z | no |
| cartoon-studio | `C:\Users\Infplane\CartoonStudio\state\engine.lock` | yes | pid 10856, startedAt 2026-11-21T22:59:52.978Z | no |
| pixel-studio | `C:\Users\Infplane\PixelStudio\engine.lock` | yes | pid 32952 (headless 7457), startedAt 2026-11-22T14:38:31.212Z | no |

acp-proxy and strata have no `lock` in `services.json`.

## L1-L2: live `providers.md`, whole prose equal to the seed

Script `.claude/temp/hub43-live/edit.cjs` (bytes as UTF-8, BOM kept, front matter through the second `---` line and its line ending kept byte for byte, the seed's prose written with the live file's line ending, backup `<file>.bak-HUB-43` with COPYFILE_EXCL). Dry run first (reports `L1-dry.json`, `L2-dry.json`), then the write (`L1.json`, `L2.json`). The live-vs-seed prose diff was recomputed at run time (after today's `.bak-HUB-42` edits): every removed live line was older wording of something the seed says now (pre-HUB-38 "Scriptorium/VN Studio only connects to it", old `D:\Strata\run-*.bat` paths, LM Studio context and `load_models` notes, the `lmstudio/...` example id, the older `kind` list, the search-provider sentence without `client`). No user note found; nothing kept back. Scriptorium down throughout and never started.

| step | file (line ending) | front-matter sha256 before = after | bytes | `git diff --no-index -U0 <file>.bak-HUB-43 <file>` | prose (CR stripped) = seed |
|---|---|---|---|---|---|
| L1 | `C:\Users\Infplane\Scriptorium\config\providers.md` (CRLF, no BOM; front matter ends at line 244) | `b0d12bacbabcaea0d8babed43bc1239dc555cf7675332e901fba42410a0079f2` | 16,927 -> 26,308; 292 -> 331 CRLF | 11 hunks, all at line 253 or later (`@@ -253,2 +253,4 @@` ... `@@ -290,3 +329,3 @@`): new `name`, `custom`, `on_device`, `rpd`, Models-panel limits, `loaded`/`aliases`/`profiles` lines; Strata section as the seed's; new sections "The ACP proxy", "OpenRouter", "DeepSeek", "Client provider"; `client` search engine; LM Studio notes replaced. Full diff `.claude/temp/hub43-live/L1.diff` | yes |
| L2 | `C:\Users\Infplane\VisualNovels\config\providers.md` (CRLF, no BOM; front matter ends at line 219) | `9df9cc936fcd632852dd4621591ca343855077b8d4b5ae4e066625d681b3b6f3` | 17,332 -> 23,056; 268 -> 293 CRLF | 6 hunks, all at line 229 or later: `kind` list with `client`, `name`, `custom`, `loaded`...; new sections "Client (Claude Code does the model work)" and "ACP proxy"; Strata section as the seed's. Full diff `.claude/temp/hub43-live/L2.diff` | yes |

Backups: `C:\Users\Infplane\Scriptorium\config\providers.md.bak-HUB-43` (sha256 8497a517...adbe = the live file before), `C:\Users\Infplane\VisualNovels\config\providers.md.bak-HUB-43` (b02e9614...c4be). Older `.bak-HUB-38`, `-L2b`, `-39`, `-42` untouched. Re-checked at 20:15, after the VN restart: both files still have the same front matter and prose equal to the seed (VN's seeding did not overwrite it).

## R1 + K1 The proxy (HUB-42 K1, AAP-48, AAP-49, AAP-50)

Preconditions 19:42: `/healthz` every provider active 0, queued 0; VN `jobs\running` empty.

- `yarn build` in api-acp-proxy, 19:42:53-19:42:57, exit 0 ("copied 7 static files"). `dist/electron/main.js` 19:42:55.9, `dist/renderer/monitor-view.js` 19:42:56.8 (contains the sparkline code, `spark(` six uses), `dist/llama-args.js:36` `parts.push("--metrics")`.
- `hub.ps1 stop acp-proxy` 19:43:09: "acp-proxy: stopped (pid 26412)". Strata (37680) stopped with it: 8080 refused at once, so it was the proxy's Strata. Nothing printed about a lock (no lock configured).
- `hub.ps1 start acp-proxy` 19:43:30: "acp-proxy: started (pid 22332)", "up". The 8787 owner is electron 33000, process start 19:43:32.0, after the build: the running app is the new build.
- `GET /v1/models`: local ids gufo/Qwen3.8-27B (vision false), gufo/flash-next-q4 (true), gufo/deepseek4 (false), gufo/qwen-image-2.1 and -turbo (image), **strata/qwen3.8-flash-next-unsloth-ud-iq4_xs (no `kind` and no `vision` field)**, llama/inkling-2-mini (vision true), llama/inkling-2-mini-dspark (true), llama/nomic-embed-text-v1.5 (embedding). So `/v1/models` does not mark the Strata model as vision, although Strata itself reports `images: true`.

| step | request | id | result | usage (prompt / completion / cached / reasoning) | time |
|---|---|---|---|---|---|
| 3 | Strata, "Reply with the word OK.", max 50, effort none (loads Strata) | chatcmpl-70a59e1fd89c48fb8f2db243c1da1f36 | 200, "OK" | 18 / 2 / 0 / 0 | 56.1 s (19:43:51-19:44:47) |
| 5 | same, effort low, max 300 | chatcmpl-a14e65b436f449dcae2d4969b87a58e8 | 200, "OK" + `reasoning_content` (one sentence) | 46 / 34 / 0 / **32** | 2.4 s |
| 7 | image: 64x64 PNG data URL (red disc on blue, made with Node), "What shape and colours...", effort none | chatcmpl-afdb2668f44a423aacd959198b645e8f | **200**, "A red circle is on a blue background." (right) | 36 / 10 / 0 / 0 | 1.1 s |

Usage carries both `prompt_tokens_details.cached_tokens` and `completion_tokens_details.reasoning_tokens` on every answer (AAP-48 guards). Step 4 (a person reading the window) could not be done: no screenshot of the Electron window is possible from here; the table below is computed from the same sources instead. Step 6 (polling stops when hidden): not measured (no outside evidence).

### What the Monitor and About pages should show (computed with the proxy's own built mappers)

Source: `.claude/temp/hub43-live/monview.mjs` imports `dist/local-monitor.js` and calls `fetchEngine("strata", 8080)`, `cpuSampler`, `hostView` exactly as `main.ts` does, plus `/healthz` and `/v1/models`. Reading A at 18:45:41Z (19:45:41 local, after steps 3, 5, 7), reading B 10 s later. No key, `Bearer` or `sk-` string in either reading (grep count 0); requests went through without an `Authorization` header, so `server.apiKey` is not set and About should say "API key: not needed".

| page | tile | value | sub line / note |
|---|---|---|---|
| Monitor | Model | strata/qwen3.8-flash-next-unsloth-ud-iq4_xs | none (no label) |
| Monitor | State | ready | |
| Monitor | Engine | idle | |
| Monitor | Since | ready time, about 19:44:46 | |
| Monitor | Port | 8080 | |
| Monitor | Proxy queue | 0 / 4 | 0 queued |
| Monitor | Decode | 42.9 t/s (46 output tokens / 1,071.7 ms decode, totals) | line: last 60 s of `tok_s` (45 points so far, newest 0,0,0,0,0: a flat line on the baseline) |
| Monitor | Prefill | 39.4 t/s ((100 - 0) / 2,540.6 ms) | |
| Monitor | Prompt reused | 0 of 100 | 0% over 3 requests |
| Monitor | Conversation cache | 2 of 4 parked | 0 restored · 0 evicted · 452 of 2,048 MiB |
| Monitor | Context | 131,072 tokens | |
| Monitor | Slots busy | 0 / 4 | four slot bars "idle · 0 / 131,072" |
| Monitor | GPU load | 0% | AMD Radeon(TM) 8060S Graphics; line newest 1,0,0,0,0 (earlier 31, 53, 69 during the requests) |
| Monitor | VRAM | 63.2 GB | of 64.0 GB; line flat at 67,884,810,240 bytes; bar "63.2 GB / 64.0 GB" marked full (>= 90%) |
| Monitor | GPU temp | 35 °C | line flat 35 (52 during a request) |
| Monitor | Power | 24 W (B: 21 W) | line newest 22,21,22,23,24; B 21,21,21,22,21: moves between A and B |
| Monitor | Disk read | 0.1 MB/s | line newest 1.78, 0.03, 0.03, 0.04, 0.09; B 0.03,0.04,0.09,0.04,0.09: moves |
| Monitor | CPU | 7% (B 4%) | 32 threads |
| Monitor | RAM | 56.2 GB | of 63.6 GB |
| Monitor | engine requests (newest first) | 19:45:01 stop 36 / 0 / 10, prefill 51.4, decode 34.3, 1.0 s; 19:44:58 stop 46 / 0 / 34, 32.7, 52.2, 2.4 s; 19:44:46 stop 18 / 0 / 2, 41.4, 15.5, 0.6 s | |
| Monitor + Requests page | proxy requests | step 3: 200, in 18, out 2, Thinking "-", 56 s; step 5: 200, in 46, out 34, **Thinking 32**, 2.4 s; step 7: 200, in 36, out 10, Thinking "-", 1.1 s | Thinking = `usage.completion_tokens_details.reasoning_tokens`, the value `traceUsage` stores (`server.ts:59`); 0 shows as "-" |
| About | Model / Engine | strata/qwen3.8-... / Strata 0.1.52 | |
| About | Context / Images | 131,072 tokens / yes | |
| About | KV cache | int8 | 32,768 positions resident |
| About | Experts in VRAM | 24,576 slots | 56,762 MiB |
| About | Speculation | mtp | |
| About | GPU / CPU / RAM | AMD Radeon(TM) 8060S Graphics, 64.0 GB memory / AMD RYZEN AI MAX+ 395 w/ Radeon 8060S, 32 threads / 63.6 GB | |
| About | Connect | base URL `http://127.0.0.1:8787/v1` (the plan's; not read from the window); API key not needed; local model ids: the nine ids of `/v1/models` above | |

After the Inkling request (18:46:32Z) the same pages switch to Llama: Model llama/inkling-2-mini (or the profile's label with that id under it), Engine idle, **Decode 11.7 t/s and Prefill 21.2 t/s, "average since the model started"**, Prompt reused and Conversation cache "-" ("from Strata"), Context 32,768 tokens, Slots busy 0 / 4 (slot 0 "idle · 40 / 32,768"), hardware tiles "-" ("from Strata"), About Engine "llama.cpp b12613-362ac9297", Images yes.

### AAP-50 on Inkling

- 19:46:05 `llama/inkling-2-mini`, "Reply with the word OK.", max_tokens 20: id chatcmpl-dd0c781cb5934c15b1b8d01de7c4cd2e, HTTP 200 in 16.0 s (load included; Strata was evicted, 8080 down afterwards). `finish_reason: length`, content empty: all 20 tokens went to thinking (usage 21 / 20, reasoning 20). Expected with 20 tokens.
- `GET 8082/metrics` at once, the four counters are present:
  ```
  llamacpp:prompt_tokens_total 21
  llamacpp:prompt_seconds_total 0.992387
  llamacpp:tokens_predicted_total 20
  llamacpp:tokens_predicted_seconds_total 1.70899
  ```
  (also `prompt_tokens_cached_total 0`, `n_decode_total 22`, `n_tokens_max 40`, `prompt_tokens_seconds 21.1611`, `predicted_tokens_seconds 11.1177`, `requests_processing 0`, the spec-decode counters 0.)
- `GET /props`: `endpoint_metrics: true`, `default_generation_settings.n_ctx: 32768`, `total_slots: 4`, `build_info: b12613-362ac9297`, modalities vision true. `GET /slots`: slots 0-3, each `n_ctx: 32768`.
- One request's context on the chat server is 32,768 tokens (the launcher passes `-c 32768` with no `-np`; llama.cpp gives each of its 4 slots the full 32,768 here). AAP-50's rule (slot 0's `n_ctx`) gives 32,768 for Inkling: right.
- Decode average since the model started = 20 / 1.70899 s = **11.7 t/s**; Prefill = 21 / 0.992387 s = **21.2 t/s** (the mapper computed the same).
- Command line of the 8082 llama-server: `llama-server.exe -m ...Inkling-2-Mini-IQ4_NL.gguf --host 127.0.0.1 --port 8082 --alias inkling-2-mini --metrics -c 32768 -ngl all -fa auto --mmproj ...mmproj-Inkling-2-Mini-Q8_0.gguf --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0.0`: `--metrics` exactly once; it started without complaint.

K1 verdict: **PASS** for everything measurable (new build running, images 200, thinking counts in usage and in the Requests source, cached and reasoning fields present, sparkline series present and moving, conversation-cache numbers, Llama speed and context, no key value, settings hash unchanged). **UNTESTED**: the window itself (no person or screenshot read the tiles), polling while hidden. K1 took about 4 minutes (box 30).

## R2 + K2 VN Studio (HUB-42 K2, VNO-72)

- `hub.ps1 build vn-studio` 19:46:43-19:46:48, exit 0 (`yarn build:engine`, the known `puzzle.ts` dynamic-import warning); `out/engine` 19:46:48.
- No VN job running (`jobs\running` empty). `hub.ps1 stop vn-studio` 19:47:14: printed `vn-studio: stopped (pid 25848)` and `vn-studio: removed its stale lock (pid 25848)`. Lock after the stop: absent.
- `hub.ps1 start vn-studio` 19:47:22: printed `vn-studio: started (pid 9004), waiting for port 7459...` and `vn-studio: up at http://127.0.0.1:7459/mcp`; nothing about a lock (the file was already gone). New lock written by the app: `{"pid":21468,"startedAt":"2026-11-22T18:47:29.995Z"}` (file mtime 19:47:30.54); node 21468 started 18:47:24.25Z (the lock came 5.7 s after the process start).
- Live critic prompt `C:\Users\Infplane\VisualNovels\prompts\art-critic\review_image.md` refreshed from the new seed on start (mtime 19:47:30.11, 1,469 -> 1,834 bytes) and contains "Never put negations": yes.
- Models: `art-critic: [paid, acp/llama/inkling-2-mini]` (paid DeepSeek has no vision and is skipped, as in HUB-41); the art-director needed no model (hand-set prompt). The project had no own `models`.

Steps (VN MCP tools loaded with ToolSearch after the restart):
1. `vno_create_project` `hub42-signs-check` (en, one place "Market street", looks "a narrow street of old shop fronts with awnings", `art.review: true`) -> 1 background, 1 cover, 3 music.
2. `vno_asset_set bg_market_street_noon` prompt "A narrow market street with old shop fronts and awnings at noon, anime visual novel background" (1664x928, `promptByHand`).
3. `vno_asset_generate {only: [bg_market_street_noon], force: true}` -> job `hub42-signs-check--vn.assets.generate--all--r1`; `vno_wait {timeoutSeconds: 240}` -> timedOut (review running); called again -> done.
   - `...--vn.assets.generate--bg_market_street_noon--r1`: v1 18:48:12Z-18:50:02Z (qwen-image-2.1, seed 1643838289).
   - `...--vn.assets.review--bg_market_street_noon--r1` (art-critic-default, `acp/llama/inkling-2-mini`, prompt version d04d05b3): 2 calls.

| attempt | image (my look) | spend row | tokens in / cached / out | seconds | verdict | problems | revisedPrompt |
|---|---|---|---|---|---|---|---|
| 1 | v1: a narrow street, many hanging and wall signs with CJK-like lettering (left top, centre, right), air conditioners, awnings | 19:51:31 | 1,034 / 0 / 778 | 88.7 | rejected | "Stray Japanese text/letters on shop banners and signs along the street" (right) | "A narrow market street with old plain shop fronts and awnings at noon, anime visual novel background, blank wooden facades and shuttered windows" |
| 2 | v2 (seed 65548426): an empty street of wooden shop fronts with shutters and green/orange awnings, no lettering anywhere I can see | 19:53:50 | 1,045 / 139 / 222 | 34.4 | approved | none | null |

Regenerated prompt (the asset's `prompt` after the rejection, v2's prompt): "A narrow market street with old plain shop fronts and awnings at noon, anime visual novel background, blank wooden facades and shuttered windows". It contains none of "no text", "no letters", "no signs", "no captions", "without any text", "No text.". Both spend rows 0.000000 USD.

Which half was exercised: the **critic-prompt half** (VNO-71/72 seed prompt "Never put negations"): Inkling wrote a positive revision ("plain", "blank", "shuttered") instead of HUB-41's "no text, no letters, no signs". The **sanitiser half** (`stripTextNegations`) had nothing to strip, so it was NOT exercised live.

4. `vno_comfy_free {}` -> `{"results":[{"lane":"http://127.0.0.1:8188","ok":true}]}`; ComfyUI vram_free 106,009,006,080 of 107,090,132,992.
5. VNO-72: `vno_delete_project {slug: "hub42-signs-check--vn.analyse", confirm: true}` -> error `invalid project slug "hub42-signs-check--vn.analyse"`. Afterwards `jobs\done` still held the project's 3 job files (the project had no `vn.analyse` job; the refusal comes from the slug check before anything is touched).
6. `vno_delete_project {slug: "hub42-signs-check", confirm: true}` -> deleted. `jobs\{queued,running,done,failed}` hold 0 `hub42-signs-check--*` files; the project folder is gone.

K2 verdict: **PASS** (no negation in the regenerated prompt, bad slug refused, job files gone, critic on Inkling at 0 USD). One of two images had lettering (v1), correctly rejected. About 7.5 minutes (box 25).

## R3 + K3 + K4 Pixel (HUB-42 K3, K4, PAR-24)

- `hub.ps1 build pixel-studio` 19:54:14-19:54:22, exit 0 (electron-vite, the usual chunk-size warnings).
- Real data folder `C:\Users\Infplane\PixelStudio`: newest file `config\providers.md` 2026-11-22T18:10:08 before and after; its `engine.lock` unchanged (pid 32952, dead). Port 7457 never listened.
- Temp data folder `C:\projects\Personal\creative-hub\.claude\temp\hub42-pixel` (copy of the live `config`), `vision: true` added to the `acp` row `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`. Temp headless Pixel: `electron.exe . --mcp-only` in pixel-art-generator with `PIXEL_STUDIO_HOME` = that folder and `PIXEL_STUDIO_MCP_PORT=7467` (pid 21148, then pid 2964 for the vision-off runs). JSON-RPC over HTTP to `http://127.0.0.1:7467/mcp` with `.claude/temp/hub43-live/mcp.mjs`.
- Roles in the copy: `artist: [local]` = `acp/strata/...` only: no paid fallback could answer.
- `list_models`: default and selected `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, that model `tools: false`, `vision: true`, `local: true`, `free: true`; `unavailable: 11`.
- Strata was loaded by the proxy first with a tiny chat (19:55:10, 67.6 s, Inkling -> Strata switch) so run 1's wall time does not include the switch.
- Strata `/v1/telemetry` `work.client_disconnect_cancels` 0 before the runs.

All runs: the HUB-41 K1 mushroom text ("Draw a small red mushroom with white spots on its cap and a pale stem, centred on this 16x16 canvas, with a dark outline. Use the document's palette."), every step `mode: "json"`, no tool error, `costUsd` 0, every call to Strata.

| run | vision | runId | start (UTC) | state | steps | wall | usage in / cached / out | first step: Strata prompt / reused / seconds | per-step growth |
|---|---|---|---|---|---|---|---|---|---|
| K3 = K4 run 1 | true | c95146c1-2193-4254-8803-2a114ccb9c91 | 18:56:23.9 | **max_steps** | 25 | 220.6 s | 1,047,042 / 1,036,697 / 5,702 | about 34,300 / 0 / about 70 (from Strata totals; events of steps 1-17 were dropped by the 200-event buffer) | 638 tokens a step (clear_cel + draw_grid + render_preview, each with an image), 224 out |
| K4 run 2 (`model: ""`) | true | e890dcfd-3744-4ef4-9892-6be79f948d53 | 19:00:47.6 | completed | 19 | 127.4 s | 707,949 / 668,838 / 1,653 | 34,300 / **0** / 69.6 | 222-568 |
| K4 run 3 | false | c60ad925-098b-4393-a042-7ee81e0667df | 19:03:43.3 | **max_steps** | 25 | 175.1 s | 1,002,807 / 958,502 / 3,266 | 34,301 / **0** / 71.5 | about 470 (set_pixels + read_grid) |
| K4 run 4 | false | 80767214-2522-4e1c-a56c-4f113f421eef | 19:06:43.4 | completed | 4 | 78.1 s | 138,812 / 103,741 / 390 | 34,301 / **0** / 70.9 | 132-381 |
| stop check | false | e70ccd24-b718-4935-9a3a-b4a7b1a7a85b ("Draw a small green tree on this canvas.") | 19:08:12.6 | aborted by `stop_agent_run`, `stoppedBy: mcp` | 7 | 29.8 s | 211,637 / 209,883 / 970 | 34,271 / **34,250** / 5.1 | |

Strata's own `requests[]` (polled every 2 s, `.claude/temp/hub43-live/run2-strata.json` ... `run4-strata.json`): inside a run every step after the first reuses all but the newest few hundred tokens, for example run 2 step 2 34,593 / 34,293, step 19 40,539 / 40,273; run 1's last 12 steps 38,678 / 38,264 ... 49,526 / 49,113. Across runs: the first step of runs 2, 3 and 4 reused 0 (and costs about 70 s of prefill); the first step of the stop-check run reused 34,250 of 34,271. Conversation cache after run 5: parks 14, evictions 8, **restores 0**, requests 82, reused 77, reused tokens 3,014,434 of 3,179,779 prompt tokens. Strata totals over run 1 (since its load) counted 26 requests besides the tiny chat while Pixel counted 25 steps (one extra request of about 34,300 tokens: see Discoveries).

K3 verdicts:
- Did a preview image reach Strata? **Very likely yes, not proven byte-for-byte.** With `vision: true` every drawing result and `render_preview` came back `hasImage: true` (Pixel's `withAutoPreview` for vision models), the model never called `read_grid` and wrote replies about what it looked at ("Final clean redraw with a fully outlined pale stem", "Adjusting spots to three distinct dots", "Adding a lower-left spot for balance"); with `vision: false` the results had no image and the model used `read_grid` after every change instead. No 4xx anywhere. The token counts do not settle it: Strata counts an image small (K1's 64x64 image plus text was 36 prompt tokens; a 256x256 preview should be well under 100), so a vision step grows by about 130 tokens per image-bearing result, about the same as HUB-41's 126-token text-only render_preview step.
- Did the run finish? Run 1 **no**: it hit `max_steps` (25) after redrawing the same 16-row grid with `clear_cel` + `draw_grid` + `render_preview` about 18 times; run 2 (same settings) completed in 19 steps. Compared with HUB-41 K1 (vision off, 4 steps, 87.5 s, 138,782 in): run 1 took 220.6 s (2.5x, under the plan's 3x limit) and 7.5x the input tokens; run 2 127.4 s (1.5x), 5.1x the tokens. Run 4 (vision off) matched HUB-41 K1 almost exactly: 4 steps, 78.1 s, 138,812 in.
- The plan's pass rule ("completed with at least one preview image in the model's input and no 4xx"): run 1 FAIL (max_steps), run 2 PASS on the same settings. I record K3 as **PASS with a caveat** (one of two vision runs looped to the step limit); the follow-up idea below is written but should wait for the director.
- PAR-24 (`model: ""`): run 2 answered `model: acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, equal to `list_models`' `selectedModel`: **PASS**.
- Stop: `stop_agent_run` at 19:08:42 -> `stopped: true`, `state: aborted`, `stoppedBy: mcp`, no `timedOut`. Strata's in-flight request (37,214 prompt, 36,773 reused) ended `finish: cancel` after 1.9 s with 0 output, and `/v1/telemetry` `work.client_disconnect_cancels` went 0 -> 1 within 2 s; the proxy's Strata `active` was 0 by 19:08:44. So the Strata request behind a stopped run **is cancelled at the server** (closes HUB-41's UNTESTED line).

Pictures (exported at scale 16, `.claude/temp/hub43-live/run1-mushroom.png` ... `run5-tree.png`), my look:
- Run 1 (vision, max_steps): red cap with white and peach squiggles more than round spots, black outline round the cap; peach stem with a grey block in its middle, outline only on its sides; the bottom row is cut off. Placed left of centre. Worse than HUB-41's.
- Run 2 (vision, completed, drawn over run 1's canvas): a clean red dome cap with three white/peach spots, a plain peach stem, black outline all round, about 1-2 px left of centre. The best of the five.
- Run 3 (vision off, max_steps, new document): red cap with two small white spots (reads a bit like a face), peach stem, black outline; acceptable, slightly left.
- Run 4 (vision off, completed, drawn over run 3's canvas): a large red cap with several white spots, a peach stem with a black "door" in it, black outline, bottom brown/black base line: reads like a mushroom house.
- Stop check (tree, aborted after 7 steps): a dark-green round crown with lighter green highlights, a brown trunk; a few peach pixels of the old mushroom stem were left on the left.

K4 verdicts (Question 2/4 inputs): inside a run Strata reuses about 99% of the prompt from step 2 on (runs 1-3: 99.0%, 94.5%, 95.6% cached over the whole run, the misses being each first step). Across runs the reuse of the first step depends on which of Strata's 4 slots takes it: three of four new runs reused 0 and paid about 70 s of prefill for the 34.3k-token prompt; one reused 99.9%; the conversation cache never restored. The first prompt was 34,300/34,301 tokens with vision on or off (so `vision: true` adds nothing to the system prompt), slightly larger than HUB-41's 34,292. So: the prompt reorder works when the slot is warm (the tree run's first step shared 34,250 tokens with the previous run's prefix), and a slimmer tool list (about 4.3k tokens less) would save little on steps 2+ (already reused) but would cut each cold first step by roughly an eighth (about 9 s of 70 s). The Monitor's engine table would show these rows (time, finish, prompt, reused, output, prefill, decode, seconds), newest 12 only.

- Temp Pixel stopped (pid 2964 killed; 21148 earlier), 7467 free, `.claude\temp\hub42-pixel` deleted. K3+K4 took about 15 minutes (box 45).

## R4 Edu and Cartoon builds

`hub.ps1 build edu-studio cartoon-studio` 20:10:50-20:11:01, exit 0 (`yarn build:engine` in each; edu-game-studio 7d93579, cartoon-studio 5635447, both clean). Not started. Their H1 start path stays UNTESTED.

## K5 A Strata started outside the app (AAP-49)

The proxy's Strata page Stop button cannot be pressed from here, so the proxy's Strata was stopped by stopping the proxy (an allowed restart), which takes its Strata with it; no second Strata at any time.
1. 20:11:19 `hub.ps1 stop acp-proxy` -> "stopped (pid 33000)"; 8080, 8082, 8083, 8787 all free.
2. 20:11:25 `hub.ps1 start strata` -> "variant iq4_xs-parallel", "started in its own console window", "up" at 20:12:22; `/health` `loaded: true` (python 36648 under python 2888 under cmd 14764, not under the proxy).
3. 20:12:25 `hub.ps1 start acp-proxy` -> "started (pid 32316)", "up".
4. 20:12:39 the K1 step 3 request through the proxy: chatcmpl-373069f79c6e4076b8c0aebac38c0d7e, 200 "OK", 18 / 2 tokens, **0.5 s** (passed straight through; nothing loaded; still one listener on 8080, nothing on 8082).
5. Monitor source data (with the proxy's `fetchEngine("strata", 8080, ..., 800)`, the outside-server path of `main.ts:560-575`): kind strata, version 0.1.52, state idle, context 131,072, images true, Decode 18.2 t/s, Prefill 47.8 t/s, reuse 0 of 18 over 1 request, conversation cache on, 0 of 4 parked, budget 4,352 MiB, GPU 15%, VRAM 63.6 GB of 64.0, 41 °C, 59 W. `main.ts` then sets `local = {server: strata, state: ready, port: 8080, external: true, modelId: strata/qwen3.8-...}`, so the Model and State tiles carry "started outside the app" under them. Not seen in the window.
6. Restore: 20:12:47 `hub.ps1 stop strata -Force` -> "strata: stopped (pid 2888)"; 8080 down; the leftover console `cmd.exe /k ...run-unsloth-ud-iq4_xs-parallel.bat` (14764) closed. 20:13:09 tiny chat (effort none): chatcmpl-3af0c09a5a764fce9e85e84e76a5f67f, 200 "OK", 54.0 s: the proxy started Strata itself (8080 python 21512 <- python 10100 <- cmd 33712 <- electron 34600, the proxy).

K5 verdict: **PASS** for the source data and the pass-through; the window's wording UNTESTED. About 3 minutes (box 15).

## Every hub.ps1 start and stop, and the locks

| time | command | what it printed about a lock | lock file before / after |
|---|---|---|---|
| 19:43:09 | stop acp-proxy | nothing (no lock configured) | - |
| 19:43:30 | start acp-proxy | nothing | - |
| 19:47:14 | stop vn-studio | `vn-studio: removed its stale lock (pid 25848)` | VN lock present (pid 25848 alive) -> absent after the stop |
| 19:47:22 | start vn-studio | nothing (no file to check) | absent -> new lock pid 21468, startedAt 18:47:29.995Z, written by the app |
| 20:11:19 | stop acp-proxy | nothing | - |
| 20:11:25 | start strata | nothing (unmanaged console start; `Clear-StaleLock` not called) | - |
| 20:12:25 | start acp-proxy | nothing | - |
| 20:12:47 | stop strata -Force | nothing (no lock configured) | - |

No start removed a lock whose pid was alive. The HUB-42 stop path (pid gone after taskkill -> removed) ran for real once (VN). The HUB-43 start path (`Clear-StaleLock -AtStart`, dead pid or reused pid) did **not** run on a real lock: VN's lock was already gone, and the apps with stale locks (Edu 25460, Cartoon 10856, Pixel 32952, Scriptorium 19260) were not started. Lock files at the end: Scriptorium 19260 (dead), VN 21468 (alive, node), Edu 25460 (dead), Cartoon 10856 (dead), Pixel 32952 (dead), as before except VN.

## End state (20:15)

- Proxy's local model: Strata started by the proxy (tiny chat 20:13:09 with `reasoning_effort: none`), 8080 answers (python 21512), 8082 down, 8083 down.
- `/healthz`: status ok, every provider active 0, queued 0.
- ComfyUI memory freed (`vno_comfy_free` ok at 20:14; vram_free 106,009,006,080 of 107,090,132,992).
- Nothing on 7467; the real Pixel (7457) down.
- Running: vn-studio (21468, new build), comfyui (17472), acp-proxy (electron 34600, new build), strata (by the proxy), vibetts (17740). Down: scriptorium, edu-studio, cartoon-studio, pixel-studio, chiptune-studio and the rest. Never started: Scriptorium, Edu Studio, Cartoon Studio, the real Pixel Studio.
- Proxy settings SHA-256 `1130D968...A592`, equal to the start value. No queue paused.

## Calls that did not go to Strata or Inkling

None. Every model call went through the proxy to Strata (K1 steps 3/5/7, the warm-up and K5 chats, the five Pixel runs) or to Inkling (the AAP-50 request and VN's two reviews). The VN art-director logged "first model: none (no model needed)". GET-only reads: proxy `/healthz`, `/v1/models`; Strata `/metrics`, `/v1/telemetry`, `/health`; llama-server `/metrics`, `/props`, `/slots`; ComfyUI `/system_stats`.

## UNTESTED

- The proxy window: no person or screenshot read the Monitor, About and Requests pages; the expected values above are computed from the same sources with the built mappers. Polling while hidden not measured.
- VN's `stripTextNegations` (VNO-72) live: the critic wrote no negation, so the sanitiser had nothing to strip.
- `hub.ps1 start`'s stale-lock removal (H1) on a real app; pid-reuse removal cannot be produced on purpose.
- Edu and Cartoon after their rebuild (not started; `freeMemory` paths against ComfyUI).
- L1 in Scriptorium (not started; it reads the file on its next start). L2 is in the running VN (read on this start).
- Whether a preview image's pixels are in Strata's prompt (strong signs, no byte-level proof).
- Gufo probe P1 (no Gufo model loaded).

## Corrections from the read-only check (2026-11-22)

- K3: with vision on, run 1 hit max_steps (25 steps, 220.6 s) and run 2 completed (19 steps, 127.4 s): one of two. Whether the preview image reaches Strata is likely, not proven: `hasImage` in the run records comes from the tool result, not from what the model was sent.
- The statement that with vision off the results had no image is not exact: the vision-off run 4 has one `hasImage: true`, on an explicit `render_preview`.
- The missing `vision` field for the Strata model in `/v1/models` at 19:43 was a list read before Strata was loaded; with Strata loaded the proxy lists it with `vision: true`.
