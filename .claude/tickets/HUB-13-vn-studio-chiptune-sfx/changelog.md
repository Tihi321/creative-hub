# HUB-13 changelog

2026-10-23. Live check on VN Studio master 2f22db1 (`runs/hub08-13-autostart.md`): with `sfxEngine` and `ambienceEngine` on `chiptune`, `sfx_bell` and `amb_waves` (60 s loop) were made by Chiptune Studio with no imported file and no fallback warning; the build cues `play ambience`, `play sound` and `stop ambience`; 0 placeholders, lint clean. Open: the user listens.

2026-10-22. Tool work: VN Studio VNO-19 (branch `VNO-10-19_hub-roadmap`) and midi-generator MDI-06 (roadmap only, PR #6, merged).

- VN Studio: with `sound.sfxEngine` or `sound.ambienceEngine` set to `"chiptune"`, VN Studio makes the `sfx_` and `amb_` sounds with Chiptune Studio's `compose_sfx`.
- Hub (commit 170ee2e): the skill says when to use it; this ticket's plan.

Verified: VN Studio tests with a fake Chiptune client; HUB-03's SFX made with `compose_sfx` by hand.
Not verified: the live check (a build with `sfxEngine: "chiptune"`). It runs after the VN Studio PR is merged.
