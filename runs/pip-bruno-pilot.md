# pip-bruno / ep00-pilot (HUB-29 pilot 2, REQ-0022)

Started 2026-11-07 (code), run 2026-11-08. Brief: premise p1 "Pip and Bruno" from the `pilot` series bible (the user's liked premise), ages 4-8, hr + en, about 60 s, 12-16 lines, intro + outro Flow clips. Cartoon Studio branch `CTS-10_pilot-2`. Plan: `.claude/tickets/HUB-29-cartoon-studio/plan.md`, section `# Pilot 2`.

## The user's answers (2026-11-07, relayed by the director)
- Nano Banana: "No spend, ask me": USD cap $0; ask before any Gemini image spend.
- Flow: intro + outro, about 24 credits, cap 50.
- SVG path (a): kept as an option, not run.
- Ask before any model download.

## Money
- Cap USD: 0 · Flow credits cap: 50 · Spent (cts_budget_get):
- video-plan.mjs estimate: · flow_status credits before / after:

## Probes (P0b and the ticket workers' live probes)
- 2026-11-07 23:13 ACE-Step v1 instrumental via comfy-mcp: 40 s requested, 39.94 s, wall 19.9 s (seed 4101), -18.3 LUFS integrated, LRA 8.5 LU. Not heard by a person (`.claude/temp/hub29/p0b/ace-40s.flac`).
- CTS-15 generateTheme probe: 40 s ACE-Step in 24.7 s wall, ogg 39.94 s, -16.5 LUFS.
- CTS-11: Z-Image img2img d0.8 36.8 s cold; mouth inpaint d0.8 28.2 s changed the mouth only mildly. img2img follows the sketch silhouette closely (a stick arm stayed).
- CTS-12 (identity across poses): squirrel body plan -> 3 candidates (32.9/28.2/28.1 s) and wave/point/shrug (32.9/28.2/28.2 s); the same character in all four (Claude read the sheet). The tail overlapped an arm and the shrug read as a cheer: rules added to the body-plan prompt.
- CTS-13 (face patches by inpaint at 0.9-1.0): mouths A, E, O read; MBP, eyes half/closed and brows did not. Fix (4f5cd9a): those states are drawn in code from the master's colours; all read on the probe rig sheet (Claude read it).

## Ids and paths

## Log

## Renders

## Reviews

## Checked / not checked

## Run 2026-11-08
- 10:20 P1: after a reboot, hub.ps1 started comfyui (pid 23544), comfy-mcp, flow-music-mcp; VibeTTS was up (tray). Not started: Scriptorium, Chiptune, Strata. Cartoon Studio built at CTS-17 08efa1d and started with hub.ps1 (pid 7568); the seed refresh updated 12 unchanged seeded files (config autostart, prices, providers, render, roles, studios; prompts ref-pick, rig-raster, composer/music, clip-shots, writer/script; style cutout-kids) and added body-plan.md and pose-review.md.
- B14 (part): cts_lint pilot/ep00-pilot on the new build: 0 errors, 0 warnings.
- 10:33 P2: cts_run_pipeline {series pip-bruno, episode ep00-pilot, brief: p1 copied from the pilot bible, ages 4-8, 60 s, lines 12-16, intro, outro}: pitch and pitch_choice "given pitch p1".
- 10:35 P0: cts_budget_set capUsd 0, flowCreditsCap 50, approvedBy user (approvedAt 2026-11-08T10:35:37+01:00).
- Bible (Claude as showrunner): palette #d9792b #f3dfb5 #8a5a35 #4e3423 #6fae4f #2b2118; cast pip (orange squirrel, green scarf), bruno (stocky brown hedgehog); set park.
- cast_sheet: body plans by Claude (character-designer). Pip: seeds 319536-319538, 40.8/28.2/28.1 s; picked c3 (c1 had a grass tuft, c2 a tree and bench: the style "look" with the park leaks into the character prompt). Poses wave/point/shrug 28.1 s each. Bruno: seeds 421246-421248, 28.1 s each; picked c2; none kept the dark spine cloak around the body (only the spiky crown). Poses 28.1 s each.
- 10:44 P3 PAUSE: both sheet.png shown to the user in chat; waiting for approve or redo per character.
- 10:53 P3: the user answered "Approve both"; cts_sheet_approve pip ok, bruno ok.
- 10:53 rig (raster, both): pip 130 s, bruno 92 s; face states A/E/O by inpaint (pip diffs 49.7/64.7/35.0, bruno 77.2/97.5/49.0, ~28 s each), MBP, eyes half/closed and brows drawn. Rig sheets read by Claude: one face, mouths distinct, joints closed. Noted: Pip's wave crosses her face at the peak; Bruno's E mouth is a white tooth strip; Bruno's ears came out lighter than on his sheet. No first rig job before 10:53:47 (both approvals 10:53:46-47).
- poses: none asked (gestures stay part rotations).
- set park: Z-Image background 2880x1620 and a bush prop; the prop (682x458, native size) was resized by hand to 340 px wide (pilot 1 discovery repeats). groundY 1480, actorScale 0.41, marks left/center/right/bench, shots wide/two/cuLeft/cuRight.
- script (Claude as writer): "Where Is the Acorn?", 14 lines, intro first, outro last, no sfx. safety: pass (5/5/5/5).
- voice_cast: pip hr OmniVoice "female, child, high pitch" seed 3101 / en Kokoro af_sky; bruno hr OmniVoice "male, middle-aged, low pitch" seed 4207 / en bm_george. cts_voice_quota before: 10 of 10 left (14 lines per language > 10, so both local by the hub rule); 0 Gemini requests. voice: 28 clips, 0 placeholders, hr 31.3 s, en 32.7 s.
- music: ace-step-v1-instrumental, seed 4101, bpm 100, C major, 39.9 s, 24.7 s wall; no sfx. No Chiptune call.
- clips: video-plan.mjs plan 2 x 12 = 24 credits (30 with reserve) of cap 50; next max_credits 15 each. Flow balance before the clips: not shown by flow_status (Chrome was not running); each video job measured its own balance change: intro 12, outro 12. Balance after: 884 (flow_status, PRO plan) - the same number as after pilot 1, unexplained. Keyframes are player stills (clips/keyframes/intro.png, outro.png). Reviews by Claude (frame-critic): intro pass, outro pass. spend.json: 2 credit entries (24), no usd. video-plan record: spent 24 of 50.
- timeline: hr 57.2 s, en 58.6 s, lint 0/0. Previews hr 7.3 s, en 9.3 s wall. Frame review round 1: hr pass, en pass (the bench close-up keeps Pip near the right frame edge: taste).
- 11:08 finals: hr 57.25 s in 22.1 s, en 58.67 s in 22.7 s, h264_amf, 1920x1080 24 fps yuv420p + aac, same scriptHash 986c3a14, integrated -16.0 / -15.9 LUFS. mix-check: hr min 25.6 dB, median 29.7, gap 24.8; en min 26.0, median 29.4, gap 25.0 (target >= 15 / >= 17). Frames at 4 s and 53 s show the Flow intro and outro spliced in (evidence splice-check.jpg).
- B14: pilot 1 en preview re-rendered on the new build (55.96 s, 8.7 s wall) after lint 0/0.
- P6 PAUSE: pip-bruno hr/en MP4s and the pilot 1 re-renders sent to the user; waiting for the verdict (look, music and its level, go/no-go).
- 11:48 P6 USER VERDICT: "Good, go" (answer to: the films' look, the music and its level, go for phase 2). Recorded as: hr and en good, the Z-Image puppet look good, music and level good, phase 2 GO with this method. The pilot 1 re-renders were offered; no separate verdict given on them.
