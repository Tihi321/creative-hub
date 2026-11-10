---
status: in-progress
request: REQ-0023
repos: [creative-hub, midi-generator, edu-game-studio, visual-novels-orchestrator, creative-hub-web]
branch: HUB-33_better-music
updated: 2026-11-10
---

# HUB-33: better music (SoundFont sound in Chiptune Studio, varied tracks, re-score 6 works)

User, word for word: "as well music in landuage learning and learning games it is same and bad, we need to change it, same as in bell and the bicycle and snail, not sure seems like something in music is dihtering" / "ok and maybe we should add better chiptune midis that we can use, someting more advanced thatn sega saurn or someting tha twe have".

Reading: the **full** one. Chiptune Studio gets a real-instrument SoundFont sound that the apps can use. Composition gets more varied. All 33 tracks of the 6 works are re-scored, the user auditions them, and the works are rebuilt and republished.

## Why it sounds "dithered" and "the same" (confirmed in code)

All 33 tracks were made by Chiptune Studio on the SNES chip with the calm-mood presets.

**Grit (the "dithering"):**
- Every SNES sample goes through a real BRR encode and decode: 4-bit residuals in 16-sample blocks (`midi-generator/src/core/synth/samplegen/brr.ts`, used by `snes.ts` presets).
- The samples are generated at low rates: kick and tom 16 kHz, harp, pluck, guitar and snare 22.05 kHz (`samplegen/bank.ts`, the `RATE(...)` params).
- Leads are 256-sample single-cycle loops pitched across octaves (`bank.ts` `lead`, `loopLen: 256`).
- Playback runs at the DSP's native 32 kHz with Gaussian interpolation, then a cubic resample to the output rate (`synth/chips/spc700.ts`, `SNES_DSP_RATE = 32000`). Quantisation noise, aliasing and a hissy floor are the result.
- There is no extra bit-depth reduction after the mix.

**Lossy re-encodes on top:**
- Chiptune exports ogg at `-q:a 6` (`src/main/ffmpeg.ts`).
- creative-hub-web then re-encodes every ogg above 112 kbps at `libvorbis -q:a 2` (`creative-hub-web/scripts/lib/encode.mjs`, `RECIPES.ogg = 'ogg@1:q2'`, `AUDIO_TARGET_KBPS = 96`). On this sparse material q2 comes out at about 53 kbps on average: 37 music oggs, 20.7 MB, about 3,135 s.
- Low-bitrate Vorbis on noisy 4-bit material adds pre-echo and a swirl that sounds like dithering.

**Sameness:**
- `compose_track` (`midi-generator/src/tools/composer.ts`) has one texture: bass, 1-2 pads, lead in MIDI 60-84, optional arp. The 4/8-bar progression repeats with no B section.
- For calm SNES moods, `softPresetRef` always picks `snes.flute.soft` / `snes.bell.soft`, `snes.pad.soft-strings`, `snes.bass.soft` and `snes.strings.swell`.
- Edu's fallback plan (`edu-game-studio/src/engine/edu/music.ts`: `AREA_MOOD` and `fallbackMusicLines`, plus `studios/chip-plan.ts`) gives only calm moods, BPM 64-100 (`MAX_BPM = 100`) and `chip: 'snes'` (`chipFor` default).
- HUB-28 used `edu_music_plan {fallback:true}` with `provider: "chiptune"` (`runs/hub-28-edu-mobile-music.md`). The picture books used chiptune SNES too (`runs/the-bell-and-the-bicycle.md`, `runs/the-snail-and-the-salad.md`).
- Edu and VN pass only `mood, chip, bpm, key, bars`. They never pass `variation` or `instruments`.

## Scope

- **A. `gm` chip in Chiptune Studio.**
  - A General MIDI SoundFont chip: 12 melodic voices plus 4 drum voices.
  - Played by the pure-JS SoundFont synth `spessasynth_core` in both the audio worklet and the headless renderer.
  - Uses the GeneralUser GS SoundFont, which lives in the data folder and is not in the repo.
  - GM presets come by role, so `compose_track`, `convert_chip`, `export_midi` and the tracker all work.
- **B. Variety in `compose_track`.**
  - Textures, a per-mood instrument pool picked by seed, A/B form, and lead range per instrument.
  - Light percussion for calm moods.
  - New moods for kids and learning.
  - A returned `fingerprint` plus an `avoid` input, so the tracks of one work never share a texture, lead or tempo band.
  - Edu and VN planners spread mood, tempo and texture across a work and pass `avoid`.
- **C. SNES `fidelity: "clean"`.**
  - An opt-in chip option: no BRR quantisation, 32 kHz generation, longer lead loops.
  - The default stays `authentic`, so the golden SNES render hashes are unchanged.
  - Decision and reason: SNES grit is the chip's identity and many works rely on it. "Clean" gives a softer retro option for an audition candidate at little cost (the bank already takes rate and loop parameters). Nothing in D depends on it, so it can be cut first if time runs short.
- **D. Re-score the 6 works.**
  - Mix ACE-Step (ComfyUI, local, $0) and the new `gm` sound, in a distinct style per work.
  - The user auditions 2-3 styles per work, then all tracks are made, each work is rebuilt in its own tool, and creative-hub-web is republished.
  - The publish bitrate for music goes up within the budget.
- **E. Hub wiring.**
  - The `make-edu-game` and `make-visual-novel` skills say to prefer `gm` or ACE-Step over SNES for kids and learning unless asked.
  - Also update the README tool rows, the `services.json` docs, ROADMAP row 27 and the tools' own ROADMAPs.

## Out of scope

- Flow Music or any paid music. No Flow credits.
- Changing voices, SFX or ambience. SFX stay chiptune `compose_sfx`. A SoundFont SFX set comes later.
- Bundling the SoundFont in the installer or committing it to git.
- 3/4 meter: `ROWS_PER_BAR = 16` is hard-wired in `composer.ts`. Waltz feel is faked with a 3-against-4 comping pattern, or deferred.
- The 11 VN works with mp3 music (circuit-breaker etc.) and the other picture-book or VN tracks not named here.
- An AICA microcode DSP and other MDI-10 follow-ups.
- Starting Scriptorium. It is not needed.

## Files and modules to touch

**midi-generator (Chiptune Studio).** Branch `MDI-14-16_soundfont-variety` from `master` (`dc6ac95`). Tickets MDI-14 (gm chip), MDI-15 (variety), MDI-16 (SNES clean).
- `package.json` / `yarn.lock`: add `spessasynth_core`, pinned to an exact release at least two weeks old (Apache-2.0).
- `src/core/types.ts`: add `'gm'` to `ChipId` and `CHIP_IDS`; add `GmConfig {chip:'gm', soundfont: string, reverb: 0..1, chorus: 0..1}`; add instrument kinds `sf-program {program 0-127, bank, ...}` and `sf-drum {key: GM percussion note, bank}`.
- `src/core/chips/gm.ts` (new) and `src/core/chips/index.ts`:
  - `gmProfile` with channels `M1`..`M12` (kind `gm-melodic`, MIDI channels 0-8 and 10-12) and `D1`..`D4` (kind `gm-drums`, all on MIDI channel 9).
  - Allowed effects: `v`, `Xxx`, `4xy` (mod wheel / vibrato), `1xx`/`2xx`/`3xx` (pitch bend, RPN range ±12), `Sxx`, `Gxx`, `Exx` (reverb send CC91), `Fxx`, `Bxx`/`Dxx`/`C00`.
  - The arpeggio effect `0xy` is a strict error with the fix "put chord tones on separate channels".
- `src/core/instruments/presets/gm.ts` (new) and `presets/index.ts`, with `gm.<role>.<name>` ids:
  - piano grand 0, epiano 4, celesta 8, glock 9, musicbox 10, vibes 11, marimba 12, xylophone 13, accordion 21, guitar nylon 24 / steel 25, bass upright 32 / finger 33, violin 40, cello 42, pizzicato 45, harp 46, timpani 47, strings ensemble 48 / slow 49, choir aah 52, trumpet 56, tuba 58, horn 60, brass section 61, oboe 68, bassoon 70, clarinet 71, flute 73, recorder 74, panflute 75, whistle 78, ocarina 79, pad warm 89 / halo 94, kalimba 108.
  - Drum presets: kick 36, snare 38, side-stick 37, hat 42, open hat 46, ride 51, crash 49, tambourine 54, shaker / maracas 70, claves 75, woodblock 76, triangle 81, conga 63/64, bongo 60/61, and a brush kit (the GS brush kit, bank 128 program 40, if the SoundFont has it).
  - Update `ROLE_CHANNELS` in `instruments/roles.ts` for gm.
- `src/core/synth/chips/soundfont.ts` (new):
  - `SoundFontBus` on `SharedBus` (the `sampler/bus.ts` pattern, as `EchoBus` uses) holds one spessasynth processor per render.
  - Each `GmVoice.control()` turns the channel's note, volume, pan and pitch into MIDI events at the tick boundary.
  - The bus renders the block. Stems come from per-channel outputs if spessasynth gives them; otherwise there is one mix stem with a warning.
  - Register the voice with `registerVoice('gm','gm-melodic'|'gm-drums', ...)` in `synth/chips/index.ts`; add a mix profile.
- `src/main/soundfont.ts` (new):
  - Finds `~/ChiptuneStudio/soundfonts/<chipConfig.soundfont>` (default `GeneralUser-GS.sf2`; `CHIPTUNE_STUDIO_HOME` respected) and loads the bytes once.
  - When the file is missing, it raises an error naming the path and the source URL.
- `src/renderer/audio/audioEngine.ts` and `protocol.ts`: post the SoundFont bytes to the worklet once (transferable).
- The headless path in `src/core/synth/render.ts` and `src/tools/audioExport.ts`: inject the SoundFont bytes.
- `src/core/codecs/gmMap.ts`, `convert.ts`, `midi.ts`: gm uses the GM program directly on export, and `convert_chip` maps role to program.
- `src/tools/composer.ts`, split into `src/tools/composer/` if it grows past about 1,200 lines (`textures.ts`, `palettes.ts`):
  - `TEXTURES`: `pad-lead` (today's), `broken-chord` (piano or harp arpeggio), `ostinato`, `chorale`, `march`, `bossa` (syncopated comp), `lullaby-rock`, `pizzicato-walk`.
  - `PALETTES[mood][chip]`: the instrument pools that `pickPalette(seed)` chooses from.
  - `form`: `"A"` | `"AB"` | `"ABA"` | `"AABA"`; B uses a second progression (IV or vi centre).
  - Lead range comes from the instrument's preset range, not a fixed 60-84.
  - Calm percussion roles: shaker, side-stick, brush, triangle.
  - `ComposeOptions` gets `texture?`, `form?`, `palette?` and `avoid?: Fingerprint[]`.
  - `ComposeResult` gets `fingerprint {texture, lead, pad, bass, bpm, key, scale, form}`.
  - With `avoid` given, re-roll (up to 8 tries, deterministic per seed) until no entry shares the texture and lead, the tempo is at least 8 BPM from the others, and the key differs from the last entry.
- `src/core/theory/moods.ts`: new moods `playful`, `curious`, `focus`, `wonder`, `cafe`, `adventure-light`, `storybook`. Each has BPM ranges (`focus` 80-100, `playful` 100-126, `adventure-light` 104-128), progressions in `progressions.ts`, and drum styles in `drums.ts` (light ones).
- `src/core/chips/snes.ts`, `samplegen/bank.ts`, `spc700.ts` and the snes presets (MDI-16): `SnesConfig.fidelity?: 'authentic'|'clean'`. Clean means:
  - samples skip `encodeBrr` quantisation (the PCM is played directly) but still count toward ARAM;
  - recipe default rates go to 32 kHz;
  - `lead` uses `loopLen` 2048;
  - Gaussian interpolation stays.
- `src/tools/defs/studio.ts`: add the new compose params; add a `soundfont_status` tool (file present, name, size, preset count).
- `src/main/mcpContent.ts`: list gm in the prompts.
- `docs/llm-guide.md`: a gm section, textures and form, fidelity. Then run `yarn gen:guide`.
- `README.md` and `ROADMAP.md`: the MDI-14 to MDI-16 rows.
- Tests: `tests/` (vitest), few and important, per `test-discipline`.

**edu-game-studio.** Branch `EGS-70_music-variety` from `master` (`3280274`).
- `src/shared/media.ts` `CHIPS`: add `'gm'`.
- `src/shared/music.ts`: add `texture?`, `form?` and `instruments?` to `MusicTrackEntry`; `MAX_BPM` per chip (gm 128).
- `src/engine/studios/chip-plan.ts`:
  - `chipFor` returns `'gm'` when the course is not pixel style (pixel keeps snes / nes / gb as now).
  - `MUSIC_MOODS` gets the new moods.
  - Fallback BPM and key tables are spread wider.
- `src/engine/edu/music.ts` `AREA_MOOD` and `fallbackMusicLines`, one distinct mood, texture and tempo band per area:
  - menu `wonder`/`playful` 96-110
  - units rotate `focus`/`curious`/`cafe`/`storybook` with distinct textures
  - boss `adventure-light` 116-126
  - end `storybook` warm
  - castle `mysterious-calm` (chorale on organ or choir)
  - rpg-overworld `adventure-light` (march or pizzicato-walk)
  - rpg-battle `playful` 120+
  - The ACE-Step prompt words per area go genre-specific: no more "calm instrumental ... slow tempo" on every track.
- `src/engine/studios/chiptune.ts` / `music.ts`: pass `texture`, `form`, `instruments` and `avoid` (the fingerprints of the work's earlier tracks); store the fingerprint in the asset version.
- `src/engine/assets/generate-audio.ts`, ComfyUI music: make the loop seamless if not done already. Check first; today no loop points are written for comfy. Method: an ffmpeg equal-power crossfade of the last 3 s into the start, then `loopStartSec 0` and `loopEndSec` set.
- `docs` / `contracts.md` lines on the music plan.

**visual-novels-orchestrator (VN Studio).** Branch `VNO-66_music-variety` from `master` (`9598d32`).
- `src/shared/vn.ts` and the chip list: add `'gm'`.
- `src/engine/studios/chip-plan.ts`:
  - `chipFor` returns `'gm'` for genre `kids|children|picture book|bedtime` and for `presentation: picture-book`, unless `music.chip` is set or the style is pixel.
  - Add the new moods.
- `src/engine/studios/chiptune.ts` / `music.ts` and `src/engine/vn/agents/composer.ts`: pass `texture`, `form`, `instruments` and `avoid` across `music_0n` of one book.
- The ComfyUI music seamless loop: same check-and-add as Edu.
- `docs/mcp-guide.md`.

**creative-hub-web.** Branch `WEB-08_music-rescore` from `master` (`3ce3a75`).
- `scripts/lib/encode.mjs`, music-only recipe:
  - `isMusic(rel)` matches `/assets/mus-[^/]+/` and `/audio/music_\d+\./`.
  - Music ogg: re-encode at `libvorbis -q:a 5` when the source is above 192 kbps, else copy.
  - Music mp3: 160 kbps when the source is above 192 kbps.
  - Recipe ids `ogg-music@1:q5` and `mp3-music@1:160k`. Speech and SFX stay on q2 / 96k.
  - Update the `--dry-run` estimate.
- `content/catalog.json`: blurbs only if they mention "chiptune" (check).
- `public/play/<the 6 works>/` by `npm run publish --only <workId>`; `content/publish-manifest.json`.

**creative-hub.** Branch `HUB-33_better-music`.
- `.claude/skills/make-edu-game/SKILL.md` and `.claude/skills/make-visual-novel/SKILL.md`: music guidance.
- `README.md`: the Chiptune Studio row names the gm chip and the SoundFont path.
- `services.json`: the chiptune-studio `docs` line notes the SoundFont data file.
- `ROADMAP.md` row 27 and the per-tool table ("Open there").
- `runs/hub-33-better-music.md` (new run log).

## Tasks

Order: T1 → T2 → (T3, T4 and T5 in parallel) → T6 → T7 (audition) → T8 → T9 → T10.

**T1. Downloads (user yes first). Owner: hub.**
- Inputs: the user's answer to Q1.
- Outputs:
  - `~/ChiptuneStudio/soundfonts/GeneralUser-GS.sf2`, with its licence file next to it as `GeneralUser-GS-LICENSE.txt`, and the sha256 in the run log;
  - `spessasynth_core` installed by yarn in midi-generator, as part of T2.
- Contract: T2 tests read the SoundFont path from `CHIPTUNE_STUDIO_HOME` or skip with a clear message. CI has no SoundFont, so the unit tests use a tiny SF2 fixture generated in the test, or a skip.

**T2. MDI-14 gm chip. Owner: midi-generator implementer.**
- Inputs: T1, and the files listed above.
- Outputs: the gm chip, presets, voice, SoundFont loader, worklet transfer, `soundfont_status`, export and convert, guide.
- Contract with T3, T4 and T5:
  - `compose_track {chip:"gm", ...}` and `render_audio {format:"ogg"}` work headless on port 7458.
  - Preset ids are `gm.<role>.<name>`, so `instruments: {"M4":"gm.lead.clarinet"}` resolves.
  - A missing SoundFont gives an error whose text contains `soundfonts` and the URL.
  - Rendering is deterministic: the same song and seed give the same bytes.
  - All 7 old chips render bit-identical (the existing golden and hash tests pass unchanged).

**T3. MDI-15 variety, plus MDI-16 SNES clean. Owner: midi-generator implementer, after T2 on the same branch.**
- Outputs: textures, palettes, form, new moods, fingerprint and avoid, calm percussion, and `fidelity`.
- Contract: `compose_track` without the new params and with an old mood gives exactly today's song (old seeds stay stable, checked by a hash test). The new params are additive. `fingerprint` is always returned. With `avoid`, the result's fingerprint satisfies the distinctness rule or a `warning` says which rule could not be met.

**T4. EGS-70. Owner: edu-game-studio implementer. Needs the T2/T3 contract; can stub the client in tests.**
- Outputs: gm in CHIPS, a varied fallback and model plan, avoid / fingerprint plumbing, and the comfy seamless loop.
- Contract with T8: `edu_media_settings {music:{provider, chip:"gm"}}` and per-track `provider` overrides in `music.json` work. `edu_music_plan` gives distinct mood, texture and tempo per area. `edu_asset_generate kind=music` makes a new version (`v2.ogg`, ...) without deleting v1.

**T5. VNO-66. Owner: VN Studio implementer. Same shape as T4.**
- Contract with T8: `music: {provider:"chiptune", chip:"gm"}` or `{provider:"comfy"}` per project; `vno_asset_regen` / `vno_asset_replace` for `music_01` makes a new version.

**T6. WEB-08 publish recipe. Owner: creative-hub-web implementer. Independent; can run any time before T9.**
- Output: the music recipe.
- Contract: `npm run publish --dry-run` reports the total for dist. It must stay at or under 520 MB, leaving 80 MB of headroom inside 600. If it does not, music falls back to q4 / 128k.

**T7. Audition. Owner: hub (director / producer).**
- Inputs: T2 and T3 built (`hub.ps1 build chiptune-studio`), ComfyUI and comfy-mcp running, and Chiptune Studio started for this work only (`hub.ps1 start chiptune-studio comfyui comfy-mcp`).
- Method: per work, render 2-3 candidates of one representative track:
  - Edu: `mus-menu` plus one unit track;
  - picture books: `music_01`.
- Tools: comfy-mcp `generate_music {engine:"ace-step-v1-instrumental", tags, seconds, seed, out}` and Chiptune `compose_track` + `render_audio`, written to `creative-hub/.claude/temp/hub-33/audition/<work>/<letter>-<style>.ogg`.
- Before listening, check each candidate:
  - `ffmpeg -af ebur128` shows integrated loudness of -18 LUFS ±2;
  - true peak is at or below -1 dBTP;
  - `astats` shows no clipping.
- Then a local `audition.html` (scratch, not published) lists each work's candidates with `<audio>` tags. The user listens and picks per work; record the picks in the run log.
- Candidates (style letter, source, target):

| Work | Tracks to make (asset ids) | A | B | C |
|---|---|---|---|---|
| suncev-sustav (hr, kids, solar system; quiz, encyclopedia, mindmaze, rpg, detective) | mus-menu, mus-unit-u1..u3, mus-boss, mus-end, mus-castle, mus-rpg-overworld, mus-rpg-battle (9) | ACE-Step "cinematic space ambient, celesta, soft synth pads, harp, slow strings, wonder" (menu, units, end) + gm orchestral adventure (castle, rpg, boss: horn, strings, timpani, harp) | all gm: `wonder` / `focus`, celesta, vibes, harp, strings, pad halo | ACE-Step for all 9 |
| deutsch-a1-pilot (beginners; quiz, encyclopedia, mindmaze, rpg) | mus-menu, mus-unit-u1..u4, mus-boss, mus-end, mus-castle, mus-rpg-overworld, mus-rpg-battle (10) | gm Central-European folk-pop: accordion, nylon guitar, clarinet, glockenspiel, upright bass, light drums | ACE-Step "acoustic folk pop, ukulele, whistling, hand claps, cheerful" | gm `storybook` / `playful` chamber: pizzicato, flute, bassoon, marimba |
| deutsch-roleplay-a1 (role-play: cafe, shop, travel) | mus-menu, mus-unit-u1..u4, mus-boss, mus-end (7) | ACE-Step "light bossa nova cafe, nylon guitar, upright bass, brushed drums, vibraphone" | gm `cafe`: bossa texture, nylon guitar, vibes, upright bass, brush kit | ACE-Step "French-German cafe jazz, accordion, piano trio" |
| deutsch-roleplay-b2 (adults, B2) | mus-menu, mus-unit-u1, mus-unit-u2, mus-boss, mus-end (5) | ACE-Step "lo-fi neo-soul, Rhodes piano, soft boom-bap beat, warm bass, focus" | ACE-Step "modern minimal piano and strings, Nils Frahm-like, calm focus" | gm `focus`: epiano, finger bass, side-stick, pad warm |
| the-bell-and-the-bicycle (picture book, watercolour, park, bedtime end; 102 s) | music_01 (1) | gm `storybook`: celesta, pizzicato strings, clarinet, harp, triangle | ACE-Step "gentle children's storybook, music box, soft piano, harp, warm strings" | SNES `fidelity:"clean"` `lullaby` (keeps a retro feel without the grit) |
| the-snail-and-the-salad (picture book, bright flat cartoon, funny) | music_01 (1) | gm `playful`: bassoon, pizzicato-walk, xylophone, tuba, woodblock | ACE-Step "whimsical cartoon orchestra, pizzicato, bassoon, xylophone, playful" | gm `curious`: marimba, kalimba, flute, shaker |

- Output: the picks, recorded in `runs/hub-33-better-music.md`.
- Contract with T8: each work has one chosen style. Its source per area (`comfy` or `chiptune`/gm) and the words or texture are written down.

**T8. Make the full sets in each tool. Owner: hub producer. After the T7 picks and with T4/T5 merged and built (`hub.ps1 build edu-studio vn-studio`).**
- Edu (each of the 4 slugs):
  - `edu_media_settings` sets the picked provider, with `chip:"gm"` where gm;
  - `edu_music_plan` uses the model path (`client` provider, $0), or the fallback, with per-area provider and words from T7;
  - then `edu_asset_generate kind=music`, `edu_wait` and `edu_asset_list`;
  - select the new versions; `edu_build`; `edu_lint`; bot at 375x667 and 1280x800.
- VN (2 books): `vno_set` / settings music, then `vno_asset_regen music_01` (or `vno_asset_replace` with the auditioned file), then `vno_run_pipeline {from:"stage"}` (stage, build, lint).
- Every track gets the T7 loudness, true-peak and clipping check. Each work's set must be pairwise distinct: no two Chiptune tracks share a fingerprint texture and lead; ACE-Step tracks use different tags or seeds.
- Log every asset id, version, seed, engine and fingerprint in the run log.
- Output: 33 new tracks in their tools and 6 rebuilt builds; the old v1 versions are kept.

**T9. Republish. Owner: hub, in creative-hub-web on `WEB-08_music-rescore`.**
- Steps:
  1. Run `npm run publish -- --only <workId>` for each of the 6 works (smoke check on), then `npm run build`, `npm run check` (budget included) and `npm run test:e2e`.
  2. Commit, merge `--no-ff` to master, and push once. Never force.
  3. Wait for the Pages workflow (`gh run watch`).
  4. Then poll the 6 play URLs on `https://tihi321.github.io/creative-hub-web/` and one music file per work, with `curl -I`, every 2 min for up to 30 min. Compare the ETag or Content-Length with the local `public/` file.
- GitHub Pages was slow on 2026-11-08. A slow deploy is not a failure; do not re-push. Past 30 min, record "deployed, CDN not yet updated" and check again later.
- Output: the site live with the new music, and the sizes in the run log.

**T10. Hub wiring and close. Owner: hub.**
- Skills:
  - Both skills, music section: "For kids' and learning works prefer ACE-Step (ComfyUI) or Chiptune Studio `chip: "gm"` over SNES unless the user asks for a retro chip. Give each track of a work its own mood, texture and tempo (pass `avoid`). Audition 2-3 styles with the user before making a full set."
  - `make-edu-game`: the per-area defaults.
  - `make-visual-novel` line 123/135: add `gm` to the chip list.
- README: the Chiptune Studio row.
- `services.json` docs.
- ROADMAP row 27 (style below) and the per-tool "Open there" cells.
- Run log; REQ-0023 status through the scribe.

ROADMAP row to add, in the existing table style:
`| 27 | HUB-33 | Better music: a General MIDI SoundFont chip `gm` in Chiptune Studio (GeneralUser GS, spessasynth), varied compose_track (textures, palettes, form, avoid), SNES clean option, then re-score the 4 Edu games and 2 picture books with ACE-Step and gm after a user audition, republish with a higher music bitrate (`.claude/tickets/HUB-33-better-music/plan.md`, REQ-0023) | `midi-generator` (MDI-14 to MDI-16), `edu-game-studio` (EGS-70), `visual-novels-orchestrator` (VNO-66), `creative-hub-web` (WEB-08), hub | ComfyUI (ACE-Step), Chiptune Studio; SoundFont download (user yes); $0; the user auditions and listens | Planned |`

## Acceptance criteria

- **C1** gm chip renders.
  - Check: vitest `tests/core/gm.test.ts` with a generated mini SF2. A note on M1 and a kick on D1 render non-silent audio at the right times (onset within 1 tick), and two renders are byte-identical.
  - Live: with the real GeneralUser GS, `compose_track {mood:"storybook", chip:"gm", seed:1}` + `render_audio` gives an ogg with peak at or below -1 dBFS and no clipped samples (ffmpeg `astats`).
- **C2** Old chips unchanged. Check: the existing golden and render-hash tests (nes, gb, genesis, snes, pce, ps1, dreamcast) pass with no fixture updated.
- **C3** Missing SoundFont is a clear error. Check: a test with an empty `CHIPTUNE_STUDIO_HOME`. The `render_audio` error names `soundfonts\GeneralUser-GS.sf2` and the source URL; `soundfont_status` reports `missing`.
- **C4** gm works in the app window too. Check: the Playwright `_electron` spec (or a manual check recorded in the run log) opens a gm song and plays it. No worklet error appears in the console, and the SoundFont is posted once.
- **C5** Old compose seeds are stable. Check: a test hashes `composeSong({mood:"peaceful", chip:"snes", seed:7})` and 3 other old mood/chip/seed triples against hashes recorded before T3.
- **C6** Variety rule. Check: a test composes 8 tracks for one work with `avoid` chained. No two share texture and lead; the BPMs are pairwise at least 8 apart, or a warning says which rule could not be met. The fingerprint is always present.
- **C7** SNES clean is opt-in. Check: a test shows `fidelity` absent gives the same render hash as before. With `"clean"`, the SNR of a lead sample against its source PCM is at least 40 dB (`snrDb` exists in `samplegen/brr.ts`); the authentic BRR value is lower.
- **C8** Edu plan spread. Check: an EGS test. `fallbackMusicLines` for a course with mindmaze and rpg gives at least 5 distinct moods across 10 areas, a BPM span of at least 40, and `chip: 'gm'` for a non-pixel course. A pixel course still gets snes.
- **C9** VN chip default. Check: a VNO test. A picture-book or kids project without `music.chip` gets `gm`; `art.style: pixel` keeps today's chip.
- **C10** ComfyUI music loops seamlessly. Check: an Edu and a VN test on a synthetic tone file. After processing, the RMS difference across the loop seam is at most that of any other 50 ms window; `loopEndSec` is set.
- **C11** Publish budget. Check: `npm run check` passes (budget section). dist is at or under 520 MB; record the before and after MB in the run log. Music oggs in `public/` average at least 112 kbps (ffprobe).
- **C12** Loudness match. Check: an ffmpeg `ebur128` table for all 33 new tracks. Integrated loudness is -18 LUFS ±2 and true peak at or below -1 dBTP. Fix by cue volume or a re-render; never ship a clipped file.
- **C13** Builds pass. Check: `edu_build`, `edu_lint` with 0 errors, and the bot at 375x667 and 1280x800 with 0 console errors, for 4 Edu games; `vno` build and lint clean for 2 books; the `publish` smoke check passes for all 6.
- **C14** Live site. Check: for each of the 6 works, the play page URL returns 200 and one music file's Content-Length equals the local `public/` file. Allow 30 min of CDN delay.
- **C15** $0. Check: the run log shows no Flow call and no paid model call. No new rows in `~/EduGames/logs/spend/2026-11.md` or the VN spend log, apart from $0 `client` rows.
- **C16** Hub docs. Check: grep shows `gm` and the "prefer ... over SNES for kids and learning" line in both skills, the README row, the `services.json` docs, ROADMAP row 27, and the midi-generator, edu-game-studio and VN ROADMAP rows.
- **C17** Done only when heard. Check: the user has listened to the final music of each of the 6 works on the live site (or locally) and said so. Record their words per work in the run log. Until then, each work is UNTESTED.

## User checkpoints

1. **Before T1:** a yes to download the SoundFont (Q1) and the npm package (Q2).
2. **After T2 (optional, 1 min):** listen to one gm demo track (`audition/_gm-demo.ogg`). If the SoundFont sounds wrong, switch before T3.
3. **T7 audition:** the user picks one style per work (Q3).
4. **Before T9 push:** a short yes to push the site, confirming the list of 6 works and the dist size.
5. **After T9:** the user listens to the 6 works (C17).

## Open questions for the user (recommended answer first)

1. **SoundFont and download.**
   - Recommended: **GeneralUser GS v2.0.x** by S. Christian Collins. File `GeneralUser-GS.sf2`, about 31 MB.
   - Licence: GeneralUser GS License v2.0. Free to use, modify and redistribute, also commercially, and music made with it is unrestricted.
   - Source: https://github.com/mrbumpy409/GeneralUser-GS (release asset; also https://schristiancollins.com/generaluser.php).
   - Saved to `~\ChiptuneStudio\soundfonts\`. Yes to download?
   - Alternatives: MuseScore_General.sf3 (MIT, about 38 MB, compressed SF3, needs the Vorbis path in spessasynth) and FluidR3_GM.sf2 (MIT, about 141 MB, older sound).
2. **The npm package `spessasynth_core`** (Apache-2.0, about 1 MB, pure JS, no native binary). Yes to add it to midi-generator? The alternative is a FluidSynth CLI binary download: offline render only, no in-app playback. Not recommended.
3. **ACE-Step or gm per work.** Recommended: the A column of the T7 table.
   - suncev-sustav: ACE-Step plus gm for castle, rpg and boss.
   - deutsch-a1-pilot: gm folk-pop.
   - roleplay-a1: ACE-Step bossa cafe.
   - roleplay-b2: ACE-Step lo-fi.
   - Bell: gm storybook.
   - Snail: gm playful.
   - B and C are auditioned next to A, and the user picks.
4. **Keep the old SNES v1 tracks** as unselected versions in the tools (recommended: yes; nothing is deleted).
5. **Music bitrate on the site.** Recommended: Vorbis q5 / mp3 160k for music only, about +25-30 MB, dist about 470 MB of 600. Speech stays as it is.
6. **SNES clean (MDI-16).** Recommended: build it, small and opt-in, used as candidate C for the Bell. Answer no to cut it.

## Risks

- **spessasynth_core does not fit.** Its API or worklet use may not fit the per-tick voice contract, or it may be slow: a 90 s offline render should take 15 s or less. Mitigation: a time-boxed spike first in T2 (render one MIDI file headless; measure time and determinism). Fallback 1: render gm songs through `export_midi` plus spessasynth's own sequencer in `render_audio` only, with no tracker preview. Fallback 2: the FluidSynth CLI (needs another download yes).
- **Per-channel stems.** They may be unavailable from the bus. Accept one mix stem for gm and say so in the guide.
- **Determinism and golden drift.** Any shared-code change in the mixer or sampler could move old renders. C2 and C5 guard this; keep gm code in new files.
- **ACE-Step quality and loops.** v1 output varies with the seed and is not loopable. Render 2 seeds per candidate in T7. The seamless crossfade (C10) is new code; listen at the seam.
- **ACE-Step model location.** `ace_step_v1_3.5b.safetensors` was not under `models/checkpoints` in a quick look, though ACE-Step ran on 2026-11-08 (`runs/pip-bruno-3d-pilot.md`), so it lives in an extra model path. If `generate_music` fails, check comfy-mcp `checkCheckpoints` before anything else. Do not download without a yes.
- **Loudness mismatch between ACE-Step and gm** within a work. C12 checks it; adjust the cue volume in the pack.
- **Edu course text keys.** New versions keep their asset ids, so the `asset.<id>.alt` keys stay. If an alt says "chiptune" (HUB-28 wrote such alts), update it with `edu_text_set` in en, hr and de, or `edu_build` fails on wording checks. This happened in HUB-28.
- **Site budget.** The dry-run in T6 catches it; fall back to q4 / 128k.
- **GitHub Pages and CDN delay.** Allow 30 min, push once, never force-push.
- **Starting services.** Chiptune Studio may be started for this work only. ComfyUI must not start while Strata answers (VN autostart rule). Scriptorium is never started.
- **A headless Chiptune on 7458 holding the old build.** Stop it and restart after `hub.ps1 build chiptune-studio`. `hub.ps1 status` can flicker; confirm with an HTTP probe.
