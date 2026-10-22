# HUB-12 changelog

2026-10-22, branch `HUB-02-13_roadmap-tasks`, commit 2c97b21.

- `scripts/hub.ps1` `start` launches the tool detached through WMI (`Win32_Process.Create`, `cmd /d /c` with `1>>out.log 2>>err.log`), so `start` returns when its output is piped. Environment variables go through `Win32_ProcessStartup`; `-Window` shows the window.
- `call` serialises its arguments with `ConvertTo-Json -Depth 100 -Compress`, so deep arguments (puzzle cores, story JSON) reach the tool whole.
- Logs are appended to at each start instead of overwritten.

Verified: every tool call of this run went through `hub.ps1 call` while the MCP links were down; book-translator, vn-studio, comfyui and scriptorium were started from a piped shell.
Not verified: a start with `-Window` from a piped shell.
