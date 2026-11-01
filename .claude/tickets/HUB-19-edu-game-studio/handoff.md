# HUB-19 Edu Game Studio: handoff (2026-10-31)

## State
All merged. Hub PR #16 (8607f53); edu repo master c4c5294 (includes EGS-23 moss, fb26927). Nothing to merge for this ticket.
Hub services stopped gracefully (edu-studio was already down).

## Pilot: course `suncev-sustav` (solar system)
- Run log with resume steps: `runs/edu-solar-system-pilot.md` (untracked in hub repo).
- Build: `C:\Users\Infplane\EduGames\courses\suncev-sustav\build\index.html`. STALE: rebuild with `edu_build {slug:"suncev-sustav", force:true}`.
- Done: pipeline run 2 published 8.57, lint 0 errors, bot 5/5, 9 chiptune tracks + 5 sfx.
- Not done: 5 RPG pictures (ComfyUI died twice; Strata uses the GPU, free it first). English edition (314 strings in `.claude/temp/en-text.json`; Book Translator was down).
- Config change: `~/EduGames/config/providers.md` search_order is now `[client-search, wikipedia]`.
- Pilot is not "done" until the user plays it.

## Known bugs (edu repo, not fixed)
- Starter agents are not copied when `~/EduGames/agents` already exists.
- Designer prompt says only the quiz is playable.
- `edu_asset_generate` image error message says `media.music.enabled` (wrong flag).
- Pilot log claimed edu-studio is missing from `services.json`: FALSE, it is present on master (id edu-studio, port 7463). Correct the log.

## Housekeeping
- Edu worktrees `-p3`, `-egs19`, `-moss` still exist. `-egs19` and `-moss` have `node_modules` as junctions to `-p3`: `rmdir` the junction (not recursive delete) before removing the worktree.
- Main edu checkout is still on branch EGS-14: switch to master and rebuild.

## Next
1. Edu checkout to master, rebuild; free GPU, start ComfyUI (ask before starting anything heavy), generate 5 pictures; rebuild course.
2. English edition once Book Translator is up.
3. User plays the pilot; fix the three bugs in the edu repo on ticket branches.
