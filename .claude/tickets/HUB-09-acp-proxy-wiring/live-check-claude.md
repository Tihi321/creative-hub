# HUB-09 live check: Claude provider through the ACP proxy (2026-11-01)

Result: Claude enabled in the proxy and checked directly through the proxy. The user accepted the terms risk explicitly (2026-11-01).

## What was done
- `claude auth status`: logged in (claude.ai, Max subscription).
- `services.json` acp-proxy env: added `PROXY_CLAUDE_ENABLED=1`, `PROXY_CLAUDE_ACCEPT_TERMS=1`, `PROXY_CLAUDE_MAX_CONCURRENT=2`. The proxy's `settings.json` still says `providers.claude.enabled: false`; the env vars override it, so it was left alone.
- Proxy restarted with `hub.ps1 stop/start acp-proxy`. `/healthz` now lists `claude` (cap 2). `/v1/models` lists claude/default, opus, fable, sonnet, haiku, claude-haiku-4-5-20251001, claude-sonnet-5, claude-opus-5, claude-fable-5, claude-opus-4-8, -4-7, -4-6, claude-sonnet-4-6.
- Added `claude/claude-sonnet-5` (family claude, context 200000; `tools: false` for Pixel and Chiptune) to the `acp` entry in `config/providers.md` of Scriptorium (~\Scriptorium), Book Translator (~\BookTranslator), VN Studio (~\VisualNovels), Pixel Studio (~\PixelStudio), Chiptune Studio (~\ChiptuneStudio). These are user data dirs, not repos, so no PR there.

## Table
| App | Check | Result |
|---|---|---|
| Proxy | `POST /v1/chat/completions` model `claude/claude-sonnet-5`, "Reply with exactly: OK" | PASS (reply "OK") |
| Book Translator | model id in providers.md; app not running, prompt sent straight to proxy with the same id | PASS (proxy level); app UI UNTESTED |
| VN Studio | same | PASS (proxy level); app UI UNTESTED |
| Pixel Studio | same (app was up, UI path not driven) | PASS (proxy level); app UI UNTESTED |
| Chiptune Studio | same | PASS (proxy level); app UI UNTESTED |
| Scriptorium | config edited, never started | UNTESTED |

Note: the proxy reported ~48k prompt tokens for a one-line prompt (Claude Code's own system prompt overhead), so every call is heavy on the subscription.
