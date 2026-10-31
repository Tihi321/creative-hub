# Handoff: HUB-15 post-merge live checks

Refreshed 2026-10-31 after C1 to C5 (done 2026-10-24). Plan: `plan.md` next to this file (C1 to C5 ticked). Results: `changelog.md`.

## State

- **Repos:** hub branch `HUB-15_post-merge-live-checks` was merged up to `master` (69231fa, fast-forward) on 2026-10-31 and carries the roadmap refresh and this handoff on top. Its earlier tip was `2761783`. PR #14 (HUB-18) is open; this PR should merge after #14. Untracked and not ours: `.agents/`, `.codex/`, `AGENTS.md`, `.claude/tickets/HUB-19-edu-game-studio/`.
- **Services (checked with `scriptshub.ps1 status`, 2026-10-31):** up: acp-proxy (7461), vibetts (7723), comfyui (8188), lmstudio (1234). Down: scriptorium, book-translator, vn-studio, pixel-studio, chiptune-studio, comfy-mcp, flow-music-mcp, strata. Never start Scriptorium without asking.
- **Flow Music:** dropped by the user 2026-10-31. HUB-07 has only the 6 hr clips left, waiting on Gemini daily quota.
- **HUB-09:** done (PRs #12, #13). Claude provider not enabled in proxy; see `.claude/tickets/HUB-09-acp-proxy-wiring/live-check-claude.md`.

## Done this session

| Check | Book / project | Result | Run log |
|---|---|---|---|
| C1 VN adaptation | `the-local-patch-2` (from `the-local-patch`), score 7.36, VN Studio preview import | SCP-28, 35, 36 and the SCP-37 target verified; SCP-34 verified for bare weekdays only. New: SCP-38 to 42. | `runs/the-local-patch-2.md` |
| C3 puzzle mystery | `the-trap-room-at-the-lanterna`, score 8.36, imported with the art and music plan (no images) | SCP-30, 31, 33, VNO-26, 29 verified; VNO-30 verified in the data only; SCP-32 not exercised; VNO-25 and VNO-31 partly fixed. New: VNO-36, 37, 38. | `runs/the-trap-room-at-the-lanterna.md` |
| C2 screenplay | `the-local-patch-3` (short-film), score 7.09 at round 2 (round 1 rejected at 6.73 under `max_rounds: 1`; reopened with `reopen_book {mode: "rewrite"}`), runtime 120 s in [60, 180], 18 shots | SCP-29 verified: prompts in seconds, length gate `ok, seconds: 120`, no length rewrite. Filed SCP-43 (short film gets 2 rewrite rounds, user OK); the unused `target_words` not filed. | `runs/the-local-patch-3.md` |
| C4 parallel images | `the-trap-room-at-the-lanterna` (Flow, 63 assets) + `hub08-13-autostart` (ComfyUI) | VNO-28 verified: 19 consecutive polling captures show Flow jobs and ComfyUI jobs running simultaneously without deadlock. Lanterna game built cleanly and linted. | `runs/hub15-c4-parallel.md` |
| C5 Gemini voice quota | `hub07-flow-test` (Croatian edition) | All 6 missing Croatian audio clips generated after quota reset; 9/9 Croatian clips and 9/9 English clips in `game/voice/`. Transcriptions of `b004` and `b006` 100% matched edition text. Game rebuilt and clean. | `runs/hub07-flow-test.md` |

## What is left

1. **C6 the user verdicts:** ask the user to play or watch and write their notes in each run log. Tickets to cover: HUB-02, 03, 05, 06, 10, 11, 13, 16, 17 (film `runs/the-lighthouse-that-kept-lists-2/video/out/final.mp4`, *The Winter Garden Clock*, *The Lighthouse That Kept Lists (VN)*, `hub07-flow-test`, `hub08-13-autostart`, the Croatian edition and EPUB, the picture books, *The Trap Room at the Lanterna* if built).
2. **Close HUB-15:** fill `changelog.md`, tick the plan, set HUB-15 to Done in `ROADMAP.md`, merge the PR (after #14).
3. Open bugs are tool tickets (Scriptorium SCP-38 to 43, VN Studio VNO-36 to 38); fix only when the user asks, in each tool repo, one ticket branch per fix.

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

C6: user verdicts, then close steps above.
