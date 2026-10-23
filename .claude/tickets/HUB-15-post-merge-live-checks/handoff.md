# Handoff: HUB-15 post-merge live checks

Refreshed 2026-10-23, about 20:15, after C1, C2 and C3. Plan: `plan.md` next to this file (C1, C2 and C3 ticked, with notes). Results: `changelog.md`.

## State

- **Repos:**
  - Hub on `HUB-15_post-merge-live-checks` at `d181f82`, pushed (run logs, plan, changelog).
  - Scriptorium `master` at `d7c4499`, pushed (roadmap SCP-38 to SCP-43).
  - VN Studio (`visual-novels-orchestrator`) `master` at `f73ed28`, pushed (roadmap VNO-36 to VNO-38).
  - All working trees clean. No tool code changed.
- **Services running:** scriptorium (7341), vn-studio (7459), vibetts, flow-music-mcp (7462). Down: book-translator, pixel-studio, chiptune-studio, comfyui and comfy-mcp; C4 needs ComfyUI started.
- **Scriptorium spend today:** about $0.27 of the $5 cap, all on reviewers. Client tasks: none waiting.
- **Credits:** Flow 858, Flow Music 13,169 (unchanged this session).

## Done this session

| Check | Book / project | Result | Run log |
|---|---|---|---|
| C1 VN adaptation | `the-local-patch-2` (from `the-local-patch`), score 7.36, VN Studio preview import | SCP-28, 35, 36 and the SCP-37 target verified; SCP-34 verified for bare weekdays only. New: SCP-38 to 42. | `runs/the-local-patch-2.md` |
| C3 puzzle mystery | `the-trap-room-at-the-lanterna`, score 8.36, imported with the art and music plan (no images) | SCP-30, 31, 33, VNO-26, 29 verified; VNO-30 verified in the data only; SCP-32 not exercised; VNO-25 and VNO-31 partly fixed. New: VNO-36, 37, 38. | `runs/the-trap-room-at-the-lanterna.md` |
| C2 screenplay | `the-local-patch-3` (short-film), score 7.09 at round 2 (round 1 rejected at 6.73 under `max_rounds: 1`; reopened with `reopen_book {mode: "rewrite"}`), runtime 120 s in [60, 180], 18 shots | SCP-29 verified: prompts in seconds, length gate `ok, seconds: 120`, no length rewrite. Filed SCP-43 (short film gets 2 rewrite rounds, user OK); the unused `target_words` not filed. | `runs/the-local-patch-3.md` |

## What is left

1. ~~C2 screenplay~~: done (see above).
2. **C4 Flow and ComfyUI side by side (VNO-28):** start ComfyUI (`scripts\hub.ps1 start comfyui`, plus comfy-mcp if needed). Then run two small VN projects at once, one with `art.provider: flow` and one on ComfyUI, and check that `vno_status` shows an image job of each running at the same time. A candidate is to build C3's `the-trap-room-at-the-lanterna` with Flow images (free) alongside a small ComfyUI project. That would also do C3's optional build for the user to play.
3. **C5 Gemini quota (VNO-24, FMM-15):** after about 09:00 on 2026-10-24, run `vno_run_pipeline {slug: "hub07-flow-test", from: "voice"}` to make the 6 missing Croatian clips, and transcribe two with `flow_transcribe {language: "hr"}`. If the quota runs out again, check for one "daily quota, resets at ..." stop and that `flow_narrate`'s error says "daily".
4. **C6 the user's verdicts:** ask the user to play or watch, and write their notes in each run log.
   - The film `runs/the-lighthouse-that-kept-lists-2/video/out/final.mp4`.
   - *The Winter Garden Clock*.
   - *The Lighthouse That Kept Lists (VN)*.
   - `hub07-flow-test` and `hub08-13-autostart`.
   - *The Trap Room at the Lanterna*, if it gets built.
5. **Then:** the open bugs are tool tickets, not part of this ticket: Scriptorium SCP-38 to 43, and VN Studio VNO-36 to 38 plus its earlier open items. Fix them in each tool's repo, one ticket branch per fix, using the `implement` skill, only when the user asks.
6. **Close HUB-15:** fill `changelog.md`, tick the plan, set the HUB-15 status in `ROADMAP.md`, and open a PR from `HUB-15_post-merge-live-checks` to `master`.

## How to work (lessons)

- **Calling tools:** call service tools with `pwsh -NoProfile -File scripts\hub.ps1 call <service> <tool> '<json>'` (or `'@file.json'`); calls get 660 s. Scriptorium client prompts are large (60 KB or more). Save `get_client_task` output to `.claude/temp/task.json` and pull out only what you need with `node -e`. Submit with `submit_client_task '@.claude/temp/submit.json'`.
- **Helpers in `.claude/temp/`:**
  - `hum.js` makes light humanizer edits.
  - `splice.js` applies edit lists to a chapter file (`chapters/ch-0N.md`) for a rewrite task.
  - `rep.ts` runs `analyzeRepetition` by hand (`npx tsx` from the scriptorium repo).
- **Writing scripts:**
  - Write VN drafts at the full target per chapter, or every chapter gets a grow rewrite (SCP-42).
  - Only `Place, Weekday, time` headings survive. To get "a week later", write `Thursday, before dawn a week later` (SCP-38 workaround).
  - Keep the days running forward.
- **Leasing tasks:** lease only tasks with your own `book` / `slug`.
- **Bash quirk:** a heredoc whose text holds apostrophes failed in the Bash tool here. Submit long text through the MCP tool or the Write tool instead.
- **Asking first:** the auto-mode check refuses some actions without the user's explicit word, such as starting Scriptorium or editing `~/Scriptorium` and `~/VisualNovels` config. Ask the user.
- **Tool fixes:** plan in the tool repo's `.claude/tickets/`, use the `implement` skill, one commit per ticket.

## Next step

Start ComfyUI for C4 (the user said subagents run as the orchestrator's workers; they asked for Sonnet, but only inherit/pro/flash/flash_lite can be picked, and C2 ran on flash).
