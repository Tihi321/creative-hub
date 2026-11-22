# Changelog HUB-40

## 2026-11-22 - HUB-40, hub tasks H1-H4 (L1-L2, N1-N4 and the eight repo tickets are not part of this entry)

Outcome: `hub.ps1 start` stops at a `requires` cycle, `-Window` applies only to named services, a service without `start` is reported, LM Studio has no start command, HUB-38 has a changelog, ROADMAP row 33 exists.

creative-hub, branch `HUB-40_extra-ideas` (from master):
- `scripts/hub.ps1`: `Start-Service1($s, $Chain, $Named)` with a cycle guard (prints `requires cycle a -> b -> a, skipped`), required services started with `Named = $false` so `-Window` affects only the named ones, "no start command in services.json; start it yourself" and return when a service has no `start`, `startWhenSilent` comment reworded, header line 12 notes the `-Window` scope (H1).
- `services.json`: `lmstudio` lost `startWhenSilent` and `start` (H2).
- `README.md`: `lmstudio` row start cell is "none (not installed)"; the `no-http` comment line reworded (H2).
- `.claude/tickets/HUB-38-acp-for-all/changelog.md`: new, from REQ-0030's Log and the repos' merge commits (H3).
- `ROADMAP.md`: row 33 HUB-40, Planned (H4).

Deviations: none.

Verification (run):
- Parser check of `scripts/hub.ps1`: 0 errors.
- Dry run with fake services a and b requiring each other (copy in `.claude/temp/hub40`, since deleted): `start a -Window -WaitSeconds 1` printed "a: requires b", "b: requires a", "a: requires cycle a -> b -> a, skipped", one "-Window has no effect" line for `a` only, two "not listening after 1 s" lines and the status table. Nothing started.
- `hub.ps1 start lmstudio -WaitSeconds 1` printed "lmstudio: no start command in services.json; start it yourself" at once.
- `services.json` parses with node; `grep "lms.exe\|lms server"` over `services.json`, `README.md`, `scripts/hub.ps1` finds nothing; `hub.ps1 status` still lists `lmstudio`.

Not run: -Window with a real Electron service; L1, L2, N1-N4; the repo tickets SCP-66, BTT-37, VNO-69, EGS-73, CTS-56, PAR-20, MDI-19, AAP-44.

Follow-ups: L1-L2 after the repo merges and the user's go-ahead; N1-N4 on the user's word.

Commit status: committed on `HUB-40_extra-ideas`, not merged, not pushed.
Polish 1: N2 corrected: a plain re-index does not re-chunk unchanged files (SCP-66 checker finding)
