# Changelog

## 2026-11-22 HUB-43 hub tasks H1, H2 (creative-hub only)

Outcome: `hub.ps1 start` clears a stale or reused-pid engine lock; ROADMAP row 36 added. L1-L2, R1-R4, K1-K5 and the other repos' tickets are not part of this entry.

Branch `HUB-43_open-ideas` (creative-hub).
- `scripts/hub.ps1`: `Clear-StaleLock($s, [switch]$AtStart)`; at start it removes the lock when its pid is gone, or the process with that pid started more than 5 s after the lock's `startedAt`/`started` (ISO or epoch ms, compared in UTC); unreadable lock, or live pid with no timestamp: left with a message. `Start-Service1` calls it for managed services. Header line updated. `status` unchanged.
- `services.json`: `_about` sentence on start-time deletion.
- `ROADMAP.md`: row 36 (HUB-43), proxy repo row mentions AAP-48, AAP-49.

Verification: parse check 0 errors; services.json parses; dry runs on a copy with a fake registry: dead pid removed, live older pid left, live reused pid removed (ISO and epoch ms), unreadable left, no-timestamp left, after-stop removal unchanged, status read-only. Real lock files read only (no deletion). Not run: H1 with a real app (UNTESTED).

Commit status: committed on the branch, not merged or pushed.
