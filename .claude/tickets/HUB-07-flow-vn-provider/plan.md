# HUB-07: Google Flow as a VN Studio provider (images, voices, music)

Plan only. Written 2026-10-22 from reading the code and docs of VN Studio (`C:\projects\Personal\visual-novels-orchestrator`,
master 7ff8a2d), flow-music-mcp (`C:\projects\Personal\flow-music-mcp`, master 8e7d01e plus its FMM-04..10 plans) and the hub.
Nothing was run, no service was started, no credits were spent.

## Goal

VN Studio makes a project's art, voices and music through Google Flow by itself, as providers next to ComfyUI, Pixel Studio,
Chiptune Studio and VibeTTS. Today Flow files come in by hand with `vno_asset_replace` / `vno_asset_import` / `vno_voice_import`.

- `art.provider: flow`: backgrounds, character sheets, sprites, CGs (full and insert) and the cover from Flow's free Nano Banana images.
- `voice.provider: flow`: clips from `flow_narrate` with the free engines `gemini` and `windows`.
- `music.provider: flow`: tracks from Flow Music (`music_generate`). This spends credits.

## Scope

- VN Studio (branch `VNO-10_flow-provider` from `master`): a Flow client, the three providers, settings, status, UI pickers, docs, tests.
- flow-music-mcp (branch `FMM-11_vn-studio-hooks` from `master`, see the decisions): small changes the voice provider needs.
- Hub (branch `HUB-07_flow-vn-provider` from `master`): the `make-visual-novel` skill, README, ROADMAP, a run log for the live run.

## Out of scope

- Flow video, video edits, `flow_continue`, and the paid `flow_narrate` engine `flow`. VN Studio never sends them.
- Ambience and SFX from Flow. Ambience stays on the ComfyUI engine; SFX stay on import or a custom workflow.
- Loop-point detection and the Flow Music Advanced settings (BPM, Length): they belong to FMM-06 / FMM-07. VN Studio uses them when they land.
- Auto-starting flow-music-mcp from VN Studio (the existing "auto-start the studios" roadmap item).
- Batching images through `flow_agent_images` (later; see open question 5).
- Editing a finished asset with `flow_edit` (later; see open question 10).

## What the code says today (facts the design rests on)

- VN Studio already has an MCP client: `src/engine/studios/mcp-http.ts` (Streamable HTTP, JSON-RPC over `fetch`, session id,
  bearer token, `structuredContent`). Pixel Studio, Chiptune Studio and VibeTTS use it. flow-music-mcp's `src/mcp/http.ts` is the
  same transport (copied from comfy-mcp, which copied VN Studio) and returns `structuredContent` for every tool.
- After a flow-music-mcp restart an old session id gets HTTP 404 "Session not found". VN Studio's client only re-initializes on
  `unreachable`, so it would fail until the engine restarts. This needs a fix (phase 0).
- Image generation is a `switch` on the asset kind in `src/engine/assets/generate.ts` (`generateAsset`), every branch calls
  `ctx.comfy.generate`, then `finishImage` post-processes (fit, sprite cutout, trim, pixel art). `finishImage` is engine-agnostic.
- Sprite cutout: `removeBackground` (BiRefNet through VN Studio's own ComfyUI client, `qwen-edit`, or the local flat-colour `key`)
  falls back `qwen-edit -> birefnet -> key`. comfy-mcp `remove_background` is not needed: VN Studio calls the same BiRefNet itself.
- Every asset is its own job (`vn.assets.generate`, `handlers.ts` `generateJob` / `dispatchGenerate`), gated by `comfySem`. Jobs
  have `max_attempts` and are retried with backoff (`queue/scheduler.ts` ~line 670).
- Music follows its provider in `generateAsset` (the `CHIPTUNE_ENGINE` pseudo engine). Ren'Py loops music by itself; a version's
  `loopStartSec` becomes `<loop X>file` (`renpy/emit.ts` `musicFile`). A track with no loop point repeats from the start.
- Voice: `voice.provider` is `vibetts | comfy` (`shared/vn.ts`); clips are `voice/<lang>/<beatId>.<format>` with a hash index
  (`voice/jobs.ts` `generateVibeClips`); `config/voice.md` `format` is `mp3 | wav`. VN Studio has no ffmpeg.
- flow-music-mcp:
  - `flow_generate` queues one paced job per scene (25-70 s apart, one Flow job at a time for every client), takes `project`,
    `create_project`, `aspect_ratio`, `model`, `reference_images` (`asset:<media_id>` or an absolute path, max 3),
    `download_quality` (`upscaled` = 2K image), `max_credits` (images: 0, a paid image model is refused), `out`, `name`,
    `start_number`, `wait` (0-50 s). It returns `images: [{scene, file, media_id, title, variant}]` or a job id for `flow_wait`.
  - `flow_wait` waits at most 50 s per call. Jobs live in memory until FMM-05 persists them (`jobs.json`).
  - `flow_edit` (image), `flow_character`, `flow_assets`, `flow_download` refuse with "A Flow job is running" while the Flow
    queue is busy. They are not queued.
  - An image edit replaces the tile in place with a new media id. So `flow_edit` on a sheet would turn the sheet itself into
    the first sprite.
  - Uploading a local file needs the user's `FLOW_MUSIC_MCP_UPLOAD_RIGHTS=agree` (set). `asset:<media_id>` needs no upload.
  - `flow_narrate` engines: `gemini` (free, AI Studio key, model `gemini-2.5-flash-preview-tts` unless
    `FLOW_MUSIC_MCP_GEMINI_TTS` is set), `windows` (System.Speech), `flow` (paid). `text` is 1-400 characters. It always writes
    `.m4a`. `flow_voices` lists 30 Gemini voices (name + description, no gender) and only `en-*` Windows voices.
  - `music_generate` has no credit quote and no `max_credits` (Flow Music shows no quote; the cost per song is unknown until
    FMM-06). A take is about 2:40-3:00 and plays through. FMM-07 plans `music_loop` and a `loop_friendly` prompt option.
  - Credit cap: `FLOW_MUSIC_MCP_MAX_CREDITS=50` caps each paid Flow call (video, Flow voices). It does not cover Flow Music.
- flow-music-mcp ticket numbers FMM-04 to FMM-10 are already taken (`.claude/tickets/FMM-04-10_roadmap-tasks/plan.md`;
  FMM-04_unit-tests is the checked-out branch with uncommitted work).

### Voice language coverage (docs only, nothing called)

- Gemini TTS, per https://ai.google.dev/gemini-api/docs/speech-generation (read 2026-10-22): the language is detected from the
  text (no language parameter). `gemini-3.8-flash-tts` reads 130+ languages, `gemini-3.8-flash-lite-tts` 100+. **Croatian is
  listed for both**, as are Serbian and Bosnian; Slovenian only for 3.8 Flash.
- The model flow-music-mcp uses by default, `gemini-2.5-flash-preview-tts`, is **not on that page any more**. Its coverage is not
  documented there and it may be retired. For Croatian, use `gemini-3.8-flash-tts`.
- The rate-limits page gives no free-tier numbers for TTS ("view them in AI Studio"). Assume a low per-minute and per-day limit:
  VN Studio paces and retries.
- Windows: only Microsoft David and Zira (en-US) are installed, and flow-music-mcp filters the list to `en-*`. System.Speech
  usually does not see the newer OneCore voices. So Croatian through the `windows` engine is not realistic; Gemini is the route.

## Decisions made

1. **MCP, not a new HTTP API.** VN Studio talks to flow-music-mcp over MCP with its existing `mcp-http.ts` client.
   flow-music-mcp gets no HTTP API. Reason: the client exists, is tested, and the transport is the same code.
2. **Images through `flow_generate`, one asset per Flow job, exact prompts.** Not the agent. The direct composer keeps the prompt
   as written and is the verified path for single images.
3. **Sprites are new images with the sheet as a reference, not edits.** `flow_generate` with
   `reference_images: ["asset:<sheet media id>"]`. `flow_edit` on the sheet is rejected: it replaces the sheet tile in place,
   so the next sprite would start from the last sprite. `flow_character` is not used in the pipeline (it refuses while the
   queue is busy, and draws 16:9 portraits).
4. **One Flow project per VN**, named `vno-<slug>` (`create_project: true`). Keeps media ids and titles apart from other work.
5. **VN Studio waits, flow-music-mcp queues.** VN Studio starts a job with `wait: 0`, then polls `flow_wait` / `music_wait`
   (40 s per call) until done or a timeout. A VN abort calls `flow_cancel` / `music_cancel`.
6. **One Flow job at a time from VN Studio** (`flowSem`, 1 permit, separate from `comfySem`), so a VN job's timeout measures its
   own work, not a queue it filled itself. Other clients may still queue in between.
7. **Images always pass `max_credits: 0`.** A paid image model is refused by flow-music-mcp, never charged.
8. **Voices: only `gemini` and `windows`.** VN Studio never sends `engine: "flow"`.
9. **No silent fallback to another provider.** When Flow is down or not signed in, the asset or clip fails with the reason and
   the start hint. Mixing ComfyUI and Flow art in one book would change the look. A single asset can still be made with
   ComfyUI on purpose: `vno_asset_regen {engine: "<comfy engine>"}` uses ComfyUI for that run (as engines work today).
10. **Music jobs are never retried automatically** (`max_attempts: 1`). A failed take may already have spent credits.
11. **flow-music-mcp changes go on `FMM-11_vn-studio-hooks`**, because FMM-04 to FMM-10 are taken. (The brief said
    `FMM-04_<what>`; see open question 1.)

## Open questions for the user (with my recommendation)

1. **Ticket number in flow-music-mcp.** FMM-04 (unit tests) to FMM-10 are already planned there. *Recommend `FMM-11_vn-studio-hooks`.*
2. **Sprites.** (a) `flow_generate` with the sheet as reference (decided above), (b) a Flow character per cast member and
   `asset:<name>` as the reference, (c) `flow_edit` on a copy. *Recommend (a); (b) can come later if likeness drifts.*
3. **Cutouts.** BiRefNet through ComfyUI (better edges; needs ComfyUI up) with the flat-colour key as the fallback, or the key
   only (no ComfyUI at all; sprite prompts ask for a plain flat background). *Recommend: keep `art.bgRemoval` as set
   (default `birefnet`) with the existing fallback to `key`, and always ask Flow for a plain flat background so the key works.*
4. **Fallback when Flow is down.** *Recommend none (fail with the hint); per-asset ComfyUI on purpose via `vno_asset_regen {engine}`.*
5. **Batching.** `flow_agent_images` makes 3 images in ~35 s instead of ~3 paced jobs (~3-4 min), but the agent may reword
   prompts. *Recommend per-asset `flow_generate` first; batch backgrounds later if the run is too slow* (a small VN of ~15
   images takes about 20-30 min).
6. **Image size.** *Recommend 2K (`download_quality: upscaled`) for backgrounds, full CGs and the cover (1K is 1376x768, below
   1920x1080); 1K for sheets, sprites and inserts.* Config key, so it can change.
7. **Music spend cap.** No quote exists. *Recommend: `music.provider: flow` only when set by hand, a cap of songs per project
   (`flowMusicMaxSongs`, default 4), the pipeline only makes missing tracks, and the hub asks the user before the first song.*
   What cap do you want?
8. **Gemini TTS model.** *Recommend `gemini-3.8-flash-tts` (Croatian listed): set `FLOW_MUSIC_MCP_GEMINI_TTS` in your `.env`
   now, and make it the code default in FMM-11.*
9. **Voice clip format.** *Recommend FMM-11 adds `format` (`mp3 | wav | ogg | m4a`) to `flow_narrate`, and VN Studio asks for
   its `config/voice.md` format (mp3).* Alternative: VN Studio keeps `.m4a`, which Ren'Py does not list as supported.
10. **Editing finished assets with `flow_edit`** ("make her coat red"). Free, but it refuses while the Flow queue is busy.
    *Recommend later, after FMM-11 or a later FMM ticket queues image edits as jobs.*
11. **Windows voices for Croatian.** *Recommend not pursuing; Gemini covers Croatian.* Installing a Croatian Windows voice is
    your call in Windows settings.
12. **Loops.** Until FMM-07's `music_loop` lands, a Flow song repeats from its start (with its intro and fade-out). *Recommend
    accepting that for v1 and adding loop wording to the sound prompt ("steady, no intro, no ending, no fade-out").*

## Design

### Config (VN Studio)

`config/studios.md` (zod defaults in `src/engine/studios/config.ts`, so old data folders need no migration):

| Key | Default | What |
|---|---|---|
| `flowUrl` | `http://127.0.0.1:7462/mcp` | flow-music-mcp (`VNO_FLOW_URL` overrides) |
| `flowRepo` | `C:\projects\Personal\flow-music-mcp` | for the start hint |
| `flowToken` | `''` | `FLOW_MUSIC_MCP_TOKEN` (env or credential store) wins |
| `flowPollS` | 40 | seconds per `flow_wait` / `music_wait` call (max 50) |
| `flowJobTimeoutS` | 900 | give up on one Flow image job after this |
| `flowMusicTimeoutS` | 600 | same for a song |
| `flowImageQuality` | `{background: upscaled, cover: upscaled, cg: upscaled, sheet: original, sprite: original, insert: original}` | download size per kind |
| `flowVoicePauseMs` | 1500 | pause between `flow_narrate` calls |
| `flowVoiceRetries` | 3 | retries of a clip on a rate-limit error (backoff 10 s, 30 s, 90 s) |
| `flowMusicMaxSongs` | 4 | songs one project may make through Flow Music (counted from its asset versions) |

Project settings (`src/shared/vn.ts`):

- `ART_PROVIDERS` gains `'flow'`. `art.flowModel?: string` (e.g. `Nano Banana Pro`; missing: Flow's newest Nano Banana).
  `art.flowProject?: string` (missing: `vno-<slug>`).
- `MUSIC_PROVIDERS` gains `'flow'`. `resolveMusicProvider` never picks it by default.
- `voice.provider` gains `'flow'`. Voice ids: `gemini:<Name>` (e.g. `gemini:Charon`) or `windows:<Voice Name>`.
  `voice.flowStyles?: Record<speakerKey, string>` (optional Gemini delivery note, e.g. "gruffly, tired").
- Pseudo engines `FLOW_ENGINE = 'flow'` and `FLOW_MUSIC_ENGINE = 'flow-music'` (like `CHIPTUNE_ENGINE`).
- `assetVersionSchema` gains `remote?: { provider: 'flow' | 'flow-music', id: string, project?: string }` (Flow media id or song id).

### The Flow client (`src/engine/studios/flow.ts`)

A typed wrapper over `createMcpClient` (label "flow-music-mcp", token var `FLOW_MUSIC_MCP_TOKEN`), like `pixel.ts`:

- `status()` -> `flow_status {detailed: false}` (signed in, busy, upload rights).
- `generateImage({prompt, aspect, model?, references?, quality, project, out, name})` -> `flow_generate {scenes: [{prompt,
  type: "image", aspect_ratio, model, reference_images, download_quality, max_credits: 0, retries: 1}], project,
  create_project: true, out, name, start_number: 1, wait: 0}`, then `waitJob`.
- `waitJob(ids, {timeoutMs, signal})`: loops `flow_wait {job_ids, timeout_seconds: flowPollS}` (HTTP timeout poll + 20 s)
  until `finished`; `status: "unknown"` (server restarted) -> error "flow-music-mcp restarted; generate again"; on abort
  -> `flow_cancel` and throw `aborted`.
- `voices()` -> `flow_voices`. `narrate({text, engine, voice, style?, out, name, format?})` -> `flow_narrate`.
- `song({sound, title, out, name, format})` -> `music_generate {instrumental: true, wait: 0}`, then `music_wait` the same way.
- Errors map to a `StudioError` kind: `unreachable` (hint: `hub.ps1 start flow-music-mcp`), `signedOut` (hint: `yarn login`
  in flow-music-mcp), `busy`, `rateLimit` (Gemini 429), `credits` (refused by a cap), `tool`.

`mcp-http.ts` change: on HTTP 404 with a session id, drop the session, re-`initialize` once and repeat the request. Helps every studio.

### How an image job runs

1. `generateAsset` resolves the provider: an unlocked generated image follows `art.provider` (`flow` -> engine `flow`),
   unless an engine was given for this run (then ComfyUI, as today). Same rule music already has.
2. Prompt: the planned prompt or `fallbackPrompt` (English, full looks; the art-director already writes it that way).
   Sprites need a full prompt, not a ComfyUI edit instruction: `flowSpritePrompt(entry, book)` = "The same character as in the
   reference image: <looks>. <expression> expression, full body, standing, facing the viewer, centred, plain flat light grey
   background, nothing else in the picture." plus the planned instruction.
3. Aspect from the kind: background, full CG, cover `16:9`; sheet, sprite `9:16`; insert `1:1`.
4. References: sprite -> its sheet; CG -> the sheets of its characters (first 3, warn about the rest). A sheet version with
   `remote.id` is passed as `asset:<id>`. A sheet without one (made by ComfyUI or by hand) is passed as its absolute file
   (an upload; works only with the user's upload rights, else the error says so). A stale media id (trashed, edited) falls
   back to the file once.
5. `out` is `<project>/.vno-tmp/flow/<assetId>`; the file is read, then `finishImage` runs as for ComfyUI (fit, cutout, trim,
   pixel art), the raw image of a sprite is kept as `v<n>.raw.jpeg`, and the tmp folder is removed.
6. The version records `engine: flow`, `prompt`, `seed: null`, `remote: {provider: 'flow', id: media_id, project}`.
7. Before the fan-out, `dispatchGenerate` calls `status()` once: not signed in or unreachable -> the step fails at once with the
   hint, instead of every asset failing one by one.

### How a voice job runs

1. `voice.plan` with provider `flow`: candidates are `flow_voices` (Gemini for every language VN Studio knows; Windows only
   for the culture each voice reports after FMM-11). Gender comes from `flow_voices` after FMM-11, else a fixed table in
   `voice/flow-catalog.ts`. The existing `pickVoices` assigns them.
2. `voice.generate` (new `generateFlowClips` next to `generateVibeClips`, same index, same hash idea): hash =
   `flow|engine|voice|lang|style|format|text`. One beat is one call and one file. `flow_narrate` caps `text` at 400
   characters for every engine, although only the paid `flow` engine needs it: FMM-11 lifts the cap to 4000 for `gemini`
   and `windows`. Until then a longer beat fails with a clear error (VN Studio cannot join parts: it has no ffmpeg).
3. One call at a time, `flowVoicePauseMs` between calls, retry on 429 with backoff. The index is saved after every clip, so a
   stopped job continues.
4. `vno_voice_set` / `vno_voice_preview` work through `narrate` with the provider's voices.

### How a music job runs

1. Only when `music.provider` is `flow` (never a default). The job gets `max_attempts: 1`.
2. Before the call: count this project's versions with engine `flow-music`; at `flowMusicMaxSongs` the job fails with
   "Flow Music cap reached (n songs); raise flowMusicMaxSongs in config/studios.md".
3. Prompt: the composer's plan for the track plus loop wording (open question 12). `title` = `<book title> <track id>`,
   `format: mp3`, `instrumental: true`.
4. Result: `v<n>.mp3` in the asset folder, `remote: {provider: 'flow-music', id: song id}`, `loopStartSec: null`. Once
   FMM-07's `music_loop` exists, call it and store its loop file and loop start.
5. Each song is logged in the job log and in the run log (hub), so credits can be counted until FMM-06 reads the balance.

### Waiting, caps, failure (summary)

| Case | What happens |
|---|---|
| flow-music-mcp not running | Asset/clip fails, hint `hub.ps1 start flow-music-mcp`; the generate step fails early after the status check |
| Not signed in | Same, hint `yarn login` in flow-music-mcp |
| Flow queue busy with other work | VN job waits in `flow_wait` up to `flowJobTimeoutS` |
| Flow reports a failed tile / high demand | Image job fails, scheduler retries (images are free) |
| A paid image model chosen | Refused by `max_credits: 0`, error says so |
| Gemini 429 | Retry with backoff, then the clip fails; others continue |
| Song fails | No retry; the user decides |
| Song cap reached | Job fails before any call |
| VN stop / abort | `flow_cancel` / `music_cancel` (a running Flow Music take cannot be stopped; its file may still arrive) |
| flow-music-mcp restarted mid-job | `status: unknown` -> fail with "generate again" (FMM-05 makes this a clear `failed`) |

## Phases

Each phase is one PR-sized step, tested and committed before the next. VN Studio phases are on `VNO-10_flow-provider`.

### Phase 0: groundwork (VN Studio)

Files:
- `src/engine/studios/mcp-http.ts`: re-initialize on 404 "Session not found".
- `src/engine/studios/flow.ts` (new): the Flow client above.
- `src/engine/studios/config.ts`: the `flow*` keys, `VNO_FLOW_URL`, `StudioId` gains `flow`, start hint, token.
- `src/engine/vn/service.ts`: `studios()` returns `flow`; `studiosStatus()` probes it (`vno_studios_status` shows it).
- `src/shared/vn.ts`: the provider enums, `art.flowModel`, `art.flowProject`, `voice.flowStyles`, `remote` on versions,
  `FLOW_ENGINE`, `FLOW_MUSIC_ENGINE`.
- `seed/config/studios.md`: the new keys, commented.
- `tests/studio-fakes.ts`: a fake Flow server (tools/list, the tool calls, a job that finishes after N polls).

Tests: `tests/mcp-http.test.ts` (404 -> re-init -> success), `tests/studios-flow-client.test.ts` (generate -> wait loop ->
files; unknown job; abort -> cancel; error kinds), `tests/vn.test.ts` (settings parse: old project.md unchanged, new values round trip).

Done when: `yarn test`, `yarn typecheck`, `yarn lint` are green; old projects load unchanged.

### Phase 1: images (VN Studio)

Files:
- `src/engine/assets/generate.ts`: provider resolution for images; a `flow` branch per kind (aspect, references, quality,
  tmp out, `finishImage`, raw sprite kept); `remote` on the version; `GenerateContext.flow?: FlowClient`.
- `src/engine/assets/flow-prompts.ts` (new): `flowSpritePrompt`, `flowAspect`, `flowReferences`.
- `src/engine/vn/handlers.ts`: `flowSem` (1 permit), pass `studios.flow`, the status check in `dispatchGenerate`; hand-mode
  checks untouched.
- `src/engine/assets/derive.ts`: stubs get engine `flow` when `art.provider` is `flow`.
- `src/engine/mcp/tools.ts`: `vno_update_settings`, `vno_asset_regen`, `vno_asset_generate` descriptions name `flow`.
- `src/engine/vncli.ts`: `--art-provider flow` (from `ART_PROVIDERS`), `--flow-model`.
- `src/renderer/ui/book/LookTab.tsx`: "Google Flow (free images)" in the provider picker.
- `docs/mcp-guide.md` (a "Google Flow" section), `docs/protocol.md` (Studios), `README.md`.

Tests (`tests/flow-generate.test.ts`, with the fake client; no ComfyUI image call for any image kind):
- each kind sends the right aspect, quality and `max_credits: 0`;
- a sprite references `asset:<sheet media id>`; a sheet without `remote` is sent as its file; a CG sends at most 3 sheets and warns;
- the version has `engine: flow` and `remote.id`; a sprite keeps `v<n>.raw.jpeg` and `reprocess` works on it;
- `vno_asset_regen {engine: "qwen-image-2.1"}` on a flow project uses ComfyUI for that run;
- not signed in -> the generate step fails once with the hint; unreachable -> hint;
- pixel style + flow: the Flow image goes through pixel finishing.

Done when: the tests above and the full suite, typecheck and lint are green. Not live yet (phase 4).

### Phase 2: voices (flow-music-mcp first, then VN Studio)

flow-music-mcp, `FMM-11_vn-studio-hooks` (after FMM-04 is merged, so `yarn test` exists):
- `src/flow/local-tools.ts`: `flow_narrate` gains `format` (`mp3 | wav | ogg | m4a`, default `m4a` so nothing changes);
  `text` may be up to 4000 characters for `gemini` and `windows` (400 stays for `flow`).
- `src/flow/voices.ts`: `windowsVoices()` lists every installed voice with its culture (not only `en-*`); `flow_voices`
  returns `culture`.
- `src/flow/gemini.ts`: `GEMINI_VOICES` gain `gender`; default model `gemini-3.8-flash-tts` (still overridable by
  `FLOW_MUSIC_MCP_GEMINI_TTS`); `flow_voices` reports the model in use. A 429 says "rate limited" in the error text.
- Tests (vitest): the format to ffmpeg target mapping, the voice list parsing (cultures), the gender table is complete.
- Docs: README, CLAUDE.md, ROADMAP (tick the Gemini/Windows items it covers; Croatian stays "try live" under FMM-10).
- Done when: `yarn build`, `yarn test` green. Live (free): one `flow_voices`, one Gemini line in English and one in Croatian
  as mp3, checked by ear. Ask the user before the first Gemini call only if the key is missing.

VN Studio:
- `src/engine/voice/flow.ts` (new): `planFlowVoices`, `generateFlowClips`, preview.
- `src/engine/voice/flow-catalog.ts` (new): which voices read which language, gender fallback.
- `src/engine/vn/handlers.ts` (~lines 600-660): route `voice.provider === 'flow'`.
- `src/engine/vn/service.ts`: voice status for the flow provider.
- `src/engine/mcp/tools.ts`, `src/renderer/ui/book/VoiceTab.tsx`, `docs/mcp-guide.md` (Voices section).
- Tests (`tests/voice-flow-jobs.test.ts`): plan picks Gemini voices for `hr` and `en` and a Windows voice only for its culture;
  generate makes `voice/<lang>/<beatId>.mp3`, saves the index per clip, keeps unchanged and imported clips; a 429 retries
  then fails one clip; a beat over the tool's limit fails alone with a clear error; `engine: flow` is never sent.
- Done when: tests, typecheck and lint green.

### Phase 3: music (VN Studio; FMM-07 optional)

- `src/engine/studios/flow-music.ts` (new): `makeFlowTrack` (cap check, prompt, song, wait, file, `remote`).
- `src/engine/assets/generate.ts`: the `music` case routes `FLOW_MUSIC_ENGINE`.
- `src/engine/vn/handlers.ts`: music jobs of a flow project get `max_attempts: 1`.
- `src/shared/vn.ts`: `resolveMusicProvider` unchanged (never defaults to flow).
- UI music provider picker, `vno_update_settings` text, docs (say it spends Flow Music credits and the cap).
- When FMM-07 has merged: call `music_loop` and store `loopStartSec`. Until then `loopStartSec: null`.
- Tests (`tests/flow-music.test.ts`): cap reached -> no call; a song lands as `v<n>.mp3` with `remote`; a failed song is not
  retried; a pixel book without `music.provider` still picks chiptune.
- Done when: tests, typecheck and lint green.

### Phase 4: hub wiring and the live run (creative-hub, `HUB-07_flow-vn-provider`)

- `.claude/skills/make-visual-novel/SKILL.md`: when the user wants Flow art/voices/music, set `art.provider: flow`,
  `voice.provider: flow` (Gemini voices), `music.provider: flow` only after the user's OK; start `flow-music-mcp` with
  `hub.ps1 start flow-music-mcp`; replace the "import Flow files by hand" text.
- `README.md` table / `services.json` note: VN Studio uses flow-music-mcp. `ROADMAP.md`: move "Flow in VN Studio" to done when
  played. Tick the item in VN Studio's and flow-music-mcp's `ROADMAP.md`.
- `runs/<slug>.md` for the live run.

## Branches

- VN Studio: `VNO-10_flow-provider` from up-to-date `master`. (The repo now sits on `VNO-09_roadmap` with an untracked
  `ROADMAP.md`; leave that alone and branch from `master`.)
- flow-music-mcp: `FMM-11_vn-studio-hooks` from `master`, after FMM-04 merges. (The working tree now has uncommitted
  FMM-04 work; do not touch it.)
- Hub: `HUB-07_flow-vn-provider` from `master` (the hub now sits on `HUB-01_roadmaps-to-repos` with uncommitted changes).
- Each repo: ticket folder `.claude/tickets/<ticket>/` with `plan.md` (its part of this plan) and `changelog.md`.

## Verification

Unit (every phase): VN Studio `yarn test`, `yarn typecheck`, `yarn lint`; flow-music-mcp `yarn build`, `yarn test`.

Live run in the hub (after phases 0-2; phase 3 only with the user's OK for credits):
1. `hub.ps1 build vn-studio`, `hub.ps1 stop vn-studio`, `hub.ps1 start vn-studio`; `hub.ps1 build flow-music-mcp`,
   `hub.ps1 start flow-music-mcp`; reconnect `/mcp`. Do not start Scriptorium.
2. `flow_status`: signed in. `flow_voices`: Gemini key ready, model `gemini-3.8-flash-tts`.
3. `vno_create_project` with a small story: 2 characters, 2 places, 2 chapters, one choice, one full CG, an English text and
   a Croatian edition (`vno_edition_set`). Settings: `art: {provider: "flow"}`, `voice: {enabled: true, provider: "flow",
   langs: ["en", "hr"]}`, music on chiptune or ComfyUI (or one Flow song if the user agrees).
4. `vno_run_pipeline {from: "art"}`, `vno_wait`. Check: every image has `engine: flow` and a `remote.id`; sprites are cut out;
   no ComfyUI image call in the log (BiRefNet cutouts only if chosen); the Flow balance is unchanged (images are free).
5. `vno_voice_plan`, `vno_voice_generate` for en and hr; listen to a few Croatian clips.
6. `vno_build`, `vno_lint` clean. The user plays it in both languages. Only then is it done (hub rule).
7. Log every id, setting, time taken and anything unverified in `runs/<slug>.md`.

Record what was verified and what was not in each repo's changelog and ROADMAP (for example: asset references by media id,
2K downloads under load, Gemini rate limits on a full book, loops).

## Risks

- Flow's UI changes break flow-music-mcp; VN Studio then fails with the tool's message. Nothing to do on the VN side.
- `asset:<media_id>` as an image reference in the direct composer is implemented in flow-music-mcp but only a local reference
  file was verified live. Check it first in the live run; if it fails, sprites fall back to uploading the sheet file.
- Character likeness across sprites from one reference image is not tested. The art-critic (`art.review`) can catch drift.
- Free Gemini TTS limits may stop a long book halfway; the job resumes where it stopped.
- Flow Music cost per song is unknown until FMM-06.
