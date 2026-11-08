---
status: in-progress
request: REQ-0022
repos: [creative-hub, cartoon-studio (new, C:/projects/Personal/cartoon-studio)]
branch: cartoon-studio `CTS-10_pilot-2` (from `CTS-01_pilot` f5c37b9; phase 1 on `CTS-01_pilot`, PR #1); creative-hub `HUB-29_cartoon-studio`
updated: 2026-11-08
---

> Pilot 2 (section `# Pilot 2 (CTS-10..)` at the end) was approved by the user on 2026-11-07 (answers recorded in handoff.md); phase 1 (everything above it) stays approved and done.

# HUB-29: Cartoon Studio, cutout-puppet cartoon series for children (phase 1: scaffold + 60 s pilot)

Evidence base: `research.md` in this folder (C = confirmed, I = inferred; file:line refs there). Request: `.claude/director/requests/REQ-0022-cartoon-episodes.md`. Template repo: `C:\projects\Personal\edu-game-studio` at `master` `46b6ec1`.

**Reading of the request (full, phased).** A new tool with its own repo that makes a *series* of South Park-style cutout cartoons for ages 4-8: cast, rigs and sets are made once and reused; each episode is 5-10 min with a Croatian and an English voice track over the same animation; the cutout base animation rendered locally to MP4 at $0, plus a few Flow video "hero shots" under a credit cap (user decision 6); a team of agent roles does the model work through the `client` provider (Claude, $0). Phase 1 (this plan, full task detail): repo scaffold plus a **60 s pilot** the user watches. Phase 2 (outline + acceptance only): episode 1 of a named series, 5-10 min. Phase 2 starts only after the user has watched the pilot and said go.

## User decisions (2026-11-07, binding; they resolve the plan's earlier open questions)

1. **Premise:** the showrunner pitches 3 series premises with two leads each; the user picks one before any art is made (a pause in the pipeline, step 1 of T7 and P2).
2. **Croatian voice:** OmniVoice through ComfyUI is the hr default (the user listened to samples; measured about 2x real time warm, about 17 s of audio for the test text). The Gemini allocation still runs first under the hub rule, but 12-16 lines do not fit the 10 free requests, so hr goes local, and local hr = OmniVoice (`comfy` provider); Supertonic is the hr fallback. en stays Kokoro.
3. **Budget: $0 for the pilot, no paid images.** The image provider slot, keyring, budget gate, ledger and `svg-split` are still built (T9), because later work depends on them. The rig comparison on character B is (a) vs (c); (b) Recraft is NOT RUN (no budget).
4. **Desktop app in phase 1:** Edu's Electron main/preload/renderer are copied, not deleted, and a studio UI (T10, CTS-09) plus the Windows installer are part of phase 1.
5. **GitHub (changed 2026-11-07):** public repo `Tihi321/cartoon-studio` (owner confirmed from Edu Studio's `origin`, `https://github.com/Tihi321/edu-game-studio.git`). T1 creates it after the first commit and pushes `master` with README/.gitignore/LICENSE only. `CTS-01_pilot` is pushed only after the checker (V) passes, then a PR to `master` with no auto-merge. A3's grep passes before every push. No force-push.
6. **Flow video hero shots are part of the pilot.** The base animation stays cutout. Flow video adds an 8 s series intro with the two leads (made from our character images as references, kept at series level and reused by every episode) and at most one 8 s hero moment inside the episode. Flow credits have their own cap (decision 7). The USD cap stays $0.
7. **Pilot Flow credit cap: 50 credits** (`flowCreditsCap: 50`, approvedBy user, 2026-11-07). `cts_budget_set` records it in the pilot episode's `budget.json` before any Flow video call; going past it needs a new yes from the user.
8. **Default ComfyUI image model: Z-Image Turbo** (`comfy.imageModel: z-image-turbo`, about 26 s per character reference and 39 s per background in the bake-off; Krea 2 Turbo is the configured alternative; `research.md` bake-off addendum).

Branches (named here so the user approves them with the plan; nobody creates one silently):
- `cartoon-studio` (new, public `Tihi321/cartoon-studio`): `git init` on `master` with one commit holding only `README.md` + `.gitignore` + `LICENSE`, then branch `CTS-01_pilot`; one commit per ticket CTS-01..CTS-09 (the Edu `roadmap` style). `master` is pushed by T1 (first commit only); `CTS-01_pilot` is pushed after V passes, then a PR to `master`, no auto-merge, no force-push (user decision 5).
- `creative-hub`: `HUB-29_cartoon-studio` from `master` for the wiring and records.

## Decisions taken in this plan (weighed from the director's notes and the research)

1. **Puppets: three candidate rig paths, one rig format.** The rig format takes `src: *.svg` or `*.png` per part, so every path below is a data producer, not a separate player.
   - **(a) Claude-drawn SVG from a reference: the default.** ComfyUI makes one front/three-quarter reference on flat grey; the character-designer (Claude in the hub session during P3, answering the `client` task) draws each part in **VectorCraft** over MCP from `ref.png` (`draw_shape`, `draw_path`, `set_paint`, `pathfinder`), checks it with `render_preview`, exports SVG, and hands the files to `cts_rig_set` / `cts_rig_check`. Hand-written SVG is the fallback when VectorCraft is not available or a part is simpler to write. A VectorCraft probe (test head + mouth set) is running; its result goes in `research.md` as an addendum (**pending**). The rig contract does not change and Cartoon Studio has no VectorCraft dependency. The parts are SVG (body, head, arms, feet, 3 eye states, 4 brows, 8 mouths) and `rig.json`. Why default: $0 and needs no budget yes; parts always match (one author, one palette, one outline width); pivots are exact; the face set is complete by construction; the South Park look is flat shapes by design. Diffusion cannot be told to draw in parts (research Risk 1).
   - **(b) Recraft V3 SVG parts (paid; NOT RUN in the pilot, budget $0; the code path exists for later).** Recraft makes the character as a vector illustration in one saved style (`style_id`), then the same style for a mouth sheet and an eye/brow sheet. Code parses the SVG and assigns each path to a part by Claude-given cut polygons (path centroid inside polygon); the sheets are sliced into the face states by their grid cells; Claude sets pivots. Risk: Recraft paths are not grouped by body part and an arm path may run under the torso, so joints may need a Claude touch-up of 1-3 paths.
   - **(c) Raster cutout (fallback).** Master on flat grey, keyed to alpha, cut by Claude-given polygons into part PNGs with overlap at joints (head over neck, arm over shoulder, rotation about +-25 deg max); the face stays a vector overlay from (a).
   - **Pilot comparison on one character:** character A is built with (a) only. Character B is built two ways from the **same reference image**: (a) and (c); (b) is recorded as NOT RUN (no budget). Each path is time-boxed to 45 min of the pilot run (P3b), its time recorded. One comparison sheet puts the B rigs side by side (neutral, two emotions, a gesture peak, A/E/O/MBP mouths) and a 10 s preview render of each. The pilot film uses B(a); the user picks the phase 2 default from the sheet when watching the pilot. A path over its time box is dropped and recorded as NOT DONE.
   - Optional painted texture: a part SVG may embed one `<pattern>` with a data-URI PNG (cut from the reference) clipped to its shape. Allowed by the format, used only if the flat look reads too plain.
2. **Phase 1 is a desktop app (Electron, copied from Edu) around the same engine.** The engine also runs headless (`node out/engine/index.js --mcp-only`, what `hub.ps1` starts) and serves MCP on 7465; one engine per data folder (Edu `store/lock.ts`), so the app and the headless engine do not run on the same data folder at once (the app's "Open in" pattern from Edu applies). The Canvas player is one bundle used three ways: embedded in the studio's timeline view, served at `http://127.0.0.1:7465/preview/...`, and loaded by the renderer in headless Chromium. "Build the app" means the Windows installer (`yarn dist:installer`, NSIS) and portable exe, as in Edu.
3. **Render**: deterministic Canvas 2D `renderFrame(i)` in headless Chromium driven by `playwright-core` (bundled Chromium if installed, else `channel: 'msedge'`), frames piped to ffmpeg. Output 24 fps; puppet poses step at 12 fps ("on twos"), camera moves at 24. Preview quality 960x540, final 1920x1080. Encoder `h264_amf` if it works on this machine, else `libx264 -preset veryfast -crf 20`; `yuv420p`, AAC 160k.
4. **Lip-sync**: amplitude in phase 1 (3 shapes: rest, E half-open, A open). Phase 2: whisper word times (flow-music-mcp `flow_transcribe`, shifted 0.12 s earlier) plus a Croatian letter-to-viseme table (8 shapes). Rhubarb is not used (optional later for English only).
5. **Two languages = one script, two timelines.** The episode script is language-independent (beats with line ids); text lives in `text/<lang>.json`. Each language gets its own timeline built from its own audio durations, then its own render. The beat order, blocking, gestures and camera are the same; only timing differs.
6. **Script**: Claude writes the episode through the `client` provider (writer role). A Scriptorium `cartoon-episode` format is a phase 2 option only (not committed).
7. **Voices**: Edu's allocation rule (Gemini free 10/day through flow-music-mcp, languages allocated whole, Croatian first) with one change: the local chain per language comes from `config/voice.md` (`localOrder: { hr: [comfy, vibetts], en: [vibetts, comfy] }`) instead of VibeTTS-first. With 12-16 pilot lines, hr goes local, so the pilot is **hr = OmniVoice via ComfyUI** (Supertonic fallback), **en = Kokoro** (user decision 2). OmniVoice's `instruct` takes attribute tags (gender, age, pitch and the like), not free style words, so a character's voice is its attribute tags plus an optional reference clip (`ref` + transcript), stored per character per language in the bible. comfy-mcp has no OmniVoice workflow, so Cartoon Studio posts the graph to ComfyUI `:8188` itself, as Edu's `tts-engines.ts` does; a working reference script is `creative-hub/.claude/temp/voice-test/gen.py` (graph: `OmniVoiceEngineNode` -> `UnifiedTTSTextNode` -> `SaveAudio`, `/prompt` then poll `/history/<id>`). A paid voice provider slot exists as an interface behind the same budget gate as images (decision 9); no paid voice client is written in phase 1.
8. **Roles: 8** (research "worth it" list): showrunner, writer, character-designer, background-artist, voice-director, composer, child-safety-reviewer (must pass), frame-critic (vision, Claude reads contact sheets). All default to `client/claude-code`, fallbacks `strata`, `lmstudio`; no paid model alias in any role. Translator is a phase 2 candidate (9th).
9. **Image providers and a spend cap.** One image interface `generate({ prompt, size, refs?, format: "png" | "svg", styleId? }) -> { file, costUsd, provider, model }` with providers `comfy` (local, $0, default), `flow` (free Google Flow images through flow-music-mcp, `max_credits: 0`, never video; tool `flow_generate`: the names `flow_generate`, `flow_narrate`, `flow_transcribe`, `flow_character`, `flow_wait`, `flow_status` exist in `flow-music-mcp/src` (grep, 2026-11-07); their arguments are checked by T6/T9 in the source before use), `fal` (FLUX 2 Pro / FLUX Schnell / Recraft V3 / SD3.5 through fal.ai) and `recraft` (vendor API, SVG). Keys live in the OS keyring (`@napi-rs/keyring`, Edu `models/keys.ts`, set with `node out/engine/index.js key-set <provider>`), never in files. Each production has a cap: `cts_budget_set { series, episode, capUsd, approvedBy, note }` writes `episodes/<ep>/budget.json`; every paid call (image or voice) estimates its cost from `config/prices.md`, and the engine refuses (`BUDGET_EXCEEDED`) when `spent + estimate > capUsd`; with no `budget.json` the cap is 0, so nothing is spent without the user's yes. Spend is appended to `episodes/<ep>/spend.json`; the skill copies cap and spend into `runs/<slug>.md`. **Pilot cap: $0** (user decision 3): no `budget.json` with a positive cap is written for the pilot, so every paid call is refused. Prices to check before any future budget: for Recraft V3 vector the user's source lists about $0.02-0.04 per image, the planner's memory about $0.04-0.08; neither is verified. **Flow credits** are a second currency in the same gate: `budget.json` has `flowCreditsCap` next to `capUsd`; `charge({ ..., currency: "credits", estimate })` refuses past it (`FLOW_CREDITS_EXCEEDED`), and with no recorded cap it is 0.
10. **ArtCraft apps are optional helpers in the hub session, never dependencies** (MCP servers of the suite, getartcraft.com): VectorCraft draws rig parts for path (a); PhotoCraft is an option for background cleanup and keying when the `sharp` colour key leaves a fringe; EffectCraft, FilmCraft and SoundCraft appear only under the phase 2 options. Cartoon Studio's code calls none of them, and our Canvas renderer stays the renderer.
11. **ComfyUI image model is configurable** (`config/providers.md`: `comfy.imageModel`, seeded as `z-image-turbo` with `krea2-turbo` as the listed alternative; user decision 8, from the bake-off of Z-Image, Qwen-Image 2.1 and Krea 2 in `research.md`'s addendum). Z-Image draws a white sticker halo round the figure: harmless for path (a), where the reference only guides the VectorCraft redraw; for path (c) the colour key must remove it (key the grey and then the near-white rim that touches the alpha edge, or PhotoCraft cleanup). **ComfyUI memory is freed between voice and image jobs** (comfy-mcp `free_memory` or ComfyUI `POST /free` with `unload_models: true, free_memory: true`), because a stale Higgs state broke the Qwen image runs in the bake-off; the queue does this whenever the next job's kind (voice/image) differs from the last.
12. **Flow hero clips (user decision 6).** New beat `clip`; clip files are MP4s at series level (`series/<slug>/clips/<id>.mp4`, the intro, reused by every episode) or episode level (`episodes/<ep>/clips/<id>.mp4`, the hero moment). Made through flow-music-mcp (`flow_character` portraits are not used; our `ref.png` and the pose-sheet render, or the VectorCraft render, go in as `reference_images`; a keyframe image first with `flow_generate` at `max_credits: 0`, then the 8 s video scene with `first_frame` from it), prompt asks for flat 2D cutout motion, no 3D, no shading, no speech. Estimates and each call's `max_credits` come from the hub's `scripts/video-plan.mjs` (reused, not copied: its `price()`/`PRICES` table and `next`/`record` state; 720p Omni 8 s = 12 credits seen). The frame-critic compares frames of the clip with the pose sheet; an off-style clip gets at most 1 retry, else it is dropped and the beat falls back to a title card plus a cutout bounce of the leads. The Canvas player draws a placeholder card in clip ranges (preview only, still deterministic); the final render splices the real clip in with ffmpeg.
13. Port **7465**, MCP prefix `cts_`, tickets `CTS-NN`, data `~\CartoonStudio`, env `CTS_DATA`, `CTS_MCP_PORT`, `CTS_MCP_TOKEN`, `CTS_SEED`, `CTS_AUTOSTART`, skill `make-cartoon`.

## Scope (phase 1)

0. Desktop app: Edu's Electron shell (main, preload, React renderer, electron-builder config, `dist*` scripts) copied and turned into the Cartoon Studio UI (T10), with a Windows NSIS installer and portable exe.
1. New repo `C:\projects\Personal\cartoon-studio` with the Edu engine core copied and trimmed: store + lock, queue, logs, budget, models (`client`, `mock`, openai-compat for Strata/LM Studio, router, registry), MCP server (Streamable HTTP, Host/Origin allow-list, `def(...)` tools), studios HTTP clients and autostart (VibeTTS, Chiptune Studio, flow-music-mcp, comfy), ComfyUI image client, voice allocation and quota.
2. The data contracts (series bible, rig, set, episode script, text catalog, voice manifest, lip-sync track, timeline) as zod schemas in `src/shared/contracts.ts`, documented in `docs/contracts.md`.
3. The puppet player (Canvas 2D, deterministic): embedded in the studio UI, served as the preview page, and used by the renderer.
4. Timeline builder, amplitude lip-sync, seeded blinks and idle bob.
5. Voice generation (allocation; Gemini via flow-music-mcp; OmniVoice via ComfyUI as the local hr default, Supertonic as hr fallback; Kokoro for en; paid slot stub behind the budget gate), music via Chiptune Studio.
6. Render (Playwright + ffmpeg), audio mix with ducking and loudness, contact sheets.
6b. Flow hero clips: the `clip` beat, the clip step (intro + at most one hero shot), the splice in the final render, and the Flow credit cap.
6a. Image providers (`comfy`, `flow`, `fal`, `recraft`), keyring keys, the per-production budget gate and spend ledger; the three rig paths of decision 1 as code (the pilot runs (a) and (c); its cap is $0).
7. Pipeline with the 8 roles as client tasks, `cts_*` MCP tools, `cts_lint`.
8. Hub wiring: `services.json`, `.mcp.json`, README table, `make-cartoon` skill, CLAUDE.md line, ROADMAP row HUB-29, `runs/cartoon-pilot.md`.
9. The pilot: one series stub, 2 characters, 1 set, 12-16 lines, hr and en MP4s of about 60 s, final render under 5 min per language; the user watches both.

## Out of scope (explicit)

- Phase 2 work (below, outline only): 5-10 min episode, named series, word-timed visemes, walk cycles beyond a slide-with-bob, more sets, Scriptorium format.
- Android; macOS/Linux builds; code signing of the installer; auto-update.
- Flow video beyond the intro and one hero shot, or any Flow video before `flowCreditsCap` is recorded; Flow Music; lip-synced speech inside Flow clips; paid LLM models; any paid TTS call. The `voicecreator` provider is an interface stub that refuses to run; no HTTP client for it is written (its API and timestamps are unconfirmed, research Q1).
- Any paid image call in the pilot (cap $0); running rig path (b) Recraft in the pilot; any spend past a cap in later work.
- Pushing `CTS-01_pilot` before V passes or before A3's grep passes; auto-merge of the PR; any force-push; pushing anything under `~\CartoonStudio` (user decision 5).
- Ideogram (text in images) and FLUX 3 via other resellers (Replicate) are not wired in phase 1; fal.ai and the Recraft API cover the candidates.
- Buying Voice Creator Pro (research verdict: skip the $55 app).
- Starting Scriptorium (CLAUDE.md: never without asking); Book Translator; Pixel Studio.
- Rhubarb install; whisper word-timed lip-sync (phase 2).
- Subtitles/captions burned into the MP4; title animation beyond one static title card.
- Changing code in any other tool's repo (Edu, VibeTTS, comfy-mcp, flow-music-mcp, Chiptune Studio). If a gap there is found, it goes into that tool's `ROADMAP.md` as a note.
- Publishing the cartoon anywhere (site, YouTube).

## Data layout (`~\CartoonStudio`, `CTS_DATA`)

```
config/            roles.md settings.md providers.md voice.md budget.md render.md studios.md autostart.md  (seeded from seed/config, editable markdown)
agents/            <role>-<name>.md
state/             gemini-tts.json (quota, Edu format) engine.lock
jobs/              queued/ running/ done/ failed/   (Edu queue)
series/<slug>/
  bible.json
  cast/<id>/       ref.png  parts/*.svg|*.png  rig.json  sheet.png (pose sheet render)
                   variants/<a|b|c>/{parts/, rig.json, sheet.png}  (pilot comparison of rig paths; the chosen one is copied up)
  sets/<id>/       layers/*.png  set.json
  music/           <cue>.ogg
  clips/           <id>.mp4 (series clips, e.g. the intro, reused by every episode)  clips.json [{ id, file, seconds, credits, flowMediaId, prompt, review }]
  episodes/<ep>/
    budget.json    { capUsd, flowCreditsCap, approvedBy, approvedAt, note }   spend.json  [{ t, provider, model, what, currency: usd|credits, amount }]
    clips/         <id>.mp4 (episode clips, e.g. the hero moment)   video/ (video-plan.mjs state for the clips)
    script.json    text/hr.json text/en.json
    reviews/       safety.json frames-<lang>-<n>.json
    voice/<lang>/  <lineId>.wav  manifest.json
    lipsync/<lang>/<lineId>.json
    timeline.<lang>.json
    render/<lang>/ sheet-<n>.png  render.log
    out/           <lang>.mp4  <lang>.preview.mp4
```

## Data contracts (owned by task T2; every other task imports them from `src/shared/contracts.ts`)

All files carry `schema: "cts.<kind>/1"`. Ids are `[a-z0-9-]+`. Times are seconds (float). Coordinates are pixels, y down. Text is never stored outside `text/<lang>.json` or the bible's `{hr, en}` maps.

### Series bible `series/<slug>/bible.json`

```json
{
  "schema": "cts.bible/1",
  "slug": "pilot",
  "title": { "hr": "...", "en": "..." },
  "audience": { "ageMin": 4, "ageMax": 8 },
  "logline": { "hr": "...", "en": "..." },
  "tone": ["gentle humour", "no peril beyond mild", "every episode ends warm"],
  "style": { "look": "flat paper cutout, solid colours, 6 px black outline", "palette": ["#f4d35e", "#ee964b", "#0d3b66", "#faf0ca", "#222222"], "outlinePx": 6, "refPrompt": "..." },
  "languages": ["hr", "en"],
  "cast": [
    {
      "id": "mia", "name": { "hr": "Mia", "en": "Mia" }, "role": "lead",
      "personality": "curious, talks fast, a bit bossy", "catchphrases": { "hr": ["..."], "en": ["..."] },
      "rig": "cast/mia/rig.json",
      "voice": {
        "hr": { "provider": "auto", "gemini": "Leda", "comfy": { "engine": "omnivoice", "instruct": "female, child, high pitch", "ref": null, "refText": null, "seed": 7 }, "vibetts": "supertonic:F3", "speed": 1.0 },
        "en": { "provider": "auto", "gemini": "Leda", "vibetts": "af_bella", "speed": 1.0, "style": "bright child-like" }
      }
    }
  ],
  "sets": [ { "id": "park", "name": { "hr": "Park", "en": "Park" }, "description": "...", "file": "sets/park/set.json" } ],
  "music": { "theme": "music/theme.ogg", "stings": ["music/sting-happy.ogg"] },
  "rules": ["lines of at most 12 words", "no name-calling", "..."],
  "episodes": [ { "id": "ep00-pilot", "title": { "hr": "...", "en": "..." }, "status": "draft" } ],
  "pitches": [ { "id": "p1", "title": { "hr": "...", "en": "..." }, "logline": { "hr": "...", "en": "..." }, "leads": [ { "name": "...", "what": "..." }, { "name": "...", "what": "..." } ], "sets": ["..."], "why": "..." } ],
  "chosenPitch": null
}
```

`pitches` holds the showrunner's 3 premises; the pipeline waits until `chosenPitch` is set by the user (studio UI or `cts_pitch_choose`), then the showrunner fills `cast`, `sets` and the rest from it. `comfy.instruct` uses OmniVoice's attribute tags only (T6 takes the accepted tag list from Edu's `tts-engines.ts` / the node); `ref` is an optional reference WAV under `cast/<id>/voice/`.

### Rig `cast/<id>/rig.json`

Each part is its own file (SVG with a px `viewBox`, or PNG). `pivot` is in the part's own pixel coords; `at` is where that pivot sits in the parent part's coords. The root part's pivot is the feet point; the actor's stage position is that point.

```json
{
  "schema": "cts.rig/1", "id": "mia", "kind": "vector", "drawnFacing": "right", "height": 600,
  "parts": [
    { "id": "body",  "src": "parts/body.svg",  "parent": null,   "pivot": [150, 420], "at": [0, 0],     "z": 10 },
    { "id": "feet",  "src": "parts/feet.svg",  "parent": "body", "pivot": [90, 10],   "at": [150, 400], "z": 8 },
    { "id": "head",  "src": "parts/head.svg",  "parent": "body", "pivot": [160, 300], "at": [150, 60],  "z": 20, "rot": [-12, 12] },
    { "id": "arm_l", "src": "parts/arm_l.svg", "parent": "body", "pivot": [20, 15],   "at": [45, 130],  "z": 5,  "rot": [-160, 40] },
    { "id": "arm_r", "src": "parts/arm_r.svg", "parent": "body", "pivot": [20, 15],   "at": [255, 130], "z": 25, "rot": [-160, 40] }
  ],
  "face": {
    "parent": "head",
    "eyes":  { "at": [160, 170], "z": 30, "states": { "open": "parts/eyes_open.svg", "half": "parts/eyes_half.svg", "closed": "parts/eyes_closed.svg" } },
    "brows": { "at": [160, 120], "z": 31, "states": { "neutral": "...", "happy": "...", "sad": "...", "surprised": "..." } },
    "mouth": { "at": [160, 245], "z": 32, "shapes": { "rest": "...", "A": "...", "E": "...", "O": "...", "U": "...", "MBP": "...", "FV": "...", "L": "..." } }
  },
  "emotions": { "neutral": { "brows": "neutral", "eyes": "open" }, "happy": { "brows": "happy", "eyes": "open" }, "sad": { "brows": "sad", "eyes": "half" }, "surprised": { "brows": "surprised", "eyes": "open" } },
  "gestures": {
    "wave":  { "part": "arm_r", "seconds": 1.0, "keys": [[0, -10], [0.25, -150], [0.5, -120], [0.75, -150], [1, -10]] },
    "point": { "part": "arm_r", "seconds": 0.8, "keys": [[0, -10], [0.3, -85], [1, -85]] },
    "shrug": { "part": "arm_l", "seconds": 0.8, "keys": [[0, -10], [0.4, -40], [1, -10]] }
  },
  "move": { "bobPx": 8, "stepSeconds": 0.33 }
}
```

Part file rules (checked by `cts_rig_check`): SVG only flat fills and strokes, stroke width = `style.outlinePx` at rig scale, no `<text>`, no filters, no `<script>`, no external `href` (data-URI images allowed only inside one `<pattern>`), at most 30 KB (200 KB with a pattern); PNG parts have alpha. All 8 mouth shapes, the 3 eye states, and the 4 emotions' brows must exist (phase 1 lip-sync uses only rest/E/A, but the set is complete so phase 2 needs no redraw). Facing the other way = horizontal flip of the whole actor.

### Set `sets/<id>/set.json`

```json
{
  "schema": "cts.set/1", "id": "park", "size": [2880, 1620], "groundY": 1380, "actorScale": 1.0,
  "layers": [
    { "id": "bg", "src": "layers/bg.png", "z": 0, "parallax": 1.0 },
    { "id": "bench", "src": "layers/bench.png", "z": 100, "at": [2200, 1420], "anchor": "bottom", "parallax": 1.1 }
  ],
  "marks": { "offL": [-300, 1380], "left": [1000, 1380], "center": [1440, 1380], "right": [1880, 1380], "offR": [3180, 1380] },
  "shots": { "wide": { "center": [1440, 810], "zoom": 1.0 }, "two": { "center": [1440, 900], "zoom": 1.25 }, "cuLeft": { "center": [1000, 760], "zoom": 1.5 }, "cuRight": { "center": [1880, 760], "zoom": 1.5 } }
}
```

`zoom` is relative to fitting the set's height into the frame (wide = whole height). Backgrounds are generated at 1920x1080 and upscaled 1.5x (ComfyUI upscale or sharp lanczos) so a 1.5 close-up stays sharp.

### Episode script `episodes/<ep>/script.json` (language-independent) and text catalog

```json
{
  "schema": "cts.episode/1", "series": "pilot", "id": "ep00-pilot", "titleKey": "title",
  "cast": ["mia", "bobo"],
  "scenes": [
    {
      "id": "s1", "set": "park",
      "start": { "mia": { "mark": "left", "facing": "right", "emotion": "happy" }, "bobo": { "mark": "offR", "facing": "left" } },
      "shot": "wide",
      "beats": [
        { "id": "b01", "type": "music", "cue": "theme", "action": "start", "gain": 0.35 },
        { "id": "b02", "type": "move", "who": "bobo", "to": "right", "seconds": 2.0 },
        { "id": "b03", "type": "line", "line": "l01", "speaker": "mia", "emotion": "happy", "gesture": "wave", "look": "bobo", "pauseAfter": 0.3 },
        { "id": "b04", "type": "camera", "shot": "cuLeft", "transition": "cut" },
        { "id": "b05", "type": "line", "line": "l02", "speaker": "bobo", "emotion": "surprised", "with": "prev" },
        { "id": "b06", "type": "emote", "who": "mia", "emotion": "sad" },
        { "id": "b07", "type": "gesture", "who": "bobo", "gesture": "shrug" },
        { "id": "b08", "type": "camera", "shot": "two", "transition": "pan", "seconds": 1.5 },
        { "id": "b09", "type": "turn", "who": "mia", "facing": "left" },
        { "id": "b10", "type": "sfx", "cue": "boing" },
        { "id": "b11", "type": "pause", "seconds": 0.8 },
        { "id": "b12", "type": "music", "cue": "theme", "action": "stop", "fade": 1.5 }
      ]
    }
  ],
  "music": { "theme": "music/theme.ogg" }, "sfx": { "boing": "music/sfx-boing.ogg" }
}
```

Beat types in phase 1: `line`, `move` (slide between marks with bob; also enter/exit via `offL`/`offR`), `turn`, `emote`, `gesture`, `look`, `camera` (`cut` | `pan`), `pause`, `sfx`, `music` (`start` | `stop`), `title` (static card, `seconds`), `clip` (`{ "type": "clip", "clip": "intro", "seconds": 8, "audio": "keep" | "mute" }`; the id is looked up in the episode's `clips/` first, then the series' `clips/`; `keep` mixes the clip's own sound at 0.3 under music and voice, `mute` drops it; no beat runs `with: "prev"` over a clip). Beats run one after another; `"with": "prev"` starts a beat together with the previous one (for a reaction during a line). A `line` beat lasts its audio length plus `pauseAfter` (default 0.25).

`text/<lang>.json`: `{ "schema": "cts.text/1", "lang": "hr", "strings": { "title": "..." }, "lines": { "l01": { "text": "...", "delivery": "cheerful" } } }`. Every `line` id in the script must exist in every language of the bible.

### Voice manifest `voice/<lang>/manifest.json`

```json
{
  "schema": "cts.voice/1", "episode": "ep00-pilot", "lang": "hr",
  "allocation": { "provider": "vibetts", "reason": "14 clips > 10 left of the Gemini quota (Croatian first)" },
  "lines": {
    "l01": { "file": "voice/hr/l01.wav", "seconds": 2.31, "provider": "vibetts", "engine": "supertonic", "voice": "F3", "speed": 1.0,
             "hash": "<clipHash of text+lang+voice+speed+style>", "words": null, "status": "ok" }
  },
  "costUsd": 0
}
```

`status`: `ok` | `placeholder` (silence of the estimated length, 2.5 words/s, so timing still builds) | `failed`. `words` is `[{ "w": "...", "t0": 0.1, "t1": 0.4 }]` when a provider or whisper gives them (phase 2), else `null`. A clip is re-made only when its `hash` changes.

### Lip-sync track `lipsync/<lang>/<lineId>.json`

`{ "schema": "cts.lipsync/1", "method": "amplitude", "fps": 12, "shapes": ["rest", "E", "A", "A", "E", "rest"] }`: one shape per animation frame from the clip start. Phase 2 adds `method: "words-hr" | "words-en"` with the same output.

### Timeline `timeline.<lang>.json` (built by code, never hand-written)

```json
{
  "schema": "cts.timeline/1", "series": "pilot", "episode": "ep00-pilot", "lang": "hr", "scriptHash": "<sha1 of script.json>",
  "size": [1920, 1080], "fps": { "anim": 12, "out": 24 }, "duration": 61.4, "seed": 29,
  "scenes": [ { "id": "s1", "set": "park", "t0": 0, "t1": 61.4 } ],
  "camera": [ { "t": 0, "center": [1440, 810], "zoom": 1.0, "ease": "cut" }, { "t": 20.5, "center": [1440, 900], "zoom": 1.25, "ease": "inOut" } ],
  "actors": {
    "mia": {
      "x": [[0, 1000, "step"]], "y": [[0, 1380, "step"]], "facing": [[0, "right"]], "visible": [[0, true]],
      "emotion": [[0, "happy"]], "eyes": [[0, "open"], [2.9, "closed"], [3.05, "open"]],
      "mouth": [[1.2, "E"], [1.283, "A"], [3.5, "rest"]],
      "rot": { "head": [[0, 0, "step"]], "arm_r": [[1.2, -10, "inOut"], [1.45, -150, "inOut"]] },
      "bob": [[0, 0]]
    }
  },
  "audio": [
    { "kind": "voice", "line": "l01", "file": "voice/hr/l01.wav", "t": 1.2, "gain": 1.0 },
    { "kind": "music", "file": "music/theme.ogg", "t": 0, "until": 61.4, "gain": 0.35, "duckTo": 0.12, "fadeOut": 1.5 },
    { "kind": "sfx", "file": "music/sfx-boing.ogg", "t": 40.2, "gain": 0.8 }
  ],
  "lines": [ { "id": "l01", "speaker": "mia", "t0": 1.2, "t1": 3.5 } ],
  "clips": [ { "id": "intro", "file": "clips/intro.mp4", "t0": 0, "t1": 8, "audio": "keep", "fallback": false } ]
}
```

Numeric tracks interpolate (`step` | `linear` | `inOut`) and are sampled on the 12 fps grid for actors; camera is sampled at 24 fps. Discrete tracks (`facing`, `eyes`, `mouth`, `emotion`, `visible`) hold until the next key. Blinks come from a seeded PRNG (every 2.5-5 s, 2 frames closed), never during a gesture key. Paths are relative to the series folder. The sampling function lives in `src/shared/sample.ts` and is used by the player, the lint and the tests.

### Player API (owned by T3, used by T5)

The page `player/index.html` exposes `window.cts = { load(timeline, baseUrl, { width, height }): Promise<void>, frameCount(): number, renderFrame(i): Promise<void>, canvas: HTMLCanvasElement }`. `renderFrame(i)` draws output frame `i` (time `i / fps.out`) and depends only on `(timeline, i)`: no `Date.now`, no `requestAnimationFrame`, no randomness, all images decoded in `load`. Inside a `clips` range `renderFrame(i)` draws a placeholder card (clip id and seconds on a flat card, plus the clip's first-frame still if `load` was given one), the same pixels every time; the final render never uses these frames for the clip range. Preview mode (`?preview=1`) adds play/pause, scrub, language switch and plays the audio with an `<audio>` per clip (preview audio sync is best effort; the MP4 is the reference).

### Role task contract (owned by T7)

Every role job is a `client` task (Edu `client.ts` lease model): `{ id, role, kind, prompt, inputs: { paths[], json }, output: { schema, path } }`. The answer submitted by `cts_submit_task` is validated against the named schema before it is written; a failing answer goes back as a retry with the zod errors. Reviews use Edu's review JSON `{ verdict: "pass" | "revise", scores, notes, problems: [{ where, what, fix }] }`.

## Files and modules

### cartoon-studio (new)

| Path | What | Task |
|---|---|---|
| `package.json`, `.yarnrc.yml`, `tsconfig*.json`, `vite.engine.config.ts`, `vite.player.config.ts`, `vitest.config.ts`, `vitest.e2e.config.ts`, `eslint.config.mjs`, `.gitignore`, `LICENSE` (MIT) | Copied from Edu with Electron, electron-vite, React 19, zustand kept; adds `playwright-core`; dev: `playwright`; `electron.vite.config.ts`, `electron-builder.config.cjs` (appId, product "Cartoon Studio", NSIS + portable x64), `scripts/verify-package.mjs`, `scripts/make-icons.mjs`, `scripts/studio-shots.mjs` | T1 (copy, rename), T10 (UI) |
| `README.md`, `AGENTS.md`, `ROADMAP.md` | What it is; rules (public repo, no keys/paths, `cts_*`, tests with `mock`, no real app in tests, Node via fnm, every interactive element has a `data-testid`); CTS-01..09 rows | T1 |
| `src/main/`, `src/preload/`, `src/shared/protocol.ts`, `src/renderer/` | Electron main and preload (bridge `window.cartoonstudio`, file protocol `cartoonstudio-file://`), engine events; the studio UI views | T1 (shell boots with an empty view), T10 (views) |
| `src/engine/{index,engine,cli}.ts` | Headless engine, `--mcp-only`, env names `CTS_*`, port 7465 | T1 |
| `src/engine/{store,queue,logs,budget,models}/` | Copied from Edu unchanged except names; `models` keeps `client`, `mock`, `openaiCompat`, `router`, `registry`, `limiter`, `keys` | T1 |
| `src/engine/mcp/{http,server,stdio,config}.ts` | Copied; `http.ts` adds static GET routes `/preview/` (player bundle) and `/files/<series>/...` (read-only, path-guarded to `series/`) | T1 |
| `src/engine/studios/{mcp-http,autostart,launch,config,vibetts,chiptune,flow}.ts`, `src/engine/comfy/{client,graphs,tts-engines,audio-save}.ts` | Copied from Edu | T1 |
| `seed/config/*.md`, `seed/agents/*.md` (8), `seed/prompts/<role>/*.md` | Roles (all `[client/claude-code, strata, lmstudio]`), settings, voice (Edu `voice.md` adapted), `budget.md` (`voice.paidMaxUsd: 0`), `render.md` (sizes, fps, encoder order, loudness) | T1 (config, agents), T7 (prompts) |
| `seed/style/cutout-kids.md` | Part drawing rules for the character-designer: shapes, outline, palette use, pivots, mouth set reference drawings; reference prompts ask for arms held away from the body; the reference is a guide to redraw, not to trace its halo | T7 |
| `src/shared/contracts.ts`, `src/shared/sample.ts`, `docs/contracts.md` | Zod schemas above; key sampling/interpolation | T2 |
| `src/engine/series/{paths,service,lint}.ts` | Create/read/write series, cast, sets, episodes; path guard; `cts_lint` checks | T2 |
| `src/player/{index.html,main.ts,assets.ts,puppet.ts,stage.ts,preview.ts,preview.css}` | Canvas player and preview | T3 |
| `src/engine/anim/{timeline,lipsync,blink,ease}.ts` | Timeline builder, amplitude lip-sync, blinks | T4 |
| `src/engine/render/{browser,render,ffmpeg,mix,sheet}.ts` | Chromium launch, frame loop, ffmpeg encode, audio mix, contact/pose sheets | T5 |
| `src/engine/voice/{allocate,quota,run,manifest}.ts`, `src/engine/voice/providers/{vibetts,gemini,comfy,paid}.ts`, `src/engine/music/chiptune.ts` | Voice generation and music | T6 |
| `src/engine/images/{provider,comfy,flow,fal,recraft,svg-split,key}.ts`, `src/engine/budget/spend.ts`, `seed/config/prices.md` | Image provider slot, SVG path-to-part split, colour key, budget gate and ledger | T9 |
| `src/engine/pipeline/{steps,run,handlers,tasks}.ts`, `src/engine/images/{reference,background}.ts`, `src/engine/mcp/tools.ts`, `docs/mcp-guide.md`, `docs/pipeline.md` | Pipeline, role tasks, image generation, all `cts_*` tools | T7 |
| `tests/` | The 8 tests listed under Tests | each task its own |

### creative-hub

| File | Change | Task |
|---|---|---|
| `services.json` | Entry `cartoon-studio`: name "Cartoon Studio (cutout cartoons)", repo, data `~\CartoonStudio`, port 7465, mcp URL, `default: false`, `managed: true`, start `node out/engine/index.js --mcp-only`, build `yarn build:engine`, docs `docs/mcp-guide.md`, `docs/contracts.md` | T8 |
| `.mcp.json` | `"cartoon-studio": { "type": "http", "url": "http://127.0.0.1:7465/mcp" }` | T8 |
| `README.md` | Table row and docs line | T8 |
| `CLAUDE.md` | Tool list in the first line; bullet: "For a cartoon episode or a cartoon series (cutout puppets, 5-10 min, hr/en), use the `make-cartoon` skill (Cartoon Studio, port 7465). Voice allocation applies." | T8 |
| `.claude/skills/make-cartoon/SKILL.md` | Skill (structure of `make-edu-game`): start services, client-task loop, pipeline steps, voice rule, budget rule, run log, how to show the user the MP4s | T8 (draft), T7 (tool names final) |
| `ROADMAP.md` | Row HUB-29 | T8 |
| `runs/cartoon-pilot.md` | Run log (ids, decisions, timings, verdicts) | P (pilot) |
| `.claude/tickets/HUB-29-cartoon-studio/changelog.md` | At the end | P |

## Tasks for workers

Order: **T1, T2, T8 in parallel** -> **T3, T4, T6, T9 in parallel** (need T2; T6 and T9 also T1) -> **T5** (T3, T4) and **T10** (starts after T1 + T2 with views on fixture `mini`; embeds T3's player when it lands; wires to T5-T7 tools as they land) -> **T7** (T1-T6, T9) -> T10 finished against T7 -> **P** (pilot, hub session) -> **V** (checker). T10 owns only `src/renderer/`, `src/main/`, `src/preload/` and `src/shared/protocol.ts`; engine features it needs that do not exist are asked of the owning task, not written by T10. Each worker: Node via `fnm exec --using default`; Yarn per memory note (fnm default alias dir on PATH); scratch in `.claude/temp/`; no real app started by tests; ends with DONE / NOT DONE / UNTESTED per item.

### T1. Repo scaffold and engine core (CTS-01)
- **Inputs:** Edu repo at `46b6ec1` (`AGENTS.md`, `src/engine/*`, `seed/config/*`, build configs).
- **Do:** `git init`, first commit (README, .gitignore, LICENSE) on `master`, branch `CTS-01_pilot`. Copy the modules in the table plus Edu's Electron shell (`src/main`, `src/preload`, `src/renderer` app frame, store and design tokens, `electron-builder.config.cjs`, `dist*` scripts); delete everything Edu-specific (`edu/`, `android/`, `live/`, `stt/`, `research/`, `puzzles/`, `themes/`, `review/` except the review JSON type, `src/live-client`, the course views in `src/renderer`). Right after the first commit (before branching): run A3's grep, then `gh repo create Tihi321/cartoon-studio --public --source . --remote origin` and `git push -u origin master` (README, .gitignore, LICENSE only); no other push in T1. Rename tools prefix, env, port, data dir, bridge (`window.cartoonstudio`), file protocol, app id and product name. The app boots to an empty "Series" view; `yarn build` and `yarn dist:dir` work. Keep MCP tools: `cts_status`, `cts_wait`, `cts_get_task`, `cts_submit_task`, `cts_client_tasks`, `cts_release_task`, `cts_pause_all`, `cts_resume_all`, `cts_stop_now`, `cts_studios_status`. Record the Edu commit and every copied file in `docs/provenance.md`.
- **Outputs:** `yarn build:engine` makes `out/engine/index.js` and `out/player/` (empty player stub until T3); `node out/engine/index.js --mcp-only` with `CTS_DATA=.claude/temp/t1` serves MCP on 7465 and lists the tools.
- **Contract:** exports `def(name, desc, schema, run)` registration for T6/T7 tools; `Engine` with `queue.register(task, handler)`; `clientProvider` task API; studio clients `vibetts`, `chiptune`, `flow`, `comfy` as in Edu.

### T2. Contracts, series store and lint (CTS-02)
- **Inputs:** this plan's Data contracts section.
- **Do:** `src/shared/contracts.ts` (zod for bible, rig, set, episode, text, voice manifest, lipsync, timeline, review); `src/shared/sample.ts` (`sampleNumber(track, t, gridFps?)`, `sampleStep(track, t)`); `src/engine/series/{paths,service}.ts` (create series from a brief stub, read/write each file atomically, resolve paths only inside `series/<slug>`); `lint.ts` with codes below; `docs/contracts.md` (the schemas as prose plus the examples above, made valid).
- **Lint codes:** `E_SCHEMA` (file fails its schema), `E_CAST_UNKNOWN`, `E_SET_UNKNOWN`, `E_MARK_UNKNOWN`, `E_SHOT_UNKNOWN`, `E_GESTURE_UNKNOWN`, `E_LINE_NO_TEXT` (per lang), `E_LINE_NO_AUDIO` (per lang, after voice), `E_RIG_PART` (missing file, bad SVG per part rules, missing mouth/eye/brow state), `E_TIMELINE_STALE` (scriptHash differs), `E_MOUTH_SILENT` (mouth not `rest` outside every line interval of that speaker), `E_LANG_ORDER` (hr and en timelines' beat sequences differ), `W_LINE_LONG` (> 12 words or > 5 s), `W_OFF_FRAME` (a speaking actor's feet point outside the camera rect while speaking), `W_LANG_DRIFT` (language durations differ > 25 %), `W_PLACEHOLDER` (voice placeholders).
- **Outputs/contract:** the schemas are the only definition; T3-T7 import, never redefine. Fixture series in `tests/fixtures/mini/` (2 tiny vector rigs from simple shapes, 1 set with a 320x180 solid PNG, 1 script with 3 lines, text hr/en, a voice manifest pointing at fixture WAVs made by a script copied from Edu's `make-fixture-audio.mjs`) used by every later test.

### T3. Puppet player and preview (CTS-03)
- **Inputs:** T2 contracts, `sample.ts`, fixture `mini`.
- **Do:** `assets.ts` loads every part (SVG as `Image` from blob URL, rasterised once per needed scale to `ImageBitmap`; PNG direct) and set layer; `puppet.ts` draws one actor: transform stack from root part (position, facing flip, bob), parts in `z` order with rotation at pivots, face plate (eyes, brows, mouth) on the head; `stage.ts` draws set layers with parallax around the camera, actors at `actorScale`, camera transform; `main.ts` the `window.cts` API; `preview.ts` controls. Bundle via `vite.player.config.ts` to `out/player/`.
- **Outputs:** `window.cts` exactly as in "Player API". Pose sheet mode `?sheet=<castId>`: draws the rig in neutral, each emotion, each gesture's peak, all 8 mouths and 3 eye states in a grid (used by T5 `sheet.ts` and the frame critic).
- **Contract:** deterministic: the same `(timeline, i)` gives the same pixels in two runs (tested in T5's e2e).

### T4. Timeline builder, lip-sync, blinks (CTS-04)
- **Inputs:** T2 contracts; a script, the text catalogs, the voice manifest, rigs and sets.
- **Do:** `timeline.ts` `buildTimeline(series, episode, lang): Timeline`: walk beats in order with a clock; `line` = manifest seconds + `pauseAfter`; `with: "prev"` shares the previous start; `move` keys x from mark to mark over `seconds` with bob amplitude on; speaker's head turns to `look` target via facing; listeners face the speaker unless told otherwise; camera keys from `shot` (`cut` = step, `pan` = inOut over `seconds`); music/sfx entries; music `duckTo` while any voice plays. `lipsync.ts` `amplitudeVisemes(wavPath, fps=12)`: decode with `ffmpeg -f f32le -ac 1 -ar 16000`, RMS per 1/12 s window, thresholds from the line's own 20th and 70th percentile of voiced windows, hysteresis, minimum hold 2 frames, `rest` for the first and last silent windows; writes `lipsync/<lang>/<line>.json`; the timeline places the shapes at `line.t0`. `blink.ts` seeded (seed in timeline).
- **Outputs:** `timeline.<lang>.json` valid against the schema; same beat order for every language (`E_LANG_ORDER` never fires for a built pair).
- **Contract:** the timeline is the only input the player and render need besides asset files.

### T5. Render and mix (CTS-05)
- **Inputs:** T3 player bundle, T4 timeline, ffmpeg/ffprobe on PATH.
- **Do:** `browser.ts` launches `playwright-core` Chromium (bundled if present, else `channel: 'msedge'`), opens the player from the engine's `/preview/` route or `file://`; `render.ts` loops `renderFrame(i)`, takes the canvas as JPEG quality 0.95 by default (`render.md: frameFormat: jpeg | png`) and writes it to ffmpeg stdin (`-f image2pipe -framerate 24`); if the actor state hash is unchanged and the camera is static, it resends the previous frame bytes without drawing. `ffmpeg.ts` probes `h264_amf` once (encode 1 s of black) and caches the result in `state/encoder.json`, else `libx264 veryfast crf 20`. **Clip splice:** with `clips` in the timeline, the final render renders the cutout segments between clips as separate video-only files, normalises each clip (`scale`/`pad` to 1920x1080, `fps=24`, `yuv420p`, `setsar=1`, same encoder settings) to a temp file, joins all segments with the concat demuxer, then mixes the audio over the whole joined video (clip audio per `keep`/`mute` as one more track at its `t0`). A missing clip file is a lint error (`E_CLIP_MISSING`) unless the clip is marked `fallback`, in which case the cutout fallback (title card plus a cutout bounce of the leads) is rendered there. `mix.ts` builds one ffmpeg filter graph: each clip `adelay` to its `t`, music with `volume` automation for ducking and fade, `amix`, `loudnorm` I=-16 LUFS, TP=-1.5; muxes into `out/<lang>.mp4` (`+faststart`). `sheet.ts` grabs N frames evenly spread (or at given times) into one PNG contact sheet with time labels, and renders the pose sheet for a rig. Writes `render/<lang>/render.log` with frame count, wall time per stage and the encoder used.
- **Outputs:** MP4 per language and quality, clips spliced in the final only (`preview` 960x540 -> `out/<lang>.preview.mp4`; `final` 1920x1080 -> `out/<lang>.mp4`); sheet PNGs.
- **Contract:** `renderEpisode({ series, episode, lang, quality }) -> { file, seconds, wallSeconds, encoder }`; `contactSheet({ ..., count | times }) -> png path`; `poseSheet({ series, cast }) -> png path`.

### T6. Voices and music (CTS-06)
- **Inputs:** T1 studio clients, T2 manifest schema, bible voices, Edu `voice/{allocate,quota,run}.ts`.
- **First:** check in the flow-music-mcp source (`src/flow/*tools*.ts`) the real name and arguments of the Gemini narration tool; `flow_narrate` (from the research) is **unverified**. Record what was found in the changelog.
- **Do:** copy `quota.ts` unchanged and `allocate.ts` with one change: `localChain` reads the per-language order from `config/voice.md` `localOrder` (default `hr: [comfy, vibetts]`, `en: [vibetts, comfy]`); note the change in `docs/provenance.md`. Adapt `run.ts` to lines: clips = script lines x languages, `clipHash` as Edu; providers: `comfy` (**OmniVoice, the hr default**: build the graph `OmniVoiceEngineNode` (language, `instruct` = the bible's attribute tags, seed) -> `UnifiedTTSTextNode` (optional `ref` clip as narrator voice) -> `SaveAudio`, POST to ComfyUI `:8188/prompt`, poll `/history/<id>`, copy the output, exactly as `creative-hub/.claude/temp/voice-test/gen.py` and Edu's `tts-engines.ts` do; one clip per line, the model kept warm by sending lines back to back; ComfyUI started via autostart), `vibetts` (`synthesize_batch`; Kokoro for en, Supertonic as hr fallback), `gemini` (flow-music-mcp narration tool as verified above, one request per clip, counted in `state/gemini-tts.json`), `paid` (interface `synthesize(text, lang, voiceRef, style) -> { file, seconds, words? }`; goes through T9's `spend.ts` gate first (`BUDGET_EXCEEDED` with no or too small `budget.json`), and in phase 1 always throws `NOT_IMPLEMENTED` after the gate). A failed clip becomes a placeholder (silence at 2.5 words/s) and a lint warning, never a failed run. Normalise each clip to 44.1 kHz mono WAV, trim leading/trailing silence over 0.15 s. `music/chiptune.ts`: `compose_track {mood, chip, seed}` + `render_audio` for the theme (30-40 s loop) and up to 2 SFX via `compose_sfx`; missing Chiptune Studio = no music and a warning.
- **Outputs:** `voice/<lang>/*.wav`, `manifest.json`; `music/*.ogg`; MCP tools `cts_voice_plan`, `cts_voice_generate`, `cts_voice_status`, `cts_voice_quota`, `cts_music_generate`.
- **Contract:** manifest per schema; `costUsd` always 0 in phase 1.

### T9. Image providers and budget gate (CTS-08)
- **Inputs:** T1 (keyring `models/keys.ts`, comfy client, flow client), T2 schemas, decision 9.
- **First:** check in the flow-music-mcp source the real name and arguments of the image tool (`flow_generate` with `max_credits` is from the research, **unverified**); if Flow images cannot be forced to 0 credits, `flow.ts` is left out and recorded as NOT DONE.
- **Do:** `budget/spend.ts`: `charge({ series, episode, provider, model, what, currency: "usd" | "credits", estimate }, run)` reads `budget.json` (absent = caps 0), refuses before the call when `spent + estimate > cap` (`BUDGET_EXCEEDED` for usd against `capUsd`, `FLOW_CREDITS_EXCEEDED` for credits against `flowCreditsCap`; `cts_budget_set` takes `flowCreditsCap` too), appends the real cost (or the estimate when the API gives none) to `spend.json` after it; one lock per episode so two parallel calls cannot both pass. `seed/config/prices.md`: per provider/model USD per image (FLUX 2 Pro, FLUX Schnell, Recraft V3 raster and vector, SD3.5), marked "check before use; last read <date>". `images/provider.ts` the interface of decision 9 and `pick(provider | "auto")`; `comfy.ts` (model from `config/providers.md` `comfy.imageModel`; Qwen edit, BiRefNet via Edu graphs), `flow.ts` (`flow_generate`, `max_credits: 0`, images only), `fal.ts` (HTTPS queue API: submit, poll, download; model ids in `prices.md`), `recraft.ts` (vendor API; `format: "svg"`, `style_id` create/reuse stored in the bible `style.recraftStyleId`). `svg-split.ts`: parse an SVG (no external deps beyond a small XML parser already in the tree, else `yaml`-free hand parser of `<path>` elements), assign paths to parts by centroid-in-polygon, write one SVG per part keeping the original `viewBox`, and slice a sheet SVG into grid cells. `key.ts`: flat-grey colour-distance key with `sharp`. Every paid call is behind `charge`. Keys read only from the keyring; a missing key gives `KEY_MISSING <provider>` with the `key-set` command to run. MCP: `cts_budget_set`, `cts_budget_get` (cap, spent, ledger), `cts_image_generate { provider, ... }`, `cts_svg_split`.
- **Outputs:** images or SVGs under the series folder; ledger entries.
- **Contract:** T6's paid voice and T7's image steps call `charge`; no other code path calls a paid API.

### T7. Pipeline, roles, image generation, MCP tools (CTS-07)
- **Inputs:** T1-T6.
- **Do:** steps in `pipeline/steps.ts` (resumable, state in `episodes/<ep>/pipeline.json`, Edu `edu_run_pipeline` pattern: re-call with the same ids resumes; `retry`, `from: <step>`):
  1. `pitch` (showrunner): brief -> 3 `pitches` in `bible.json`, each with a title, logline, two leads and 1-2 sets, in hr and en. **The pipeline then stops with state `waiting-on-user`** (`cts_status` and the studio say so); nothing visual is made until `cts_pitch_choose { series, pitch }` (or the studio's Series view) sets `chosenPitch`.
  1b. `bible` (showrunner): from the chosen pitch, `bible.json` cast without rigs, sets, tone, rules; voices are filled in step 7.
  2. `cast_ref` (character-designer writes the prompt; code calls ComfyUI with `comfy.imageModel` (`z-image-turbo`), 1024x1536 on flat `#808080`, the figure front or three-quarter with **arms held away from the body** so arms and torso can be told apart; Claude picks 1 of up to 3). The reference is only a guide for the VectorCraft redraw in path (a); its halo matters only for path (c).
  3. `rig` (character-designer): `path: "claude-svg"` (default) writes `parts/*.svg` + `rig.json` from `ref.png` and `seed/style/cutout-kids.md`; `path: "recraft-svg"` calls T9 Recraft for the figure and face sheets, then the role gives cut polygons, sheet grid and pivots and code runs `cts_svg_split`; `path: "raster"` keys `ref.png`, the role gives cut polygons and pivots, code crops PNG parts and adds the (a) face. `variant: a|b|c` writes under `cast/<id>/variants/`; `cts_rig_check` must pass; T5 pose sheet rendered; `cts_rig_compare { series, cast }` renders the comparison sheet.
  4. `set` (background-artist): prompt -> ComfyUI 1920x1080 background + foreground prop on flat grey keyed to alpha (`sharp` colour-distance key, BiRefNet `remove_background` via comfy-mcp only if the key leaves a fringe); upscale 1.5x; `set.json` marks and shots placed by reading the image.
  5. `script` (writer): `script.json` + `text/hr.json` + `text/en.json` from bible and brief, 12-16 lines for the pilot, only beat types and gestures that exist; self-check against `W_LINE_LONG`.
  6. `safety` (child-safety-reviewer, must pass, up to 2 revise rounds back to the writer): `reviews/safety.json`.
  7. `voice_cast` (voice-director): fills bible voices per language: hr OmniVoice attribute tags (and optionally a reference clip, made once and kept), hr Supertonic fallback voice, en Kokoro voice, Gemini voice names; a 1-line audition per character goes into `cast/<id>/voice/` for the user to hear in the Cast view.
  8. `voice` (code, T6). 9. `music` (composer picks mood/seed; code, T6).
  9b. `clips` (after rigs and pose sheets exist; T7 owns the step, T9 the credit gate, T5 the splice). For each `clip` beat whose file is missing (the intro once per series, at most one hero clip per episode): the showrunner writes the shot (who, action, 8 s, flat 2D cutout motion, no 3D or shading, no speech). Code writes the clips as shots into `episodes/<ep>/video/` in the input shape `scripts/video-plan.mjs plan` reads (the worker reads `buildPlan(film)` in `creative-hub/scripts/video-plan.mjs` and the `make-video` skill for the order), and the hub session runs `video-plan.mjs plan`/`next`/`record` for the estimate and each call's `max_credits`; Cartoon Studio does not copy its price table. Then: keyframe via `flow_generate` (`max_credits: 0`, `reference_images` = `ref.png` plus the pose-sheet or VectorCraft render of each lead), `flow_wait`; the video scene via `flow_generate` with `first_frame` = that keyframe, `duration: 8`, `max_credits` from `next`, behind `charge(currency: "credits")`; `flow_wait`; download to the clip path; `record` the credits. Every Flow tool name and argument is checked in `flow-music-mcp/src/flow/*tools*.ts` before use. Frame-critic: a 6-frame sheet of the clip next to the pose sheets (style, faces, colours, no 3D or shading); `revise` gives at most 1 retry, a second fail sets `fallback: true` and records the spend. MCP: `cts_clip_plan`, `cts_clip_generate { series, episode?, clip, maxCredits }`, `cts_clip_review`.
  10. `lipsync` + `timeline` (code, T4), then `cts_lint` must have 0 errors.
  11. `preview_render` per language (T5, 960x540) + contact sheet of 12 frames + pose sheets.
  12. `frame_review` (frame-critic, reads the contact sheet and the pose sheets: off-model, overlap, mouth open in silence, wrong facing, actor off-frame, missing background; up to 2 rounds; fixes are data edits by the owning role, e.g. a mark or an SVG): `reviews/frames-<lang>-<n>.json`; not must-pass, unresolved problems listed in the run summary.
  13. `final_render` per language (T5, 1920x1080) + summary (`cts_status` shows paths, durations, render times, encoder, open problems).
  - MCP tools (all in `docs/mcp-guide.md`): `cts_series_create`, `cts_pitch_choose`, `cts_series_get`, `cts_series_update`, `cts_cast_get`, `cts_rig_set`, `cts_rig_check`, `cts_set_get`, `cts_set_update`, `cts_episode_create`, `cts_episode_get`, `cts_script_set`, `cts_text_set`, `cts_timeline_build`, `cts_lint`, `cts_render`, `cts_frames` (contact sheet), `cts_pose_sheet`, `cts_run_pipeline`, plus T1's, T6's and T9's. Long calls return job ids (Edu pattern).
  - Prompts in `seed/prompts/<role>/*.md` for the 8 roles; `seed/style/cutout-kids.md`.
- **Outputs:** `cts_run_pipeline { series, episode, brief }` runs the pilot end to end with Claude answering client tasks.
- **Contract:** finalises tool names in the hub skill (edits `make-cartoon/SKILL.md` section "Tools").

### T10. Studio UI and Windows installer (CTS-09)
- **Inputs:** T1 shell, T2 contracts and fixture `mini`, T3 player bundle, engine events and MCP-equivalent IPC from T5-T7, T9; Edu's renderer patterns (zustand store with event reducers `src/renderer/store/*`, design tokens, `scripts/studio-shots.mjs`, the browser harness with a mocked bridge).
- **Do:** views, each reading the engine through the preload bridge (no file access from the renderer), every interactive element with a `data-testid`:
  1. **Series and bible**: series list; the 3 premise pitches as cards with a "Choose" button (`cts_pitch_choose`); bible fields (title, logline, tone, rules) editable.
  2. **Cast**: per character the reference image, pose sheet, rig variants (a)/(b)/(c) side by side with time and spend, `cts_rig_check` result, voice per language with the audition clip player.
  3. **Sets**: background layers with marks and shots drawn as an overlay (rectangles at each shot's camera rect, dots at marks).
  4. **Episode**: script beats in order, each `line` with its hr and en text side by side, the voice status per line and language (ok / placeholder / failed, provider, seconds) and a play button per line; lint results.
  5. **Timeline preview**: the T3 player embedded (`?preview=1` mode) with play/pause, scrub and a hr/en switch.
  6. **Render and jobs**: job queue with progress, pause/resume/stop, render buttons (preview/final per language), render times, "Open MP4" (shell open) and "Show in folder".
  7. **Client tasks**: parked client tasks with role, prompt summary and state (lease, waiting), release button.
  8. **Settings**: providers (ComfyUI, VibeTTS, Chiptune, flow-music-mcp status; image/voice provider choice), budget per episode (cap, spent, ledger; editing the cap needs a confirm dialog), keys via the keyring (set/clear, never shown back), data folder.
  - Windows build: `yarn dist:installer` (NSIS) and `yarn dist:portable` produce the exe; `scripts/verify-package.mjs` adapted (the packaged app contains `out/engine`, `out/player`, seed).
  - Copy `scripts/studio-shots.mjs` (mocked bridge, visits every view, saves screenshots) as the view check used by A15.
- **Outputs:** the app; the installer under `release/`.
- **Contract:** IPC names mirror the `cts_*` tools (`window.cartoonstudio.call(tool, args)` plus an event stream); T10 adds no engine logic.

### T8. Hub wiring (HUB-29, creative-hub)
- **Inputs:** this plan, `services.json` edu-studio entry, `make-edu-game` skill.
- **Do:** branch `HUB-29_cartoon-studio`; the files in the hub table; `hub.ps1 status` lists `cartoon-studio` (it reads `services.json`; no hub.ps1 code change expected, verify).
- **Outputs:** wiring files; skill draft with the client loop, budget rule ("no paid provider without an agreed budget recorded in the run log"), voice rule, "Scriptorium only if the user agrees", run-log template.

### P. Pilot production (hub session through the skill, after T7; not a code worker)
- P1 `hub.ps1 start cartoon-studio`; ComfyUI, VibeTTS, Chiptune Studio started via `hub.ps1` (ask nothing for these; never Scriptorium). Strata not running during ComfyUI work (shared memory, research Risks).
- P2 `cts_run_pipeline` with a short brief (ages 4-8, two leads, one set, about 60 s); Claude answers every client task. **Pause:** after the `pitch` step the pipeline stops; Claude shows the user the 3 pitches (in chat and in the app's Series view) and waits. Only after the user's pick (`cts_pitch_choose`, recorded in the run log) does the run continue. No image is generated before that.
- P0 Budget: the pilot is $0 USD (user decision 3) and 50 Flow credits (user decision 7). `budget.json` has `capUsd: 0`, `flowCreditsCap: 50`; the run log states both.
- P0b Image model: decided (user decision 8): `comfy.imageModel: z-image-turbo`, Krea 2 Turbo as alternative (`research.md` bake-off addendum). Check `config/providers.md` says so and copy the bake-off timings into the run log.
- P3 Rigs: character A with path (a), parts drawn in VectorCraft (hand-written SVG if VectorCraft is unavailable; record which). P3b: character B from one reference with (a) and (c), each time-boxed to 45 min; (b) Recraft recorded as NOT RUN (no budget). `cts_rig_compare` sheet and a 10 s preview per variant in `runs/cartoon-pilot.md` with each path's time. The pilot film uses B(a).
- P3c Flow clips (after P3, before P4): first `cts_budget_set { flowCreditsCap: 50, approvedBy: "user", note: "user decision 7, 2026-11-07" }` (USD cap stays 0). `flow_status` (signed in, credits before), the `video-plan.mjs` estimate in the run log, then step 9b for the intro (series level) and at most one hero shot; credits after, ledger and estimate in the run log.
- P4 Voices, music, timeline, preview render, frame review, final render hr and en; time each stage.
- P5 Record everything in `runs/cartoon-pilot.md` (ids, allocation, encoder, render times, review verdicts, what is UNTESTED); open both MP4s for the user; the user watches and gives go / no-go and the look choice (vector vs raster) for phase 2.
- P6 App check: build the installer (`yarn dist:installer`), install or run the portable exe, open the pilot series in the app and go through each view (screenshots in the run log). The engine started by `hub.ps1` is stopped first (one engine per data folder).

### V. Check (director-checker, fresh context)
Runs every acceptance check below and writes PASS/FAIL with evidence; fixes nothing. After a full PASS (and A3's grep once more), the hub session pushes `CTS-01_pilot` to `origin` and opens a PR to `master` with `gh pr create` (body ends with the attribution line); no auto-merge, no force-push; the user merges.

## Tests (test-discipline: only these eight)

1. `tests/contracts.test.ts`: fixture `mini` parses; one broken rig (a missing mouth shape) and one script with an unknown cast id are rejected by `cts_lint` with `E_RIG_PART` and `E_CAST_UNKNOWN`.
2. `tests/timeline.test.ts`: from `mini` with fake manifests (hr lines longer than en), line `t0`s equal cumulative durations + pauses, `with: "prev"` overlaps, both languages have the same beat order and different durations, and the mouth is `rest` outside every line interval (`E_MOUTH_SILENT` does not fire).
3. `tests/lipsync.test.ts`: golden: a generated WAV (0.5 s silence, 1 s tone with 2 loudness levels, 0.5 s silence) gives the expected shape sequence at 12 fps.
4. `tests/voice-allocate.test.ts`: Edu's allocation test copied (hr+en over quota -> hr Gemini, en local) plus the changed chain: 14 hr clips with 10 left -> hr local with chain `[comfy, vibetts]`, en `[vibetts, comfy]`.
4a. `tests/budget.test.ts`: `charge` refuses with no `budget.json`; with cap $1 and $0.95 spent it refuses a $0.08 estimate and passes a $0.04 one; two concurrent $0.04 calls at $0.94 spent let only one through; a fake paid image call writes its cost to `spend.json`; with `flowCreditsCap: 30` and 24 spent, a 12-credit estimate is refused. (`svg-split` has no unit test in phase 1: path (b) is not run.)
5. `tests/client-task.test.ts`: a role task submitted with an answer that fails its schema comes back as a retry with the errors; a valid one is written to its path.
6. `tests/render.e2e.test.ts` (Chromium): renders 2 s of `mini` at 320x180 twice; ffprobe shows h264 + aac, 24 fps, 2.0 +-0.1 s; the frame hashes of the two runs are identical (determinism); one more assert for the splice: with a 1 s fixture clip (ffmpeg `testsrc`, 640x360 30 fps) as a `clip` beat, the final file is 3.0 +-0.1 s at 24 fps and the frame at the clip's middle differs from the placeholder card.

7. `tests/ui-episode.test.ts` (the one UI test; Edu tests its renderer the same way, as zustand store reducers fed engine events, `tests/ui-store.test.ts`, `tests/ui-course.test.ts`): the episode store, fed `voice.clip` and `job.progress` events, shows each line's status per language and a pitch choice moves the series out of `waiting-on-user`. View rendering is checked by `scripts/studio-shots.mjs` (A15), not by a test.

`yarn test` runs 1-5, 4a and 7 (no Chromium, no real app, `mock` provider, fake studios); `yarn test:e2e` runs 6 and fails, not skips, without a browser.

## Acceptance criteria (phase 1)

| # | Criterion | Check that proves it |
|---|---|---|
| A1 | Repo builds and its tests pass | `yarn typecheck && yarn lint && yarn test && yarn test:e2e && yarn build` all exit 0 (output in changelog) |
| A2 | Engine serves MCP on 7465 with the `cts_*` tools | `node out/engine/index.js --mcp-only` with a scratch `CTS_DATA`; an MCP `tools/list` call returns every tool named in T1, T6, T7 |
| A3 | Repo is clean for a public push | `git grep -nE "C:\\\\Users|Infplane|sk-[A-Za-z0-9]|AIza"` on `CTS-01_pilot` returns nothing |
| A4 | Hub wiring | `pwsh -File scripts\hub.ps1 status` lists `cartoon-studio`; `start`/`stop cartoon-studio` work; `.mcp.json`, README row, CLAUDE.md line, skill and ROADMAP row exist (`git diff --stat` on `HUB-29_cartoon-studio`) |
| A5 | Pilot data is complete and consistent | `cts_lint {series, episode}` returns 0 errors; 2 rigs pass `cts_rig_check`; script has 12-16 lines; `reviews/safety.json` verdict `pass` |
| A6 | Both MP4s from one script | `out/hr.mp4` and `out/en.mp4` exist; `timeline.hr.json` and `timeline.en.json` carry the same `scriptHash`; `E_LANG_ORDER` absent |
| A7 | MP4 format and length | `ffprobe`: h264 1920x1080, 24 fps, yuv420p, aac; duration 50-75 s each; `ffmpeg -af ebur128` integrated loudness -16 +-2 LUFS |
| A8 | Render speed | `render/<lang>/render.log`: final 1080p render (frames + encode + mux) under 300 s per language; times in the run log |
| A9 | Lip-sync tracks speech | Automated: `E_MOUTH_SILENT` absent and at least 60 % of each line's frames are non-`rest` (lint stats); by eye: the user watching (A12) |
| A10 | On model | Contact sheet of 12 frames per language and both pose sheets read by Claude: in at least 4 sampled frames per language both characters are complete (no missing or detached part, correct facing toward the speaker); frame-critic review file present with `pass`, or its remaining problems listed in the run log |
| A11 | $0 pilot | Voice manifests `costUsd: 0`; `spend.json` has no `usd` entries and `budget.json capUsd` is 0; no fal/recraft request in `logs/`; hr clips' provider is `comfy` (OmniVoice) except recorded fallbacks; Gemini requests <= the quota remaining at the start (`cts_voice_quota` before/after in the run log); no Flow Music call, Flow images only at 0 credits |
| A17 | Intro clip reused and spliced | `series/<slug>/clips/intro.mp4` exists (or the beat is `fallback` and P3c NOT RUN / dropped is recorded); the episode's `clip` beat resolves to the series file, not a copy; a frame at the intro's middle in `out/hr.mp4` and in `out/en.mp4` shows the clip (read by Claude); at most one hero clip, checked the same way; the clip style is judged by the user when watching (A12) |
| A18 | Flow credits within the confirmed cap | `spend.json` credits total <= `budget.json flowCreditsCap` (50, user decision 7, in the run log); no Flow video job before the cap's `approvedAt`; ledger, `video-plan.mjs` estimate and `flow_status` credits before/after in the run log |
| A11b | Rig paths compared | `cts_rig_compare` sheet for character B with (a) and (c), each path's time in the run log, (b) listed as NOT RUN (no budget), the user's pick recorded (A12) |
| A11c | Premise picked before art | Run log shows the 3 pitches and the user's choice with a time earlier than the first image job in `jobs/done/` |
| A12 | User watched | `runs/cartoon-pilot.md` records the user's verdict on hr and en, the vector/raster look choice, and go/no-go for phase 2 |
| A13 | Preview page works | `/preview/` opened in the Browser pane plays the pilot with sound and the scrub bar moves (screenshot in the run log); else marked UNTESTED |
| A14 | The app starts | `yarn dev` (or the built exe) opens the main window with no error in the main or renderer log; the engine inside answers `cts_status` |
| A15 | Each view loads the pilot | `node scripts/studio-shots.mjs` saves a screenshot of all 8 views with no console error; in the real app on the pilot data (P6) every view shows the pilot (pitches, both rigs and variants, the set overlay, all lines with hr/en status, the player scrubbing, the render jobs, client tasks, settings with cap $0); screenshots in the run log |
| A16 | The installer builds | `yarn dist:installer` and `yarn dist:portable` exit 0, `scripts/verify-package.mjs` passes, the NSIS exe and portable exe exist under `release/`; the installed or portable app starts (P6) |

Every item ends DONE, NOT DONE (reason) or UNTESTED in `changelog.md`.

## Phase 2 (outline): episode 1 of a named series, 5-10 min

- **Series bible** for the series the user picked from the pitches (it may continue the pilot's): 3-5 recurring characters, 4-6 sets, tone and rules, voice per character per language with a stored reference clip (OmniVoice/Qwen3 VoiceDesign through ComfyUI for a fictional voice, engine/version/seed kept in the bible), theme + stings.
- **Writer at length**: 300-600 s, 60-120 shots, 150-250 lines per language, beats with more staging; optional **translator** role (9th) adapting hr/en for length and humour; Scriptorium `cartoon-episode` format as an option only (SCP ticket, needs the user's go-ahead to start Scriptorium).
- **Lip-sync step 2**: `flow_transcribe` word times (shift -0.12 s), Croatian letter-to-viseme table (`seed/style/viseme-hr.md`: Croatian is near-phonemic; m/b/p -> MBP, f/v -> FV, o -> O, u -> U, a -> A, e/i -> E, l/lj -> L) and the same table for English as a first cut; amplitude stays the fallback.
- **Animation**: walk cycle (feet swap + bob), 6-8 gestures, look/turn timing, two-shot/close-up grammar, scene transitions (cut, fade, wipe), crowd of background extras as static parts.
- **Voices at volume**: OmniVoice hr (about 2x real time warm, measured by the user's test) and Kokoro en (about 5x), with Supertonic as hr fallback; Gemini batched per scene only if flow-music-mcp can split; per-character reference clips for consistency across episodes.
- **Paid images** (Recraft path (b), FLUX backgrounds) only with a cap the user agrees for that production, after the prices in `prices.md` are checked (Recraft vector: user's source about $0.02-0.04, planner's memory about $0.04-0.08).
- **Frame critic per scene**, parallax sets with 2-3 layers, episode title card and end card.
- **ArtCraft options (hub session only, never dependencies):** EffectCraft for title and end cards, FilmCraft for final polish of the rendered MP4, SoundCraft for the final mix; our Canvas renderer stays the renderer.
- **Phase 2 acceptance**: hr and en MP4 each 300-600 s, 1080p24, loudness -16 +-2 LUFS; `cts_lint` 0 errors; final render per language under 20 min; every recurring character and set reusable by a second episode without new art (proved by building `ep02` stub timelines from the bible with no new rigs); `costUsd` 0 unless a budget was agreed; the user has watched both languages.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Paid spend runs past what the user agreed | One gate (`charge`) in front of every paid call, cap 0 by default, estimate checked before the call, ledger after; test 4a |
| Paid API key leaks into the public repo or logs | Keys only in the OS keyring, entered by the user; logs print the provider, never the key; A3 grep |
| Recraft SVG paths not grouped by part, face sheets drift from the figure | Centroid-in-polygon split plus a small Claude touch-up; same `style_id`; time box; (a) stays the default |
| fal.ai / Recraft prices or model ids change | `prices.md` is editable data with a "last read" date; the real cost from the API response is logged |
| Claude-drawn SVG looks crude or off the reference (top risk, replaces raster part extraction) | Style guide with reference shapes; pose sheet reviewed before any animation; the raster fallback on character B in the same pilot; the user picks the look |
| Raster cutting leaves gaps at joints | Overlap at joints, rotation limits, vector face plate; only a fallback |
| OmniVoice drifts between lines or characters sound alike (attribute tags only) | Fixed seed per character; optional reference clip per character; audition per character in the Cast view before the episode; Supertonic fallback |
| OmniVoice/Higgs state in ComfyUI breaks later image runs (seen in the bake-off: a stale Higgs state broke Qwen images) | Queue calls comfy-mcp `free_memory` or ComfyUI `/free` whenever the job kind switches between voice and image; voice steps run after the image steps |
| Z-Image white sticker halo | Irrelevant for path (a) (redraw); path (c) key removes the near-white rim |
| Gemini 10/day cannot carry 12-16 lines | Allocation rule sends hr local (OmniVoice) by design |
| Electron app and `hub.ps1` engine on the same data folder | One engine per data folder (lock); P6 stops the headless engine first; the app shows the lock holder |
| Installer build breaks on native modules (`sharp`, keyring) | Copy Edu's working builder config and `verify-package.mjs` unchanged where possible |
| Render slower than 5 min (JPEG transfer over CDP, Edge vs Chromium) | Unchanged-frame reuse, 12 fps poses, preview at 960x540 first; measure and record; PNG only if JPEG edges show artefacts |
| `h264_amf` unavailable or unstable | Probe once, fall back to libx264 |
| hr lines much longer than en | Separate timelines; `W_LANG_DRIFT` warns; writer keeps lines short |
| Shared APU memory (ComfyUI, TTS, Strata, Chromium) | Run steps in turns; pipeline is sequential; Strata off during image work |
| Copied engine drifts from Edu | `docs/provenance.md` lists files and commit; changes noted in the changelog |
| Public repo leak | A3 grep; data only under `~\CartoonStudio` |
| Flow clip off-style (3D look, shading, faces off-model) | Our refs and pose sheet as references, flat-cutout prompt, frame-critic against the pose sheet, 1 retry max, then the cutout fallback |
| Flow credits past the cap | Gate in `charge(credits)` plus `video-plan.mjs` `max_credits` per call; a refused quote spends nothing; ask the user before raising |
| Splice seams (fps, colour, loudness jumps) | Normalise every clip to the render's size, fps and pixel format; one audio mix with loudnorm over the joined video |
| Amplitude lip-sync reads as "flapping" | Acceptable for the pilot by decision; phase 2 word-timed visemes |

## Open questions for the user

None open. All questions were answered on 2026-11-07 (see User decisions): premise by pitch pick, GitHub public `Tihi321/cartoon-studio` (master at T1, the branch after V), hr on OmniVoice, pilot USD budget $0, Flow credit cap 50 (the intro and one hero shot cost about 12 credits each at 720p Omni 8 s, the `video-plan.mjs` seen price, so 50 covers both plus one retry each). The pilot itself asks the user for the pitch pick (P2) and for the verdict and look choice (P5).

# Pilot 2 (CTS-10..)

Status: **draft**, written 2026-11-07 after the user's verdict on pilot 1 (good, phase 2 go) and this direction from the user (verbatim): "ok not sure we need svg we can use z image, we do not need recraft, if you add image to image you can add rough sketch with poses to get image with poses, you can use nano banana if we cannot have that in z image, but try with z image, so you do not need to draw svg, otherwise we should use only google flow for videos like intro or outro or something, not for images in general. We can add another pilot for Pip and Bruno as a test. And ower down music agains voice, as in this case music was bad and it was loud. For music you can use comfy ui, this is not for midi generator."

**Reading (narrow, stated per the global Scope rule):** a second 60 s pilot of premise p1 "Pip and Bruno", hr and en, made the new way (Z-Image image-to-image puppets, ComfyUI music, music well under the voices, Flow only for intro/outro video). Not the phase 2 episode (5-10 min); phase 2 waits for the user's look at pilot 2.

## P0 probe result (2026-11-07; ComfyUI was already up, nothing was started)

- **Installed (ComfyUI 0.44.0, `/object_info`):** UNETs `z_image_turbo_bf16`, `krea2_turbo_fp8_scaled`, `qwen_image_2.1(_turbo)_int8_convrot`, `moss_image_sft_int8_convrot`, `minimax_music3_dit_fp16`; checkpoints `ace_step_v1_3.5b`, `stable_audio_3_medium`, `yue2_3b_int8_convrot`; nodes `ZImageFunControlnet`, `QwenImageDiffsynthControlnet`, `SetLatentNoiseMask`, `InpaintModelConditioning`, the ACE-Step v1 and 1.5 nodes, `ConditioningStableAudio`, `MossSoundEffectV2EngineNode`.
- **Not installed:** any ControlNet (`ControlNetLoader` list empty) and any model patch (`ModelPatchLoader` list empty). So neither the Z-Image Fun ControlNet union nor a Qwen DiffSynth ControlNet can run today. Getting one means downloading a model, which needs the user's yes and is not in this plan.
- **Plain img2img works.** Graph = the Z-Image Turbo text-to-image graph with `LoadImage -> VAEEncode` as the latent and KSampler `denoise < 1` (8 steps, res_multistep, cfg 1, AuraFlow shift 3). Input: an app-style rough sketch (flat colour blobs of a squirrel on `#808080`, right arm raised, 1024x1536). Results in `.claude/temp/zimage-i2i-probe/` (`sketch.png`, `d060.png`, `d080.png`, `compare.jpg`, `probe.py`):
  - denoise 0.6: 34.5 s (first run, includes the model load). Pose and colours kept, but it stays close to the sketch (stick arms, no hands).
  - denoise 0.8: 26.2 s warm. Pose kept (right arm up waving, left arm out, legs apart, tail behind), palette kept, and it is a real cartoon squirrel with hands, feet and an open smile. Flat fills, dark outline, clean grey background, **no white halo**.
  - So 0.75-0.85 for a character sheet from a rough sketch, and lower (0.4-0.6) to clean up a pose render of an existing rig (to be measured in P0b).
- **Not yet probed (P0b, the first pilot step):** identity across poses (two sketches of the same character, same seed and palette), masked inpaint of the mouth/eye region (face states), ACE-Step instrumental quality and time.

## Decisions for pilot 2

1. **Puppets come from Z-Image image-to-image, not SVG.** The app makes a rough sketch, Z-Image draws the character over it, and the result is cut into puppet parts (raster rig). Face states (mouths, eyes, brows) are PNG patches made by masked inpaint of the same master. There is no vector face plate, so no "double face" (the pilot 1 discovery: the raster rig kept the painted face under the vector plates).
2. **Path (a) Claude-drawn SVG stays as an optional path, not the default, and is not run in pilot 2.** Why keep it: it is built and tested, pilot 1's two characters (`lana`, `fido`) are SVG rigs that must keep rendering, and it is a $0 fallback if Z-Image cannot hold a character. Why not the default: the user does not want to depend on drawing SVG. The raster path stops needing variant (a)'s face.
3. **Path (b) Recraft is removed** (code, the tool `cts_svg_split`, prices, docs, the UI column). No data uses it (pilot 1 recorded it as NOT RUN).
4. **No image goes to Google Flow.** The `flow` image provider is removed. The clip keyframe (pilot 1 made it with a free `flow_generate` image) becomes a still rendered by our own player from the clip's staging, optionally cleaned by Z-Image img2img at denoise <= 0.4. Flow gets only video calls, and only for the clips `intro` and `outro` (both series level, reused by every episode). The episode `hero` clip is dropped.
5. **Nano Banana only as a paid fallback.** A `gemini` image provider (Gemini API image model, key in the keyring, every call behind `charge`) is written but runs only after the user says yes and a USD cap is recorded with `cts_budget_set`. The pilot 2 cap is $0, so it is refused unless the user agrees to spend. Fallback order when Z-Image cannot hold a character or pose: (1) Z-Image at a lower denoise from a rig render, (2) Qwen-Image 2.1 edit (local, $0, already in the client) with the character sheet as reference, (3) Nano Banana after a user yes.
6. **Music from ComfyUI, not Chiptune Studio.** Default engine `ace-step-v1-instrumental` (ACE-Step v1 3.5B, installed; the graph builder is already in `comfy/graphs.ts`), with `minimax-music-3` as the configured alternative. Stable Audio 3 medium is installed but has no graph builder; it is listed as an option, not wired. Sound effects: MOSS-SoundEffect v2 through ComfyUI (already an engine in `tts-engines.ts`), or none. Cartoon Studio no longer calls Chiptune Studio.
7. **Music sits well under the voice, by measurement.** Every voice clip is normalised to -20 LUFS and the music file is measured once. The music bed is placed **18 dB under the voice level while someone speaks** (hard floor 15 dB) and **8 dB under in the gaps**. A mix check measures this on the rendered stems and writes the result next to the render.
8. **Series `pip-bruno`** (new, not the pilot 1 series `pilot`), episode `ep00-pilot`. Pitch p1 is already the user's pick (pilot 1 run log, 2026-11-07 20:59: the user liked p1; this direction: "another pilot for Pip and Bruno"), so the pitch pause is skipped and the bible starts from p1.

## Scope (pilot 2)

1. Remove Recraft (path b) and the Flow image provider. Clip keyframes come from our player. Flow video only for `intro`/`outro`.
2. Z-Image img2img and masked inpaint in the ComfyUI client and the image provider. The `gemini` (Nano Banana) paid fallback behind the gate.
3. Rough sketches made by the app: a character sketch from a body plan, and pose sketches from the rig.
4. A character sheet step (sketch -> Z-Image -> master plus 3 poses) with a pause for the user's look.
5. A raster rig from the master with image face patches (no SVG, no variant a needed). Optional pose images for gesture peaks.
6. Music from ComfyUI (ACE-Step instrumental theme, optional MOSS sound effects).
7. The mix: stem loudness normalisation, bed levels, ducking and the mix check.
8. Pipeline, UI, docs and hub skill updated. The pilot 2 run (hr + en, about 60 s), which the user watches.

## Out of scope (explicit)

- Phase 2 (a 5-10 min episode, more characters and sets, word-timed visemes, walk cycles).
- Downloading any model (a Z-Image ControlNet union or model patch, a new ACE-Step 1.5 checkpoint) and writing a Stable Audio 3 graph builder. Recorded as options for the user.
- Any paid call without the user's yes and a recorded cap: Nano Banana, fal, paid voice. The pilot USD cap is $0.
- Flow images of any kind. Flow video other than `intro` and `outro`. More than 50 Flow credits. Flow Music.
- Removing path (a) or changing pilot 1's series data (it must still lint and render).
- Chiptune Studio as a music source; MIDI generation; Scriptorium (never started without asking).
- Changing another tool's repo (comfy-mcp, flow-music-mcp, Chiptune Studio, Edu). Gaps go in that tool's `ROADMAP.md`.
- New UI views beyond the fields named in CTS-17; Android; code signing.
- Pushing anything before the checker passes; force-push; auto-merge.

## Branches

- cartoon-studio: a new branch **`CTS-10_pilot-2`** cut from `CTS-01_pilot` (its tip, 77743e1 when this plan was written; checked at the start), one commit per ticket CTS-10..CTS-17. It is pushed after V passes and A3's grep, then a PR (base `CTS-01_pilot` if that PR is still open, else `master`), no auto-merge.
- creative-hub: the hub files (skill, run log, plan) on `HUB-29_cartoon-studio` (the current branch).

## Files and modules to touch

| Repo / path | Change | Task |
|---|---|---|
| `src/engine/images/recraft.ts`, `src/engine/images/svg-split.ts`, `src/engine/images/flow.ts` | delete | CTS-10 |
| `src/engine/images/provider.ts`, `src/engine/images/tools.ts` | `IMAGE_PROVIDERS = ['comfy', 'gemini', 'fal']`; `cts_svg_split` removed; `cts_image_generate` gains `init`, `denoise`, `mask` | CTS-10, CTS-11 |
| `src/engine/pipeline/rig.ts`, `media.ts`, `steps.ts`, `tasks.ts` | drop `recraft-svg` and variant b; the raster rig no longer needs variant a; new `cast_sheet` step and pause | CTS-10, CTS-12, CTS-13 |
| `src/engine/pipeline/clips.ts`, `src/engine/pipeline/handlers.ts` (writer prompt) | keyframe = player still; clip ids `intro`/`outro` only (series level); no `hero` | CTS-10 |
| `src/engine/studios/flow.ts` | `generateImage` removed; `generateVideo` kept | CTS-10 |
| `src/shared/contracts.ts`, `docs/contracts.md` | `RIG_VARIANTS = ['a', 'c']`; face states may be PNG; rig `poses` (optional) and gesture `pose`; bible `cast[].sheet`; clip ids; the timeline music fields unchanged | CTS-10, CTS-12, CTS-13, CTS-14 |
| `src/engine/comfy/graphs.ts`, `client.ts`, `kind-switch.ts` | `buildZImageImg2Img`, `buildZImageInpaint`; `ComfyRequest.init { image, denoise, mask? }`; job kind `music` | CTS-11, CTS-15 |
| `src/engine/images/gemini.ts` (new), `seed/config/prices.md` | the Nano Banana provider behind `charge`; price row marked "check before use"; Recraft rows removed | CTS-10, CTS-11 |
| `src/engine/images/sketch.ts` (new) | body plan JSON -> sketch PNG (sharp); pose sketch from a body plan or a rig render | CTS-12 |
| `src/engine/images/face.ts` (new), `src/engine/series/lint.ts`, `src/player/assets.ts`, `src/player/puppet.ts` | face patches by inpaint; PNG plates checked (alpha, size); the player draws PNG plates and pose images | CTS-13, CTS-14 |
| `src/engine/music/comfy.ts` (new), `src/engine/music/chiptune.ts` (delete), `seed/config/providers.md`, studios/autostart config | `comfy.musicModel: ace-step-v1-instrumental`; Chiptune removed from Cartoon Studio's pipeline, studios status and autostart | CTS-15 |
| `src/engine/render/mix.ts`, `src/engine/render/mixcheck.ts` (new), `src/engine/anim/timeline.ts`, `seed/config/render.md` | per-stem normalisation, bed and duck in dB from `render.md`, the mix check | CTS-16 |
| `src/renderer/` (Cast and Settings views), `docs/mcp-guide.md`, `docs/pipeline.md`, `README.md`, `ROADMAP.md`, `seed/prompts/*`, `seed/style/cutout-kids.md` | sketch/sheet/poses in the Cast view, the music engine and image fallback in Settings, docs, roadmap rows CTS-10..17 | CTS-17 |
| creative-hub `.claude/skills/make-cartoon/SKILL.md`, `runs/pip-bruno-pilot.md`, `ROADMAP.md` (HUB-29 row note), this ticket's `changelog.md` | skill steps (sheet pause, no Flow images, music from ComfyUI, mix-check numbers), run log | CTS-17 (hub side), P |
| `tests/` | only the tests listed below | each task |

## Tasks (one commit each on `CTS-10_pilot-2`)

Order: CTS-10 -> CTS-11 -> CTS-12 -> CTS-13 -> CTS-14. CTS-15 and CTS-16 run in parallel with CTS-11..14 (disjoint files). CTS-17 last, then P (pilot 2, hub session) and V (checker). Workers: Node via `fnm exec --using default`, Yarn per the memory note, scratch in `.claude/temp/`, tests with fakes (no live ComfyUI or Flow in `yarn test`), DONE / NOT DONE / UNTESTED per item.

### CTS-10. Remove Recraft and Flow images; Flow video for intro/outro only
- **Inputs:** `images/{provider,tools,recraft,svg-split,flow}.ts`, `pipeline/{rig,media,clips,handlers,steps,tasks}.ts`, `studios/flow.ts`, `contracts.ts`, `seed/config/prices.md`, the Cast view, `docs/*`.
- **Do:** delete the Recraft provider, `buildRecraftRig`, the `rig-recraft` task, `svg-split.ts` and `cts_svg_split`. Set `RIG_PATHS = ['claude-svg', 'raster']` and `RIG_VARIANTS = ['a', 'c']`. Delete `images/flow.ts`; `pick()` knows `comfy`, `gemini` (a stub that refuses until CTS-11) and `fal`. In `clips.ts` the keyframe is a still: the player renders the clip's staging (set, the leads at their marks, emotion, gesture peak; the showrunner's clip answer gains `staging`) through `render/sheet.ts` at 1280x720, saved as `clips/keyframes/<id>.png`. An optional `polish: true` runs Z-Image img2img (CTS-11) at denoise 0.35 on it. The video call is unchanged (`first_frame` = that still, `max_credits` from `video-plan.mjs`, behind `charge(credits)`). Allowed clip ids: `intro` and `outro`, both series level (`series/<slug>/clips/`). The writer prompt asks for an intro at the start and an outro at the end, no hero; `heroCount` is replaced by a check that refuses any other clip id. `studios/flow.ts` keeps `generateVideo` and loses `generateImage`.
- **Outputs/contract:** no code path can make an image through Flow (`git grep generateImage -- src` returns nothing); `cts_clip_generate { series, clip: "intro" | "outro", maxCredits }`.

### CTS-11. Z-Image img2img and inpaint; the Nano Banana fallback
- **Inputs:** the P0 probe graph (`creative-hub/.claude/temp/zimage-i2i-probe/probe.py`), `comfy/{graphs,client}.ts`, `images/{provider,comfy}.ts`, `budget/spend.ts`.
- **Do:** `buildZImageImg2Img(o)` = `buildZImage` with node 7 replaced by `LoadImage(init) -> VAEEncode` and `denoise` from the request. `buildZImageInpaint(o)` adds `LoadImageMask` (or the init PNG's alpha) -> `SetLatentNoiseMask` before the sampler, so only the masked region is redrawn. `ComfyRequest.init?: { image: string | Buffer, denoise: number, mask?: string | Buffer }` uploads the files the way references are uploaded. `ImageRequest.init` passes through `comfyProvider`. `images/gemini.ts`: Nano Banana through the Gemini API (`generateContent` with image output; the model id and price are read from `prices.md`, and the worker checks the current model id and price in Google's docs and records the date). The key comes from the keyring account `GEMINI_API_KEY` (set with `key-set gemini`), refs go as inline images, and every call goes through `charge({ currency: "usd", estimate })`; without a key it fails with `KEY_MISSING gemini`. ControlNet is not wired (no model installed); `docs/pipeline.md` notes `ZImageFunControlnet` plus a union model patch as the upgrade path.
- **Outputs/contract:** `cts_image_generate { provider: "comfy", init, denoise, mask? }` returns `{ file, costUsd: 0, provider, model: "z-image-turbo" }`; `provider: "gemini"` is refused with `BUDGET_EXCEEDED` at cap $0 before any network call.

### CTS-12. Sketches and the character sheet step (pause for the user)
- **Inputs:** CTS-11; `pipeline/{steps,media,tasks}.ts`; `images/reference.ts`; the bible.
- **Do:** `images/sketch.ts`: a **body plan** (character-designer answer, schema `body-plan`: canvas 1024x1536, background `#808080`, a list of primitives `ellipse | circle | capsule | polygon`, each with a colour from the bible palette, plus a `limb` id and a joint point per limb) rendered to PNG with `sharp`. `poseSketch(bodyPlan, pose)` rotates each limb's primitives about its joint (pose = degrees per limb) and renders it. The body plan is a throwaway sketch, not a rig part; no SVG is drawn by hand. A new step `cast_sheet` replaces `cast_ref`: for each character the designer gives the body plan and a prompt; the app renders the front sketch (arms away from the body) and runs Z-Image img2img at denoise 0.8 with seeds `seed..seed+2`; the designer picks one -> `cast/<id>/ref.png` (the master). Then 3 pose sketches (the wave, point and shrug peaks) at the same seed -> `cast/<id>/sheet/<pose>.png`, and one sheet image `cast/<id>/sheet.png` (the master and the poses side by side). **The pipeline then stops in `waiting-on-user` (`sheet_review`)** until `cts_sheet_approve { series, cast, ok, note? }` has been given for every character. A "redo" note reruns that character's sheet with the note added to the prompt. The bible's cast entry gains `sheet: { approvedAt, seed, denoise, model }`.
- **Outputs/contract:** `ref.png` at 1024x1536 on flat grey; `sheet.png`; the time per image in the step log.

### CTS-13. Raster rig from the master with image face patches
- **Inputs:** CTS-11, CTS-12; `pipeline/rig.ts` `buildRasterRig`, `images/key.ts`, lint, player.
- **Do:** `buildRasterRig` no longer needs variant a. It keys `ref.png` and cuts the parts by the designer's polygons with joint overlap (unchanged), and builds the face from patches. `images/face.ts`: the designer gives the mouth, eye and brow boxes in `ref.png` pixels. For each state the app runs a masked inpaint of the master (CTS-11; mask = the box with a soft edge; denoise 0.7-0.9; a prompt such as "same character, mouth wide open"). The patch is that box cropped from the result with a feathered alpha edge, so it covers the painted mouth or eyes. The **rest** patch is cut from the master itself. Mouths made: `rest, A, E, O, MBP`; `U` -> `O`, `FV` -> `E` and `L` -> `E` point at the same files (the contract allows this; all 8 keys are present). Eyes `open, half, closed`; brows `neutral, happy, sad, surprised` (one brow patch spans both brows). The plates are PNG with `at` = the box centre in head-part pixels. Lint `E_RIG_PART` accepts PNG plates (alpha present, at most 512 KB each). The player draws PNG plates like parts.
- **Outputs/contract:** `cast/<id>/variants/c/{parts/*.png, face/*.png, rig.json}` with `kind: "raster"`, passing `cts_rig_check`; the pose sheet rendered.

### CTS-14. Pose images (optional per gesture)
- **Inputs:** the CTS-13 rig, the player's sheet mode, CTS-11 img2img.
- **Do:** contract: rig `poses?: { <name>: { src, pivot, face?: { at, scale } } }` (a full-body PNG; pivot = the feet point) and gesture `pose?: <name>`. The pose image replaces the parts for the middle 60 % of the gesture, with the face plates drawn at `face.at` if given; otherwise the painted face shows and there is no lip-sync during it, and the timeline never puts such a pose over a line. Making a pose: the player renders the rig at the gesture peak (`?sheet=<cast>&pose=<gesture>`), then Z-Image img2img at denoise 0.45-0.6 cleans up the joints and hands -> `cast/<id>/poses/<gesture>.png`, keyed to alpha. The frame-critic compares it with `sheet.png` (identity: colours, markings, proportions). `revise` gives one retry at a lower denoise; after that the gesture stays a part rotation.
- **Outputs/contract:** zero or more poses per rig; a rig without poses works as before.

### CTS-15. Music from ComfyUI
- **Inputs:** `comfy/graphs.ts` (`buildAceStep`, `buildMiniMaxMusic`, `ENGINES`), `comfy/client.ts`, `kind-switch.ts`, `pipeline/handlers.ts` `musicStep`, `musicAnswer`.
- **Do:** `music/comfy.ts` `generateTheme({ series, tags, bpm, key, seed, seconds })`: the engine comes from `config/providers.md` `comfy.musicModel` (`ace-step-v1-instrumental` by default, `minimax-music-3` as the alternative); 40 s, instrumental (empty lyrics), converted to `music/theme.ogg` with ffmpeg (fade-in 0.5 s, fade-out 2 s, so a loop or an ending is clean). Sound effects: up to 2 through the `moss-soundeffect-v2` engine (`music/sfx-<cue>.ogg`), or none. `musicAnswer` becomes `{ tags, bpm, key, seed, seconds?, sfx?: [{ name, prompt, seconds }] }`. The composer prompt asks for soft, sparse, light instrumentation (ukulele, glockenspiel, soft pizzicato, light percussion), no vocals, no heavy drums: "background music for a children's cartoon under dialogue". `ComfyJobKind` gains `music`, so ComfyUI memory is freed between image, voice and music jobs. Delete `music/chiptune.ts` and its use in the pipeline; Cartoon Studio's autostart and studios status drop Chiptune.
- **Outputs/contract:** `cts_music_generate { series, tags, bpm?, seed?, seconds? }` -> `{ file, seconds, engine, wallSeconds }`; the step log records the engine and the time.

### CTS-16. The mix: music well under the voice
- **Inputs:** `render/mix.ts`, `anim/timeline.ts` (`DEFAULT_MUSIC_GAIN`, `DUCK_SHARE`), `seed/config/render.md`.
- **Do:** `render.md` gains `mix: { voiceLufs: -20, musicUnderVoiceDb: 18, musicGapUnderVoiceDb: 8, sfxUnderVoiceDb: 6, clipUnderVoiceDb: 10, minUnderVoiceDb: 15 }`. Before the mix, each input file's integrated loudness is measured once (ffmpeg `ebur128`, cached by file hash in `render/<lang>/levels.json`) and a normalising gain is applied: voices to `voiceLufs`; music to `voiceLufs - musicGapUnderVoiceDb` in the gaps and `voiceLufs - musicUnderVoiceDb` while a voice plays (the existing duck trapezoid, attack 0.15 s, release 0.35 s, now in dB); sfx and clip audio likewise. The script's music `gain` is a trim of at most 0 dB on top, never a boost. Then `loudnorm` to -16 LUFS as before (one gain on the sum, so the ratios stay). `render/mixcheck.ts` renders two stems with the same graph (voice only, music only) to WAV, runs `ebur128` short-term loudness (3 s windows, 0.1 s steps), and for every line interval longer than 0.8 s takes the energy mean of both stems. It writes `render/<lang>/mix-check.json { lines: [{ id, voice, music, underDb }], minUnderDb, medianUnderDb, gapMusicUnderVoiceDb }`. `cts_render` returns `minUnderDb`; lint gives `W_MIX_MUSIC_LOUD` when `minUnderDb < minUnderVoiceDb`.
- **Outputs/contract:** every final render has a `mix-check.json`; the timeline schema is unchanged.

### CTS-17. Pipeline, UI, docs and the hub skill
- **Inputs:** CTS-10..16.
- **Do:** the step order: `bible` (from a given pitch: `cts_run_pipeline { brief: { pitch: {...} } }` writes `pitches: [p1]` and `chosenPitch: "p1"` and skips the pitch pause) -> `cast_sheet` (pause) -> `rig` (raster from the master by default; `claude-svg` only when asked) -> `poses` (optional) -> `set` (Z-Image text-to-image, unchanged) -> `script` -> `safety` -> `voice_cast` -> `voice` -> `music` (ComfyUI) -> `clips` (intro/outro) -> `lipsync`/`timeline` -> preview -> `frame_review` -> final + mix check. Cast view: sketch, master, sheet poses, rig variants a/c, approve and redo buttons (with `data-testid`s). Settings: the music engine, the image fallback order with the gemini cap. Docs (`mcp-guide.md`, `pipeline.md`, `contracts.md`), `README.md`, `ROADMAP.md` rows CTS-10..17 (and the stale CTS-02..04 and CTS-09 rows set to Done), the prompts and `seed/style/cutout-kids.md` (sketch and body-plan rules instead of SVG drawing rules; the SVG rules kept under "path a, optional"). Hub: the `make-cartoon` skill (sheet pause, no Flow images, Flow only for intro/outro, music from ComfyUI, mix-check numbers, Nano Banana only after a yes and a cap) and a `runs/pip-bruno-pilot.md` template.
- **Outputs/contract:** `cts_run_pipeline` runs pilot 2 end to end with its two pauses (the sheets, then the user watching).

## Pilot 2 steps (hub session through the skill, after CTS-17)

- **P0 budget:** `capUsd: 0` and `flowCreditsCap: 50` recorded with `cts_budget_set` (approvedBy user, note "pilot 2, intro/outro only") before any Flow call. Nano Banana is not used unless the user says yes to an amount; then the cap is raised to that amount and recorded.
- **P0b probes (about 10 min, first thing in the run):** (1) identity across poses: the same body plan in two poses at denoise 0.8 and the same seed, then compare colours, markings and proportions; (2) one mouth inpaint on the master (rest -> A) and its patch over the head; (3) one 40 s ACE-Step instrumental, its wall time and its loudness stats (the user judges the sound in P6). Results go in the run log. If (1) or (2) fails, try the fallback order of decision 5 (a lower denoise from a rig render, then Qwen edit), and ask the user before using Nano Banana.
- **P1** `hub.ps1 start cartoon-studio`, ComfyUI, VibeTTS and flow-music-mcp (not Chiptune Studio, not Scriptorium; Strata off during image work).
- **P2** `cts_run_pipeline { series: "pip-bruno", episode: "ep00-pilot", brief: { pitch: p1 (copied from the `pilot` series bible), ages 4-8, 60 s, 12-16 lines, intro + outro } }`.
- **P3 sheets, then PAUSE:** body plans, sketches, masters and pose sheets for Pip (a fast squirrel) and Bruno (a slow hedgehog). Show the user both `sheet.png` (in chat and in the Cast view) and wait for approve or redo per character. Nothing is rigged before both are approved (time order in the run log).
- **P4 rigs:** raster rigs with face patches; pose sheets read by Claude (no double face, the mouths read, the joints are closed); poses for at most 2 gestures per character; the time per character.
- **P5 sets, script, safety, voices, music, clips:** voice allocation by the hub rule (Gemini free 10/day, Croatian first; with 12-16 lines hr goes local to OmniVoice and en to Kokoro; `cts_voice_quota` before and after); music from ComfyUI; Flow `intro` and `outro` (keyframes are player stills; `video-plan.mjs` estimate 2 x 12 = 24 credits, cap 50).
- **P6 renders and the mix check:** preview, frame review, then the final hr and en renders; `mix-check.json` per language in the run log. **PAUSE: the user watches both MP4s** and gives a verdict on the look (Z-Image puppets), on the music and its level, and go/no-go for phase 2 with this method.
- **P7 records:** `runs/pip-bruno-pilot.md` (ids, timings, decisions, verdicts, UNTESTED items), the changelog, evidence under the ticket's `evidence/`.

## Tests (test-discipline: only these; existing tests updated where removed code was tested)

1. `tests/clips.test.ts` (new): with a fake Flow client whose `generateImage` throws and a fake renderer, `cts_clip_generate { clip: "intro" }` makes its keyframe from the player still and sends exactly one video call; `clip: "hero"` is refused. Proves that no image step reaches Flow.
2. `tests/budget.test.ts` (one case added): a `gemini` image request at cap $0 is refused with `BUDGET_EXCEEDED` and the fake `fetch` is never called.
3. `tests/rig-raster.test.ts` (new): from a fixture master PNG, polygons and fixture face patches, `buildRasterRig` with **no variant a** writes a rig that passes `cts_rig_check`, all 8 mouth keys resolve to PNG files, and the rest patch covers the designer's mouth box.
4. `tests/mix.test.ts` (new, ffmpeg): a loud music fixture (a square wave at about -8 LUFS) and two quiet voice fixtures (about -32 LUFS) mixed by `muxEpisode` give a `mix-check.json` with `minUnderDb >= 15` and `gapMusicUnderVoiceDb` within 8 +-2.
5. Updated, not new: `tests/render.e2e.test.ts` (the splice case uses a clip with id `intro`); `tests/contracts.test.ts` (variant `b` and `recraft-svg` are rejected; fixture `mini` with its SVG rigs still parses).

## Acceptance criteria (pilot 2)

| # | Criterion | Check that proves it |
|---|---|---|
| B1 | Builds and tests pass | `yarn typecheck && yarn lint && yarn test && yarn test:e2e && yarn build` exit 0 on `CTS-10_pilot-2` |
| B2 | Recraft is gone | `git grep -niE "recraft\|svg-split\|svg_split" -- src seed docs` (pipes escaped for the table) returns nothing; MCP `tools/list` has no `cts_svg_split` |
| B3 | No image goes to Flow | `git grep -n generateImage -- src` returns nothing; `IMAGE_PROVIDERS` has no `flow`; test 1; the flow-music-mcp calls in the pilot 2 logs are video scenes for `intro`/`outro` only |
| B4 | Z-Image img2img is live | this plan's P0 probe plus the P0b results in the run log; sheet images from sketches at <= 40 s warm per image; `ref.png` made by `z-image-turbo` per the step log |
| B5 | The user saw the sheets before rigging | run log: `cts_sheet_approve` for Pip and Bruno earlier than the first `rig` job in `jobs/done/` |
| B6 | Rigs without SVG | both rigs `kind: "raster"`, every part and face state a PNG, no `variants/a` for Pip or Bruno, `cts_rig_check` passes (test 3 covers the code path) |
| B7 | No double face, the mouths read | pose sheets read by Claude: one face per character, A/E/O/MBP distinct, the rest patch hides the painted mouth; frame-critic `pass` or its problems listed |
| B8 | The character holds across poses | sheet poses and any pose images compared with `ref.png` by Claude (colours, markings, proportions); any fallback used, and the user's yes for Nano Banana if it was used, recorded |
| B9 | $0 unless agreed | `spend.json` has no `usd` entries (or only up to a cap the user agreed, with the yes quoted); otherwise no gemini or fal request in `logs/`; voice manifests `costUsd: 0`; test 2 |
| B10 | Music from ComfyUI | step log: theme engine `ace-step-v1-instrumental` (or the configured alternative), wall time recorded; no Chiptune Studio call in the logs; `git grep -n chiptune -- src/engine/pipeline src/engine/music` returns nothing |
| B11 | Music under the voice | `render/<lang>/mix-check.json` for hr and en: `minUnderDb >= 15` and `medianUnderDb >= 17`; test 4; integrated loudness -16 +-2 LUFS (`ebur128`) |
| B12 | Flow only for intro/outro, within the cap | `series/pip-bruno/clips/{intro,outro}.mp4` exist (or `fallback` recorded); Flow credits in `spend.json` <= 50; no episode-level clip; frames at both clip middles show the clip (read by Claude) |
| B13 | Both films | `out/hr.mp4` and `out/en.mp4`: h264 1920x1080 24 fps yuv420p + aac, 50-75 s; the same `scriptHash`; `cts_lint` 0 errors |
| B14 | Pilot 1 unharmed | `cts_lint { series: "pilot", episode: "ep00-pilot" }` gives 0 errors and a 2 s preview render of it succeeds |
| B15 | The app shows pilot 2 | `scripts/studio-shots.mjs` runs with no console error; the Cast view shows the sketch, master, sheet poses and approve state for Pip and Bruno (screenshot in the run log) |
| B16 | Public repo clean | A3's grep on `CTS-10_pilot-2` returns nothing |
| B17 | The user watched | the run log records the user's verdict on hr and en, the look, the music level, and go/no-go for phase 2 with this method |

Every item ends DONE, NOT DONE (reason) or UNTESTED in `changelog.md`.

## Risks (pilot 2)

| Risk | Mitigation |
|---|---|
| Z-Image does not keep the same character across poses (only the prompt and palette tie them; no ControlNet, no reference input) | Poses come from a render of the approved rig (the character's own pixels) at a low denoise, not from new sketches; the user approves the sheets; fallback order: lower denoise, Qwen edit with the sheet as reference ($0), Nano Banana only after a yes |
| Inpainted mouth and eye patches do not match the head (colour, line weight, position) | Each patch is a crop of the same master region with a feathered edge; rest is cut from the master; P0b tests one patch before the run; frame-critic on the pose sheet |
| Raster parts show gaps at the joints when rotated | Overlap at the joints and rotation limits (phase 1); pose images for the big gestures |
| A halo or grey fringe around keyed parts | The probe showed no halo at denoise 0.8; the key still removes a near-white rim; BiRefNet as a fallback |
| ACE-Step adds vocals or sounds busy | Instrumental graph (empty lyrics), tags for sparse light instruments, up to 3 seeds if the first is bad; MiniMax Music 3 as the alternative; the user judges it in P6 |
| The music is still too loud, or now too quiet | A numeric target (18 dB under, floor 15) measured per line on the stems; `W_MIX_MUSIC_LOUD`; the levels are config, not code |
| ComfyUI memory with Z-Image, OmniVoice and ACE-Step in one process | `music` job kind in the kind switch (models freed between kinds); steps run in turns |
| A ControlNet would hold poses better than plain img2img | Recorded upgrade path (Z-Image Fun ControlNet union model patch); needs a model download and the user's yes |
| The Nano Banana price or model id changes | Price row "check before use" with its date; refused at cap $0; the user agrees an amount first |
| Removing Recraft and Flow images breaks pilot 1 | Pilot 1 used neither (b NOT RUN; its keyframes exist as files); B14 regression check |
| The pitch pause is skipped by mistake for other series | The skip happens only when the brief carries an explicit `pitch`; otherwise the phase 1 pause stays |

## Open questions for the user (pilot 2)

1. Nano Banana: the free route is Google Flow's image model at 0 credits, which the direction rules out ("only google flow for videos"). Is the paid Gemini API route right for the fallback, and what USD cap may it use if Z-Image fails (for example $1, about 25 images at an unverified ~$0.04 each)?
2. Keep path (a) SVG as an optional fallback (planned), or delete it too?
3. Outro: one series outro clip besides the intro (planned, 2 x 12 credits), or the intro only?
4. If plain img2img cannot hold poses, may a Z-Image ControlNet model patch be downloaded later (a few GB)?
