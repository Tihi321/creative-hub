# HUB-29 research: Cartoon Studio (cutout-puppet children's cartoon series)

Date 2026-11-07. Read-only research. **C** = confirmed (read or ran, with path or command), **I** = inferred. I installed and ran nothing; render speed and lip-sync quality are unmeasured.

## Question
What exists in the hub and its tool repos that a new Cartoon Studio (5-10 min, ages 4-8, South Park-style cutout puppets, lip-synced, hr + en voice tracks over one animation, reusable series bible, local MP4 at $0) can reuse, and what is missing?

## Answer
- **Script**: Scriptorium's `kids-cartoon` screenplay (`get_screenplay`) gives scenes, shots, cast, dialogue per speaker, SFX, music cues and places with looks (C: `scriptorium/docs/screenplay.md:26-100`), but it is capped at 45-120 s, 1-2 chapters (`:15`), has no series bible shared across episodes, no per-line timing, no staging/gesture vocabulary. Needs a new `cartoon-episode` format, or Cartoon Studio's own writer role via the `client` provider (cheaper for the pilot).
- **Art**: nothing makes layered puppet parts today. VN Studio makes one sheet plus one flat-grey-background full-body sprite per expression and keys/BiRefNet-cuts it (C: VN `docs/mcp-guide.md:55,121`). comfy-mcp has `generate_image`, `edit_image` (Qwen-Image 2.1 edit, 1-16 refs), `remove_background` (BiRefNet), `run_workflow` (C: `comfy-mcp/README.md:12-19`). Parts must be derived from one master image (code split plus vector faces), not generated separately (I).
- **Lip-sync**: no phoneme/viseme timings anywhere. VibeTTS returns path and duration only (C). Rhubarb is not installed (C). ffmpeg 9.0.2 is on PATH (C). flow-music-mcp already runs whisper.cpp for word times (C: `src/flow/captions.ts:36-60,141-146`; words 0.13-0.18 s late on half of them). Plan: amplitude envelope first, whisper word times plus a Croatian letter-to-viseme table second, Rhubarb optional for English (I).
- **Render**: headless Chromium (Playwright) running a deterministic Canvas 2D puppet player, frames piped to ffmpeg; same page is the studio preview (I). Estimate 5-15 min for 10 min at 1080p30, 2-6 min with 12 fps limited animation (I, unmeasured).
- **Repo template**: copy Edu Studio (engine + MCP + queue + roles + `client` provider). Next free port: **7465** (C: netstat shows nothing on 7464-7466; 7464 is Edu's optional STT default, `edu-game-studio/docs/speaking.md:17,46`).
- **Roles**: 8-9 roles are worth it, the rest of Scriptorium's 17 are overkill (section below). Highest-value reviewer: a vision "frame critic" on rendered frames.
- **Paid voice (Voice Creator Pro)**: verdict **skip the $55 desktop app**; OmniVoice, Qwen3-TTS (Base and VoiceDesign) and Higgs v3 are already downloaded in this machine's ComfyUI (C). Keep a paid provider slot only. Details below.

## Path through the code (evidence)

### 1. Script
- **C** Grammar: `SCENE`, `SHOT (framing, move, Ns)`, `ON SCREEN`, `MUSIC`, `SFX`, `TITLE`, `NAME (delivery): words`, action; JSON `characters[{name,looks,voice,aliases}]`, `places`, `music[{id,description,from,to}]`, `chapters[scenes[shots[{id,framing,move,seconds,continuous,action,cast,sfx,title,lines[{speaker,delivery,text,kind}]}]]]` (`scriptorium/docs/screenplay.md:26-100`).
- **C** Formats `short-film`, `cartoon` (60-180 s), `kids-cartoon` (45-120 s, ages 3-8, child-safety reviewer) (`screenplay.md:11-16`); length gate rewrites when more than 15% outside range (`:107`); 2.5 words/s, shots 4-10 s (`:47,96`); humanizer off, max_rounds 1.
- **C** The VN pack is the translation seam: fixed template plus per-language text catalog (README.md:28). A screenplay book has no pack (`screenplay.md:7`). Reuse the pattern: episode file language-independent, text and audio per language.
- **I** No series entity shared between books exists in Scriptorium for screenplays (not found in the docs read).
- **Gaps for 5-10 min**: runtime range (300-600 s = about 60-120 shots, 750-1,500 spoken words); series bible with stable cast/set ids, voices, catchphrases outside any book; dialogue-first staging (enter/exit/walk/gesture/camera vocabulary); mouth-friendly short lines; hr text is usually longer than en, leave 15-25% air (I).
- Option A: Scriptorium `cartoon-episode` format (SCP ticket). Option B: Claude writes episode JSON through Cartoon Studio's `client` provider, using `get_screenplay` only for book adaptations. B first.

### 2. Art
- **C** VN assets: backgrounds, `sheet_<char>` (reference only), `sprite_<char>_<expression>` (neutral, happy, sad, angry, surprised, worried, scared, thinking; custom sets), CGs (`mcp-guide.md:19,55`). A sprite is a new image from the sheet reference on "a plain flat grey background", cut by flat-colour key or BiRefNet; Flow route uses `asset:<media id>` refs (max 3 sheets per CG); Flow images free, one job at a time, 30-70 s each (`:121`). Regenerating a sheet marks sprites stale (`:213`). Backgrounds 1920x1080, sprites transparent and bottom-aligned (`:113`).
- **C** No layering or part split in VN, Edu or comfy-mcp.
- **C** comfy-mcp: `generate_image` (z-image-turbo, qwen-image-2.1, krea2, moss-image), `edit_image` (Qwen-Image 2.1 edit), `remove_background` (BiRefNet to PNG alpha), `run_workflow` (`README.md:11-22`).
- **I** Consistency: flat South Park look (solid colours, black outline) is the easiest to hold. Separately generated head and body will mismatch. Route: one front-facing neutral master per character; split by code (neck/shoulder line); inpaint hidden areas by Qwen edit; draw eyes and mouths as vector from a per-character template; one arm sprite rotated on a pivot. Grey-background key beats BiRefNet for clean edges.
- **I** Backgrounds: 2-3 parallax layers per set (sky/mid/foreground), Qwen edit can split one painting.

### 3. Voice and lip-sync
- **C** Hub rule: Gemini free 10 requests/day, Croatian first, languages allocated whole (`creative-hub/CLAUDE.md`; Edu `seed/config/voice.md`: `state/gemini-tts.json`, `edu_voice_quota`). A 5-10 min episode is 150-300 lines per language; Gemini only works if lines are batched per scene (the lighthouse run hit the daily 429 at once: `runs/the-lighthouse-that-kept-lists-2.md`, Found).
- **C** VibeTTS engines (README:186-192): Kokoro (en, es, fr, hi, it, pt; no Croatian), Supertonic 3 (31 languages incl. Croatian, 10 voices F1-F5 M1-M5, about 11x real time), Higgs v3 (100 languages incl. Croatian, bosnian, serbian; 4 presets and own clips; 3.85 GB; slower than real time on CPU). MCP returns path, duration, size, voice, language; `synthesize_batch` items `{text, output, voice, speed}` (MCP instructions). Grep for timestamp/phoneme/alignment/viseme in `vibe-tts-flow/vibetts` found nothing: **no word or phoneme timings**.
- **C** Rhubarb: not on PATH; no `*rhubarb*` under `D:\Programs` or `C:\Users\Infplane\AppData\Local\Programs` (find, maxdepth 3). ffmpeg and ffprobe 9.0.2 on PATH (Gyan.FFmpeg WinGet). Node is not on the Bash PATH (fnm).
- **I** Lip-sync ladder: (1) RMS envelope per frame to rest/half/open; (2) whisper word times (shift 0.12 s early like captions) plus Croatian grapheme-to-viseme table (Croatian orthography is near-phonemic) and M/B/P closure, O/U rounding; (3) Rhubarb for English only. 6-8 mouth shapes (rest, A, E/I, O, U, M/B/P, F/V, L) are enough for ages 4-8.
- **I** hr and en: one rig, sets and script graph, **two renders** with the timeline rebuilt from each language's audio durations; a shared video with two audio tracks only if line lengths are forced to match.

### 4. Render
- **C** flow-music-mcp: `flow_assemble` runs ffmpeg (`src/flow/assemble.ts:12,106,144,214`) over video clips and image+seconds+zoom stills, places voices, music cues, ducking, `clip_volume` (`timeline-pure.ts`). Captions: whisper.cpp for words, **headless Chrome draws the lettering, ffmpeg overlays it** (`captions.ts:29-34`); `playwright-core` dependency (`package.json:18`).
- **C** `scripts/video-plan.mjs` (512 lines, dependency-free, `node --test`): plan.json state, `fitSeconds` (2.5 words/s, shots 4/6/8/10), `assignVoices` (Gemini voices by gender and tags), Flow credit estimates, `flow_assemble` timeline. Reuse the plan.json + `record`/`next` state pattern; credit math is not needed.
- **C** Browser rendering in repos: Edu uses Playwright Chromium for the autoplay bot (`scripts/play.mjs:8,115`) and its own Canvas 2D player (`AGENTS.md`); VN builds an HTML5 player (`src/engine/game/player-runtime.ts`). No Remotion, node-canvas or skia dependency found in package.json files (some repos not inspected).
- **C** Machine: AMD Radeon 8060S (Strix Halo APU; Ryzen AI Max+ 395 per VibeTTS README:10), no NVIDIA (`nvidia-smi` not found; WMI lists the Radeon; AdapterRAM 4 GB is a capped field, real memory is shared).
- **Options** (I, unmeasured): (1) **Playwright + Canvas 2D `renderFrame(t)` -> ffmpeg stdin (recommended)**: 18,000 frames at 30 fps, 15-50 ms/frame => 5-15 min; render at 12 fps limited animation then `fps` filter to 24/30 => 7,200 frames, 2-6 min; preview 960x540. Try `h264_amf` else x264 veryfast. (2) `@napi-rs/canvas` (Skia) in Node: faster, one drawing code if written to the Canvas 2D API only; second step. (3) Electron `capturePage`: no gain. (4) Remotion: heavy, licence; skip. (5) pure ffmpeg overlays: not viable for puppets.

### 5. Repo template (Edu Studio)
- **C** `edu-game-studio` layout: `src/engine/{agents,assets,budget,comfy,edu,live,logs,mcp,models,pipeline,queue,research,review,store,studios,stt,themes,voice}`, `src/{main,preload,renderer,player,shared,design,live-client}`, `seed/{agents,config,prompts,palettes,workflows}`, `docs/`, `scripts/play.mjs`, `tests/` (Vitest fast; `*.e2e.test.ts` Chromium). Stack: Electron 44, electron-vite, React 19, zustand, zod 4, Yarn 4, Node 24, `@modelcontextprotocol/sdk`, `sharp`, `yaml`, `@napi-rs/keyring` (`package.json`, `AGENTS.md`).
- **C** Conventions (`AGENTS.md`): MCP tool = `def(name, description, zod, run)` in `src/engine/mcp/tools.ts` or `xxxTools(svc, def, opts)` lists; job handlers in `src/engine/edu/handlers.ts`; `node out/engine/index.js --mcp-only`; env `EDU_DATA`, `EDU_MCP_PORT`, `EDU_MCP_TOKEN`, `EDU_SEED`, `EDU_AUTOSTART=0`; one engine per data folder (`store/lock.ts`); seed config as editable markdown with migrations (`store/seedRefresh.ts`); public repo (no keys, no personal paths); tickets `EGS-NN` in `.claude/tickets/`, branch `EGS-NN_<what>`.
- **C** `client` provider: `src/engine/models/client.ts` (task queue with lease, model id `client/claude-code`), tools `edu_get_task`/`edu_submit_task`/`edu_client_tasks`/`edu_release_task`, `edu_wait` returns `clientTasks` (skill `make-edu-game` section 1).
- **C** Registry steps: `services.json`, `.mcp.json`, README table, skill, ROADMAP (`CLAUDE.md`). Ports in use: 7341, 47811, 7459, 7463, 7457, 7458, 7723, 8188, 7460, 1234, 8080, 7461, 7462. Proposed: repo `C:\projects\Personal\cartoon-studio`, port **7465**, data `~\CartoonStudio`, tools `cts_*`, tickets `CTS-NN`, skill `make-cartoon`. HUB-28 folder exists (untracked); HUB-29 is free.

## Roles
- **C** Role = job type with ordered default models in `config/roles.md` (aliases `paid/strata/lmstudio` resolved from `config/settings.md`; next model on failure, rate limit or budget). Agent = persona file `seed/agents/<role>-<name>.md` (front matter `kind, role, name, model, focus, pin, max_parallel, paused` + short system prompt); several agents per role. Task prompts in `seed/prompts/<role>/*.md` with format variants (`_sp`, `_vn`). Scriptorium: 28 agent files, 17 roles (architect, archivist, beta-reader, child-safety-reviewer, continuity-checker, copy-editor, developmental-editor, editor-in-chief, fact-checker, humanizer, idea-generator, line-editor, originality-checker, publisher, read-aloud-reviewer, researcher, writer). Edu: 21 roles, 23 agents (`edu-game-studio/seed/config/roles.md:1-82`, `seed/agents/`). Reviewers prefer a different model family from the writer; must-pass roles (fact-checker, accessibility, child-safety) block; publisher decides from reviews and hard gates; `art-critic` needs a vision model, loops pass/revise up to `max_rounds`, not must-pass. `client/claude-code` parks jobs for Claude ($0).
- **Worth it for v1** (mostly `client/claude-code`): (1) **showrunner** (Edu director + series bible keeper, run summary, folds in publisher gates); (2) **writer** (dialogue-first script plus beats/staging/camera; storyboard merged in for the pilot); (3) **character-designer/rigger** (shape language, palette, part list, pivots, mouth/eye sets; prompts for ComfyUI; rig JSON; rigging itself is code plus check); (4) **background-artist**; (5) **voice-director** (voice per character per language, quota rule, references); (6) **composer** (series theme, stings, 1-2 cues per episode); (7) **child-safety-reviewer** (must pass; copy); (8) **frame-critic** (vision: contact sheet of 6-12 sampled rendered frames per scene, checks off-model, overlaps, mouth open on silence, wrong facing, missing background; not must-pass, 1-2 rounds; highest value because every other check is blind to the picture).
- **Later**: translator (hr/en adaptation for length and humour, reuse Edu's), editor (pacing/loudness; start deterministic), animator performance direction (kept inside the writer; lip-sync/walk are code).
- **Overkill**: archivist, humanizer, originality-checker, idea-generator, researcher and fact-checker (no facts unless educational), the developmental/line/copy editor trio, read-aloud reviewer (merge into writer self-check), beta-reader, playtester, accessibility-reviewer (a legibility check inside the critic). 8-9 roles is plenty.

## Paid TTS: Voice Creator Pro versus what we already have
- **C** No repo has a paid TTS provider (grep of vibe-tts-flow, flow-music-mcp, edu-game-studio, visual-novels-orchestrator, comfy-mcp: no ElevenLabs/Azure/OpenAI-TTS/Polly code; `alignment` hits are edition text alignment). Edu's `voice.md` already has `media.voice.provider: auto` and per-speaker reference assets to copy.
- Coordinator read the pricing page (2026-11-07): Cloud Free 5k tokens/mo and no API; Starter $5/mo 250k tokens (about 80 h) with Cloud API; Premium $20/mo 1.5M; Desktop Lifetime from $54.99, offline, local API, "GPU 8 GB+ VRAM"; models Kokoro, OmniVoice, Qwen3; zero-shot cloning/voice design from 3-10 s; 600+ languages; STT and subtitle generator.
- **NOT CONFIRMED**: I could not read `/api`. `curl https://voicecreator.pro/api` returned HTTP 429, a Vercel Security Checkpoint page (saved at `C:\Users\Infplane\AppData\Local\Temp\vcp-api.html`, no docs in it); I have no web-fetch tool. Whether its TTS or STT returns word or phoneme timestamps is **unknown**; someone must open the page and look for `timestamps/words/alignment` fields (TTS) and `verbose_json`/SRT/VTT (STT). **I**: Kokoro/OmniVoice/Qwen3 do not emit phoneme timings natively, so TTS probably returns audio only; its STT likely gives word times of whisper quality, which we already have free.

### Direct comparison: desktop app ($55) vs what is already here
| | Voice Creator Pro desktop | Already on this machine |
|---|---|---|
| OmniVoice (600+ languages, includes Croatian, cloning optional, `instruct` style) | yes | **Installed**: `ComfyUI-Shared/models/TTS/omnivoice/OmniVoice` 3.1 GB (C: `du`); engine spec `OmniVoiceEngineNode`, default engine of Edu/VN, languages `*`, clone optional, ref-free from style (C: `edu-game-studio/src/engine/comfy/tts-engines.ts:78-91`; `voice.md`) |
| Qwen3-TTS (10 languages: en, zh, ja, ko, de, fr, ru, pt, es, it; **no Croatian**) | yes | **Installed**: `qwen3_tts/Qwen3-TTS-12Hz-1.7B-Base` and `...-1.7B-VoiceDesign` 12 GB (C: `du`, `ls`); engine spec with `instruct`, cloning, x-vector-only mode (C: `tts-engines.ts:134-149`; comfy-mcp `generate_speech` workflow `qwen3-tts`, `README.md:34-38`) |
| Kokoro | yes | VibeTTS, about 8x real time on CPU, 41 voices, no Croatian (C: README:186-192) |
| Higgs Audio v3 (100+ languages incl. Croatian, cloning, inline delivery tags) | not listed | **Installed** in ComfyUI (8.7 GB) and optional in VibeTTS (3.85 GB); research/non-commercial licence (C: `voice.md`, `comfy-mcp/README.md:38`) |
| Supertonic 3 (31 languages incl. Croatian) | not listed | VibeTTS, about 11x real time, 10 voices (C) |
| Chatterbox 23 languages (no Croatian), F5-TTS, IndexTTS-2, VibeVoice, CosyVoice | not listed | Also under `models/TTS` (C: `ls`) |
| Voice design / cloning | yes | Qwen3-TTS VoiceDesign (installed) and cloning in OmniVoice, Qwen3 Base, Higgs, F5, IndexTTS-2 via TTS-Audio-Suite |
| Word/phoneme timings | unknown | none from TTS; whisper.cpp word times in flow-music-mcp (C) |
| Runs on this PC | needs "GPU 8 GB+ VRAM": **no NVIDIA here**; AMD Radeon 8060S (C); unknown whether the app has a non-CUDA path | The same models already run here through ComfyUI (the hub's comfyui service, 8188) |
| Cost | $54.99 one time | $0 |

- **I** Licences (not verified, check model cards before publishing episodes): OmniVoice (k2-fsa) and Qwen3-TTS are, to my knowledge, open-weight under Apache-2.0-class terms, i.e. fine for commercial/YouTube use; Higgs v3 is research/non-commercial (C, `voice.md`); F5-TTS is CC-BY-NC (C). A bundled app does not change the model licences.
- **I** VRAM: OmniVoice about 3 GB of weights, Qwen3 1.7B about 4-8 GB loaded; both fit this machine's shared memory (VibeTTS README:10, Strix Halo). The hub's note that Strata uses most GPU memory applies: do not run TTS in ComfyUI while Strata is up (`services.json` strata note).
- **Croatian**: OmniVoice (hr claimed, 600+ languages), Supertonic (hr), Higgs (hr) cover it; Qwen3-TTS does not (C: its language list). Actual quality: **not listened to**, needs a user test of one hr paragraph per engine.
- **Cloning / design for a series (I)**: yes, it is the right way to keep a character's voice the same across episodes: generate one 3-10 s reference per character (VoiceDesign for a fictional voice, no real person), store `voice_<char>.wav` plus transcript and style in the series bible (Edu's `voice.refTexts` / `voice.styles` mechanism, `voice.md`), reuse for all episodes. Zero-shot drift between sentences and languages is real: test hr and en per character, keep engine, version and seed in the bible, and re-synthesise a line rather than splice.
- **Verdict**: **Skip the $55 desktop app.** Every model it names is already installed and callable (OmniVoice, Qwen3-TTS, Kokoro) or beaten by what is installed (Supertonic, Higgs for Croatian), it is $0, and the desktop app may not run on an AMD APU. Nothing needs adding to VibeTTS: VibeTTS has Kokoro, Supertonic and Higgs; OmniVoice and Qwen3 are already reachable through ComfyUI (TTS-Audio-Suite) and Edu/VN already drive them. The one real gap is **timings**, which neither the app (unconfirmed) nor our engines solve; whisper does. Optional later step: add `OmniVoice` (and the Qwen3 VoiceDesign workflow) as selectable engines in Cartoon Studio's voice step, copying Edu's `tts-engines.ts`; check that comfy-mcp's `generate_speech` table lists OmniVoice (I read only the rows for chatterbox, f5, indextts-2, qwen3, higgs: `README.md:34-38`). If the user wants a trial of the cloud, **Starter $5/mo** (1 month) is the cheap probe, but only after the API page confirms timestamps; it stays a provider slot, never a dependency.
- **Provider slot design**: one interface `synthesize(text, lang, voiceRef, style) -> {file, seconds, words?: [{w,t0,t1}]}` with providers `auto | gemini | vibetts | comfy(omnivoice|qwen3|higgs) | voicecreator`; missing `words` falls back to whisper then to amplitude; keys in the OS keyring as Edu does.

## Reproduction
Not a bug; nothing reproduced. Commands run: `which ffmpeg ffprobe rhubarb node`; `netstat -ano` (7463-7466); `Get-CimInstance Win32_VideoController`; `du -sh`/`ls` of `ComfyUI-Shared/models/TTS`; `curl https://voicecreator.pro/api` (HTTP 429 challenge).

## What the plan needs
1. New repo `cartoon-studio` from Edu's skeleton (drop course/quiz/android/live/classroom). Data layout: `series/<slug>/bible.json`, `cast/<id>/{master.png,parts/,rig.json,voice.json}`, `sets/<id>/{layers/,set.json}`, `episodes/<ep>/{script.json,text/<lang>.json,audio/<lang>/,timeline.<lang>.json,out/<lang>.mp4}`.
2. Modules: queue, store, models (`client`), MCP `cts_*`, roles seed, comfy client, voice (provider slot, quota), puppet player (Canvas 2D), lip-sync, render (Playwright + ffmpeg), lint (`cts_lint`: unknown cast id, line without audio, missing viseme track, character off-frame).
3. Interfaces: series bible, episode script (language-independent beats + text catalogs), rig, per-language timeline (line starts, viseme track, walk/gesture keys, camera keys).
4. Reuse as services: comfy-mcp 7460, Chiptune Studio 7458 (`compose_track`, `render_audio`), VibeTTS 7723 (`synthesize_batch`), flow-music-mcp 7462 (`flow_narrate`, `flow_generate` with `max_credits: 0`, `flow_transcribe`, optional `flow_assemble`/`flow_captions`), Scriptorium `get_screenplay` (only if the user agrees to start it), Book Translator for catalogs.
5. Reuse by copy: voice quota, asset manifest and placeholders, job queue and resume, roles/agents seed, `client` loop, `edu_wait` pattern, `tts-engines.ts`.
6. Tests: fast Vitest with fakes (no real app starts), one Chromium e2e rendering 2 s and checking ffprobe duration/size, golden viseme timeline from a fixture wav; follow `test-discipline`.
7. Hub: skill `make-cartoon`, run log `runs/<slug>.md`, `services.json`, `.mcp.json`, README, ROADMAP row.
8. **First milestone, 60-second pilot scene**: 2 characters, 1 set, 12-16 lines hr and en (Claude writes via `client`); each character from one flat master, grey-key cutout, split into head/body/arms, 6 mouth and 3 eye states in vector; one background plus a foreground layer; voices from Supertonic and OmniVoice (Gemini optional for hr); lip-sync amplitude first, then whisper word-timed visemes, compare; idle bob, blink, head turn, one walk-in, one gesture, one cut, one pan; render 960x540 12 fps then 1080p30, hr.mp4 and en.mp4, record render time; ffprobe, 6 frames read by Claude; the user watches. Success: on-model in 4 sampled frames, mouths visibly track speech, 60 s renders in under 5 min, both languages from one script.

## Risks
- **Part extraction** (highest): diffusion cannot be told to draw a character in parts; mitigation above (one master, code split, vector faces, simple geometry).
- **Croatian voice and lip-sync**: no Kokoro hr; Supertonic/OmniVoice/Higgs hr quality unheard. Gemini 10/day cannot carry an episode (C).
- **Two-language timing**: separate timelines per language, or forced-length rewrites.
- **Scriptorium cap and no series**: cross-repo change; Scriptorium must not be started unasked (CLAUDE.md).
- **Render speed and AMF** unmeasured. **Whisper lateness** 0.13-0.18 s (C): apply the 0.12 s shift.
- **Licences**: Higgs v3 research-only, F5 CC-BY-NC (C); verify OmniVoice/Qwen3 and any cloud terms before publishing.
- **Shared compute**: ComfyUI image models, TTS, Strata and the render share one APU; run them in turns.
- **Public repo**: no keys or data committed; any paid key in the keyring. Do not hard-depend on Voice Creator Pro.

## Open questions
1. Does the Voice Creator Pro API (`https://voicecreator.pro/api`) return word/phoneme timestamps on TTS or STT? Blocked for me (429 bot check); needs a browser. Does the desktop app run on AMD (Radeon 8060S, no CUDA)? System requirements.
2. Listening test of Croatian: Supertonic, OmniVoice, Higgs, per voice (user).
3. Install Rhubarb (English only) or stay with amplitude + whisper? Is a vision model available at $0 for the frame critic (Claude client, Gemini free)?
4. Scriptorium `cartoon-episode` format, or Claude-written episodes in Cartoon Studio? Where does the series bible live?
5. Exact look: stiff paper cutout with open/close mouths (simple rig) or smoother limb animation?
6. Render target time; does ffmpeg `h264_amf` work here (not run)?
7. Confirm port 7465, name `cartoon-studio`, prefix `CTS`, data `~\CartoonStudio`.
8. A background grep for ports 7464-7470 across all repos timed out and I did not read its result; `netstat` shows no listener and the only hit found was 7464 (Edu STT). A repo might still name another of these ports in docs.
9. Licences of OmniVoice and Qwen3-TTS (inferred permissive, not read from the model cards).

## Addendum: measured speeds and where an episode's time goes

**Measured by the coordinator on this machine, 2026-11-07 (reported, not re-run by me):** VibeTTS Supertonic F3 made 28.2 s of Croatian in about 11.3 s wall (about 2.5x real time, MCP round trip included). Kokoro af_bella made 18.1 s of English in about 3.7 s (about 5x). `higgs_installed` is **false in VibeTTS**, so VibeTTS has no Croatian voice cloning today. This corrects my table above ("Higgs optional in VibeTTS"): the only local cloning route for Croatian is ComfyUI, where the folders `models/TTS/omnivoice` (3.1 GB) and `models/TTS/higgs_audio_v3` (8.7 GB) exist (C: `du`); that the nodes run and read Croatian well is **UNTESTED** (I). The rated speeds in the VibeTTS README (8x, 11x) are slower in practice (5x, 2.5x), so use the measured numbers.

**Time budget for one 10-minute episode in hr + en (all estimates, I; only the voice rows rest on measurements).** Assumes the pilot's rig is done and 6 new set backgrounds, 3 guest props, 220 lines per language.

| Stage | Machine time | Human/Claude time | Notes |
|---|---|---|---|
| Voices, hr (about 600 s of audio, 220 lines) | about 4 min at 2.5x (Supertonic) | review by ear | measured rate; Gemini free tier covers only about 10 requests |
| Voices, en (about 600 s) | about 2 min at 5x (Kokoro) | review by ear | measured rate |
| Voice retakes (10-15% of lines) | about 1 min | listening | cost is the user's ear, not CPU |
| Word timings (whisper on 2 x 600 s) | about 3-10 min on CPU | none | unmeasured; a small model is much faster than real time |
| Lip-sync tracks | seconds (amplitude), under 1 min (word-timed) | none | code |
| Script and beats (writer, showrunner, safety review) | none | about 15-40 min of Claude client tasks | $0 on `client/claude-code`; the largest model-work block |
| Set backgrounds (6 sets, 2-3 layers each, with retries) | about 18 images x 20-70 s plus 2 retries each => 15-45 min (Flow is one job at a time at 30-70 s: `mcp-guide.md:121`; ComfyUI faster) | Claude reads every image: 15-30 min | VN-style regen loop; art is the volatile part |
| New puppet (per new character, first time) | 10-30 min generation and edits (master, variants, mouth/eye edits, cutouts) | 30-90 min of checking and fixing parts | pays off once: cast is reused by every episode; this is where retries concentrate |
| Frame critic (vision) | 5-15 min | Claude reads 30-60 sampled frames | only if run on rendered frames after each render |
| Render, per language, 1080p30 (18,000 frames) | 5-15 min (browser path), 2-6 min at 12 fps | none | unmeasured; render both languages = double |
| Final mux, loudness, ffprobe | 1-2 min | none | ffmpeg |
| User review | | 10-20 min per language | the real acceptance |

Totals (I): a **repeat episode** with existing cast, mostly new dialogue and 2-3 new sets is about 1-2 h of mostly waiting machine time and Claude's client loop; a **first episode** adds roughly 2-4 h for cast and rig (art plus fixes) and is dominated by art retries and human checking, not by voices or render. Voices (about 6-10 min total) and render (about 10-30 min for both languages) are small; model work (script, beats, reviews) and art with checking are the two big blocks. Therefore: spend design effort on part extraction and reusable rigs, keep hr/en as two cheap renders, and run the frame critic on contact sheets, not every frame.

## Addendum: VectorCraft probe (2026-11-07)

Drew one head set (7-year-old girl: round head, pigtail buns with pink ties, ears, bangs, cheeks; eyes open/half/closed; mouths rest, A, E, O, MBP) in VectorCraft over MCP (headless backend), one layer per part on a 600x600 artboard, each part exported alone by toggling layer visibility. Files: `.claude/temp/vectorcraft-probe/` (9 SVGs, 5 composed PNGs `c_*.png`, `sheet.png` = head + eyes_open + each mouth side by side).

- Wall time: about 2.5 min (147 s from first call to last export), about 27 tool calls, of which 4 drawing batches (`command_batch` with `draw_shape`/`draw_path`), 3 previews, 1 batch that did all 8 part exports plus 5 composed PNGs. One look-and-fix round (hair ties were behind the face; brought to front).
- Clean SVGs: yes. Every file has `viewBox="0 0 600 600"`, only `circle`/`ellipse`/`rect`/`path` with flat `fill` and `stroke`/`stroke-width="6"`; no filters, gradients, `<image>`, `style=`, text or hrefs (grep checked). Hidden layers are left out. Leftovers: a `<title>Untitled-1</title>`, an unused `xmlns:xlink`, `stroke-miterlimit="10"`, ids suffixed `-2` with `data-name`; harmless, strip in the pipeline if wanted. A rounded rect comes out as a `path`.
- Sizes: head 1536 B, eyes_open 789, eyes_half 1047, eyes_closed 561, mouth_rest 395, mouth_A 589, mouth_E 850, mouth_O 359, mouth_MBP 557; composed PNGs about 25 KB each, sheet 62 KB.
- What was hard: nothing in the drawing itself; the friction was setup. `export` only writes under `C:\Users\Infplane` (the hub's `.claude/temp` was refused: "outside the write root"), so files went to the scratchpad and were copied. Z-order has to be planned (draw order = stack order; `object.arrange.bringToFront` fixes it). No layer-solo export, so per-part export is a visibility toggle per layer (fine inside one batch). The sheet was composed with PowerShell System.Drawing, not in VectorCraft.
- What it really is: Claude writes the geometry by hand (coordinates, Bezier `d` strings) either way; VectorCraft adds layers, previews, z-order, pathfinder and clean export. The art quality equals what hand-written SVG would give with the same coordinates; the gain is the render-and-look loop, not the drawing.

Verdict (I): good enough for a South Park-style kids' show (ages 4-8): the parts read clearly at TV size, stack exactly, and the files are tiny and clean. Versus hand-written SVG: same output quality, a bit faster to iterate because of `render_preview` and layer toggling, but it adds a running app and a write-root quirk. Recommend: Cartoon Studio stores parts as plain SVG in a fixed 600x600 frame (the format both routes produce), and treats VectorCraft as an optional authoring and preview tool, not a dependency; for repeat characters a parametric SVG template (colors, hair style, eye/mouth library) written by code would beat both. Not verified: the look in motion (blinks and visemes swapped at 12-24 fps), and other body parts (torso, arms) and turnarounds.

## Addendum: ComfyUI image bake-off (2026-11-07)

Seed 7, via comfy-mcp `generate_image`. Images and contact sheet: `.claude/temp/image-bakeoff/` (`bakeoff.png`). Wall s is warm unless noted. Scores 1-5: flat / outline / grey bg / separable limbs / kid / adherence (limbs and grey bg n/a for C).

| model | prompt | wall s | scores | note |
|---|---|---|---|---|
| z-image-turbo | A | 26 (seed 8; seed 7 cold run not timed) | 4/4/3/3/5/4 | white sticker halo, light grey ~#aaa, arms hug body, hood hides hair |
| z-image-turbo | B | 26 | 4/4/3/2/4/3 | not scruffy, arms at sides, white halo |
| z-image-turbo | C | 39 | 3/2/-/-/5/3 | clean flat shapes, thin outlines only, trees crop at top |
| qwen-image-2.1-turbo | A | 37 | 4/3/5/3/3/3 | exact grey, thin outline, flat, plain face |
| qwen-image-2.1-turbo | B | 31 | 2/2/4/2/2/3 | furry hatching, thin line, creepy |
| qwen-image-2.1-turbo | C | 42 | 2/2/-/-/4/3 | white gradient sky, vignette, tiny props |
| qwen-image-2.1 | A | 102 | 5/4/5/4/3/3 | flattest and greyest (#808080), but bald and odd |
| qwen-image-2.1 | B | 101 | 3/4/4/3/3/3 | hatched fur, hands raised |
| qwen-image-2.1 | C | 145 | 2/1/-/-/3/2 | gradients, no outlines, objects tiny |
| krea2-turbo | A | 68 (cold) | 4/5/4/5/5/5 | thick black outline, paper texture, arms clear of body, best cutout feel |
| krea2-turbo | B | 64 | 4/5/4/4/5/5 | scruffy, friendly, arms away, tail separate |
| krea2-turbo | C | 88 | 3/3/-/-/4/4 | real paper-cutout layers, grain texture, bench and pond ok |
| moss-image | A | 123 (cold) | 4/5/4/3/5/5 | nice, ground shadow, arms close to coat |
| moss-image | B | 122 | 3/4/4/3/4/5 | collar, fur shading |
| moss-image | C | 171 | 3/2/-/-/5/4 | flowers, sky gradient, pond cut off |

Pick for characters: Krea 2 Turbo (about 65 s), thick outline, clear grey, arms away from the body, kid-friendly, follows the prompt best. Z-Image Turbo (26 s) is the fast fallback, but its white halo and hugging arms need rework.
Pick for backgrounds: Z-Image Turbo (39 s) for the flattest shapes that vectorise easily; use Krea 2 Turbo C if a real paper-grain look is wanted. Neither draws thick outlines on backgrounds; add them in the vector step.

Caveats: the first Qwen runs all failed with `'HiggsAudioV3Engine' object has no attribute 'clone_base_uuid'` (stale voice-model state in ComfyUI); `free_memory` fixed it, so free it before image work after speech work. One seed only (second seed added just for Z-Image A). Z-Image seed 7 A cold time was lost.
