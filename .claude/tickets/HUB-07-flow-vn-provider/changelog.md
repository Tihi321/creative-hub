# HUB-07 changelog

2026-10-22. Tool work: flow-music-mcp FMM-11 (PR #5, merged) and VN Studio VNO-10 phases 0 to 3 (branch `VNO-10-19_hub-roadmap`).

- flow-music-mcp: `flow_narrate` output formats, Gemini TTS `gemini-3.8-flash-tts`, and `flow_voices` with each voice's gender.
- VN Studio: the `flow` provider for `art.provider`, `voice.provider` and `music.provider`, through a flow-music-mcp client that renews its session.
- Hub (commit 170ee2e): the skill. What phase 4 needs is in `hub-notes.md`.

Verified: flow-music-mcp live (an English and a Croatian Gemini mp3, the Windows voices); the VN Studio tests with a fake client.
Not verified: phase 4, a VN made with the Flow provider (credits up to `flowMusicMaxSongs` 4). It runs after the VN Studio PR is merged.
