# HUB-02: Book Translator live check (BTT-11)

## Goal

Prove on the hub's running Book Translator that what BTT-11 added works with real data, and leave a Croatian VN edition that VN Studio can use. No code change is planned. A failure becomes a new BTT ticket in `C:\projects\Personal\book-translator\ROADMAP.md`.

## Background

- BTT-11 (merged, master 1895741) added: providers.md / models.md / defaults.json reload every 3 s; client model context default 200,000; seed migration with `config/seed-state.json`; the prompt sent once in client tasks; `localizeNames` for VN book folders; "Open a book folder" in the app. 283 tests pass. Changelog: `book-translator/.claude/tickets/BTT-11-roadmap-fixes/changelog.md`.
- The hub's copy (`out/engine/index.js`) was built on 2026-10-20, before the merge.

## Decisions

- Made: the live check runs on the user's real data folder `~\BookTranslator`.
- Inferred: the VN run uses the linear *Clockless God* VN book (`the-clockless-god-3`, 9 chapters) into Croatian with `clientOnly: true`, so Claude does the model work for $0, and book 1's Croatian glossary terms (`runs/the-clockless-god.md`) go into the brief.
- Open (ask the user): `localizeNames` on or off for this edition. On renames speaker tags and bible names from the glossary (for example a Croatian form of a name); off keeps the English names. Recommendation: on only if the user wants Croatian name forms in the game.

## Steps

- [ ] 1. `pwsh -File scripts\hub.ps1 build book-translator`, then `stop book-translator`, `start book-translator` (do not pipe `start`; see HUB-12), then `/mcp` reconnect.
- [ ] 2. Seed migration: `~\BookTranslator\config\seed-state.json` exists after the first start, and `logs\book-translator.out.log` lists what was added (or nothing). The user's `config/providers.md` edits are unchanged (diff against a copy taken before step 1).
- [ ] 3. Reload: copy `config/providers.md` to `.claude/temp/`, add a harmless test model to an existing provider, and within ~5 s `list_models` shows it with no restart. Put the file back and check it is gone. Also break the YAML once: the log says so and the old providers stay.
- [ ] 4. Client context: `list_models` shows the client model with context 200000.
- [ ] 5. VN run: `create_project` with the folder of Scriptorium book `the-clockless-god-3`, target `hr`, `clientOnly: true`, `localizeNames` as decided; `set_brief` in Croatian with book 1's glossary terms. Work the client tasks (glossary, translation, proofreading, QA) with subagents as in `runs/the-clockless-god.md`. Check one `get_client_task`: a plain task has `system` + `user` and no `messages`.
- [ ] 6. `export_project` writes a mirrored book folder. With `localizeNames` on: speaker tags, `ON SCREEN:` names and bible character bullets use the glossary names; the bible prose and cover brief stay English.
- [ ] 7. Hand the folder to VN Studio: `vno_add_edition {slug: the-clockless-god-3, source: <export folder>, lang: hr}`, then `vno_align_report` (no missing or extra beats). The build and play are in HUB-03.
- [ ] 8. Log everything in `runs/the-clockless-god-vn.md` (ids, what was checked). Mark the BTT-11 live checks done in `ROADMAP.md`.

## Acceptance

- `seed-state.json` written, providers.md reload seen without restart, broken file kept the old config.
- A Croatian VN edition exported and aligned in VN Studio with 0 missing and 0 extra beats.
- Client tasks carry the prompt once.
- Anything that failed is written as a BTT item in Book Translator's `ROADMAP.md`.

## Not in scope

- The Electron UI (book-folder picker, checkboxes): a manual check in Book Translator's own roadmap.
- The *Hour That Happens Twice* translation (HUB-05).
