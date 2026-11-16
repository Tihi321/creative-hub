---
status: done
request: REQ-0025
repos: [creative-hub]
branch: HUB-35_usage-limit-status
updated: 2026-11-16
---
# HUB-35: `hub.ps1 status` shows a provider that hit its usage limit

Request: `REQ-0025`, bug 7. Depends on the proxy's AAP-31
(`C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-31-usage-limit\plan.md`, branch `AAP-31_usage-limit`), which
adds `providers.<id>.exhausted_until` to `/healthz`. Research: the same AAP-31 folder, `research.md`.

## Scope

- `Get-Health` already makes the one request to `services.json`'s `http` URL (acp-proxy: `http://127.0.0.1:8787/healthz`,
  `services.json:179`). It also returns `Notes`: one string per `providers.<id>` that has `exhausted_until`.
- `Show-Status` prints each note under the table, Yellow, like the existing `Note:` lines:
  `Note: acp-proxy: codex hit its usage limit until 2026-11-29 11:07; its models answer 429 usage_limit_exceeded.`
  The time is shown in local time, `yyyy-MM-dd HH:mm`.
- No extra request, no new column. A proxy without AAP-31 (no field) prints nothing new.

## Out of scope

- A rule in the production skills (make-visual-novel, make-video, make-edu-game) to check this before choosing
  `acp/codex` roles: the consumer side is Scriptorium's bug-2 ticket (SCP, planned separately), which reads the 429.
- Any change in the proxy (AAP-31) or in `services.json`.
- `hub.ps1 start` behaviour: an exhausted provider is still a running proxy (`up`).

## Files and modules

| File | Change |
|---|---|
| `scripts/hub.ps1:180-195` (`Get-Health`) | after the `model` parse (`:188-189`), read `$h.providers` (a PSCustomObject; iterate `PSObject.Properties`); for each with `exhausted_until`, add a note; return `[pscustomobject]@{ Ok; Model; Notes = @(...) }` (also `Notes = @()` in both other branches, `:192`, `:194`); update the comment above it |
| `scripts/hub.ps1:244-260` (`Show-Status`) | keep `$hl` notes per row (e.g. `$health += [pscustomobject]@{ Id = $s.id; Notes = $hl.Notes }`); after the `$silent` loop (`:258-260`), print `Note: <id>: <note>` Yellow |
| `ROADMAP.md:39` | the task row below (the director adds it) |
| `runs/ash-and-brass.md` | one line: bug 7 handled by AAP-31 + HUB-35 (the director or the run's owner) |

PowerShell 7.6 (`pwsh` on this machine) turns an ISO string with `Z` into a `[datetime]` of Kind `Utc` in `ConvertFrom-Json`
(checked 2026-11-15). Convert with: `$t = if ($v -is [datetime]) { $v.ToLocalTime() } else { [DateTimeOffset]::Parse([string]$v).LocalDateTime }`,
then `$t.ToString('yyyy-MM-dd HH:mm')`. If parsing fails, print the raw value instead (never throw out of `Get-Health`).
A time already past is skipped (the proxy drops it lazily anyway).

## Tasks for workers

1. **`Get-Health` notes** (input: `/healthz` JSON per the Contract; output: `Notes` string array; contract: one request,
   never throws, empty array when there is no `providers` or no `exhausted_until`).
2. **`Show-Status` print** (input: `Notes` from task 1; output: Yellow `Note:` lines after the `no-http` notes).
3. **Check** (no hub test suite exists): run the stub check below, then the normal `pwsh -File scripts\hub.ps1 status`
   against the live services (read-only: status makes only GET requests). No restart of the proxy.

## Contract

Identical in AAP-31's plan. HUB-35 reads only the `/healthz` field; the 429 body is listed for completeness.

Refusal (and the first failing request), HTTP:

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 1203420

{
  "error": {
    "message": "Codex has hit its usage limit; it resets at 2026-11-29 11:07 (local time). Use another model or wait.",
    "type": "rate_limit_error",
    "param": "model",
    "code": "usage_limit_exceeded",
    "provider": "codex",
    "exhausted_until": "2026-11-29T10:07:00.000Z",
    "retry_after": 1203420
  }
}
```

- `provider`: the provider id (`codex`, `claude`, `antigravity`), the prefix of the model id.
- `exhausted_until`: ISO 8601 in UTC (`Z`), always present. `retry_after`: whole seconds from now, at least 1, always
  present, equal to the `Retry-After` header.
- `message` is for people; do not parse it.
- A stream refused before it starts gets this same HTTP answer (JSON, not SSE). Only a stream whose first request fails
  mid-turn gets it as an SSE event `data: {"error": {...same object...}}` with no `Retry-After` header.

`/healthz` (unauthenticated) and `/v1/models`:

```
GET /healthz
{ "status": "ok", "uptime_seconds": 28994,
  "providers": { "codex": { "active": 0, "queued": 0, "max_concurrent": 4, "max_queue": 0,
                            "exhausted_until": "2026-11-29T10:07:00.000Z" } } }

GET /v1/models
{ "object": "list", "data": [ { "id": "codex/gpt-6-luna", "object": "model", "created": 0, "owned_by": "openai",
                                "exhausted_until": "2026-11-29T10:07:00.000Z" } ] }
```

`exhausted_until` is absent when the provider is not exhausted (including after the time has passed).

## Acceptance criteria

| # | Criterion | Proven by |
|---|---|---|
| H1 | A `/healthz` with `providers.codex.exhausted_until` gives the Yellow note with the local time | stub check, case 1 |
| H2 | Today's `/healthz` (no field, `providers` present) and a body with no `providers` give no note and no error | stub check, cases 2-3 |
| H3 | A non-JSON or failing URL still gives `Ok`/`no-http` as in HUB-34 | stub check, case 4 |
| H4 | `hub.ps1 status` against the live services prints the same table as before (no new note while nothing is exhausted) | live run, read-only |
| H5 | After AAP-31 is deployed and Codex is exhausted, status shows the codex note | live run after the deploy; UNTESTED until then |

## Reproduction (fails before the fix)

Stub check, as a scratch script in `.claude/temp/hub-35/` (not committed): load `Get-Health` from `scripts/hub.ps1` with
the PowerShell parser (`[System.Management.Automation.Language.Parser]::ParseFile`, find the `FunctionDefinitionAst`
named `Get-Health`, invoke its text), start an `HttpListener` on a free port (e.g. 18787, never 8787) answering in turn:
(1) the Contract `/healthz` with `exhausted_until` an hour from now, (2) today's live `/healthz` shape without the field,
(3) `{"status":"ok"}`, (4) `not json`. Today case 1 returns no `Notes` (the property does not exist), so the check fails;
after the fix it returns one note with the local `yyyy-MM-dd HH:mm`. Cases 2-4 return `Notes` empty and `Ok` true.

## ROADMAP.md entry (the director adds it, a task row after row 27)

```
| 28 | HUB-35 | `hub.ps1 status` prints a Note when a subscription provider of the ACP proxy hit its usage limit (from `/healthz` `providers.<id>.exhausted_until`, no extra request) (`.claude/tickets/HUB-35-usage-limit-status/plan.md`, REQ-0025 bug 7) | hub (`scripts/hub.ps1`), `api-acp-proxy` (AAP-31 on `AAP-31_usage-limit`) | AAP-31 merged and the proxy restarted after REQ-0024 ends and the user says go | Planned (2026-11-15) |
```

## Deploy note

`hub.ps1` changes take effect on the next run; nothing restarts. The note can appear only once AAP-31 runs in the proxy:
**restart the proxy only after REQ-0024's production has finished and the user says go** (never from this ticket).
Merge HUB-35 after AAP-31 or with it; before AAP-31 it is harmless (prints nothing new).
