# HUB-27 changelog

## 2026-11-05: HUB-27, the VN player works on TV and touch screens, and all 13 plays are rebuilt and live

### visual-novels-orchestrator (branch `VNO-62_tv-touch-controls`, merged locally into `master` at `ab4589c`, not pushed)

- `src/engine/game/player-runtime.ts`
  - **Language picker.** The three language `<select>`s are now buttons with the same ids. They open a shared picker `#vno-picker` that works with keys, touch and mouse.
  - **Voice controls.** A top-right HUD cluster holds `#vno-voice-stop` and `#vno-voice-mute`. Preferences gets a matching Voices row. `settings.voiceMuted` defaults to false, and a mute skips the line and picture-book clips and un-ducks the music.
  - **Keys.** One key handler on `document` with key and keyCode fallbacks:
    - Focus moves within layers, arrows move it by position, and OK clicks.
    - Back closes a layer. In play it opens the new pause menu `#vno-pause-menu`, which replaces "Esc opens Preferences". On the main menu Back is left to the site.
    - History `pushState`/`popstate` handles Android Back.
    - Something is focused on load and whenever a layer opens. The `vno-kb` focus ring shows during key use.
  - **Flag.** The player sets `data-vno-nav="1"` and `window.VNO_NAV.focusFirst`.
  - **Touch.**
    - `--vno-hud-k` scales HUD targets to at least 48 px on a coarse pointer.
    - A tap anywhere on the stage advances, except on controls.
    - Portrait shows the rotate hint.
    - Hover styles apply only under `(hover: hover)`, and the stage has `touch-action: manipulation`.
  - **OK grace.** An OK within 700 ms of an auto focus is ignored only on choices and the ending card, and any arrow key ends the grace (two follow-up commits, `11ff056` and `35a23cd`).
- `src/shared/ui-strings.ts`: 8 new `PLAYER_UI_KEYS`, each with a Croatian string.
- `tests/renpy-template.test.ts`:
  - The FakeElement harness gained focus, closest and matches, plus `document.activeElement`.
  - Chip and Preferences tests now click the trigger and then pick from the picker.
  - New tests: the generated HTML has no `<select`; Enter on a HUD button clicks once and does not advance; voice Stop and Mute work.
- `ROADMAP.md`: the VNO-62 row.
- `.claude/tickets/VNO-62_tv-touch-controls/plan.md`: a pointer to this plan.

### creative-hub-web (branch `WEB-02_vn-tv-touch`, merged into `master` at `1718a13` and pushed)

- `src/bridge/hub-bridge.js`: with `data-vno-nav="1"` (checked at key time) the bridge stands down for vn:
  - In the capture phase it handles only keys aimed at its own pill.
  - In the bubble phase it acts on a Back key, and on ArrowUp (focusing the pill), only when the player left the key unhandled.
  - It does no auto focus and no `hubb-kb`.
  - Builds without the flag behave as before.
- `playwright.config.mjs`: new projects `vn-tv` (1920x1080) and `vn-touch` (844x390, touch).
- `tests/e2e/helpers.mjs`: VN selectors.
- `tests/e2e/vn-player.spec.mjs`: new, 6 tests (the reproduction test, A2, A3, A4, A6 and A7).
- `README.md`: a note on the flag.
- `public/play/<13 VN plays>/`: the player files and `game-data` changed. `content/publish-manifest.json` was updated.

### creative-hub

- `ROADMAP.md`: the HUB-27 row.
- `runs/hub-27-vn-tv-touch.md`: the run log, with the rebuild table, ids and md5s.

### Deviations

- Two player fixes were needed after the first full e2e run on the rebuilt plays (OK grace scope, then arrow ends grace). Each meant another rebuild of all 13 plays and another publish. The final state is run 3.
- From T1's report:
  - In a picture book, Back still goes to the main menu, because it has no pause menu.
  - A puzzle overlay counts as a layer.
  - Android Back in plain play leaves the page, because no baseline history state is pushed.
- Publishing used `--only` for the 12 VN works rather than `--force`. Media was cached, and only the JS changed.

### Verification

| Check | Result |
|---|---|
| VN Studio `yarn test` | 1151 of 1151 passed (88 files) |
| VN Studio `yarn typecheck` | ok |
| VN Studio `yarn lint` | ok |
| chrome61 lowering and `node --check` of `player.js` (T1) | ok |
| Reproduction spec before the fix | 6 of 6 failed (`creative-hub-web/.claude/temp/hub-27-repro-before.txt`) |
| Reproduction spec after the fix | 6 of 6 passed |
| Rebuild | 13 of 13 ok, 0 missing assets, 0 placeholders |
| Publish smoke check | 13 of 13 ok |
| Site `check` | PASSED |
| Site `test:unit` | 4 of 4 passed |
| Site full `playwright test` | 50 of 50 passed |
| Pages deploy run 42044090742 | success |
| Live play | `player.js` md5 matches, the flag is present, 0 selects, focus on Start, Esc opens the pause menu, no errors |

Not run (UNTESTED): the real TV, phones and tablets, real audio, and puzzle overlays with a remote or touch.

### Follow-ups

- Push VN Studio `master`; it needs the user's go-ahead.
- The user plays a rebuilt story on the TV and on a touch device.
- Delete the backups in `.claude/temp/hub-27-backup/` when the user says so.

### Commit status

- VN Studio: committed and merged locally, not pushed.
- Site: committed, merged and pushed.
- Hub: committed on `master`.
