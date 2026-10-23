# Handoff: HUB-15 post-merge live checks

Written 2026-10-23 at the end of the session that ran the hub's live checks, three productions and four rounds of tool fixes. Plan: `plan.md` next to this file.

## State at the end of 2026-10-23

- **Repos:** all nine on `master`, pulled, clean. Merged today: scriptorium PR #11 (SCP-20 to SCP-37), book-translator PR #13 (BTT-15 to BTT-20), visual-novels-orchestrator PR #12 (VNO-20 to VNO-35), flow-music-mcp PR #6 (FMM-13 to FMM-16), creative-hub PR #8 (records, HUB-14). Fix worktrees and local fix branches are removed.
- **Tests on master:** Scriptorium 629 + recovery 1, Book Translator 313, VN Studio 930 (typecheck and lint clean in all three), flow-music-mcp 154 + tsc, hub planner 15/15.
- **Services:** rebuilt from master; running: scriptorium (7341, factory idle, $0.23 spent today), vn-studio (7459), flow-music-mcp (7462, Chrome signed in), comfyui, chiptune-studio, pixel-studio, vibetts. book-translator built, not running. Seed updates applied at start: VN Studio `config/studios.md` (fixed `flowRepo`), Scriptorium screenplay prompts (SCP-29).
- **User config changed today (by the user's choice):** `~/Scriptorium/config/settings.md` fallbacks start with `deepseek/deepseek-flash`; three failed start jobs moved to `.claude/temp/scp-failed-starts/`.
- **Credits:** Flow 858 (192 spent on the film), Flow Music 13,169.

## Productions waiting for the user (C6)

| Run log | What | Play / watch |
|---|---|---|
| `runs/the-lighthouse-that-kept-lists-2.md` | HUB-11 film, 123 s | `Start-Process 'C:\projects\Personal\creative-hub\runs\the-lighthouse-that-kept-lists-2\video\out\final.mp4'` (media is local only, git-ignored) |
| `runs/the-winter-garden-clock.md` | HUB-10 puzzle VN (Murdle + Knights and Knaves) | Ren'Py, slug `the-winter-garden-clock` |
| `runs/the-lighthouse-that-kept-lists-vn.md` | HUB-06 VN adaptation | slug `the-lighthouse-that-kept-lists-vn` (some CGs merge two people) |
| `runs/hub07-flow-test.md` | HUB-07 Flow art, voices, music | slug `hub07-flow-test` (6 hr clips missing, C5) |
| `runs/hub08-13-autostart.md` | HUB-08/13 auto-start, chiptune SFX | slug `hub08-13-autostart` |

Ren'Py: `& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\<slug>\game"`.

## How to work (lessons from 2026-10-23)

- MCP links to the hub services may be down in a new session: call tools with `pwsh -NoProfile -File scripts\hub.ps1 call <service> <tool> '<json>'` (or `@file.json`); calls get 660 s.
- The auto-mode permission check refuses some actions without the user's explicit word: starting Scriptorium, editing the user's data config (`~/Scriptorium`, `~/VisualNovels`), and at first pushing. Ask the user; do not work around it.
- Client tasks: only lease tasks with your own `book` / `slug`; several productions can share the services.
- File-writing tools in this environment have collapsed backslashes (`\f` became a form feed in a Windows path twice): read back any path or regex written.
- Tool fixes: plan in the tool repo's `.claude/tickets/`, `implement` skill with `implementer` agents, one commit per ticket, worktree when the app is running from the main checkout.
- Large media under `runs/*/video/*/` is git-ignored.

## Next step

Start with C1 and C3 of `plan.md` (two Scriptorium books, Claude as the client, stop at the book plus import); C5 after about 09:00 on 2026-10-24; ask the user for C6 verdicts.
