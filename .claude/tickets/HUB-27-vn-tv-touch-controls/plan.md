---
status: in-progress
request: REQ-0017
repos: [visual-novels-orchestrator, creative-hub-web, creative-hub]
branch:
  visual-novels-orchestrator: VNO-62_tv-touch-controls
  creative-hub-web: WEB-02_vn-tv-touch
  creative-hub: master (roadmap row, run log, this plan)
updated: 2026-11-05
---

# HUB-27: VN player on TV and touch screens, then rebuild and republish

Research: `research.md` in this folder (file:line refs). Reading of the request: the **full** one. All three language dropdowns are replaced, the player gets its own D-pad support, a voice stop and mute control and touch fixes, and all 13 published VN plays are rebuilt and pushed.

## Scope

1. **Language picker (VN Studio).** The three native `<select>`s (`#vno-stage-language`, `#vno-pref-language`, `#vno-pref-ui-language`, `player-runtime.ts:201-210, 280-283`) become `<button>`s with the **same ids**. Each opens one shared in-stage picker `#vno-picker`: a scrollable list of `<button class="vno-picker-item" role="option" aria-selected>` items with native names, the current one marked and focused. It works with arrows plus OK, touch and mouse. Esc or Back closes it and puts focus back on its trigger. Picking a language calls `switchLanguage` / `switchUiLanguage` as `change` did before. The 36 UI languages show as a list of two or three columns that scrolls with focus (`scrollIntoView`).
2. **Voice controls (VN Studio).** These go in a HUD cluster at the top right of the stage, next to the language chip:
   - `#vno-voice-stop`: enabled only while a line or page clip plays. It calls `stopVoice()` and then `setVoiceActive(false)`, which un-ducks the music.
   - `#vno-voice-mute`: a toggle with `aria-pressed`. It sets `settings.voiceMuted`, saves `vno_settings` and stops the current line. While it is on, `playVoiceForBeat` and `playNextPageVoiceClip` play nothing. The picture-book replay button is hidden while voices are muted.
   - Preferences gets a matching "Voices: on/off" button row.
   - The cluster is hidden when the game has no voice files.
   - New strings go in `PLAYER_UI_KEYS` with Croatian text.
3. **D-pad in the player (VN Studio).**
   - One key handler on `document` (bubble phase) replaces the `window` handler at `player-runtime.ts:2056-2108`. It reads `e.key` with a `keyCode` fallback, not `e.code`, because TV remotes often send no `code`.
   - **Layers.** Focus moves only inside the topmost visible layer, in this order: picker > open screen (prefs, save, history, about) > pause menu > choice overlay > ending card > main menu > in-game HUD (quick menu, voice cluster, language chip).
   - **Arrows.** Arrows move focus spatially, using `getBoundingClientRect` centres (same idea as the bridge's `pick`). A range slider keeps Left and Right for itself.
   - **OK / Enter** clicks the focused control. With no control focused during gameplay, Enter or Space advances and Left or PageUp rolls back (as today). Up or Down with nothing focused in gameplay focuses the HUD.
   - **Back** means Escape, Backspace, `keyCode` 4, 461 or 10009, and `key` `GoBack` or `BrowserBack`:
     - On the picker or a screen, it closes the topmost one.
     - From a focused HUD control, it returns focus to the stage.
     - In gameplay with nothing focused, it opens the new **pause menu** `#vno-pause-menu`: Resume, Save, Load, History, Preferences, Main menu. These reuse the quick-menu handlers.
     - On the main menu, the player does **not** handle Back, so the site bridge can leave the game.
   - **Android Chrome Back.** This Back is often a history navigation rather than a key event. Opening the picker, a screen or the pause menu calls `history.pushState({vno:1}, '')`, and `popstate` closes the topmost layer. Closing a layer some other way calls `history.back()` only for the state the player pushed itself.
   - **Focus on open.** Something is focused on load: the main menu's first button. The first control also gets focus each time a layer opens; for choices that is the first choice.
   - **Double OK.** An OK within 700 ms of an auto focus is ignored, so a held OK does not pick a choice (this repeats the bridge's grace).
   - **Focus ring.** Keyboard use adds `vno-kb` to `<html>`, and pointer or touch input removes it. The ring is drawn by `.vno-kb :focus` (Chrome 61 has no `:focus-visible`). It is a 4 px outline plus a glow.
4. **Touch (VN Studio).**
   - The stage stays 16:9 and scaled.
   - On a coarse pointer in portrait, a rotate hint `#vno-rotate-hint` shows over the letterbox. A tap dismisses it for the session.
   - On `pointer: coarse`, JS sets the CSS variable `--vno-hud-k = max(1, 48 / (baseHeight × stageScale))` from `handleResize`. Quick-menu buttons, the voice cluster, the chip, the picker items and the Preferences buttons are sized with `calc(... * var(--vno-hud-k))`, so each target is at least 44×44 CSS px on an 844×390 screen.
   - In VN mode, a tap anywhere on the stage advances. A tap inside a `button`, `input`, `.vno-slot-card`, the picker, a screen or an overlay does not (checked with `closest`).
   - The stage gets `touch-action: manipulation` and `-webkit-tap-highlight-color: transparent`.
   - Hover styles move under `@media (hover: hover)`, so a tapped button does not stay highlighted.
5. **Site bridge (creative-hub-web).** The bridge stands down for builds that carry the player flag (contract below). Old builds keep today's path.
6. **Rebuild and republish.** All 13 VN plays are rebuilt and published with the new player and bridge, then committed and pushed to `master`. GitHub Pages deploys them.
7. **Hub records.** Add a HUB-27 row to `ROADMAP.md`, write the run log `runs/hub-27-vn-tv-touch.md`, and add the VNO-62 row in VN Studio's `ROADMAP.md`.

## Out of scope (explicit)

- Edu Studio players and the 3 Edu plays in `public/play/`, plus the reader pages.
- Puzzle-overlay D-pad and touch work (drag widgets in `.vno-puzzle-container`). It is noted in VNO-62 "Later".
- A real portrait layout. Portrait shows only the rotate hint.
- Regenerating any art, voice, music or text. That rules out `generate`, `voice`, `run` and `asset regen`, and any Flow, ComfyUI, TTS or model call.
- The `fonts.ts` url root cause. The site's workaround stays.
- Swipe-to-rollback in VN mode.
- Starting Scriptorium or the VN Studio app, unless the CLI build fails. In that case, ask first.
- Unpublished projects (lighthouse, `hub-*`, test projects).

## Files and modules to touch

| Repo | File | Change |
|---|---|---|
| visual-novels-orchestrator | `src/engine/game/player-runtime.ts` | HTML (selects to buttons; `#vno-picker`, `#vno-voice-*`, `#vno-pause-menu`, `#vno-rotate-hint`), CSS (coarse sizes, focus ring, hover gating, no banned features), JS (picker, nav, Back, history, voice mute and stop, tap to advance, `loadSettings` default and clamp for `voiceMuted`, `data-vno-nav` flag) |
| visual-novels-orchestrator | `src/shared/ui-strings.ts` | New keys in `PLAYER_UI_KEYS` plus hr strings (e.g. `voiceStop`, `voiceMute`, `voiceUnmute`, `voicesPref`, `pauseResume`, `rotateHint`, `pickLanguage`) |
| visual-novels-orchestrator | `tests/renpy-template.test.ts` | Extend FakeElement (`focus`, `activeElement`, `closest`, `getBoundingClientRect` stub) only as far as the new tests need; move the existing `.change('hr')` chip tests to click then pick |
| visual-novels-orchestrator | `ROADMAP.md`, `.claude/tickets/VNO-62_tv-touch-controls/plan.md` (pointer to this plan) | Row and changelog |
| creative-hub-web | `src/bridge/hub-bridge.js` | Flag check, stand-down path |
| creative-hub-web | `tests/e2e/vn-player.spec.mjs` (new), `playwright.config.mjs` (projects `vn-tv` 1920×1080 and `vn-touch` 844×390 hasTouch/isMobile), `tests/e2e/helpers.mjs` (VN selectors) | Repro and acceptance |
| creative-hub-web | `public/play/<13 VN ids>/`, `content/publish-manifest.json` | Republished output |
| creative-hub-web | `.claude/tickets/WEB-02-vn-tv-touch/plan.md` (pointer), `README.md` (one line on the flag) | Notes |
| creative-hub | `ROADMAP.md` (HUB-27 row), `runs/hub-27-vn-tv-touch.md` | Records |

## Player and bridge key contract (T1 and T2 both implement this)

1. **Flag.** At start-up, before any key can arrive, the player sets `document.documentElement.setAttribute('data-vno-nav', '1')`. It also exposes `window.VNO_NAV = { version: 1, focusFirst: function () {...} }`, where `focusFirst` focuses the first control of the topmost layer and returns true or false.
2. **Player listens** on `document`, bubble phase. It calls `preventDefault()` and `stopPropagation()` on every key it handles. It leaves Back unhandled on the main menu, and ArrowUp unhandled when there is nothing above in the HUD.
3. **The bridge with the flag present** (`data-vno-nav="1"`):
   - It does no VN candidate navigation, no `cycleSelect`, no auto focus and no Enter grace handling for `vn`.
   - In capture phase, it handles only keys whose target is its own pill: Enter follows the link, Up is swallowed, and Down or Right blurs the pill, calls `VNO_NAV.focusFirst()` and swallows the key.
   - Back keys are **not** swallowed in capture. A bubble listener on `window` (which runs after the player's `document` listener) calls `back()` for a Back key only when `!e.defaultPrevented`. It does the same for ArrowUp: when the key was not prevented and focus is on body or html, it focuses the pill.
   - It drops its own `hubb-kb` marking for `vn` and keeps the pill show and hide.
4. **The bridge without the flag** (the old builds, and the Edu or read pages): today's behaviour, unchanged. After the rebuild no published VN lacks the flag, but this path stays so a play published later from an older build still works.
5. **Ids** stay as they are: the `vno-screen-*`, `#vno-ending-card`, `#vno-choice-overlay`, `#vno-stage-language` and `#vno-container` ids, and `</body>` in `index.html`.

## Tasks for workers

**T1: VN Studio player** (implementer; repo `visual-novels-orchestrator`, branch `VNO-62_tv-touch-controls` from `master` 61a4ba7; VNO-62 checked free).
- *Inputs:* Scope items 1-4, the contract, and research sections 1-3.
- *Outputs:*
  - The `player-runtime.ts` and `ui-strings.ts` changes, plus the tests named under Acceptance.
  - `yarn test`, `yarn typecheck` and `yarn lint` all green.
  - The ROADMAP VNO-62 row.
  - A local merge to `master` once tests pass, per the repo's habit (VNO-60).
- *Constraints:*
  - The generated JS must be valid chrome61 syntax after esbuild lowering. Runtime APIs it may rely on: `closest`, `scrollIntoView({block:'nearest'})`, CSS variables and `history.pushState`.
  - No banned CSS: `gap` without a fallback, `min()`, `clamp`, `aspect-ratio`, `inset`, `:is`, `:has`, `:focus-visible`-only rules, `backdrop-filter`. Check them against `creative-hub-web/scripts/check-site.mjs`.
  - The generated code is inside a template literal, so no backticks or `${`.
- *Contract:* T1 sets the flag and `VNO_NAV` and follows the listener rules above.

**T2: Site bridge and e2e** (implementer; repo `creative-hub-web`, branch `WEB-02_vn-tv-touch` from `master` 0406aaf). It can run in parallel with T1.
- *Inputs:* the contract, plus `hub-bridge.js:195-220, 290-495`.
- *Outputs:*
  - The bridge changes.
  - A new `tests/e2e/vn-player.spec.mjs` and the two Playwright projects.
  - A `README.md` line.
  - Existing `players`, `tv-nav` and `touch` specs still green on the old `dist/` before publish.
- *Unit tests:* `npm run test:unit` tests the publish scripts, not the bridge, so the bridge has no unit test. It is covered by e2e only.

**T3: Rebuild** (main session or a worker with shell; after T1 is merged). This follows the procedure below.
- *Outputs:* 13 fresh `game/` folders, and a table in the run log with slug, build messages, file count and size before and after.

**T4: Publish, verify, push** (after T2 and T3).
- *Steps:* site `npm run publish -- --force` (or `--only` per work), `build`, `check`, `test:unit`, `test:e2e`.
- *Commit:* public, content, bridge and specs go on `WEB-02_vn-tv-touch`. Merge that into `master` and `git push origin master` (pre-approved; no force push).
- *Watch:* the Pages Action, then load the live URL of one play.

**T5: Hub records** (main session). HUB-27 roadmap row, run log with every id, md5 of the new `player.js`, and the DONE / NOT DONE / UNTESTED list.

## Acceptance criteria and the test proving each

| # | Criterion | Proof |
|---|---|---|
| A1 | The player has no `<select>`. The chip and both Preferences rows open `#vno-picker`. Picking `hr` switches the story language, and picking a UI language switches the UI. | vitest: the generated `index.html` contains no `<select` (one assert). In the harness, a chip click shows the picker, and a click on item `hr` calls `switchLanguage` (rewrite of the chip test at `renpy-template.test.ts:348/538`). |
| A2 | Keyboard only (arrows, Enter, Escape, `GoBack`) at 1920×1080: the story language can be changed from the main menu and from in game, and the UI language from Preferences. Focus is visible at each step. | Playwright `vn-tv`, on clockless-god-3 (en,hr) in `dist/`. |
| A3 | Something is focused on load (main menu). A new layer focuses its first control. Back closes the picker or screen, opens the pause menu in game, and on the main menu leaves to `data-back`. | Playwright `vn-tv` |
| A4 | No double handling: Enter on a focused choice or menu button clicks once and does not also advance. The bridge stands down when the flag is present. | Playwright `vn-tv`: a counter on `click` plus the dialogue index unchanged. Also vitest: Enter on a focused HUD button does not call `onAdvanceClick`. |
| A5 | Stop ends the current line and un-ducks the music. Mute stops the line, skips later lines, survives a reload (`vno_settings.voiceMuted`) and restores the music volume. | vitest (FakeElement audio): one test for stop (paused, music back to full) and one for mute (no `src` set on the next beat; setting saved; `loadSettings` default is `false`). |
| A6 | Touch at 844×390 hasTouch: every HUD target (quick-menu buttons, chip, voice buttons) is at least 44×44 CSS px. A tap on the background advances, and a tap on a HUD button does not advance. | Playwright `vn-touch` |
| A7 | Portrait on a coarse pointer (390×844) shows `#vno-rotate-hint`. | Playwright `vn-touch` (one assert) |
| A8 | The site still passes: `check` (old-browser syntax, banned CSS, budget), `test:unit`, and the existing e2e specs. | `npm run check && npm run test:unit && npm run test:e2e` |
| A9 | The 13 rebuilt plays pass the publish smoke check and share one `player.js` md5. | `publish` output, plus `md5sum public/play/*/player.js` in the run log |

## Reproduction test (fails before the fix)

`tests/e2e/vn-player.spec.mjs`, test `language can be changed with remote keys only`:
1. Open `play/the-clockless-god-linear/` at 1920×1080 and press Enter (start).
2. Press only ArrowUp, ArrowRight and Enter until `#vno-stage-language` is focused, then press Enter.
3. Expect `#vno-picker` to be visible with `button` items. Press ArrowDown until the `hr` item is focused, then press Enter.
4. Expect the dialogue text to be the Croatian edition, and the language chip label to read `Hrvatski`.

- **Before** (run on today's `dist/`, before T4): it fails. During play the chip is not reachable (no player focus handling, and the bridge has no candidates in gameplay), and `#vno-picker` does not exist.
- **After:** it passes.
- **Record:** the failing run goes into the run log before the publish.
- The vitest no-`<select` assert also fails before the fix. A headless browser cannot show the native popup failure itself; see UNTESTED below.

## Rebuild and publish procedure

1. **Pre-checks.**
   - Run `scripts\hub.ps1 status`. VN Studio must not be running. If `~/VisualNovels/engine.lock` names a dead pid, or a pid that is not VN Studio, the lock is stale and the CLI replaces it. Record the pid.
   - Free disk space must be above 2 GB.
   - Node: put the fnm default alias dir on PATH (memory note); `fnm exec yarn` fails.
2. **Backup.** For each of the 13 slugs (research section 5), run:
   `robocopy C:\Users\Infplane\VisualNovels\projects\<slug>\game C:\projects\Personal\creative-hub\.claude\temp\hub-27-backup\<slug>\game /E`
   Then write `build.json`, the file count and the size into the run log. `.claude/temp` is git-ignored.
3. **Canary.** Rebuild `the-trap-room-at-the-lanterna` (the old variant B) first with `yarn engine -- build the-trap-room-at-the-lanterna` on branch VNO-62 or merged `master`.
   - Compare new against old: file count, size, `build.json` messages (no new placeholders or "edition X was made for pack" warnings), and images and voices still present.
   - Load the result with `node scripts/shot-game.mjs <slug>`.
   - If assets went missing, stop and report.
4. **The other 12.** Run them sequentially with the same check after each. Any failure: restore that slug (step 7) and continue. Mark it NOT DONE.
5. **Publish.** In `creative-hub-web` on `WEB-02_vn-tv-touch`, run the commands below. Exit 1 means a smoke check failed (that play is left out); stop. Exit 2 means over budget (about 175 MB headroom; player-only changes add kilobytes).
   `npm run publish -- --force` (or `--only <workId>` for each of the 13)
   `npm run build && npm run check && npm run test:unit && npm run test:e2e`
6. **Commit and push.**
   - Commit the work with a heredoc message ending with the attribution line.
   - Merge `WEB-02_vn-tv-touch` into `master` and run `git push origin master`.
   - Watch `.github/workflows/pages.yml`, then load the live play URL.
7. **Rollback.**
   - *A game:* `robocopy <backup>\<slug>\game <project>\game /MIR`.
   - *The site before the push:* `git checkout master -- public content` or drop the branch.
   - *The site after the push:* `git revert <merge>` and push. No force push.
   - *The player:* revert the VNO-62 merge locally.
   - Keep the backups until the user has played on the TV, then delete them only when the user says to.

## Stays UNTESTED (until the user tries it)

- The real Android / Google TV Chrome: remote key codes (OK, Back as a key versus history Back), the focus ring at TV distance, overscan near the top-right HUD and the bridge pill.
- Real phones and tablets: tap feel, the rotate hint and fullscreen.
- Voice mute and stop on the real device's audio, beyond the fake DOM and headless Chromium.
- Puzzle overlays with a remote or by touch (out of scope).
- Per the hub rule, the production is done only after the user has played a rebuilt story on the TV and on a touch device.

## Decisions for the parent or user

- Rebuild with the merged VNO-62 `master` (recommended; matches VNO-60's local merge) or straight from the branch.
- The pause menu is new UI. It is added because Back must open a menu that has Save, Load and Preferences. Replacing today's "Esc opens Preferences" with it is a behaviour change on desktop too.
