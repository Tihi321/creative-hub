# HUB-04: Scriptorium live check (SCP-14) and `wait_for_book` in the hub

## Goal

Prove on the hub's Scriptorium that what SCP-14 added works on the real `~\Scriptorium` folder, then let the hub use `wait_for_book` instead of `scripts\wait-book.ps1`.

## Background

- SCP-14 (merged, master 46e5e8a): seed migrations (`migrateClientProvider`, `migrateSeedPrompts`), `wait_for_book`, `get_script`, absolute paths, `factory_status.dataDir` / `embeddings` / `blocked`, and many pipeline fixes. 501 tests pass. Changelog: `scriptorium/.claude/tickets/SCP-14-roadmap-fixes/changelog.md`.
- The hub's copy (`out/`) was built on 2026-10-21, before the merge.
- **Starting Scriptorium resumes its whole book factory and may spend on paid models** (budget in `~\Scriptorium\config\budget.md`). Every start in this ticket needs the user's go-ahead first.

## Decisions

- Made: ask the user before step 2.
- Inferred: check `factory_status` right after the start; if the factory picks up open ideas the user did not want, pause them (`pause_book` or the equivalent) and ask.
- Inferred: the `wait_for_book` test uses a small story the user agrees to (a short story is the cheapest; Claude can do the writing through the client provider for $0).

## Steps

- [x] 1. `hub.ps1 build scriptorium`. Back up `~\Scriptorium\config\` to `.claude\temp\scriptorium-config-<date>\` first.
  - Result: done by orchestrator (master a8cf243 built, config backed up).
- [x] 2. With the user's go-ahead: `hub.ps1 stop scriptorium` (if up), `hub.ps1 start scriptorium -Force` (do not pipe it), `/mcp` reconnect.
  - Result: done by orchestrator (started headless with the user's go-ahead).
- [x] 3. The log (`logs\scriptorium.out.log`) shows the migrations: client provider (added switched off, or context added) and humanizer prompt upgrades for unedited prompts. Diff `config/` against the backup: only those changes.
  - Result: done. Log: 38 migrations (settings.md fallbacks, 36 unedited seed prompts incl. humanizer, templates/cover.html). No client-provider migration needed: `providers.md` already had `client` (dated 2026-10-21). Config diff vs backup: only `settings.md` (default_*_model + model_order became `fallbacks` + `fallback_shared: true`, same models; docs text updated) and `budget.md` (daily counter reset).
- [x] 4. `factory_status` has an absolute `dataDir`, `embeddings` (up or down with a reason) and `blocked`. Stop LM Studio for a moment: `embeddings` says down and no job fails; start it again.
  - Result: partly. `factory_status`: `dataDir` absolute, `embeddings` {lmstudio/text-embedding-nomic-embed-text-v1.5, down:false}, `blocked: []`, `lastResort: null`, `providers`. LM Studio stop NOT run: it is in use (VN Studio vno-media-test pipeline running, `stage`/`build` queued, and embeddings and the read-aloud reviewer use it). So `embeddings` down was not tested.
- [x] 5. `get_script {book: the-clockless-god-3}` returns the parsed chapters (scenes, beats, speakers, choices empty for the linear book). `get_book` paths are absolute.
  - Result: done. `get_script the-clockless-god-3`: 9 chapters, 21 characters, 22 places, 5-7 scenes and 122-163 beats per chapter, `choices: []`, `ending: null`, `sourceChapters` [n,n+1]. `get_book` paths all absolute (folder, epub, coverPng, readerDir, chapters; articlePage null).
- [x] 6. `add_story` for a short story (with the user's choice of premise and models), then `wait_for_book {story: <slug>}` returns when it is published (or failed, with the reason).
  - Result: done. Story/book `the-umbrella-conductor` (bedtime-story, models editor-in-chief/architect/writer = client/claude-code). `add_story {models}` reached `start_book` (fixed). `wait_for_book` returned `client-task` whenever a task waited (also for a story with no book yet), `timeout` while reviewers ran, and `done: true, reason: published` at the end (score 8.53, round 2, $0.044). Problems: see report (title changed despite title_fixed; false 'set in 1989' calendar; slow lmstudio read-aloud review).
- [x] 7. Hub switch: in `.claude/skills/make-visual-novel/SKILL.md` replace the `scripts\wait-book.ps1` paragraph with `wait_for_book {story}`; keep `wait-book.ps1` for when the MCP link is down, or delete it if the user prefers. Update `README.md` (`scripts/` line).
  - Result: done. SKILL.md `wait_for_book {slug}` paragraph, `wait-book.ps1` kept as fallback; README `scripts/` line and the command line updated. (`make-video/SKILL.md` already mentions wait_for_book.)
- [x] 8. Log the run in `runs/<story-slug>.md`; mark the SCP-14 live checks and the `wait_for_book` switch done in `ROADMAP.md`. Problems go to Scriptorium's `ROADMAP.md`.
  - Result: done except ROADMAP.md (orchestrator). Run log: `runs/the-umbrella-conductor.md`.

## Acceptance

- Migrations ran once on the real folder and touched only seed-owned text.
- `factory_status`, `get_script`, `get_book` and `wait_for_book` behave as documented in `scriptorium/docs/mcp.md`.
- The skill uses `wait_for_book`.

## Not in scope

- `yarn test:electron` and the kill-mid-job flake (Scriptorium's own roadmap).
