# HUB-27 research: VN web player on TV and touch, then rebuild and republish

## Question
Why do the language dropdowns of the exported HTML5 VN player not open on a smart-TV browser, how are voice and touch handled today, and what does a plan need to fix them (language pick, a voice mute/stop button, better touch UX), rebuild every published VN and republish the site?

## Answer
- The player has exactly three native `<select>` elements: Interface Language and Story Language in Preferences, and the stage language chip `#vno-stage-language` (top right, shown only when the book has 2+ languages). All are plain `<select>`s inside a 1920x1080 stage that is scaled with a CSS transform. (confirmed, below)
- No player code handles TV remote keys. Nothing is focused on load. The language chip is not reachable by D-pad during play. Whether the popup fails because of the TV engine, the transform or the key handling is **inferred**, not reproduced (no TV here). Cleanest fix: replace the selects by a button list (an in-page picker), not a native popup.
- Voice: one `<audio id="vno-audio-voice">`, volume slider only (`volVoice`, default 90). No mute, no stop button, no "voice off" setting. Settings persist in `localStorage["vno_settings"]`.
- Touch: tap advances only on the dialogue box (278 px of 1080). The quick menu is 18 px text on the 1920 stage, so a phone shrinks it to a few px. No `pointer: coarse` handling, hover-only highlights, no menu without Escape.
- Rebuild: `yarn engine -- build <slug>` (CLI, no MCP needed) is a pure local rewrite from stored assets. No ComfyUI, TTS or model call. It deletes and rewrites the whole `game/` folder.
- 13 VN/picture-book plays are published, 4 player variants exist. A rebuild with the new player makes them all one version. The site copies the player files as-is (JS lowered to chrome61, bridge script injected).
- Next free VNO number: VNO-62 (last used VNO-61; master clean, no VNO-62 branch or ROADMAP line). Default branch `master`.

## Path through the code

All player code is one file: `C:/projects/Personal/visual-novels-orchestrator/src/engine/game/player-runtime.ts` (3378 lines). `generateIndexHtml` (line 10), `generatePlayerCss` (302), `generatePlayerJs` (1307, a template literal: no backticks or `${` in the generated code), `writePlayerBundle` (3296). Constraint from the VNO-48 plan: every `ui('...')` key must be in `PLAYER_UI_KEYS` (`src/shared/ui-strings.ts`), enforced by tests.

### 1. Language pickers (confirmed)
| Picker | HTML | Populate | Change handler |
|---|---|---|---|
| Stage chip (title screen, in game, every screen; z-index 200) | `player-runtime.ts:280-283` (`#vno-lang-bar`, `<select id="vno-stage-language" class="vno-lang-select">`) | `populateLanguageSelect` 1473-1483 (option text `nativeName (name)`) | `bindUiEvents` 1932-1934 -> `switchLanguage` |
| Story Language (Preferences) | 207-210 `#vno-pref-language` `.vno-select` | same function | 1935-1937 -> `switchLanguage` |
| Interface Language (Preferences; hidden if no `uiLanguages`) | 201-204 `#vno-pref-ui-language` | `populateUiLanguageSelect` 1494-1514 | 1973-1975 -> `switchUiLanguage` |

- Chip is hidden when the book has fewer than 2 languages (`updateLangBarVisibility` 1528-1533; `returnToMainMenu` repeats it). Single-language VNs (en only: most of the published ones) show no chip. Published books with 2 languages: clockless-god-3 (en,hr), snail, bell, soother. Preferences still has the Interface Language row (about 36 menu languages) in every build that ships `uiLanguages`.
- Chip CSS: `.vno-lang-bar` 1072-1086, `.vno-lang-select` 1100-1111 (transparent, `font-size: 20px`, `outline: none`, `option` styled 1118). `.vno-select` 922-949 uses `appearance: none` plus a data-URI chevron.
- Event swallowing: `bindUiEvents` 1925-1930 stops propagation of `click, mousedown, mouseup, touchstart, keydown` on the chip, so no player handler sees keys from it. The window keydown handler (2056-2108) also returns early when the target is a SELECT or INPUT (2066), so the player never handles keys from selects, and nothing helps the TV browser open the popup.
- No `.focus()` is called anywhere on load or on screen open (no D-pad support; WEB-01 audit sections 1.2-1.3). The only keys: Space/Enter advance, PageUp/ArrowLeft roll back, Esc toggles Preferences (the only way into Preferences in game besides the mouse-only quick menu), F/F11 fullscreen.
- Why it fails on TV (**inferred**, not reproduced): (a) smart-TV browsers (webOS, Tizen, Android TV WebView) often do not open a native select popup for a focus plus OK press, or open it off-screen/wrong size when the select sits inside a `transform: scale()` stage (`handleResize` 1450-1459 sets `translate(-50%,-50%) scale(min(w/1920, h/1080))`); (b) the chip is not in the hub bridge's candidate list during play, only on the main menu; (c) the hub bridge works around it for screens by turning Enter on a focused select into "next option" (`creative-hub-web/src/bridge/hub-bridge.js:320-330`, called at 458), which is a site-only hack, not a dropdown; (d) the stage language bar sits where the hub's "Library" pill and the top-right chrome appear (z-index 200), possibly overlapping on TV overscan (not checked).
- Other selects: none. Edu player is separate (not in scope).

### 2. Voice (confirmed)
- Element: `<audio id="vno-audio-voice" preload="auto">` (`player-runtime.ts:286-290`), plain HTMLAudioElement, no WebAudio. `dom.audioVoice` cached at 1443.
- VN lines: `playVoiceForBeat(beatId)` 2710-2725 (called from the beat handler at 2316): sets `src`, `play()`, rejected play un-ducks. `stopVoice()` 2727-2735 pauses, clears `onended`, empties page chain. Called when advancing/rolling back/loading (2144, 2288, 3146, 3183).
- Picture book: `playPageVoice` chain, `playNextPageVoiceClip` 3187-3207, replay button `#vno-page-replay` (`vno-hidden` until a page has voice), `replayPageVoice` 3209.
- Ducking: `voiceActive` flag + `setVoiceActive` 1910-1914, `applyAudioVolumes` 1915-1922 (music x0.35, ambience x0.7 while voice plays). A mute must call `setVoiceActive(false)` or it leaves the music ducked.
- Settings: object at 1339-1348, `volVoice` 90, slider `#vno-pref-vol-voice` (bound 1984), `loadSettings` 3220-3246 (clamps each key, unknown stored keys are kept: `Object.keys(stored).forEach`), `saveSettings` 3248-3250 -> `localStorage.vno_settings` (shared by every VN on the same origin, so a mute carries over between games on the site; recorded earlier as acceptable). `settings.schema` is 2; a new key such as `voiceMuted` needs a default and clamp in `loadSettings`, no schema bump needed (migration only fires when schema is missing).
- No mute/stop UI exists. Candidate places: the quick menu (`#vno-quick-menu`, HTML 140-ish; buttons `vno-qm-*`, listeners 1959-1965, CSS 556-585) for VN; picture-book footer next to `#vno-page-replay` (HTML ~118, listener 1991) and `.vno-page-menu`. The scene needs a button that is always visible and large (not in the 18 px quick menu). New label keys need `PLAYER_UI_KEYS` entries and Croatian strings (`src/shared/ui-strings.ts`).

### 3. Touch and pointer (confirmed unless marked)
- Stage is a fixed 1920x1080 box, scaled to fit (1450-1459). Everything scales with the viewport: on a 390 px portrait phone the scale is about 0.2, so the 18 px quick-menu buttons (`.vno-qm-btn` 575-585, padding 4px 8px) are about 4 px; on a 1280x800 tablet about 12 px (hit area about 30x20). Viewport meta disables zoom (line 20). No `@media (pointer: coarse)`, no portrait layout; the only media queries are `max-width: 900px` for the prefs rows (956) and `prefers-reduced-motion` (1295).
- Tap to advance: only `dom.textboxContainer` click -> `onAdvanceClick` (1939). The container is `bottom: 20px; height: 278px` (455-463). Tapping the art/background does nothing. In picture-book mode tapping image or caption turns the page (1987-1988) and horizontal swipe (40 px) turns pages (1994-2008, `touchstart/touchend`, no `touch-action`). VN mode has no swipe.
- Hover-only: `.vno-qm-btn:hover`, `.vno-choice-btn:hover` (610-613, scale 1.02), `.vno-menu-btn:hover`, `.vno-slot-card:hover`, `.vno-page-nav:hover` are visual only. The functional UI is not hover-gated. On touch, `:hover` sticks after a tap (cosmetic).
- Menu without Escape: quick menu buttons give Prefs, Save, History, Menu on touch. Picture book has `Menu`. Fine for touch if the buttons were bigger; for a remote there is no path (WEB-01 audit 1.3).
- Everything has `user-select: none` (`* {}` rule at 307-311): includes `select`/inputs, harmless.
- Fullscreen toggle exists only in Preferences and by F key.
- Puzzle overlay is a fixed 1700x960 box (`.vno-puzzle-container` 970-ish); drag/pointer widgets in puzzle handlers (not read in detail; **inferred** pointer-only per WEB-01 audit).
- Slider/range inputs in Preferences are default browser controls, small on TV and phone.

### 4. Existing player tests (confirmed; ran 3 files: 35 passed in 2.5 s)
- Framework: vitest 5 (`vitest.config.ts`, `tests/**/*.test.ts`, node environment). The player is executed in Node through a hand-written fake DOM harness in `tests/renpy-template.test.ts` (class `FakeElement` at line 75; elements by id; `h.getById('vno-stage-language').change('hr')`, 27 tests: language chip 348/538/1058, voice + ducking 1033/1228, keys). Also `tests/player-theme-css.test.ts` (6), `tests/player-ui-language-data.test.ts` (3). Typecheck `yarn typecheck`, lint `yarn lint`, full suite `yarn test`.
- Run (Windows, fnm): put the fnm default node dir on PATH, then `node node_modules/vitest/vitest.mjs run tests/renpy-template.test.ts ...` (this is what I ran; `fnm exec yarn` fails per memory note, use the fnm default alias dir on PATH). Browser behaviour is not covered by unit tests; `scripts/shot-game.mjs` exists for screenshots. The site repo has Playwright specs `tests/e2e/{tv-nav,touch,players,desktop,screens}.spec.mjs` (touch at 768x1024 and 1024x768, `hasTouch`) that run over `dist/`.

### 5. Rebuilding every VN (confirmed)
- CLI: `yarn engine -- build <slug>` (`src/engine/vncli.ts:382-392`, usage line `build <slug>`). `yarn engine` is `yarn build:engine && node out/engine/index.js`. It starts the headless engine (same code as the app), enqueues `TASKS.build` and waits. `acquireEngineLock` (`src/engine/store/lock.ts`) relays to a running owner; `~/VisualNovels/engine.lock` currently names pid 25812, mcpUrl `http://127.0.0.1:7459/mcp`, started 2026-11-04. Port 7459 is down per the brief, so the lock is probably stale (stale locks are replaced, lock.ts:8); not verified. Alternative: `scripts\hub.ps1 start vn-studio`, then `hub.ps1 call vn-studio <tool>`; there is an MCP build tool too (not looked up; the CLI is enough).
- What a build does (`src/engine/vn/handlers.ts:768-806` -> `src/engine/game/build.ts:98-`): `fs.rmSync(<project>/game)` then rewrites it: theme, fonts, copies existing music/sfx/voice/image files via `resolveAsset` (`fs.existsSync` guarded; missing assets become placeholders/warnings, never generated), writes `game-data.json/.js`, `player.css/js`, `index.html`. The handler is registered `{ noModel: true }` (no model, ComfyUI, TTS or Flow call). It also writes `build.json` and generates Ren'Py `tl` files (`generateTranslations`, build.ts:298; local text work). **No spend.** Do not run `generate`, `voice`, `run`, or `asset regen`.
- A separate "player only" refresh does not exist. `writePlayerBundle(outputDir, gameData, themeCss)` (3296) could be wrapped to rewrite only player.js/css/index.html from an existing `game-data.json` (option B), but the build is simpler and reproduces everything from the project.
- Cautions (**inferred**): a rebuild re-resolves assets and editions, so any asset or text change made since the last build (or a stale edition: the build reports `edition X was made for pack...`) goes into the new game; compare `build.json` messages and the old `game` folder size before replacing. The old `game/` is deleted at the start of the build. Back it up under `.claude/temp/` first (cheap for most; the folders are 20-80 MB; check size).
- Published VN plays and sources (from `creative-hub-web/content/catalog.json`; all under `C:/Users/Infplane/VisualNovels/projects/<slug>/game/game`, player md5 in brackets):
  | Play id | Slug | Type | Langs | Player variant |
  |---|---|---|---|---|
  | the-clockless-god-choices | the-clockless-god-2 | choice-game | en | A accc8c79 (1977 lines) |
  | the-clockless-god-linear | the-clockless-god-3 | visual-novel | en,hr | C cb23db85 (1248) |
  | the-snail-and-the-salad-picture-book | the-snail-and-the-salad | picture-book | en,hr (de in project) | A |
  | the-bell-and-the-bicycle-picture-book | the-bell-and-the-bicycle | picture-book | en,hr | A |
  | the-soother-that-fell-into-dragon-land-choices | the-soother-that-fell-into-dragon-land | choice-game | en,hr | D fa23d4b1 (1283) |
  | the-trap-room-at-the-lanterna-vn | the-trap-room-at-the-lanterna | visual-novel | en | B 2a37464d (1208) |
  | the-winter-garden-clock-vn | the-winter-garden-clock | visual-novel (puzzles) | en | A |
  | the-local-patch-vn | the-local-patch-2 | visual-novel | en | A |
  | circuit-breaker-vn | circuit-breaker-2 | visual-novel | en | A |
  | echoes-in-the-deep-vn | echoes-in-the-deep-2 | visual-novel | en | A |
  | the-salt-line-vn | the-salt-line-2 | visual-novel | en | A |
  | the-silent-signal-vn | the-silent-signal-2 | visual-novel | en | A |
  | the-silent-summit-vn | the-silent-summit-2 | visual-novel | en | A |
  That is 13 plays (11 VN/choice builds + 2 picture books). `public/play/` also holds 3 Edu plays (not VN Studio, no change). `the-lighthouse-that-kept-lists-vn` is a project but is no longer published (WEB-01 dropped it, commit 96e1ad1). Other projects in `~/VisualNovels/projects` (hub-*, quarter-tone-test, vno-media-test) are test projects, not published.

### 6. Player versions (confirmed)
- Four variants of `player.js` among the published builds (table above; md5 and line counts measured now with `md5sum`/`wc`). Variant A equals the current generator (the 1977-line `generatePlayerJs` body, 1307-3288). B, C, D (trap room, clockless-god-3, soother) lack picture-book mode, "Esc closes a screen", `:focus-visible` rules and the UI-language select. A rebuild of all 13 gives one version.
- The site (`creative-hub-web/scripts/publish.mjs`, `scripts/lib/encode.mjs`) copies the VN `game/game/` folder as the play root as-is: skips `*.rpy`, `*.rpyc`, `tl/`, `cache/`, `saves/`; re-encodes images/audio at the same format (MP3 96 kb/s); lowers `.js` with esbuild to `chrome61` (so use no syntax newer than that; runtime APIs are not polyfilled); rewrites `fonts.css` urls (the "fonts.css path bug", encode.mjs:77-87, a site-side workaround; the root cause in VN Studio `src/engine/game/fonts.ts` is a ROADMAP candidate); injects `<script src="<up>assets/hub-bridge.js" data-player="vn" data-back=...>` before `</body>` of the play's `index.html`. A new `index.html` must keep `</body>` and `#vno-container`, and the ids that `hub-bridge.js` uses (`VN_SELECTOR = 'button, select, input, .vno-slot-card'`, containers `#vno-screen-main-menu`, `#vno-ending-card`, `#vno-choice-overlay`, `#vno-screen-prefs|save|history|about`). The bridge `cycleSelect` hack stays harmless if selects are removed, but its tests (`tests/e2e/players.spec.mjs`, `tv-nav.spec.mjs`) may reference them.
- Local storage on the site: `vno_settings` shared across all VN games (same origin); saves per game under `saveDir`.

### 7. Publish steps for creative-hub-web (confirmed from README and workflow; not run)
1. Node 24 (`.nvmrc`), `npm ci` done (node_modules present), `npx playwright install chromium` (smoke check), ffmpeg on PATH. `content/sources.local.json` already exists with `vn: C:/Users/Infplane/VisualNovels/projects`.
2. `npm run publish` (flags `--only <workId>`, `--force`, `--dry-run`, `--skip-smoke`). Cached by source change; a rebuilt game changes hashes so it rewrites those plays. Use `--only <workId>` or `--force`. Smoke check in headless Chromium: assets resolve, no page errors, else exit 1 and the play is left out. Exit 2 if over budget.
3. Budget: `site.budgetMB` 600 MiB in `content/catalog.json` (public/ plus 5 MiB site); any file over 95 MB fails. Now `public/` is 423 MB, `dist/` 424 MB, so about 175 MB headroom. A rebuild should not change asset sizes; new player files add only KB.
4. `npm run build` (renders `dist/`), `npm run check` (links, game asset references, old-browser syntax, banned CSS features, size budget), `npm run test:unit`, optional `npm run test:e2e` (Playwright over `dist/`; includes `touch` and `tv-nav` specs).
5. `git add public content && git commit`, `git push origin master`. The GitHub Action `.github/workflows/pages.yml` (push to master or manual dispatch) runs `npm ci`, `test:unit`, `build`, `check` and deploys `dist` to Pages; it never publishes (`public/` is committed). Site URL `https://tihi321.github.io/creative-hub-web/`. The repo is clean on `master`. Per hub rules, the change in VN Studio goes on a VNO-62 branch in its own repo; the site gets its own branch (WEB-style) and commit.
6. Node is not on PATH in Bash here; use the fnm default dir on PATH (done in this research for `node -v` = 24.14.0).

## Reproduction
Not reproduced. No TV browser or emulator was run; the TV failure cause is inferred from the code (no remote-key support, native selects inside a transformed stage). The site's Playwright specs only simulate keys and touch on Chromium and do not show native popups (headless Chromium does not render select popups). Smallest check for a plan: a real TV or a Chrome 60-80 build; the old-TV class is the target (publish lowers JS to chrome61).

## What the plan needs
- VN Studio, branch `VNO-62_tv-touch-player` (suggested; style `VNO-NN_short-name`), file `src/engine/game/player-runtime.ts` (single owner), `src/shared/ui-strings.ts` (`PLAYER_UI_KEYS` + hr strings), tests in `tests/renpy-template.test.ts` (FakeElement harness; extend it for new elements) and `tests/player-theme-css.test.ts`; ROADMAP.md line. Run `yarn test`, `yarn typecheck`, `yarn lint`.
- Options for the language picker (plan must choose one):
  A. Replace all three `<select>`s by an in-page picker: a button that opens a list of `<button>`s (focusable, large, closes on Esc/Back), used by chip and Preferences. Same `change` semantic via `switchLanguage` / `switchUiLanguage`. Works on every TV and with touch. Recommended.
  B. Keep selects, add a cycle button (click = next language). Smallest, but poor with 36 UI languages.
  C. Only fix keys (focus plus Enter cycles). Leaves the TV popup problem.
- D-pad/focus in the player itself (VNO row proposed by WEB-01 audit section 7): focus the first button when a screen/menu/choice list opens, arrow keys move between buttons, Enter activates, visible focus ring, Enter and ArrowLeft must not reach `onAdvanceClick`/`rollback` while a screen or choice list is open. Then the site's injected bridge should stand down or stay compatible (decision in the site ticket). In-game menu without Escape: a key or an on-screen button that focuses the quick menu.
- Voice button: persistent, large, in every scene (VN and picture book), tri-state is enough: mute (voice off, saved as `voiceMuted`) and stop-current. Stop must call `stopVoice()`; mute must also skip `playVoiceForBeat`/`playNextPageVoiceClip` and un-duck music. Persist in `vno_settings`; show state (icon plus `aria-pressed`). Preferences gets a matching row. Label strings in `PLAYER_UI_KEYS` + hr.
- Touch: tap anywhere on the stage (not on buttons) advances in VN mode; min target size about 48 CSS px after scaling (compute from stage scale, or enlarge in CSS under `@media (pointer: coarse)`/small viewport); larger quick menu and prefs controls; portrait handling (stage letterbox is tiny: consider a rotate hint or a portrait layout); swipe for rollback in VN; `touch-action` and tap-highlight settings; no hover-only dependence; fullscreen button.
- Old-TV CSS fallbacks (from the audit): flex `gap` (about 14 rules), `min()`, `:focus-visible` need non-gap/`:focus` fallbacks; no JS newer than chrome61 syntax (site lowers syntax only). New CSS must not use `aspect-ratio`, `inset`, `clamp`, `:is`, `:has`, `backdrop-filter`; `check-site.mjs` bans features (see its list).
- Rebuild: back up each `game/` first; `yarn engine -- build <slug>` x13 (sequential, one engine); check each `build.json` for placeholders/warnings; do not run generate/voice/run. Then `npm run publish` in the site repo with `--only` per affected work (or `--force`), build, check, e2e, commit, push, and watch the Action. Verify the live URL.
- Verification that remains for the user: play on the real TV and a phone/tablet; a production is done only when the user has played it (hub CLAUDE.md).

## Risks
- Fix cannot be proven without a real TV; headless Chromium does not show a select popup, so the old behaviour is not reproducible there. State UNTESTED on the TV until the user tries it.
- Rebuilding changes content as well as the player: any asset/edition/pack change since the last build lands in the published games (stale-edition and placeholder messages). Compare before and after (`build.json`, file counts, sizes). The three older-variant projects (trap room, clockless-god-3, soother) were built on 2026-10-24/25; their project data may have older formats (**inferred**, not tried).
- `fs.rmSync(game)` at build start: a failed build leaves no game folder; keep the backup until the site publish smoke check passes.
- Possible stale `engine.lock`/port 7459 conflict; starting the app via `hub.ps1 start vn-studio` while the CLI runs could double-own the data folder (the lock makes the second one relay).
- Shared state: `vno_settings` is shared by all VNs on the origin, so a new `voiceMuted` default carries across games; the schema migration is keyed on a missing `schema`, so old stored values need explicit defaults in `loadSettings`.
- Bridge interplay: the site's `hub-bridge.js` captures keydown on `window` while menus are open and relies on specific ids/selectors. Changing ids or adding a built-in D-pad could double-handle keys (Enter clicking twice). Needs a joint decision and a bridge update in the site repo (own branch).
- Site budget headroom is about 175 MB (423/600 MiB); fine for player-only changes, but a full `--force` re-encode of audio is slow (ffmpeg).
- The GitHub Action runs `test:unit` and `check` only; e2e (touch/tv-nav) runs locally, so run them before the push.
- The `tests/renpy-template.test.ts` harness is a fake DOM: it can pass while real browsers fail (focus, layout, transform). Plan needs at least one Playwright pass at TV (1920x1080, keys only) and touch (hasTouch) on a rebuilt game before publishing.
- The fonts.css url problem is patched in the site's copy only; a rebuild reproduces it in the VN output (still fixed by the site). Fixing it in `fonts.ts` is separate scope.

## Open questions
1. Which TV (brand, browser engine and version) does the user use? Determines the minimum JS/CSS target and whether the popup fails because of the engine or the transform.
2. Voice button behaviour wanted: mute-all-voice toggle, stop-current-line, or both? Persisted across scenes and games (current thinking: yes)?
3. Should the in-player D-pad support land in VNO-62 too (it is the same root cause family), or only the language picker plus voice button plus touch?
4. Is `engine.lock` pid 25812 really stale, and is the CLI path (`yarn engine -- build`) preferred over starting VN Studio with `hub.ps1 start vn-studio` (user said starting VN Studio is fine)?
5. Should the older unpublished-variant projects be rebuilt only if their stored project data is current? Check one (trap room) first as a canary.
6. Does the user want the 3 other `public/play/` Edu games touched? Assumed no.
7. Phones in portrait: accept letterbox plus rotate hint, or build a real portrait layout (bigger scope)?
