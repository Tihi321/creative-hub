# Changelog

## 2026-10-28: HUB-18, PS1 and Dreamcast music in visual novels

VN Studio can now plan and compose music on Chiptune Studio's `ps1` and `dreamcast` chips with the synth moods (`dreamwave`, `synthwave`, `darkwave`, `outrun`). Chiptune Studio's MCP prompts list all seven chips. The hub skill and docs describe both. Everything is uncommitted on ticket branches.

### visual-novels-orchestrator, branch `VNO-51_ps1-dreamcast-chips` (from `master` @ daf830f)
- `src/shared/vn.ts`: `CHIPS` now ends with `ps1` and `dreamcast`. The zod `music.chip`, the Look tab select and the CLI all read this list, so they follow.
- `src/engine/studios/chip-plan.ts`:
  - New `SYNTH_MOODS`, `MUSIC_MOODS` and `MAX_SYNTH_BPM` 118. `mergeChipPlan` accepts the synth moods, caps them at 118 BPM, and keeps the 100 BPM cap for calm moods.
  - A synth/neon/80s/retro-futuristic genre gets `dreamwave` as its base mood and rotates dreamwave, synthwave, darkwave, dreamwave, ambient. The fallback BPM is clamped into each mood's Chiptune range.
  - `chipFor(genreText)` checks in this order: the user's chip, the palette, a synth genre (`dreamcast`), a 90s/PlayStation genre (`ps1`), else `snes`.
  - Other genres get exactly the old plan. Tests pin this.
- `src/engine/vn/agents/composer.ts`: the composer prompt gets `CHIPS` and `MUSIC_MOODS` instead of the hard-coded lists.
- `seed/prompts/composer/plan_music.md`: the prompt says when to pick ps1 or dreamcast and when to use a synth mood. The BPM guidance is 55-90 for calm moods and 80-110 for synth moods.
- `src/engine/vncli.ts`, `src/engine/mcp/tools.ts`, `docs/mcp-guide.md`: they name the seven chips (plus a guide bullet on the synth moods).
- Tests: new `tests/chip-plan.test.ts` (schema, merge, fallback, pinned old plans). `tests/chiptune-sfx.test.ts` checks that `compose_sfx` receives `chip: 'dreamcast'`.
- `ROADMAP.md` Done row, `.claude/tickets/VNO-51-ps1-dreamcast-chips/plan.md`.

### midi-generator, branch `MDI-11_mcp-prompts-seven-chips` (from `master` @ 3c0276d)
- `src/main/mcpContent.ts`: the `compose_track` and `remix_to_chip` MCP prompts list the seven chips, and "synthwave" is a mood example. With no chip given, the `compose_track` prompt no longer forces `nes`: the mood picks the chip, as the tool does.
- `tests/mcp/assets.test.ts`: a new test for these prompt texts. `ROADMAP.md` MDI-11 paragraph, `.claude/tickets/MDI-11-mcp-prompts-seven-chips/plan.md`.

### creative-hub (master, uncommitted)
- `.claude/skills/make-visual-novel/SKILL.md`: the chip list, when to pick ps1 or dreamcast, the synth moods, reverb/DSP `chipConfig` for hand-made songs, and `compose_sfx` on both chips.
- `README.md` chiptune row, `ROADMAP.md` HUB-18 row, this plan and changelog.

### Deviations
- The fallback BPM for synth moods is clamped to each mood's range. The old slow tempos sat below the synthwave and darkwave minimums, and the plan did not cover this case.
- MDI-11 changed behaviour, not only wording: the old prompt sent `"chip":"nes"` when no chip was given, which contradicted the tool.
- No `SEED_HISTORY` entry was added. Unedited data folders refresh from the hash recorded in `.seed-hashes.json`, as with the earlier `plan_music.md` edits.
- Nothing is committed: the user has not asked for commits yet.

### Verification
- VN Studio: typecheck passes. 83 files and 1131 tests pass. I re-ran the 3 chip test files: 43 tests pass. Lint has 1 error in `scripts/shot-game.mjs:111` (`no-empty`), which the implementer reports is also on master.
- Chiptune Studio: `tsc` for both projects passes, `eslint .` is clean, and 79 files and 1183 tests pass.
- Live MCP against the running Chiptune Studio (7458, built master with MDI-10), `.claude/temp/hub18/live.mjs`: I rendered dreamwave/dreamcast 42.7 s, darkwave/ps1 38.4 s, synthwave/ps1 35.6 s and outrun/dreamcast 33.7 s to ogg, plus stingers on ps1 and dreamcast and a 20 s Dreamcast rain ambience. Every ffprobe duration equals the reported one.

### Not run
- A VN Studio pipeline run with a synth book (the planner on a real model, then the build). The new VN Studio code ran in unit tests only, not live.
- Listening: nobody has listened to the renders.

### Follow-ups
- A synth production that the user plays.
- The ideas for using the chips more in VNs, in the session summary: stingers per scene, leitmotifs, per-chapter reverb, battle/chase tracks.
