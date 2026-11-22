# HUB-44 changelog

## 2026-11-22 HUB-44 hub tasks H1-H4 (creative-hub only)

Outcome: `scripts/hub.ps1` refuses Windows PowerShell 5.1, says why a running pid's lock was left, and `start` prints the port owner's pid; ROADMAP row 37 added. The live round (P0, R, L, K, B1, End) and the other repos' tickets are not part of this entry.

### creative-hub, branch `HUB-44_pending-ideas`
- `scripts/hub.ps1`
  - H1: `#Requires -Version 7.0` before `param(`; header line says it needs pwsh 7.
  - H2: in `Clear-StaleLock -AtStart`, `$why` is set for a missing time, a zoneless datetime or string, an unreadable time, and a time outside 2001-2100; the "held by running pid ..., left" line appends ": <why>, so pid reuse cannot be told". A zoned time before the process start is removed as before; a zoned time after it is left with no reason, as before.
  - H3: `start` prints "started (launcher pid N)" and, on success, "up at <url> (pid M)" with M from `Get-Owner` (the same pid `status` shows).
- `ROADMAP.md`: row 37 (HUB-44, Planned); the ACP proxy repo row gains "; AAP-51 for HUB-44".
- Ticket files: `plan.md` (status in-progress), `events.jsonl`, this `changelog.md`.

### Deviations
- `#Requires` sits directly above `param(` (after the existing blank line), not on the blank line itself; same effect.
- For a datetime, the zoneless message prints the time with `ToString('s')` (so "2026-01-01T00:00:00"), the string form for strings.
- Extra dry-run cases beyond the plan: (e) no time, (g) epoch 12345, (h) garbage string.

### Verification (all PASS)
- H-1: `powershell.exe -NoProfile -File scripts\hub.ps1 status` printed `cannot be run because it contained a "#requires" statement for Windows PowerShell 7.0 ...` (ScriptRequiresUnmatchedPSVersion), exit 1, ran nothing. `pwsh -NoProfile -File scripts\hub.ps1 status` ran as before (read-only), exit 0. Parse check: 0 errors.
- H-2, dry run on a temp copy with a fake node server on port 65014 (cleaned up):
  - (a) dead pid: `fake: removed its stale lock (pid 999999)`
  - (b) zoned 2020 time: `fake: removed its stale lock (pid 15588 is now node, started after the lock)`
  - (c) zoned 2099 time: `... held by running pid 15588 (node), left` (no reason), file kept
  - (d) no zone: `... held by running pid 15588 (node), left: its time 2026-01-01T00:00:00 has no zone, so pid reuse cannot be told`, file kept
  - (e) no time: `... left: it has no time, so pid reuse cannot be told`
  - (g) `12345`: `... left: its time 12345 is outside 2001-2100, so pid reuse cannot be told`
  - (h) `yesterday`: `... left: its time yesterday has no zone, so pid reuse cannot be told`
- H-3: `fake: started (launcher pid 10368)` then `fake: up at http://127.0.0.1:65014/ (pid 30100)`; the temp copy's `status` showed Pid 30100 for fake.
- H-4: `git diff --stat`: ROADMAP.md and scripts/hub.ps1 only; CRLF line endings preserved (crlf count equals lf count in both).
- Cleanup: temp folder `.claude/temp/hub44` deleted, port 65014 free, background node stopped. 8787, 7459, 8188, 8080 still listening; 8787/8080/8188 health answered 200.

Not run (by plan): the whole live round; R1's start against `status` for H-3 on the real proxy. The real `hub.ps1` was only run with `status`.

### Follow-ups
- None added.

Commit status: committed on `HUB-44_pending-ideas` (not pushed, not merged).
