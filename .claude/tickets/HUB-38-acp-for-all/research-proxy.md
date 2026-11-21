# HUB-38 research: what the ACP proxy offers for local models

Date: 2026-11-21. Proxy repo `C:\projects\Personal\api-acp-proxy` (master at 93403ad, AAP-37, AAP-38, AAP-39 merged). Live GETs only (`/healthz`, `/v1/models`); no chat, completion or image request sent. Paths below are relative to the proxy repo unless stated. **confirmed** = read or run; **inferred** = reasoned.

## Question

What does the proxy offer today for `gufo/*`, `strata/*` and `llama/*`, and where does it fall short of what LM Studio (1234) and a direct Strata (8080) gave the creative-hub apps?

## Answer (short)

- The proxy is a thin OpenAI-compatible forwarder to a local llama-server style process. Chat completions (streaming, thinking, vision on some models), `/v1/models` and, for Gufo only, `/v1/images/generations|edits` work. **There is no `/v1/embeddings` (404).** No tools / function calling, no structured output enforced by the server (JSON schema is only a prompt instruction plus cleanup), no `stop`, `n>1`, `top_k`, `min_p`, `temperature`, `top_p`, `seed` (all dropped or refused).
- Only the **desktop app** (ACP Proxy.exe) launches and switches local servers. The headless CLI (`node dist/index.js`, which `hub.ps1` starts) has no launcher: it only passes requests through to something already listening.
- The live proxy on 8787 is the portable desktop exe, not the hub.ps1 node process. That is why it ignores the hub env (bare aliases, 300 s timeout).
- On this PC today `llama/*` cannot start (no llama-server build installed, preset model files not on disk) and `gufo/flash-next-q4` has no model folder.

## 1. The three providers: what they start, who launches them, GPU switching

**Registration** (confirmed): `src/providers/local-openai.ts:291-307` builds one `LocalOpenAiProvider` per id with base URL `http://127.0.0.1:<port>/v1`, Node's global `fetch` (Strata refuses a browser `Origin`, `:294`). The same class serves all three.

| | `gufo/*` | `strata/*` | `llama/*` |
|---|---|---|---|
| Port (default, confirmed `src/settings.ts:81,311`, live settings.json) | 8081 | 8080 | 8082 |
| What runs | `D:\Gufo\gufo.cmd serve llm\|image ...` with per-profile args (`settings.ts:51-57`, `main.ts:151`) | `D:\Strata\terminal\run-unsloth-ud-iq4_xs.bat` (one fixed bat, one model; `main.ts:136`) | `llama-server.exe` with args generated from the profile (`src/llama-args.ts:31-51`, `main.ts:147`) |
| Models listed | static, one per profile, listed whether or not running (`local-openai.ts:77-81`) | whatever the upstream `/v1/models` returns; with no server running the list comes from `models-cache.json` (inferred: live list shows `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` though nothing listens on 8080, and proxy.log has "Listing models for 'strata' failed: Strata is not running") | static, one per profile |
| Who launches | the desktop app only | the desktop app only (or the user / hub.ps1, then it is "external") | the desktop app only |

**Who launches** (confirmed):
- Desktop app: `src/electron/main.ts:120-168` creates `LocalServerManager` and `LocalModelCoordinator` and gives the coordinator to all three registrations.
- Headless CLI: `src/controller.ts:90` registers `gufoRegistration, strataRegistration, llamaRegistration` with **no coordinator** (`local-openai.ts:295` adds it only when `host.coordinator` is set). So no launching, no switching, no queue: `prepareModel` returns undefined (`:108`), the request goes straight to the port, and if nothing answers the client gets 503 `local_server_not_running` ("Gufo is not running - start it from the app", `:37`).
- README: "A server is **not** started automatically: not at app start" (`README.md:138`). In the app, a *request* does start it through the coordinator (see below); README line 138 describes the no-request case. The two statements are slightly in tension; the code is authoritative: `local-models.ts:176-196` `ensureReady` starts the target on a request.
- hub.ps1 does not know about any of this (inferred; hub.ps1 not read for this note): it only starts the node CLI.

**One model at a time across all three** (confirmed):
- `LocalServerManager.start` (`src/local-servers.ts:116-159`) stops any *other server the app owns* before spawning (`:138-141`), waits up to 30 s for the port to free (`:143`, `releaseTimeoutMs` `:106`), then refuses with "Port N already answers (a server started outside the app?)" if the target port is occupied (`:145`).
- `LocalModelCoordinator` (`src/local-models.ts:54-197`): FIFO queue of waiters by target key (`gufo:<id>`, `llama:<id>`, `strata`). A request for the *active* target is admitted at once. A request for a *different* target waits until the active one has zero requests in flight and is not still starting (`pump`, `:127-137`), then the app stops the old server and starts the new one (`ensureReady` -> `startAndWait`, `:176-196`). Every admitted request holds a lease until its response ends (`prepareModel` `local-openai.ts:101-110`, `release` in server.ts handlers).
- **Case asked:** app asks `llama/inkling-2-mini` while a gufo or strata model is loaded and app-owned: the request queues (FIFO) until in-flight requests on the loaded model finish, then Gufo/Strata is killed (process tree), Llama is started with the profile's flags, and the request is served once `GET /v1/models` on 8082 answers 200 (`local-servers.ts:256-268`; start timeout 10 min default, per-profile `startTimeoutMs`, `:104,269`). A waiter longer than `switchWaitMs` (default 30 min) gets 503 `local_model_busy` with `Retry-After` <= 60 s (`local-models.ts:83-89`); a failed start gives 503 `local_model_start_failed`, Retry-After 30 (`:171`). A client that disconnects while queued leaves the queue; a start under way is not cancelled (`:131,187`).
- **External servers are never touched** (confirmed `local-servers.ts:169-174`, `local-models.ts:180-181`): if the app owns no process for a server and its port answers, requests to that provider go straight upstream (no switch, even if it serves a different model than named). Consequence (inferred, from `start()` only stopping `this.entries` it owns, `:138`): if the user (or hub.ps1) runs Strata on 8080 outside the app and an app requests `llama/*`, the proxy does NOT stop Strata. It starts llama-server beside it, with both on the GPU/RAM (Strata "uses most of the GPU memory", services.json note). The same for LM Studio on 1234, which the proxy does not know at all.
- Gufo and Llama coordinator keys are separate, so a Gufo and a Llama profile may share an id (`local-models.ts:11-13`).

## 2. Model ids and capabilities

Live `GET /v1/models` (confirmed, 2026-11-21 ~17:20) local entries:

| id | kind | vision | notes |
|---|---|---|---|
| `gufo/Qwen3.8-27B` | llm | false | profile `qwen27-q4`; dflash2 speculative, context 32768 (`settings.ts:51`) |
| `gufo/flash-next-q4` | llm | true | MTP + mmproj, `--context 32768`, `--max-request-bytes 33554432` (`settings.ts:56`). **Model folder `D:\Gufo\models\flash-next-q4` does not exist on disk** (ls confirmed), so a start would fail the file precheck (`local-servers.ts:22-28`) |
| `gufo/deepseek4` | llm | false | DSpark, `--context 16384` (`settings.ts:57`); ~93 GB per README |
| `gufo/qwen-image-2.1`, `gufo/qwen-image-2.1-turbo` | image | n/a | `serve image`; `/v1/images/*` only; a chat to them is 400 `model_not_capable` (`local-openai.ts:104`) |
| `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` | (none) | (none) | no kind/vision fields; id is whatever the bat serves |
| `llama/inkling-2-mini` | llm | true | |
| `llama/inkling-2-mini-dspark` | llm | true | |

`/v1/models` fields added by the proxy: `kind`, `vision`, `max_prompt_chars` (only when the provider has a limit; **none for local models**), `exhausted_until` (`src/server.ts:509`). No context length is exposed for any local model: context is set in the profile args (`ctxSize` for llama, `--context N` in Gufo args) and the proxy does not report it or check prompt size against it (confirmed: `maxPromptChars` exists only for the ACP providers, README:224-232). An over-long prompt reaches llama-server and fails or truncates there (inferred).

**What Inkling is** (confirmed from `.claude/tickets/AAP-38-llama-cpp-provider/research.md:9,113-114`): Inkling 2 Mini by Thinking Machines Lab, released 2026-11-20, Apache-2.0, looped MoE 26.4B params / 3.4B active, text+image in, text out, 1M context in the model card. `inkling-2-mini` = `ggml-org/Inkling-2-Mini-GGUF` Q8_0 (~28 GB) + BF16 mmproj, no drafter. `inkling-2-mini-dspark` = `unsloth/Inkling-2-Mini-GGUF` UD-Q8_K_XL + F16 mmproj + `dspark-...-Q8_0.gguf` drafter, `--spec-type draft-dspark`, draft max 3, draft ngl 99, Unsloth llama.cpp build only (`settings.ts:134-150`).

**What the presets set** (confirmed `settings.ts:132-149`): `-ngl all`, `-fa auto`, `-c 32768`, `extraArgs` `--temp 1.0 --top-p 1.0 --top-k 0 --min-p 0.0` (the Inkling sampling recipe, set server-side), `--alias <model>`, `--host 127.0.0.1`, `--port {port}`, `-m`, `--mmproj` (`llama-args.ts:31-51`). **No `--jinja` flag and no `--reasoning` flag is generated** (inferred: absent from `buildLlamaArgs`; whether this llama-server build needs it for chat templates or tools is unknown). Build gate: `inkling-2-mini` needs ggml-org b12607 or newer, or the Unsloth build; DSpark needs Unsloth.

**Capability matrix for any local model** (confirmed `local-openai.ts:113,150-223`, `src/api.ts:21,26,53-62`, `server.ts:123-133,182`):
- Streaming: yes. Upstream is always called with `stream: true, stream_options.include_usage` (`:166`); the proxy re-streams or collects for non-stream clients (inferred).
- Thinking: `delta.reasoning_content` / `reasoning` from upstream becomes `reasoning_content` in the answer, never in `content` (`:181-182`, AAP-36).
- Tools / function calling: **no**. Provider status `features.tools:false` (`:113`); `toolCalling` is not set, so `canCallTools` is false (`router.ts:166`) and a request with `tools` is 400 `model_not_capable` (`server.ts:123`). Same for MCP and web search. ROADMAP lists "tools for local models" as open (`ROADMAP.md:38`).
- JSON / structured output: `response_format` (`json_object`, `json_schema`) is accepted by the schema (`api.ts:39-44,61`) but **not forwarded upstream**. It becomes a system-message instruction (`formatInstructions`, `api.ts:505-510`, pushed as a `system` message at `local-openai.ts:153`), and the answer is passed through `extractJson` (strip fences / prose, `server.ts:182`, `api.ts:593-605`). No grammar-constrained decoding, no schema validation. The hub's services.json already says `json_schema false` for the proxy.
- Vision: image parts become `image_url` data URLs only for profiles with `vision` (llama: needs mmproj) (`:91,155`); otherwise 400 `unsupported_content` before any switch (`:105`). Strata never accepts images (no profile).
- Sampling passthrough: of the client's parameters only `max_tokens` / `max_completion_tokens` / `max_output_tokens` is forwarded upstream as `max_tokens` (`:166`, README:142). **Dropped silently** (accepted, named in response header `x-acp-proxy-ignored-params`): `temperature, top_p, presence_penalty, frequency_penalty, seed, logit_bias` (`api.ts:26`). **Refused with 400 `unsupported_parameter`**: `n` > 1, `stop`, `functions`, `function_call`, `audio`, `logprobs`, `top_logprobs`, `prediction`, `service_tier` (`api.ts:21,154`). Other unknown fields (`top_k`, `min_p`, `repeat_penalty`, `chat_template_kwargs`, `reasoning_effort`) pass the `.passthrough()` schema (`api.ts:62`) but are simply not sent (the upstream body is built field by field, `local-openai.ts:166`). `reasoning_effort` is not mapped (ROADMAP.md:42).
- Roles: `developer` becomes `system`, `tool` becomes `user` (`:156`); assistant `tool_calls` are not carried (only `messageText`). Multi-turn tool loops through local models are therefore not possible.
- Responses API (`/v1/responses`) exists but has no reasoning item and also routes through the same text-only provider (inferred).

## 3. Embeddings and image generation

- **Embeddings: not served.** The route list in `src/server.ts:498-515` has only `GET /healthz`, `GET /v1/models`, `POST /v1/chat/completions`, `/v1/images/generations`, `/v1/images/edits`, `/v1/responses`, `/v1/mcp`. Anything else is 404 `not_found` (`:514-515`). A repo-wide grep for "embeddings" finds only an AAP-35 research note saying the Gufo binary *itself* has `/v1/embeddings` (`.claude/tickets/AAP-35-gufo-strata-speed-preview/research.md:21`, inferred from exe strings). Not exposed by the proxy, and no provider has an embedding model profile. So Scriptorium's RAG (nomic-embed-text-v1.5 on LM Studio) has **no replacement** in the proxy. Also: with the one-model-at-a-time rule, an embedding model would have to be its own profile and would evict the chat model on every switch (inferred), which is a design problem for RAG alongside generation.
- **Images:** `POST /v1/images/generations` (JSON: `model, prompt, size WxH, steps, seed, negative_prompt, guidance_scale, n, response_format=b64_json`) and `POST /v1/images/edits` (multipart, 1-10 `image` files, no `mask`) forward to the Gufo `kind: image` profiles' own `/images/generations` and `/images/edits` (`local-openai.ts:226-279`, `GENERATION_FIELDS` `:34`). Models: `gufo/qwen-image-2.1`, `gufo/qwen-image-2.1-turbo`. Response `data[].b64_json`, `created`, `output_format: png`. Image routes accept 64 MiB (README:162) and a 15 min request timeout (`:33`, `requestTimeoutMs` `:95-98`). `response_format: url` is 400. Not available: MCP `generate_image` on Gufo image models (still goes the chat path, AAP-37 attention.md:2), `loras`, `n > 1` (`ROADMAP.md:39`). Codex/Antigravity also generate images through the same routes; Llama and Strata never do.

## 4. Concurrency, queueing, timeouts, load time

- **Local providers:** `maxConcurrent` 1 each (live `/healthz`: gufo, strata, llama `max_concurrent: 1`; settings default `README.md:135`, `settings.ts` `localBase`). The hub env `PROXY_MAX_CONCURRENT=4` applies to codex/antigravity/claude only; local providers have their own default of 1 in settings.json, so no hub env change is needed. Effect: one local generation at a time per provider, others wait in the FIFO limiter (`src/limiter.ts`, README:214-220); LM Studio served parallel requests, this does not (inferred about LM Studio). `PROXY_MAX_QUEUE` (default 0 = unlimited) would 429 `provider_queue_full`.
- **Two queues stack** (inferred from `prepare` before the limiter in `server.ts:100-107` and README:160): first the coordinator lease (model switch, up to `switchWaitMs` 30 min, not part of the request timeout), then the provider limiter slot (counts toward `PROXY_TIMEOUT_MS`, README:218).
- **Timeouts:** request timeout = `server.timeoutMs`. **Live settings.json says 300000 (5 min)** (confirmed); the hub's 900000 only applies when started through hub.ps1. A long thinking answer from a local model above 5 min is cut with 504 `request_timeout` (inferred from README:218). Image profiles: 15 min. Model start: 10 min default per profile (`local-servers.ts:104`), server-ready poll every 1 s via `GET /v1/models` (`:103,256`). Port release wait 30 s. Models list upstream probe: 5 s (`local-openai.ts:137`). `PROXY_MODELS_WAIT_MS` 3 s for `/v1/models`.
- **First-request model load time:** not measured anywhere I found. AAP-37 README says a switch "can take many minutes" (README:159); memory notes: deepseek4 ~93 GB, flash-next-q4 ~115 GB, Qwen 27B Q4 smaller; Inkling Q8_0 ~28 GB (README:164,205). All live checks in AAP-35/37/38 are marked UNTESTED (`ROADMAP.md:34-37`). So an app's first request after a model change blocks silently (HTTP connection open, no progress) for minutes, bounded by the 10 min start timeout.
- Body size: `maxBodyBytes` live 20 MiB (hub env would set 8 MiB); image routes 64 MiB.

## 5. Settings and env

- **No environment variables exist for the local providers** (confirmed: grep `PROXY_(GUFO|STRATA|LLAMA)` in `src` = 0 hits; README:123 "no environment variables"). Everything is in `settings.json` (`providers.gufo|strata|llama`) or the desktop settings window: `enabled` (default true for all three), `port`, `command`, `cwd`, `apiKey`, `maxConcurrent`, `switchWaitMs`; Gufo `profiles[]`; Llama `modelsDir`, `hfToken`, `binary{mode,source,backend,arch,dir,customPath}`, `profiles[]` (`README.md:123-135,171-197`; `settings.ts:24-29,80-92,175-200`).
- **services.json env needs nothing for local providers.** The hub's `PROXY_*_MAX_CONCURRENT` variables cover only codex, antigravity, claude. Possible additions are optional: `PROXY_MAX_QUEUE` to bound waiting; a `PROXY_TIMEOUT_MS` large enough for local thinking (already 900000 in the hub env).
- **Live settings (confirmed, secrets not read):** all three local providers `enabled: true`, gufo 8081 with five profiles, strata 8080 with the `run-unsloth-ud-iq4_xs.bat` command, llama 8082 with `binary {mode managed, dir D:\LlamaCpp\bin, source unsloth, backend rocm-gfx1151, arch x64}` and both Inkling profiles.
- **Why the live `/v1/models` shows bare aliases (confirmed cause):** the process on 8787 is `ACP Proxy.exe` (PID 18408, the Windows portable app extracted under `%TEMP%\3MQKuP55rUp1b2q71v5h4uDEWf2`, listening on 8787 per `Get-NetTCPConnection`), not `node dist/index.js` from hub.ps1. It was built 2026-11-21 17:12 (`release/ACP-Proxy-Portable-0.1.0-x64.exe`) and healthz uptime was 97 s, so it was just started. The desktop app does not read the hub's `services.json` env. Its own `%APPDATA%\api-acp-proxy\settings.json` has `server.listBareAliases: true`, `timeoutMs: 300000`, `maxBodyBytes: 20971520`, `maxConcurrent: 4`. Env wins over settings (README:88) but only when the env is set in the process that starts the app. Fix options: (a) set `server.listBareAliases: false` (and timeout, body size) in that settings.json or the Server page; (b) run the proxy only through hub.ps1; (c) start the exe from a shell with the env set. Note the desktop app is the only one that can launch local models, so (a) is the consistent choice if the apps must reach local LLMs.
- Port conflict: only one process can hold 8787, so hub.ps1's node proxy and the desktop app are mutually exclusive.

## 6. Known gaps, open items and discoveries that bite an app that drops LM Studio / direct Strata

From `ROADMAP.md:34-43`, AAP-35/36/37/38 `discoveries.md` and the code:

1. **Everything local is UNTESTED live.** AAP-35, 36, 37, 38 all say "live checks UNTESTED"; AAP-38 says no real download, llama-server or ROCm run happened (`README.md:168`, changelog "Not run: M1-M12").
2. **Llama.cpp cannot start today on this PC** (confirmed on disk): `D:\LlamaCpp` has only `models\`, no `bin\` (build not installed; `main.ts:142` would throw "Llama.cpp is not installed"). Downloaded files are `ggml-org\...\Inkling-2-Mini-IQ4_NL.gguf` and `mmproj-...-Q8_0.gguf`, but the saved profile `inkling-2-mini` points at `Inkling-2-Mini-Q8_0.gguf` + `mmproj-...-BF16.gguf` (confirmed in settings.json), and the unsloth folder has the drafter and mmproj but no `Inkling-2-Mini-UD-Q8_K_XL.gguf`. `checkLlamaFiles` would refuse both profiles ("File not found"). `minBuild` 12607 may need raising (AAP-38 changelog).
3. **Flash-Next (Gufo vision) has no model folder** on disk (`D:\Gufo\models` lacks `flash-next-q4`), so `gufo/flash-next-q4` would fail to start.
4. **No embeddings** (section 3). Hard blocker for Scriptorium RAG unless a new proxy feature is built or RAG keeps LM Studio.
5. **No tools / function calling for local models** (`ROADMAP.md:38`, `AAP-38 research.md:143`); any app agent loop that used LM Studio native tool calls fails with 400 `model_not_capable`. (The proxy's tool-calling bridge exists only for the three ACP agents.)
6. **No structured output**: `response_format` is prompt-only + `extractJson`; no GBNF / `json_schema` pass-through to llama-server. Apps that relied on LM Studio's `json_schema` enforcement need their repair step (the hub already sets `json_schema false`).
7. **Sampling control lost**: `temperature`, `top_p`, `seed`, penalties dropped; `top_k`, `min_p`, `repeat_penalty` not forwarded; `stop` is a 400 (`ROADMAP.md:41`, a hard break for any app that sends `stop`). Sampling can only be set per profile in `extraArgs` / Gufo `args`, i.e. one fixed recipe per model (Inkling's is baked in, which is good for it, bad for apps that tune per call).
8. **No context length reported and no prompt-size guard** for local models (`max_prompt_chars` absent). Contexts are small by preset: Qwen 27B 32768, Flash-Next 32768, DeepSeek 16384, Inkling 32768 (the model supports 1M, `AAP-38 research.md:114`). Long book-chunk prompts may overflow with an upstream error.
9. **One model on the GPU, one request at a time per provider, no parallelism**; switches take minutes and block the HTTP request with no progress signal. An app that alternates two local models (for example a chat model and a vision model) thrashes the GPU. Router mode is an open item (`ROADMAP.md:38`).
10. **Strata is a single fixed bat** (one model, id depends on the bat, no profiles, no vision flag, no `kind`); Gufo/Strata/Llama "Strata profiles" is an open follow-up (`ROADMAP.md:39`). The hub's `hub.ps1 start strata <variant>` variants (services.json:171) cannot be chosen through the proxy; only the one command saved in settings runs.
11. **External servers are invisible to the switch logic**: a Strata/Gufo/LM Studio started by hand or by hub.ps1 is passed through but never stopped, so a `llama/*` request can start a second large model next to it (section 1). While LM Studio (1234) is still running its model also holds memory.
12. **Headless CLI cannot launch anything**; the hub's `hub.ps1 start acp-proxy` path therefore cannot serve `gufo/*`, `strata/*`, `llama/*` unless the user starts those by hand (503 `local_server_not_running`).
13. **Timeout 5 min in the desktop app's settings** vs 15 min in the hub env; long local thinking may get 504.
14. **Thinking is always on the wire**: apps get `reasoning_content` separately; there is no per-request thinking-off toggle (`ROADMAP.md:40`). Apps that send `reasoning_effort` get it ignored.
15. **Responses API**: no reasoning items; irrelevant for the hub's apps if they use chat completions.
16. **Small defects that may bite (AAP-37/38 discoveries):** MCP `generate_image` on Gufo image models uses the chat path (wrong); "too old build" message mentions ggml-org/Unsloth even for a custom exe (largely fixed by "custom-exe wording" extra in AAP-38); `sweepOrphans` flake (fixed in AAP-39). Old ACP test flakes are not relevant to apps.
17. **Gufo image path** is complete only for generations and edits without `mask`; `n > 1` unsupported (one image per request).

## Gaps vs LM Studio / direct Strata (list)

1. Embeddings (`/v1/embeddings`, nomic-embed-text-v1.5): missing entirely.
2. Tool calls / function calling to local models: 400.
3. `response_format` json_schema / grammar enforcement: prompt-only.
4. `stop`: 400; `temperature`, `top_p`, `seed`, penalties: silently dropped; `top_k`, `min_p`, `repeat_penalty`: not forwarded. `n>1` 400.
5. Parallel requests: cap 1 per local provider; LM Studio allowed parallel (inferred).
6. Model switching is automatic only in the desktop app; takes minutes, blocks the HTTP call, 10 min start timeout, 30 min queue wait; headless proxy cannot launch.
7. No context size or prompt limit reported; presets use 16k to 32k.
8. Model list for Strata is a single cached id; no JIT model loading by id like LM Studio.
9. Live state on this PC: llama-server not installed, preset model files not on disk, Flash-Next folder missing, everything untested live.
10. Env mismatch: the running desktop exe ignores hub env (bare aliases on, 5 min timeout).
11. External servers (hub.ps1 Strata, LM Studio) are not stopped by the proxy; GPU double-load risk.
12. Image generation exists only for Gufo (Qwen-Image); not for Llama/Strata.

## What the plan needs

- Decide how the proxy is run: desktop exe (required for launching local models) versus hub.ps1 node (cannot). Then align `server.listBareAliases`, `timeoutMs`, `maxBodyBytes` in `%APPDATA%\api-acp-proxy\settings.json` with the hub env, or keep the hub env and make hub.ps1 start the exe with it.
- Proxy-side work items (each would be an AAP ticket in the proxy repo, not hub code): `/v1/embeddings` (new route + an embedding profile concept that does not evict the chat model, or a second always-on server), `stop` support, forwarding `top_k`/`min_p`/`temperature`/`seed`/`response_format` to llama-server, tools for local models, context reporting and prompt-size guard, higher `maxConcurrent` for llama-server with `--parallel`.
- Per-app inventory (not done here): which apps use `stop`, tools, embeddings, `json_schema`, temperature, vision, images against LM Studio/Strata.
- Files: `src/providers/local-openai.ts`, `src/local-models.ts`, `src/local-host.ts`, `src/local-servers.ts`, `src/api.ts` (schema, dropped/unsupported lists), `src/server.ts` (routes), `src/settings.ts`, `src/llama-args.ts`, `src/electron/main.ts`. Tests: `tests/local-openai.test.ts`, `tests/local-models.test.ts`, `tests/local-servers.test.ts`, `tests/llama-args.test.ts`, `tests/controller.test.ts` (names from the AAP-38 changelog).

## Risks

- Moving apps off LM Studio before embeddings and `stop` exist breaks RAG and any app that sends `stop` (400).
- Untested live code: the first real llama-server / Gufo switch may fail on flags that were inferred (README:156,168).
- GPU/RAM contention when external servers coexist with proxy-launched ones.
- Two proxies cannot run on 8787; flipping between the exe and hub.ps1 changes behaviour (aliases, timeouts, launch ability).
- The desktop exe running now lives in `%TEMP%` (portable extract) and its launch state is not under hub.ps1 control (inferred).

## Open questions

1. Does Gufo's `/v1/chat/completions` accept `stop`, `top_k`, `response_format` natively (so forwarding would be enough)? Not checked (no request allowed).
2. Real first-load times for each profile: not documented.
3. Does the Unsloth llama-server need `--jinja` for Inkling's chat template, and does it return `reasoning_content`? The preset sets no such flag; untested.
4. Does hub.ps1 know about the desktop exe at all, or should `services.json` `acp-proxy` change from `node dist/index.js` to the exe? (hub.ps1 not read.)
5. Exact `localBase` defaults for local-provider `maxConcurrent` (live settings say 1; `settings.ts` `localBase` body not read in full).
6. LM Studio's parallelism and JIT behaviour are stated from general knowledge, not read.
