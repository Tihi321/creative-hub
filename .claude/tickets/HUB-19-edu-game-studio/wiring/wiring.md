# HUB-19 phase 7: hub wiring (a described step, not applied)

Why not applied: the hub's `README.md`, `ROADMAP.md` and `.claude/skills/make-visual-novel/SKILL.md` carry the user's uncommitted edits on another branch, and this run may only write inside this ticket folder. The drafts are in this folder (`wiring/`). Apply them on a hub branch named after the ticket (for example `HUB-19_edu-studio`), after the other branch is merged, and ask before committing.

Checked on 2026-10-31 in the studio worktree `edu-game-studio-p3`: `node out/engine/index.js --mcp-only --port 7499 --data <temp>` printed `MCP listening`, an MCP client (SDK, Streamable HTTP) connected, `tools/list` returned 43 tools (before the EGS-18..21 tools) and `edu_status` answered; the engine was stopped and the temp data removed. `hub.ps1 check` itself was not run (the service is not registered yet).

## Steps

1. `services.json`: add `services.edu-studio.json` to `services` (after `vn-studio`). Decide the `repo` first: the integrated line lives in the worktree `C:\projects\Personal\edu-game-studio-p3` (branch `EGS-22_integration`, with EGS-18..21 on top); the main checkout `C:\projects\Personal\edu-game-studio` is on `EGS-14_detective`. Point `repo` at the checkout that has the branch the user wants to run, or, after the user merges to a `master`, at `C:\projects\Personal\edu-game-studio`. `yarn build:engine` is what `hub.ps1 build` runs; `yarn` is not on this machine's PATH (use `fnm exec --using=24 yarn ...` or the node binaries).
2. `.mcp.json`: add `mcp.edu-studio.json` under `mcpServers`.
3. `README.md`: add `README-row.md` to the tools table (after `vn-studio`), and `edu-studio` `docs/mcp-guide.md` to the "Docs inside the repos" paragraph.
4. `.claude/skills/make-edu-game/SKILL.md`: copy `SKILL.make-edu-game.md`.
5. `CLAUDE.md`: add `CLAUDE-line.md` next to the other "make ..." lines.
6. `ROADMAP.md`: add `ROADMAP-row.md` as a new row with the next number.
7. Verify: `pwsh -File scripts\hub.ps1 start edu-studio`, then `pwsh -File scripts\hub.ps1 check` lists `edu-studio` with its tool count (43 before EGS-18..21; those add `edu_stt_status`, `edu_android_prepare`, `edu_class_assign`, `edu_class_report`, `edu_live_start`, `edu_live_status`, `edu_live_stop`). A fresh Claude session in the hub makes a one-sentence course through the skill (not run). Book Translator translates a course catalog and the edition builds (not run: Book Translator was down, and the pipeline's editions step is still skipped in the studio).
8. Memory: add a HUB-19 line to the hub's memory index once the user has played the pilot.
