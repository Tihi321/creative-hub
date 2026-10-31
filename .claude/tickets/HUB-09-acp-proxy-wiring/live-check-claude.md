# HUB-09 live check: Claude provider through the ACP proxy (2026-10-31)

Result: NOT RUN for all apps. The Claude provider is disabled in the proxy and I did not enable it (see Blocker).

## State found
- `hub.ps1 start acp-proxy`: up on 7461 (pid 18104). `/healthz` lists only `codex` (cap 4) and `antigravity` (cap 3); no `claude`.
- `/v1/models` lists the same 5 codex/antigravity ids, no `claude/*`.
- `~/AppData/Roaming/api-acp-proxy/settings.json`: `providers.claude = {"enabled": false}` (no terms acknowledgement, no credentials set).
- `POST /v1/chat/completions` with `claude/default`: 404 `model_not_found` ("The model 'claude/default' does not exist."). Expected while disabled.

## Blocker (needs the user)
Enabling Claude needs `PROXY_CLAUDE_ENABLED=1` plus the terms acknowledgement (`PROXY_CLAUDE_ACCEPT_TERMS=1` or `termsAcknowledgedAt`), and a login (`claude auth login`, or API key / OAuth token). The proxy README says a Claude subscription through third-party tooling may conflict with Anthropic's consumer terms. The hub only records the user's accepted risk for Antigravity (2026-10-22), not for Claude, so I did not accept it for them. Also no `claude` login or API key was verified.

To run it after the user agrees: add `PROXY_CLAUDE_ENABLED=1`, `PROXY_CLAUDE_ACCEPT_TERMS=1` (and `PROXY_CLAUDE_MAX_CONCURRENT`) to the acp-proxy env in `services.json`, run `claude auth login` if needed, restart the proxy, `GET /v1/models` for the real `claude/<id>` list, then add that model id to each app's `acp` entry in `config/providers.md` and send one tiny prompt per app.

## Table
| App | Provider check | Result |
|---|---|---|
| Scriptorium | claude/* via acp | UNTESTED (never started; also Claude disabled) |
| Book Translator | claude/* via acp | UNTESTED (provider disabled in proxy) |
| VN Studio | claude/* via acp | UNTESTED (provider disabled in proxy) |
| Pixel Studio | claude/* via acp | UNTESTED (provider disabled in proxy) |
| Chiptune Studio | claude/* via acp | UNTESTED (provider disabled in proxy) |
| Proxy itself | claude/default direct | FAIL as expected: 404 model_not_found (disabled) |

No bugs found. Services started by this check: acp-proxy only (left running).
