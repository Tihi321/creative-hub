# HUB-12: `hub.ps1` start and call fixes

## Goal

`hub.ps1 start` returns when called through a pipe, and `hub.ps1 call` sends deep tool arguments intact.

## Background (checked in `scripts/hub.ps1` on 2026-10-22)

- **Start hangs when piped.** Run from Bash as `hub.ps1 start x | tail`, the reader never sees EOF. A managed engine is started with `Start-Process` and `RedirectStandardOutput/Error` to `logs\<id>.*.log` (lines 131-141). That path uses `CreateProcess` with handle inheritance, so the engine inherits pwsh's own stdout (the pipe) and keeps it open after pwsh exits. Seen with Scriptorium `-Window` and a headless `start book-translator`.
- **`call` timeout is already fixed.** The roadmap said 15 s, but `Invoke-Tool` passes 660 s to `tools/call` (line 209). Only `initialize`, `notifications/initialized` and `tools/list` use the 15 s default, which is fine.
- **`call` JSON depth.** `Invoke-Mcp` serialises the request with `ConvertTo-Json -Depth 10` (line 184). The tool arguments sit at depth 3 of the JSON-RPC body (`params.arguments`), so anything below about 7 levels inside the arguments is cut to a string (for example a `vno_create_project` story: book → chapters → scenes → beats → cast). PowerShell only warns.

## Decisions

- Inferred: start managed engines so they inherit no handles from pwsh, but still write their logs. Recommended way: `Invoke-CimMethod Win32_Process Create` (WMI starts the process outside our process tree, with no inherited handles), running `cmd.exe /d /c "<exe> <args> 1>>"<out.log>" 2>>"<err.log>""` in the repo folder, with the engine's env vars passed through a `Win32_ProcessStartup` `EnvironmentVariables` list (the current environment plus the service's `env`, plus the Book Translator token). Hidden window via `ShowWindow = 0`, normal for `-Window`.
- Not chosen: `Start-Process` without redirection (no inheritance, but no logs), and `cmd /c start` (still inherits handles).
- Stop must still work: `Stop-Service1` finds the process by port, so the new parent (`cmd.exe`) does not matter; check that `taskkill /T` from the listener's root still stops Electron (the root walk stops at a different process name, so `cmd.exe` is left; it exits when its child does).
- `-Depth 100` for the request body.

## Steps

- [x] 1. Reproduce: from Bash, `pwsh -File scripts/hub.ps1 start comfy-mcp | cat` hangs (stop it first; comfy-mcp is cheap to restart). Record it. Reproduced 2026-10-22: `start comfy-mcp | cat | tail` did not return in 120 s; returned only after `stop` closed the engine.
- [x] 2. Add a `Start-Detached` function in `hub.ps1` (WMI create as above), and use it in `Start-Service1` for managed engines instead of `Start-Process @p`. Keep the pid in the message (the WMI result has `ProcessId`).
- [x] 3. `Invoke-Mcp`: `ConvertTo-Json -Depth 100 -Compress`.
- [x] 4. Update the header comment (done). Deviation: ROADMAP.md left alone, the orchestrator moves its rows.
- [~] 5. Verify (2026-10-22; book-translator part NOT verified):
  - `pwsh -File scripts/hub.ps1 start comfy-mcp | cat` returns, and the engine stays up after the shell exits.
  - Logs still fill `logs\comfy-mcp.out.log` / `.err.log`.
  - `start book-translator` gets `BOOK_TRANSLATOR_MCP_TOKEN` (MCP `check` passes with the bearer token).
  - `start pixel-studio -Window` opens the window and MCP answers.
  - `stop` stops each of them; `status` shows down.
  - `hub.ps1 call vn-studio vno_story_edit @<file>` (or another tool with deep args) gets the args unflattened: no "depth" warning, and the result reflects the nested values.
  - `Invoke-ScriptAnalyzer` / a parse check reports no errors.
- [x] 6. Committed on the current branch `HUB-02-13_roadmap-tasks` (deviation: not on `HUB-12_hub-script-fixes`, per orchestrator).

## Acceptance

- Piped `start` returns within the wait time, for node and electron engines.
- Logs, env vars, `-Window`, `stop` and `call` behave as before.
- Deep tool arguments survive `call`.

## Verification results (2026-10-22)

- Parse check (`Parser::ParseFile`): 0 errors. PSScriptAnalyzer is not installed (not run).
- `pwsh -File scripts/hub.ps1 start comfy-mcp 2>&1 | cat | tail -8` returned in 8.4 s (before the fix: hung). Engine stayed up (port 7460, node); `logs\comfy-mcp.out.log` has "MCP listening", `.err.log` filled. Logs are now appended, not truncated per start.
- `start vn-studio` and `start pixel-studio -Window` piped through `cat`: both returned; `check` shows vn-studio 66 tools, pixel-studio 71 tools. `-Window` start answered on MCP; the window was not visually inspected.
- `stop comfy-mcp vn-studio pixel-studio` stopped all three, `status` showed down; restarted headless, `check` OK, left running.
- Deep args: against a local echo listener (a temp copy of hub.ps1 pointed at it), `call vn-studio vno_status @deep.json` with 9 levels of nesting sent the body intact (`"extra":{"a":{"b":{"c":{"d":{"e":{"f":{"g":{"h":"leaf"}}}}}}}}`), no depth warning. Against the real vn-studio it returned `no project "nonexistent-hub12"` (no warning; the tool does not reflect nested values).
- NOT verified: `start book-translator` (token env var, headless Electron piped). It started (pid 31384) but exited: `error: another Book Translator engine is using C:\Users\Infplane\BookTranslator (pid 15408)`. `engine.lock` there is stale (Oct 20 23:08) and pid 15408 is now an unrelated svchost.exe. Deleting the lock was denied by the permission system, so it was left. Delete `~\BookTranslator\engine.lock`, then rerun `hub.ps1 start book-translator` and `check book-translator` to finish this item. Unrelated to the fix.
