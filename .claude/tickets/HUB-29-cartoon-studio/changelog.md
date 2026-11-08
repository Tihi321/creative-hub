# HUB-29 changelog

## 2026-11-08: pilot 2 (CTS-10..17) built; "Pip and Bruno" made in hr and en; the user said "Good, go"; waiting for the checker

The new method is in: puppets from a sketch redrawn by Z-Image (no SVG, no Recraft), face states by inpaint plus drawn states, music from ComfyUI ACE-Step, music measured well under the voices, Flow only for the series intro and outro. The 57-59 s pilot 2 cost $0 and 24 of 50 Flow credits. The user approved both character sheets ("Approve both") and the films ("Good, go").

### cartoon-studio, branch `CTS-10_pilot-2` (from `CTS-01_pilot` f5c37b9; local, not pushed)

| Commit | Ticket | What changed |
|---|---|---|
| 0f79bb4 | CTS-10 | Recraft provider, `svg-split`, `cts_svg_split`, `buildRecraftRig`, the rig-recraft prompt and the Flow image provider (`images/flow.ts`, `generateImage`) deleted; `RIG_PATHS` claude-svg/raster, `RIG_VARIANTS` a/c, `IMAGE_PROVIDERS` comfy/gemini/fal; clip keyframes are player stills (`stillFrame`, 1280x720) from the showrunner's `staging`; clip ids `intro`/`outro` only, series level; `tests/clips.test.ts` (new), contracts and render e2e tests updated. |
| c0d7350 | CTS-16 | `render.md` `mix` levels; each input's loudness measured once (`levels.json`); voices to -20 LUFS, music 18 dB under during lines and 8 dB in gaps (duck in dB), sfx and clip audio relative to the voice, the script's music gain a trim of at most 0 dB; `render/mixcheck.ts` renders voice and music stems and writes `mix-check.json` for final renders; `cts_render` returns `minUnderDb`; lint `W_MIX_MUSIC_LOUD`; `tests/mix.test.ts` (new). |
| 8900236 | CTS-15 | `music/comfy.ts` `generateTheme` (ace-step-v1-instrumental, alternative minimax-music-3, 40 s, fades; up to 2 MOSS sfx); ComfyJobKind `music`; `musicAnswer` {tags, bpm, key, seed, seconds?, sfx?}; composer prompt for soft background music; `cts_music_generate`; Chiptune out of the pipeline, studios status and autostart (`music/chiptune.ts` deleted). |
| 268a0d9 | CTS-11 | `buildZImageImg2Img`, `buildZImageInpaint` (mask -> SetLatentNoiseMask, composited back); `ComfyRequest.init` / `ImageRequest.init`; `cts_image_generate {init, denoise, mask}`; `images/gemini.ts` behind `charge(usd)` before any network call, `key-set gemini`, prices row "check before use"; keyframe polish at 0.35; `tests/budget.test.ts` gemini case. |
| 21b20dc | CTS-12 | `images/sketch.ts` (body plan to sketch, pose sketches, checks); step `cast_sheet` (3 seeds at 0.8, the designer's pick, wave/point/shrug, `sheet.png`) and gate `sheet_review` with `cts_sheet_approve`; bible `cast[].sheet`; pilot 1's `cast_ref` maps to done steps. |
| 9146351 | CTS-13 | Raster rig from `ref.png` without variant a; face patches by masked inpaint (`images/face.ts`); the rig pose sheet renamed `rig-sheet.png`; `rigStep` raster by default; `tests/rig-raster.test.ts` (new). |
| 4f5cd9a | CTS-13 fix | Face states inpaint cannot make are drawn from the master's colours: MBP, eyes half and closed, brows happy/sad/surprised (inpaint stays for mouths A, E, O); `face-report.json` records the method. |
| face95e | CTS-14 | Rig `poses` and gesture `pose` contract, timeline pose track, player pose drawing and `?sheet=&pose=` render mode, `pipeline/poses.ts` `makePose` (img2img 0.55, retry 0.45), `cts_pose_make` with a frame-critic pose review. |
| 08efa1d | CTS-17 | `brief.pitch` skips the pitch pause; step `poses` (`options.poses`); final render step detail with the mix numbers; Cast view (sketch, master, sheet poses, approval, Approve and Redo) and Settings (engines, read-only, new `cts_media_config`); sheet state in `cts_series_get`/`cts_cast_get`; Chiptune removed from UI, protocol, docs and seed; docs, README, ROADMAP rows CTS-10..17, cutout-kids style with body-plan rules. |

### creative-hub, branch `HUB-29_cartoon-studio`

- `.claude/skills/make-cartoon/SKILL.md`: the new steps (sheet pause, raster rigs with drawn face states, poses, music from ComfyUI, Flow video only for intro/outro, mix-check numbers, Nano Banana only after a yes and a cap, no model download without a yes) and the run log template.
- `runs/pip-bruno-pilot.md` (new): the run with every id, timing and decision.
- `ROADMAP.md`: the HUB-29 row (only that row staged).
- This folder: plan front matter and line 9, `handoff.md`, events, discoveries, this entry, `evidence/pilot2/`.

### Deviations from the plan (and why)

- Branch cut from f5c37b9 (the polished phase 1 tip), not 77743e1.
- The face states that inpaint could not make (closed mouth, half and closed eyes, brows) are drawn in code from the master's colours (decided by implement on 2026-11-08 after the CTS-13 probe; $0, no download).
- `sheet_review` is a separate gate step after `cast_sheet`; `cts_media_config` added so the Settings panel has data; the Settings panel is read-only.
- The `poses` step runs only for gestures listed in `options.poses`; pilot 2 asked for none.
- The mix check uses momentary loudness (400 ms windows) instead of 3 s short-term, because 3 s windows mix the gap level into short lines.
- The set's foreground prop was resized by hand to 340 px wide (drawn at native size otherwise; pilot 1 discovery).
- `tests/clips.test.ts`, `mix.test.ts`, `rig-raster.test.ts`, the budget case and the updated contracts/render tests are the plan's tests; no others added.

### Verification

- B1: `yarn typecheck`, `lint`, `test` (14 files, 37 tests), `test:e2e`, `build`, `build:engine` exit 0 at 08efa1d.
- B2 `git grep -niE "recraft|svg-split|svg_split" -- src seed docs`, B3 `git grep -n generateImage -- src`, B10 `git grep -n -i chiptune -- src/engine/pipeline src/engine/music`, B16 A3 grep on `CTS-10_pilot-2`: no match (exit 1 each).
- B4: Z-Image img2img live (P0 probe, the CTS-11/12 probes, the pilot sheets at about 28 s per image warm; `sheet/meta.json` model z-image-turbo).
- B5: sheets shown at 10:44, the user's "Approve both" at 10:53, `cts_sheet_approve` 10:53:46-47, rigs after.
- B6/B7: both rigs `kind: raster`, PNG parts and face states, no `variants/a`, rig check passed; rig sheets read by Claude: one face, A/E/O/MBP distinct, closed eyes and brows read.
- B8: sheet poses match the masters (Claude); no fallback used, no Nano Banana.
- B9: `spend.json` has 2 credit entries (24), no usd; 0 Gemini requests (quota 10 before and after); voices local (hr OmniVoice, en Kokoro).
- B10: theme `ace-step-v1-instrumental`, 39.9 s, 24.7 s wall; no Chiptune call.
- B11: `mix-check.json` hr min 25.6 / median 29.7 dB, en 26.0 / 29.4 dB; integrated -16.0 / -15.9 LUFS.
- B12: `series/pip-bruno/clips/intro.mp4` and `outro.mp4` (12 credits each, reviews pass), 24 <= 50, no episode-level clip, frames at 4 s and 53 s show both clips (`evidence/pilot2/splice-check.jpg`).
- B13: hr 57.25 s, en 58.67 s, h264 1920x1080 24 fps yuv420p + aac, same scriptHash 986c3a14, lint 0/0.
- B14: `cts_lint` pilot/ep00-pilot 0/0 and an en preview render of pilot 1 (55.96 s, 8.7 s wall) on the new build.
- B17: the user's verdict "Good, go" (look, music and its level, phase 2 go).

### Not run / not verified

- B15: `studio-shots.mjs` passed in mocked mode only (CTS-17); the Cast view with the real pip-bruno data was not opened (the app and the headless engine cannot share the data folder).
- The sound was judged by the user ("Good"), not by a tool; Nano Banana (gemini), fal and the Gemini voice were never called live; the gemini price row is unverified.
- The Flow balance before the clips was not shown (Chrome was not running); each job measured its own balance change (12 + 12); the balance after was 884, the same number as after pilot 1 (unexplained).
- `cts_pose_make` and the `poses` step were not run live (no poses asked); MOSS sfx and minimax-music-3 not run.

### Commit status

cartoon-studio: CTS-10..17 committed on local `CTS-10_pilot-2`, not pushed (push and PR after the checker; PR base `CTS-01_pilot` while PR #1 is open). creative-hub: committed on `HUB-29_cartoon-studio` with this entry, not pushed.

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
