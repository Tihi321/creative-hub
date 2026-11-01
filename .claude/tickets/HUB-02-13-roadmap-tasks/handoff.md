# Handoff: hub roadmap run (HUB-02 to HUB-13)

Written 2026-10-22 before the machine was shut down at the user's request. Plan: `plan.md`; PR links: `prs.md`; tool bugs found: `followups.md`.

## State

- Merged on master: scriptorium PR #10 (SCP-16/17/18, roadmap SCP-20 to 25), flow-music-mcp PR #5 (FMM-11/12), book-translator PR #12 (BTT-15 to 20), midi-generator PR #6 (MDI-06).
- Pushed, waiting for the user to merge: visual-novels-orchestrator `VNO-10-19_hub-roadmap` (ef3dcf3: VNO-16, 19, 11, 10, 12, 13, 14, 15, roadmap VNO-20/21; 903 tests) and creative-hub `HUB-02-13_roadmap-tasks` (this run). Links in `prs.md`.
- Hub tickets with changelogs: HUB-02 to 08, 10 to 13. Done and verified: HUB-12, the code of every tool ticket, the HUB-02/03/04/05 productions up to the user's play or read.

## Next, after the user merges both PRs

1. `git pull` on master in creative-hub and visual-novels-orchestrator. Remove the worktree `C:\projects\Personal\visual-novels-orchestrator-wt` (first `cmd /c rmdir` its `node_modules` junction, then `git worktree remove`).
2. `pwsh -File scripts\hub.ps1 build` for vn-studio, scriptorium and flow-music-mcp; start vn-studio and flow-music-mcp. Scriptorium: the user already allowed starting it for this run; check `factory_status` right after and pause ideas nobody asked for.
3. Live checks, each with a run log: HUB-06 H2 (adapt `the-lighthouse-that-kept-lists` to a VN), HUB-08 auto-start, HUB-13 chiptune SFX, HUB-07 Flow provider (up to `flowMusicMaxSongs` 4), HUB-10 phase 5 (first puzzle VN), HUB-11 phase 3 (first video, animatic first, then up to 150 Flow credits).
4. Add VN Studio's own follow-ups to its ROADMAP if the VN branch did not (lost ComfyUI job, partial hr UI strings).

## Waiting on the user to play or read

vno-media-test (HUB-03), the Croatian *Clockless God* VN (HUB-02), the puzzle PoC (`npx tsx scripts/puzzle-poc.ts --play` in VN Studio), *The Umbrella Conductor* (HUB-04), the HUB-05 EPUB.

- 2026-11-01: the user accepted HUB-02, 03, 05, 06, 07, 10, 11, 13 and 17 productions (no redo needed).
