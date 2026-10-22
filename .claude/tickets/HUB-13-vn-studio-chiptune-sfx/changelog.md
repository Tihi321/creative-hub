# HUB-13 changelog

2026-10-22. Tool work: VN Studio VNO-19 (branch `VNO-10-19_hub-roadmap`) and midi-generator MDI-06 (roadmap only, PR #6, merged).

- VN Studio: with `sound.sfxEngine` or `sound.ambienceEngine` set to `"chiptune"`, VN Studio makes the `sfx_` and `amb_` sounds with Chiptune Studio's `compose_sfx`.
- Hub (commit 170ee2e): the skill says when to use it; this ticket's plan.

Verified: VN Studio tests with a fake Chiptune client; HUB-03's SFX made with `compose_sfx` by hand.
Not verified: the live check (a build with `sfxEngine: "chiptune"`). It runs after the VN Studio PR is merged.
