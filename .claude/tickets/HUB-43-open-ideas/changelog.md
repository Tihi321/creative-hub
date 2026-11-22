# Changelog

## 2026-11-22 HUB-43 hub tasks H1, H2 (creative-hub only)

Outcome: `hub.ps1 start` clears a stale or reused-pid engine lock; ROADMAP row 36 added. L1-L2, R1-R4, K1-K5 and the other repos' tickets are not part of this entry.

Branch `HUB-43_open-ideas` (creative-hub).
- `scripts/hub.ps1`: `Clear-StaleLock($s, [switch]$AtStart)`; at start it removes the lock when its pid is gone, or the process with that pid started more than 5 s after the lock's `startedAt`/`started` (ISO or epoch ms, compared in UTC); unreadable lock, or live pid with no timestamp: left with a message. `Start-Service1` calls it for managed services. Header line updated. `status` unchanged.
- `services.json`: `_about` sentence on start-time deletion.
- `ROADMAP.md`: row 36 (HUB-43), proxy repo row mentions AAP-48, AAP-49.

Verification: parse check 0 errors; services.json parses; dry runs on a copy with a fake registry: dead pid removed, live older pid left, live reused pid removed (ISO and epoch ms), unreadable left, no-timestamp left, after-stop removal unchanged, status read-only. Real lock files read only (no deletion). Not run: H1 with a real app (UNTESTED).

Commit status: committed on the branch, not merged or pushed.

## Polish 1 (checker notes N5, N6, N7, N4)

- N5: at start, the pid-reuse branch of `Clear-StaleLock` removes a lock only when its time is unambiguous: a DateTime of Kind Utc or Local, a string with `Z` or an explicit offset, or epoch milliseconds. A string without a zone, or a DateTime of Kind Unspecified, is unknown: the lock is left with the "held by running pid ..., left" message. The dead-pid branch is unchanged.
- N6: the function never ends `hub.ps1 start` with an error. A pid outside the int32 range prints the "unreadable, left" message; a `Remove-Item` that fails prints "lock <path> could not be removed: <message>, left"; in both cases the function returns and the start goes on.
- N7: comment above the 5-second tolerance (an app writes its lock a few seconds after its process starts; measured 2.9 s for VN Studio on 2026-11-22).
- Deviation from the plan text, not written down earlier (N4): the plan's literal `[datetime]::Parse($stamp ...)` would have read the real VN lock one hour off on pwsh 7.6, because `ConvertFrom-Json` already returns a DateTime, and would have removed a live app's lock. The built code handles DateTime, zoned-string and epoch-ms stamps instead.
- Verification: dry runs on a copy with a fake registry (dead pid removed; live pid with old Z stamp removed; zoneless stamp left; future Z stamp left; epoch ms in the past removed; no stamp left; unreadable left; pid 99999999999 left; a lock without delete sharing: "could not be removed, left" and the start went on; after-stop removal unchanged; status leaves the file). The real VN lock decides "left" (read only).

## Polish 2 (delta re-check)

- A lock time counts as known only inside 2001-01-01 (floor: epoch ms 978307200000) and 2100-01-01 (4102444800000), for epoch numbers and for DateTime or string stamps alike. Outside the range it is unknown, `$t` stays `$null`, the lock is left. An epoch-seconds stamp (read as 1970) no longer makes a live app look "started after the lock".
- A lock pid of zero or below is unreadable: "unreadable, left", not a dead pid.
- Verification: parse check 0 errors. Dry runs on a copy with a fake registry and a long-lived node pid: epoch seconds 1795000000 left; epoch ms 1767225600000 removed (pid reuse); `1969-12-31T23:00:00Z` left; `2026-01-01T00:00:00Z` removed; zoneless left; `2200-01-01T00:00:00Z` left; pid -5 and 0 "unreadable, left"; dead pid removed; after-stop removal unchanged. Real VN lock re-computed read only: left (process began 2.9 s before the lock time). Not run: a real app (UNTESTED).
