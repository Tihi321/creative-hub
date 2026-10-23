# HUB-14: make-video planner and skill fixes from the first film

Found 2026-10-23 by the first production of HUB-11 phase 3 (`runs/the-lighthouse-that-kept-lists-2.md`, "Found"; plan files `runs/the-lighthouse-that-kept-lists-2/video/plan.json`, `screenplay.json`). Hub code only: `scripts/video-plan.mjs` and `.claude/skills/make-video/SKILL.md`. Branch: the hub's current branch `HUB-06-13_live-checks` (user: one branch per repo, one commit per ticket); commit `HUB-14: ...`.

## Fixes

- [x] **Title card prompt.** The title-card keyframe prompt starts with the style's "no text on screen" and then asks for the title text. For a title shot, drop the no-text clause (and any "no lettering" negative) and ask for the title clearly.
- [x] **Voice-over style.** `voices` prints no `style` for a voice-over line without a delivery tag; the skill says such a line is read "as a voice-over narrator". Give it that default style.
- [x] **Insert shots carry no cast.** An `insert` shot inherits the scene's ON SCREEN cast (screenplay rule), so its keyframe puts the character in and adds her reference image. For insert shots, leave the cast and character references out unless the shot text names a character.
- [x] **Two balances.** Flow Music song credits are added to the Flow video budget's `spent`. Keep them apart: `spent` (Flow) and `musicSpent` (Flow Music), each against its own budget, shown separately in the estimate and summary.
- [x] **Prices.** The 720p Omni prices seen live are 4 s = 7, 6 s = 10, 8 s = 12, 10 s = 15 credits. Update the planner's table and drop the "guessed" marks for the seen ones.
- [x] **Skill text.** The skill says `hub.ps1 call` gives up after 15 s; tool calls get 660 s (only `flow_wait` caps `timeout_seconds` at 50). Correct it.
- [x] Tests: if `scripts/` has tests for the planner, extend them; otherwise run the planner on `runs/the-lighthouse-that-kept-lists-2/video/screenplay.json` into `.claude/temp/hub14/` and check the output for each point (do not overwrite the production's `plan.json`).

## Rules

- Do not touch `runs/` files of the productions (other agents are writing them), services, or other repos. One commit `HUB-14: ...` with the code and skill, then `HUB-14: plan, changelog` (tick this plan, write `changelog.md` here). Each message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. No push, no branch change.

## Done (2026-10-23)

- All six fixes and the tests are in; `node --test scripts/video-plan.test.mjs` 15 of 15 pass. Planner run on the lighthouse screenplay into `.claude/temp/hub14/` (production `plan.json` untouched): title prompt has no "no text" and asks for the title, 20 of 21 lines carry a style (the 21st is a dialogue line with no delivery), all 19 estimates are `seen`, the dry run shows a Flow budget and a Flow Music budget. That screenplay has no `insert` shot, so the insert rule is covered by the new unit test only.
- Deviations: the voice-over default was already printed for `kind: "voice-over"` lines in the code; I also gave it to a `Narrator` speaker whatever the kind. The music budget has a default of 10 (two songs) and the flag `--music-budget`; an insert keeps a character only when its action text names her.
