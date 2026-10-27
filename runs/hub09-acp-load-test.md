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
