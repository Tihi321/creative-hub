# HUB-28 research: Edu Studio games on phones, music options like the VNs, rebuild and republish

## Question
How is the Edu player laid out (and what breaks at ~375 px), what "music options" do the VN Studio player and studio have versus Edu Studio today, how are edu games published to creative-hub-web, how are they rebuilt, and how are they tested?

## Answer
1. **The Edu player is not desktop-only already.** It has the viewport meta (viewport-fit=cover), media queries in every shell CSS, 44 px tap targets, a coarse-pointer rule and a no-sideways-scroll rule. What is missing is evidence at phone width for the five non-quiz shells (only the quiz arena is checked at 390x844, RPG once at 360x740). Nothing was rendered in this research, so "what breaks at 375" is **inferred from CSS only**; a screenshot pass at 375 px per shell is the first plan step.
2. **Music "same as VNs": the gap is on the player side.** Edu's generation side already mirrors VN (provider comfy/chiptune/flow, chip, engine, tracks, per-area plan, MCP tools). The Edu player has only two title-screen toggles (Sounds, Reduce audio); the VN player has music/sound/voice volume sliders in a Preferences panel, a voice mute button in the HUD, a pause menu, ducking under voice, and persistence. "Both" is plausible but the code makes the player-side reading the obvious one; a user question remains (below).
3. **Publishing: 3 edu games are already live** in creative-hub-web (suncev-sustav, deutsch-roleplay-a1, deutsch-roleplay-b2), `type: "edu-game"`, `player: "edu"`. The 4 other EduGames courses (deutsch-a1-pilot, a2/b1/b2-smoke) are not in the catalog. REQ-0020 rebuilt only the VNs. Edu games are rebuilt with `edu_build` over MCP (engine on 7463, **not running now**) or **without the engine** by the CLI `node out/engine/index.js build <slug>` (`src/engine/educli.ts:32`, needs `yarn build:engine` first).
4. **Tests**: vitest fast suite (`yarn test`), Chromium suite (`yarn test:e2e`), autoplay bot `yarn play` / `node scripts/play.mjs <build-dir> --mode ... --viewport 375x667`.

## Path through the code

### 1. Edu player layout (all confirmed by reading)
- Host page: `renderIndexHtml` in `C:/projects/Personal/edu-game-studio/src/shared/game-data.ts:58` has `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`, one `#edu-root`, `player.css`, `game-data.js`, `player.js`. `base.css` uses `min-height: 100vh` then `100dvh` (`src/player/style/base.css:13-20`).
- Bundle: one IIFE `out/player/player.js` + `player.css` (`docs/player.md` "The browser player"); built by `yarn build:player` (`vite.player.config.ts`). A built game folder contains its own copy of player.js/css (EduGames build dirs dated 2026-11-01/02; engine `out/player` is dated 2026-11-04), so **every game must be rebuilt to get a CSS change**.
- Shells (shell picker on the title screen; `GameData.shell` picks the default; the user's screenshot is the encyclopedia shell). All are DOM + CSS except where noted:

| Shell | Code | CSS | DOM/Canvas | Media queries |
|---|---|---|---|---|
| Quiz arena (chalkboard) | `src/player/shells/quiz-arena.ts` | `src/player/style/arena.css`, `style/items.css`, `style/base.css` | DOM | arena 560 px; items 700/560/480 px, `(pointer: coarse)`, `(hover: none)` (`items.css:1268-1302`) |
| Shared start screen, mode picker | `src/player/kit/start.ts` (+ `kit/screens.ts`, `kit/session.ts`) | `src/player/kit/kit.css` (151 lines) | DOM | **none** in kit.css (grid with `max-width` / `auto 1fr` rows; `kit.css:56-110`) |
| Encyclopedia explorer | `shells/encyclopedia/{app,view-*}.ts` | `encyclopedia.css` (1672 lines) | DOM (SVG for places/timeline) | mobile-first: 1 column by default (`:245`), 2 columns from 840 px (`:250-252`, search+illustration vs lists), index uses CSS `columns: 250px 2` (`:430`), `max-width: 640px` (`:1437`) and `760px` (`:1623`) blocks |
| MindMaze castle | `shells/mindmaze/{index,layout,walk,art}.ts` | `mindmaze.css` (1250) | DOM + inline SVG art (inferred from `art.ts`; not opened) | 900 px and 560 px blocks (`:1201`, `:1211`); `minmax(250px,340px)` side column at `:563` |
| RPG quest | `shells/rpg/{index,draw,ui}.ts` | `rpg.css` (715) | **Canvas 2D** (`draw.ts:10, 345-361`: buffer is a whole multiple of the logical size, shown at container width via a resize watcher), battle canvas in `ui.ts:60`, minimap canvas 192 px (`index.ts:393`) | 860 px (`:624`), 560 px (`:630`); 3x`--edu-tap` d-pad grid (`:288`) |
| Language role-play | `shells/roleplay/{board,dialogue,garden}.ts` | `roleplay.css` (692) | DOM | only 480 px (`:669`); fixed 44/76/96 px avatar columns (`:189, 386, 504`) |
| Detective / escape room | `shells/detective/{board,grid,map}.ts` | `detective.css` (945) | DOM + SVG | 560 px twice (`:863, :932`), 900/1000 px upwards |

- Touch handling: `touch-action: manipulation` and 44 px targets at `(max-width:560px),(pointer:coarse)` (`items.css:1268-1300`), `hover: none` disables lift effects (`:1302`), RPG buttons `touch-action` (`rpg.css:309`), Android back button hook `src/player/android-back.ts`, `safe-area` CSS (tested by `tests/android-mobile.e2e.test.ts:45`). No swipe gestures, no pinch rules, no orientation handling found (grep).
- Documented promise: tap targets >= 44 px except grids, "No page scrolls sideways from 360 px up" (`docs/player.md`, "Keyboard and accessibility"). The bot checks `scrollWidth <= innerWidth` (`scripts/play.mjs:323`).

**Likely trouble at 375 px (inferred, not rendered):**
- Encyclopedia: stat pills row (`.enc-stats`, `encyclopedia.css:215`) and the top tabs (`.enc-tabs`, `:68`) are the screenshot's wide items; below 640 px tabs only shrink padding (`:1437-1441`); whether they wrap or scroll is unverified. Page frame (parchment) padding eats width.
- Role-play: only one breakpoint (480 px) and fixed side columns.
- Start screen `kit.css` has no breakpoint at all; the mode grid and settings must be checked.
- Detective and MindMaze have side columns with `minmax(250px, ...)` that collapse only at 560/900 px; at 375 px the main column is 1fr, probably fine, but board/grid sizes are unverified.
- Hover-only controls: only lift effects are hover-based and are already disabled on `hover: none`; no hover-only functionality found (inferred from grep of `:hover` was not done exhaustively).

### 2. Music options

**VN player side** (`C:/projects/Personal/visual-novels-orchestrator/src/engine/game/player-runtime.ts`, one 4404-line generated file; confirmed):
- Preferences panel "Audio" section: sliders Music Volume (default 48), Sound Effects Volume (80), Voice Volume (90), each with an `<output>` value (`:236-258`).
- Settings object `{textSpeed, autoDelay, volMusic, volSfx, volVoice, storyTextSize, uiLang, voiceMuted, schema:2}` (`:1752-1761`), persisted in `localStorage['vno_settings']` (`:4248`, `:4275`), clamped on load, migration for old music default 80 (`:4266-4272`).
- Perceptual gain curve `(v/100)^1.6` (`:2400-2405`), 180 ms volume ramp (`:2408-2426`), `applyAudioVolumes` ducks music to 0.35 and ambience to 0.7 while a voice clip plays (`:2439-2444`).
- HUD: voice stop and mute buttons (only when the game has voice) and a Preferences "Voices On/Off" row (`:296-300`, `:2196-2236`); pause menu (Resume/Save/Load/History/Preferences/Main Menu, `:285-292`).
- Tracks: per-scene `scene.music` (track id, null = silence) with chapter fallback, `playMusic(trackId, loopStart)` with loop-start points, `stopMusic` (`:3213-3217`, `:3662-3699`); menu music `music_01` (`:2021`). No crossfade (hard switch; grep found none).
- Autoplay gesture handling for music (`:1923-1926`).
- There is **no on/off music toggle** apart from setting the slider to 0 (inferred: no `musicMuted` setting).

**VN studio side** (confirmed):
- Project settings `music: {provider: comfy|chiptune|flow, chip, engine, tracks}` (`src/shared/vn.ts:240, 352-357`), provider default chiptune for pixel books else comfy (`:416`). UI card "Music" in `src/renderer/ui/book/LookTab.tsx:207-256` (test ids `music-provider`, `music-chip`, `music-engine`, `music-tracks`, Flow credits note).
- Scene/chapter assignment UI in `ScenesTab.tsx` (music select, preview of resolved scene audio, `:141-197, :553`).
- MCP: `vno_update_settings {music:{provider,chip,tracks,...}}` (`src/engine/mcp/tools.ts:184-195`), `vno_set_music` (menu, chapters, scenes -> track ids, `tools-plan.ts:58-73`), `vno_set_cues` (menuMusic, chapters, per-scene music/ambience, `tools-plan.ts:79-108`), `vno_plan_art_music`, `vno_asset_generate`, `vno_asset_replace` (import own file as `music_01`), `vno_studios_status`.
- Agent: composer `plan_music` plans track prompts and chapter assignments (`src/engine/vn/agents/composer.ts`); Chiptune Studio client (`src/engine/studios/music.ts`) gives loop points; Flow Music is credit-gated.

**Edu player side** (confirmed):
- `src/player/audio.ts` (`GameAudio`, 272 lines): area-based music `music:<area>` cues (menu, `unit-<id>`, boss, end, castle, rpg-overworld, rpg-battle), one track at a time with 400 ms fade between areas, menu fallback, loop points from `pack.extensions.audio.loops`, duck to 0.3 under narration/listening, SFX events (correct, wrong, combo, level-up, boss), gesture-resume, error reporting.
- Settings: only two booleans in progress, `sound` and `reduceAudio` (+ `speak`) (`progress.ts:58, 81, 211-212`), shown **only on the title screen** (`kit/start.ts:152-165, :225`; test ids `setting-sound`, `setting-reduce-audio`). No in-game control, no volume sliders, no separate music/sfx/voice level, no music-only toggle (reduceAudio kills music and quietens SFX to 0.4, `audio.ts:67` / `:133`). Strings in `i18n.ts:15-17, 232-234, 447-449`.
- Volumes come only from cue `volume` in the pack (`DEFAULT_MUSIC_VOLUME`, `src/shared/music.ts`).

**Edu generation side** (confirmed): `media.music {enabled, engine, tracks, provider comfy|chiptune|flow, flowCredits, chip}` (`src/shared/media.ts:128-143`), MCP `edu_media_settings {slug,set}`, `edu_music_plan {slug,fallback}`, `edu_asset_generate {kind:"music"|"sfx"}`, `edu_asset_list/select/replace/lock` (`src/engine/mcp/tools-media.ts:27-184`), composer role, `src/engine/edu/music.ts`/`music-service.ts`, Chiptune/ComfyUI/Flow providers, placeholder silence when a provider is down. Studio UI: `ui/course/AssetsTab.tsx` lists music assets (no dedicated music settings card found in `src/renderer`; `GeneratorsPage.tsx` mentions music) - **inferred** that Edu has no equivalent of the VN `LookTab` Music card.

**Gap table**

| Capability | VN Studio | Edu Studio today |
|---|---|---|
| Music volume slider | yes (0-100, default 48, gain curve ^1.6) | no (cue volume fixed in the pack) |
| SFX volume slider | yes (80) | no |
| Voice volume slider | yes (90) | no |
| Mute/toggle | voice mute in HUD + prefs; no music toggle | `Sounds` on/off and `Reduce audio` on the title screen only |
| In-game access | Preferences from pause menu, HUD buttons | none; title screen only |
| Persistence | `localStorage vno_settings` with schema/migration | `localStorage edu-studio:progress:<id>` `settings.sound/reduceAudio` |
| Ducking under voice | music 0.35, ambience 0.7 | music 0.3 under narration/listening |
| Per-scene/area tracks | per scene + chapter + menu | per area: menu, unit, boss, end, castle, rpg areas (more granular by shell) |
| Crossfade | none (hard switch) | 400 ms fade out/in |
| Loop points | yes (Chiptune) | yes |
| Provider choice | comfy / chiptune / flow, chip, engine, tracks | same fields, same MCP style (`edu_media_settings`) |
| Studio UI music card | yes (`LookTab` MusicCard) | not found (assets list only) |
| MCP to assign tracks | `vno_set_music`, `vno_set_cues` | none to reassign a track to an area; `edu_music_plan` then `edu_asset_select/replace` (inferred from the tool list) |
| Music preview in studio | scene preview audio | not found |

### 3. Publishing and rebuilding
- `creative-hub-web/content/catalog.json` has 3 edu works: `suncev-sustav` (line ~651), `deutsch-roleplay-a1`, `deutsch-roleplay-b2`; each play is `{type: "edu-game", player: "edu", source: "edu:<slug>/build"}`. Valid types/players: `scripts/lib/catalog.mjs:25-26`. Sources resolved from `content/sources.local.json` (`edu` -> `C:/Users/Infplane/EduGames/courses`). The publish manifest records an `inject-bridge@1:edu:<id>` recipe for index.html (TV bridge) (`scripts/lib/encode.mjs:101`, `content/publish-manifest.json:2474`). Published copies exist under `public/play/{suncev-sustav-game,deutsch-roleplay-a1-game,deutsch-roleplay-b2-game}`.
- The brief's claim "REQ-0020 says the 3 edu games were skipped": REQ-0020 only says it rebuilt the 13 VN plays (lines 25, 32); the text "different player" was not found. Edu plays were left on the old player (not rebuilt).
- EduGames courses (`C:/Users/Infplane/EduGames/courses`): suncev-sustav, deutsch-roleplay-a1, deutsch-roleplay-b2 (published); deutsch-a1-pilot, deutsch-a2-smoke, deutsch-b1-smoke, deutsch-b2-smoke (not in catalog; the smoke ones are test builds; b1/b2-smoke have no `build/assets`). All have `build/` with player.js dated 2026-11-01/02, older than the engine's current player (2026-11-04).
- suncev-sustav's built game-data already has 9 music cues (menu, unit-u1..u3, boss, end, castle, rpg-overworld, rpg-battle) and 3-4 shells; default shell quiz-arena (`game-data.json`). So the music already exists to play; only controls are missing. The other courses were not checked for cues (`grep` found `musicCues=0` for the German ones with a simple pattern; unreliable, not confirmed).
- Rebuild routes: (a) MCP `edu_build {slug}` needs the engine (`engine.lock` at `~/EduGames/engine.lock` shows pid 31968, started 2026-11-04; port 7463 did not answer `curl` on 2026-11-07, so **the engine is down, lock stale**); (b) **no engine needed**: `yarn build:engine` (bundles the player into `out/player`) then `node out/engine/index.js build <slug> [--data <dir>]` (`src/engine/educli.ts:32`, commands courses/validate/build/lint/import-course). Exact flags were not read; the plan should read `educli.ts` and `tests/edu-cli.test.ts`. Agents must not point scratch runs at `~/EduGames` (`AGENTS.md`), but a rebuild of the real data is the user's request.
- Publish: `cd creative-hub-web && npm run publish -- --only <workId>` (smoke check in headless Chromium, size budget 600 MB; currently 418.8 MB per REQ-0020), then `npm run build`, `npm run check`, `git add public content && git commit`, `git push origin master` (README.md "Publish, build, check, push"). Pages deploy is by GitHub Actions on push (per REQ-0020 text).
- The previous republish pattern: WEB-02/WEB-03 branches ("republish the 13 VN plays"); latest web master `47aa1a8`.

### 4. Tests
- Fast: `yarn test` (vitest; `tests/player-audio.test.ts` for `GameAudio` with a fake Audio; `player-progress.test.ts`, `player-shell-kit.test.ts`, `player-i18n.test.ts`, per-shell logic tests, `edu-build.test.ts`, `edu-cli.test.ts`). `yarn typecheck`, `yarn lint`.
- Browser: `yarn test:e2e` (`vitest.e2e.config.ts`, `*.e2e.test.ts`, fails without Chromium): `android-mobile.e2e.test.ts` (390x844, touch, 44 px targets, no sideways scroll, safe-area, quiz arena), `audio-shells.e2e.test.ts` (music in every shell with a recording Audio, reduce-audio, sound off), `bot*.e2e.test.ts` per shell (rpg at 360x740), `player-shell-picker.e2e.test.ts`, `classroom`, `speaking`, `live-quiz`.
- Autoplay bot: `node scripts/play.mjs <build-dir> --mode perfect|wrong|random [--shell <id>] [--viewport 375x667] [--keyboard] [--axe]` (drivers in `scripts/bot/*.mjs`). AGENTS.md: anyone changing a shell, the player or the bot also runs `yarn test:e2e`. Node via `fnm exec --using=24 yarn <script>` (Yarn under fnm quirk in memory: put the fnm default dir on PATH).
- creative-hub-web: `npm run test:unit`, `npm run test:e2e` (Playwright over `dist/`: `tests/e2e/players.spec.mjs`, `touch.spec.mjs`, `tv-nav.spec.mjs`, `desktop.spec.mjs`, `screens.spec.mjs`), `npm run check`.
- Not run in this research (read-only brief, no build).

## Reproduction
Not reproduced: no browser render was made. Cheapest repro for the plan: build one course (`suncev-sustav`) and run `node scripts/play.mjs <build> --mode perfect --shell <id> --viewport 375x667 --shots <dir>` for each of the six shells, then read the screenshots.

## What the plan needs
- Edu repo ticket (EGS-NN, branch `EGS-NN_<what>` cut from master; one commit; do not commit unless asked) for: (a) phone-width fixes per shell CSS (files in table above); `kit.css` and roleplay first; (b) audio preferences (below); (c) docs (`docs/player.md`, test ids list), i18n strings in en/hr/de (`i18n.ts`), progress schema (`progress.ts:58-81, 211`; old saves must stay valid: missing -> defaults).
- Audio options design (options, not decided): (1) minimal: add in-game settings panel/button (a gear in the shell HUD or the kit) with Music volume, Sound effects volume sliders and a music on/off, persisted in `settings`, applied through `GameAudio` (add a `musicVolume` and `sfxVolume` multiplier to `AudioSettings`, `audio.ts:44-47`; keep `sound` and `reduceAudio` semantics); (2) VN-parity: add Voice volume (narration/listening clips in `items/listening.ts`, encyclopedia narration) with the same curve (^1.6) and defaults (48/80/90), a mute button in the HUD; (3) option on the studio side: a Music card in the Edu course UI and an MCP tool to assign a track to an area (like `vno_set_music`). Choose with the user.
- Shared test ids needed: `setting-music-volume`, `setting-sfx-volume`, etc. (rule: every interactive element has `data-testid`, `AGENTS.md`).
- Tests: extend `tests/player-audio.test.ts` (volume multipliers), `tests/player-progress.test.ts` (migration), `tests/audio-shells.e2e.test.ts` (slider changes `audio.volume` in each shell), phone-width e2e (extend `android-mobile.e2e.test.ts` to all shells, 375 px).
- Rebuild: `yarn build:engine`, then CLI build of the 3 published courses (and maybe the 4 other ones if they should be published), bot run per course, then web: `npm run publish -- --only <id>` x3, build, check, e2e, commit/push in creative-hub-web on a `WEB-NN_...` branch (pattern WEB-02/03). Hub ticket HUB-28 for the log; `runs/` or ticket changelog with ids.
- Check first whether the TV bridge (`inject-bridge` for edu) still works with a new player (REQ-0014 follow-ups for Edu D-pad/Back keys were "tool roadmap, not built").
- The user plays it: "done only when the user has played it" (hub CLAUDE.md); untestable here: real phones.

## Risks
- Shared CSS (`items.css`, `base.css`) is used by all shells and the studio live preview (`embed.css`): a global change affects them; a test checks every selector starts with `.edu-stage`.
- Progress save format (`ProgressStore`, `localStorage`): changes must be backward compatible; export/import validation in `progress.ts:211`.
- Size budget 600 MB on the site (418.8 MB used): rebuilt Edu games change only player files, so small.
- Edu games on the site go through `inject-bridge` (TV bridge), which may touch the DOM; a player change can break the bridge (the web e2e `tv-nav.spec.mjs` checks).
- Music exists only in games whose pipeline made it (suncev-sustav yes; German ones unverified). Settings for a game with no `cues` are hidden by design (`start.ts:152`: only when `pack.cues.length`), so a game without music would show no controls; decide whether to keep that.
- Chiptune/ComfyUI/Flow cost: regenerating music would spend credits (Flow) or GPU; this ticket should not regenerate.
- Engine is down; MCP build requires it. CLI build avoids this but must be confirmed to rewrite the player into `build/` (CLI uses `PLAYER_OUT`, inferred from the tests).
- Large CSS files (encyclopedia 1672 lines): regressions at desktop; screenshot compare needed.

## Open questions
1. (User) "Music options like the VNs": player settings (volume sliders, in-game settings, voice mute), generation options in the studio (music card, track assignment), or both? Code makes the player side the clear gap; the studio side is mostly present via MCP.
2. (User) Which edu games to rebuild and publish: the 3 live ones only, or also deutsch-a1-pilot (and the smoke builds, which look like test builds)?
3. (User) Do the games need music generated where missing (German courses), or only controls?
4. (Inferred, unanswered) Exact CLI flags of `node out/engine/index.js build` and whether it uses the current `out/player`; read `educli.ts` before planning.
5. (Unanswered) Real phone layout of each shell: needs the 375 px screenshot pass.
6. (Unanswered) Does "mobile friendly" include the Edu studio app or only the player? Assumed player only.
