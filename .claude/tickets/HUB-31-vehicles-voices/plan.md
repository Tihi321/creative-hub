---
status: in-progress
request: REQ-0022
repos: [creative-hub, cartoon-studio, flow-music-mcp]
branch: HUB-31_vehicles-voices; CTS-30_vehicles-elevenlabs (cartoon-studio), FMM-17_elevenlabs-voices (flow-music-mcp)
updated: 2026-11-09
---

# HUB-31: ElevenLabs voices and vehicle characters (pilot 4, Pip the car and Bruno the train)

Request: `.claude/director/requests/REQ-0022-cartoon-episodes.md`. The user's words after pilot 3: "ok so 3d is ok, but for text i need eleven labs or something and characters needs to be simpler, like cars, trains or something that moves with no legs and have no arms". Their answers are in the brief: ElevenLabs free tier for every line within the free monthly quota, VibeTTS past it, hr and en, $0. Pip becomes a small zippy car and Bruno a big gentle train engine, with no arms and no legs and an original look. Pilot 4 follows the pilot 3 path, and the user approves the sheets and watches the result.

Read before this plan: `.claude/tickets/HUB-30-cartoon-3d/plan.md` (the 3D route, its contracts and the acting library), `runs/pip-bruno-3d-pilot.md`, `.claude/skills/make-cartoon/SKILL.md`, and in `cartoon-studio` on `CTS-18_blender-3d` at `dc92781`: `src/shared/contracts.ts`, `src/engine/voice/*`, `src/engine/studios/flow.ts`, `blender/cts_blender/acting/library.json`, `seed/style/toon-3d.md`. In `flow-music-mcp` on `master` at `56cf836`: `src/flow/local-tools.ts`, `src/flow/keys.ts`, `.env.example`. ElevenLabs docs read on 2026-11-08: models overview, the `with-timestamps` endpoint, `GET /v1/user/subscription`, the pricing page and the Eleven Creative quickstart.

**Reading (per the global Scope rule):** I am building the **narrow reading**. That means an ElevenLabs voice engine that Cartoon Studio uses now and other tools can call later, a vehicle body type for the existing 3D route (contract, builder, sheet, set kit, acting library), and pilot 4 (60 s, hr and en). VN Studio and Edu Studio get no ElevenLabs provider in this ticket.

## Scope

1. **An ElevenLabs engine in flow-music-mcp.** It includes:
   - key lookup with no key-setting tool;
   - a status tool with the live quota and the models that read hr and en;
   - a voice listing;
   - `flow_narrate` engine `elevenlabs` with character timestamps turned into word times;
   - a quota and tier guard that refuses before any request that could go past the free quota or bill money.
2. **ElevenLabs as the first voice provider in Cartoon Studio.** It covers:
   - allocation: ElevenLabs, then Gemini, then local, whole languages at a time, Croatian first;
   - ElevenLabs voice ids per character per language in the series bible;
   - word times from ElevenLabs alignment, with whisper kept for every other provider;
   - `cts_voice_quota` showing the ElevenLabs credits.
3. **Vehicle characters in Cartoon Studio's 3D route.** It covers:
   - a character `kind: "vehicle"` in `cts.character3d/1` (no arm or leg controls; wheels, lamp eyes, bumper mouth, chimney puffs, antenna chain);
   - a `cylinder` part shape;
   - the builder, the turnaround and expression sheet with a motion strip;
   - a road and rail set kit with paths;
   - a vehicle acting library;
   - timeline, assembly, lint, prompts and frame checks for vehicle series.
4. **Pilot 4**: series `pip-bruno-wheels`, episode `ep00-pilot`, about 60 s, hr and en, with the vehicle Pip and Bruno, ElevenLabs voices, $0, and 0 Flow credits.
5. **Hub wiring.** It covers:
   - the new CLAUDE.md voice rule, written only after the user approves the wording;
   - the make-cartoon skill, the README, the `services.json` note and the ROADMAP row;
   - the run log `runs/pip-bruno-wheels-pilot.md`.

## Out of scope

- ElevenLabs providers in VN Studio and Edu Studio. They can call `flow_narrate` engine `elevenlabs` later. That is a row in each tool's `ROADMAP.md`, not code here.
- Any paid ElevenLabs plan, overage, paid-only endpoint or paid-only output format (`pcm_44100`, `wav_44100`, `mp3_44100_192`), plus voice cloning, the dubbing, sound-effects or music APIs, and speech-to-speech.
- Typing, creating, pasting or storing an API key or an account by the agent. Only the user does that.
- Downloading ElevenLabs voice preview files. Auditions are generated from our own lines inside the quota.
- Flow video (0 credits). The pilot 3 intro and outro show the animal Pip and Bruno, so they do not fit (decision 12).
- Phase 2 (a 5-10 min episode), more characters or sets, an animated level-crossing barrier, retiring the Canvas player.
- Changing pilot 1, 2 or 3 data. Deleting the creature acting code (decision 9).
- Starting Scriptorium or Chiptune Studio. Touching the hub's uncommitted HUB-28 files (`ROADMAP.md` row 22, `.claude/tickets/HUB-28-edu-mobile-music/`, `runs/hub-28-edu-mobile-music.md`).
- Pushing before the checker passes, force-push, auto-merge.

## Decisions

1. **The ElevenLabs client lives in flow-music-mcp, not in Cartoon Studio or VibeTTS.** Why:
   - flow-music-mcp is already the hub's cloud speech gateway. `flow_narrate` engine `gemini` is free cloud TTS with a key kept in `~/.flow-music-mcp`, and `flow_transcribe` gives whisper word times. Cartoon Studio, VN Studio (Flow voice provider) and Edu Studio already call it. A new `engine: "elevenlabs"` on the same tool makes the engine usable by all three without a second client.
   - The key stays in one place outside every repo, and Cartoon Studio never holds it.
   - VibeTTS is the local, offline Python tray app. A cloud engine with a key and a quota does not belong in it.
   - A client inside Cartoon Studio would have to be copied for VN and Edu later.
   - What is built now is only what the cartoon needs: status, voices and narrate with timestamps. There is no streaming, cloning or dubbing.
2. **The key is set by the user only.** flow-music-mcp reads `ELEVENLABS_API_KEY` from the environment first, then from `~/.flow-music-mcp/.env`. That file already exists as the tool's ignored settings file and lives outside every repo. Rules:
   - There is **no** `flow_set_key`-style tool for ElevenLabs, so no chat ever holds the key.
   - Requests send it only as the `xi-api-key` header.
   - Every error, log line and tool result goes through a redactor that replaces the key value with `[key]`. Status reports only `ready: true|false` and `source: "env" | "file"`, never the key or part of it.
   - Setup for the user (in the README and the skill): make a free account, create an API key, and restrict it to Text to Speech plus read access for Voices, Models and User if the key dialog offers those scopes. Then put it in one of the two places and restart flow-music-mcp.
3. **The quota guard is in the engine, before every request.**
   - `flow_elevenlabs_status` calls `GET /v1/user/subscription` (`tier`, `character_count`, `character_limit`, `next_character_count_reset_unix`, `can_extend_character_limit`) and `GET /v1/models` (per model: `can_do_text_to_speech`, `languages[].language_id`, and the character cost multiplier when the response has one, else 1.0).
   - `remaining = character_limit - character_count`.
   - `flow_narrate` engine `elevenlabs` computes `estimate = ceil(chars x multiplier)` and refuses with `E_ELEVEN_QUOTA` when `estimate > remaining - reserve` (default `reserve` 200 credits, set by `FLOW_MUSIC_MCP_ELEVEN_RESERVE`).
   - It refuses with `E_ELEVEN_PAID_TIER` when `tier` is not `free` or `can_extend_character_limit` is true, so usage-based billing can never run. An override env var exists only for a later, user-approved plan and is not set here.
   - Both refusals send no TTS request. After each line the result carries `credits_estimate` and `remaining_after` (from a fresh subscription read).
   - Server answers are mapped as follows: a 401 `quota_exceeded` gives `E_ELEVEN_QUOTA`; `detected_unusual_activity` gives `E_ELEVEN_BLOCKED` (the free tier blocks some VPNs and proxies); a 429 is retried with backoff, with requests sent one at a time (free concurrency is 2-4).
4. **Model: `eleven_multilingual_v2` by default, with Croatian checked live.**
   - The ElevenLabs models page (2026-11-08) lists Croatian for `eleven_multilingual_v2`, `eleven_flash_v2_5`, `eleven_v3` and `eleven_v4`. Only `eleven_flash_v2` is English-only.
   - `eleven_multilingual_v2` costs 1 credit a character (pricing page). It is the default model of the timestamps endpoint and is stable on short lines.
   - It does **not** take `language_code` (the language follows the text). If the hr audition has an English accent, the fallback is `eleven_flash_v2_5` with `language_code: "hr"` at 0.5 to 1 credit a character. The user hears both in the audition (pilot step 5).
   - The model is a per-character bible field with a series default in `config/voice.md` (`elevenlabs.model`).
   - The engine refuses a model whose live `languages` lack the line's language (`E_ELEVEN_LANG`). The status result records which models read `hr` and `en`, and that goes in the run log (C5).
   - `eleven_v3` and `eleven_v4` are not used: their credit rate and timestamp support were not confirmed for the free tier.
5. **Voices: ElevenLabs' default (premade) voices, not Voice Library voices.**
   - The official quickstart says "The voice library is not available via the API to free tier users". So pilot 4 picks from the voices that `GET /v1/voices` returns for this account with category `premade`.
   - Each candidate is auditioned with a line in each language: 3 candidates per character, and the same candidate in hr and en where it sounds right, so a character keeps one voice across languages.
   - The chosen ids go in the bible as `voice.<lang>.elevenlabs = { voiceId, name, model, settings: { stability, similarity_boost, style, speed } }` and are reused in every episode. `cts_voice_plan` warns `W_VOICE_ID_CHANGED` when an episode's voice id differs from the one recorded at the first approval.
   - See open question 1 for Voice Design as the alternative.
6. **Allocation (pure, in `voice/allocate.ts`).**
   - Languages are allocated whole, Croatian first, then English.
   - Each language goes to ElevenLabs if all its lines that need speaking fit in `remaining - reserve` credits. Else it goes to Gemini if they fit in today's free requests. Else it goes to the local chain.
   - The local chain is unchanged: hr is OmniVoice through ComfyUI, then Supertonic through VibeTTS; en is Kokoro through VibeTTS. This is what the hub rule calls "local VibeTTS". The user approved OmniVoice for Croatian in pilot 3.
   - If a language that was allocated to ElevenLabs hits `E_ELEVEN_QUOTA` mid-run (only when someone else used the account during the run), its remaining lines go to the next provider and lint warns `W_VOICE_MIXED`, which is named in the run log.
   - A character's `provider` may pin `elevenlabs`. That still obeys the quota.
7. **Word times: ElevenLabs alignment replaces whisper for ElevenLabs lines, and whisper stays for the rest.** This is simpler and better than whisper here:
   - The alignment is of the exact script text, so no edit-distance matching is needed and coverage is 1.0. Whisper aligned only 85 % of the hr lines in pilot 3.
   - It costs no extra request, because `with-timestamps` costs the same as plain TTS.

   How it works:
   - flow-music-mcp groups `alignment.characters` with their start and end times into words (split on whitespace, punctuation stripped from the word edges, Croatian letters kept).
   - The voice step stores them in the manifest `words`, with `wordsCoverage: 1` and a new optional `wordsFrom: "elevenlabs" | "whisper"`. The lip-sync then runs the existing `words-<lang>` method unchanged.
   - **The trim shift:** `normaliseWav` trims the leading silence, so it gains a `leadTrimS` result (measured with ffmpeg `silencedetect` with the same threshold on the input). Every ElevenLabs word time is shifted by `-leadTrimS` and clamped to `[0, seconds]`. Test 3 guards this.
   - Lines from Gemini or the local voices keep the whisper path (`flow_transcribe`, language always passed).
8. **Vehicles are a body kind inside `cts.character3d/1`, not a new contract version.**
   - The spec gains `kind: "creature" | "vehicle"` (default `creature`, so the pilot 3 specs parse unchanged).
   - For `vehicle`, the required controls are `root squash body head lid_L lid_R pupil_L pupil_R mouth` plus at least one `wheel_<n>`. `head` is the front face block, which tilts and turns within limits.
   - `arm_*`, `hand_*` and `leg_*` are **errors** (`E_VEHICLE_LIMB`).
   - Optional controls: `brow_L/R` (lamp hoods), `chimney` (puff source and squash), `exhaust`, `horn`, `antenna1..n` (a spring chain), `acc_<name>1..n`.
   - A new `vehicle` block: `{ type: "car" | "train", wheelRadius, wheels: [control names], track: bool }`. A train has `track: true` and only moves along a `track` path.
   - The motion profile for vehicles is `motion: { tempo, energy, bounce, drive: { style: "zip" | "chug", topSpeed, accel, suspension } }` (a zod union on `kind`).
   - `PART_SHAPES` gains `cylinder` (wheels, chimney, buffers). `shapes.py` already has a cylinder mesh.
   - The face's eyes get `lamp: { glow: hex, rim: palette name }` for lamp eyes that can flash.
9. **The acting library is rebuilt for vehicles. The creature moves leave the vehicle vocabulary, but their code stays frozen for pilot 3.**
   - Every action in `library.json` gets `bodies: ["creature"] | ["vehicle"] | ["creature", "vehicle"]`. Lint `E_ACTION_BODY` refuses an action that a cast member's body cannot do.
   - The writer prompt lists only the actions of the series' bodies.
   - The arm and leg functions (`walk`, `run`, `point`, `wave`, `shrug`, `think`, `sit`, `stand_up`, `cheer`, the arm swing) are not deleted, because `pip-bruno-3d` must still re-render. They are tagged `creature` and get no new features, which is the same rule as the frozen Canvas player.
10. **The face: an original "lamp-eyes and bumper-mouth" design for the series.** The rule for every vehicle in this series:
    - **Eyes are the vehicle's own front lamps.** Two round domed lamps, each with a hood that is the lid (blink, half lid, squint) and a dark pupil disc that aims at the look target. A small chrome visor above each lamp is the brow.
    - **The mouth is the bumper slot (car) or the buffer-beam slot (train)** under the lamps, with the six viseme shapes.
    - **No nose, no cheeks, no sculpted human face plate.** Windscreens and cab windows stay plain tinted windows and are never eyes. No face sits on a round smokebox door.

    This avoids the two franchise signatures: eyes in the windscreen (Cars) and a human face on the smokebox front (Thomas). The designer prompt, the frame-critic prompt and the sheet review check it (C9).
    - **Pip, a small zippy car.** A round one-box "pebble" two-seater in the bible orange `#d9792b`, with a cream `#f3dfb5` lower front.
      - The lamp-eyes sit **on top of the front wings**, raised and close together, so they read as eyes from the side and the three-quarter view as well as the front.
      - Four short fat wheels with cream hubs, a short bumper-mouth, and a dark tinted windscreen set back.
      - A whip antenna with a green `#6fae4f` pennant replaces his scarf. It is the secondary spring chain and his telling detail.
      - Motion `zip`: tempo 1.4, bouncy suspension, quick starts with a squat and a nose lift, a little hop on surprise.
    - **Bruno, a big gentle train engine.** A long rounded "loaf" engine in brown `#8a5a35` and `#4e3423` on six wheels. It has no classic round smokebox front; the front is a flat, rounded-rectangle nose.
      - Two big cream lamp-eyes are low on the nose, on the buffer beam line, with heavy hoods (a sleepy, kind look).
      - A wide buffer-beam mouth sits between the two buffers.
      - A short chimney on top puffs, and a row of rounded roof vents nods to his hedgehog spines.
      - A small brass bell, and the whistle on the cab.
      - Motion `chug`: tempo 0.75, a heavy suspension that settles late, puffs in time with speed.
    - The two differ in silhouette (small and tall-round against long and low), main colour and scale. Pip is about 1.6 m long and 1.1 m high; Bruno about 4 m long and 2.2 m high.
11. **Sets for vehicles: paths and a road-and-rail kit.**
    - `cts.set3d/1` gains optional `paths: { <id>: { kind: "road" | "track", points: [[x, y], ...], width? } }`, so old sets parse.
    - New prop kinds: `road` (made from a path: asphalt strip with dashes), `track` (rails and sleepers along a path), `crossing` (a level crossing where a road path meets a track path: crossing boards, a static barrier and a sign), `platform` (a small station platform with a roof), `signal`, `buffer_stop`. Each has a footprint in `props.json`.
    - Lint:
      - `E_MARK_OFF_PATH`: a mark used by a vehicle move is more than 0.3 m from a path of the right kind.
      - `E_OFF_TRACK`: a train move whose two marks are not on the same track path.
      - `E_PATH_BLOCKED`: a path runs through a prop footprint.
    - Pilot 4 set: `crossing`, where a road and a track meet in a meadow with trees, bushes, a small house and the platform. Marks: `road_left`, `road_right`, `crossing_road` (just before the crossing), `track_left`, `track_right`, `platform`. Cameras: `wide`, `crossing`.
12. **Flow: none.** The pilot 3 intro and outro show the squirrel and the hedgehog, so they do not fit the vehicles. Pilot 4 runs with `options.skipClips: true` and a title card, and `flowCreditsCap` stays 0. A new Flow intro needs the user to ask, a new budget and `video-plan.mjs`.
13. **Kept from HUB-30 unchanged:**
    - the toon look (`style3d.json` defaults) and the inverted-hull outlines `#2b2118`;
    - the six visemes `rest A E O U MBP` at 24 fps, and the 18 dB music duck (floor 15) with the mix check;
    - the Blender 5.2 pin (`E_BLENDER_VERSION`) and the chunked EEVEE render;
    - the sheet pause, the client-task loop and the budget gate.
14. **The horn and the whistle are sounds.** `honk` and `whistle` animate the body, lamps and puff, and the writer pairs each with an `sfx` beat (`with: prev`). The script may use at most two SFX cues. The composer makes `music/sfx-horn.ogg` and `music/sfx-whistle.ogg` with MOSS-SoundEffect v2, which is installed in ComfyUI (`ComfyUI-Shared/models/TTS/moss_soundeffect_v2`). A missing SFX file is a lint warning and silence, never a failure.
15. **Free plan terms.** The ElevenLabs free plan has no commercial licence (the pricing page lists "Commercial License" from Starter up), and attribution is expected. The pilot is for the user's own viewing. The last title card carries "Glasovi: ElevenLabs" / "Voices: ElevenLabs", and the run log notes the plan and that the films are not for commercial use (open question 3).

## Files and modules to touch per repo

### flow-music-mcp (branch `FMM-17_elevenlabs-voices` from `master` `56cf836`)

- `src/flow/elevenlabs.ts` (new): key lookup through `env.ts`, the redactor, the `fetch` client (Node 24, no SDK, no new package), subscription and models reads, the voices list, `speak` with `with-timestamps`, the alignment-to-words function and the guard.
- `src/flow/local-tools.ts`: the tools `flow_elevenlabs_status` and `flow_elevenlabs_voices`; `flow_narrate` `engine` enum gains `elevenlabs`, plus the args `model?`, `voice_settings?`, `language?` and `timestamps?`; the result gains `words?`, `credits_estimate` and `remaining_after`.
- `src/flow/voice-pure.ts`: the pure parts (estimate, guard decision, alignment to words), so tests need no network.
- `.env.example`: `ELEVENLABS_API_KEY=` (empty) and `FLOW_MUSIC_MCP_ELEVEN_RESERVE`, with a comment that the user fills these in.
- `README.md`, `CLAUDE.md` (the free-tier rule, no key tool), `ROADMAP.md` rows FMM-17 and FMM-18.
- `test/elevenlabs.test.ts` (new; test 1).

### cartoon-studio (branch `CTS-30_vehicles-elevenlabs` from the tip of `CTS-18_blender-3d` **after HUB-30's checker passes**; the tip is read at the start, because a polish round may add commits)

- Voice: `src/engine/studios/flow.ts` (`elevenStatus`, `elevenVoices`, `narrate` with engine `elevenlabs`), `src/engine/voice/providers/elevenlabs.ts` (new speaker), `voice/allocate.ts`, `voice/run.ts` (probe, chain, words from alignment), `voice/audio.ts` (`leadTrimS`), `voice/tools.ts` (`cts_voice_quota` shows ElevenLabs; new `cts_voice_audition { series, cast, lang, provider: "elevenlabs", voiceIds, model?, text? }`), `voice/manifest.ts`, `seed/config/voice.md` (`elevenlabs: { model, reserve }`), `src/shared/contracts.ts` and `src/shared/media.ts` (`VOICE_PROVIDERS` gains `elevenlabs`, `voiceSpec.elevenlabs`, `wordsFrom`).
- Contracts and lint: `src/shared/contracts.ts` (`kind`, vehicle controls and block, the motion union, `cylinder`, `lamp`, set `paths`, new prop kinds, `MOVE_STYLES` gains `drive | zoom | reverse | chug`), `src/engine/series/lint.ts`, `src/engine/blender/library.ts` and `props.ts`, `docs/contracts.md` (`yarn docs:check`), and the fixture `tests/fixtures/mini-vehicles`.
- Blender: `blender/cts_blender/shapes.py` (cylinder part), `build_character.py` (wheels with hubs, lamp eyes with hood lids and glow, bumper mouth slots, chimney puff pool, antenna chain, the ray test against the body), `sheets.py` (vehicle motion strip), `build_set.py`, `props.json` (road, track, crossing, platform, signal, buffer stop; paths as curves), `acting/vehicle.py` (new), `acting/library.json` (`bodies`, vehicle actions), `acting/__init__.py` (registry), `acting/compose.py` and `springs.py` (antenna chain), `framing.py` (vehicle height and length), `assemble.py` (place on paths, puffs, lamp glow keys).
- Engine: `src/engine/anim/timeline3d.ts` (path moves, train limits, vehicle listening and talking automation), `src/engine/pipeline/handlers.ts` (writer facts by body, SFX pairing), and the prompts `seed/prompts/character-designer/character-spec.md` and `character-review.md`, `background-artist/set-spec.md`, `writer/script.md`, `frame-critic/frames-3d.md`, `voice-director/voice-cast.md`; `seed/style/toon-3d.md` (vehicle rules and the Pip-car and Bruno-engine example specs).
- App: `src/renderer/ui/CastPage.tsx` (shows the body kind and the ElevenLabs voice name and id per language), `SettingsPage` (the ElevenLabs line from `cts_voice_quota`: ready, tier, credits left, reset date).
- Docs: `README.md`, `ROADMAP.md` (CTS-30 to CTS-36), `docs/blender.md` (vehicles, paths, the new actions), `docs/mcp-guide.md`, `docs/pipeline.md`.

### creative-hub (branch `HUB-31_vehicles-voices` from `HUB-30_cartoon-3d`)

- `CLAUDE.md`: the voice-allocation bullet, replaced with the wording in open question 2, **only after the user approves it**.
- `.claude/skills/make-cartoon/SKILL.md`: vehicle bodies, the lamp-eyes rule, the road and rail kit, the vehicle action names, the ElevenLabs voice rule and key setup (the user does it), the quota read, auditions, and no Flow by default.
- `README.md` (the flow-music-mcp and cartoon-studio rows), `services.json` (the flow-music-mcp note: ElevenLabs engine, key in `ELEVENLABS_API_KEY` or `~/.flow-music-mcp/.env`), `ROADMAP.md` (a HUB-31 row only; row 22 of HUB-28 stays uncommitted and untouched; commit with `git add -p` or a patch that leaves it out).
- `runs/pip-bruno-wheels-pilot.md`, and in this folder `changelog.md`, `evidence/`, `events.jsonl`.
- The VN Studio and Edu Studio `ROADMAP.md` files each get one "Later" row: "ElevenLabs voices through flow-music-mcp `flow_narrate` engine `elevenlabs` (HUB-31)". These are docs only, one commit each on a ticket branch in that repo's style, or left to the user if they say so.

## Tickets

Order: FMM-17 then FMM-18. In parallel: CTS-31, then CTS-32, CTS-33 and CTS-34 (disjoint files after CTS-31). CTS-30 runs after FMM-18 (it codes against the FMM-18 contract with a fake client and can start once that contract is fixed). Then CTS-35 and CTS-36. Then pilot 4 (P, hub) and the checker (V). Workers run Node with `fnm exec --using default`, run Yarn per the memory note, keep scratch files in `.claude/temp/`, and end every item DONE, NOT DONE or UNTESTED. One commit per ticket.

### FMM-17. ElevenLabs client, key and status (flow-music-mcp)

- Inputs: decisions 1-4; ElevenLabs `GET /v1/user/subscription`, `GET /v1/models`, `GET /v1/voices`.
- Outputs:
  - `src/flow/elevenlabs.ts` and the pure parts;
  - `flow_elevenlabs_status` returning `{ ready, source, tier, used, limit, remaining, reserve, resetAt (ISO), paidRisk: bool, models: [{ id, tts, hr, en, multiplier }] }` (with no key: `{ ready: false, hint }`, and never an exception that carries the key);
  - `flow_elevenlabs_voices` returning `[{ voiceId, name, category, labels: { gender, age, accent, description } }]` (no preview downloads);
  - the `.env.example` lines and docs.
- Contract with CTS-30: the two tool result shapes above (the field names are fixed in `docs` and the tests).

### FMM-18. `flow_narrate` engine `elevenlabs` with timestamps and the guard (flow-music-mcp)

- Inputs: FMM-17.
- Outputs:
  - `flow_narrate { engine: "elevenlabs", text, voice: <voiceId>, model?, voice_settings?, language?, timestamps: true, out, name, format }`;
  - it calls `POST /v1/text-to-speech/{voice_id}/with-timestamps` with `output_format: "mp3_44100_128"` (allowed on the free tier) and converts with ffmpeg to the asked format;
  - result `{ file, durationSec, engine, voice, model, words: [{ w, t0, t1 }], characters, credits_estimate, remaining_after }`;
  - refusals `E_ELEVEN_QUOTA`, `E_ELEVEN_PAID_TIER`, `E_ELEVEN_LANG`, `E_ELEVEN_BLOCKED`, `E_ELEVEN_KEY` as tool errors with a readable message and no key;
  - 429 handled with backoff and requests made one at a time.
- Contract with CTS-30: the result shape and the error codes. `words` times are relative to the start of the returned file.

### CTS-30. ElevenLabs voice provider (cartoon-studio)

- Inputs: FMM-18 contract; decisions 5-7.
- Outputs:
  - `studios/flow.ts` methods and the `providers/elevenlabs.ts` speaker (the stop kinds `quota`, `down`, `unreadable` as the other speakers);
  - the allocation with ElevenLabs first, `voiceSpec.elevenlabs` in the bible, `wordsFrom` in the manifest, and `leadTrimS` with the shift;
  - `cts_voice_quota` returning `{ gemini: {...}, elevenlabs: { ready, tier, remaining, reserve, resetAt } }`;
  - `cts_voice_audition` (writes `cast/<id>/voice/audition-<lang>-<voiceId>.wav` and records credits in the run report);
  - `cts_voice_plan` showing the provider per language with the credit estimate and why;
  - spend entries in a new ledger currency `eleven-credits` (always USD 0);
  - `W_VOICE_MIXED` and `W_VOICE_ID_CHANGED`.
- Contract with CTS-35 and the pilot: a manifest line from ElevenLabs has `provider: "elevenlabs"`, `engine: <model>`, `voice: <voiceId>`, `words` (shifted), `wordsCoverage: 1`, `wordsFrom: "elevenlabs"`.

### CTS-31. Vehicle contracts, lint and the `mini-vehicles` fixture (cartoon-studio)

- Inputs: decisions 8, 9, 11.
- Outputs:
  - the contract changes in `contracts.ts` and `docs/contracts.md`;
  - `library.json` `bodies` (creature actions tagged, vehicle actions listed with seconds, `overLine`, `needsTarget`, params; Python registry stubs for the new names so B2's name check passes from this ticket on);
  - lint `E_VEHICLE_LIMB`, `E_ACTION_BODY`, `E_MARK_OFF_PATH`, `E_OFF_TRACK`, `E_PATH_BLOCKED`;
  - the fixture `tests/fixtures/mini-vehicles`: one car, one train, a small crossing set, a 4-beat script with a drive, a chug, a honk with an SFX beat and a react, and fake voice manifests (one with `wordsFrom: "elevenlabs"`).
- Contract with CTS-32 to CTS-35: the zod types and the action names.
- Done when: `mini`, `mini3d`, `mini-vehicles` and the real `pip-bruno-3d` data lint to 0 errors.

### CTS-32. Vehicle builder and sheet (cartoon-studio)

- Inputs: CTS-31; decision 10.
- Outputs:
  - `build_character.py` for `kind: vehicle`: cylinder wheels with hubs and outlines, each on a `wheel_<n>` control with its spin axis; lamp eyes (eyeball, hood lid, pupil, emission glow keyed by `lamp_glow`); bumper-mouth slot objects; a chimney puff pool (8 cloud ellipsoids, hidden at rest); the antenna chain; the face ray test against the body and front block (`E_FACE_HIDDEN`).
  - `sheets.py` motion strip for vehicles: squash, stretch, lean left and right, nose up, honk or puff.
  - the designer prompt with the lamp-eyes rule and the "not like" list (no windscreen eyes, no smokebox face, no human nose or cheeks);
  - `seed/style/toon-3d.md` vehicle section with the Pip-car and Bruno-engine example specs.
- Contract with the pilot: `cast/<id>/character.blend`, `sheet.png`, `build.json` (as HUB-30).

### CTS-33. Road and rail set kit (cartoon-studio)

- Inputs: CTS-31; decision 11.
- Outputs:
  - `build_set.py` paths as Blender curves (named `path:<id>`, read by the assembler);
  - the props `road`, `track`, `crossing`, `platform`, `signal`, `buffer_stop` in `props.json` and the builder;
  - the set sheet showing the paths;
  - the background-artist prompt (vehicle marks on paths; a crossing where road meets track).
- Contract with CTS-34 and CTS-35: path curves in `set.blend`, and `marks` that lie on paths.

### CTS-34. Vehicle acting library (cartoon-studio)

- Inputs: CTS-31; the HUB-30 principles (anticipation, easing, overlap, moving holds, springs, tempo) applied to vehicle bodies.
- Outputs: `acting/vehicle.py` with these actions:
  - **Auto:** `idle_engine` (a fine suspension bob and engine shiver; Bruno's slow breathing puff), `blink` (the lamp hoods), `look_at` (pupils lead, then the front block yaw and pitch within limits; a car's body turns only when stopped and past 60 degrees; a train never yaws), plus the listening and talking automation (front-block accents on word onsets, lamp-hood lifts, a lean toward the speaker).
  - **Locomotion along paths:**
    - `drive`: anticipation is a rear squat; the nose lifts on start; wheel spin equals distance over radius; the body rolls into turns; on braking the nose dips with a damped rock.
    - `zoom`: fast; stretch along travel; a puff from the exhaust at the start.
    - `reverse` and `turn` (car only: a short arc on the ground).
    - `chug` (train only, on the track: slow start with puffs every n metres tied to speed, a heavy late settle).
  - **Gestures and reactions:** `nod` (front dips on the suspension), `shake_head` (front-block yaw wiggle), `bounce` (happy, wheels leave the ground), `lean` (toward a target), `tilt` (a quizzical roll, the "think"), `wiggle` (a rear wiggle, the "cheer"), `rev` (squash and shiver plus an exhaust puff), `honk` (front squash and stretch plus a lamp flash; car), `whistle` (chimney stretch plus a big puff; train), `puff`, `flash` (both lamps) and `wink` (one hood), `point_nose` (aim the front at a target, with a small lunge and a lamp flash), `spin_wheels` (wheelspin in place), `park` (settle, engine off, half hoods) and `start_up` (shiver, hoods open, puff), `droop`, `react_surprised` (a jump with wheels off the ground, a stretch, wide lamps, a puff), `laugh` (a suspension shake, squinting hoods).
  - **Camera:** unchanged.
  - an acting reel of `mini-vehicles` at preview size, read by the worker, with what looks wrong written down.
- Contract with CTS-35: action names equal `library.json` (test B2v); each action keys only the controls in its `parts`.

### CTS-35. Timeline, assembly, pipeline and app for vehicle series (cartoon-studio)

- Inputs: CTS-30 to CTS-34.
- Outputs:
  - `timeline3d.ts`: moves follow a path when both marks are on it; a train is held to its track; `drive | zoom | reverse | chug` styles; a gesture length within min and max.
  - `assemble.py`: places vehicles on path marks facing along the path; wheels on the ground plane or the rail height; puffs; lamp glow keys.
  - writer facts filtered by body; the writer prompt pairs `honk` and `whistle` with an `sfx` beat.
  - the frame-critic checks: wheels touch the road or rails; no wheel slide; the face is visible in close-ups; the lamp-eyes rule is kept.
  - the bible accepts vehicle cast; the Cast and Settings views (above).
  - `cts_run_pipeline` on `mini-vehicles` with the mock provider, the fake Blender runner and a fake ElevenLabs flow client reaches `done` (the existing pipeline test pattern).
- Contract with the pilot: the step list of HUB-30 is unchanged; `voice` now allocates ElevenLabs first.

### CTS-36. Docs and roadmap (cartoon-studio)

- `README.md` (vehicles, ElevenLabs through flow-music-mcp), `ROADMAP.md` rows CTS-30 to CTS-36, `docs/blender.md`, `docs/mcp-guide.md`, `docs/pipeline.md`. Plus the A3-style grep (C3).

### P. Pilot 4 (hub session, through the skill, after CTS-35)

See the next section.

### V. Checker (director-checker, fresh context)

Checks C1-C18 against this plan and the run log.

## Pilot 4 steps with user checkpoints

0. **Before.**
   - **The user** creates the ElevenLabs free account and API key and puts the key in `ELEVENLABS_API_KEY` or `~/.flow-music-mcp/.env`. The agent asks for this and waits, and never asks for the key in chat.
   - Build and start flow-music-mcp from `FMM-17_elevenlabs-voices` with `hub.ps1 build/start flow-music-mcp`. Build and start Cartoon Studio from `CTS-30_vehicles-elevenlabs`. Start ComfyUI, comfy-mcp and VibeTTS. Do not start Scriptorium, Chiptune Studio or Strata.
   - Run `cts_blender_status` (5.2.x, GPU named) and `flow_elevenlabs_status` (`ready`, `tier: free`, `paidRisk: false`, remaining and reset, models reading hr and en). Record all of this in the run log.
   - Run `cts_budget_set { series: "pip-bruno-wheels", episode: "ep00-pilot", capUsd: 0, flowCreditsCap: 0, approvedBy: "user", note: "pilot 4, ElevenLabs free tier only, no Flow" }`.
   - Record a hash list of the `out/*.mp4` files of `pilot`, `pip-bruno` and `pip-bruno-3d` (C14).
1. **Bible.** `cts_run_pipeline { series: "pip-bruno-wheels", episode: "ep00-pilot", brief: { pitch: <p1 from pip-bruno-3d, rewritten for a car and a train: Pip the quick little car and Bruno the slow kind engine solve one small puzzle at the crossing>, ages 4-8, seconds 60, lineRange [12, 16] }, options: { renderer: "blender", skipClips: true } }`. The palette is kept from pilot 3.
2. **Character specs and sheets, then a PAUSE (checkpoint 1).**
   - The designer writes the vehicle specs from the `toon-3d.md` examples (decision 10), builds them and self-reviews (at most 2 revisions).
   - Claude checks the lamp-eyes rule and the "not like" list on each sheet and writes the result in the run log.
   - Show both `sheet.png` files in chat and in the Cast view, and **wait for approve or redo per character**. Nothing else is built before both are approved.
3. **Set.** `crossing` (decision 11). Build it and read its sheet.
4. **Script and safety.**
   - 12-16 lines in hr and en, at most 12 words a line.
   - At least 8 distinct vehicle actions, including a `drive` of at least 5 m on the road, a `chug` on the track, `honk` and `whistle` each with an SFX beat, a `react_surprised`, a `laugh`, and one `push` or `pan`.
   - No creature action (lint `E_ACTION_BODY`). A title card at the end carries the ElevenLabs credit (decision 15).
   - Safety must pass.
5. **Voice auditions, then a PAUSE (checkpoint 2).**
   - Run `cts_voice_quota` (record the ElevenLabs remaining credits before).
   - `flow_elevenlabs_voices` gives the premade voices. The voice director proposes 3 candidates per character from their labels: Pip bright, quick and young-sounding; Bruno deep, warm and slow.
   - `cts_voice_audition` speaks one line of each character in hr and en per candidate with `eleven_multilingual_v2`, plus Bruno's and Pip's hr line once with `eleven_flash_v2_5` and `language: "hr"`. That is about 14 clips of 40-60 characters, about 800 credits.
   - Give the user the file paths (and open them). **Wait for the pick per character per language and the hr model choice.**
   - Write the voice ids, names, model and settings to the bible and the run log.
6. **Voices.**
   - `cts_voice_plan` must show hr and en on ElevenLabs with an estimate inside `remaining - reserve` (with about 1,400 characters for 13 lines a language, both fit). If one does not fit, the rule applies (hr first, the other language to Gemini or local) and the run log says so.
   - `cts_voice_generate`, then `cts_voice_quota` again (record the credits after, and the delta against the estimates).
   - Every ElevenLabs line has `wordsFrom: "elevenlabs"`. Fallback lines use whisper.
7. **Music and SFX.** The ComfyUI ACE-Step theme (40 s, soft) and MOSS `sfx-horn` and `sfx-whistle`. Record the seeds and wall times.
8. **Timeline, assembly, preview, frame review, finals.**
   - Lint 0 errors, then assemble per language, then preview per language with the times.
   - Frame review of the 12-frame contact sheets against the sheets: on model, wheels on the road and rails, no wheel slide, a train never off its track, face visible in close-ups, mouth shut in silence, lamps on the speaker, framing. Up to 2 rounds; fixes are data edits by the owning role.
   - The 1080p finals in hr and en with `mix-check.json`.
9. **PAUSE: the user watches (checkpoint 3)** `out/hr.mp4` and `out/en.mp4`. Ask for a verdict on the vehicle look, the acting, the ElevenLabs voices in hr and en, the lip-sync and the music level, and for GO or NO-GO.
10. **Run log and evidence.** `runs/pip-bruno-wheels-pilot.md` gets every id, time, credit count before and after, decision, measurement and verdict, plus the UNTESTED items. Evidence goes in `.claude/tickets/HUB-31-vehicles-voices/evidence/`, and the changelog in this folder.

## Acceptance criteria

| # | Criterion | Check that proves it |
|---|---|---|
| C1 | Builds and tests pass | flow-music-mcp `yarn build && yarn test` (exact scripts from its `package.json`); cartoon-studio `yarn typecheck && yarn lint && yarn test && yarn test:blender && yarn test:e2e && yarn build && yarn docs:check`; all exit 0 on the ticket branches (outputs in the changelog) |
| C2 | The key never leaks | the key is held only in the env var or `~/.flow-music-mcp/.env`. `rg -c -F "$ELEVENLABS_API_KEY"` (prints counts only) over the three repos' working trees, `git log -p` of the three branches, `runs/`, `logs/`, `~/CartoonStudio/**/logs`, `~/.flow-music-mcp/logs` and the run log gives 0 matches. Test 1c passes. `flow_elevenlabs_status` shows only `ready` and `source` |
| C3 | Public repos clean | the A3-style `git grep -nE "C:\\\\Users\|Infplane\|sk_[A-Za-z0-9]{20,}\|AIza"` on `CTS-30_vehicles-elevenlabs` and `FMM-17_elevenlabs-voices` returns nothing |
| C4 | Quota read and refused past it; $0 | test 1a (refusal with no TTS request for over-quota and for a non-free tier); the run log has `flow_elevenlabs_status` before and after (tier `free`, used, remaining), and the credits used are no more than remaining minus reserve before the run; `spend.json` has no `usd` entry and `eleven-credits` entries that sum to within ±10 % of the API delta; `budget.json` `capUsd 0`, `flowCreditsCap 0`; no Flow request in the logs |
| C5 | Croatian support named | the run log records the model used for hr and en and the `flow_elevenlabs_status` models entry showing `hr: true` for it (expected `eleven_multilingual_v2`, or `eleven_flash_v2_5` if the user picks it in checkpoint 2) |
| C6 | Voices fixed per character | the bible has `voice.hr.elevenlabs.voiceId` and `voice.en.elevenlabs.voiceId` for `pip` and `bruno`, equal to the manifest `voice` of every ElevenLabs line and to the run log; the user's pick in checkpoint 2 is logged with its time |
| C7 | Visemes from ElevenLabs times | every ElevenLabs line has `wordsFrom: "elevenlabs"`, `wordsCoverage: 1`, and its first word starts within 0.25 s of the clip start (shift applied); test 3 passes; lint: at least 60 % non-rest frames, at least 3 distinct visemes, `MBP` on labial lines, no `E_MOUTH_SILENT` or `W_VISEME_FLAT`; fallback lines show method and whisper alignment in the run log |
| C8 | No arms, no legs | both `character.json` files have `kind: "vehicle"` and no `arm_*`, `hand_*` or `leg_*` control; `assembly.json` lists only actions whose `bodies` include `vehicle`; lint has no `E_ACTION_BODY` or `E_VEHICLE_LIMB` |
| C9 | Original look | Claude's sheet check in the run log: eyes are the front lamps (Pip on the wings, Bruno on the buffer beam), the mouth is the bumper or buffer-beam slot, no eyes in a windscreen or window, no face on a round smokebox door, no nose; frame-critic `pass` on the same points; the user approved both sheets (C15) |
| C10 | Vehicle acting sound | B2v passes (wheel roll equals distance, wheels on the ground, train on the track, gestures settle); `assembly.json` has at least 8 distinct vehicle actions including `drive` (at least 5 m), `chug`, `honk`, `whistle`, `react_surprised`, `laugh` and a `push`/`pan`; Claude's frame review notes no wheel slide or floating wheels |
| C11 | Road and rail set | `sets/crossing/set3d.json` has a `road` and a `track` path that cross at the `crossing` prop; every vehicle mark is on a path; lint 0 errors; the set sheet is in the evidence |
| C12 | HUB-30 kept | the toon look and outlines are visible in the stills; six visemes; `mix-check.json` hr and en `minUnderDb >= 15`, `medianUnderDb >= 17`, integrated -16 ±2 LUFS; `cts_blender_status` 5.2.x |
| C13 | Both films | `out/hr.mp4` and `out/en.mp4`: h264 1920x1080, 24 fps, yuv420p plus aac, 50-75 s; `cts_lint` 0 errors |
| C14 | Older pilots unharmed | before and after hash lists of the `out/*.mp4` of `pilot`, `pip-bruno` and `pip-bruno-3d` are equal; `cts_lint` 0 errors on their `ep00-pilot`; a 2 s preview of `pip-bruno-3d` renders on the new build |
| C15 | Sheets before sets | run log: `cts_sheet_approve` for both vehicles earlier than the first `set3d` job in `jobs/done/` |
| C16 | Hub wiring | the skill, README, `services.json`, the ROADMAP HUB-31 row and the run log on `HUB-31_vehicles-voices` (`git diff --stat`); the HUB-28 files are not in any HUB-31 commit; CLAUDE.md changed only with the wording the user approved (their words and time in the run log) |
| C17 | The user watched | the run log records the user's verdict on hr and en (look, acting, voices, lip-sync, music) and GO or NO-GO |
| C18 | Reusable engine | `hub.ps1 call flow-music-mcp flow_elevenlabs_status '{}'` answers from outside Cartoon Studio (evidence file), so VN Studio and Edu Studio can use it later without new client code |

Every item ends DONE, NOT DONE (with the reason) or UNTESTED in `changelog.md`.

## Tests (few, important only)

1. **`flow-music-mcp test/elevenlabs.test.ts`** (fake `fetch`):
   - (a) over-quota (`estimate > remaining - reserve`) and a non-free tier are refused with `E_ELEVEN_QUOTA` and `E_ELEVEN_PAID_TIER`, and no TTS URL is requested;
   - (b) an alignment of "Bruno, čekaj malo!" gives three words with the right times, punctuation dropped and `č` kept;
   - (c) a 401 whose body echoes a fake key gives an error, a log line and a result in which the fake key does not appear.
2. **`cartoon-studio tests/voice-allocate.test.ts`** (one added case): with the ElevenLabs remaining credits fitting only hr, hr goes to ElevenLabs and en goes to Gemini when it fits, else local; with 0 credits the old rule results are unchanged.
3. **`cartoon-studio` voice words shift** (added to the existing voice or visemes test): a generated WAV with 0.4 s of leading silence and ElevenLabs words starting at 0.42 s is normalised; the stored words start at about 0.17 s (0.42 - 0.4 + 0.15 kept), within the clip, with `wordsCoverage` 1.
4. **B1v `blender/tests/test_build.py`** (one case): the `mini-vehicles` car builds with its wheel controls, lamp eyes, six mouth slots and outlines, and no arm or leg control; a lamp buried in the body gives `E_FACE_HIDDEN`.
5. **B2v `blender/tests/test_acting.py`** (cases added):
   - registry names equal `library.json` including `bodies`;
   - in a 5 m `drive`, wheel rotation times radius equals the root path length within ±2 %, and each wheel bottom stays within 1 cm of the ground outside jump actions;
   - in a `chug`, the wheel centres stay within 1 cm of the track path sideways;
   - `honk` and `bounce` return to rest.
6. **Updated, not new:**
   - `tests/contracts.test.ts`: `mini-vehicles` parses; a vehicle with `arm_L` fails `E_VEHICLE_LIMB`; `wave` on a vehicle fails `E_ACTION_BODY`; a train move off its track fails `E_OFF_TRACK`; the pilot 3 bible and specs still parse.
   - `tests/blender.e2e.test.ts` renders a 2 s `mini-vehicles` preview instead of adding a new e2e.
   - The pipeline test runs `mini-vehicles` to `done` with a fake ElevenLabs client.

## Downloads and costs

- **Downloads: none expected.** The ElevenLabs client uses Node's `fetch`, with no SDK or npm package. Whisper models are already in `~/.flow-music-mcp/models`. Blender 5.2 is installed. MOSS-SoundEffect v2 and ACE-Step are installed in ComfyUI. No voice preview files are fetched. If a worker finds that something must be downloaded, it stops and asks with the file name, source and size.
- **The account and key:** made by the user on elevenlabs.io (free plan). The agent never visits the sign-up page, types anything there or handles the key.
- **ElevenLabs credits (free plan, 10,000 a month, about 10 minutes; read live before the run):**

  | Item | Estimate |
  |---|---|
  | Auditions | about 14 clips x 50 characters, about 800 credits |
  | Episode voices | about 13 lines x 55 characters x 2 languages, about 1,400 credits at 1 credit a character |
  | Redos (reserve) | about 600 credits |
  | **Total** | **about 2,800 credits**, under a third of the month |

  The engine refuses anything past `remaining - 200`.
- **USD: $0** (`capUsd 0`, free tier enforced by `E_ELEVEN_PAID_TIER`). **Flow credits: 0.** Gemini: not used if ElevenLabs fits; it would count against the 10 a day.
- **Local compute:** Blender renders as in pilot 3 (about 0.2 s a frame at 1080p, about 5.5 min per language final), ComfyUI music and SFX in under a minute.

## Open questions for the user (as few as possible)

1. **Where the voices come from.** ElevenLabs' own docs say "The voice library is not available via the API to free tier users". So the shared community Voice Library is out at $0. The choices:
   - (a) ElevenLabs' default (premade) voices, which free API users can use, auditioned per character;
   - (b) Voice Design: a voice made from a text description, kept in 2 of the 3 free custom-voice slots, which costs credits per design.

   **Recommendation: (a).** It costs no credits to set up, the ids are stable across episodes, and you pick by ear in checkpoint 2. (b) stays available later if no default voice fits Pip.
2. **The new CLAUDE.md voice rule.** Approve this wording, which replaces the current "Voice allocation" bullet. **Recommendation: approve as written.**

   > - Voice allocation (ElevenLabs free tier, Google Voice Gemini TTS, local voices): languages are allocated whole, Croatian first, then English. (1) ElevenLabs free tier, about 10,000 credits a month: read the remaining credits from the API before every run; a language whose lines fit in what is left goes to ElevenLabs. Never a paid plan, never past the free quota, never a paid-only endpoint or format. The user alone creates the account and the API key and puts the key in the `ELEVENLABS_API_KEY` environment variable or `~/.flow-music-mcp/.env`; it never appears in a repo, a log, a run log or a commit. It is called through flow-music-mcp (`flow_narrate` engine `elevenlabs`); today only Cartoon Studio uses it. Keep each character's ElevenLabs voice id in the series bible and reuse it in every episode. (2) Gemini TTS free tier, 10 requests a day: a language that does not fit in ElevenLabs goes to Gemini if its lines fit in today's remaining requests. (3) Otherwise the language goes to the local voices (VibeTTS; in Cartoon Studio Croatian is OmniVoice through ComfyUI first, Supertonic through VibeTTS as the fallback). If both languages are needed and together exceed a free quota, Croatian takes the free cloud voice and English moves to the next step down.
3. **Free plan terms.** The free plan is for non-commercial use and expects attribution. The pilot films are for you to watch, and the end card says "Glasovi: ElevenLabs" / "Voices: ElevenLabs". **Recommendation: yes, keep pilot 4 non-commercial with the credit line.** A plan with a commercial licence would be a paid decision for later.
