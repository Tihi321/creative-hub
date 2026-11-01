# HUB-07 changelog

2026-11-01. Closed. Verified on disk: VN Studio project hub07-flow-test has 9 hr clips in voice/hr (the 6 missing ones written 2026-10-24 09:26-09:27, HUB-15 check C5, Gemini TTS) and 9 en clips in voice/en; game/ holds 19 mp3 files. Flow Music was dropped by the user on 2026-10-31. Remaining: the user plays the game.

2026-10-23. Live run, free part (`runs/hub07-flow-test.md`): 12 Flow images (backgrounds, sheets, sprites with the sheet as reference, a CG with both sheets, the cover) and Gemini voices (en 9/9, hr 3/9) for a choice VN with a Croatian edition; Flow balance 1,050 before and after. Found and fixed: VNO-22 (pre-check failed while Flow's Chrome was not open yet), VNO-23 (form feed in the seeded `flowRepo`), VNO-24 (a daily Gemini quota retried per clip), FMM-13 (settings popover over the prompt box; the cover worked after the fix). Open: 6 hr clips after the quota resets, Flow Music (credits), the user plays.

2026-10-22. Tool work: flow-music-mcp FMM-11 (PR #5, merged) and VN Studio VNO-10 phases 0 to 3 (branch `VNO-10-19_hub-roadmap`).

- flow-music-mcp: `flow_narrate` output formats, Gemini TTS `gemini-3.8-flash-tts`, and `flow_voices` with each voice's gender.
- VN Studio: the `flow` provider for `art.provider`, `voice.provider` and `music.provider`, through a flow-music-mcp client that renews its session.
- Hub (commit 170ee2e): the skill. What phase 4 needs is in `hub-notes.md`.

Verified: flow-music-mcp live (an English and a Croatian Gemini mp3, the Windows voices); the VN Studio tests with a fake client.
Not verified: phase 4, a VN made with the Flow provider (credits up to `flowMusicMaxSongs` 4). It runs after the VN Studio PR is merged.
