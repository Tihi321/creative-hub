# HUB-29 changelog

## 2026-11-07: polish round 1 after the checker's FAIL

- cartoon-studio `CTS-01_pilot` f5c37b9 CTS-09 (polish):
  - `src/engine/anim/lipsync.ts`: every voiced window opens the mouth (E, A above the line's 70th percentile); the mouth anticipates the first sound by 2 frames and releases 2 after the last; a run shorter than 2 frames joins an open neighbour, and the silence at either end stays rest.
  - `tests/lipsync.test.ts`: the tone test expects the lead and release; a new case with the pilot's "Vau?" loudness reaches 60 %.
  - `src/engine/pipeline/tools.ts`: `cts_clip_plan` prints the record payload `video-plan.mjs record` reads (`{"clip": {"file", "credits"}}`).
  - `src/shared/contracts.ts`: the header says a voice manifest's `file` is relative to the episode folder (matches the field comment and docs/contracts.md).
- creative-hub `HUB-29_cartoon-studio`:
  - `scripts/hub.ps1`: `Get-Listener` falls back to a TCP connect when `Get-NetTCPConnection` sees no listener (it sees none in this sandboxed shell); `Get-Owner` finds a hub-started service by the cmd.exe whose command line names its log file. status shows every running service up with its pid; stop cartoon-studio stopped it, start brought it back.
  - README Cartoon Studio row: backslashes restored. ROADMAP HUB-29 row: real state. Run log: A18b line (balance before not read, after 884), the 22:23 rewrite, the polish re-render.
- Pilot re-rendered from `timeline`: lint 0/0, all 30 lines >= 0.69 mouth open; hr 57.875 s, en 55.958 s, h264 1080p 24 fps + aac. The frame review step kept its earlier 2 rounds (no new model round); Claude looked at the new hr contact sheet only.
- Checks at f5c37b9: yarn typecheck 0, lint 0, test 0 (11 files, 31 tests), test:e2e 0; A3 grep no match.
- Not done: the user has not watched the re-rendered films; hub.ps1 not tested on a shell where Get-NetTCPConnection works.

## 2026-11-07: phase 1 built, pilot made; user verdict recorded (good, vector, go); waiting for the checker (V)

Cartoon Studio exists as a new public repo (`master` only pushed), with the engine, contracts, player, timeline, voices, render, images and budget gate, pipeline, studio UI and Windows installer on `CTS-01_pilot` (11 commits, CTS-01..CTS-09). The 60 s pilot "Grandma Vera's Kitchen: Pancakes" was made in hr and en for $0 and 24 of 50 Flow credits. The hub wiring is on `HUB-29_cartoon-studio`.

### cartoon-studio (`C:\projects\Personal\cartoon-studio`, public `Tihi321/cartoon-studio`)

Branch `CTS-01_pilot` from `master` 0df2a79 (README, .gitignore, LICENSE; the only commit pushed, after the A3 grep). Commits:

| Commit | Ticket | What changed |
|---|---|---|
| f1bc8ed | CTS-01 | Engine core copied from Edu Studio 46b6ec1 and renamed (`cts_*`, port 7465, `~\CartoonStudio`, `CTS_*` env, `window.cartoonstudio`, `cartoonstudio-file://`); the engine lock moved to `state/engine.lock`; static `/preview/` and `/files/<series>/` routes with a path guard (`src/engine/mcp/static.ts`); `CtsService` (`src/engine/service.ts`); Electron shell; seed config (8 roles on `client/claude-code`, $0 caps, `localOrder`, `z-image-turbo`); `docs/provenance.md`. |
| 1bfd38f | CTS-02 | `src/shared/contracts.ts` (all schemas), `src/shared/sample.ts`, `src/engine/series/{paths,service,lint,tools}.ts` (`cts_lint`, `cts_rig_check`), `docs/contracts.md` with checked examples, fixture `tests/fixtures/mini`, test 1. |
| 80ec377, 1e9276f | CTS-03 | Canvas player `src/player/*` (deterministic `window.cts`, preview mode, pose-sheet mode, title cards), `docs/player.md`. |
| 18f6638 | CTS-04 | `src/engine/anim/*` timeline builder, amplitude lip-sync, seeded blinks; timeline gains optional `titles`; tests 2 and 3. |
| a46927b | CTS-06 | `src/engine/voice/*` (allocation with `localOrder`, OmniVoice through ComfyUI, Kokoro/Supertonic through VibeTTS, `flow_narrate` Gemini, paid stub behind `charge`), `src/engine/music/chiptune.ts`, `src/engine/comfy/kind-switch.ts` (frees ComfyUI memory on voice/image switches); test 4. |
| b8370db | CTS-08 | `charge()` budget gate and ledger (`src/engine/budget/spend.ts`), `src/engine/images/*` (comfy, flow at 0 credits, fal, recraft, svg-split, colour/halo key), `seed/config/prices.md` (unverified prices), `key-set fal|recraft`; test 4a. |
| ecc347d | CTS-05 | `src/engine/render/*` (Chromium frame loop into ffmpeg, encoder probe, audio mix with ducking and two-pass loudnorm, contact and pose sheets, clip splice), `cts_render`/`cts_render_status`/`cts_frames`/`cts_pose_sheet`; test 6 (e2e). |
| 65f96d8, 77743e1 | CTS-09 | Studio UI (8 views), generic `call` route to the engine's tools, engine events, dead Edu CSS pruned, `scripts/studio-shots.mjs` (mocked and `--engine` modes), installer config and `verify-package.mjs`; test 7. |
| 46e3b0d | CTS-07 | `src/engine/pipeline/*` (resumable pipeline with the mandatory pitch gate, role tasks validated against schemas, rig paths and variants, sets, script, safety, voice cast, clips behind the credit gate, lint gate, renders, frame review), `src/engine/images/{reference,background}.ts`, 8 role prompts, `seed/style/cutout-kids.md`, `docs/pipeline.md`, full tool table in `docs/mcp-guide.md`; test 5. |

Facts checked in source (T6/T9 "first" steps): the Gemini narration tool is `flow_narrate` (`flow-music-mcp/src/flow/local-tools.ts:94`, engine `gemini`, format `wav`); `flow_generate` (`src/flow/tools.ts:247`) forces images to `max_credits: 0`, so `flow.ts` is built; video takes `max_credits`, `first_frame`, `duration`, `resolution`. OmniVoice accepted instruct tags come from `omnivoice/utils/voice_design.py` (one per category).

### creative-hub (branch `HUB-29_cartoon-studio`)

- f694b47: `services.json` entry `cartoon-studio`, `.mcp.json` entry, README row and docs line, `CLAUDE.md` tool list and bullet, `.claude/skills/make-cartoon/SKILL.md` (Tools section finalised by T7), ROADMAP row HUB-29 (only that row staged; the working tree's uncommitted HUB-28 row belongs to another session and was left alone).
- Uncommitted until the hand-back commit: this ticket folder (plan, research, events, discoveries, changelog, `evidence/`) and `runs/cartoon-pilot.md`.

### Deviations from the plan (and why)

- Rig path (a) was drawn as hand-written SVG from a Claude-written generator script, not in VectorCraft (the plan allows it as the fallback; chosen for exact pivots and speed). Recorded in the run log.
- Rig comparison `cts_rig_compare` puts the variants' full pose sheets side by side (they contain neutral, emotions, a gesture, all mouths) instead of a hand-picked crop; the raster face sheet slicing for (b) is not built (b is not run at $0); the 45 min time box is recorded, not enforced.
- Raster variant (c) keeps the painted eyes and mouth under the vector face plates (double face); recorded as the comparison result, not fixed.
- The clip fallback renders the leads bouncing over the scene without title text (the player's title card replaces the whole scene).
- Render jobs run in-process (not in the markdown job queue) with ids `<series>--render--...`; `cts_render_status` added.
- Contracts: `spend.json`/`clips.json` are objects with a `schema` field; timeline gained `beats` and `titles`; ids for marks/shots/gestures/parts allow `_` and capitals (the plan's own examples need it).
- The pilot's music step needed a manual repair (see Discoveries): the first answer used an invalid mood, the failed step pruned the script's cues, and a `from: "music"` restart left a stale job running; the script was restored with `cts_script_set` and the stale job file moved aside.
- The frame review round 1 found 2 framing problems; fixed by data (`cts_set_update` on the kitchen shots) and a rerun from `timeline`; round 2 passed.
- The first Flow `record` used the `{clips:[...]}` shape printed by `cts_clip_plan`, which `video-plan.mjs` ignores; re-recorded with `{clip:{file,credits}}`.

### Verification (run)

- A1: `yarn typecheck`, `yarn lint`, `yarn test` (11 files, 30 tests), `yarn test:e2e` (render test in Chromium), `yarn build`, `yarn build:engine`: all exit 0 at 77743e1 (logs in the cartoon-studio checkout `.claude/temp/a1/`).
- A2: headless engine lists 45 `cts_*` tools (T7 run on a scratch data folder, and this session's MCP client).
- A3: `git grep -nE "C:\\\\Users|Infplane|sk-[A-Za-z0-9]|AIza"` on `CTS-01_pilot` (77743e1): no match (exit 1). Also run before the `master` push.
- A5: `cts_lint` 0 errors 0 warnings; rigs lana/a, fido/a, fido/c pass `cts_rig_check`; 15 lines; `reviews/safety.json` pass.
- A6/A7: `out/hr.mp4` 57.875 s, `out/en.mp4` 55.958 s; h264 1920x1080 24 fps yuv420p + aac; same `scriptHash` 1f0b8a37; loudness -15.8 / -15.9 LUFS.
- A8: final render wall 20.4 s (hr) and 18.8 s (en), encoder `h264_amf`.
- A9 (before polish): lint mouth stats had 6 line/language pairs under 60 %: hr l05 0.23, hr l07 0.50, hr l13 0.50, en l05 0.57, en l07 0.55, en l10 0.57. Fixed in polish round 1 (see the entry above): all 30 pairs now >= 0.69. E_MOUTH_SILENT absent.
- A10: contact sheets (12 frames) per language and both pose sheets read by Claude; frame review round 2 pass both languages.
- A11: manifests `costUsd: 0`; `spend.json` has only `credits` entries; `budget.json capUsd 0`; no fal/recraft call; hr 15/15 OmniVoice; 0 Gemini requests (quota 10 before and after); no Flow Music; Flow images at 0 credits.
- A11b: Fido (a) vs (c) sheet, times in the run log, (b) NOT RUN (no budget).
- A11c: pitches at 19:51, user's pick p2 at 20:16:56, first image job after it.
- A13: `/preview/` in the Browser pane plays (theme and l01 audio elements playing, scrub moves), no console errors.
- A14/A15: built app (unpacked from the installer build) on the pilot data: all 8 views show the pilot, 0 console errors (`evidence/app-views-grid.jpg`); `studio-shots.mjs` mocked and `--engine` modes passed (T10).
- A16: `yarn dist:installer` and `yarn dist:portable` exit 0, `verify-package` passed after each, exes in `release/`.
- A17: intro at series level resolved without a copy; frames at the clip middles show the Flow clips in both MP4s (`evidence/splice-check.jpg`).
- A18: 24 credits spent of the 50 cap (approvedAt 20:29:33, before the first Flow video at 20:34); ledger, estimate and balance in the run log.

### Not run / not verified

- A12: answered after the pilot: hr and en good, vector (a) for phase 2 (read from "yes" to the either/or question), phase 2 go.
- A4: `hub.ps1 status` lists `cartoon-studio`; `start cartoon-studio` started it; `stop` reported "not running" while the engine ran, because `Get-NetTCPConnection` returns nothing intermittently in this environment (affects every service).
- The installer was built and verified but not installed; the window checked was the unpacked build of the same version.
- Live paid providers (fal, Recraft) never called (by design, $0); their API shapes are unverified.
- Gemini voice path never called live (quota not needed); audio heard by no person yet.

### Commit status

cartoon-studio: committed on local `CTS-01_pilot` (not pushed; push and PR after the checker passes). creative-hub: f694b47 on `HUB-29_cartoon-studio` (not pushed); the ticket folder and run log committed in the hand-back commit.
