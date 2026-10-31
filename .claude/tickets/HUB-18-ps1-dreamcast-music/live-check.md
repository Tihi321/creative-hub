# HUB-18 live check, 2026-10-31

Code under test, built from the unmerged branches (both repos were already checked out on them, so nothing to restore):
- visual-novels-orchestrator `VNO-51_ps1-dreamcast-chips` @ d91ac6b, engine rebuilt (`vite build --config vite.engine.config.ts`), VN Studio on 7459 via `hub.ps1 start vn-studio`.
- midi-generator `MDI-11_mcp-prompts-seven-chips` @ b924fed, rebuilt (`build:mcp` + electron-vite), Chiptune Studio on 7458 via `hub.ps1 start chiptune-studio`.
- No paid model: both projects use `models.composer = client/claude-code` (this session answered the composer task over `vno_get_task` / `vno_submit_task`); art provider `hand`. Spend stayed 0.00 today.

## What ran (all over MCP, real apps)
1. `vno_create_project` x2, `music.provider = chiptune`, `music.chip` left unset (auto), `vno_run_pipeline from=music`.
2. The composer task prompt from the new `plan_music.md` really contains the seven chips and the four synth moods, the synth-mood rule, and "80 to 110 BPM for synth moods". Answers were accepted by the schema.
3. The engine merged the plan (`vno_set_music` read-back) and Chiptune Studio composed and rendered every track to ogg.

| Project | Track | mood / chip / bpm / key / bars | File | ffprobe |
|---|---|---|---|---|
| hub18-neon-static (80s neon synthwave) | music_01 menu | dreamwave / dreamcast / 92 / F / 40 | ~/VisualNovels/projects/hub18-neon-static/assets/music_01/v1.ogg | 104.35 s (40 bars at 92 = 104.35) |
| | music_02 | synthwave / dreamcast / 104 / A / 40 | .../music_02/v1.ogg | 92.31 s (expected 92.31) |
| | music_03 | darkwave / dreamcast / 96 / D / 36 | .../music_03/v1.ogg | 90.00 s (expected 90.00) |
| hub18-hollow-memory (90s PlayStation gothic horror) | music_01 menu | darkwave / ps1 / 88 / D / 36 | ~/VisualNovels/projects/hub18-hollow-memory/assets/music_01/v1.ogg | 98.18 s |
| | music_02 | darkwave / ps1 / 96 / A / 36 | .../music_02/v1.ogg | 90.00 s |
| | music_03 | sad / ps1 / 60 / E / 20 | .../music_03/v1.ogg | 80.00 s |

All six: vorbis, 44.1 kHz stereo, durations equal bars x 240 / bpm. Neon plan: menu music_01, chapters 1/2/3 = music_01/music_03/music_01 (music_02 unused: my choice, not a bug).
`vno_build` then `vno_lint` of hub18-neon-static: both ok, `game/index.html` built, lint lists the three tracks ("start music with chiptune"); only placeholders for the three hand-art images.

Earlier on master (HUB-18 changelog): direct compose_track renders dreamwave/dreamcast, darkwave/ps1, synthwave/ps1, outrun/dreamcast, stingers on both chips, Dreamcast rain ambience.

## Verified
- VNO-51 code live: new chips/moods reach the composer prompt; synth moods and ps1/dreamcast pass `mergeChipPlan` unclamped (104 and 96 BPM) and are stored in the project music plan; the chiptune provider composed with them; ogg valid, durations exact; game builds and lints.
- MDI-11 branch builds and Chiptune Studio starts and serves compose_track/render_audio.

## Not verified
- Nobody has listened to the tracks (a production is done only when the user plays them). Per CLAUDE.md this stays open.
- The chip actually used by the renderer is not logged by either app. Indirect evidence only: volumedetect of hollow music_01 (-17.4 mean / -2.4 max dB) sits next to a same-params ps1 render (-17.3 / -2.1) rather than snes (-16.4 / -4.0), different seed, so weak. The MCP arguments came from the stored plan, which names ps1/dreamcast.
- The deterministic fallback (`fallbackChipPlan` when the composer model fails: genre -> dreamcast / ps1) was not run live (it needs the planner to fail, and the role list ends in paid models). Unit tests only.
- The MCP prompts of MDI-11 (`compose_track`, `remix_to_chip`) not called live, unit test only.
- Voices, art, stage cues, a full pipeline with a real local LM Studio composer, the app UI chip select.

## Findings
1. Stale `~/VisualNovels/engine.lock`: it held pid 41240 from 2026-10-28, which Windows had reused for `msedgewebview2.exe`, so `hub.ps1 start vn-studio` printed nothing useful and VN Studio refused with "already running on this data folder (pid 41240)" in `logs/vn-studio.err.log`. The lock check seems to test only that the pid is alive. Fix idea (VN Studio repo, own ticket): also compare the process name or start time, or ping the mcpUrl. I deleted the lock by hand. Not fixed here.
2. `plan_music.md` persona still says "calm instrumental music ... never loud" and the rules say "Calm, gentle ... no sudden loud parts" above the synth-mood rules. The planner still chose synth moods with a client model, but a small local model may follow the persona over the later rule. Worth reading with a real LM Studio composer.
3. `hub.ps1 start` output for a failed vn-studio start showed only the tail of other services, not the error.
