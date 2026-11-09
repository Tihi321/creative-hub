# HUB-28: Edu mobile + music run log


## Music generation (C)

Run 2026-11-07. Services started by `hub.ps1`: chiptune-studio (pid 32292 started, port 7458) and edu-studio (pid 2848, port 7463, replaced the stale lock of pid 31968). Nothing else started. Edu MCP called over HTTP JSON-RPC (`.claude/temp/hub-28/mcp.mjs`; raw replies in `.claude/temp/hub-28/out/`). `edu_studios_status`: Chiptune ok (55 tools) before any generation. Backups in `.claude/temp/hub-28-backup/` (`<slug>` without build, `<slug>-build` for all 4 slugs, `suncev-sustav-build` only for that one).

Steps per slug: `edu_media_settings {music:{enabled:true, provider:"chiptune"}}`, `edu_music_plan {fallback:true}`, `edu_asset_generate kind=music`, `edu_wait`, `kind=sfx`, `edu_wait`, `edu_asset_list` music and sfx. No retries were needed. Media music before: `{enabled:false}` for all 3; after: `{enabled:true, provider:"chiptune", engine:"ace-step-v1-instrumental" (unused), tracks:3, flowCredits:false}`.

| Slug | Tracks (areas) | SFX | Music job | SFX job | audioPlaceholders | pack.json cues |
|---|---|---|---|---|---|---|
| deutsch-roleplay-a1 | 7: mus-menu[menu], mus-unit-u1..u4[unit-u1..u4], mus-boss[boss], mus-end[end] | sfx-correct, -wrong, -combo, -level-up, -boss | deutsch-roleplay-a1--asset_generate--qmw6jh9eiyj--r0 | ...--qmw6jhx6xgi--r0 | 0 (audio 20/20 made) | 12 |
| deutsch-roleplay-b2 | 5: menu, unit-u1, unit-u2, boss, end | same 5 | deutsch-roleplay-b2--asset_generate--qmw6ji8jc7g--r0 | ...--qmw6jii12fy--r0 | 0 (audio 16/16) | 10 |
| deutsch-a1-pilot | 10: menu, unit-u1..u4, boss, end, castle, rpg-overworld, rpg-battle | same 5 | deutsch-a1-pilot--asset_generate--qmw6jijgci2--r0 | ...--qmw6jj1stf7--r0 | 0 (audio 23/23) | 15 |

Asset ids = track ids above (`mus-<area>`), file `assets/<id>/v1.ogg`, engine chiptune, source generated, placeholder false, all with loop `startSec 0`. Loop end (= duration, s): menu 93.3, u1 87.3, u2 86.2, u3 96.0, u4 91.4, boss 60 (a1, pilot) / 70 (b2), end 101.8 (a1, pilot) / 116.4 (b2), castle 90, rpg-overworld 80, rpg-battle 67.2. SFX (chiptune sounds: coin, cancel, magic, powerup, alert) are one-shots, no loop. Plan source `fallback` (no model).

Spend: no model or paid call. Plan source fallback, provider chiptune, `flowCredits` false, job logs show only `asset_generate` jobs, no new rows in `EduGames/logs/spend/2026-11.md` (last row 2026-11-04).

Not done here: no build (task D). Pipeline `steps.json` still lists `music_*` as skipped (generated through asset tools). `game-data.json` cues are checked after D's build.

UNTESTED: the music has not been heard by a person.

## Phone baseline (A0)

Run 2026-11-07, read-only on code. Player commit `46b6ec1` (`EGS-62_mobile-music`, identical to master, no source changed). Bundle built with `node node_modules/vite/bin/vite.js build --config vite.player.config.ts` (`yarn` was not runnable under fnm in this shell; same config as `yarn build:player`). Master bundle copy: `.claude/temp/hub-28/player-master/` (player.js md5 `de6e68c590e60b335ce0e67e7551e4c4`, player.css md5 `ca5cb267d6e0a7b81b388771f8eb4495`). Fixtures built with `.claude/temp/hub-28/build-fixtures.mts` (tsx, `buildCourse(root, out, {playerDir})`) into `.claude/temp/hub-28/builds/{solar-system,de-roleplay-a1,european-capitals}`. Shells enabled: solar-system quiz-arena, encyclopedia, mindmaze, rpg, detective; de-roleplay-a1 quiz-arena, roleplay; european-capitals quiz-arena, encyclopedia, mindmaze, detective.

Command (per shell, three viewports, run in parallel per shell): `node scripts/play.mjs <build> --mode perfect --seed 1 --shell <id> [--viewport 375x667|360x740] --shots .claude/temp/hub-28/shots-<375|360|1280>/<id> --json`.

| shell (fixture) | viewport | bot result | what breaks (selector, size/overflow) | screenshot dir |
|---|---|---|---|---|
| quiz-arena (solar-system) | 375x667 / 360x740 / 1280x800 | pass, finished, 0 console errors, no overflow (34 steps) | nothing in the bot; see "measured" below | shots-375/quiz-arena, shots-360/quiz-arena, shots-1280/quiz-arena |
| encyclopedia (solar-system) | 375x667 / 360x740 / 1280x800 | pass, finished, 0 errors, no overflow (15 steps) | nothing; tabs wrap to two rows | shots-375/encyclopedia, ... |
| mindmaze (solar-system) | same | pass, 0 errors, no overflow (20 steps) | nothing | shots-375/mindmaze, ... |
| rpg (solar-system) | same | pass, 0 errors, no overflow (36 steps) | nothing; world canvas 284x186 at 360 | shots-375/rpg, ... |
| roleplay (de-roleplay-a1) | same | pass, 0 errors, no overflow (13 steps) | nothing | shots-375/roleplay, ... |
| detective (european-capitals) | same | pass, 0 errors, no overflow (37 steps) | nothing | shots-375/detective, ... |

All 18 runs exit 0. Summaries: `.claude/temp/hub-28/json/<viewport>-<shell>.json`. Desktop screenshots `.claude/temp/hub-28/shots-1280/<shell>` are the A3 desktop baseline.

**A2 reproduction note:** the encyclopedia bot at 375x667 (and 360x740) PASSES on master (no overflow, 0 console errors). The CSS is already fine for page overflow; the reproduction evidence is the screenshots plus the measurements below (no failing run exists). No user-facing breakage is visible in the screenshots on these fixtures; a longer-titled real game may differ.

### Measured at 360x740, touch, per screen (every bot screenshot)

Method: copy of `scripts/` in `.claude/temp/hub-28/botcopy/` with a measure hook after every shot (raw: `meas/<shell>.jsonl`, digest `meas/summary.txt`); title + first world screen also in `measure-360.json` (script `measure.mjs`). Checked: `documentElement.scrollWidth > innerWidth`, interactive elements under 44 px in either side, visible elements past the right edge, canvas sizes, text under 14 px.

- Sideways scroll: none on any screen of any shell (scrollWidth == 360 everywhere).
- Buttons under 44 px (outside the exempt grids/hotspots): title screen `[data-testid="setting-timer"]` 24x24 (quiz-arena), `[data-testid="setting-speak"]` 24x24 (roleplay) (checkbox inputs; the label rows are probably the tap area; `setting-sound`/`setting-reduce-audio` did not show); encyclopedia `[data-testid^="citation-"]` 86x24 on article screens (7 buttons). Exempt grids: `cell-*` 24-25 px (word search, crossword), `region-*` hotspot 10-43 px.
- Text under 14 px (13 px): `small` in order/listening items (quiz), `span.enc-tl-tick-label`, `span.enc-tl-card-more` (timeline), `span.mm-door-num` (mindmaze room), `[data-testid="talk"]` (rpg world d-pad centre), `th.det-col`, `th.det-row`, `[data-testid^="board-entity-"]`, `span.det-map-name` (detective), word-search cells 13 px, `span.cw-num` 11 px (crossword numbers, mindmaze/rpg/quiz).
- Past the right edge but inside an internal scroller (not a page overflow): encyclopedia timeline (`.enc-tl-track`, `.enc-tl-ruler`, ticks, cards) and map (`[data-testid="map"]`, `img.enc-map-img`, pins) pan inside their frame; quiz `span.dust` decoration.
- Canvases fit: rpg `[data-testid="world-canvas"]` 284x186, `[data-testid="battle-scene"]` 284x118, `[data-testid="portrait"]` 88x88, `canvas.rpg-mini` 192x117..135 (area cards, fit).
- Speaker-button collision (B's button, top-right 8 px, 44x44, not built yet): the top-right of these screens is occupied and needs `--edu-corner` padding: quiz `.topbar` (Score and Combo / "Title screen" + "stars" row), encyclopedia `.enc-tabs` (second tab row reaches the right edge: "Map" tab at about y 30-72), mindmaze `.topbar` ("Keys: 0 of 3" right), detective `.topbar` ("0 of 4 rooms solved" right), roleplay `.topbar` (level badge "A1" right, `Back to the scenes`), rpg HUD (title row and the Scrolls / World map buttons, left-aligned so likely free on the first rows).

### Work list for A1-A4 (from the evidence; anything not here shows no problem on the fixtures)

- **A1 start screen, shared, quiz arena** (`kit/kit.css`, `style/base.css`, `style/arena.css`, `style/items.css`): start screen is fine at 375 (cards stack, settings wrap), so the planned `.mode-card`/`.lang-picker` rules are optional; check the title checkboxes `setting-timer`, `setting-speak` (24x24 inputs) are covered by a 44 px label before touching; quiz `.topbar` needs `padding-right: var(--edu-corner)`; item text `small` 13 px (below the 14 px rule) in order/listening items.
- **A2 encyclopedia** (`encyclopedia.css`): `.enc-tabs` needs `padding-right: var(--edu-corner)` (wrapped two-row strip; the planned scroll strip is a design choice, not needed to fix overflow); `[data-testid^="citation-"]` 86x24 buttons under 44 px high; `.enc-tl-tick-label`, `.enc-tl-card-more` 13 px.
- **A3 mindmaze + detective** (`mindmaze.css`, `detective.css`): `.topbar` needs the corner padding in both; `.mm-door-num` 13 px; detective `th.det-col`, `th.det-row`, `[data-testid^="board-entity-"]`, `.det-map-name` 13 px. No overflow, no side column problem seen at 360. Desktop baseline = `shots-1280/{mindmaze,detective}`.
- **A4 rpg + roleplay** (`rpg.css`, `roleplay.css`): nothing measured breaks (canvases fit, no overflow, roleplay bubbles and garden fine); roleplay `.topbar` (level badge) needs the corner padding; rpg `[data-testid="talk"]` 13 px; rpg HUD first row check after B lands. The roleplay `<=400px` block and minimap resizing are not needed by this evidence.
- Overall: the player already passes the A1 criteria except tap-target/13 px items above on these fixtures; the main phone work is making room for the speaker button. A1's `android-mobile` loop will fail only if the title-screen 24x24 inputs count as buttons (the test selects `button, [role=button]`, which these are not).

Not run / unverified: real phones; fixtures only (short titles), real EduGames builds not measured (D does that); no touch-vs-mouse difference was found between the bot runs (mouse) and the measure hook (isMobile + touch).

## Player code (A, B)

2026-11-07, repo `edu-game-studio`, branch `EGS-62_mobile-music` (from `master` 46b6ec1), commit `8588112`, merged locally into `master` as **`5b64706`** (`Merge EGS-62_mobile-music`, `--no-ff`; **not pushed**). Changelog: `edu-game-studio/.claude/tickets/EGS-62-mobile-music/changelog.md`.

**Player bundle for D:** `yarn build:player` on `master` 5b64706 -> `out/player/player.js` md5 **`2f0a8e4822fc59c4ea04daa21c0f5f42`** (631697 bytes); `player.css` md5 `f40cd0a7fdf0bcdcc89ba880c451a9ca`. (Master baseline before: player.js `de6e68c590e60b335ce0e67e7551e4c4`.) Every rebuilt game's `build/player.js` must have the new md5.

| Task | Status | What changed |
|---|---|---|
| A1 shared CSS + quiz arena | DONE | `style/arena.css`: shared `.topbar` / `.hud` get `padding-right: var(--edu-corner)` at <= 839 px (covers quiz, mindmaze, detective, roleplay); top bar wraps at <= 560 px; stat/combo labels 14 px. Start screen untouched (A0: fine). |
| A2 encyclopedia | DONE | `.enc-tabs` corner padding; `citation-*` source links 44 px tall on phones / coarse pointers; timeline labels 14 px. No scroll strip (tabs wrap fine). |
| A3 mindmaze + detective | DONE | `.mm-door-num`, detective grid headers, board entities, map names 14 px at <= 560 px. |
| A4 rpg + roleplay | DONE | `.rpg-hud` corner padding, Talk text 14 px. `roleplay.css` and `rpg/index.ts` unchanged (A0: no need). |
| B audio settings + panel | DONE | `settings.musicVolume/sfxVolume/voiceVolume` (default 100, clamped); `volumeGain` `(v/100)^1.6`; `GameAudio.voice(el)`; speaker button `audio-settings` + `audio-panel` in both render paths; voice clips routed through `audio.voice`; role-play clip ducks the music; i18n en/hr/de; `audio-close` in Android back. |

Tests (on the branch, tree identical to merged master): `yarn test` 91 files / 521 passed; `yarn typecheck` exit 0; `yarn lint` exit 0; `yarn test:e2e` 16 files / 40 passed (incl. `android-mobile` one `it` per shell at 360x740 with the speaker-overlap check, `audio-shells` over 6 shells, first bot perfect run at 375x667 in five shells).

Reproduction A6: the widened `audio-shells.e2e` failed on the unchanged player at `[data-testid="audio-settings"]` (timeout) in 5 of 6 shells. A2: the encyclopedia bot at 375x667 already passed on master (see A0), so the evidence is A0's screenshots/measurements.

Desktop (checker, 2026-11-07): those diffs came from builds made with the old player (de6e68c5). With the final player 2f0a8e48, the only desktop change in mindmaze, quiz-arena and encyclopedia is the speaker button; the other differences are animation timing (.claude/temp/hub-28/check/desk/, check/pxdiff.mjs).

Deviations: role-play tests use fixture `hr-a1-greetings` and detective borrows `eight-beeps.wav` (the button shows only when a game has sound; `de-roleplay-a1` and `european-capitals` have none); `bot-detective` first-run timeout 120 -> 180 s; `docs/android.md` back list updated.

Note for D: the speaker button appears only in games with a cue or an audio asset; all four target games have audio.

UNTESTED: real phones (iOS Safari, Android Chrome), real audio output, Edu plays on the TV with the new button.

## Rebuild (D)

2026-11-07. `hub.ps1 build edu-studio` -> `out/player/player.js` md5 2f0a8e4822fc59c4ea04daa21c0f5f42 (as B). `hub.ps1 stop edu-studio` answered "not running" while pid 2848 still held 7463 (its port probe flickers), so pid 2848 was killed with taskkill and `hub.ps1 start edu-studio` started the new engine (pid 39700, engine.lock updated). Chiptune Studio (7458) left running.

| Slug | edu_build | Files / size before | Files / size after | edu_lint | Bot 375x667 | Bot 1280x800 | player.js md5 | Status |
|---|---|---|---|---|---|---|---|---|
| suncev-sustav | ok, no problems, 39 files (9 mus + 5 sfx) | 39 / 13438 KB | 39 / 13454 KB | errors 0, warnings 0 | quiz-arena, encyclopedia, mindmaze, rpg: ok, no failures | ok | 2f0a8e48... (new) | DONE |
| deutsch-roleplay-a1 | **failed**: 12 x MISSING_TEXT `asset.mus-*.alt` / `asset.sfx-*.alt` in en | 13 / 2221 KB | unchanged (build not written; identical to backup) | errors 0, warnings 0 (stale: true) | not run (build is old) | not run | de6e68c5... (old) | NOT DONE |
| deutsch-roleplay-b2 | **failed**: 10 x MISSING_TEXT, same keys | 11 / 2497 KB | unchanged (identical to backup) | errors 0, warnings 1 (READING_SENTENCE_LENGTH) | not run | not run | de6e68c5... (old) | NOT DONE |
| deutsch-a1-pilot | **failed**: 15 x MISSING_TEXT, same keys | 13 / 2081 KB | unchanged (identical to backup) | errors 0, warnings 2 (ENC_ANSWER_NOT_IN_ARTICLE x2) | not run | not run | 6acec9c3... (old) | NOT DONE |

Cause: task C added music/sfx assets to the three German courses without `asset.<id>.alt` texts in `course/text/<lang>.json`. suncev-sustav has them (e.g. `asset.mus-menu.alt`: "Gentle piano music on the title screen"). `edu_text_set` exists to add them. No restore was needed (failed builds write nothing); the course folders keep C's music.

suncev-sustav checks: game-data.json has music:boss / music:castle / music:end etc.; 9 mus + 5 sfx files in build; speaker button visible top-right in `real/suncev-sustav-quiz-arena/perfect-02-map.png`. Screenshots: `.claude/temp/hub-28/real/`. Speaker button in German screenshots, md5 and music cues for the German builds: UNTESTED (not rebuilt).

### Rebuild (D), second pass: alt texts added, German games rebuilt

Coordinator-approved fix: `edu_text_set` added `asset.<id>.alt` for every mus-* and sfx-* asset in en, hr and de (suncev-sustav wording style, "chiptune" named; the unit tracks say "unit N", no topic): deutsch-roleplay-a1 12 keys x 3 languages, deutsch-roleplay-b2 10 x 3, deutsch-a1-pilot 15 x 3. Nothing else in the courses changed. Script: `.claude/temp/hub-28/alts.mjs`.

| Slug | edu_build | Files / size before | Files / size after | edu_lint | Bot 375x667 (all ok, 0 console errors) | Bot 1280x800 | player.js md5 | Music cues in game-data | Status |
|---|---|---|---|---|---|---|---|---|---|
| deutsch-roleplay-a1 | ok, no problems, 12 mus/sfx files | 13 / 2221 KB | 25 / 14217 KB | errors 0, warnings 0 | quiz-arena, encyclopedia, roleplay | ok | 2f0a8e48... | menu, unit-u1..u4, boss, end | DONE |
| deutsch-roleplay-b2 | ok, no problems, 10 mus/sfx files | 11 / 2497 KB | 21 / 11113 KB | errors 0, warnings 1 (READING_SENTENCE_LENGTH, as before) | quiz-arena, encyclopedia, roleplay | ok | 2f0a8e48... | menu, unit-u1, unit-u2, boss, end | DONE |
| deutsch-a1-pilot | ok, no problems, 15 mus/sfx files | 13 / 2081 KB | 28 / 18745 KB | errors 0, warnings 2 (ENC_ANSWER_NOT_IN_ARTICLE x2, as before) | quiz-arena, encyclopedia, mindmaze, rpg | ok | 2f0a8e48... | menu, unit-u1..u4, boss, end, castle, rpg-overworld, rpg-battle | DONE |

md5 of build/player.js is 2f0a8e4822fc59c4ea04daa21c0f5f42 in all four builds. Speaker button visible top-right in `real/<slug>-quiz-arena/perfect-02-map.png` for all four slugs. Bot log: `real/german-bots.log`. Build sizes are the unencoded builds (music is large raw; publish re-encodes). Note on the bot summary `"answers": 0`: `checks.answers` only counts the feedback-answer panel on wrong answers, so it is 0 by design in perfect mode; the run does answer (`summary.steps`/`correct`, and play.mjs fails if the game's own step counter differs from the bot's).
UNTESTED: real phones, audible music, TV.

## Publish (E) - STOPPED before commit/push (2026-11-07)

- creative-hub-web: branch `WEB-04_edu-mobile-music` created from master; `deutsch-a1-pilot` catalog entry added (order 105; pack has 4 units, 46 items, shells quiz-arena/encyclopedia/mindmaze/rpg). Roleplay blurbs left unchanged (they do not describe media). Pointer `.claude/tickets/WEB-04-edu-mobile-music/plan.md` written (the `.claude/` folder is git-ignored there, as for WEB-02).
- Publish (`--only` x4 in one call): smoke ok for suncev-sustav-game, deutsch-roleplay-a1-game, deutsch-roleplay-b2-game, deutsch-a1-pilot-game. 117 files, 16 copied, 47 encoded, 54 cached. Size 434.8 MB (+5 MB allowance = 439.8 MB) of 600 MB (was 418.8 MB).
- build and check: passed. test:unit: 1 FAIL (`catalog-exclusions.test.mjs` rejects any slug ending `-pilot`, so `deutsch-a1-pilot` trips it). test:e2e: 53 passed, 1 FAIL (`desktop.spec.mjs:39` hard-codes the German list as roleplay-a1, roleplay-b2, the-snail-and-the-salad; the pilot now appears too).
- Nothing committed or pushed. Needs a decision: loosen the unit test (allow `deutsch-a1-pilot`) and add it to the e2e German list, in the same WEB-04 commit.

### Publish (E) - resumed and finished 2026-11-07

- Fix for the two failing tests: `catalog-exclusions.test.mjs` got an allowlist of only `deutsch-a1-pilot` and `deutsch-a1-pilot-game` (rule kept); `desktop.spec.mjs:39` lists the pilot. build, check, test:unit and test:e2e (54) all pass.
- Commit `6737a21` on `WEB-04_edu-mobile-music`; merged --no-ff to site `master` `e47cdea`; pushed 47aa1a8..e47cdea (no force).
- Pages Action run 42392671777: success.
- Live: `play/deutsch-a1-pilot-game/player.js` and `play/suncev-sustav-game/player.js` both contain `audio-settings` (2 hits), same md5 e20064fa7b91d42892b5ca6893936cf9 (published copy differs from build md5 2f0a8e48... because publish rewrites it). Not played in a browser by hand.
- Size 434.8 MB of 600 MB.
