---
status: done
request: REQ-0022
repos: [creative-hub, cartoon-studio]
branch: HUB-30_cartoon-3d (hub), CTS-18_blender-3d (cartoon-studio)
updated: 2026-11-08
---

# HUB-30: Cartoon Studio goes 3D (Blender render backend + pilot 3, Pip and Bruno)

Request: `.claude/director/requests/REQ-0022-cartoon-episodes.md` (log 2026-11-08). Before this: `HUB-29-cartoon-studio/plan.md` (phase 1 and `# Pilot 2`), its `changelog.md` and `handoff.md`, `runs/cartoon-pilot.md`, `runs/pip-bruno-pilot.md`. Evidence for this plan: the Blender probe in `.claude/temp/blender-probe/` (`notes.md`, `build_scene.py`, `render.py`, `shot.json`, `visemes.json`, `contact.jpg`, `stills/`). Code read: `cartoon-studio` on `CTS-10_pilot-2` at `08efa1d`.

**Why.** On 2026-11-08 the user judged both cutout pilots "not good at all" and said changing models will not fix it. The run log of pilot 2 and the HUB-29 roadmap row still say "Good, go"; the REQ log supersedes them. The director proposed a 3D route in Blender. A 15 s probe of Pip and Bruno in the park looked clearly better (`contact.jpg`). It used simple primitive characters built in Python, parented-empty rigs, six-mouth visemes from text + audio, inverted-hull outlines and EEVEE at 0.13 s a frame at 1080p on the AMD 8060S. The user said "Yes, plan it".

**Reading (narrow, per the global Scope rule):** this plan builds a **Blender render backend inside Cartoon Studio** and makes **pilot 3**: a 60 s Pip and Bruno episode in hr and en, made the 3D way from start to finish through the pipeline and the `cts_*` tools. Phase 2 (a full 5-10 min episode) comes after the user's verdict on pilot 3 and is only outlined here (last section).

## Decisions

1. **One script, two renderers, chosen per series.** The bible gets `renderer: "canvas" | "blender"` (default `canvas`, so pilot 1 `pilot` and pilot 2 `pip-bruno` parse and behave as before). Pilot 3 is a **new series `pip-bruno-3d`**, episode `ep00-pilot`, so no pilot 2 file is touched. The script contract (`script.json`, `text/<lang>.json`) stays shared and gains only optional fields (decision 9).
2. **Characters and sets are data built by code.** No AI image is part of a character or set. A character is a JSON spec of primitives (`character.json`). The character-designer role writes it. A Python asset builder makes `character.blend` from it, which every episode reuses. Sets work the same way (`set3d.json` -> `set.blend`). This removes the identity drift seen with Z-Image: the same file is used in every shot and in both languages.
3. **Rig: parented empties, no armature.** Each character has the same named controls (decision 6). Why empties are enough: the parts are rigid primitives, so nothing needs skinning or weights. Every motion is computed in Python and baked to keys, so Blender's IK, NLA and pose library are not needed. Foot planting in the walk cycle is computed, not solved by IK. Empties are what the probe proved, and they are trivial to build, read and debug. **The way out:** the Python `Rig` wrapper addresses controls by name (`rig.ctrl("arm_L")`) and keys data paths only through it. If phase 2 needs bendy limbs, an armature can replace the empties with bones of the same names, and the acting library does not change.
4. **Motion is computed in Python as dense per-frame channels, then written in one go.** The acting library builds numpy arrays at 24 fps for every control channel, in layers: base (idle, locomotion), gesture (arms, body), head (look, accents), face (mouth, lids, brows, pupils) and secondary (springs on the ears, tail and scarf chains). They are written with the 5.x channelbag API (`bpy_extras.anim_utils.action_get_channelbag_for_slot`, `keyframe_points.add` + `foreach_set`). The interpolation is set on the keyframes after keying (CONSTANT for mouths and lids, LINEAR for dense channels), because `keyframe_new_interpolation_type` is ignored in background mode (probe). Dense keys make the layering, overlap and springs straightforward, and two builds of the same input give the same keys (determinism).
5. **Node owns the timing, Python owns the motion.** The engine keeps building a timeline per language from that language's audio lengths, as it does today. For a `blender` series the timeline is a new contract, `cts.timeline3d/1`. It holds the beats as semantic actions with times (walk to a mark, wave, look at, the shot list, visemes per frame, blinks). The Python assembler turns it into a Blender scene. **The two languages:** the animation of each language is regenerated from the same script beats with that language's timings. The hr and en films therefore have the same actions in the same order, stretched to their own line lengths. A gesture has a minimum and a maximum length. Inside a long line, the speaker fills the time with accents on word onsets (small head and hand beats from the whisper word times), so the gesture is not stretched past its maximum.
6. **Standard controls per character:** `root` (position on the ground, yaw), `squash` (scale about the feet), `body` (lean), `head`, `arm_L`, `arm_R` (shoulder pivot; optional `hand_L`/`hand_R`), `leg_L`, `leg_R` (optional: a character without legs hops or slides), `ear_L1..n`, `ear_R1..n`, `tail1..n`, `acc_<name>1..n` (chains for accessories such as the scarf tail), `lid_L`, `lid_R` (blink and half-lid by scale and rotation), `brow_L`, `brow_R` (optional), `pupil_L`, `pupil_R` (aim at a world target, clamped inside the eye), and `mouth` with six slot objects `rest A E O U MBP` (one shown at a time, by scale as in the probe). A character also has a **motion profile** in its spec: `tempo` (gesture speed factor), `energy` (amplitude), `bounce` (hop and idle bob), `walk` (stride, cadence, style `walk | hop | waddle`). Pip is fast, Bruno is slow, both from the same library.
7. **Lip-sync: six visemes from text + audio, word-timed where whisper hears the words.** It is code in the engine (TypeScript), so it is tested in the fast suite and Blender only keys the result. The order of methods:
   1. **`words-<lang>`.** The line WAV goes through flow-music-mcp `flow_transcribe` (whisper.cpp). It is installed, and the models are already in `~/.flow-music-mcp/models`: `ggml-large-v3-turbo-q5_0.bin` and `ggml-base.en.bin`, so nothing is downloaded. The language is always passed (`hr` is misdetected on auto, per the tool's note). Whisper words are aligned to the script words by a normalised edit distance. Each matched word's letters get visemes inside its `[t0, t1]`.
   2. **`text-<lang>`.** If whisper is down or less than 70 % of the words align, the probe's method is used: RMS voiced segments matched to phrases, letters spread by weight.
   
   Letter rules: hr is the probe's table (`lj`/`nj`/`dž` as one letter, vowel visemes, labials `m b p f v` -> `MBP`, `k g h` -> the next vowel, other consonants -> `E`). en uses a small grapheme table (digraphs `th sh ch ph ee oo ou ow ai ay`, silent final `e`, `w`/`qu` -> `U`, labials -> `MBP`); English spelling is rough, so the word times carry it. Then the probe's rules: 24 fps, a minimum hold of 2 frames, and a lip closure always shown for 2 frames. The method used per line goes in the lip-sync file and the run log. **Rhubarb is an optional English-only aid:** it needs a download and the user's yes, and it is not used in pilot 3.
8. **Look: one style file per series** (`style3d.json`) with the probe's clean look as the default:
   - Toon material: Diffuse -> Shader to RGB -> a constant two-stop ColorRamp (shadow shade 0.74, threshold 0.36) -> Emission.
   - View transform `Standard`, so the palette hexes come out exact.
   - Inverted-hull outlines (Solidify, offset 1, flipped normals, a backface-culled dark emission material; width per part size, colour `#2b2118`).
   - Sun without shadows, plus blob shadows under the characters.
   - Sky gradient; EEVEE with no raytracing and no shadows; TAA 16 samples for the final, 4 for the preview.
   
   Post effects are optional and off by default (`post: none | paper | posterize`), built with the 5.x compositor: a node group with a Group Output and `ShaderNodeMix` for mixing. The probe showed posterize crushes dark spines, so it stays off.
9. **The script vocabulary grows by optional fields only:**
   - `move` gains `style?: "walk" | "hop" | "run" | "tiptoe"` (default from the motion profile).
   - `gesture` gains `target?: <cast id | prop id | mark>` (point at, sit on, look at).
   - Gesture names, emotions and camera shot names must come from the acting library manifest and the set (lint).
   
   Old scripts parse unchanged.
10. **Cameras.** A set may define named cameras (`loc`, `target`, `lens`). The assembler also makes four computed shots from the actors' positions at the cut time: `wide`, `two`, `cu-<id>` and `ots-<a>-<b>`. Cuts are timeline markers bound to cameras (probe); pans and push-ins are keyed camera moves with ease. Framing rules: headroom, the speaker on a third, and no character cut at the feet in `wide`.
11. **Render: headless Blender (EEVEE) to PNG frames in chunks, then the existing ffmpeg path.**
    - Blender renders chunks of `chunkFrames` (default 240).
    - The engine encodes each finished chunk to a video segment with the chosen encoder (`h264_amf`, else `libx264`), then deletes its frames. A 10 min episode would otherwise need about 40 GB of PNGs (the probe made 1.1 GB for 15 s).
    - The segments are joined with the concat demuxer. The Flow clip splice, `muxEpisode`, the mix and `mix-check.json` are reused as they are.
    - Preview mode: 50 % resolution (960x540), TAA 4, the same scene.
    - Frame times are recorded with `render_pre`/`render_post` handlers into `render/<lang>/blender-times.json` (first frame, warm mean, p95, total), and `render.log` gets them next to the encode and mux stages.
12. **Blender version pinning.** `config/blender.md` has `path` (default `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`), `version: "5.2"` (major.minor; any patch), `chunkFrames`, the preview and final settings, and `allowUntestedVersion: false`.
    - The runner reads `blender --version` once per engine start and refuses another major.minor with `E_BLENDER_VERSION`, unless the override is set. It refuses a missing executable with `E_BLENDER_MISSING`.
    - Every run is `blender -b --factory-startup --python-exit-code 1 --python <script> -- <job.json>` with `PYTHONNOUSERSITE=1`, so the user's prefs and add-ons never change a render.
    - The 5.x API shims (channelbag, constant interpolation after keying, compositor group output, Workbench backface culling) live in one module, `cts_blender/api5.py`, and nowhere else.
13. **Engine to Blender protocol.**
    - The engine writes a job JSON (inputs, outputs, options) and spawns Blender.
    - The Python side prints one line per event on stdout: `CTS {"type":"progress","done":n,"total":m,"stage":"..."}`, `CTS {"type":"chunk","index":k,"from":f0,"to":f1,"dir":"..."}`, `CTS {"type":"result",...}` and `CTS {"type":"error","code":"...","message":"..."}`.
    - The engine parses these lines into `job.progress` events and the result. Any other output goes to the job log.
    - An `AbortSignal` kills the process tree.
    - A non-zero exit without a `result` line is `E_BLENDER_FAILED` with the last 40 log lines.
14. **The Canvas player stays, frozen, for `renderer: canvas` series. It is decided again after the user's verdict on pilot 3.** Why keep it now:
    - It renders pilot 1 and pilot 2 data and the `mini` fixture.
    - The fast suite and `render.e2e.test.ts` guard the shared code through it (timeline timing, mix, splice).
    - Deleting it on the same branch as the new backend adds risk to pilot 3's critical path for no gain to pilot 3.
    
    It gets no new features. If pilot 3 is a GO, phase 2 retires it together with Playwright (open question 3).
15. **The cutout authoring path is retired; only Z-Image text-to-image stays.**
    - **Deleted:** the body plan and sketches (`images/sketch.ts`), the Z-Image character sheet step (`cast_sheet` for cutout), raster rig building and face patches (`images/face.ts`, the raster and `claude-svg` builders in `pipeline/rig.ts`), pose images (`pipeline/poses.ts`), and the 2D set step (`images/background.ts`; `images/key.ts` if nothing kept imports it). Also the tools `cts_rig_build`, `cts_rig_compare`, `cts_rig_choose`, `cts_rig_set`, `cts_pose_make` and `cts_cutout`, and the test `rig-raster.test.ts`.
    - **Kept:** the rig and set contracts, `cts_rig_check`, `cts_pose_sheet` and lint (they read pilot 1/2 data).
    - **Kept for concept art:** `cts_image_generate` with the ComfyUI Z-Image graphs. The character-designer may make one concept picture per character for the user to look at next to the 3D sheet, but nothing is built from it. Img2img and inpaint stay in the ComfyUI client because `polish` on clip keyframes uses them.
    - **Gemini (Nano Banana) and fal** stay behind the budget gate, unused at $0.
    - In a `canvas` series the retired steps answer `E_RETIRED` (cutout authoring was retired in CTS-28). The code steps (timeline, preview, final render) still run, so pilot 1 and 2 can be re-rendered.
16. **Licence of the Blender scripts.** Scripts that `import bpy` are generally treated as covered by Blender's GPL when they are distributed. The repo is public and MIT. So the `blender/` folder gets its own `LICENSE` (GPL-3.0-or-later) and a README line, and the rest of the repo stays MIT; the engine calls Blender as a separate program. This is open question 2.
17. **Flow: intro and outro video only, cap 50 credits.** The keyframe is a Blender still of the clip's staging, not a player still. The pip-bruno intro and outro from pilot 2 are cutout-style. Whether they are reused, made again from Blender stills (about 2 x 12 = 24 credits) or skipped is open question 1. Until the user answers, the `clips` step waits (it already waits for a cap and `max_credits`).

## Kept, replaced, retired

| Part | Fate | Note |
|---|---|---|
| Bible, pitches, the given-pitch skip | kept | bible gains `renderer`, `style3d` path |
| Script and text per language, writer, safety (must pass) | kept | optional `move.style`, `gesture.target`; writer prompt lists the library names |
| Voice casting and allocation (hub rule), OmniVoice hr, Kokoro en, quota | kept | manifest `words` filled from whisper |
| Music from ComfyUI (CTS-15), mix and mix-check (CTS-16), ffmpeg mux, loudnorm | kept | unchanged |
| Flow intro/outro clips, credit gate, `video-plan.mjs` | kept | keyframe = Blender still |
| Frame review (frame-critic), contact sheets | kept | contact sheet cut from the preview MP4 frames; new checks (feet slide, limbs through body, framing) |
| Budget gate, spend ledger, $0 caps | kept | unchanged |
| Pipeline state machine, client tasks, roles, MCP server | kept | step list per renderer |
| Studio app views, installer | kept | Cast and Settings changed, Preview plays the preview MP4 for `blender` series |
| Z-Image character sheets, sketches, raster rigs, face patches, pose images | **retired** (deleted) | replaced by character specs and the Blender builder |
| Claude-drawn SVG rigs (path a) | **retired** (deleted builder) | pilot 1 rigs still render |
| 2D sets (Z-Image backgrounds and keyed props) | **retired** (deleted step) | replaced by set specs |
| Canvas puppet player as the renderer | **replaced** for `blender` series; **frozen** for `canvas` series | decision 14 |
| Amplitude lip-sync (12 fps, 3 shapes) | kept for `canvas`; `blender` uses the 6-viseme lip-sync at 24 fps | |
| Z-Image text-to-image | kept as an optional concept-art tool | not a pipeline input |

## Data layout (new files, `~\CartoonStudio\series\<slug>\`)

```
bible.json                     renderer: "blender", style3d: "style3d.json"
style3d.json                   cts.style3d/1 (look, decision 8)
cast/<id>/character.json       cts.character3d/1 (the spec)
cast/<id>/character.blend      built asset (appended into every scene)
cast/<id>/sheet.png            turnaround + expressions (the user's pause)
cast/<id>/sheet/*.png          front, three-quarter, side, back; expressions; mouths
cast/<id>/build.json           spec hash, Blender version, build seconds, control list
cast/<id>/concept.png          optional Z-Image concept picture (never an input)
sets/<id>/set3d.json           cts.set3d/1
sets/<id>/set.blend            built asset
sets/<id>/sheet.png            4 views (wide, two marks, each named camera)
episodes/<ep>/timeline.<lang>.json     cts.timeline3d/1
episodes/<ep>/lipsync/<lang>/<line>.json   cts.lipsync/1, fps 24, method words-<lang> | text-<lang>
episodes/<ep>/render/<lang>/scene.blend    assembled scene (kept for inspection, rebuilt when inputs change)
episodes/<ep>/render/<lang>/assembly.json  actions per actor, shots, spec and asset hashes, warnings
episodes/<ep>/render/<lang>/blender-times.json, render.log, mix-check.json, levels.json
episodes/<ep>/out/<lang>.mp4, <lang>.preview.mp4
```

## Contracts (all zod in `src/shared/contracts.ts`, documented with checked examples in `docs/contracts.md`)

- **`cts.character3d/1`**: `{ id, units: "m", height, palette: { <name>: "#hex" }, motion: { tempo, energy, bounce, walk: { style, stride, cadence } }, controls: { <name>: { parent, at: [x,y,z], rot?: [deg x3] } }, parts: [{ id, shape: "ellipsoid" | "cone" | "box" | "capsule" | "torus" | "arc" | "spines", size, at, rot?, colour: <palette name>, control: <control name>, outline?: <m>, spines?: { count, length, radius, keep: "back" | "top" | "all", lean } }], face: { control: "head", eyes: { x, z, r, faceY, pupil: { size, lead } }, lids: { colour }, brows?: { colour, at, length }, mouth: { at, scale, inner: "#hex", tongue?: "#hex" } }, accessories?: [...parts] }`. Lint: every standard control exists (legs, ears, tail, brows optional), every part names a known control and palette colour, the eyes and mouth lie in front of the head surface (the probe's buried-mouth bug: the check is a ray test in the builder, `E_FACE_HIDDEN`).
- **`cts.set3d/1`**: `{ id, ground: { size, colour, patches: [{ shape, at, size, colour }] }, sky: { top, horizon }, props: [{ id, kind: "tree_round" | "tree_cone" | "bush" | "bench" | "rock" | "flowers" | "fence" | "house" | "cloud", at, rot?, scale?, colours?, seat?: { height, at } }], marks: { <name>: [x, y] }, cameras: { <name>: { loc, target, lens } } }`. Lint: marks are on the ground and clear of prop footprints; a `sit` target has a `seat`.
- **`cts.style3d/1`**: `{ toon: { shade, threshold }, outline: { colour, scale }, world: { sky }, sun: { angle, energy }, samples: { final, preview }, post: "none" | "paper" | "posterize", stepped: false }` (`stepped: true` holds poses on twos for a stop-motion feel; off by default).
- **`cts.timeline3d/1`**: `{ schema, series, episode, lang, scriptHash, fps: 24, size, duration, seed, scenes: [{ id, set, t0, t1 }], actors: { <id>: { start: { mark, facing }, actions: [{ beat, action, t0, t1, params }], look: [[t, target | null]], emotion: [[t, name]], mouth: [[t, viseme]], blinks: [t], speaking: [[t0, t1]], accents: [t] } }, shots: [{ t, shot, transition: "cut" | "pan" | "push", seconds? }], audio, lines, clips, titles, beats }`. `audio`, `lines`, `clips`, `titles` and `beats` have the exact shapes of `cts.timeline/1`, so `render/mix.ts`, the splice and `E_LANG_ORDER` are reused.
- **`cts.lipsync/1`** gains `fps: 24` and `method: "words-hr" | "words-en" | "text-hr" | "text-en"` beside `amplitude`; `shapes` uses `rest A E O U MBP` for these methods.
- **Acting library manifest** `blender/cts_blender/acting/library.json` (the single source for names): per action `{ name, kind: "gesture" | "locomotion" | "react" | "camera", parts, seconds: { min, default, max }, overLine: bool, needsTarget: bool, params }`. The engine reads it for lint, the writer prompt and the timeline; the Python registry must match it (test B2).
- Bible: `renderer`, `style3d?`; cast entry `character?: "cast/<id>/character.json"` and `sheet` (approval, now with `specHash` instead of `denoise`/`model` for 3D); `rig` stays for canvas series.

## The acting library (the main quality risk, designed in)

`blender/cts_blender/acting/`: each action is a Python function `(ctx, actor, t0, t1, params) -> channel layers`. `ctx` holds the fps, the actor's rig, motion profile, positions of the others and props, and a seeded RNG.

**Principles every action follows.** These are code, not hopes:
- **Phases:** anticipation (5-15 % of the time, opposite direction), action, overshoot and settle (a damped return, 10-25 %).
- **Easing:** slow-in/slow-out curves, never linear on poses.
- **Overlap:** the head lags the body by 2 frames and the arms by 1-3 frames (offset layers).
- **Arcs:** hand paths are rotations about the shoulder, so the hand already moves on an arc.
- **Moving holds:** idle breathing continues under every hold, so nothing freezes.
- **Secondary motion:** ears, tail and accessory chains follow their parent's world motion through a damped spring (stiffness and damping per chain in the spec), baked per frame after all other layers.
- **Timing:** scaled by the profile's `tempo` (Pip about 1.4x faster than Bruno).

**Actions in pilot 3:**
- **Idle and body:** `idle` (breathe, weight shift, seeded micro-motion; always on), `blink` (seeded every 2.5-5 s, also on a head turn), `look_at` (pupils lead, head follows 2-3 frames later, body only past 60 degrees).
- **Locomotion:** `walk` (a cycle from the profile: contact, down, passing, up; feet planted in the contact phases with less than 2 cm of slip, hips bob, arms swing opposite, a start and a stop step; for a character without legs a `hop` cycle), `hop`, `run`, `turn` (anticipation, then root yaw).
- **Gestures:** `point` (at a target), `wave`, `nod`, `shake_head`, `shrug`, `think` (hand to chin), `sit` / `stand_up` (onto a prop `seat`), `cheer` (both arms up).
- **Reactions:** `react_surprised` (squash, stretch, small jump, ears up, eyes wide), `laugh` (body shake, head back, eyes closed), `droop` (sad).
- **Listening (automatic):** when nobody gives the listener a beat, the listener looks at the speaker, nods now and then on the speaker's accents, and blinks.
- **Talking (automatic):** small head accents and eyebrow lifts on word onsets during the actor's own lines.
- **Camera:** `cut`, `pan` (ease), `push` (slow dolly-in), `follow` (keeps a walking actor framed), `shake_small`.

Layer composition, per channel and frame:

```
value = base + gesture (weight-blended in/out over 4 frames) + head + face + secondary
```

Mouths, lids and pupils are a separate layer from the body, so lip-sync never fights a gesture. Whether a gesture may overlap a line comes from the manifest (`overLine`); lint warns `W_GESTURE_OVER_LINE` when it may not.

## Engine integration

- **Where the code lives:**
  - `blender/` at the repo root: `cts_blender/` (`api5.py`, `io.py` for the job JSON and the CTS stdout protocol, `materials.py` for the look, `build_character.py`, `build_set.py`, `sheets.py`, `acting/` with `library.json` and one module per family, `assemble.py`, `render.py`, `still.py`), plus `blender/tests/`, `blender/LICENSE` and `blender/README.md`.
  - Entry scripts: `blender/run.py <command>`, where the command is `build-character | build-set | sheet | assemble | render | still | probe`.
- **The Node side** (`src/engine/blender/`):
  - `config.ts` (`config/blender.md`), `runner.ts` (spawn, version check, protocol parse, abort), `jobs.ts` (character build, set build, sheet, assemble, render, still, as queue jobs with `job.progress` events), `tools.ts` (the MCP tools below).
  - `src/engine/anim/timeline3d.ts` (beats -> `cts.timeline3d/1`, sharing the beat timing pass with `timeline.ts`, which is refactored so both use one timing function).
  - `src/engine/anim/visemes.ts` (decision 7).
  - `src/engine/render/blender.ts` (chunk loop, encode, then `muxEpisode`). `cts_render` dispatches on the bible `renderer`.
- **Packaging:** `electron-builder.config.cjs` `extraResources` gains `{ from: "blender", to: "blender", filter: ["**/*", "!tests/**"] }`, and `scripts/verify-package.mjs` checks `resources/blender/run.py`. Blender itself is not bundled; the user has it installed, and Settings shows the path.
- **Tests:**
  - `yarn test:blender` runs `blender -b --factory-startup --python-exit-code 1 --python blender/tests/run.py` (unittest, Blender's own Python, no pip installs). It fails, not skips, when Blender is missing, like `test:e2e` without a browser.
  - `yarn test:e2e` runs the existing render e2e plus `tests/blender.e2e.test.ts`.
  - `yarn test` stays fast (no Blender, no browser).

## MCP tools and the app

- **New tools:**
  - `cts_blender_status` (path, version, GPU from `gpu.platform`, OK or the error code).
  - `cts_character_set { series, cast, spec }` (validates and writes `character.json`) and `cts_character_build { series, cast }` (job: `character.blend`, `sheet.png`, `build.json`; Blender errors such as `E_FACE_HIDDEN` come back as the result).
  - `cts_character_get`.
  - `cts_set3d_set` / `cts_set3d_build` (the same for sets).
  - `cts_scene_assemble { series, episode, lang }` (job: `scene.blend`, `assembly.json`).
  - `cts_still { series, episode, lang, t }` (one frame as PNG; used for the clip keyframes and for quick looks).
- **Changed tools:**
  - `cts_sheet_approve` (works for 3D sheets; writes `specHash`).
  - `cts_render` (dispatch, plus `blenderTimes` in the result).
  - `cts_timeline_build` (3D for `blender` series).
  - `cts_lint` (the new contracts, `E_ACTION_UNKNOWN`, `E_MARK_UNKNOWN`, `E_SHOT_UNKNOWN`, `W_GESTURE_OVER_LINE`, viseme coverage).
  - `cts_clip_generate` (keyframe from `cts_still`).
  - `cts_status` (shows the Blender job stage).
- **Removed tools:** those listed in decision 15. `docs/mcp-guide.md` lists them under "retired in CTS-28".
- **Studio app:**
  - The Cast view shows, for a `blender` series, the turnaround and expression sheet, the spec hash, the build time, the optional concept picture and the approve and redo buttons (with `data-testid`s). Canvas series keep their view.
  - The Sets view shows the set sheet.
  - The Preview view plays `out/<lang>.preview.mp4` in a `<video>` for `blender` series.
  - Settings gains a Blender section: path (editable, written to `config/blender.md` through a new `cts_blender_config` tool), detected version, GPU and the preview and final samples.

## Tickets (cartoon-studio, one commit each)

Branch: **`CTS-18_blender-3d`**, cut from `CTS-10_pilot-2` (tip `08efa1d`, checked at the start), so the ComfyUI music, the mix and mix-check work (CTS-15/16) and the rest of pilot 2 are kept.

**What happens to pilot 2's PR plan:** `CTS-10_pilot-2` is not pushed on its own. The user rejected its look, and CTS-28 deletes most of what it added. Its commits reach GitHub inside `CTS-18_blender-3d`, which is pushed after the checker passes and A3's grep. The PR goes to base `CTS-01_pilot` while PR Tihi321/cartoon-studio#1 is open, else to `master`. No auto-merge, no force-push. The local `CTS-10_pilot-2` branch stays as history. (Open question 4.)

Order: CTS-18 -> CTS-19 -> (CTS-20, CTS-21, CTS-22 and CTS-24 in parallel; disjoint files) -> CTS-23 -> CTS-25 -> CTS-26 -> CTS-27 -> CTS-28 -> CTS-29. Then pilot 3 (P, hub session) and V (checker). Workers run Node through `fnm exec --using default` and Yarn per the memory note, keep scratch files in `.claude/temp/`, and end every item DONE, NOT DONE or UNTESTED.

### CTS-18. Blender runner and config
- `config/blender.md` seed (decision 12), `src/engine/blender/{config,runner}.ts`, the stdout protocol (decision 13), `blender/run.py` + `cts_blender/{api5,io}.py`, the `probe` command (version, GPU), `cts_blender_status`, `cts_blender_config`. Add `yarn test:blender`, the `blender/tests/run.py` harness, `blender/LICENSE` (subject to Q2) and the packaging (`extraResources`, `verify-package`).
- Output: `cts_blender_status` answers `{ ok: true, version: "5.2.x", gpu: {...} }` on this machine; a wrong path gives `E_BLENDER_MISSING`.

### CTS-19. 3D contracts, lint and the `mini3d` fixture
- The contracts above, the bible fields, the optional script fields, the lip-sync methods, the library manifest reader, lint dispatch by renderer and the new codes, plus `docs/contracts.md` (`yarn docs:check` passes).
- Fixture `tests/fixtures/mini3d`: one series, two small characters (one with legs, one without), a set with a bench, a 3-beat script, fake voice manifests.
- Output: `mini` and `mini3d` both lint to 0 errors.

### CTS-20. Character builder and sheet
- `build_character.py` (primitives, materials from the style, outlines, controls, face and mouth slots, the ray test for the face, `character.blend`) and `sheets.py` (front, three-quarter, side and back at 1024x1024 each; six mouths; blink and half lid; happy, sad and surprised; pupils looking left and right; one `sheet.png`). Plus `cts_character_set/build/get` and the designer's prompt (`seed/prompts/character-designer/character-spec.md`), which starts from the bible look and a reference spec (the probe's Pip and Bruno converted to specs as examples in `seed/style/toon-3d.md`).
- Designer loop: spec -> build -> the designer reads `sheet.png` (vision) -> at most 2 revisions -> the user's pause.

### CTS-21. Set builder and sheet
- `build_set.py` with a prop kit (round and cone trees, bush, bench with a seat, rock, flower scatter, fence, simple house, cloud): ground and paths, sky gradient, marks as empties, named cameras, `set.blend`; the set sheet (4 views), `cts_set3d_set/build`, and the background-artist prompt (`set-spec.md`).

### CTS-22. Look
- `materials.py` and the style file (decision 8): toon ramp, outlines, blob shadows, sky, view transform, samples, optional post through the 5.x compositor. The default `style3d.json` is the probe's look.
- Output: a still of `mini3d` with the default look and one with `post: paper`, both read by the worker.

### CTS-23. Acting library
- `acting/` with every action named above, the layer composition, the springs, the walk and hop cycles with foot planting, listening and talking automation, and the camera moves; `library.json`; the dense-channel writer through `api5.py`.
- Output: a 10 s acting reel of `mini3d` (walk 3 m, sit, stand, wave, point, nod, shake, shrug, react, laugh, camera push) rendered at preview size. The worker reads its contact sheet and writes down what looks wrong (feet sliding, limbs through the body, pops).

### CTS-24. Lip-sync from text, audio and whisper word times
- `anim/visemes.ts` (decision 7). `studios/flow.ts` gains `transcribe(file, language)`, which calls flow-music-mcp `flow_transcribe`. The voice step fills the manifest `words` (alignment and coverage per line). Lint: every line has a lip-sync file of a six-viseme method, at least 60 % non-rest frames, at least 3 distinct visemes, and an `MBP` when the text has a labial (`E_MOUTH_SILENT`, `W_VISEME_FLAT`).

### CTS-25. Timeline 3D and scene assembly
- `anim/timeline3d.ts` (beats -> actions with times, gesture length limits, accents from word onsets, seeded blinks, look targets, the shot list from camera beats and the computed shots) and `assemble.py` (append the character and set assets, place actors at marks, run the acting library, key mouths, lids and pupils, add the cameras and cut markers, add the title cards as 3D text over a plate, write `scene.blend` and `assembly.json`). Plus `cts_scene_assemble` and `cts_still`.
- Output: `mini3d` assembles in hr and en with the same action list and different times.

### CTS-26. Blender render backend
- `render.py` (chunks, frame time handlers, preview/final settings) and `render/blender.ts` (chunk encode, concat, splice, `muxEpisode`, mix-check, `render.log` with the Blender frame stats). Contact sheets from the preview MP4 frames, and `cts_render` dispatch.
- Output: the `mini3d` preview and final MP4s; `blender-times.json`.

### CTS-27. Pipeline, tools and app for `blender` series
- The step list for `renderer: blender`:
  1. `pitch` / `pitch_choice` (skipped with `brief.pitch`)
  2. `bible` (writes `style3d.json` from the default)
  3. `character` (designer spec + build + self-review)
  4. `sheet_review` (**pause**)
  5. `set3d` (spec + build + self-review)
  6. `script`
  7. `safety`
  8. `voice_cast`
  9. `voice` (+ whisper words)
  10. `music`
  11. `clip_shots` / `clips` (keyframe = `cts_still`; waits for the cap and `max_credits`)
  12. `timeline` (3D + lip-sync + lint)
  13. `assemble`
  14. `preview_render`
  15. `frame_review`
  16. `final_render`
  
  `normalise` keeps canvas states as they are. Also: the Cast, Sets, Preview and Settings views (above); the writer, background-artist and frame-critic prompts (library names, marks, shots, 3D review checks); `docs/pipeline.md`, `docs/mcp-guide.md`.
- Output: `cts_run_pipeline` on `mini3d` with the mock provider reaches `done` (the existing pipeline test pattern, with the fake Blender runner).

### CTS-28. Retire the cutout authoring path
- Decision 15: delete the modules, tools, prompts (`body-plan.md`, `rig-raster.md`, `pose-review.md`, the SVG drawing rules) and `rig-raster.test.ts`; the canvas steps that are retired answer `E_RETIRED`. Pilot 1 and 2 still lint and re-render.
- Output: `git grep -nE "body-plan|buildRasterRig|face-report|poseJob|cts_rig_build|cts_pose_make|cts_cutout" -- src seed` returns nothing; `cts_lint` pilot and pip-bruno 0 errors.

### CTS-29. Docs and roadmap (repo side)
- `README.md` (3D first, the canvas renderer as legacy, Blender 5.2 as a requirement), `ROADMAP.md` rows CTS-18..29 (and pilot 2's rows marked "superseded by the 3D route"), `docs/blender.md` (protocol, the 5.x gotchas from the probe, how to add an action or a prop), `seed/style/toon-3d.md`, `docs/provenance.md` (the probe as origin of the builder, lip-sync and look code).

## Hub side (creative-hub, branch `HUB-30_cartoon-3d` cut from `HUB-29_cartoon-studio`)

`HUB-29_cartoon-studio` holds unpushed hub commits, so the new branch is cut from it, not from `master`.

- `.claude/skills/make-cartoon/SKILL.md`: the description and the steps become the 3D route:
  - character specs and the sheet pause, set specs, the acting library names, lip-sync methods, Blender status first;
  - the Flow intro/outro rule with the 50 cap; the voice rule unchanged;
  - "ask before any download (Rhubarb, add-ons, models)" and "never start Scriptorium".
- `ROADMAP.md`: a HUB-30 row. The HUB-29 row note corrected to "pilots 1 and 2 judged not good (2026-11-08); superseded by HUB-30". The uncommitted HUB-28 row belongs to another session and is left alone.
- `README.md`: the Cartoon Studio row (3D in Blender, needs Blender 5.2).
- `runs/pip-bruno-3d-pilot.md`: the run log (template from the skill).
- The `services.json` description line, if it says cutout.
- This ticket folder: `changelog.md`, `evidence/`.

## Pilot 3 steps (hub session through the skill, after CTS-27; CTS-28/29 may land before or during)

0. **Before.**
   - Run `cts_blender_status` (5.2.x, GPU named).
   - Run `cts_budget_set { series: "pip-bruno-3d", episode: "ep00-pilot", capUsd: 0, flowCreditsCap: 50, approvedBy: "user", note: "pilot 3, intro/outro only" }` before any Flow call.
   - Start cartoon-studio, ComfyUI, VibeTTS and flow-music-mcp with `hub.ps1`. Do not start Scriptorium, Chiptune Studio or Strata.
   - Record a hash list of `series/pilot/**/out/*.mp4` and `series/pip-bruno/**/out/*.mp4` (C13).
1. **Bible from p1.** `cts_run_pipeline { series: "pip-bruno-3d", episode: "ep00-pilot", brief: { pitch: <p1 copied from the pip-bruno bible>, ages 4-8, seconds 60, lineRange [12, 16], intro, outro }, options: { renderer: "blender" } }`. The showrunner keeps the pilot 2 cast looks (orange squirrel with a green scarf; stocky brown hedgehog) and palette.
2. **Character specs and sheets, then a PAUSE.**
   - The designer writes Pip's and Bruno's specs, starting from the probe geometry. Pip is quick and bouncy (`tempo` 1.4, hop-walk); Bruno is slow and heavy (`tempo` 0.75, waddle). Pip's tail has 3 joints and Bruno's back has spines.
   - Build both and self-review (at most 2 revisions).
   - Show both `sheet.png` in chat (and in the Cast view) and **wait for approve or redo per character**. Nothing else is built before both are approved (times in the run log).
3. **Sets.** `park`: an oak, a bench with a seat, round and cone trees, bushes, a sand path, clouds, sky. Marks: `left`, `center`, `right`, `bench`, `oak`. Cameras `wide` and `bench`. Build it and read the set sheet.
4. **Script and safety.** 12-16 lines, hr and en; at most 12 words a line. The episode must use at least 8 distinct library actions, including a `walk` of at least 3 m, a `sit` on the bench, a `point` at the oak, a `react_surprised` and a `laugh`, plus at least one `push` or `pan`. Intro first, outro last (if Q1 keeps them). Safety must pass.
5. **Voices (hub voice rule).** Run `cts_voice_quota` before and after. With 12-16 lines per language and 10 free Gemini requests, both languages go local: hr = OmniVoice through ComfyUI, Supertonic as the fallback; en = Kokoro. Whisper words for every line (`flow_transcribe`, language passed). Record the alignment rate per language.
6. **Music.** ComfyUI ACE-Step instrumental theme (40 s, soft and sparse), the engine and wall time in the log.
7. **Flow intro and outro (cap 50 credits).**
   - Show the user the pilot 2 intro and outro next to a Blender still of the pilot 3 staging, and ask: reuse, regenerate from Blender stills (`video-plan.mjs` estimate, about 24 credits) or skip (a title card).
   - Act only on the answer. Record the credits before and after (`flow_status`), the ledger and the `video-plan.mjs` record.
8. **Assembly, preview, frame review, finals.**
   - `timeline` (lint 0 errors), `assemble` per language, `preview_render` per language with the times.
   - Frame review: Claude reads the 12-frame contact sheets and the character sheets (on model, feet planted, no limb through the body, mouth shut in silence, eyes on the speaker, framing). Up to 2 rounds; fixes are data edits by the owning role.
   - Then the final 1080p renders in hr and en with `mix-check.json`.
9. **PAUSE: the user watches** `out/hr.mp4` and `out/en.mp4`. Ask for a verdict on the look, the acting (walks, gestures), the lip-sync and the music level, and for GO or NO-GO on phase 2 with this method.
10. **Run log** `runs/pip-bruno-3d-pilot.md`: every id, time, decision, measurement and verdict, and the UNTESTED items. Evidence goes in `.claude/tickets/HUB-30-cartoon-3d/evidence/`; the changelog goes in this folder.

## Tests (test-discipline: only these; existing tests updated where retired code was tested)

1. **B1 `blender/tests/test_build.py`** (Blender, background): the `mini3d` legged character builds with every standard control, six mouth slots and outlines; the face ray test catches a buried mouth (`E_FACE_HIDDEN`); two builds of the same spec give the same object, control and key hash.
2. **B2 `blender/tests/test_acting.py`**: the registry names equal `library.json`. Each gesture's keys stay inside `[t0, t1 + settle]` and come back to the rest pose. In a 3 m walk, each planted foot moves less than 2 cm in world space during its contact phase. A tail spring settles within 1 s after the root stops.
3. **`tests/visemes.test.ts`**:
   - hr golden: a generated WAV with two voiced segments and the text "Mama, dobro jutro!" gives the expected viseme sequence at 24 fps, with the `MBP` closures held 2 frames and `rest` outside the voiced time.
   - With given whisper words (one of them misheard), the visemes of each matched word fall inside its times, and alignment below 70 % falls back to `text-hr`.
   - en: "Bruno, look up!" gives `MBP` for the b and an `U` for "oo/u".
4. **`tests/timeline.test.ts`** (updated, one case added): from `mini3d` with fake manifests (hr longer than en), both 3D timelines have the same beat and action order, different durations, the gestures within their min/max seconds, and the mouth `rest` outside every line.
5. **`tests/blender.e2e.test.ts`** (real Blender): build `mini3d`, assemble 2 s, render a 320x180 preview. ffprobe shows h264 + aac, 24 fps, 2.0 ±0.1 s. `blender-times.json` has 48 frame entries. A bad `path` gives `E_BLENDER_MISSING`. The test checks no pixel hashes (EEVEE on a GPU need not be bit-identical); B1 covers determinism.
6. **Updated, not new:** `tests/contracts.test.ts` (`mini3d` parses; a script with an unknown gesture fails `E_ACTION_UNKNOWN`); the pipeline test of CTS-07 (a `blender` mock run reaches `done` with a fake runner); `rig-raster.test.ts` deleted with its code.

`yarn test` = 3, 4, 6 and the existing fast tests. `yarn test:blender` = 1, 2. `yarn test:e2e` = 5 and the existing render e2e (canvas, kept while the player is kept).

## Acceptance criteria (pilot 3)

| # | Criterion | Check that proves it |
|---|---|---|
| C1 | Builds and tests pass | `yarn typecheck && yarn lint && yarn test && yarn test:blender && yarn test:e2e && yarn build && yarn docs:check` exit 0 on `CTS-18_blender-3d` (outputs in the changelog) |
| C2 | Blender pinned, scripts packaged | `cts_blender_status` reports 5.2.x and the GPU; a 5.3 or missing path is refused (test 5, plus one manual run with `version: "5.1"` in a scratch config); `yarn dist:installer` passes `verify-package` with `resources/blender/run.py` present |
| C3 | Public repo clean | `git grep -nE "C:\\\\Users\|Infplane\|sk-[A-Za-z0-9]\|AIza"` on `CTS-18_blender-3d` returns nothing (A3 style), and `git grep -n "Program Files"` only in `seed/config/blender.md` and docs as the default install path |
| C4 | Render time per frame and per minute | `render/<lang>/blender-times.json` for the hr and en finals: warm mean ≤ 0.35 s a frame at 1920x1080 and p95 ≤ 0.6 s; final wall (Blender + encode + mux) ≤ 10 min per minute of film; preview wall ≤ 3 min per minute of film; the numbers are in the run log |
| C5 | Lip-sync visemes on every line | for both languages every line has `lipsync/<lang>/<line>.json` with method `words-*` or `text-*`; lint stats: ≥ 60 % non-rest frames, ≥ 3 distinct visemes, `MBP` present on lines with a labial; `E_MOUTH_SILENT` and `W_VISEME_FLAT` absent; whisper alignment rate per language in the run log; by eye: the user (C17) |
| C6 | Character consistency | `assembly.json` of hr and en carries the same `specHash` and asset hash per character as `build.json` and the approved `sheet.specHash`; Claude compares 12 contact-sheet frames per language with `sheet.png` (colours, parts, proportions, accessories present) and lists any difference; frame-critic `pass` or its problems listed |
| C7 | The user saw the sheets first | run log: `cts_sheet_approve` for Pip and Bruno earlier than the first `set3d` job in `jobs/done/` |
| C8 | Acting library used and sound | `assembly.json` lists at least 8 distinct actions including `walk` (≥ 3 m), `sit`, `point`, `react_surprised`, `laugh` and one `push`/`pan`; B2 passes (feet planted, settle, spring); Claude's frame review notes no limb through the body and no foot slide in the contact sheets |
| C9 | One animation plan, two languages | both timelines and both `assembly.json` have the same beat order and action ids (only the times differ); the same `scriptHash`; `E_LANG_ORDER` absent |
| C10 | Both films | `out/hr.mp4` and `out/en.mp4`: h264 1920x1080, 24 fps, yuv420p + aac, 50-75 s; `cts_lint` 0 errors |
| C11 | The mix-check numbers | `render/<lang>/mix-check.json` for hr and en: `minUnderDb ≥ 15`, `medianUnderDb ≥ 17`; integrated loudness -16 ±2 LUFS (`ebur128`); numbers in the run log |
| C12 | $0, Flow within the cap | `spend.json` has no `usd` entry; `budget.json capUsd 0`; voice manifests `costUsd: 0`; no gemini or fal request in `logs/`; Flow credits in `spend.json` ≤ 50 and only `intro`/`outro` video calls (or none, if the user chose reuse or skip); `flow_status` before and after in the run log; no download made (whisper models were already present; no Rhubarb, no add-on, no model) |
| C13 | Pilot 1 and pilot 2 data unharmed | the before/after hash lists of their `out/*.mp4` are equal; `cts_lint` on `pilot/ep00-pilot` and `pip-bruno/ep00-pilot` gives 0 errors; a 2 s canvas preview render of each succeeds on the new build |
| C14 | Cutout authoring retired, canvas renderer kept | CTS-28's grep returns nothing; MCP `tools/list` has none of the retired tools and has `cts_blender_status`, `cts_character_build`, `cts_set3d_build`, `cts_scene_assemble`, `cts_still`; C13 shows the canvas renderer still works |
| C15 | The app shows pilot 3 | `scripts/studio-shots.mjs` with no console error; in the built app on the real data (engine from `hub.ps1` stopped first): the Cast view shows both 3D sheets and the approval, Sets shows the park sheet, Preview plays the preview MP4, Settings shows the Blender path, version and GPU (screenshots in the run log) |
| C16 | Hub wiring | skill, ROADMAP rows (HUB-30 added, HUB-29 corrected), README row and run log exist (`git diff --stat` on `HUB-30_cartoon-3d`) |
| C17 | The user watched | the run log records the user's verdict on hr and en (look, acting, lip-sync, music level) and GO or NO-GO for phase 2 |

Every item ends DONE, NOT DONE (reason) or UNTESTED in `changelog.md`.

## Out of scope (explicit)

- **Phase 2:** a 5-10 min episode, more sets or characters, scene transitions between sets, a Scriptorium episode format, retiring the Canvas player and Playwright.
- **Downloads without the user's yes:** Rhubarb, Blender add-ons, extensions, asset packs, models. Bundling Blender in the installer. Any Blender version other than 5.2.x.
- **Paid work:** any paid call (cap $0), and Flow video beyond `intro`/`outro` or above 50 credits. Flow images, Flow Music.
- **Assets made another way:** AI image-to-3D meshes, Godot, Cycles renders, sculpted or hand-modelled characters (everything is built from specs), and AI images as character or set inputs.
- **Starting tools without asking:** Scriptorium (never without asking), Chiptune Studio.
- **Other repos:** changing another tool's repo (flow-music-mcp, comfy-mcp, VibeTTS, Edu); a gap there goes into that tool's `ROADMAP.md`.
- **Pilot 1 and 2 data:** changing it.
- **Git:** pushing before the checker passes, force-push, auto-merge.
- **Delivery:** subtitles, publishing anywhere, Android, macOS and Linux builds, code signing.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| The acting looks stiff or robotic (walks slide, gestures pop, nothing overlaps) | Principles are code (decision list in the acting section), B2 measures foot slip and settle, the CTS-23 acting reel is read before the pipeline uses it, the frame-critic checks feet and limbs, the motion profile gives each character its own tempo; the user judges the acting in step 9 |
| Primitive characters look cheap next to real shows | The probe already read clearly better than the cutouts; the sheet pause lets the user redo a character before anything else is built; spines, scarf and outlines give detail; the style file allows post effects later |
| Limbs pass through the body in gestures (rigid parts) | Per-gesture rotation limits per control in the spec; the builder records the body's radius so `point` and `wave` keep the arm outside it; frame review |
| Whisper misreads Croatian or is down | Language always passed; alignment by edit distance with a 70 % floor, else the text + RMS method (probe-proven); method per line recorded |
| English spelling makes the visemes wrong | Word times anchor them; grapheme table for the common digraphs; Rhubarb noted as an optional aid only after a yes |
| Render time grows with props and dense keys | Probe 0.134 s a frame; C4 allows 0.35 s; instanced props (linked duplicates); props far from the camera without outlines; preview at 50 % and 4 samples |
| Disk fills with frames | Chunked render: frames of a chunk are deleted once its segment is encoded; peak about 240 frames |
| EEVEE in background mode loses the GPU or a driver update breaks it | `cts_blender_status` names the GPU before a run; a failed render reports `E_BLENDER_FAILED` with the log tail; Workbench is a documented emergency fallback (probe: works, not faster, flat look) |
| Blender updates to 5.3 and the 5.x API moves again | Version pin with a refusal, all API differences in `api5.py`, `yarn test:blender` as the canary |
| GPL and the MIT repo | `blender/` under GPL-3.0-or-later (open question 2); the engine talks to Blender only through a process and JSON |
| Two renderers double the upkeep | The canvas side is frozen (no new features) and decided again after the pilot 3 verdict |
| The shared timing refactor breaks canvas timelines | `timeline.test.ts` keeps its canvas cases; C13 re-renders pilot 1 and 2 |
| Flow intro/outro clash with the 3D look | Keyframe from a Blender still; the user chooses reuse, regenerate or skip (Q1); credit cap 50 |
| Auto camera framing cuts heads or feet | Framing rules in code, named set cameras override, the frame-critic checks framing |
| Claude-time cost of the specs and reviews | Specs start from the probe's geometry and examples in `seed/style/toon-3d.md`; at most 2 self-revisions per asset |

## Phase 2 (outline, after the user's GO on pilot 3)

Episode 1 of `pip-bruno-3d`, 5-10 min, hr and en, 2-3 sets (the park plus, for example, Bruno's burrow and a pond), possibly a third character, scene changes with a short transition, more library actions as the script needs them (climb, carry, dig, run-and-stop), and longer music (two or three cues). Render budget: 14,400 frames at about 0.2-0.35 s means 50-85 min per language, run as a background job. Retire the Canvas player, Playwright and the canvas render e2e if 3D is confirmed. Optional: Rhubarb for English (after a yes), a stepped "on twos" look, a paper post effect, and a Scriptorium episode format (asked first). Acceptance mirrors C1-C17 with the length 300-600 s and the render time per minute of film unchanged.

## Open questions for the user

1. **Flow intro and outro for pilot 3:** (a) reuse the pilot 2 clips, (b) make them again from Blender stills (about 24 of the 50 credits), (c) skip them and use a title card. Recommendation: **(b)**. The pilot 2 clips are cutout-style and will clash with the 3D episode, and the cost fits the cap. The plan shows you both before spending.
2. **Licence of the Blender scripts:** put the `blender/` folder under GPL-3.0-or-later (the rest stays MIT). Recommendation: **yes**. Scripts that import Blender's API are generally treated as GPL when published, and the repo is public.
3. **Canvas player:** keep it frozen for pilot 1 and 2 until your verdict on pilot 3, or delete it now. Recommendation: **keep it frozen**. It keeps the old pilots renderable and the shared tests running, and deleting it now adds risk without helping pilot 3.
4. **Pilot 2 branch:** no separate PR for `CTS-10_pilot-2`; its commits go up inside `CTS-18_blender-3d` after the checker. Recommendation: **yes**. Its look was rejected, and most of what it added is retired by CTS-28. The music and mix work it carries is kept.
