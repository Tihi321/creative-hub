---
name: make-cartoon
description: Turn an idea into a cutout-puppet cartoon episode or series for children (ages 4-8, South Park style flat cutouts, 60 s pilot to 5-10 min, Croatian and English from one script) by driving Cartoon Studio over MCP - a team of roles pitches premises (the user picks one), designs the cast from sketches with Z-Image, rigs the puppets, makes sets, writes and safety-checks the script, casts voices, makes music in ComfyUI, lip-syncs, renders MP4s locally at $0 and reviews the frames. Use when the user asks for a cartoon episode, a cartoon series, cutout animation or a kids' cartoon with recurring characters. For a one-off short film made of Flow video shots use make-video; for a story or visual novel use make-visual-novel; for a game use make-edu-game.
---

# Make a cartoon episode or series

The hub is `C:\projects\Personal\creative-hub`. Cartoon Studio is `C:\projects\Personal\cartoon-studio` (public repo `Tihi321/cartoon-studio`), MCP on port 7465, data in `~\CartoonStudio`. Its own guide is the source of truth: `docs\mcp-guide.md` in that repo (also the MCP resource `cartoon-studio://guide`); the data contracts are `docs\contracts.md`. The plan behind it: `.claude/tickets/HUB-29-cartoon-studio/plan.md` (phase 1 and the `# Pilot 2` section).

What it makes: a series bible, cast (character sheets and raster puppets), sets, an episode script that is language-independent, a Croatian and an English timeline, and one MP4 per language rendered by a deterministic Canvas player in headless Chromium plus ffmpeg (24 fps, 960x540 preview, 1920x1080 final). Optional Flow video clips, only a series `intro` and `outro` (8 s each), are spliced into the final render only.

## 0. Before you start

1. `pwsh -File scripts\hub.ps1` (status). Start the studio with `pwsh -File scripts\hub.ps1 start cartoon-studio`, and what the run needs: `start comfyui`, `start comfy-mcp`, `start vibetts` (or the tray app), and `start flow-music-mcp` only for the Flow intro/outro. Chiptune Studio is not used. Strata is not running during ComfyUI work (shared memory). If the tools are missing from your list, the server was down when the session began: start it, then ask the user to reconnect (`/mcp`) or call tools through `pwsh -File scripts\hub.ps1 call cartoon-studio <tool> '<json>'`.
2. **One engine per data folder.** If the Cartoon Studio desktop app is open, its engine holds `~\CartoonStudio` and the headless start fails; to open the app, stop the hub's engine first (`hub.ps1 stop cartoon-studio`).
3. Never start Scriptorium for this (it resumes its whole book factory and may spend on paid models).
4. Open a run log `runs/<slug>.md` (template below): series slug, episode id, every decision, every id, timings, what you checked. A later session resumes from it.
5. Agree briefly, only if the user did not say: audience and age (default 4-8), languages (default hr + en), length (pilot about 60 s; an episode 5-10 min), who does the model work (default: you, $0, every role on `client/claude-code`).
6. **Never download a model** (a ControlNet, a new checkpoint) without the user's yes.

## 1. Money rule (read before any generator runs)

- **No paid provider without an agreed budget recorded in the run log.** Paid means any Nano Banana (Gemini image) or fal image, any paid voice, any Flow credit. The default is $0 and no paid call.
- The engine enforces it: `cts_budget_set { series, episode, capUsd, flowCreditsCap, approvedBy, note }` writes `episodes/<ep>/budget.json`; every paid call is refused (`BUDGET_EXCEEDED`, `FLOW_CREDITS_EXCEEDED`) when spent plus the estimate would pass the cap, and with no `budget.json` both caps are 0. Only set a cap after the user said yes in this conversation; copy the user's words, the cap and the date into the run log. Going past a cap needs a new yes. `cts_budget_get` shows cap, spent and the ledger; copy it into the run log at the end.
- **Nano Banana** (`provider: "gemini"`) is a paid fallback only: ask the user for an amount first, record the cap, and check the model id and price in Google's docs (the `prices.md` row is marked "check before use").
- **Flow** gets video only, never images: the series `intro` and `outro` clips (8 s each, about 12 credits each at 720p Omni), under their own cap (`flowCreditsCap`, default pilot 50). Estimates and each call's `max_credits` come from the hub's `scripts\video-plan.mjs` (`fnm exec --using=24 node scripts\video-plan.mjs <plan|next|record> <dir>`, see the `make-video` skill); `record` takes `{"clip": {"file", "credits"}}`. No Flow Music.
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

1. **pitch** (showrunner): 3 premises, each with a title, logline, two leads and 1-2 sets, in hr and en. **The pipeline stops here (`waiting-on-user`).** Show the user the 3 pitches in chat (and in the app's Series view) and wait. Only after the user picks do you call `cts_pitch_choose {series, pitch}`; write the pick and the time in the run log. No image is made before that. When the user already chose a premise (for example one from an earlier series), pass it as `brief.pitch` and the pause is skipped.
2. **bible**: cast without rigs, sets, tone, rules from the chosen pitch.
3. **cast_sheet** (character-designer): per character a **body plan** (flat palette shapes with limbs and joints; head on a short neck, arms attached at the shoulders and held away from the body, tail behind and clear of the arms), rendered as a rough sketch on grey; Z-Image img2img (denoise 0.8, three seeds) draws the character over it; the designer picks the master `ref.png`; three pose sketches (wave, point, shrug) at the same seed give `sheet.png`.
4. **sheet_review: PAUSE.** Show the user every `cast/<id>/sheet.png` in chat (and in the app's Cast view) and wait. Call `cts_sheet_approve {series, cast, ok: true}` only on the user's approval, or `{ok: false, note}` for a redo with their words. Nothing is rigged before every character is approved; write the times in the run log.
5. **rig**: `raster` by default: parts cut from `ref.png` by the designer's polygons with joint overlap; mouths A, E, O by masked Z-Image inpaint, the other face states (closed mouth, half and closed eyes, brows) drawn from the master's colours. `claude-svg` (path a, hand-drawn SVG) only when asked (`options.rigPaths`). Read the rig pose sheet (`cast/<id>/rig-sheet.png`, `cts_pose_sheet`) before any animation: one face, the mouths read, the joints closed.
6. **poses** (optional, at most 2 gestures per character): the rig at the gesture peak cleaned by Z-Image img2img (`cts_pose_make`), reviewed against `sheet.png`; a pose that fails twice stays a part rotation.
7. **set** (background-artist): background and foreground prop from Z-Image, keyed, marks and shots placed by reading the image.
8. **script** (writer): `script.json` plus `text/hr.json` and `text/en.json`; short lines (at most 12 words); an `intro` clip beat first and an `outro` last when the episode has them.
9. **safety** (child-safety-reviewer): must pass; up to 2 revise rounds back to the writer.
10. **voice_cast** (voice-director): voice per character per language in the bible, with a short audition clip per character in `cast/<id>/voice/` for the user to hear.
11. **voice**: see the voice rule below.
12. **music** (composer): a 40 s instrumental theme from ComfyUI (`ace-step-v1-instrumental`, alternative `minimax-music-3`; soft, sparse, under dialogue) and up to 2 MOSS sound effects.
13. **clips** (only with intro/outro beats and a recorded Flow credit cap): `cts_clip_plan`, the keyframe is a still rendered by the player from the clip's staging, then the 8 s scene with `max_credits` from `video-plan.mjs next`, `cts_clip_review`, `record` the credits. A clip that fails review twice is dropped and the beat falls back to a title card with a cutout bounce.
14. **lipsync + timeline** (code), then `cts_lint` must have 0 errors.
15. **preview_render** per language (960x540), a 12-frame contact sheet and the rig pose sheets.
16. **frame_review** (frame-critic): you read the contact sheets and pose sheets for off-model parts, overlaps, mouth open in silence, wrong facing, actor off-frame, missing background; up to 2 rounds, fixes are data edits by the owning role.
17. **final_render** per language (1920x1080) with the **mix check**: music 18 dB under the voice while someone speaks (floor 15 dB) and 8 dB under in the gaps (`config/render.md` `mix`); `render/<lang>/mix-check.json` has `minUnderDb`, `medianUnderDb`, `gapMusicUnderVoiceDb`, and lint warns `W_MIX_MUSIC_LOUD` under the floor. Copy those numbers into the run log.

## 4. Voice rule

The hub rule applies (hub `CLAUDE.md`): Gemini TTS free tier is 10 requests a day; Croatian goes first on Google voice; if the lines for a language exceed the remaining free quota, that language goes local. Run `cts_voice_quota` before and after and write both in the run log. A pilot has 12-16 lines, so hr goes local by design:

- local **hr = OmniVoice through ComfyUI** (attribute tags per character plus an optional reference clip, fixed seed), Supertonic through VibeTTS as the fallback;
- local **en = Kokoro** through VibeTTS.

`cts_voice_plan` shows the allocation and why; `cts_voice_generate` makes the clips; a failed clip becomes a placeholder (silence) with a lint warning. **ComfyUI memory is freed between image, voice and music jobs** (the engine's queue does it when the job kind changes). If you run ComfyUI work by hand in between, call comfy-mcp `free_memory` first.

## 5. Check and show

- `cts_lint {series, episode}` must have 0 errors (warnings: read them; `W_PLACEHOLDER` means a voice is a stand-in, `W_MIX_MUSIC_LOUD` that the music is too close to the voice).
- Look at the contact sheets yourself with the Read tool (frames, not just the verdict file); in at least 4 sampled frames per language both leads must be complete and facing the speaker.
- Show the user the files: `~\CartoonStudio\series\<slug>\episodes\<ep>\out\hr.mp4` and `en.mp4` (and `*.preview.mp4`). Open them for the user (`Start-Process <file>` in PowerShell) and give the full paths in the reply. The `/preview/` page at `http://127.0.0.1:7465/preview/...` plays a timeline in the browser pane. **A production is done only when the user has watched it.** Record their verdict on hr and en, the look, the music and its level, and go/no-go in the run log.
- Say what you verified and what you did not (real audio, the user watching, the desktop app).

## 6. Tools

The studio's `docs\mcp-guide.md` has every argument, `docs\pipeline.md` the steps.

- Engine and queue: `cts_status {series}`, `cts_wait`, `cts_get_task`, `cts_submit_task`, `cts_client_tasks`, `cts_release_task`, `cts_pause_all`, `cts_resume_all`, `cts_stop_now`, `cts_studios_status`.
- Pipeline: `cts_run_pipeline {series, episode, brief?, options?, retry?, from?}` (resume by re-calling; it stops at `waiting-on-user` after the pitches and at the sheet review), `cts_pitch_choose {series, pitch}` (only with the pitch the user chose), `cts_sheet_approve {series, cast, ok, note?}` (only with the user's word), `cts_timeline_build`, `cts_lint {series, episode, requireAudio}`.
- Series and data: `cts_series_create`, `cts_series_get`, `cts_series_update`, `cts_cast_get`, `cts_set_get`, `cts_set_update`, `cts_episode_create`, `cts_episode_get`, `cts_script_set`, `cts_text_set`.
- Rigs and poses: `cts_rig_set {series, cast, variant?, rig, parts}`, `cts_rig_check`, `cts_rig_build {series, episode, cast, path}` (claude-svg = a, raster = c), `cts_rig_compare`, `cts_rig_choose {series, cast, variant}` (before making poses), `cts_pose_sheet`, `cts_pose_make {series, episode, cast, gesture, facePlates?}`. Options for the run: `options.rigPaths {cast: [paths]}`, `options.rigChoice {cast: variant}`.
- Render: `cts_render {series, episode, langs, quality}` (jobs; `cts_render_status`; a final render returns `minUnderDb`), `cts_frames` (contact sheet).
- Flow clips: `cts_clip_plan {series, episode}` (prints the `video-plan.mjs` commands), `cts_clip_generate {series, episode?, clip: "intro"|"outro", maxCredits, polish?}`, `cts_clip_review`. The clips step waits (`waiting-on-user`) until `cts_budget_set` recorded a `flowCreditsCap` and every missing clip has its `max_credits` (`cts_run_pipeline {options: {clipCredits: {intro: <n>, outro: <n>}}}`); `options.skipClips: true` drops them (record NOT RUN).
- Voices and music: `cts_voice_plan`, `cts_voice_generate`, `cts_voice_status`, `cts_voice_quota`, `cts_music_generate {series, tags, bpm?, seed?, seconds?}`.
- Images and budget: `cts_budget_set`, `cts_budget_get`, `cts_image_generate {provider, prompt, init?, denoise?, mask?, refs?}` (comfy Z-Image text-to-image, img2img or inpaint; gemini only after a yes and a cap).

## 7. Run log template

Copy `runs/_template.md` to `runs/<slug>.md` and add:

```
# <series> / <episode>
Started <date>. Brief: <idea or given pitch, ages, languages, length>.
## Money
- Cap USD: 0 · Flow credits cap: <n> (user said "<words>" on <date>) · Spent (cts_budget_get): <usd> / <credits>
- video-plan.mjs estimate: · flow_status credits before / after (write "not read" when it was not read)
## Ids and paths
- Series slug / episode id · data folder · engine started with hub.ps1 (time) · encoder
- Pitches shown (time), user pick (time, id) or the given pitch
- Character sheets: per character the seeds, the picked candidate, seconds per image; shown to the user (time), approved or redo (time, the user's words) · first rig job time (must be later)
- Rigs: character -> path (raster | claude-svg), face states (inpaint / drawn), minutes · poses made (gesture, denoise, review verdict)
- Voice allocation per language (reason) · cts_voice_quota before / after · providers per language
- Music: engine, seed, wall time · sound effects
- Clips: ids, files, credits, review verdicts
## Log
- <date time> step, job id, result
## Renders
- per language: preview and final seconds, wall time per stage, file paths, ffprobe summary, loudness, mix-check (minUnderDb, medianUnderDb, gapMusicUnderVoiceDb)
## Reviews
- safety verdict · frame-review verdicts and open problems
## Checked / not checked
- DONE / NOT DONE / UNTESTED per item; the user's verdict on hr and en, the look, the music and its level, go/no-go
```
