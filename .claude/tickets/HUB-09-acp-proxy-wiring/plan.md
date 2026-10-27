# HUB-09: ACP proxy as a provider in all five apps

**Active** (user revived and widened it, 2026-10-27; was on hold since 2026-10-22: "no need for now, later if needed"). Branch `HUB-09_acp-everywhere`.

## Goal

Scriptorium, Book Translator, VN Studio, Pixel Studio and Chiptune Studio can use models from the user's subscriptions (Codex, Antigravity, Claude) through `api-acp-proxy`, as an `openai-compat` provider `acp`, with a proxy-side cap so parallel jobs from several apps cannot overload a provider.

## Background

- Proxy: `C:\projects\Personal\api-acp-proxy`, hub service `acp-proxy`, port 7461 (its default 8787 is flow-mcp's panel), `PROXY_IGNORE_SAMPLING=1` (AAP-05, merged; it drops `stream_options`, `max_tokens`, `temperature`, which the apps send).
- AAP-25 (branch `AAP-25_provider-concurrency-cap`, commit acef8a3, dist rebuilt, **not merged**): per-provider FIFO cap. Env `PROXY_MAX_CONCURRENT`, `PROXY_MAX_QUEUE`, `PROXY_CODEX_MAX_CONCURRENT`, `PROXY_ANTIGRAVITY_MAX_CONCURRENT`, `PROXY_CLAUDE_MAX_CONCURRENT`; `/healthz` shows `providers.<id>.{active,queued,max_concurrent,max_queue}`.
- Decision (user, 2026-10-22): no Antigravity login inside the apps; the proxy only, accepting the terms risk in the hub `ROADMAP.md` ("Antigravity models and the ACP proxy"). If Antigravity is used, use an account the user can afford to lose, not the one with the Flow Pro plan.
- Limits: text only, no JSON schema (apps use prompt + repair), each request a fresh agent session. Usage numbers are present in the replies (checked 2026-10-27), but local providers show cost 0.
- Load test (2026-10-27, 30 requests, `runs/hub09-acp-load-test.md`): codex clean to 6 in parallel with no slowdown; antigravity clean to 6 but latency doubles at 4+ (3.9 s alone, about 8 s at 4 to 6). No 429 seen. Recommended app concurrency: codex 4, antigravity 3; proxy cap 4.
- Models (`/v1/models`): codex/gpt-6-luna, codex/gpt-5.6-terra, codex/gpt-5.6-luna (also without the prefix), antigravity/gemini-4-argon, antigravity/gemini-3.8-flash.
- Add-provider UI for Pixel Studio and Chiptune Studio: PAR-14 (`PAR-14_acp-custom-providers`) and MDI-07 (`MDI-07_acp-custom-providers`), unmerged; their migration skips an existing `acp`. Their master already parses `openai-compat` entries with `json_schema`, `concurrency`, `discover` and `models`.

## Done (2026-10-27)

- [x] `services.json` acp-proxy: env `PROXY_MAX_CONCURRENT=4`, `PROXY_CODEX_MAX_CONCURRENT=4`, `PROXY_ANTIGRAVITY_MAX_CONCURRENT=3`, note updated. Proxy restarted with `hub.ps1`; `/healthz` shows the providers block with those caps; `/v1/models` answers; one tiny chat per provider returned "OK".
- [x] Live `config/providers.md` of all five apps: `acp` entry enabled, `concurrency: 4`, `json_schema: false`, `discover: true`, the five model ids listed (Pixel and Chiptune: new entry, `tools: false`). Backups `providers.md.bak-2026-10-27` next to each. Each file parses with its app's own `providersSchema`. No role or model selection was changed, no role points at `acp`.
- [x] The apps were not started.

## Left (not done, each needs the user's go-ahead or a merge)

- [ ] 1. One real request from each app through the proxy (app level, not curl): Book Translator (one page, translator agent on an `acp/...` model), Scriptorium (one role on an `acp/...` model, one job; never start Scriptorium without asking), VN Studio (a text role), Pixel Studio and Chiptune Studio (a chat or an agent turn on an `acp` model). Note speed, errors, the JSON repair rate, the cost display.
- [ ] 2. Merge `AAP-25_provider-concurrency-cap` (api-acp-proxy), `PAR-14_acp-custom-providers` (pixel-art-generator), `MDI-07_acp-custom-providers` (midi-generator), then restart the proxy from the merged build. Until AAP-25 merges, the hub instance runs the capped build from the branch.
- [ ] 3. The packaging tickets SCP-47 (Scriptorium) and VNO-50 (VN Studio): merge them, and check that the packaged apps read the same user data `providers.md`.
- [ ] 4. Pixel and Chiptune before PAR-14 / MDI-07 merge: their live file already holds the entry, which the migration then skips; check the Settings screen shows it once merged and started.
- [ ] 5. Problems in the proxy go to `api-acp-proxy/ROADMAP.md`; in an app, to its own `ROADMAP.md`.

## Acceptance

- One real request from each of the five apps answered through the proxy, with no 400s.
- Under parallel load from several apps the proxy queues instead of failing (`/healthz` `queued` rises, no 429).
- The providers entry documented with real model ids (done).

## History

- 2026-10-22: plan written and put on hold. Original scope: Scriptorium and Book Translator only, steps: install the provider server(s) and log in (the user), set port 7461 and ignore-sampling, back up both apps' `providers.md`, add the `acp` entry, one request from each app, note speed/errors/repair rate/cost, update `services.json` and the roadmap.
- 2026-10-27: user revived and widened it to all five apps. AAP-25 cap added in the proxy; load test run; live configs wired; this plan rewritten.

## Status (2026-10-27, end of day)

All five apps pass on acp end to end (real app, real proxy): Scriptorium (SCP-48 real job, 14 jobs), Pixel Studio (PAR-15, codex 3/3, gemini 3/3), Chiptune Studio (MDI-08, codex 3/3, gemini 3/3), Book Translator and VN Studio (earlier app-level checks in `runs/hub09-acp-load-test.md`). Details and open items: "Full UI checks (2026-10-27)" there.

Branches awaiting PRs (nothing pushed or merged):
- api-acp-proxy: AAP-26 (`70e7740`, hides bare ids; `PROXY_LIST_BARE_ALIASES=0`)
- pixel-art-generator: `PAR-15_acp-live-ui-check` (`88cecf7`, `6d2a171`, `ac5c1e2`)
- midi-generator: `MDI-08_acp-live-ui-check` (`e403948`, `7c73e6e`, `c89d2cc`, `d442616`, `ce81908`)
- scriptorium: `SCP-48_single-idea-run` (`d3eb599`, `edb4bcc`)
- creative-hub: `HUB-09_bare-aliases`
Still open: Claude provider, `gpt-6-luna` / `gpt-5.6-terra` / `gemini-4-argon`, native tool_calls in Pixel, Scriptorium Models dialog UI, art and melodies not looked at or listened to.
