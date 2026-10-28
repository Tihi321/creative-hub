# HUB-09 ACP proxy live load test

- Date: 2026-10-27. Proxy: api-acp-proxy commit f72e725, port 7461, started with `hub.ps1 start acp-proxy` (already built). Left RUNNING.
- Requests sent: 30 chat requests total (budget 30). Script: .claude/temp/acp-load.mjs; raw output: .claude/temp/codex-burst.json, ag-burst.json.
- Models (GET /v1/models): gpt-6-luna, codex/gpt-6-luna, gpt-5.6-terra, codex/gpt-5.6-terra, gpt-5.6-luna, codex/gpt-5.6-luna, antigravity/gemini-4-argon, antigravity/gemini-3.8-flash.
- Tested: gpt-5.6-luna (codex), antigravity/gemini-3.8-flash. Prompt "Reply with exactly: OK <n>".

## Feature checks (3 requests per provider)
| Check | codex gpt-5.6-luna | antigravity gemini-3.8-flash |
|---|---|---|
| (a) non-stream chat | 200, "OK 1", 2.2 s, usage present | 200, "OK 1", 3.9 s, usage present |
| (b) stream + include_usage + temperature + max_tokens | 200, 6 chunks, [DONE], usage chunk, finish stop, first token 1.9 s | 200, 4 chunks, [DONE], usage, stop, first token 3.9 s |
| (c) `tools` array (1 function) | accepted, 200, model answered in text (no tool call triggered), valid SSE | same, accepted, text answer |
| (d) temperature + max_tokens | no 400 (done within b) | no 400 |

Note: (b) and (d) were combined in one request to save budget; (c) ran without sampling fields. Whether a tool call is ever emitted natively (tool_calls delta) was NOT verified, only that tools is accepted and does not break the stream.

## Bursts (simultaneous streaming requests)
| Provider | N | ok/failed | median total | max total | first token (min-max) |
|---|---|---|---|---|---|
| codex | 1 (from feature check b) | 1/0 | 2.2 s | 2.2 s | 1.9 s |
| codex | 2 | 2/0 | 2.2 s | 2.3 s | 1.9-2.1 s |
| codex | 4 | 4/0 | 2.15 s | 2.24 s | 1.9-2.1 s |
| codex | 6 | 6/0 | 2.09 s | 2.29 s | 1.5-2.2 s |
| antigravity | 1 (from feature check b) | 1/0 | 3.9 s | 3.9 s | 3.9 s |
| antigravity | 2 | 2/0 | 5.3 s | 6.1 s | 4.5-6.1 s |
| antigravity | 4 | 4/0 | 7.7 s | 8.2 s | 6.5-8.1 s |
| antigravity | 6 | 6/0 | 8.2 s | 9.0 s | 7.0-9.0 s |

All HTTP 200, all streams ended with [DONE], no errors. Proxy log grep for rate/429/error/limit/quota found nothing.

Reading: codex shows no slowdown up to 6, so it runs truly in parallel. Antigravity latency grows with N (3.9 s alone, ~8 s at 4-6), so it queues or serialises partly upstream (wall time for 6 is about 2x a single call, still better than serial 6x).

## Recommendation
- App config `concurrency`: codex 4 (verified clean to 6); antigravity 3 (verified clean to 6, but latency doubles at 4+; 3 keeps first-token under ~7 s).
- Proxy-side per-provider cap default: 4 (queue the rest, do not reject).
- Timeouts are safe with the hub's 900 s; short prompts never approached them.

## Not verified
- Burst of 8 (budget cap; stopped at 6). No rate-limit/429 was ever seen, so the real ceiling is unknown.
- Long generations (big max_tokens, minutes-long streams) under concurrency; only 1-token-class replies measured.
- gpt-6-luna, gpt-5.6-terra, gemini-4-argon not exercised; limits may differ.
- Native tool_calls output, response_format, Claude provider (disabled, not touched).
- Daily quota consumption on the subscriptions beyond these 30 requests.

## Wiring (2026-10-27)

Proxy restarted from the AAP-25 build (acef8a3) with `PROXY_MAX_CONCURRENT=4`, `PROXY_CODEX_MAX_CONCURRENT=4`, `PROXY_ANTIGRAVITY_MAX_CONCURRENT=3`. `/healthz`: `providers.codex` max_concurrent 4, `providers.antigravity` max_concurrent 3 (active 0, queued 0, max_queue 0). `/v1/models` lists the 8 ids above. Smoke (2 requests, "Reply with exactly: OK"): codex/gpt-5.6-luna "OK", antigravity/gemini-3.8-flash "OK", both 200 with usage.

Each `acp` entry: enabled true, concurrency 4, json_schema false, discover true, models codex/gpt-5.6-luna, codex/gpt-5.6-terra, codex/gpt-6-luna, antigravity/gemini-3.8-flash (context 1000000), antigravity/gemini-4-argon (context 1000000). No role or other provider touched. Parse check: each app's own `providersSchema` plus its `yaml` package, all passed.

| File | Backup (same folder) | Change |
|---|---|---|
| ~/Scriptorium/config/providers.md | providers.md.bak-2026-10-27 | existing acp entry enabled, models listed |
| ~/BookTranslator/config/providers.md | providers.md.bak-2026-10-27 | same |
| ~/VisualNovels/config/providers.md | providers.md.bak-2026-10-27 | same |
| ~/PixelStudio/config/providers.md | providers.md.bak-2026-10-27 | new acp entry before `ollama`, models with `tools: false` |
| ~/ChiptuneStudio/config/providers.md | providers.md.bak-2026-10-27 | same |
| creative-hub/services.json | git | acp-proxy env caps and note |
| creative-hub/ROADMAP.md, README.md, .claude/tickets/HUB-09-acp-proxy-wiring/plan.md | git | HUB-09 off hold, docs |

No app was started. Not verified: a real request from any app through the proxy; whether each app shows the entry in its UI; Pixel and Chiptune were parse-checked with the PAR-14 / MDI-07 branch schema (their checked-out branches), not master.


## App-level checks (2026-10-27)

Proxy on 7461 (healthz ok, active 0 before and after each call; the user's 8787 proxy untouched). 7 LLM requests in total, all free (`cost_usd` 0). Apps were down before; each was started with `hub.ps1 start` and stopped afterwards. Builds were current (Pixel out/main 21:35, Chiptune 21:41, VN 21:16, all after their last merge; Book Translator out/engine 10-25 13:16, only docs commits since).

Pixel Studio and Chiptune Studio have no MCP tool that calls an LLM (their agent runs from the UI over IPC). Those two were checked through the app's own LLM layer (`src/llm`: `createLlm`, which reads the live `~/PixelStudio` / `~/ChiptuneStudio` `config/providers.md`, then `router.chatFn` and `chatJson`) run with tsx from the app repo, with the app's MCP server up. The UI agent loop itself and the PAR-14 / MDI-07 settings form were not exercised.

### Book Translator (MCP :47811, bearer token from BOOK_TRANSLATOR_MCP_TOKEN)

| Check | Result |
|---|---|
| Path | `create_project` (txt, one paragraph, en to Croatian, glossary/proofreader/qa off, `agentModels.translator = [acp/codex/gpt-5.6-luna]`, no fallback) then `start_translation`, `wait_for_progress`, `get_chunk` |
| Model named by the app | chunk `model: acp/codex/gpt-5.6-luna` |
| Latency | 2748 ms (project done in about 6 s) |
| Tokens | 11309 in, 112 out, cost 0 |
| Output | "Brodovi su ponovno kasnili, pa je Mara sjedila na hladnom kamenom gatu i promatrala sivu vodu sve dok sunce nije izašlo." |
| Errors / JSON repair | none / not applicable (plain text) |
| Config changes | none (override per project). Left behind: `~/BookTranslator/projects/acp-test-zz` (no delete tool in the MCP) |
| Verdict | PASS |

### VN Studio (MCP :7459)

| Check | Result |
|---|---|
| Path | `vno_create_project` (1 character, 1 place, 1 scene; slug `acp-test-zz`, not run) then `vno_plan {wait: true}`. No per-call model: `~/VisualNovels/config/roles.md` backed up, `art-director` set to `[acp/codex/gpt-5.6-luna]` and `composer` to `[acp/antigravity/gemini-3.8-flash]` (single entry, so no fallback to paid), restored afterwards |
| art-director | job `vn.art.plan` model `acp/codex/gpt-5.6-luna`, 4681 ms, 11734 in / 431 out; spend log row 4650 ms. Wrote 4 sensible image prompts |
| composer (JSON plan, gemini) | job `vn.music.plan` model `acp/antigravity/gemini-3.8-flash`, 9737 ms, 15541 in / 251 out. Wrote 3 music prompts; `vno_plan` total 14.9 s |
| Errors / JSON repair | none, `attempts: 0`, no repair text in either job |
| Restore | roles.md sha256 69fdc788...5a9a67 identical to before; test project deleted with `vno_delete_project`. Job and log records of the test remain in `~/VisualNovels/jobs/done/acp-test-zz--*` and `logs/` |
| Verdict | PASS |

### Pixel Studio (MCP :7457, app llm layer, live `~/PixelStudio/config`)

| Check | Result |
|---|---|
| Registry | provider `acp` available; models `acp/codex/gpt-5.6-luna`, `-terra`, `gpt-6-luna`, `acp/antigravity/gemini-3.8-flash`, `-gemini-4-argon`, plus 3 unprefixed duplicates from `/v1/models` discovery (`acp/gpt-6-luna`, `acp/gpt-5.6-terra`, `acp/gpt-5.6-luna`) |
| codex luna | "Reply with exactly: PONG" returned "PONG", 2200 ms, 10775 in / 6 out |
| gemini-3.8-flash | `chatJson` with a zod schema: `{"color":"red","count":3}`, 17659 ms (cold start; 4450 ms in Chiptune). The reply came wrapped in a ```json fence, so `extractJson` unwrapped it; no repair round trip |
| Errors | none. Config changes: none |
| Verdict | PASS (LLM layer only) |

### Chiptune Studio (MCP :7458, app llm layer, live `~/ChiptuneStudio/config`)

| Check | Result |
|---|---|
| Registry | same 8 acp entries as Pixel |
| codex luna | "PONG", 2384 ms, 10773 in / 6 out |
| gemini-3.8-flash | same JSON in a fence, parsed, 4450 ms, no repair |
| Errors / config changes | none / none |
| Verdict | PASS (LLM layer only) |

### Notes and not verified
- The proxy log lines were not read; confirmation is the apps' own model names, usage and spend rows, plus healthz ok afterwards. healthz counters show only active/queued (idle at every sample), no request totals.
- Gemini wraps JSON in code fences and prepends about 14.6k input tokens (the proxy's agent preamble); `json_schema: false` is therefore right, and the apps' extraction handles it.
- Discovery adds unprefixed duplicate model ids to the list in Pixel and Chiptune (and likely the others); harmless but visible in model pickers.
- Not verified: the Pixel / Chiptune UI agent loop and Settings screens, tool calls (`tools: false` on all acp models), gpt-6-luna, gpt-5.6-terra, gemini-4-argon, the Book Translator glossary/proofreader/QA agents on acp, concurrency from inside an app.
- Test helper scripts are in `.claude/temp/` (mcp.mjs, schema.mjs, llmcheck.mts, vnproj.json, bt-acp-test.txt).

### Scriptorium (2026-10-27)

Factory kept idle with the supported `paused: true` in `~/Scriptorium/config/factory.md` (the scheduler skips all queued jobs while it is set, `src/engine/queue/scheduler.ts:316`). The file was backed up, edited, and restored byte-for-byte (sha256 80e599bb...87ad2b6 before and after). Rebuilt out/ (it was older than HEAD), started with `hub.ps1 start scriptorium -Force` only after confirming the pause. The proxy answered with prefixed ids only before any request.

| Check | Result |
|---|---|
| `acp/codex/gpt-5.6-luna` | `engine probe --model` (real request through Scriptorium's ModelRouter, no factory): "Libraries are quiet gateways to knowledge, imagination, and discovery.", 10777 in (9472 cached) / 16 out, 11.8 s wall incl. node/discovery start, cost shown 0 USD (model not priced as paid) |
| `acp/antigravity/gemini-3.8-flash` | same probe: "Libraries are quiet sanctuaries that preserve human knowledge...", 14640 in / 20 out, 4.2 s wall, cost 0 |
| MCP `list_models` | 21 models, 0 duplicate ids; the 5 acp models listed once each, no unprefixed ids; `factory_status`: paused true, running [], openStories 0, provider acp up |
| Jobs / ideas / books before and after | queued+running empty, 37 ideas, 33 books, unchanged; no throwaway idea created |
| Errors | probe exit code 1 only because the lmstudio embedding step failed (LM Studio is down, unrelated) |

Not verified: a role job run through the factory via MCP (impossible while paused; no per-call run tool exists), paid-model cost display for acp, the Models dialog in the UI (only the MCP list). Scriptorium stopped.

Follow-up, JSON path (2 more requests, one per model, no engine/scheduler running, so no idea or job could start). A throwaway tsx harness (deleted afterwards) built a ModelRouter on the live data dir with one acp model and called the factory's own `chatJson` (`src/engine/pipeline/llm.ts:69`) with a zod schema (3-chapter outline). Paid spend stayed 0 (both models unpaid, cost 0); jobs 0, ideas 37, books 33 before and after; factory.md sha unchanged; no throwaway idea made.

| Model | Result |
|---|---|
| `acp/antigravity/gemini-3.8-flash` | schema sent, 7753 ms, 14673 in / 208 out, valid bare JSON, parsed first time, no repair |
| `acp/codex/gpt-5.6-luna` | schema sent, 4001 ms, 10810 in / 192 out, valid JSON, no repair. Finding: chapter summaries came back in Chinese although the prompt was English (the proxy's codex agent preamble or the model); title and keys were English |

Still not verified: the fenced-JSON/repair branch (neither reply was fenced this time), a job through the real scheduler with job records (the harness skips job files and the job log), the UI Models dialog.

### Scriptorium real job (SCP-48)

2026-10-27. Scriptorium branch `SCP-48_single-idea-run` commit d3eb599 (`only:` in config/factory.md, `--only <slug>`, MCP `set_factory_only`; 4 new tests).
- Setup: roles.md all roles on acp only (writer and humanizer `acp/codex/gpt-5.6-luna`, every other role `acp/antigravity/gemini-3.8-flash`), settings.md fallbacks only the gemini model with `fallback_shared: false`, factory.md `only: zz-scp48-test`. Throwaway idea `zz-scp48-test`, format `bedtime-story` (600-2000 words, 1 chapter). Proxy on 7461 untouched.
- Run: started with `hub.ps1 start scriptorium -Force`; `factory_status.only` showed the idea. The whole pipeline ran in about 2 minutes: eic start, pitch, outline, draft ch01, humanize ch01, 8 reviews, publish = 14 jobs, book `the-truth-lantern` published (1046 words). Stopped right after (it ran past the planned stop point, the 14 jobs ~ 14 LLM requests).
- Models in job records: 12 jobs `acp/antigravity/gemini-3.8-flash`, 2 jobs (draft, humanize) `acp/codex/gpt-5.6-luna`. attempts 0 on all, no fallback, cost_usd 0, today's spend unchanged (2.03 USD before and after).
- Latency (ms): outline 8349, pitch 10920, start 14511, draft ch01 12655 (12257 in / 1429 out), humanize 12162, reviews 10.4-25.5 s (copy-editor 25.5 s), publish 15270. About 15-17k input tokens per job.
- JSON repairs: none recorded (no repair line in the book log; every job attempts 0).
- Language: all English. Draft/humanize by codex/gpt-5.6-luna came back in English; scan of the book and job records for CJK characters found none. The Chinese answer did not reproduce here.
- Before/after: ideas 37 -> 37, books 33 -> 33, jobs done 2777 -> 2777, queued 0, running 0, failed 1 -> 1 (after deleting the throwaway idea, its book folder and its 14 job records). Other books and ideas were not touched during the run (only the throwaway's jobs ran; `booksByStage` showed 33 published + the new one).
- Cleanup: Scriptorium stopped (7341 down). roles.md, settings.md and factory.md restored from `.bak-scp48` (byte-for-byte, sha256 match, backups removed). config/budget.md has a new sha (caps unchanged: 40/20/null/0.8); the engine rewrote it at start, I had no backup of it. Not cleaned: appended lines in logs/agents/*.md, spend log rows, index/library.sqlite (still lists the throwaway until a reindex).

## Full UI checks (2026-10-27)

- Proxy: AAP-26 (api-acp-proxy `70e7740`) hides bare ids via `PROXY_LIST_BARE_ALIASES=0`. `/v1/models` lists only `codex/gpt-6-luna`, `codex/gpt-5.6-terra`, `codex/gpt-5.6-luna`, `antigravity/gemini-4-argon`, `antigravity/gemini-3.8-flash`. Bare ids still route.
- Pixel Studio PAR-15 (pixel-art-generator branch `PAR-15_acp-live-ui-check`: `88cecf7`, `6d2a171`, `ac5c1e2`): the real Electron app driven by the Playwright spec `tests/e2e/acp-live.spec.ts` (`ACP_LIVE=1`, `ACP_REPEAT=N`, temp home seeded from the real config). Settings form: a) prefixed ids only, b) add / Test / detect / remove pass. Agent "draw a 16x16 red heart": final `ACP_REPEAT=3` run codex 3/3 (12-14 s), gemini 3/3 (53-73 s). Earlier batches this round: codex 1/3 and 2/3 (failed draw calls ending the run, fixed by the failed-last-action guard), and one run where the last call succeeded but the canvas stayed empty (not caught by the guard). Twice the gemini option was missing from the chat model list right after a codex failure (cause not found; the spec now logs the options). Fixes: provider edit lock, refusal nudge (`NO_TOOLS_REFUSAL`, max 2), 2 JSON repair retries, failed-last-action guard (`MAX_ERROR_NUDGES=2`). Native tool mode is not covered by the guard.
- Chiptune Studio MDI-08 (midi-generator branch `MDI-08_acp-live-ui-check`: `e403948`, `7c73e6e`, `c89d2cc`, `d442616`, `ce81908`): same spec style. Reliability before the guard: JSON-action 6/6 vs native tools 5/6 (slower), so acp stays `tools: false`. After restoring the spec (`c89d2cc` had collapsed it to one line, `d442616` restored it) and the parity fixes: `ACP_REPEAT=3` codex 3/3 (9.9-21.3 s), gemini 3/3 (22-47 s). Fixes: migration places acp before mock with seed comments, `removeProvider` resets the chat model, file lock, the form selects the new provider, refusal nudge + guard same as Pixel. The nudges did not trigger live (unit-tested only). `genesis.test.ts` timing failure also on master.
- Scriptorium SCP-48 (scriptorium branch `SCP-48_single-idea-run`: `d3eb599`, `edb4bcc`): factory `only` filter (`factory.md` `only`, `--only`, `set_factory_only`); start gates scoped to the idea after checker review. A real throwaway bedtime story ran 14 jobs on acp (gemini flash + codex luna), no JSON repairs, cost 0, English; counts unchanged; cleaned up.
- Codex Chinese output: not reproduced in 4 requests nor in the SCP-48 run; the proxy keeps the system message; no language config found. Treated as a one-off.
- Open / not verified: Claude provider, `gpt-6-luna` / `gpt-5.6-terra` / `gemini-4-argon`, native `tool_calls` in Pixel, the Scriptorium Models dialog UI, nobody looked at the art or listened to the melodies.
