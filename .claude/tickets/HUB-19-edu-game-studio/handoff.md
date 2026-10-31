# HUB-19 handoff: Edu Studio (refreshed 2026-10-31, after the resumed run)

Goal (user, 2026-10-29): "use director pattern, implement the app from first to last phase, as close to MVP and polished as possible, add Later features fully." Director request file `C:\projects\Personal\creative-hub\.claude\director\requests\REQ-0004-edu-game-studio.md` (only the director-scribe agent writes it; its pieces table still says "running" for pieces that stopped; it was not updated in this run). Plan: `plan.md` here (unchanged). Hub wiring drafts: `wiring/` here (described step, NOT applied, see below).

Project: `edu-game-studio`, a PUBLIC repo, ticket prefix EGS-NN, remote `origin` set (`Tihi321/edu-game-studio`), nothing pushed, no `master` branch. Engine + DOM/Canvas player + React studio + MCP server on port 7463 (tools `edu_*`).

## Rules in force
- Never push, never force-push, do not merge PRs. One commit per ticket on `EGS-NN_<what>` branches; commit messages through a Bash heredoc ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Nothing private in the public repo.
- No paid models or credits. Never start Scriptorium, ComfyUI, Book Translator, VibeTTS, Pixel Studio or Chiptune Studio without asking.
- Hub files: the user's own edits in `README.md`, `ROADMAP.md`, `.claude/skills/make-visual-novel/SKILL.md` (and untracked `.agents/`, `.codex/`, `AGENTS.md`, HUB-18) are on another branch. In the resumed run only this ticket folder was written. Hub wiring goes on a hub branch named after the ticket, and ask before committing.
- `yarn` is NOT on this machine's PATH (fnm default is Node 24.14.0). Run the tools as `fnm exec --using=24 node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json` (also `.web.json`, `.player.json`), `... node_modules/eslint/bin/eslint.js .`, `... node_modules/vitest/vitest.mjs run [files]`, builds `... node_modules/vite/bin/vite.js build --config vite.player.config.ts` (also `vite.live.config.ts`, `vite.engine.config.ts`) and `... node_modules/electron-vite/bin/electron-vite.js build`.
- The full vitest suite takes 7 to 12 minutes; under that load two CPU-bound tests (`tests/puzzles.test.ts` "logic: proves 200 seeds", and sometimes an art or scheduler test) hit their timeouts and pass alone. Treat that as a known flake, not a failure, and re-run the file alone.

## Repository state (verified with git on 2026-10-31; all local, nothing pushed)

One history now (git worktrees of one repo):

- Main checkout `C:\projects\Personal\edu-game-studio`: checked out `EGS-14_detective` (835ff07), tree clean.
- Worktree `C:\projects\Personal\edu-game-studio-p3`: checked out `EGS-22_integration` (a4333ca), clean. Has `node_modules` and `out/` builds.
- Worktree `C:\projects\Personal\edu-game-studio-egs19`: checked out `EGS-19_android` (c4c5294, the tip of everything), clean. Its `node_modules` is a JUNCTION to the p3 one: remove the junction with `cmd /c rmdir <path>` BEFORE `git worktree remove`, or git may delete the target's files.
- The temporary worktrees for EGS-18, -20, -21 were removed; their branches remain.
- Local safety branch `backup-pre-rebase-EGS-17` (96c36a0): the old tip of the phase 3/6 line before it was rebased.

Branch stack (each one commit unless noted):

`EGS-01_skeleton` e1a3792 -> `EGS-02_course-contract` 49c5a38 -> `EGS-03_player-runtime` 42e0458 -> `EGS-04_autoplay-bot` 1982630 -> `EGS-05_design-system` c78d3b2 -> `EGS-10_encyclopedia` d5f89ed -> `EGS-11_mindmaze` c5522ce -> `EGS-12_rpg` 44c9176 -> `EGS-13_roleplay` 3e89db9 -> `EGS-14_detective` 835ff07 -> `EGS-06_roles` f2c16be -> `EGS-07_content-roles` d2113ab -> `EGS-08_pipeline` bc8674f -> `EGS-15_art` 2e5292c -> `EGS-16_music` cbd9f53 -> `EGS-17_voice` 956f22d -> `EGS-22_integration` a4333ca -> `EGS-18_speaking` 876c274 -> `EGS-20_classroom` 14fe905 -> `EGS-21_live-quiz` 09a3788 -> `EGS-19_android` 9650227 (+ the docs commit c4c5294 "EGS-18..21: README, ROADMAP and guide rows", on the same branch).

EGS-22 is not in the first plan's numbering: it is the integration ticket (the rebase of the phase 3/6 line onto the shells and what it took to make them work together). Ticket folders `.claude/tickets/EGS-NN-*/` in the repo have plan.md and changelog.md (EGS-10..14 also player-doc.md).

## What was done in the resumed run (2026-10-31)

1. Verify phase 5 on EGS-14: DONE. In the main checkout: typecheck (3 tsconfigs) 0 errors, eslint 0, vitest 63 files / 1154 tests pass (the bot e2e files run perfect, wrong, random, keyboard-only and axe for every shell on solar-system and european-capitals, the role-play on hr-a1-greetings), vite and electron-vite builds pass. The EGS-11 and EGS-12 changelogs are complete.
2. Integration: DONE (EGS-22). Rebased EGS-06..08 and EGS-15..17 onto EGS-14 (conflicts in README, ROADMAP, docs, `scripts/play.mjs`, `progress.ts`, `quiz-arena.ts`; the hover fix was already in `items.css`). Then: the pipeline enables quiz arena, encyclopedia, MindMaze and RPG and records role-play and detective in `extensions.pipeline.requestedShells` (no `requested` key in strict shell sections any more); RPG art goes in its own section fields, other shell art in `extensions.art`; the RPG gets the frame story; every shell has music and sound effects (`ShellSession.audio`, `musicAreaOf`) and the reduce-audio toggle; listening clips and the encyclopedia narration duck the music; `KNOWN_ROLES` equals `ROLES`; units written in parallel can link to each other (planned article ids); the curriculum check flags objectives asking for causes, consequences or dates that their facts do not state (heuristic, English only). Not re-tested ticket by ticket after the rebase: only the tip was.
3. EGS-18 speaking practice (speak your answer on text answers: Web Speech or a local whisper.cpp through a loopback endpoint, `edu_stt_status`), EGS-20 classroom mode (assignment, result file, class report; MCP tools, no studio tab), EGS-21 live multiplayer quiz (room state machine, HTTP + SSE server, client, host page, `edu_live_*`), EGS-19 Android (generates `courses/<slug>/android/`, `edu_android_prepare`): DONE in code, built by four parallel agents in separate worktrees, then stacked in that order on EGS-22 with small fixes (a settings test, the classroom CSS moved under `.edu-stage` and made to pass the 13 px / no-all-caps rule, a race in the live e2e after the room closes).
4. Verification of the final tip (EGS-19 worktree): typecheck 0, eslint 0, vitest 105 files, 1660 tests, 1658 passed in the whole-suite run and the 2 that failed are the load timeouts above, which pass alone; all three vite builds and electron-vite build pass.

## What is NOT done or NOT verified

- NOT DONE: Phase 7 hub wiring (blocked by the rule not to touch hub files; drafts and the steps are in `wiring/wiring.md`: `services.json` entry, `.mcp.json` entry, README row, `make-edu-game` skill, CLAUDE.md line, ROADMAP row). Checked: the headless engine starts, the MCP handshake works and `tools/list` gave 43 tools (before EGS-18..21 added `edu_stt_status`, `edu_android_prepare`, `edu_class_assign`, `edu_class_report`, `edu_live_start`, `edu_live_status`, `edu_live_stop`), `hub.ps1 check` not run (not registered).
- NOT DONE: Phase 4 pilot (stopped before it, as instructed), the final `director-checker` pass, the scribe closing REQ-0004, PRs and any push or merge (the user decides; the stack is 20 local branches on one line).
- NOT DONE: a studio Class tab for classroom mode (MCP tools only); MindMaze rooms and encyclopedia plates do not draw their generated pictures yet (recorded in `extensions.art`); the live quiz does not show pictures in questions.
- UNTESTED, never verified: the Electron window (`yarn dev`), real audio playback and listening to any clip (browser tests use a recording `Audio`), a real microphone with the real Web Speech service, the browser's whisper recorder (`getUserMedia`), touch on a real device, an APK installed on a device (a debug APK was BUILT from a fixture: 5.2 MB, app id `org.edustudio.solar`), a signed release, the live quiz on real phones on a real LAN (tests bind 127.0.0.1 only), real web search, real models, real Scriptorium, Gemini TTS, ComfyUI TTS, Book Translator editions, a human play-through of anything.
- Heads up: the engine reads provider keys from the Scriptorium credential store at start (log line `key from the scriptorium credential store`); it makes a model-list request to OpenRouter on start but spends nothing.

## What the pilot needs (Phase 4, EGS-09)

1. The user chooses the topic (history or geography, for example Ancient Rome or European capitals), audience, age, language(s) and length (`format`: quick 2 units, standard 4, deep 6).
2. Which checkout to run: the integrated tip is the EGS-19 worktree (everything) or the EGS-22 worktree (without the later features); the main checkout is still at EGS-14. Build the engine there (`build:engine`) and start `node out/engine/index.js --mcp-only` (port 7463, data `~\EduGames`); or register the service in the hub first (`wiring/`).
3. Model work: the `client` provider (`model: "client/claude-code"`, $0): the session loops `edu_get_task` / `edu_submit_task`, and does the web research itself (the studio has no real web search key; Wikipedia or client search).
4. Generators: ComfyUI, Pixel Studio and Chiptune Studio only after the user says start (placeholders are used when they are down, the lint warns PLACEHOLDER_ASSET); voices follow the hub's voice rule (Gemini TTS free quota 10 a day, Croatian first, else local VibeTTS), only if the user wants voices.
5. Run log: hub `runs/<slug>.md` (copy `runs/_template.md`) with every id and decision.
6. **The user plays the built game** (`~\EduGames\courses\<slug>\build\index.html`, in the quiz arena and in the encyclopedia explorer, and any other shell they like) and says what is wrong. A production is done only after that.

## Resume

Open a new session in `C:\projects\Personal\creative-hub` and paste:

> Resume HUB-19 (Edu Studio) from `.claude/tickets/HUB-19-edu-game-studio/handoff.md`. Read the handoff and `wiring/wiring.md`, verify the repo state with git in `C:\projects\Personal\edu-game-studio`, `-p3` and `-egs19`, then ask me which of these I want: (a) apply the hub wiring on a hub branch, (b) start the pilot (EGS-09), (c) push the branches and open PRs, (d) the final director-checker pass and closing REQ-0004. Follow the rules in the handoff.

Everything lives on this machine only. This ticket folder is untracked in the hub.
