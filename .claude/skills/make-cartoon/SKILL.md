---
name: make-cartoon
description: Turn an idea into a 3D toon cartoon episode or series for children (ages 4-8, characters and sets built in Blender 5.2 from specs, toon look with outlines, 60 s pilot to 5-10 min, Croatian and English from one script) by driving Cartoon Studio over MCP - a team of roles pitches premises (the user picks one), writes character specs that Blender builds into turnaround sheets (the user approves each), builds sets, writes and safety-checks the script with the acting library, casts voices, makes music in ComfyUI, lip-syncs six visemes from whisper word times, assembles and renders MP4s locally in Blender at $0 and reviews the frames. Use when the user asks for a cartoon episode, a cartoon series, 3D or cutout-style animation or a kids' cartoon with recurring characters. For a one-off short film made of Flow video shots use make-video; for a story or visual novel use make-visual-novel; for a game use make-edu-game.
---

# Make a cartoon episode or series

The hub is `C:\projects\Personal\creative-hub`. Cartoon Studio is `C:\projects\Personal\cartoon-studio` (public repo `Tihi321/cartoon-studio`), MCP on port 7465, data in `~\CartoonStudio`. Its own guide is the source of truth: `docs\mcp-guide.md` in that repo (also the MCP resource `cartoon-studio://guide`); the data contracts are `docs\contracts.md`. The plans behind it: `.claude/tickets/HUB-29-cartoon-studio/plan.md` (phase 1, the cutout pilots) and `.claude/tickets/HUB-30-cartoon-3d/plan.md` (the 3D route; the user judged both cutout pilots "not good at all" on 2026-11-08). Blender notes: the studio's `docs\blender.md`.

What it makes (series with `renderer: "blender"`, the default for new work): a series bible with `style3d.json` (the look), per character a spec `cast/<id>/character.json` built into `character.blend` and a turnaround + expression `sheet.png`, sets as specs `sets/<id>/set3d.json` built into `set.blend` with marks and named cameras, an episode script that is language-independent and uses the acting library's action names, a Croatian and an English 3D timeline (same actions, each language's own timings), and one MP4 per language rendered headless by Blender EEVEE in chunks plus ffmpeg (24 fps, 960x540 preview, 1920x1080 final). No AI image is part of a character or set; Z-Image is only an optional concept picture. Optional Flow video clips, only a series `intro` and `outro` (8 s each, keyframe = a Blender still), are spliced into the final render only. The old cutout series (`renderer: "canvas"`, pilots `pilot` and `pip-bruno`) still lint and re-render, but their authoring tools were retired (CTS-28) and answer `E_RETIRED`.

## 0. Before you start

1. `pwsh -File scripts\hub.ps1` (status). Start the studio with `pwsh -File scripts\hub.ps1 start cartoon-studio`, and what the run needs: `start comfyui`, `start comfy-mcp`, `start vibetts` (or the tray app), and `start flow-music-mcp` only for the Flow intro/outro. Chiptune Studio is not used. Strata is not running during ComfyUI work (shared memory). If the tools are missing from your list, the server was down when the session began: start it, then ask the user to reconnect (`/mcp`) or call tools through `pwsh -File scripts\hub.ps1 call cartoon-studio <tool> '<json>'`.
2. **One engine per data folder.** If the Cartoon Studio desktop app is open, its engine holds `~\CartoonStudio` and the headless start fails; to open the app, stop the hub's engine first (`hub.ps1 stop cartoon-studio`).
3. Never start Scriptorium for this (it resumes its whole book factory and may spend on paid models).
4. Open a run log `runs/<slug>.md` (template below): series slug, episode id, every decision, every id, timings, what you checked. A later session resumes from it.
5. Agree briefly, only if the user did not say: audience and age (default 4-8), languages (default hr + en), length (pilot about 60 s; an episode 5-10 min), who does the model work (default: you, $0, every role on `client/claude-code`).
6. **Ask before any download** (Rhubarb, Blender add-ons or extensions, asset packs, models, a ControlNet, a checkpoint). Whisper models for lip-sync are already in `~/.flow-music-mcp/models`.
7. **Blender first:** `cts_blender_status` must say `ok`, version 5.2.x and name the GPU. `E_BLENDER_MISSING` means the path in `config/blender.md` is wrong (fix it with `cts_blender_config`); `E_BLENDER_VERSION` means another Blender major.minor, which is refused (do not set `allowUntestedVersion` without the user's yes).

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
2. **bible**: cast, sets, tone, rules from the chosen pitch; `renderer: "blender"` (pass `options: {renderer: "blender"}` on the first `cts_run_pipeline`) and `style3d.json` written from the default look (toon ramp, outlines `#2b2118`, blob shadows, sky gradient, view transform Standard, `post: none`).
3. **character** (character-designer): per character a spec `cast/<id>/character.json` (`cts.character3d/1`: palette, primitive parts on the standard controls `root squash body head arm_L/R leg_L/R ears tail acc_* lid brow pupil mouth`, a face with six mouth slots `rest A E O U MBP`, and a motion profile `tempo energy bounce walk {style stride cadence}`), starting from the examples in the studio's `seed/style/toon-3d.md`. `cts_character_build` makes `character.blend`, `sheet.png` (front, 3/4, side, back, six mouths, blink, half lid, happy, sad, surprised, looks) and `build.json`; `E_FACE_HIDDEN` means an eye or the mouth is buried in the head. The designer reads `sheet.png` and revises at most twice.
4. **sheet_review: PAUSE.** Show the user every `cast/<id>/sheet.png` in chat (Read the PNG, and give the full path; also the app's Cast view) and wait. Call `cts_sheet_approve {series, cast, ok: true}` only on the user's approval (it records the `specHash`), or `{ok: false, note}` for a redo with their words. Nothing else is built before every character is approved; write the times in the run log.
5. **set3d** (background-artist): a spec `sets/<id>/set3d.json` (`cts.set3d/1`: ground and path patches, sky, props from the kit `tree_round tree_cone bush bench rock flowers fence house cloud`, a `seat` on what can be sat on, marks, named cameras), built with `cts_set3d_build` into `set.blend` and a 4-view `sheet.png` that the artist reads. Marks must be clear of prop footprints (`E_MARK_BLOCKED`).
6. **script** (writer): `script.json` plus `text/hr.json` and `text/en.json`; short lines (at most 12 words); gestures, reactions and camera moves only from the acting library (`blender/cts_blender/acting/library.json`: `walk hop run turn look_at point wave nod shake_head shrug think sit stand_up cheer react_surprised laugh droop` and the camera `cut pan push follow shake_small`), `move.style` (`walk | hop | run | tiptoe`), `gesture.target` (a cast id, prop or mark), marks and shots from the set (`wide`, `two`, `cu-<id>`, `ots-<a>-<b>` or a named camera). Lint: `E_ACTION_UNKNOWN`, `E_MARK_UNKNOWN`, `E_SHOT_UNKNOWN`, `W_GESTURE_OVER_LINE`. An `intro` clip beat first and an `outro` last when the episode has them.
7. **safety** (child-safety-reviewer): must pass; up to 2 revise rounds back to the writer.
8. **voice_cast** (voice-director): voice per character per language in the bible, with a short audition clip per character in `cast/<id>/voice/` for the user to hear.
9. **voice**: see the voice rule below. Then whisper word times per line (flow-music-mcp `flow_transcribe`, language always passed) fill the voice manifest `words` and `wordsCoverage`; write the alignment rate per language in the run log.
10. **music** (composer): a 40 s instrumental theme from ComfyUI (`ace-step-v1-instrumental`, alternative `minimax-music-3`; soft, sparse, under dialogue) and up to 2 MOSS sound effects.
11. **clips** (only with intro/outro beats and a recorded Flow credit cap): `cts_clip_plan`, the keyframe is a Blender still of the clip's staging (`cts_still`), then the 8 s scene with `max_credits` from `video-plan.mjs next`, `cts_clip_review`, `record` the credits. A clip that fails review twice is dropped and the beat falls back to a title card.
12. **timeline** (code): the 3D timeline per language (`cts.timeline3d/1`) and six-viseme lip-sync per line (`words-<lang>` from whisper times when at least 70 % of the words align, else `text-<lang>` from the text and the audio envelope); then `cts_lint` must have 0 errors (`E_MOUTH_SILENT`, `W_VISEME_FLAT` mean a mouth that does not move enough).
13. **assemble** per language (`cts_scene_assemble`): `render/<lang>/scene.blend` and `assembly.json` (actions per actor, shots, spec and asset hashes). hr and en must have the same action list; only the times differ.
14. **preview_render** per language (960x540, 4 samples) with `render/<lang>/blender-times.json`, and a 12-frame contact sheet cut from the preview MP4 (`cts_frames`).
15. **frame_review** (frame-critic): you read the contact sheets next to each `sheet.png`: on model (colours, parts, accessories), feet planted, no limb through the body, mouth shut in silence, eyes on the speaker, framing (no head or feet cut, speaker on a third); up to 2 rounds, fixes are data edits by the owning role.
16. **final_render** per language (1920x1080, 16 samples, rendered in chunks that are encoded and deleted as they finish) with the **mix check**: music 18 dB under the voice while someone speaks (floor 15 dB) and 8 dB under in the gaps (`config/render.md` `mix`); `render/<lang>/mix-check.json` has `minUnderDb`, `medianUnderDb`, `gapMusicUnderVoiceDb`, and lint warns `W_MIX_MUSIC_LOUD` under the floor. Copy those numbers into the run log.

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
- Blender: `cts_blender_status` (path, version, GPU), `cts_blender_config` (path, samples).
- Characters and sets (3D): `cts_character_set {series, cast, spec}`, `cts_character_build {series, cast}` (job: `character.blend`, `sheet.png`, `build.json`), `cts_character_get`; `cts_set3d_set`, `cts_set3d_build`, `cts_set3d_get`; `cts_scene_assemble {series, episode, lang}` (job: `scene.blend`, `assembly.json`); `cts_still {series, episode, lang, t}` (one frame as PNG, also the clip keyframe). `cts_rig_check` and `cts_pose_sheet` still read the old canvas series. Retired in CTS-28 (cutout authoring): `cts_rig_build`, `cts_rig_compare`, `cts_rig_choose`, `cts_rig_set`, `cts_pose_make`, `cts_cutout`.
- Render: `cts_render {series, episode, langs, quality}` (jobs; dispatches on the bible `renderer`; for blender series the result has `blenderTimes`: first frame, warm mean, p95, total; `cts_render_status`; a final render returns `minUnderDb`), `cts_frames` (contact sheet, cut from the preview MP4 for blender series).
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
- Blender: `cts_blender_status` (version, GPU) at the start
- Character sheets: per character the spec hash, revisions, build seconds; shown to the user (time), approved or redo (time, the user's words) · first `set3d` job time (must be later)
- Sets: set id, props, marks, cameras, build seconds · lip-sync methods per line and whisper alignment rate per language
- Voice allocation per language (reason) · cts_voice_quota before / after · providers per language
- Music: engine, seed, wall time · sound effects
- Clips: ids, files, credits, review verdicts
## Log
- <date time> step, job id, result
## Renders
- per language: preview and final seconds, wall time per stage, file paths, ffprobe summary, loudness, mix-check (minUnderDb, medianUnderDb, gapMusicUnderVoiceDb); `blender-times.json` (first frame, warm mean, p95) and the wall time per minute of film
## Reviews
- safety verdict · frame-review verdicts and open problems
## Checked / not checked
- DONE / NOT DONE / UNTESTED per item; the user's verdict on hr and en, the look, the music and its level, go/no-go
```
