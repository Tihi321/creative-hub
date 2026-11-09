---
status: done
request: REQ-0021
repos: [creative-hub, edu-game-studio, creative-hub-web]
branch: EGS-62_mobile-music
updated: 2026-11-07
---

# HUB-28: Edu games on phones, in-game audio settings like the VN player, music for the German games, rebuild and republish

Research: `research.md` in this folder (file:line refs). User decisions of 2026-11-07 are binding (summarised under Scope). Reading of the request: the **full** one. All six shells and the shared start screen are fixed for phones, the player gets an in-game audio panel, the three German games get Chiptune music, and four games are rebuilt and published.

Branches (named here so the user approves them with the plan; per the global rule nobody creates one silently):
- `edu-game-studio`: `EGS-62_mobile-music` from `master` `46b6ec1` (EGS-61 is the last used number; EGS-62 is free, no branch of that name exists).
- `creative-hub-web`: `WEB-04_edu-mobile-music` from `master` `47aa1a8` (WEB-01..03 used; the repo has no `ROADMAP.md`, tickets live in `.claude/tickets/WEB-NN-*`).
- `creative-hub`: records only, on `master` after asking the user (as for HUB-27).

Checked in code for this plan (beyond research.md):
- `GameAudio` (`src/player/audio.ts`) reads only `{sound, reduceAudio}`; music level is `cue.volume * duck` (`:138-140`), SFX `cue.volume * 0.4 if reduced` (`:255`). Cue defaults are already `DEFAULT_MUSIC_VOLUME = 0.45`, `DEFAULT_SFX_VOLUME = 0.8` (`src/shared/music.ts:35-36`).
- Voice clips are played outside `GameAudio`, each by a tap: listening item `<audio>` (`items/listening.ts:18-27`), encyclopedia article narration `new Audio` (`encyclopedia/view-article.ts:60`), encyclopedia reader (`view-reader.ts:167`), role-play line clips (`roleplay/index.ts:155-164`, which does **not** duck the music today).
- Two render paths draw every screen: `ShellSession.render` (`kit/session.ts:498-517`, used by encyclopedia, mindmaze, rpg, roleplay, detective) and `QuizArena.render` (`shells/quiz-arena.ts:205-224`). Both clear `#edu-root` and build `.edu-app > .frame > main#edu-main`.
- Settings are `progress.settings` (`progress.ts:58`, parse at `:209-218`), saved per game in `localStorage`.
- The 4 builds: `suncev-sustav` has 9 music cues + 5 SFX (shells quiz-arena, encyclopedia, mindmaze, rpg). `deutsch-roleplay-a1` and `-b2` (quiz-arena, encyclopedia, roleplay) and `deutsch-a1-pilot` (quiz-arena, encyclopedia, mindmaze, rpg) have **0 cues**; their `course.md` media has `music: {enabled: false}` and `pipeline/steps.json` marks `music_plan:all` / `music_generate:all` as `skipped`. All three have voice clips (8, 6, 8 audio assets).
- The site bridge pill is fixed **top-left** (`hub-bridge.js:87`); `check-site.mjs` parses every `.js` at ES2018 (publish lowers JS with esbuild, `encode.mjs:208`) and does **not** lint the Edu `player.css` (`check-site.mjs:262`).
- `edu-studio` is started by `hub.ps1` as `node out/engine/index.js --mcp-only` from the repo (`services.json:46-56`), so `edu_build` copies whatever `out/player` the repo has at that moment. `yarn build:engine` includes `build:player` (`package.json:16`).

## Scope

1. **Phones (Edu player, all shells).** Quiz arena, encyclopedia, MindMaze castle, RPG, role-play, detective and the shared start screen (`kit/start.ts` + `kit/kit.css`) work at 360-390 px portrait with touch: no page scrolls sideways, columns stack, tab and pill rows wrap or scroll inside themselves, tap targets are at least 44x44 CSS px (existing grid exemptions stay), body text at least `--edu-text-s` and not below 14 px, canvases (RPG map, battle, minimap) fit the width. Desktop at 1280 px looks as before.
2. **In-game audio panel (Edu player).** A speaker button `audio-settings`, fixed top-right on every screen of every shell (title, maps, rounds, articles, castle, RPG, scenes, cases, end), opens a modal panel `audio-panel` with:
   - Music, Sound effects and Voices sliders, 0-100, step 5, each with a visible value (`<output>`), shown only when the game has that channel;
   - a "Sound" on/off toggle (the existing `settings.sound`: off silences music and SFX) and the existing "Reduce audio" toggle;
   - a Close button; Escape, a tap on the backdrop and the Android back button close it; focus returns to the speaker button.
   Values persist in the game's progress (`localStorage edu-studio:progress:<id>`, export/import included). Ducking under voice stays (`DUCK_FACTOR` 0.3) and is added to role-play line clips.
3. **Music for the German games.** `deutsch-roleplay-a1`, `deutsch-roleplay-b2`, `deutsch-a1-pilot` get music tracks and sound effects from **local Chiptune Studio** through Edu Studio's existing pipeline (`edu_media_settings`, `edu_music_plan {fallback: true}`, `edu_asset_generate`). `suncev-sustav` keeps its music.
4. **Rebuild** the 4 games with the new player (EGS-62 merged).
5. **Publish** the 4 games to `creative-hub-web` (3 republished, `deutsch-a1-pilot` new in `content/catalog.json`), check, commit, merge, push `master` (push requested by the user).
6. **Hub records**: `ROADMAP.md` HUB-28 row, run log `runs/hub-28-edu-mobile-music.md`, EGS-62 row in Edu Studio's `ROADMAP.md`, pointer plan in `creative-hub-web/.claude/tickets/WEB-04-edu-mobile-music/plan.md`.

## Out of scope (explicit)

- A Music card in the Edu Studio app UI, a track-assignment UI, new MCP tools (e.g. an Edu `set_music`), music preview in the studio (user decision 2).
- The Edu Studio desktop app on phones (player only).
- Regenerating `suncev-sustav` music, any image, voice or text; re-running the content pipeline.
- Any paid or credit service: Flow Music, Google Flow, paid models, the composer **model** job (we use `edu_music_plan {fallback: true}`, no model). ComfyUI is not used (provider forced to `chiptune`). Scriptorium is not started.
- `deutsch-a2-smoke`, `deutsch-b1-smoke`, `deutsch-b2-smoke` (test builds; not published, not rebuilt).
- Edu D-pad / TV remote work (the bridge handles Edu as today), a rotate hint or a landscape-only layout, swipe gestures, pinch zoom.
- Per-channel mute buttons and a voice mute: every Edu voice clip is played by an explicit tap (a listening exercise needs it), so "mute" is the master Sound toggle plus each slider at 0. (Deviation from the VN `voiceMuted`; see Decisions.)
- VN Studio and the VN plays.

## Files and modules to touch

| Repo | File | Change | Task |
|---|---|---|---|
| edu-game-studio | `src/player/kit/kit.css` | Phone rules for `.start-screen`, `.mode-grid`, `.mode-card`, `.settings`, `.lang-picker`, `.start-head` | A1 |
| edu-game-studio | `src/player/style/base.css`, `style/arena.css`, `style/items.css` | `.frame` / `.board` padding at <=480 px, quiz arena HUD row wrap, item grids | A1 |
| edu-game-studio | `src/player/shells/encyclopedia/encyclopedia.css` | `.enc-tabs` scroll strip, `.enc-stats`, `.enc-index` columns, page padding, SVG fit | A2 |
| edu-game-studio | `src/player/shells/mindmaze/mindmaze.css`, `shells/detective/detective.css` | Side columns (`minmax(250px,340px)` at `mindmaze.css:563`), boards, grids, maps | A3 |
| edu-game-studio | `src/player/shells/rpg/rpg.css`, `shells/rpg/index.ts` (minimap size only if CSS cannot), `shells/roleplay/roleplay.css` | Canvas fit, minimap, d-pad; role-play fixed avatar columns (`:189, :386, :504`), <=400 px block | A4 |
| edu-game-studio | `src/player/audio.ts` | Volume channels, gain curve, `voice()` | B |
| edu-game-studio | `src/player/progress.ts` | `musicVolume`, `sfxVolume`, `voiceVolume` in `settings`, defaults and clamped parse | B |
| edu-game-studio | `src/player/types.ts` | `ItemContext.voice?(el)` | B |
| edu-game-studio | `src/player/kit/audio-menu.ts` (new), `src/player/kit/audio-menu.css` (new, imported in `main.ts`) | Button + panel | B |
| edu-game-studio | `src/player/kit/session.ts`, `src/player/shells/quiz-arena.ts` | Mount the menu in both `render`s; pass `voice` in the item context (`session.ts:399`, `quiz-arena.ts:514`) | B |
| edu-game-studio | `src/player/items/listening.ts`, `shells/encyclopedia/view-article.ts`, `view-reader.ts`, `shells/roleplay/index.ts` | Route clips through `audio.voice(el)`; role-play ducks | B |
| edu-game-studio | `src/player/i18n.ts` | New keys in en, hr, de | B |
| edu-game-studio | `src/player/android-back.ts` | `audio-close` first in `BACK_TESTIDS` | B |
| edu-game-studio | `tests/player-audio.test.ts`, `tests/player-progress.test.ts`, `tests/audio-shells.e2e.test.ts`, `tests/android-mobile.e2e.test.ts`, `tests/bot*.e2e.test.ts` | See Acceptance | A, B |
| edu-game-studio | `docs/player.md` | Settings, test ids, phone rules | B (A adds one line each) |
| edu-game-studio | `ROADMAP.md`, `.claude/tickets/EGS-62-mobile-music/plan.md` (pointer to this plan) | Row, changelog | B (owner of the merge) |
| (data) | `~/EduGames/courses/{deutsch-roleplay-a1,deutsch-roleplay-b2,deutsch-a1-pilot}/course.md` media, `course/assets*`, `pipeline/music.json`, `build/` | Through MCP only | C, D |
| creative-hub-web | `content/catalog.json` | New work `deutsch-a1-pilot` | E |
| creative-hub-web | `public/play/{suncev-sustav-game,deutsch-roleplay-a1-game,deutsch-roleplay-b2-game,deutsch-a1-pilot-game}/`, `content/publish-manifest.json` | Publish output | E |
| creative-hub-web | `.claude/tickets/WEB-04-edu-mobile-music/plan.md` | Pointer | E |
| creative-hub | `ROADMAP.md`, `runs/hub-28-edu-mobile-music.md` | Records | E |

## Audio settings contract (B implements; A, C, D and the tests rely on it)

- **Keys** in `Progress.settings` (all optional, integers 0-100): `musicVolume`, `sfxVolume`, `voiceVolume`. Missing or invalid in a save: **100**. `parseProgress` rounds and clamps to 0..100; `newProgress` writes 100/100/100. `PROGRESS_VERSION` is not bumped (old saves stay valid). Existing `sound`, `reduceAudio`, `speak` unchanged.
- **Defaults 100** keep today's loudness: the VN mix (music 48, SFX 80, voice 90) is already baked into the cue volumes 0.45 / 0.8 that the pipeline writes; a VN-style default of 48 on top would make Edu music about 3x quieter than now.
- **Curve** as the VN player: `gain(v) = (v / 100) ** 1.6`, exported from `audio.ts` as `volumeGain`.
  - Music element volume = `cue.volume * gain(musicVolume) * (ducked ? DUCK_FACTOR : 1)`. `musicVolume === 0` behaves like sound off for music (track paused, restarts when raised).
  - SFX = `cue.volume * gain(sfxVolume) * (reduceAudio ? 0.4 : 1)`; nothing plays at 0.
  - Voice = `gain(voiceVolume)`. `GameAudio.voice(el: AudioLike): void` sets the volume and remembers `el` as the current clip, so a slider move changes a clip that is playing. `sound` off does **not** silence voice (listening items must work); voice at 0 does.
  - `refresh()` re-applies all three to what plays now (a short ramp via the existing `fadeTo`, 180 ms, like VN; no ramp in tests with fake timers).
- **DOM and test ids** (rule: every interactive element has a `data-testid`):
  - `button[data-testid="audio-settings"].edu-audio-btn` (aria-label `ui('audio.settings')`, `aria-haspopup="dialog"`, `aria-expanded`), appended as the last child of `.edu-app` by both render paths, `position: fixed; top: calc(env(safe-area-inset-top) + 8px); right: calc(env(safe-area-inset-right) + 8px)`, 44x44 min. Shown when the game has any cue or any audio asset (`/\.(mp3|ogg|wav|m4a|opus)$/` in `data.assets`); else absent.
  - `div[data-testid="audio-panel"][role="dialog"][aria-modal="true"].edu-audio-panel` with `h2` `ui('audio.title')`, `input[type=range][data-testid="setting-music-volume"|"setting-sfx-volume"|"setting-voice-volume"]` each with a `<label>` and `output[data-testid="<id>-value"]`, `button[data-testid="audio-mute"][aria-pressed]` (pressed = `sound` off), `input[data-testid="audio-reduce"]` (the reduce toggle), `button[data-testid="audio-close"]`.
  - The panel's open state lives in the menu object of the session (not in the DOM), so a shell re-render while it is open redraws it open with focus on the same control.
  - While open, one capture-phase `keydown` listener on `window` stops propagation of every key whose target is in the panel, so shell keys (RPG arrows, quiz shortcuts) do not act; Escape closes. Tab is trapped in the panel.
  - The title-screen toggles `setting-sound` and `setting-reduce-audio` stay (existing tests and habits); they and the panel write the same keys.
- **Corner space**: `.edu-stage .edu-app { --edu-corner: 56px }`. Any shell row that sits at the top of the page (quiz `.topbar`, `.enc-tabs`, mindmaze/detective/roleplay `.topbar`, RPG HUD) gets `padding-right: var(--edu-corner)` so the speaker button never covers a control. A owns those rules in the shell CSS; B owns `audio-menu.css`.
- **i18n keys** (en / hr / de): `audio.settings` "Sound settings" / "Postavke zvuka" / "Toneinstellungen"; `audio.title` same text; `audio.music` "Music" / "Glazba" / "Musik"; `audio.sfx` "Sound effects" / "Zvučni efekti" / "Soundeffekte"; `audio.voice` "Voices" / "Glasovi" / "Stimmen"; `audio.mute` "Sound off" / "Isključi zvuk" / "Ton aus"; `audio.close` "Close" / "Zatvori" / "Schließen".

## Tasks for workers

Order: A0, then A1-A4 and B in parallel (disjoint files) on `EGS-62_mobile-music`; C runs at any time (data only, needs services); D after A and B are merged; E after C and D.

**A0: Phone baseline** (one worker, read-only on code; ~15 min)
- *Inputs:* research section 1; fixtures `solar-system` (quiz-arena, encyclopedia, mindmaze, rpg), `de-roleplay-a1` (roleplay), `european-capitals` (detective, as in `tests/bot-detective.e2e.test.ts:28`).
- *Do:* `yarn build:player`, build the fixtures to `.claude/temp/hub-28/` (as the e2e helpers do, never into `~/EduGames`), then per shell `node scripts/play.mjs <build> --mode perfect --shell <id> --viewport 375x667 --shots .claude/temp/hub-28/shots-375/<id>` and the same at 360x740 and at the default 1280x800 (desktop baseline).
- *Outputs:* a table in the run log: shell, screen, what breaks (overflow px from the bot, small targets, cut text, overlapping), screenshot paths. This list is the work list of A1-A4; anything it does not show is not changed.

**A1: Start screen, shared CSS and quiz arena** (implementer)
- *Files:* `kit/kit.css`, `style/base.css`, `style/arena.css`, `style/items.css`.
- *Known candidates* (confirm with A0 first): `@media (max-width: 480px)`: `.mode-card { flex-basis: 100%; max-width: none }`, `.mode-grid` gap `--edu-space-2`; `.settings` rows wrap; `.lang-picker { flex-wrap: wrap }`; `:where(.edu-stage) .frame` (`arena.css:19`) padding down to `--edu-space-2`; quiz `.topbar` wraps and gets `padding-right: var(--edu-corner)`.
- *Contract:* every selector starts with `.edu-stage` (existing test); `items.css` and `base.css` are shared with the studio preview (`embed.css`), so changes stay inside `@media (max-width: ...)` or `(pointer: coarse)` blocks.

**A2: Encyclopedia** (implementer)
- *File:* `shells/encyclopedia/encyclopedia.css` only.
- *Known candidates:* in the `@media (max-width: 640px)` block (`:1437`): `.enc-tabs { flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: thin; padding-right: var(--edu-corner) }` with `.enc-tab { flex: 0 0 auto }` (the strip scrolls, the page does not); `.enc-stats` gap `--edu-space-1`, `.enc-stat` font `--edu-text-s`; `.enc-index` (`:430`) `columns: 1`; the parchment page padding reduced; place/timeline SVG `max-width: 100%; height: auto`. The 1-column default of `.enc-columns` (`:245`) stays.
- *Contract:* the tab strip keeps its keyboard order; desktop (>= 840 px) rules untouched.

**A3: MindMaze and detective** (implementer)
- *Files:* `shells/mindmaze/mindmaze.css`, `shells/detective/detective.css`.
- *Known candidates:* at <= 560 px the castle side column (`mindmaze.css:563`) stacks under the room; room art and the detective map/board SVGs fit 100% width; grid cells stay >= 44 px or the grid scrolls inside its own box; `.topbar` gets `padding-right: var(--edu-corner)`.

**A4: RPG and role-play** (implementer)
- *Files:* `shells/rpg/rpg.css` (+ `rpg/index.ts:393` only if the 192 px minimap canvas cannot be scaled by CSS), `shells/roleplay/roleplay.css`.
- *Known candidates:* RPG canvases `max-width: 100%; height: auto` (the resize watcher in `draw.ts:345-361` keeps the buffer crisp); minimap 120 px wide at <= 480 px or hidden behind its existing toggle; d-pad stays `3 x var(--edu-tap)`; HUD row gets `padding-right: var(--edu-corner)`. Role-play: a `@media (max-width: 400px)` block: `.pc-hud-plant { grid-template-columns: 56px minmax(0, 1fr) }`, `.pc-plant-card` 56 px, reply buttons full width, bubbles `overflow-wrap: anywhere`.

**A (all):** each A worker changes **one existing run** in its shell's bot e2e test to add `--viewport 375x667` (see Acceptance) and adds one line under "Keyboard and accessibility" in `docs/player.md` if a rule changes. They do not touch `audio-menu.*`.

**B: Audio settings and panel** (implementer; one worker, owns the EGS-62 merge)
- *Inputs:* the contract above, research section 2, VN reference `visual-novels-orchestrator/src/engine/game/player-runtime.ts:236-258, 2400-2444, 4248-4275`.
- *Outputs:* the files in the table marked B; `yarn test`, `yarn typecheck`, `yarn lint`, `yarn test:e2e` green; ROADMAP EGS-62 row; `.claude/tickets/EGS-62-mobile-music/plan.md` pointer + changelog; after A1-A4 land on the branch, a local merge to `master` (repo habit, as EGS-60), **not pushed**.
- *Contract with A:* `--edu-corner` and the test ids above; B does not edit shell CSS files.
- *Contract with D:* after the merge, `out/player/player.js` built from `master` is what every game gets; B records its md5 in the run log.

**C: Music for the three German games** (main session or a worker with MCP; live; can start now)
1. `scripts\hub.ps1 status`. `~/EduGames/engine.lock` names pid 31968 (2026-11-04); port 7463 did not answer on 2026-11-07, so it is stale. Then `scripts\hub.ps1 start chiptune-studio` and `scripts\hub.ps1 start edu-studio` (user-approved). Nothing else is started (not ComfyUI, not Scriptorium). If this session's `edu-studio` / `chiptune-studio` MCP clients stay disconnected after the start, reconnect them (`/mcp`) or call `http://127.0.0.1:7463/mcp` with JSON-RPC.
2. `edu_studios_status`: Chiptune Studio must be up. If it is down, stop: placeholders (one second of silence) would be built in and the games would look "done" with no music.
3. Backup: `robocopy C:\Users\Infplane\EduGames\courses\<slug> C:\projects\Personal\creative-hub\.claude\temp\hub-28-backup\<slug> /E /XD build` and separately `build`, for all 4 slugs (suncev-sustav build only).
4. Per slug in `deutsch-roleplay-a1`, `deutsch-roleplay-b2`, `deutsch-a1-pilot`:
   - `edu_media_settings {slug, set: {music: {enabled: true, provider: "chiptune"}}}` (an explicit provider wins over the ComfyUI default for menu/unit music, `edu/music.ts:189-199`; SFX are always Chiptune; `flowCredits` stays false).
   - `edu_music_plan {slug, fallback: true}`: no model; areas menu, `unit-u1..u4`, boss, end, plus `castle`, `rpg-overworld`, `rpg-battle` for the pilot (mindmaze + rpg); default 3 tracks spread over the areas; SFX correct, wrong, combo, level-up, boss.
   - `edu_asset_generate {slug, kind: "music"}`, `edu_wait {slug}`; then `{kind: "sfx"}`, `edu_wait`.
   - `edu_asset_list {slug, kind: "music"}` and `{kind: "sfx"}`: `summary.audioPlaceholders` must be 0 and every track have `loop` points. A placeholder: retry once; still failing, mark that slug NOT DONE for music and continue.
   - `edu_status {slug}` / the job log: confirm no model call and no spend (`spend` events none).
- *Outputs:* run log rows: slug, media settings before/after, plan (track ids, areas, chip), job ids, asset ids and durations, placeholders. The course `pack.json` now has `cues` (`music:<area>` loops + one-shot events) after the re-link.
- *Contract with D:* C does not build; D builds after B's merge so the new music and the new player land in one build.

**D: Rebuild the 4 games** (main session or worker; after B's merge and C)
1. In `edu-game-studio` on `master` (with EGS-62): `scripts\hub.ps1 build edu-studio` (= `yarn build:engine`, includes the player), then `scripts\hub.ps1 stop edu-studio` and `start edu-studio` so the engine copies the new `out/player`.
2. Per slug (`suncev-sustav`, `deutsch-roleplay-a1`, `deutsch-roleplay-b2`, `deutsch-a1-pilot`): `edu_build {slug}`, then `edu_lint {slug}` (errors 0; placeholder warnings only for slugs C marked NOT DONE). Fallback without the engine: stop it, `fnm exec --using default node out/engine/index.js build <slug>`.
3. Bot per slug and per enabled shell, at phone size: `node scripts/play.mjs C:\Users\Infplane\EduGames\courses\<slug>\build --mode perfect --shell <id> --viewport 375x667 --shots .claude\temp\hub-28\real\<slug>-<id>` (pass = no overflow, no console error, the run finishes). One desktop run per slug at the default viewport.
4. `md5sum` of each `build/player.js`: one value, equal to B's.
- *Outputs:* run-log table: slug, build messages, file count and size before/after, lint, bot per shell, md5. A failing slug: restore from backup, mark NOT DONE, continue.

**E: Publish, commit, push, records** (main session)
1. `creative-hub-web`: create `WEB-04_edu-mobile-music` (approved with this plan). Add to `content/catalog.json` after `deutsch-roleplay-b2` (order 100):
   ```json
   { "id": "deutsch-a1-pilot",
     "title": { "en": "German for Beginners, A1", "hr": "Njemački za početnike, A1" },
     "blurb": { "en": "German from the first word in four units with 46 exercises, short articles, a castle to explore and a small adventure game. For Croatian and English speakers starting German.",
                "hr": "Njemački od prve riječi u četiri cjeline s 46 vježbi, kratkim člancima, dvorcem za istraživanje i malom pustolovnom igrom. Za govornike hrvatskog i engleskog koji počinju učiti njemački." },
     "order": 105,
     "plays": [ { "id": "deutsch-a1-pilot-game", "type": "edu-game", "label": { "en": "Learning game", "hr": "Igra za učenje" },
                  "languages": ["de", "en", "hr"], "source": "edu:deutsch-a1-pilot/build", "player": "edu" } ] }
   ```
   (counts checked: 4 units, 46 items in `course/pack.json`; the worker re-checks them and the blurbs of the other two German games, which do not mention music, may get "and chiptune music" added.)
2. `npm run publish -- --only suncev-sustav`, `--only deutsch-roleplay-a1`, `--only deutsch-roleplay-b2`, `--only deutsch-a1-pilot` (exit 1 = smoke failed, stop; exit 2 = over the 600 MB budget, 418.8 MB used before).
3. `npm run build && npm run check && npm run test:unit && npm run test:e2e`.
4. Commit (heredoc, attribution line) on `WEB-04_edu-mobile-music`, merge into `master`, `git push origin master` (requested by the user; no force push). Watch the Pages Action, open the live `play/deutsch-a1-pilot-game/` and one republished play.
5. Hub: HUB-28 row in `ROADMAP.md` (next row number after HUB-27's 21), `runs/hub-28-edu-mobile-music.md` with every id (job ids, asset ids, md5, commits, URLs) and the DONE / NOT DONE / UNTESTED list. Ask the user before committing on hub `master`.
- *Rollback:* a game: `robocopy <backup>\<slug>\build <course>\build /MIR` (and the course folder for C); the site before push: drop the branch; after push: `git revert <merge>` and push; the player: revert the EGS-62 merge locally.

## Acceptance criteria and the test proving each

Tests are extended, not added, per the test-discipline rule. New tests: none beyond those listed.

| # | Criterion | Proof |
|---|---|---|
| A1 | At 360x740 with touch, in each of the 6 shells, the title screen and the first in-game screen have no sideways scroll, no visible button under 44 px high, the speaker button is visible and overlaps no other visible button. | `tests/android-mobile.e2e.test.ts`: the existing quiz-arena test keeps its back-button part; its viewport/scroll/size checks move into a loop over `['quiz-arena','encyclopedia','mindmaze','rpg','roleplay','detective']` (fixture per shell as in the bot tests), entering each shell's first world screen by its existing test id. One `it` per shell in the loop. |
| A2 | Each shell plays through at 375x667 with no overflow and no console error. | `bot.e2e`, `bot-encyclopedia`, `bot-mindmaze`, `bot-rpg` (already 360x740), `bot-roleplay`, `bot-detective`: the first `--mode perfect --seed 1` run of each gets `--viewport 375x667` (the bot's `overflowCheck`, `play.mjs:322`, fails on overflow). No new runs. |
| A3 | Desktop is unchanged. | The other bot runs stay at 1280x800; A0 and D desktop screenshots compared by eye, noted in the run log. |
| A4 | Volume channels and curve: music `cue * gain`, 0 stops the track and raising it restarts; SFX scaled and silent at 0; `voice(el)` sets and live-updates the clip; duck still 0.3. | `tests/player-audio.test.ts`: two tests (music + SFX; voice + duck) with the fake Audio. |
| A5 | Old saves get 100/100/100; out-of-range values are clamped; values survive export/import. | `tests/player-progress.test.ts`: one test. |
| A6 | In every shell the panel opens from the speaker button; moving the music slider changes the playing track's volume; the value survives a reload; Escape closes it and focus returns to the button. In the quiz arena the panel also works in a round (the button is present on `item-body`), and the role-play clip ducks the music. | `tests/audio-shells.e2e.test.ts`: the existing loop `for (const shell of ['quiz-arena'])` widens to all 6 shells and gains these steps; the role-play duck is one extra assert in the roleplay iteration. |
| A7 | All new strings exist in en, hr, de. | Existing `tests/player-i18n.test.ts` (key parity). |
| A8 | Unit, type, lint and browser suites green. | `yarn test && yarn typecheck && yarn lint && yarn test:e2e` (AGENTS.md rule for player changes). |
| A9 | The 3 German games have Chiptune music and SFX, no placeholders, no paid call. | `edu_asset_list` summaries (`audioPlaceholders: 0`), `game-data.json` cues contain `music:menu` and `correct`, job log without spend; in the run log. |
| A10 | The 4 rebuilt games pass lint and the bot at 375x667 in every enabled shell, and share one `player.js`. | D step 2-4 output in the run log. |
| A11 | The site passes and shows `deutsch-a1-pilot`. | `npm run publish` smoke x4, `npm run check && npm run test:unit && npm run test:e2e` (`players.spec.mjs` picks up the new edu play from the catalog; `tv-nav.spec.mjs` still reaches Start with arrows). |
| A12 | Live. | Pages Action green; the live pilot URL loads (checked by fetch or browser). |

## Reproduction (fails before the fix)

- A2: `node scripts/play.mjs <solar-system build> --mode perfect --shell encyclopedia --viewport 375x667` on today's `master`. If it passes (the CSS may already be fine), A0's screenshots are the evidence instead; record which.
- A6: the widened `audio-shells.e2e` fails on `master` at `[data-testid="audio-settings"]` (no such element). Record the failing run in the run log before B's change.

## Risks

- **Shared CSS** (`items.css`, `base.css`) also styles the studio live preview (`embed.css`); keep phone rules inside width/pointer media queries.
- **Speaker button collisions**: fixed top-right over shell HUDs (quiz score, RPG HUD). Mitigated by `--edu-corner` and test A1. The studio preview (`embed.css`) mounts only item renderers, not the shell render paths, so the button does not appear there; but `listening.ts` runs in the preview, so `ctx.voice` must stay optional (as `ctx.duck` is).
- **Bridge and TV**: the site bridge does spatial D-pad navigation on Edu plays; a new focusable top-right button may change what ArrowUp/Down reach. `tv-nav.spec.mjs` must stay green; if it fails, give the button `tabindex` order after `main` (it already is last in `.edu-app`) rather than changing the bridge.
- **Re-render while open**: shells re-render whole screens; the open state kept in the session object covers it. RPG and timed quiz rounds keep running while the panel is open (no pause); acceptable, noted.
- **Loudness change**: defaults 100 keep today's loudness; picking VN's 48 would make music much quieter. Decision recorded below.
- **Engine and MCP**: the engine lock is stale; `hub.ps1 start edu-studio` should replace it. This session's MCP clients for edu-studio/chiptune-studio failed to connect at start (servers down); after starting them a reconnect may be needed.
- **Chiptune down mid-run** gives silent placeholders that build fine; A9 checks `audioPlaceholders`.
- **Music settings vs pipeline state**: `steps.json` still says `music_*: skipped`; we generate through the asset tools, not `edu_run_pipeline`, so the pipeline state stays stale (a later `edu_run_pipeline` resume would not redo music). Note in the run log.
- **Edu build copies the player at build time**: building before B's merge and `hub.ps1 build edu-studio` would ship the old player; D checks md5.
- **Site size**: music adds a few MB per game (re-encoded on publish); budget headroom ~180 MB.
- **Global git rules**: no branch created and no commit on a default branch without the user's yes; the plan's approval covers the two named branches and the web push; hub `master` commits are asked separately.
- **Untestable here**: real phones (iOS Safari, Android Chrome) and real audio output; the user plays it ("done only when the user has played it").

## Stays UNTESTED (until the user tries it)

- Real phones: layout feel, tap targets, the speaker button under notches, audio slider feel and volume on device speakers.
- The new Chiptune music heard by a person (quality, loudness against voices).
- Edu plays on the TV with the new button.

## Decisions for the parent or user

1. Slider defaults 100/100/100 (today's loudness) instead of VN's 48/80/90. Recommended; say if VN numbers are wanted literally.
2. No separate voice mute (all Edu clips play on tap; listening needs them). "Mute" = the Sound toggle + sliders at 0.
3. `deutsch-a1-pilot` catalog title and blurb (draft above), order 105.
4. The title-screen Sound / Reduce audio toggles stay alongside the new panel.
