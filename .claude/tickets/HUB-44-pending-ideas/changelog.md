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

## 2026-11-23 Round summary: what was built, the live round, what is open

Outcome: everything built is merged on master and pushed. The live round of 2026-11-22/23 is done except the items under "Open for the user". Full detail: `runs/hub-44-pending-ideas.md`.

### Built and merged, per repo
- api-acp-proxy: AAP-51 merge 33a76c2 (Monitor and settings leftovers; images to Strata right after a proxy start); AAP-52 merge 07bccd3 (`unsupported_content` after a lease mapped to `model_not_capable` for MCP callers, the models cache row for Strata refreshed at load, leftovers of AAP-51); AAP-53 merge 84d3f0e (Gufo tiles in the Monitor, the About image note, GiB, the dot, reason texts, the approximate mark).
- pixel-art-generator: PAR-25 part A merge 5b63ec0 (a run that redraws the same picture stops; the repeat guard counts only steps whose tool writes the picture; optional `no-files` tool set); PAR-26 merge 820f2e9 (guard and tool-set tests, abort test, `config/app.json` in the README, `chatJson` usage of repairs, `repeatStop` in `get_agent_run`); PAR-25 part B merge 5a73ed3 (Strata as vision model: a one-line migration of `providers.md`).
- visual-novels-orchestrator: VNO-73 merge 35ed8da (final full stop of a stripped prompt, a log line for stripped revisions); VNO-74 merge 95ce939 (Gufo health probe).
- edu-game-studio: EGS-76 merge 36e52ef (critic fixes without text negations); EGS-77 merge 8197a08 (Gufo health probe).
- cartoon-studio: CTS-59 merge bec990f (Gufo health probe).
- scriptorium: SCP-69 merge f67b39a (small leftovers); SCP-70 merge 18d12fc (the second adaptation test's race).
- midi-generator: MDI-21 merge f1d1d12 (perf test margin).
- creative-hub: merge 8bdf7f0 (hub.ps1 H1-H3, see the entry above); the commit after it adds the run log, the ticket records, ROADMAP row 37 and the CLAUDE.md line on Pixel's vision model.

### Live round verdicts (2026-11-22 22:09Z to 2026-11-23 09:05Z)
| step | verdict | note |
|---|---|---|
| P0 preconditions | PASS | services as planned, every provider idle, settings hash unchanged |
| R1 proxy rebuild; P-02 image to Strata right after a start | PASS | 200 with a description of the image |
| R2 VN rebuild, R3 Pixel and Edu builds, Cartoon build checked | PASS | locks replaced, `vno_status`, `edu_status`, `cts_status` answer |
| L1-L3 live prose of Edu and Cartoon | PASS | prose equals the seed, front matter hashes unchanged, `.bak-HUB-44` backups |
| K1 starts: stale locks removed, prompts refreshed | PASS | real dead-pid locks removed on real starts |
| K2 the 8 queued VN job files | PASS | in the Recycle Bin, `queued` empty |
| K3 Edu ComfyUI free | PASS | lane 8188 ok |
| K3 Cartoon ComfyUI free; autostart Gufo check | UNTESTED | no tool; ComfyUI was always up |
| K5 Strata as Pixel's vision model, three runs | PASS | 3 of 3 completed (two ended by the guard), 0 USD |
| K6 `no-files` tool set | PASS | first prompt 3,904 tokens smaller |
| K4 VN negation stripper | UNTESTED | the critic wrote no negation |
| K4 Edu critic | UNTESTED | a local-only run could not be guaranteed without a config edit |
| K8 Gufo probe | PASS | /health, /props, /slots, /metrics answer; /v1/status 404 |
| B1 + S4 Pixel migration and a real artist run | PASS | one line `vision: true` inserted, 4 steps, completed, 0 USD |
| S1 AAP-52 refusal after a load | UNTESTED | needs a text-only local model loaded; the early refusal was checked instead |
| S1 AAP-53 in the window | UNTESTED | needs the window (K9) |
| S2-S3 rebuilds of VN, Edu, Cartoon | PASS | |
| S4 PAR-26 `repeatStop` live | UNTESTED | the guard did not fire |
| K7 full Scriptorium re-chunk (09:26-09:30Z, 240 s, exit 0) | PASS | files 1,449 before and after; chunks 6,707 -> 6,645; separator-only chunks 55 -> 0; longest chunk 1,790 characters; Scriptorium not started, so a search against the new index is UNTESTED |
| K10 | NOT RUN | held, see Deviations |

### Deviations
- The stage 2 launch was denied by the permission check as possibly destructive; it was not worked around, and a reduced stage 2 ran. So K7 (Scriptorium re-chunk), K10 (Scriptorium start) and a temporary edit of Edu's live config were not run.
- The session was suspended about 9 hours (22:32Z to 07:43Z); the K4 VN job finished on its own.
- The director wrote `status: approved` and the plan events on the seven plans, because the scribe cannot see the user's messages; the user was told.
- K4 VN took two attempts; the Pixel vision migration ran at Pixel's first model use, not at start.

### UNTESTED
The VN critic's negation stripper live; the Edu critic (P-25, P-27b); AAP-52's refusal after a load; AAP-53 in the Monitor and About windows (K9); the autostart Gufo and Strata check; PAR-26 `repeatStop` live; Cartoon's ComfyUI free; pid-reuse lock removal on a real app; Strata's image input proven in its log; the Scriptorium re-chunk and start.

## Open for the user
- K7: DONE (2026-11-23): 1,449 files, chunks 6,707 -> 6,645, separator-only chunks 55 -> 0; a search against the new index is untested (Scriptorium not started).
- K10: starting Scriptorium for P-32 and P-34. Never without the user's word: it resumes the whole book factory and may spend on paid models.
- The Edu critic check (P-25, P-27b): a throwaway course whose run is local-only; needs a temporary edit of Edu's live config.
- K9: look at the ACP proxy window (Monitor and About). Expected values: `runs/hub-43-open-ideas.md`, section "What the Monitor and About pages should show". Since then AAP-51, AAP-52 and AAP-53 changed: sizes in GiB, the dot on the chart, reason texts, the approximate mark, Gufo tiles, and the About page's image note.
- Backups and scratch, to delete when happy: the Scriptorium index backup `C:\Users\Infplane\Scriptorium\index\library.sqlite.bak-HUB-44` (about 50 MB); the `.bak-HUB-44` files of Edu `providers.md`; Cartoon `providers.md` and `settings.md`; Pixel `providers.md` and `seed-state.json` (in the live data folders); and `.claude\temp\hub44-live` in this repo.
- Unbuilt extra ideas (from the request file REQ-0031, none decided): AAP-51 `architecture.input_modalities` in `/v1/models` (AAP-52 left it out: it would change Pixel's and Chiptune's fallback choice); AAP-51 Strata's `/health` `loaded: true` as its ready check (a lazy Strata would never be ready); hub planner: probe Strata's `strata_prefix` field for P-16; Monitor: a Speculation tile from spec_decode counters; Monitor: support for a Gufo started outside the app; `services.json`: a `gufo` entry; VN and Edu: mention Gufo in the seed `autostart.md`; Strata holder probe: a JSON check; Pixel: log a failed migration's warning (`setup.ts` discards the result); Pixel: run migrations at start, not at the first model call; Pixel: `migrateAcpPort` re-serializes `providers.md`; Edu: the test setup rewrites `out/live` of a running app; proxy `README.md:164` stale sentence (Strata answers after its lease since AAP-51); Pixel: `chatJson` usage lost when it fails after two repairs. Also noted: Edu's pipeline tests are timing-sensitive under load.
