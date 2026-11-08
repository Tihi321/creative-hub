# pip-bruno-3d / ep00-pilot (pilot 3, the 3D route)

Started 2026-11-08. Plan: `.claude/tickets/HUB-30-cartoon-3d/plan.md` (REQ-0022). Brief: pitch p1 copied from the `pip-bruno` bible (Pip the fast squirrel, Bruno the slow hedgehog, one small puzzle in the park), ages 4-8, hr + en, about 60 s, 12-16 lines, intro and outro.
Code: `cartoon-studio` `CTS-18_blender-3d` at `dc92781` (CTS-18..29), hub `HUB-30_cartoon-3d`.

## Money
- Cap USD: 0 · Flow credits cap: 50, intro and outro only (approved with the plan; the user's answer 2026-11-08: regenerate the intro and outro from Blender stills, about 24 of the 50 credits, after seeing pilot 2's clips next to a Blender still)
- video-plan.mjs estimate: (step 7) · flow_status credits before / after: (step 7)

## Ids and paths
- Series `pip-bruno-3d`, episode `ep00-pilot`, data `~\CartoonStudio`
- Blender: 5.2.2 LTS, GPU AMD Radeon(TM) 8060S Graphics (OpenGL 4.6, driver 24.20.79.01), `cts_blender_status` ok (2026-11-08)
- Engine restarted with `hub.ps1 stop/build/start cartoon-studio` on `dc92781`. Running: ComfyUI, comfy-mcp, VibeTTS, flow-music-mcp. Not started: Scriptorium, Chiptune Studio, Strata.
- C13 before: hashes of `pilot` and `pip-bruno` `out/*.mp4` in `.claude/tickets/HUB-30-cartoon-3d/evidence/c13-hashes-before.txt`

## Log
- 2026-11-08 15:32 `cts_run_pipeline` with brief.pitch p1 (pitch pause skipped), `options.renderer: "blender"`; `cts_budget_set` capUsd 0, flowCreditsCap 50 (15:32:16, before any Flow call)
- 15:33 bible (showrunner, Claude): pilot 2 palette kept (#d9792b #f3dfb5 #8a5a35 #4e3423 #6fae4f #2b2118), 3D look, outlinePx 2
- character (designer, Claude): Pip and Bruno specs from the toon-3d.md examples recoloured to the bible palette, shoulders moved just outside the body; both built and self-reviewed, pass on revision 0 (Pip build 2.97 s)
- Sheets in `.claude/tickets/HUB-30-cartoon-3d/evidence/pip-sheet-r1.png`, `bruno-sheet-r1.png`; pipeline `waiting-on-user` at sheet_review
- 2026-11-08 18:46 user approved both sheets (pip r1 specHash 71cf3c3, bruno r1 specHash 1e3ffe7); pipeline resumed at set3d.
- 2026-11-08 set3d park: spec = guide park in bible palette (oak, bench+seat, 3 pines, 2 round trees, 3 bushes, flowers, rock, 3 clouds; marks left/center/right/bench/oak; cameras wide, bench). Built in 1.68 s, 0 warnings, self-review pass r0. Sheet copy: evidence/park-set-sheet-r1.png.
- 2026-11-08 18:47 script "Pip i izgubljena marama / Pip and the Lost Scarf": 13 lines, 1 scene, 13 actions (sit, wave, point x2, hop moves, think, shrug, shake_head, droop, react_surprised, laugh, stand_up, nod, cheer); longest walk oak->right 6.1 m hop; push on cu-bruno. Safety pass round 1 (5/5/5/5).
- 2026-11-08 18:48 voice cast: hr OmniVoice (pip "female, child, high pitch" seed 4101; bruno "male, young adult, low pitch" seed 5207; fallback supertonic F2/M2), en Kokoro (pip af_sky 1.08, bruno am_michael 0.9). Provider pinned; Gemini quota before 0/10 used, after 0/10 used.
- 2026-11-08 18:51 voices: 26 made, 0 placeholders, $0; hr 30.24 s, en 31.6 s (2 min 23 s wall).
- 2026-11-08 18:51 music: theme 39.9 s, ace-step-v1-instrumental, seed 31417, G major 96 bpm, 21.2 s wall. No sfx.
- 2026-11-08 18:52 lip-sync whisper alignment: hr 11/13 words-hr (85 %), 2 text-hr fallback; en 13/13 words-en (100 %). Lint requireAudio: 0 errors, 0 warnings, min mouth-open share 0.69.
- 2026-11-08 18:52 assemble r1 FAILED both languages: E_ASSEMBLE_FAILED "'target'" - b07 line gesture point had no look. Fixed the script data (point moved to gesture beat b07a with prev, target oak; script hash 253d3e6); script text unchanged, safety still valid. Timelines rebuilt (hr 72.6 s, en 74.0 s), assemble r2 ok (hr 1743 frames, en 1775, 8 shots, 13 actions, 0 warnings, ~3.1 s).
- 2026-11-08 Flow estimate (video-plan.mjs plan, omni-720p): intro 12 + outro 12 = 24 credits, 30 with reserve, cap 50, spent 0. Pipeline waiting-on-user at clips. Step 7 STOP: showed pilot 2 intro/outro next to Blender stills (evidence/step7-compare.png, pip3-blender-still-t12/t52.png). Attention A-002 open.
- 2026-11-08 19:3x A-002 answered "Go, make both". flow_status before: Chrome not running, balance not readable (credits unknown); after: spend recorded by video-plan.
- 2026-11-08 19:39 intro: keyframe = Blender still (two shot), Omni 1.1 Flash 720p, max_credits 15, 12 credits, review pass (small drift: Pip buck teeth, softer spines). video-plan record ch01.s01.sh01.
- 2026-11-08 19:44 outro: two takes (max_credits 15 each), 24 credits, both failed review (Bruno drawn as a dog; take 2 also changed the set) -> fallback, the last 8 s hold the Blender scene. video-plan record ch01.s01.sh02 (24). Flow total 36 of 50.
- 2026-11-08 19:46 previews round 1: hr 72.6 s in 113.7 s, en 74.0 s in 116.6 s (Blender warm 0.061 s a frame). Frame review r1 revise: Pip's back to camera 39-70 s, cu-pip shows back of head, cu-bruno push cut.
- 2026-11-08 20:00 finals round 1 (kept in out/r1/): hr 72.6 s in 325.8 s, en 74.0 s in 326.1 s, h264_amf, warm 0.205 s a frame 1080p, -20.65 / -20.44 LUFS in, music min 27.5 / 27.2 dB under voice.
- 2026-11-08 20:01 round 2 data fixes: set mark benchside [0.7,1.7] (set rebuilt 1.63 s, 0 warnings); script b17 to benchside, b08a turn pip right, b20 push on the bench camera (script hash 3785740). Pipeline re-run from timeline.
- 2026-11-08 20:05 previews round 2: hr 115.3 s, en 113.9 s. Frame review r2 revise (open for the user): Pip three-quarter back in the two shot, Bruno's back at the bench push, Bruno in profile after stand_up.
- 2026-11-08 20:16 finals round 2: out/hr.mp4 72.6 s in 322.1 s, out/en.mp4 74.0 s in 327.3 s; warm 0.20 s a frame, p95 0.22; mix check -20.65 / -20.44 LUFS in, music min 27.5 / 27.2 dB under voice. Spend $0, Flow 36 credits.
- 2026-11-08 C13 after: sha256sum -c of the 8 pilot 1/2 MP4s all OK (evidence/c13-hashes-after.txt).
- 2026-11-08 20:17 step 9 STOP: films sent to the user; attention A-003 open.
- 2026-11-08 user verdict (C17): "GO for phase 2". No separate notes on look, acting, lip-sync or music level were given.
- 2026-11-08 checks: C10 both films h264 1920x1080 24 fps yuv420p + aac (72.6 s, 74.0 s); C11 ebur128 integrated -16.0 LUFS both, music median 28.3 / 28.2 dB under voice; C6 assembly spec/asset hashes equal build.json and the approved sheet specHash (pip 71cf3c3/858db12, bruno 1e3ffe7/30277ab); C9 same scriptHash 3785740 and the same per-actor beat/action order in hr and en; C12 spend.json only Flow credits (36), capUsd 0, voice costUsd 0.
- 2026-11-08 C15: studio-shots.mjs --blender passed (real engine on mini3d, 0 console errors). Built app release/win-unpacked on the real data with the hub engine stopped first (hub.ps1 stop cartoon-studio): Cast shows Pip and Bruno 3D sheets "approved 2026-11-08T18:46:42", Sets the park sheet, Preview plays out/hr.preview.mp4 (readyState 4, playing at 33 s), Settings shows C:/Program Files/Blender Foundation/Blender 5.2/blender.exe, 5.2.2, AMD Radeon 8060S (OpenGL); 0 console errors. Screenshots: .claude/tickets/HUB-30-cartoon-3d/evidence/c15/. Hub engine started again (hub.ps1 start cartoon-studio: up on 7465).
- UNTESTED: E_RETIRED answers of the retired tools in the live app; installing and running the Setup exe.
- Open (frame review round 2, code in Cartoon Studio): Pip three-quarter back in the two shot (40-71 s); seated Bruno turns his whole body at the bench push (46 s).
