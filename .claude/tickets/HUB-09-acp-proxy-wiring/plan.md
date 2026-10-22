# HUB-09: ACP proxy as a provider for Scriptorium and Book Translator

**On hold** (user, 2026-10-22: "no need for now, later if needed"). Start only when the user asks.

## Goal

Scriptorium and Book Translator can use models from the user's subscriptions (Antigravity, Codex, Claude) through `api-acp-proxy`, as an `openai-compat` provider.

## Background

- Proxy: `C:\projects\Personal\api-acp-proxy`, hub service `acp-proxy`, port 7461, `PROXY_IGNORE_SAMPLING=1` (AAP-05, merged; it drops `stream_options`, `max_tokens`, `temperature`, which both apps send). Never tried with a real request.
- Decision (user, 2026-10-22): no Antigravity login inside the apps; the proxy only, accepting the terms risk in the hub `ROADMAP.md` ("Antigravity models and the ACP proxy"). If Antigravity is used, use an account the user can afford to lose, not the one with the Flow Pro plan.
- Limits: text only, no JSON schema (apps use prompt + repair), no usage numbers (cost shows 0), each request a fresh agent session.

## Steps

- [ ] 1. The user installs the provider server(s) they want in the proxy (Antigravity: `npm run antigravity:install` or the app's button), acknowledges the terms and logs in. Claude does not do any Google login.
- [ ] 2. In the proxy's settings: port 7461 and "Ignore sampling fields" on (or rely on the hub's env vars). `hub.ps1 build acp-proxy`, `hub.ps1 start acp-proxy`; `GET http://127.0.0.1:7461/healthz` and `/v1/models` answer.
- [ ] 3. Back up both apps' `config/providers.md`, then add the `acp` entry from the hub `ROADMAP.md` with model ids from `/v1/models`. Book Translator and Scriptorium reload providers.md without a restart (BTT-11, SCP-14).
- [ ] 4. One Book Translator request: a tiny project (one page) with the translator agent on an `acp/...` model. One Scriptorium request: a role on an `acp/...` model for a single job the user agrees to (Scriptorium is already running, or started with the user's go-ahead).
- [ ] 5. Note speed, errors, the JSON repair rate and the cost display. Problems in the proxy go to `api-acp-proxy/ROADMAP.md`; in the apps, to theirs.
- [ ] 6. Update `services.json` note and the hub `ROADMAP.md`.

## Acceptance

- One real request from each app answered through the proxy, with no 400s.
- The providers entry documented with real model ids.
