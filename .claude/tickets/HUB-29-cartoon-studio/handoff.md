# HUB-29 handoff: pilot 2 done, waiting for the checker (2026-11-08)

Pilot 2 (plan.md section `# Pilot 2 (CTS-10..)`, approved 2026-11-07) is built and made. The user approved both character sheets ("Approve both") and the films ("Good, go"). The ticket is `in-progress` (REQ-0022, director-managed); the director's checker runs next.

## Where things are

- **cartoon-studio** branch `CTS-10_pilot-2`, cut from `CTS-01_pilot` at f5c37b9, local only, working tree clean: 0f79bb4 CTS-10, c0d7350 CTS-16, 8900236 CTS-15, 268a0d9 CTS-11, 21b20dc CTS-12, 9146351 + 4f5cd9a CTS-13, face95e CTS-14, 08efa1d CTS-17. Push and PR (base `CTS-01_pilot` while PR Tihi321/cartoon-studio#1 is open, else `master`) after the checker; the director pushes.
- **creative-hub** branch `HUB-29_cartoon-studio`: skill, run log `runs/pip-bruno-pilot.md`, this ticket folder (changelog entry 2026-11-08, `evidence/pilot2/`) and the HUB-29 roadmap row committed, not pushed. The HUB-28 roadmap row and HUB-28 files are another session's: left uncommitted.
- Pilot 2 data: `~\CartoonStudio\series\pip-bruno\` (MP4s in `episodes\ep00-pilot\out\`); copies in `.claude/temp/hub29/p2/pip-bruno-{hr,en}.mp4`.

## The user's answers (2026-11-07)

1. Nano Banana: no spend; ask first (cap $0). Not used.
2. Flow: intro + outro, cap 50. Spent 24.
3. SVG path (a): kept as an option. Not run.
4. No model download without asking. None made.

## Open items (see changelog "Not run / not verified")

- B15 only in mocked mode (the Cast view with the real pip-bruno data not opened).
- Flow balance before the clips not shown; after: 884, the same as after pilot 1.
- `cts_pose_make` / `poses` step, MOSS sfx, minimax-music-3 and gemini not run live.

## Services running now (none stopped)

cartoon-studio headless engine (7465, started by this session with hub.ps1 at the CTS-17 build), ComfyUI (8188), comfy-mcp (7460), flow-music-mcp (7462, its Chrome tab open on the Flow project), VibeTTS (7723, tray). Not started: Scriptorium, Chiptune Studio, Strata.
