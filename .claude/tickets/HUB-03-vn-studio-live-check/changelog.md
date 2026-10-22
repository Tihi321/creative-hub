# HUB-03 changelog

2026-10-22, branch `HUB-02-13_roadmap-tasks`, commit 827ecce. Run log: `runs/vno-media-test.md`.

- Test game `vno-media-test` ("The Lantern Door"): CG, insert, SFX, ambience and scene-music cues, with ja, ar and hr editions. The SFX were made with Chiptune Studio `compose_sfx`.
- It builds and lints clean.

Verified: the build and lint of every edition.
Not verified: step 7, the user playing it.
Found: a generate job stayed `running` after ComfyUI crashed natively. It was restarted by hand with `vno_stop_now` and `vno_resume_all`. This goes in VN Studio's ROADMAP.
