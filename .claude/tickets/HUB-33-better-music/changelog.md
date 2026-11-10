# HUB-33 changelog

## 2026-11-10 — HUB-33: gm SoundFont chip, varied compose, 33 tracks re-scored, site republished

All four tools changed; 6 works re-scored in style A (user pick), levelled to -18 LUFS, rebuilt, published and live. Ticket left at `in-progress` for the director's check; C17 (the user's listen) is open.

### midi-generator (Chiptune Studio) — branch `MDI-14-15_soundfont-variety`, uncommitted
- `package.json`, `yarn.lock`: `spessasynth_core` 4.4.9 exact (brings stb-vorbis 0.0.7, fflate 0.8.3); yarn.lock metadata v8 → v10.
- New `src/core/chips/gm.ts`, `src/core/instruments/presets/gm.ts`, `src/core/synth/chips/soundfont.ts`, `src/main/soundfont.ts`, `src/tools/soundfontLoad.ts`: the `gm` chip (M1-M12 melodic, D1-D4 drums on MIDI ch 10), 64 `gm.<role>.<name>` presets, a SoundFont bus playing spessasynth per tick, one `_gm` mix stem; the SoundFont is read from `~/ChiptuneStudio/soundfonts/` (`CHIPTUNE_STUDIO_HOME`), a missing file errors with the path and the source URL; `soundfont_status` tool.
- New `src/tools/composer/{palettes,textures,variety,rng}.ts` and `composer.ts`: textures, 23 gm palettes, form A/AB/ABA/AABA, `avoid` with a warning when a rule cannot be met, `fingerprint` always returned. Old chips and old seeds unchanged (textures and palettes on gm only).
- `src/core/theory/{moods,progressions,drums}.ts`: moods playful, curious (no longer an alias of mysterious-calm), focus, wonder, cafe, adventure-light, storybook.
- Worklet, render worker, headless render, MIDI export/convert, `defs/studio.ts`, `mcpContent.ts`, `docs/llm-guide.md` (+ `guideText.ts`), README, ROADMAP (MDI-14, MDI-15; MDI-16 cut).
- Tests: `tests/core/gm.test.ts` (+ `miniSf2.ts`), `tests/main/soundfont.test.ts`, `tests/tools/variety.test.ts`, `tests/e2e/gm.spec.ts`; `composerPin` gained 4 pinned seeds.

### edu-game-studio — branch `EGS-70_music-variety`, uncommitted
- `src/shared/media.ts`, `src/shared/music.ts`: `gm` chip, `fingerprint` on versions, `texture` / `form` / `instruments` on tracks.
- `src/engine/studios/chip-plan.ts`: new moods, textures, forms, `maxBpmFor` (gm 128), `chipFor` gm unless pixel / retro.
- `src/engine/edu/music.ts`: a distinct mood, tempo, texture and form per area; genre-specific ACE-Step words; per-line `provider`.
- `src/engine/edu/music-service.ts`, `src/engine/assets/{generate,generate-audio}.ts`: `avoid` from the course's other tracks, fingerprint stored; new `src/engine/assets/loop.ts`: equal-power 3 s seam crossfade for ComfyUI music, loop points set.
- `seed/prompts/composer/plan.md`, `docs/mcp-guide.md`, ROADMAP (EGS-70); tests `audio-loop`, `music-plan`, `music-generate`, `chip-plan`, `media-pipeline`, `studio-fakes`.

### visual-novels-orchestrator — branch `VNO-66_music-variety`, uncommitted
- `src/shared/vn.ts`: `gm`, `fingerprint` on versions. `src/engine/studios/chip-plan.ts`: `chipFor` gm for picture books and kids / children / bedtime genres unless the chip is set or the art is pixel; a 7-entry gm rotation.
- `src/engine/studios/{chiptune,music}.ts`, `src/engine/vn/agents/composer.ts`, `src/engine/assets/generate.ts`, `src/engine/vn/handlers.ts`: texture / form / instruments / avoid passed, fingerprint kept; new `src/engine/studios/loop.ts` seamless ComfyUI loop.
- `src/engine/mcp/tools.ts`, `src/engine/vncli.ts` help text; `docs/mcp-guide.md`; ROADMAP (VNO-66); tests `chip-plan`, `music-loop`, `studios-generate`.

### creative-hub-web — merged to master `c203ad9`, pushed
- `scripts/lib/encode.mjs`: `isMusic`, recipes `ogg-music@1:q5` and `mp3-music@1:160k` (re-encode only above 192 kbps), dry-run estimate. `tests/unit/publish-guard.test.mjs`, `README.md`.
- `public/play/` of the 6 works and `content/publish-manifest.json` republished (`104e1a8`, `51d0591`).

### creative-hub — branch `HUB-33_better-music`, uncommitted
- `.claude/skills/make-edu-game/SKILL.md`, `.claude/skills/make-visual-novel/SKILL.md`: the "prefer ACE-Step or gm over SNES for kids and learning" guidance, per-area defaults, how to set a picked style, levelling, `gm` in the chip list.
- `README.md` Chiptune Studio row; `services.json` chiptune-studio `dataFiles`; `ROADMAP.md` row 27 and per-tool cells; `runs/hub-33-better-music.md`.

### Data (not in git)
- `~/ChiptuneStudio/soundfonts/GeneralUser-GS.sf2` (v2.0.3, sha256 9575028c…8cfe) and its licence.
- Edu: 31 new v2 music versions in the 4 courses (v1 kept), `music.json` from the composer task, `media.music.chip: gm`, rebuilt. VN: `music_01` v2 in 2 books (v1 kept), `music.json` track plans, `music.chip: gm`, rebuilt.

### Deviations
- MDI-16 (SNES clean) and C7 cut by the user; the Bell's C was a second ACE-Step style.
- New tracks levelled in place to -18 LUFS with a plain gain (ACE-Step came out -15 to -14 LUFS with peaks to -0.1 dB; gm -25 to -16), originals in `.claude/temp/hub-33/backup/`; ACE-Step tracks in Edu are mp3 (ComfyUI's output).
- Edu style picks were applied by answering the composer task (model path, `client`, $0) instead of the fallback; gm palettes set through `instruments` (Edu has no `palette` field).
- VN: track plans written in `music.json` by hand; rebuild via `vno_build` + `vno_lint` instead of `vno_run_pipeline {from: "stage"}` (that re-stages the book with a model task; those jobs were dropped).
- Tool branches were not merged before T8: Edu and VN ran from the uncommitted branch builds.
- Suncev-sustav audition: A and C share the menu / unit tracks, so a boss track was added to show the difference.

### Verification
- midi-generator: vitest 1197 pass; typecheck, lint, gen:guide, build ok; e2e gm 2/2 + 24 old specs. C1-C6 pass (C4 in headless Electron).
- edu-game-studio: 528/529 (1 timeout that fails on baseline); typecheck, lint, build:engine ok. C8, C10 pass.
- visual-novels-orchestrator: 1154 pass; typecheck, lint, build:engine ok. C9, C10 pass.
- creative-hub-web: unit 5/5, check-site PASSED (471.7 MB), e2e 55/55, publish smoke 6/6, Pages success, C14 6/6 sizes match.
- C12: all 33 tracks -18.3 to -17.9 LUFS, peaks ≤ -1.8 dB, no clipping. C13: edu_build ok ×4, edu_lint 0 errors ×4, bot 28/28 (every shell, 375x667 and 1280x800, 0 console / media errors); vno_build + vno_lint ok ×2.
- Browser: gm music plays in the Bell build; Edu menu / unit tracks load on area change.
- Not run: listening on real speakers (C17), the seam of the mp3 loops by ear, C7 (cut).

### Follow-ups
- Commit / merge the three tool branches and the hub branch (not asked yet).
- `discoveries.md`: loudness normalise step in Edu / VN, VN font 404s, stale VN prompt label, VN replace / import behaviour, test timeouts, compose_sfx text.

### Commit status
creative-hub-web committed and pushed (`c203ad9`). midi-generator, edu-game-studio, visual-novels-orchestrator and creative-hub: uncommitted on their ticket branches.
