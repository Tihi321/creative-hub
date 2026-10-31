# HUB-19 changelog

## 2026-10-31: resumed run (verify, integrate, later features)

Work was in the Edu Studio repo (`C:\projects\Personal\edu-game-studio` and its worktrees); the hub was not changed except this ticket folder (`handoff.md` refreshed, `wiring/` drafts, this file). Details, SHAs and the DONE / NOT DONE / UNTESTED list are in `handoff.md`.

- Phase 5 (EGS-10..14) verified on `EGS-14_detective`: typecheck, lint, 1154 tests, builds, the bot on every shell.
- The two lines of work became one: EGS-06..08 and EGS-15..17 rebased onto EGS-14; integration ticket EGS-22 (`a4333ca`).
- Later features, each its own branch stacked in this order: EGS-18 speaking practice (`876c274`), EGS-20 classroom mode (`14fe905`), EGS-21 live quiz (`09a3788`), EGS-19 Android (`9650227`), then a docs commit (`c4c5294`).
- Final tip checked: typecheck, lint, builds, 1660 tests (two load timeouts in the whole-suite run, passing alone).
- Hub wiring prepared, not applied (`wiring/wiring.md`).
- Stopped before the pilot (the user must play it).
