# HUB-30 changelog

## 2026-11-08 - HUB-30 Cartoon Studio 3D route (CTS-18..CTS-29) and pilot 3

Outcome: Cartoon Studio renders 3D toon cartoons in Blender 5.2 from character and set specs. Pilot 3 "Pip i izgubljena marama / Pip and the Lost Scarf" is made in hr (72.6 s) and en (74.0 s) for $0 and 36 Flow credits; the user watched both films and gave GO for phase 2.

### cartoon-studio (branch `CTS-18_blender-3d`, cut from `CTS-10_pilot-2` at `08efa1d`)

14 commits, 143 files, +12211 / -2456 (`git diff --stat 08efa1d..dc92781`):

| Commit | Ticket | What changed |
|---|---|---|
| f2784f1 | CTS-18 | `blender/run.py` and `cts_blender/{api5,io,probe}.py` (headless runner, CTS stdout protocol, 5.x shims); `src/engine/blender/{config,runner}.ts` (path/version pin, E_BLENDER_MISSING / E_BLENDER_VERSION / E_BLENDER_FAILED); `cts_blender_status`, `cts_blender_config`; `seed/config/blender.md`; `blender/LICENSE` GPL-3.0-or-later; packaging of `resources/blender` with `verify-package` |
| 2b7b384 | CTS-19 | contracts `cts.character3d/1`, `cts.set3d/1`, `cts.style3d/1`, `cts.timeline3d/1`; lint by renderer; the `tests/fixtures/mini3d` fixture |
| 1fc6c1a | CTS-24 | six-viseme lip-sync (`src/engine/anim/visemes.ts`) from whisper word times (words-hr / words-en, 70 % alignment floor) with a text+RMS fallback |
| be1484b | CTS-22 | toon look: two-tone material, outlines, blob shadow, sky gradient, optional post (`cts_blender/materials.py`, `seed/style/style3d.json`, `seed/style/toon-3d.md`) |
| eeda972 | CTS-20 | character builder from shapes, face ray test (E_FACE_HIDDEN), the turnaround/mouths/expressions sheet (`build_character.py`, `shapes.py`, `sheets.py`) |
| 30fbedd | CTS-21 | set builder, prop kit, marks and cameras, the four-view set sheet (`build_set.py`) |
| 5e4c858 | CTS-23 | acting library (`acting/*`, `library.json` 24 actions): planted-foot walk/hop/waddle, gestures, springs, camera moves, dense channel writer |
| 52d2c4f | CTS-25 | 3D timeline and scene assembly (`timeline3d.ts`, `assemble.py`, `framing.py`) |
| fdd3958 | CTS-26 | Blender render backend: chunked EEVEE, h264_amf else libx264, concat, mux, mix check (`render.py`, `src/engine/render/blender.ts`) |
| df42c10 | CTS-25 | follow-up: framing follows walking actors, close-ups keep the head through a sit |
| 5d2ff44 | CTS-27 | pipeline steps for blender series (character, sheet_review, set3d, ..., final_render), MCP tools, studio views (Cast 3D sheet and approval, Sets, Preview video, Settings Blender section) |
| 7616358 | CTS-26 | follow-up: rebuild the scene when a character or set spec changes (hash check in ensureAssembled) |
| c3263fc | CTS-28 | retire the cutout authoring path (rig/pose tools return E_RETIRED); canvas renderer kept for pilots 1 and 2 |
| dc92781 | CTS-29 | `docs/blender.md`, README, ROADMAP |

### creative-hub (branch `HUB-30_cartoon-3d`, cut from `HUB-29_cartoon-studio`)

- `fdb5e46`: `.claude/skills/make-cartoon/SKILL.md` rewritten for the 3D route; `README.md` Cartoon Studio row; `services.json` name and docs; `ROADMAP.md` HUB-29 row corrected and HUB-30 row added.
- This commit: `runs/pip-bruno-3d-pilot.md` (the production log), `.claude/tickets/HUB-30-cartoon-3d/` (plan, events, attention A-001..A-003, discoveries, evidence, this changelog), `ROADMAP.md` HUB-30 row status.

### Deviations from the plan

- CTS-25 and CTS-26 each have a second follow-up commit (`df42c10`, `7616358`): 14 commits for 12 tickets.
- Pilot script: the writer put `point` as a line gesture without a `look`; lint passed but assembly failed (`'target'`). The point moved to its own gesture beat with target `oak`; the spoken text did not change, so the safety pass still holds.
- Frame review round 2 needed data changes the pipeline does not make by itself: a set mark `benchside [0.7, 1.7]` (set rebuilt), Pip moves there instead of `center`, a turn after the oak hop, and the push-in on the set's `bench` camera instead of `cu-bruno`; then a re-run from `timeline`. Round 1 films are kept in `out/r1/`.
- The long move is a `hop` (Pip's own locomotion, 6.1 m from the oak to the right mark), not a `walk`; the acting library treats both as planted-foot locomotion.
- Outro clip: both Flow takes drew Bruno as a dog and failed review; the clip fell back, so the last 8 s hold the Blender scene. Flow spend 36 credits (12 intro + 24 outro), not the estimated 24.
- `flow_status` before the clips could not read the balance (Chrome was not running); the spend is taken from `spend.json` and video-plan `record`.

### Verification

| # | Result | Evidence |
|---|---|---|
| C1 | DONE | typecheck, lint, test, test:blender, test:e2e, build, docs:check all exit 0 on `dc92781` (run during implementation, before the pilot) |
| C2 | DONE | `cts_blender_status`: usable, 5.2.2, AMD Radeon 8060S (OpenGL); a missing path and a 5.1 scratch config are refused; `dist:installer` passes `verify-package` with `resources/blender/run.py` |
| C3 | DONE | the A3 grep returns nothing; "Program Files" only in `seed/config/blender.md`, `README.md`, `docs/blender.md` |
| C4 | DONE | finals warm 0.203 / 0.202 s a frame, p95 0.223 / 0.220 (limit 0.35 / 0.6); final wall 322 s for 72.6 s and 327 s for 74.0 s = 4.4 min per minute (limit 10); preview 115 s / 114 s = 1.6 min per minute (limit 3) |
| C5 | DONE | 13/13 lines per language have lip-sync files; hr 11 words-hr + 2 text-hr (85 % aligned), en 13 words-en (100 %); lint 0 errors, 0 warnings (no E_MOUTH_SILENT, no W_VISEME_FLAT), min non-rest share 0.69 |
| C6 | DONE | `assembly.json` hr and en: pip spec 71cf3c3 / asset 858db12, bruno spec 1e3ffe7 / asset 30277ab, equal to `build.json` and the approved `sheet.specHash`; contact sheets compared with `sheet.png`: on model in every frame; frame-critic problems listed below |
| C7 | DONE | sheets approved 18:46:42, set3d job started after it (18:46:42, the pause released it) |
| C8 | DONE | 14 distinct actions (cheer, droop, hop, laugh, nod, point, react_surprised, shake_head, shrug, sit, stand_up, think, turn, wave) plus a push; hop 6.1 m; no limb through the body or foot slide seen in the contact sheets |
| C9 | DONE | same scriptHash `3785740`, same per-actor beat and action order in hr and en; lint has no E_LANG_ORDER |
| C10 | DONE | both: h264 1920x1080, 24 fps, yuv420p + aac; 72.6 s and 74.0 s; lint 0 errors |
| C11 | DONE | music min 27.5 / 27.2 dB under the voice, median 28.3 / 28.2; integrated loudness -16.0 LUFS both (ebur128) |
| C12 | DONE | `spend.json` only Flow credits (36, intro/outro); `budget.json` capUsd 0; voice manifests costUsd 0; Gemini quota 0/10 used before and after; no downloads |
| C13 | DONE | `sha256sum -c` of the 8 pilot 1 / pilot 2 MP4s: all OK (`evidence/c13-hashes-after.txt`); lint 0 errors and a 2 s canvas preview of each on the new build (during implementation) |
| C14 | DONE | CTS-28 grep empty; MCP tool list has the 3D tools and none of the retired ones |
| C15 | DONE | `studio-shots.mjs --blender` passed (real engine, mini3d); built app `release/win-unpacked` on the real data, hub engine stopped first: Cast shows both 3D sheets "approved", Sets the park sheet, Preview plays `hr.preview.mp4` (readyState 4, playing), Settings shows the path, 5.2.2 and the GPU; 0 console errors (`evidence/c15/`) |
| C16 | DONE | skill, README, services, ROADMAP rows and run log committed on `HUB-30_cartoon-3d` |
| C17 | DONE | user verdict 2026-11-08: "GO for phase 2" (no separate notes on look, acting, lip-sync or music) |

Not tested:
- `E_RETIRED` answers of the retired tools were not called in the live app.
- The installer was built and its package was verified, but it was not installed and run.

### Open problems (frame review round 2, left to the user)

- In the two-shot, Pip is seen three-quarters from behind (40-71 s).
- At the bench push-in, the seated Bruno turns his whole body toward Pip, so the shot ends on his back (46 s).
- These come from the automatic two-shot camera and the whole-body look, which are code in Cartoon Studio; they are listed in `discoveries.md`.

### Follow-ups

- The phase 2 items of the plan (the user said GO).
- The `discoveries.md` entries:
  - Lint misses a line gesture that needs a target.
  - An assembly that fails is still filed as done.
  - `clips.json` under-counts the credits of retakes.
  - Frame review round 2 has to be started by hand.
  - The two-shot camera and the seated look.
  - Flow drew Bruno as a dog from the wide keyframe.
  - The real-episode render time is not in the docs.
  - The shared prompt and the MCP instructions still say "cutout".

### Commit status

- cartoon-studio: committed locally on `CTS-18_blender-3d` (`dc92781`), not pushed.
- creative-hub: committed locally on `HUB-30_cartoon-3d`, not pushed.
- The ticket stays `in-progress` for the director's checker.
