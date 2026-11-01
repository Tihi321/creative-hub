# HUB-22 handoff (2026-11-01)

## State
All code is merged to `master` of `C:\projects\Personal\edu-game-studio` (last merge: EGS-54 #44). Hub PR #22 (`HUB-22_edu-german`) carries the roadmap rows, the make-edu-game skill, the plan, changelog, this handoff and the run logs. Edu Studio is running on port 7463 from the main checkout build (restarted 22:05 with EGS-53). Live courses in `C:\Users\Infplane\EduGames\courses\`: `deutsch-a1-pilot` (published), `deutsch-a2-smoke`, `deutsch-b1-smoke`, `deutsch-b2-smoke`, `suncev-sustav` (rebuilt). See `changelog.md` for results and the DONE / NOT DONE / UNTESTED list.

## What the user must do
Play `deutsch-a1-pilot` (open `...\courses\deutsch-a1-pilot\build\index.html`), look at the new start screen on a phone-size window, read one B2 text in `deutsch-b2-smoke`, judge the German. A production is done only when the user has played it: do not mark HUB-22 done before.

## Open items
- Mark HUB-22 done in ROADMAP only after the user played the pilot.
- HUB-23 (role-play generator, EGS-39) and HUB-24 (test diet, EGS-40..46) are next; EGS-54 (bot speed) is open.
- `deutsch-a1-pilot` last pipeline step `summarize` was left waiting for a client task (harmless).
- The old data folder backup (before the stale-engine incident) is in `.claude/temp/edu-data-backup/`; only `providers.md` `search_order: [client-search, wikipedia]` had user edits and is restored.

## Gotchas learnt
- `hub.ps1 start` can silently find an old engine still running: check the engine process start time against `out/engine/index.js`; kill by process id when needed.
- The studio runs from the main checkout's `out/`; rebuild (vite player, live, engine) and restart after each merged engine change.
- No `git stash` with worktrees (stashes are shared). Worktrees `C:\projects\Personal\edu-wt\EGS-*` can be removed (rmdir the `node_modules` junction first, never recursive delete).
- Client-model prompts are 10-15k tokens: workers run out of context; write state to the run log.
