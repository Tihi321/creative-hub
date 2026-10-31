# HUB-18: PS1 and Dreamcast music in visual novels

Chiptune Studio MDI-10 (merged, midi-generator `master` @ 3c0276d) added two sample chips, `ps1` (PlayStation SPU, hardware reverb) and `dreamcast` (AICA, DSP reverb/chorus/delay), and four `compose_track` moods: `synthwave`, `outrun`, `darkwave`, `dreamwave`. VN Studio cannot use them: its chip list is hard-coded to five chips (zod enum, UI select, CLI, composer prompt) and its music planner only accepts calm moods at 50-100 BPM. This ticket makes VN Studio pick and pass them, and documents it in the hub.

Scope: music and SFX/ambience through the existing MCP path (VN Studio -> Chiptune Studio `compose_track` / `compose_sfx`). The Chiptune Studio agent on the ACP proxy already sees the new chips through the same tool texts (MDI-10 E2), so no ACP change. New VN features (per-scene stingers, leitmotifs, ...) are recommendations only.

## 1. VN Studio, ticket VNO-51, branch `VNO-51_ps1-dreamcast-chips` from `master`

Repo `C:\projects\Personal\visual-novels-orchestrator`.

- `src/shared/vn.ts`: `CHIPS` gets `'ps1'` and `'dreamcast'` appended (order of the old five unchanged). Everything that reads `CHIPS` (zod `music.chip`, `LookTab.tsx` select, `vncli.ts` `pick('chip', CHIPS)`) follows.
- `src/engine/studios/chip-plan.ts`:
  - `SYNTH_MOODS = ['dreamwave', 'synthwave', 'darkwave', 'outrun'] as const` (calmest first) and `MUSIC_MOODS = [...CALM_MOODS, ...SYNTH_MOODS]`. `mergeChipPlan` accepts a mood in `MUSIC_MOODS`.
  - BPM cap: `MAX_BPM` stays 100 for calm moods; a synth mood may go to `MAX_SYNTH_BPM = 118` (Chiptune's own ranges: dreamwave 80-100, synthwave 96-118, darkwave 88-112, outrun 108-118).
  - `GENRE_MOOD`: a new first entry `/synthwave|retrowave|outrun|vaporwave|neon|\b80s\b|1980s|retro-?futur/i -> 'dreamwave'`; the existing entries and their order stay, so no existing book's plan changes.
  - Fallback rotation for a synth book: base `dreamwave`, then `synthwave`, `darkwave`, `dreamwave`, `ambient` (no outrun by default: too fast under reading). Other books keep today's rotation exactly.
  - `chipFor` takes optional `genreText`: user chip first, then palette (gb / nes as today), then a synth genre -> `dreamcast`, a `/ps1|playstation|psx|y2k|\b90s\b|1990s/i` genre -> `ps1`, else `snes`. Callers in `chip-plan.ts` pass `genreText` (already in `fallbackChipPlan` opts).
- `src/engine/vn/agents/composer.ts`: `chips: asJson(CHIPS)` instead of the literal list; `moods: asJson(MUSIC_MOODS)`.
- `seed/prompts/composer/plan_music.md`: chip line names what fits (snes warm and gentle, gb small cozy, nes bright simple, ps1 for late-90s, moody, noir, gothic or melancholy books with deep reverb, dreamcast for lush, neon, dreamy, retro-futuristic books with chorus). Mood line: the synth moods only for books whose setting or tone is 80s / neon / retro-futuristic / cyber / noir; `dreamwave` is the calmest and the usual pick, `darkwave` for dark chapters, `synthwave` for driving ones, `outrun` only for a chase or a climax. BPM: calm moods 55-90; synth moods 80-110. The seed refresh (`seedRefresh.ts`) updates unedited data folders; if the seed hash history needs the old hash recorded, add it.
- `src/engine/vncli.ts` help line: `--chip nes|gb|genesis|snes|pce|ps1|dreamcast|auto`.
- `src/engine/mcp/tools.ts` `vno_update_settings` text: after `chip`, name the seven chips (one short clause).
- `docs/mcp-guide.md`: one sentence where chiptune music is described: the seven chips and the four synth moods.
- Tests (vitest, existing `tests/studios-generate.test.ts` style or a new `tests/chip-plan.test.ts`):
  - `mergeChipPlan` keeps `ps1` / `dreamcast` and a synth mood; clamps a synth mood at 118 and a calm one at 100; an unknown mood still falls back.
  - `fallbackChipPlan` for a "neon 80s synthwave" genre gives `dreamwave` on `dreamcast`; a "90s" genre gives `ps1`; a mystery / kids / plain genre gives exactly today's plan (pin a few).
  - The zod settings schema accepts `music.chip: 'ps1'`.
  - `compose_sfx` passes `chip: 'dreamcast'` through (existing chiptune-sfx test style).
- Verify: `yarn typecheck`, `yarn lint`, `yarn test`. Changelog in `.claude/tickets/VNO-51-ps1-dreamcast-chips/changelog.md`, roadmap row in VN Studio `ROADMAP.md` "Done". Left uncommitted until the user says to commit.

## 2. Chiptune Studio, ticket MDI-11, branch `MDI-11_mcp-prompts-seven-chips` from `master`

Repo `C:\projects\Personal\midi-generator`.

- `src/main/mcpContent.ts`: the `compose_track` and `remix_to_chip` MCP prompt arguments list the seven chips (`nes, gb (8-bit), genesis, snes, pce (16-bit), ps1, dreamcast (sample chips)`) and the `compose_track` mood examples include `"synthwave"`.
- Any test that pins these strings updated. `yarn typecheck`, `yarn lint`, `yarn test`. Changelog and ROADMAP paragraph. Left uncommitted until the user says to commit.

## 3. Hub (this repo, done by the orchestrator, not the implementer)

- `.claude/skills/make-visual-novel/SKILL.md`: chip list with ps1 / dreamcast and when to use them, the synth moods, and the SFX chip.
- `README.md` chiptune row: mentions PS1 / Dreamcast.
- `ROADMAP.md`: HUB-18 row.

## 4. Live check

With Chiptune Studio running on 7458 (headless, `hub.ps1 start chiptune-studio`): over MCP, `compose_track {mood: "dreamwave", chip: "dreamcast", bpm: 90, ...}` and `{mood: "darkwave", chip: "ps1"}` + `render_audio` to ogg, and `compose_sfx {kind: "stinger", chip: "ps1"}`; ffprobe the files. A full VN Studio build with a synth book is left for a production (the user listens).

## Done when

VNO-51 and MDI-11 on their branches (uncommitted until the user says) with green checks, the hub docs updated, the live renders exist, and the final list says DONE / NOT DONE / UNTESTED per item.
