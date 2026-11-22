# HUB-42 changelog

## 2026-11-22 hub tasks H1-H4 (creative-hub only)

Outcome: the hub half of HUB-42 is built; live steps L1-L5 and live checks K1-K4 were not run.

Branch `HUB-42_pending-ideas-and-proxy-monitor` (from master 457b735).

- `.claude/tickets/HUB-38-acp-for-all/changelog.md` (H1): records REQ-0030 piece 31's checks and the UNTESTED line now names piece 31.
- `scripts/hub.ps1` (H2): new `Clear-StaleLock`, called after `stopped` in `Stop-Service1`; deletes only `<data>\<lock>` when its pid is gone; header line 13 extended.
- `services.json` (H2): `lock` on scriptorium, vn-studio, edu-studio, cartoon-studio, pixel-studio; `_about` extended.
- `ROADMAP.md` (H3): row 35 (HUB-42, Planned) and the ACP proxy repo row (AAP-44..47).
- `README.md` (H4): `acp-proxy` row mentions the Monitor and About page (AAP-47); correct only after AAP-47 merges.

Deviations: dry run fake service path uses `/data` (forward slash) in its fake services.json (a first attempt with a lost separator only proved the "path does not exist: do nothing" case).

Verification: PowerShell parse check 0 errors; `services.json` JSON.parse OK; dry run with a fake service on 65013 on a copy of the script (reads its own sibling services.json): dead pid -> lock removed; live pid -> lock left; `hub.ps1 status` only on the real script.
Not run: L1-L5, K1-K4, a real `hub.ps1 stop` of an app.

Commit status: committed on the branch (not merged, not pushed).
