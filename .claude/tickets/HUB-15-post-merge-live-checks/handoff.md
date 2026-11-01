# Hub overall status (HUB-15 handoff, 2026-10-31)

## Merged today
- HUB-18: hub #14, VN Studio #25 (49eb363), midi/MDI #11 (ad85fd2)
- HUB-15 bookkeeping: hub #15
- HUB-19 edu game studio: hub #16 (see its handoff)
- HUB-20 moss image: hub #17 (eb68bca), comfy-mcp #4 (68de91a), edu #21
Hub master at eb68bca.

## Decisions / state
- HUB-09 done. Claude provider NOT enabled in acp-proxy (user never chose).
- HUB-07: Flow Music dropped; 6 hr clips wait on Gemini TTS quota (10 req/day free).
- Services: acp-proxy, comfy-mcp, chiptune-studio, pixel-studio, vn-studio stopped via hub.ps1. VibeTTS (pid 16096, user's app, not hub-managed) and Strata (8080) left running. Everything else was already down (scriptorium, book-translator, edu-studio, comfyui, lmstudio, flow-music-mcp).

## Remaining: C6 user verdicts
Play HUB-02, 03, 06, 10, 16, 17. Read 05. Watch 11. Listen 13 and the six HUB-18 tracks in `C:\Users\Infplane\VisualNovels\projects\hub18-neon-static` and `hub18-hollow-memory`. Then the edu pilot after it is finished.

## UNTESTED
- moss in the edu client and at non-1024 sizes
- HUB-18 chip fallback, LM Studio composer, UI chip select
- CI on the merged masters
- Known failing: midi Genesis timing test (5.7s vs 3s expected)

## Open questions
- Codex mirrors (`AGENTS.md`, `.agents/`, `.codex/`) are untracked in the hub repo: commit, gitignore, or leave? Also `runs/edu-solar-system-pilot.md` is untracked.
- VN Studio roadmap has stale `engine.lock` and `plan_music` persona notes to clean.
- Director request: `.claude/director/requests/REQ-0005-finish-hub-roadmap.md`.

- 2026-11-01: the user accepted every C6 verdict (HUB-02, 03, 05, 06, 10, 11, 13, 16, 17 and the HUB-18 tracks), no redo needed. HUB-15 is done.
