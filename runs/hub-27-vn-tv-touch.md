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
