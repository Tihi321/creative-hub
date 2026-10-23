# HUB-11 changelog

2026-10-23. Phase 3 production (`runs/the-lighthouse-that-kept-lists-2.md`): Scriptorium screenplay (short-film, 19 shots, 123 s, Claude as writer), 18 Flow clips (Omni 720p, 0 failures), 2 Flow Music songs, VibeTTS voices (Gemini's daily quota was used up), animatic, final `video/out/final.mp4` (123 s). Spend: 192 Flow credits (1,050 -> 858), 10 Flow Music credits; budget agreed by the user (150, up to about 300). Found: FMM-14, 15, 16; HUB-14 (planner); SCP-29. Open: the user watches it.

2026-10-22. Tool work: Scriptorium SCP-17 (PR #10, merged) and flow-music-mcp FMM-12 (PR #5, merged).

- Phase 1, Scriptorium: screenplay formats (`short-film`, `cartoon`, `kids-cartoon`), `get_screenplay`, and `adapt_book` to a screenplay.
- Phase 2a, flow-music-mcp: `flow_assemble` takes stills, trims, music cues and ducking, and returns a `timeline`.
- Phase 2b, hub (commit 54fe169): the `make-video` skill and `scripts/video-plan.mjs` (shot plan, cost, budget, each call's `max_credits`, the assemble timeline), with 14 tests and a fixture screenplay; a Video block in `runs/_template.md`; the CLAUDE.md lines.

Verified: `node --test scripts/video-plan.test.mjs` (14 pass); flow-music-mcp's assemble live with synthetic media.
Not verified: phase 3, the first video (a free animatic first, then up to 150 Flow credits). It runs on the merged builds.
