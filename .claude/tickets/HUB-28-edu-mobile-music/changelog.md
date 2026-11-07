# HUB-28 changelog

## 2026-11-07 - HUB-28 tasks A0-A4 and B: Edu player on phones and the in-game audio panel (EGS-62)

Scope of this entry: player code only (tasks C, D, E are other workers' and get their own entries).

- **edu-game-studio**, branch `EGS-62_mobile-music` (from `master` 46b6ec1), commit `8588112`, merged locally into `master` as `5b64706` (not pushed). Full per-file list: `edu-game-studio/.claude/tickets/EGS-62-mobile-music/changelog.md`.
  - Phone CSS (A1-A4): corner padding for the speaker button on the shared `.topbar`/`.hud`, `.enc-tabs`, `.rpg-hud` (<= 839 px); 14 px minimum for the 13 px labels A0 measured; 44 px source links in the encyclopedia. Only what A0 measured was changed; planned candidates A0 showed unnecessary (start screen, scroll strip, side columns, canvases, minimap, roleplay <=400 px block) were not built.
  - Audio (B): `musicVolume`/`sfxVolume`/`voiceVolume` settings (default 100, clamped, export/import), `volumeGain` curve, `GameAudio.voice`, speaker button `audio-settings` + modal `audio-panel` in both render paths, voice clips at the Voices level, role-play line ducks the music, i18n en/hr/de, Android back closes the panel.
- **creative-hub**: `runs/hub-28-edu-mobile-music.md` sections "Phone baseline (A0)" and "Player code (A, B)".

Deviations: role-play tests use `hr-a1-greetings`, detective tests borrow an audio asset (button only with sound); `bot-detective` first-run timeout 180 s; `docs/android.md` updated; EGS-62 pointer plan uses a relative path (public repo).

Verification: `yarn test` 521/521, `yarn typecheck` 0, `yarn lint` 0, `yarn test:e2e` 40/40 (16 files) on the branch; `out/player/player.js` built from master md5 `2f0a8e4822fc59c4ea04daa21c0f5f42`. A0: all 6 shells pass the bot at 375x667, 360x740, 1280x800 on 46b6ec1. Not run: real phones, real audio, TV; desktop screenshots that differ by bytes (quiz 2, roleplay 1, mindmaze 17) were not compared by eye.

Commit status: edu-game-studio committed and merged locally (not pushed); creative-hub records uncommitted.
