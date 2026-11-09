# HUB-31 changelog

## 2026-11-09 (later) — pushed to master, follow-up fixes, pilot 4 re-rendered with sound effects

The user asked: "push all to master and do all fixes you recommend".

- **Pushed (fast-forward, no force):** creative-hub `HUB-31_vehicles-voices` → master (68cfe38..dc508b8); cartoon-studio `CTS-30_vehicles-elevenlabs` → master (e0aa146..d73c6c6); flow-music-mcp `FMM-17_elevenlabs-voices` → master (56cf836..a26d383). Branches pushed too.
- **flow-music-mcp `FMM-19_gemini-key-lookup`** → master (a26d383..0159583): `2f9988f` the Gemini key uses the same lookup as ElevenLabs (shared `keyFromEnv`), so an empty `GEMINI_API_KEY=` in the repo `.env` no longer hides the real key; `0159583` an empty value in any `.env` file no longer hides a later file's value. typecheck, build, test (158) pass; server restarted, ElevenLabs still ready.
- **cartoon-studio `CTS-37_pilot4-fixes`** → master (d73c6c6..0dbd024): CTS-37 `voice_review` gate + `cts_voice_approve` + ElevenLabs auditions in the pipeline; CTS-38 budget before series (`seriesExists` = has a bible); CTS-39 one revise job per pipeline; CTS-40 viseme gap bridging (en l12 52 % → 66 %); CTS-41 car turn ends on the path, antenna no longer pins, vehicle wide shot rises when occluded, `Actor.reset()`, opt-in lead measure, visor ray-test warning; CTS-42 docs. typecheck, lint, test (56), test:blender (21), test:e2e (2), build, docs:check all exit 0; creature output identical; engine rebuilt and restarted.
- **VN Studio `VNO-65_elevenlabs-later`** → master (9598d32..aa42b60) and **Edu Studio `EGS-63_elevenlabs-later`** → master (46b6ec1..376f3e8): one Later row each (done in temporary worktrees; their local checkouts untouched).
- **ComfyUI sound effects (local edits to third-party code, not in any of the user's repos):** `custom_nodes/comfyui_fill-chatterbox/chatterbox_node.py` (`patched_torch_load` no longer adds `map_location` when it was passed positionally) and `C:/projects/Public/TTS-Audio-Suite/.../diffsynth/pipelines/wan_audio.py` (`torch.compile` only when Triton imports). Originals kept in `creative-hub/.claude/temp/`. A node update can undo them.
- **Hub:** make-cartoon skill knows the `voice_review` pause and `cts_voice_approve`; run log section "Fixes after GO"; discoveries gains the stale-final-after-resume entry.
- **Pilot 4 redo:** music step with the same seed made `sfx-horn` and `sfx-whistle`; sound beats restored; new finals hr 74.167 s / en 72.042 s, -16.1 / -16.2 LUFS, horn audible (peak -1.5 dB), whistle quieter (peak -15.9 dB); lint 0 errors 0 warnings; C14 still equal. No credits spent.

| Item | Status |
|---|---|
| Push HUB-31 / CTS-30..36 / FMM-17..18 to master | DONE |
| FMM-19 Gemini key and empty .env values | DONE (live Gemini call UNTESTED) |
| CTS-37 voice review gate, ElevenLabs auditions | DONE (live pause UNTESTED; fakes only) |
| CTS-38, CTS-39, CTS-40, CTS-41, CTS-42 | DONE |
| VN Studio / Edu Studio roadmap rows | DONE |
| ComfyUI MOSS sound effects | DONE (local third-party edits) |
| Horn and whistle in pilot 4 | DONE; whistle is quiet, the user has not watched the redo yet: UNTESTED by the user |
| W_VISEME_FLAT | DONE (0 warnings) |
| C4 ledger vs API mismatch | NOT DONE (the API counter reset; nothing to fix in code) |
| Desktop app Cast/Settings and voice review button | UNTESTED; the studio UI has no voice-review button (discovery) |
| Cancel stale jobs on retry | NOT DONE (new discovery, found during the redo) |

Commit status: everything above is committed and pushed to master except the hub's last commit, which this entry is part of (pushed right after).

## 2026-11-09 — HUB-31: ElevenLabs voices and vehicle characters, pilot 4 made (user GO)

The ElevenLabs engine is in flow-music-mcp, Cartoon Studio puts ElevenLabs first in its voice allocation, vehicles are a body kind of the 3D route, and pilot 4 "Pip and Bruno at the Crossing" was made in hr and en with Liam (Pip) and Brian (Bruno). Cost: $0, 0 Flow credits, free ElevenLabs credits only. The user approved the sheets after three rounds, picked the voices, and gave GO on the films. Request REQ-0022; the director's checker (C1-C18) runs next.

### flow-music-mcp — branch `FMM-17_elevenlabs-voices` (from `master` 56cf836)

- `src/flow/elevenlabs.ts` (new):
  - The key is looked up in this order: env `ELEVENLABS_API_KEY`, then env `ELEVEN_CREATOR_KEY`, then the `.env` files (the repo's, then `~/.flow-music-mcp/.env`). The files are parsed directly, so an empty line cannot hide a real key.
  - A redactor replaces the key with `[key]` in every error, log line and result.
  - A fetch client sends the key only as the `xi-api-key` header. Requests go one at a time through a serial queue, and a 429 is retried 3 times (Retry-After, or 1, 2 and 4 s).
  - It reads the subscription, the models (cached 10 min) and the voices; previews are never downloaded.
  - `speak` calls `with-timestamps` with `mp3_44100_128`, then ffmpeg converts the result (same chain as the Gemini engine).
- `src/flow/voice-pure.ts`: the pure parts:
  - error codes and `redactKey`;
  - estimate `ceil(chars x multiplier)`;
  - a guard that refuses `E_ELEVEN_QUOTA` (estimate > remaining - reserve), `E_ELEVEN_PAID_TIER` (tier not free, or can extend its limit) and `E_ELEVEN_LANG`;
  - API error mapping (`E_ELEVEN_KEY`, `E_ELEVEN_BLOCKED`, `E_ELEVEN_MODEL`, `E_ELEVEN_API`);
  - alignment to words (`č` and the other Croatian letters kept).
- `src/flow/local-tools.ts`:
  - New tools `flow_elevenlabs_status` (`{ready, source, tier, used, limit, remaining, reserve, resetAt, paidRisk, models[{id, tts, hr, en, multiplier}]}`) and `flow_elevenlabs_voices`.
  - `flow_narrate` engine `elevenlabs` (`model`, `voice_settings`, `language`, `timestamps`) returns `words`, `characters`, `credits_estimate`, `remaining_after`.
  - No tool sets the key.
- `src/env.ts`: `presetEnv`, a snapshot of the environment taken before the `.env` files load, so `source` can be told.
- `.env.example`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `ROADMAP.md`: user setup, the free-tier rule, the no-key-tool rule, and rows FMM-17 and FMM-18.
- `test/elevenlabs.test.ts` (new): test 1a (refusals send no TTS request), 1b (word times of "Bruno, čekaj malo!"), 1c (the key appears in no error, log or result).
- Commits: `4baea13` FMM-17, `c7fa68b` FMM-18, `a26d383` FMM-17 fixup for `ELEVEN_CREATOR_KEY` (a director-approved contract fix after the user stored the key under that name).

### cartoon-studio — branch `CTS-30_vehicles-elevenlabs` (from `CTS-18_blender-3d` e0aa146), 74 files, +4661 / -311

- **CTS-31 `954796c`, contracts and lint:**
  - `kind: creature | vehicle`, vehicle controls and the `vehicle` block, a motion union with `drive`, `cylinder`, lamp eyes;
  - set `paths` and the prop kinds road, track, crossing, platform, signal and buffer_stop;
  - `MOVE_STYLES` adds drive, zoom, reverse and chug;
  - lint `E_VEHICLE_LIMB`, `E_ACTION_BODY`, `E_MARK_OFF_PATH`, `E_OFF_TRACK`, `E_PATH_BLOCKED`;
  - `library.json` gains `bodies` and `vehicleTypes`, plus the `mini-vehicles` fixture.
- **CTS-33 `55fb8c6`, road and rail kit:**
  - `path:<id>` curves with their surface heights (road 0.012, rail top 0.2), recorded in `build.json`;
  - builders for road, track, crossing (boards, ramps, barrier, sign), platform, signal and buffer_stop;
  - a plan row on the set sheet;
  - `E_SET_INVALID` for a kind with no builder;
  - background-artist prompt, test B3.
- **CTS-30 `68b81a5`, ElevenLabs voice provider:**
  - `providers/elevenlabs.ts`, and allocation by whole languages, Croatian first: ElevenLabs, then Gemini, then local;
  - `voiceSpec.elevenlabs` in the bible, `wordsFrom` in the voice manifest;
  - `leadTrimS` and `shiftWords`, so the ElevenLabs word times follow the trimmed lead silence;
  - `cts_voice_quota` shows ElevenLabs, new `cts_voice_audition`, `eleven-credits` in the spend ledger;
  - warnings `W_VOICE_MIXED`, `W_VOICE_ID_CHANGED`; tests 2 and 3.
- **CTS-32 `b44417c`, vehicle builder and sheet:**
  - wheels with hubs and spin axes; lamp eyes (lens, pod, hood lid, pupil, a glow driver on `head["lamp_glow"]`, visors);
  - bumper-mouth slots, puff pools, the antenna chain, the ray test;
  - the vehicle motion strip on the sheet;
  - designer and review prompts with the lamp-eyes rule, the `toon-3d.md` vehicle section, test B1v.
- **CTS-34 `36bb7f8`, vehicle acting library:**
  - every vehicle action (path locomotion with wheel roll = distance / radius, chug puffs, gestures and reactions, look and listen limits);
  - shared actions branch on the body kind, and creature channels are byte-identical to before;
  - glow and puff writers in compose, springs for the antenna, test B2v.
- **CTS-35 `db4474f`, timeline, assembly, pipeline and app:**
  - path moves, trains held to their track, vehicle durations;
  - `assemble.py` places vehicles on path surfaces and handles the crossing rise, puffs and lamp glow; `framing.py` frames vehicles;
  - writer facts by body, honk and whistle paired with sfx, `brief.credits`, `W_SFX_MISSING`;
  - the voice cast gets the premade ElevenLabs voices;
  - Cast and Settings views; the pipeline and e2e tests run on `mini-vehicles`.
- **CTS-36 `d73c6c6`, docs and roadmap:** README, ROADMAP CTS-30 to 36, `docs/blender.md`, `docs/mcp-guide.md`, `docs/pipeline.md`.

### creative-hub — branch `HUB-31_vehicles-voices` (from `HUB-30_cartoon-3d` 68cfe38)

- `scripts/hub.ps1` (`b6bd265`): `start flow-music-mcp` copies a user-scope ElevenLabs key into that service's environment only, and prints only whether a key is set.
- `.claude/skills/make-cartoon/SKILL.md`, `README.md`, `services.json`, `ROADMAP.md` (HUB-31 row) (`5f672dc`):
  - vehicles, the lamp-eyes rule, the road and rail kit, the vehicle actions;
  - the ElevenLabs voice rule and key setup, quota reads, auditions with the hold on the voice-cast task;
  - `skipAuditions`, `brief.credits`, no Flow by default.
  - The uncommitted acp-proxy edits and HUB-28's row 22 were left out of the commit.
- In the final commit:
  - `CLAUDE.md`: the voice-allocation bullet is replaced with the plan's wording plus the amended key sentence;
  - `runs/pip-bruno-wheels-pilot.md`;
  - this folder's `changelog.md`, `evidence/`, `discoveries.md`, `attention.md`, `events.jsonl`, plan front matter;
  - the ROADMAP HUB-31 status.

### Deviations and decisions made during the work

- **Key name.** The user stored the key as `ELEVEN_CREATOR_KEY`. The director approved adding it to the lookup (fixup commit `a26d383`) and the `hub.ps1` registry pass-through. The user approved the amended CLAUDE.md key sentence ("Yes, add it", relayed by the director), then confirmed in this session ("Yes, write it").
- **Key permissions.** The first status call got 401 `missing_permissions` (user_read). The user widened the key's permissions (attention A-001).
- **Sheets, three rounds.**
  - Pip went from round 1 (pebble) to round 2 (flat box, cheeks removed, lamps out of the front) to round 3 (shorter).
  - Bruno went from round 1 to round 2 (shorter, no gap between boiler and cab, flat top with the chimney, roof vents removed).
  - "checks" was read as "cheeks", and "shorter" as length. Approved: "all good, we can adapt them at later point if series are ok".
- **Set layout.** The road runs front to back and the track left to right, unlike the plan's sketch, so the train never stands between the default camera and the road. The car marks are therefore `road_near`/`road_far`.
- **Voices.** Picked at checkpoint 2: "Liam + Brian, multilingual". `eleven_multilingual_v2` is used for both languages.
- **Frame review round 1.** Fixed as data: a `pip_close` camera, `crossing_road` 4 m from the track, the oak and the platform moved.
- **SFX.** The ComfyUI MOSS-SoundEffect node failed, so the pipeline dropped the sfx beats and the honk and whistle are silent (plan decision 14 allows this).
- **CTS deviations accepted:**
  - a prop `path` field and `vehicleTypes` (CTS-31);
  - the plan view drawn from `build_set.py` (CTS-33);
  - an `episode` argument on `cts_voice_audition` (CTS-30);
  - the `core.py` hooks (CTS-34 and 35);
  - fixture fixes.
- **Extra error codes:** `E_ELEVEN_MODEL` and `E_ELEVEN_API` beyond the plan's list.

### Verification

Ran and passed:
- **flow-music-mcp:** `yarn typecheck`, `yarn build`, `yarn test` (12 files, 157 tests) after each commit, including after `a26d383`.
- **cartoon-studio**, final run after CTS-36:
  - `yarn typecheck`, `yarn lint`, `yarn test` (53 tests), `yarn test:blender` (20 OK, Blender 5.2.2), `yarn test:e2e` (2), `yarn build`, `yarn docs:check` (19 examples, 0 problems): all exit 0.
  - Logs are in `.claude/temp/CTS-35/final/`.
- **`hub.ps1`:** parses with 0 errors. `hub.ps1 start flow-music-mcp` printed "ElevenLabs key in environment: set".
- **C18:** `hub.ps1 call flow-music-mcp flow_elevenlabs_status '{}'` answered `ready: true, tier: free, paidRisk: false` (`evidence/c18-status-call-2-ready.txt`).
- **Pilot 4:**
  - All 28 lines are ElevenLabs, with `wordsFrom: "elevenlabs"`, `wordsCoverage: 1`, and the first word at 0.00 s.
  - Finals hr 74.167 s and en 72.042 s: h264 1920x1080 24 fps yuv420p plus aac. Loudness -16.1 and -16.2 LUFS.
  - Mix check: hr minUnderDb 25.5 / median 28.4; en 26.9 / 28.8.
  - Lint: 0 errors.
  - C14: the older pilots' out/*.mp4 hashes are unchanged, and their lint is 0/0.
  - C2: key search 0 matches; C3: no new grep hits (`evidence/c2-c3-key-and-grep.txt`).
  - C8: both `character.json` have `kind: vehicle` and no limb controls. `assembly.json` has 15 vehicle actions, including drive, chug, honk, whistle, react_surprised and laugh.

Not met, or not run:
- `W_VISEME_FLAT` on en l12 (52 % open, under 60 %), so C7's "no W_VISEME_FLAT" is not met.
- C4's ±10 % match is not met: the ledger's 1590 `eleven-credits` against an API counter of 1037. The account's reset date changed from 2026-04-01 to 2026-12-10 during the run, and the audition credits dropped out of its counter. Both are far inside the free quota; no USD and no Flow.
- The horn and whistle are silent (C10 asks for them "each with an SFX beat"; the beats were dropped when the files failed).
- The desktop app's Cast and Settings views were not opened: UNTESTED.
- The VN Studio and Edu Studio "Later" ROADMAP rows were not written. Each needs a ticket branch in a repo that other sessions may be using, so it is left to the user or the director.

### Follow-ups (see `discoveries.md`)

- Fix the ComfyUI MOSS node (`map_location` passed twice), then rerun the music step for the SFX.
- Cartoon Studio:
  - a `voice_review` gate between voice_cast and voice;
  - `cts_budget_set` on a series that doesn't exist yet leaves a folder that blocks `cts_run_pipeline`;
  - two `cts_sheet_approve ok:false` calls start two overlapping character jobs;
  - pipeline auditions ignore ElevenLabs;
  - the car-turn arc, the antenna limit, wide-shot occlusion;
  - the stale `mcp-guide` intro.
- flow-music-mcp: an empty `GEMINI_API_KEY=` in the repo `.env` can hide the real key.

### Commit status

- flow-music-mcp and cartoon-studio: committed on their branches, not pushed.
- creative-hub: `b6bd265`, `5f672dc`, and the final HUB-31 commit for the pilot, CLAUDE.md, run log and ticket files; not pushed.
- Ticket status stays `in-progress` for the director's checker.

### Items

| Item | Status |
|---|---|
| FMM-17 client, key lookup, status, voices | DONE |
| FMM-18 narrate engine, timestamps, guard | DONE |
| CTS-30 ElevenLabs provider, allocation, auditions, quota | DONE (Cast/Settings view UNTESTED in the app) |
| CTS-31 contracts, lint, fixture | DONE |
| CTS-32 vehicle builder and sheet | DONE |
| CTS-33 road and rail kit | DONE |
| CTS-34 vehicle acting library | DONE |
| CTS-35 timeline, assembly, pipeline, app | DONE (app views UNTESTED) |
| CTS-36 docs and roadmap | DONE |
| Hub wiring: skill, README, services, ROADMAP, hub.ps1 | DONE |
| CLAUDE.md voice rule | DONE (user confirmed the wording in this session) |
| Pilot 4 hr and en, user GO | DONE |
| Horn and whistle SFX | NOT DONE (ComfyUI MOSS node error; silent) |
| C7 no W_VISEME_FLAT | NOT DONE (en l12 at 52 %) |
| C4 ledger within ±10 % of the API delta | NOT DONE (counter reset mid-run; 1590 against 1037) |
| VN Studio / Edu Studio ROADMAP rows | NOT DONE (needs branches in repos other sessions may use; left to the user or director) |
