# HUB-27 VN web player on TV and touch screens: rebuild and republish

Started 2026-11-05. Ticket: `.claude/tickets/HUB-27-vn-tv-touch-controls/plan.md` (request REQ-0017). The user approved the plan on 2026-11-05 with both recommended decisions: a new pause menu that Back/Esc opens in play, and a rebuild from VN Studio `master` after a local merge of VNO-62.

## Branches and commits

| Repo | Branch | Commits |
|---|---|---|
| visual-novels-orchestrator | `VNO-62_tv-touch-controls` (from `master` 61a4ba7) | `a57cfff` player; `11ff056` OK grace only for choices and the ending card; `35a23cd` an arrow ends the OK grace |
| visual-novels-orchestrator | `master` (local merges, **not pushed**) | `7cf05e8` merge, `0880ad2` roadmap line, `b9a7786` merge, `ab4589c` merge |
| creative-hub-web | `WEB-02_vn-tv-touch` (from `master` 0406aaf) | `e444b72` bridge stand-down plus e2e; `4a664ec` republished plays |
| creative-hub-web | `master` | `1718a13` merge, pushed to `origin/master` (no force) |

The two follow-up VNO-62 commits came from the first site e2e run on the rebuilt plays:
1. The 700 ms OK grace after an auto focus also swallowed the first OK on the main menu. That broke 13 `players` tests and 3 `vn-tv` tests. The grace now applies only to choices and the ending card.
2. With a single choice, ArrowDown keeps focus on that choice, so the next OK still fell inside the grace (`the-clockless-god-choices`). An arrow key now ends the grace.

## Reproduction test (before the fix)

`tests/e2e/vn-player.spec.mjs` ran on the old `dist/` with the new bridge. Full output: `creative-hub-web/.claude/temp/hub-27-repro-before.txt`.

Result: 6 of 6 failed.
- `language can be changed with remote keys only`: "the language chip not reached with ArrowUp, ArrowRight".
- Main-menu chip and Preferences UI language: `#vno-picker` not found.
- A3: `html[data-vno-nav="1"]` count was 0.
- A4: "the History button not reached".
- A6: `#vno-voice-stop` count was 0.
- A7: `#vno-rotate-hint` not found.

After the fix the same spec passed 6 of 6, inside the full run below.

## Rebuild (T3)

Pre-checks:
- `hub.ps1 status`: every service was down.
- `engine.lock` named pid 25812, which is not running, so the lock was stale and the CLI replaced it.
- Disk: 270 GB free.

Backups:
- Location: `.claude/temp/hub-27-backup/<slug>-game` plus `<slug>-build.json` (git-ignored).
- The file counts matched the source.
- Keep them until the user has played on the TV.

Builds:
- Command: `yarn engine -- build <slug>` from VN Studio `master`.
- Canary: `the-trap-room-at-the-lanterna` went first and passed.
  - The file set was the same, and the images, audio and fonts were byte-identical.
  - `game-data.json` changed only by the new `presentation` and `uiLanguages` keys plus extra character fields. The chapters were identical.
  - `shot-game.mjs` showed the title screen.
- Run 3 was the final player at `ab4589c`. Its results are in the table.

| Slug | Play | Files old/new | KB old/new | Media files | build.json messages | Result |
|---|---|---|---|---|---|---|
| the-trap-room-at-the-lanterna | the-trap-room-at-the-lanterna-vn | 73/73 | 35835/35991 | 48/48 | none | ok |
| the-clockless-god-2 | the-clockless-god-choices | 140/140 | 44863/44895 | 104/104 | speakers RADIO, VOICE, HOODS have no sprite (same as before) | ok |
| the-clockless-god-3 | the-clockless-god-linear | 147/147 | 48287/48451 | 104/104 | speaker VOICE has no sprite (same as before) | ok |
| the-snail-and-the-salad | the-snail-and-the-salad-picture-book | 114/119 | 7670/7721 | 88/88 | none; added 5 Ren'Py `tl/german/*.rpy` files, which the site does not publish | ok |
| the-bell-and-the-bicycle | the-bell-and-the-bicycle-picture-book | 110/110 | 14418/14458 | 84/84 | none | ok |
| the-soother-that-fell-into-dragon-land | the-soother-that-fell-into-dragon-land-choices | 75/75 | 6960/7116 | 36/36 | none | ok |
| the-winter-garden-clock | the-winter-garden-clock-vn | 100/100 | 32512/32544 | 75/75 | none | ok |
| the-local-patch-2 | the-local-patch-vn | 110/110 | 51184/51212 | 85/85 | chapter 2 CG line dropped (same as before) | ok |
| circuit-breaker-2 | circuit-breaker-vn | 172/172 | 117923/117951 | 142/142 | none | ok |
| echoes-in-the-deep-2 | echoes-in-the-deep-vn | 153/153 | 108651/108683 | 123/123 | none | ok |
| the-salt-line-2 | the-salt-line-vn | 165/165 | 127895/127931 | 136/136 | none | ok |
| the-silent-signal-2 | the-silent-signal-vn | 165/165 | 121999/122043 | 135/135 | none | ok |
| the-silent-summit-2 | the-silent-summit-vn | 137/137 | 117159/117195 | 109/109 | none | ok |

- No asset went missing and there were 0 placeholders.
- Nothing was generated and nothing was spent.
- `player.js` md5:
  - Source in all 13 projects: `3a8f8fa1f2c7c8d96a837c0253342e75`.
  - Published copy, lowered to chrome61, in all 13 `public/play/*/player.js`: `1e1be1e7f83ba4cf91aacb0e501dc1e2`.

## Publish and checks (T4)

All of these ran on `WEB-02_vn-tv-touch` in `creative-hub-web`.

- Publish: `npm run publish -- --only <12 work ids>` exited 0.
  - The smoke check passed for all 13 plays.
  - Of 1791 files, 12 were re-encoded (player and game-data JS) and 1779 cached; media was unchanged.
  - Size: 418.8 MB of the 600 MB budget.
- `npm run build`: ok.
- `npm run check`: PASSED.
- `npm run test:unit`: 4 of 4 passed.
- `npx playwright test`: 50 of 50 passed. That covers the existing `players`, `tv-nav`, `touch` and `desktop` specs plus the new `vn-tv` and `vn-touch` specs.

## Push and deploy

- `git push origin master` updated `0406aaf..1718a13`.
- The "Deploy site" Action run 42044090742 succeeded: https://github.com/Tihi321/creative-hub-web/actions/runs/42044090742
- Live check at https://tihi321.github.io/creative-hub-web/play/the-clockless-god-linear/:
  - HTTP 200, and the live `player.js` md5 is `1e1be1e7...`, which matches.
  - In headless Chromium at 1920x1080: `data-vno-nav="1"`, `VNO_NAV` and the bridge are present, there are 0 `<select>`s, and Start is focused on load.
  - Enter starts the game. Esc opens the pause menu, with Resume focused.
  - No page errors.

## Status

- DONE: T1 player (VNO-62), T2 bridge and e2e (WEB-02), T3 rebuild (13/13), T4 publish, push and deploy, T5 these records.
- UNTESTED:
  - The real Android / Google TV Chrome: its key codes, Back sent as a key versus a history Back, the focus ring at TV distance, and overscan.
  - Real phones and tablets: the tap feel and the rotate hint.
  - Voice mute and stop on real audio.
  - Puzzle overlays (out of scope).
- Not pushed: VN Studio `master`. It was merged locally and needs the user's go-ahead to push.
- The production is done only when the user has played a rebuilt story on the TV and on a touch device.

## Polish round 1 (checker findings, 2026-11-05)

Four fixes after the checker's first round. Nothing was generated and nothing was spent.

| # | Finding | Result |
|---|---|---|
| 1 | Android / Google TV Chrome sends remote Back as history navigation; in plain play it left the story for the item page | DONE |
| 2 | chrome61 CSS: `min()` without a fallback, flex `gap` | DONE |
| 3 | Bridge: Back on the main menu with keyCode 4 / Esc / Backspace | DONE |
| 4 | Two vn-tv e2e tests | DONE |

### Changes

- **VN Studio** `player-runtime.ts`, branch `VNO-62_tv-touch-controls`, commit `2fccf5d`; `master` fast-forwarded to it (local, not pushed).
  - History: while a story plays (main menu hidden, counted by `inPlay()`), the player keeps one baseline history entry. Start, Load and picture-book start push it (the main menu is hidden first, then `closeAllScreens()` syncs). A popstate with no layer open in play opens the pause menu and pushes the baseline again. `returnToMainMenu` hides the screens, shows the menu and syncs once, so one `history.go(-n)` drops the baseline and any layer entries (counted by `ignorePops`). Back on the main menu then leaves the game.
  - Picture book: Back key and history Back open the pause menu (`openPauseMenu` no longer returns for picture books). Its pause menu shows Resume, Preferences and Main Menu only (Save, Load and History get `vno-hidden`, since a picture book has no such screens). The page-layer menu button still goes straight to the main menu.
  - A VN load (`loadFromSlot`) now hides the main menu before it closes the screens, as the picture-book branch already did.
  - CSS: a fixed fallback declaration before each of the 7 `min()` values; the 13 flex `gap`s became `> * + *` margins (`margin-left`, mirrored under `[dir="rtl"]`, or `margin-top`); the save slot grid uses `grid-gap`.
- **Site** `creative-hub-web`, branch `WEB-02_vn-tv-touch` (brought up to master `1718a13` first), commits `6af1aa3` (bridge, check, tests) and `ac381ec` (13 republished plays), merged as `3b7c088`, pushed to `origin/master` (no force).
  - `hub-bridge.js`: `isOwnedBackKey` (the owned bubble path only) also accepts keyCode 4, Escape and Backspace without modifiers. The old-build path is unchanged.
  - `check-site.mjs`: every VN play's `player.css` (a play whose bridge tag has `data-player="vn"`; the Edu plays ship their own minified CSS) goes through the existing banned list (`gap`, `inset`, `clamp()`, ...) plus a `min()` rule: the previous declaration in the same block must set the same property to a fixed value. Negative-tested on a copy (a removed fallback and an added flex `gap` were both flagged); the shipped CSS passes. The CSS check now covers 14 files (site.css and 13 plays).
  - Tests: `vn-player.spec.mjs` got the history-Back test (item page, then play, Start, `page.goBack()`: `#vno-pause-menu` visible and URL unchanged, again after Resume, then Main Menu and `goBack` leaves for the item page) and the choice test (`the-clockless-god-choices`: Enter to the first choice, Enter once clicks once and lands on the next chapter's start, `beatIdx` -1).

### Rebuild (13 plays, `yarn engine -- build <slug>` from VN Studio `master` 2fccf5d)

Files, KB and media (images, audio, fonts) counted in `projects/<slug>/game` before and after. The backups in `.claude/temp/hub-27-backup/` were not touched.

| Slug | Files before/after | KB before/after | Media before/after | build.json | Messages |
|---|---|---|---|---|---|
| the-trap-room-at-the-lanterna | 73/73 | 35991/35995 | 55/55 | ok, 0 placeholders | none |
| the-clockless-god-2 | 140/140 | 44895/44899 | 111/111 | ok, 0 | speakers RADIO, VOICE, HOODS have no sprite (same as before) |
| the-clockless-god-3 | 147/147 | 48451/48455 | 111/111 | ok, 0 | speaker VOICE has no sprite (same as before) |
| the-snail-and-the-salad | 119/119 | 7721/7725 | 95/95 | ok, 0 | none |
| the-bell-and-the-bicycle | 110/110 | 14458/14462 | 91/91 | ok, 0 | none |
| the-soother-that-fell-into-dragon-land | 75/75 | 7116/7120 | 43/43 | ok, 0 | none |
| the-winter-garden-clock | 100/100 | 32544/32548 | 82/82 | ok, 0 | none |
| the-local-patch-2 | 110/110 | 51212/51216 | 92/92 | ok, 0 | chapter 2 CG line dropped (same as before) |
| circuit-breaker-2 | 172/172 | 117951/117955 | 149/149 | ok, 0 | none |
| echoes-in-the-deep-2 | 153/153 | 108683/108687 | 130/130 | ok, 0 | none |
| the-salt-line-2 | 165/165 | 127931/127935 | 143/143 | ok, 0 | none |
| the-silent-signal-2 | 165/165 | 122043/122047 | 142/142 | ok, 0 | none |
| the-silent-summit-2 | 137/137 | 117195/117199 | 116/116 | ok, 0 | none |

`player.js` md5: source in all 13 projects `12727c370449ebfcd516f77548173ad1`; published copy (lowered to chrome61) in all 13 `public/play/*/player.js` `16f523ecf72871529c27046c525194e9`.

### Checks

- VN Studio: `yarn test` 1151 of 1151 (88 files), `yarn typecheck` ok, `yarn lint` ok.
- Site: `npm run publish -- --only <the 12 VN work ids>` exit 0 (smoke check 13 of 13 ok; 13 copied and encoded, 1765 cached; 418.8 MB of 600 MB), `npm run build` ok, `npm run check` PASSED (css 14 checked), `npm run test:unit` 4 of 4, full `npx playwright test` 52 of 52 (50 before, plus the 2 new vn-tv tests).
- Ad hoc in headless Chromium on the new build (not part of the suite): on the main menu Escape, Backspace and keyCode 4 each leave for the item page; a picture book opens the pause menu with Resume, Preferences and Main Menu and focuses Resume, and history Back reopens it; Save, Main Menu, Load, history Back opens the pause menu, then Main Menu and Back leaves; the gaps between the children of all 13 reworked containers measured equal to the old `gap` values.

### Push and deploy

- `git push origin master` updated `1718a13..3b7c088`; the "Deploy site" run 42049363165 succeeded: https://github.com/Tihi321/creative-hub-web/actions/runs/42049363165
- Live probe (headless Chromium 1920x1080, https://tihi321.github.io/creative-hub-web/play/the-clockless-god-linear/, arriving from the item page): after Start, `goBack` opens the pause menu and the URL stays on the play; after closing it a second `goBack` does the same; Main Menu then `goBack` lands on `/item/the-clockless-god/`. The picture book (`the-snail-and-the-salad-picture-book`) behaves the same. No page errors. The live `player.js` is the new file.

### Status

- DONE: findings 1 to 4, rebuild 13/13, publish, push, deploy, live probe.
- UNTESTED: a real Android / Google TV Chrome. In particular whether Chrome's history-manipulation intervention skips the baseline entries on a real Back press (the entries are pushed after a click or key press, so the page has user activation), the focus ring at TV distance, overscan, the old Chrome 61 layout of the margin-based gaps and `min()` fallbacks (measured only in current Chromium), phones and tablets, voice on real audio.
- Not pushed: VN Studio `master` (local, 8 commits ahead of origin) and the creative-hub repo.
