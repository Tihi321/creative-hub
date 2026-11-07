---
name: make-cartoon
description: Turn an idea into a cutout-puppet cartoon episode or series for children (ages 4-8, South Park style flat cutouts, 60 s pilot to 5-10 min, Croatian and English from one script) by driving Cartoon Studio over MCP - a team of roles pitches premises (the user picks one), designs the cast and rigs the puppets, makes sets, writes and safety-checks the script, casts voices, makes music, lip-syncs, renders MP4s locally at $0 and reviews the frames. Use when the user asks for a cartoon episode, a cartoon series, cutout animation or a kids' cartoon with recurring characters. For a one-off short film made of Flow video shots use make-video; for a story or visual novel use make-visual-novel; for a game use make-edu-game.
---

# Make a cartoon episode or series

The hub is `C:\projects\Personal\creative-hub`. Cartoon Studio is `C:\projects\Personal\cartoon-studio` (public repo `Tihi321/cartoon-studio`), MCP on port 7465, data in `~\CartoonStudio`. Its own guide is the source of truth: `docs\mcp-guide.md` in that repo (also the MCP resource `cartoon-studio://guide`); the data contracts are `docs\contracts.md`. The plan behind it: `.claude/tickets/HUB-29-cartoon-studio/plan.md`.

What it makes: a series bible, cast and rigs (cutout puppets), sets, an episode script that is language-independent, a Croatian and an English timeline, and one MP4 per language rendered by a deterministic Canvas player in headless Chromium plus ffmpeg (24 fps, 960x540 preview, 1920x1080 final). Optional Flow video "hero shots" (an 8 s series intro, at most one 8 s moment per episode) are spliced into the final render only.

## 0. Before you start

1. `pwsh -File scripts\hub.ps1` (status). Start the studio with `pwsh -File scripts\hub.ps1 start cartoon-studio`, and what the run needs: `start comfyui`, `start comfy-mcp`, `start vibetts` (or the tray app), `start chiptune-studio`, and `start flow-music-mcp` only for Flow clips. Strata is not running during ComfyUI work (shared memory). If the tools are missing from your list, the server was down when the session began: start it, then ask the user to reconnect (`/mcp`) or call tools through `pwsh -File scripts\hub.ps1 call cartoon-studio <tool> '<json>'`.
2. **One engine per data folder.** If the Cartoon Studio desktop app is open, its engine holds `~\CartoonStudio` and the headless start fails; to open the app, stop the hub's engine first (`hub.ps1 stop cartoon-studio`).
3. Never start Scriptorium for this (it resumes its whole book factory and may spend on paid models). A Scriptorium episode format is not part of phase 1; ask the user first if it is ever wanted.
4. Open a run log `runs/<slug>.md` (template below): series slug, episode id, every decision, every id, timings, what you checked. A later session resumes from it.
5. Agree briefly, only if the user did not say: audience and age (default 4-8), languages (default hr + en), length (pilot about 60 s; an episode 5-10 min), who does the model work (default: you, $0, every role on `client/claude-code`).

## 1. Money rule (read before any generator runs)

- **No paid provider without an agreed budget recorded in the run log.** Paid means any fal/Recraft image, any paid voice, any Flow credit. The default is $0 and no paid call.
- The engine enforces it: `cts_budget_set { series, episode, capUsd, flowCreditsCap, approvedBy, note }` writes `episodes/<ep>/budget.json`; every paid call is refused (`BUDGET_EXCEEDED`, `FLOW_CREDITS_EXCEEDED`) when spent plus the estimate would pass the cap, and with no `budget.json` both caps are 0. Only set a cap after the user said yes in this conversation; copy the user's words, the cap and the date into the run log. Going past a cap needs a new yes. `cts_budget_get` shows cap, spent and the ledger; copy it into the run log at the end.
- **Flow credits** are a second currency with their own cap (`flowCreditsCap`, default pilot 50). Estimates and each call's `max_credits` come from the hub's `scripts\video-plan.mjs` (`fnm exec --using=24 node scripts\video-plan.mjs <plan|next|record> <dir>`, see the `make-video` skill), not from a table of your own. Flow images stay at `max_credits: 0`. No Flow Music.
- Keys live in the OS keyring (`node out/engine/index.js key-set <provider>` in the studio repo, run by the user), never in files or the run log.

## 2. The client-task loop

With every role on `client/claude-code` each model call parks as a task and waits for you:

```
cts_run_pipeline {series, episode, brief}     (re-call with the same ids to resume; retry: true, from: <step>)
cts_wait {series}                             returns with clientTasks when something waits
loop: cts_get_task -> do the role's work exactly as the task text says (JSON only, schema named in the task) -> cts_submit_task {taskId, text}
until cts_wait says the run is done or blocked
```

A submitted answer is validated against the task's schema; a failing answer comes back as a retry with the errors. `cts_client_tasks` lists parked tasks, `cts_release_task` gives one back. `cts_status {series}` shows every step, failures, what to do next and the state `waiting-on-user`.

## 3. Pipeline steps

1. **pitch** (showrunner): 3 premises, each with a title, logline, two leads and 1-2 sets, in hr and en. **The pipeline stops here (`waiting-on-user`).** Show the user the 3 pitches in chat (and in the app's Series view) and wait. Only after the user picks do you call `cts_pitch_choose {series, pitch}`; write the pick and the time in the run log. No image is made before that.
2. **bible**: cast without rigs, sets, tone, rules from the chosen pitch.
3. **cast_ref** (character-designer): a reference image per character from ComfyUI (default model `z-image-turbo`, arms held away from the body). Look at the images and pick one.
4. **rig**: three paths, one rig format. (a) `claude-svg`, the default: you draw each part in VectorCraft over MCP from `ref.png` (or write the SVG by hand if VectorCraft is not available; say which in the run log), then `cts_rig_set` and `cts_rig_check`. (b) `recraft-svg`: paid, needs a budget, not used without one. (c) `raster`: key the reference, cut by polygons into part PNGs, vector face on top; a fallback. Variants go to `cast/<id>/variants/<a|b|c>/`; `cts_rig_compare {series, cast}` makes the side-by-side sheet; the pose sheet (`cts_pose_sheet`) is read before any animation. Time-box each path and write its time in the run log.
5. **set** (background-artist): background and foreground prop from ComfyUI, keyed, marks and shots placed by reading the image.
6. **script** (writer): `script.json` plus `text/hr.json` and `text/en.json`; short lines (at most 12 words).
7. **safety** (child-safety-reviewer): must pass; up to 2 revise rounds back to the writer.
8. **voice_cast** (voice-director): voice per character per language in the bible, with a short audition clip per character in `cast/<id>/voice/` for the user to hear.
9. **voice**: see the voice rule below.
10. **music**: theme loop and up to 2 SFX from Chiptune Studio (missing studio = no music and a warning).
11. **clips** (only if the episode has `clip` beats and a Flow credit cap is recorded): `cts_clip_plan`, then keyframe at 0 credits and the 8 s scene with `max_credits` from `video-plan.mjs next`, `cts_clip_review`, `record` the credits. A clip that fails review twice is dropped and the beat falls back to a title card with a cutout bounce.
12. **lipsync + timeline** (code), then `cts_lint` must have 0 errors.
13. **preview_render** per language (960x540), a 12-frame contact sheet and the pose sheets.
14. **frame_review** (frame-critic): you read the contact sheets and pose sheets for off-model parts, overlaps, mouth open in silence, wrong facing, actor off-frame, missing background; up to 2 rounds, fixes are data edits by the owning role.
15. **final_render** per language (1920x1080). `cts_status` shows paths, durations, render times, encoder and open problems.

## 4. Voice rule

The hub rule applies (hub `CLAUDE.md`): Gemini TTS free tier is 10 requests a day; Croatian goes first on Google voice; if the lines for a language exceed the remaining free quota, that language goes local. Run `cts_voice_quota` before and after and write both in the run log. A pilot has 12-16 lines, so hr goes local by design:

- local **hr = OmniVoice through ComfyUI** (attribute tags per character plus an optional reference clip, fixed seed), Supertonic through VibeTTS as the fallback;
- local **en = Kokoro** through VibeTTS.

`cts_voice_plan` shows the allocation and why; `cts_voice_generate` makes the clips; a failed clip becomes a placeholder (silence) with a lint warning. Do not start VibeTTS unasked beyond what the run needs. **ComfyUI memory is freed between voice jobs and image jobs** (comfy-mcp `free_memory`; the engine's queue does it when the job kind changes). If you run image work by hand between voice steps, call `free_memory` first: a stale voice-model state broke image runs before.

## 5. Check and show

- `cts_lint {series, episode}` must have 0 errors (warnings: read them; `W_PLACEHOLDER` means a voice is a stand-in).
- Look at the contact sheets yourself with the Read tool (frames, not just the verdict file); in at least 4 sampled frames per language both leads must be complete and facing the speaker.
- Show the user the files: `~\CartoonStudio\series\<slug>\episodes\<ep>\out\hr.mp4` and `en.mp4` (and `*.preview.mp4`). Open them for the user (`Start-Process <file>` in PowerShell) and give the full paths in the reply. The `/preview/` page at `http://127.0.0.1:7465/preview/...` plays a timeline in the browser pane. **A production is done only when the user has watched it.** Record their verdict on hr and en, the look they prefer (vector or raster) and go/no-go in the run log.
- Say what you verified and what you did not (real audio, the user watching, the desktop app).

## 6. Tools

The list below is final (T7, CTS-07; the studio's `docs\mcp-guide.md` has every argument, `docs\pipeline.md` the steps).

- Engine and queue: `cts_status {series}` (jobs, plus the pipelines: state, current step, hint), `cts_wait`, `cts_get_task`, `cts_submit_task`, `cts_client_tasks`, `cts_release_task`, `cts_pause_all`, `cts_resume_all`, `cts_stop_now`, `cts_studios_status`.
- Pipeline: `cts_run_pipeline {series, episode, brief?, options?, retry?, from?}` (resume by re-calling; it stops at `waiting-on-user` after the pitches), `cts_pitch_choose {series, pitch}` (only with the pitch the user chose), `cts_timeline_build`, `cts_lint {series, episode, requireAudio}`.
- Series and data: `cts_series_create`, `cts_series_get`, `cts_series_update`, `cts_cast_get`, `cts_set_get`, `cts_set_update`, `cts_episode_create`, `cts_episode_get`, `cts_script_set`, `cts_text_set`.
- Rigs: `cts_rig_set {series, cast, variant?, rig, parts}`, `cts_rig_check`, `cts_rig_build {series, episode, cast, path}` (claude-svg = a, recraft-svg = b, raster = c), `cts_rig_compare {series, cast}`, `cts_rig_choose {series, cast, variant}`, `cts_pose_sheet`. Options for the run: `options.rigPaths {cast: [paths]}`, `options.rigChoice {cast: variant}`.
- Render: `cts_render {series, episode, langs, quality}` (jobs; `cts_render_status`), `cts_frames` (contact sheet).
- Flow clips: `cts_clip_plan {series, episode}` (prints the `video-plan.mjs` commands), `cts_clip_generate {series, episode?, clip, maxCredits}`, `cts_clip_review`. The clips step waits (`waiting-on-user`) until `cts_budget_set` recorded a `flowCreditsCap` and every missing clip has its `max_credits` (`cts_run_pipeline {options: {clipCredits: {intro: <n>}}}`); `options.skipClips: true` drops them (record NOT RUN).
- Voices and music: `cts_voice_plan`, `cts_voice_generate`, `cts_voice_status`, `cts_voice_quota`, `cts_music_generate`.
- Images and budget: `cts_budget_set`, `cts_budget_get`, `cts_image_generate`, `cts_svg_split`.

## 7. Run log template

Copy `runs/_template.md` to `runs/<slug>.md` and add:

```
# <series> / <episode>
Started <date>. Brief: <idea, ages, languages, length>.
## Money
- Cap USD: 0 · Flow credits cap: <n> (user said "<words>" on <date>) · Spent (cts_budget_get): <usd> / <credits>
- video-plan.mjs estimate: · flow_status credits before / after:
## Ids and paths
- Series slug / episode id · data folder · engine started with hub.ps1 (time) · encoder
- Pitches shown (time), user pick (time, id) · first image job time (must be later)
- Rigs: character -> path (a|b|c), tool used (VectorCraft | hand-written), minutes · reference image model
- Voice allocation per language (reason) · cts_voice_quota before / after · providers per language
- Clips: ids, files, credits, review verdicts
## Log
- <date time> step, job id, result
## Renders
- per language: preview and final seconds, wall time per stage, file paths, ffprobe summary, loudness
## Reviews
- safety verdict · frame-review verdicts and open problems
## Checked / not checked
- DONE / NOT DONE / UNTESTED per item; the user's verdict on hr and en, look choice, go/no-go
```
