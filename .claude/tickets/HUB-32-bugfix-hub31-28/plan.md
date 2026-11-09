---
ticket: HUB-32
title: Fix the open bugs logged during HUB-31 and HUB-28
status: done
---

# HUB-32: fix the open bugs from HUB-31 and HUB-28

The bugs come from `../HUB-31-vehicles-voices/discoveries.md`, the top entries of `../HUB-31-vehicles-voices/changelog.md` and `../HUB-28-edu-mobile-music/discoveries.md`. Each fix goes on a ticket branch in its own repo and is merged into that repo's master. Rule: $0 spend (no Flow, no ElevenLabs calls), never start Scriptorium or Chiptune Studio.

| Repo | Ticket(s) | What |
|---|---|---|
| cartoon-studio | CTS-44..47 | voice-review button in the studio UI; a retry cancels later steps' queued or stopped jobs (no stale final after a resume); `extent()` half extents and the mini-vehicles house; 3D wording instead of "cutout" |
| flow-music-mcp | FMM-20 | fewer `/v1/user/subscription` reads (a 5 s cache minus the credits spent), after-read retried, `remaining_after` never null |
| comfy-mcp | CMC-08 | the two local ComfyUI node fixes as text patches: `out/patches.js check|apply|revert` |
| edu-game-studio, creative-hub-web | EGS-64+, WEB-05 | the HUB-28 discoveries (role-play clip on scene leave, TV remote in the audio panel, Back closes the panel, bridge pill, e2e timeout, plan paths, play.mjs tap check, stale client job, music steps, asset alt texts) |
| creative-hub | HUB-32 | `hub.ps1 status` shows the ComfyUI fix check and no longer flickers live services to down; `hub.ps1 comfy-patches` |

Run log with the DONE / NOT DONE / UNTESTED table: `runs/bugfix-hub31-28.md`.
