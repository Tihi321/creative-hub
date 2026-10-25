# HUB-16 changelog — language-independent VN packs

## 2026-10-25 — VN pack v2 across Scriptorium, Book Translator and VN Studio

Outcome: a Scriptorium VN book now has a fixed template (`vn/pack.json`) and a per-language text catalog (`vn/text/<lang>.json`). Book Translator translates only the catalog; VN Studio imports the pack by ID, adds editions without alignment, reuses every existing image/music/SFX, and keeps the game UI in its own Croatian/English tables. The live soother project builds and runs in English and Croatian with all 53 existing assets unchanged. The user's play is pending.

Branches (cut from each `master`):

| Repo | Branch | Ticket |
|---|---|---|
| hub | `HUB-16_vn-pack` | HUB-16 |
| scriptorium | `SCP-45_vn-pack` | SCP-45 |
| book-translator | `BTT-23_vn-pack` | BTT-23 |
| visual-novels-orchestrator | `VNO-46_vn-pack` | VNO-46 |

### Scriptorium — SCP-45

- New `src/engine/publish/vnPack.ts`: `compileVnPack`, `vnPackFromFolder`/`vnPackFromBook`, `writeVnPack`, `readVnPack`, canonical `packHash`, `sourceHash` (excludes `book.md`), catalog key/value validation, atomic writes. IDs from `vnKey` (`src/engine/publish/vnKey.ts`, transliteration in `translit.ts`), scene/beat IDs `ch01.s01`/`.b001`, cues attached to the next beat, CLUE/EVIDENCE/TESTIMONY/PUZZLE mapped, unknown speakers synthesized (real speaker lines only), unknown places `placeKey: null`, ON SCREEN props dropped with a warning.
- Publish hook in `pipeline/handlers.ts` for every `script: true` book, plus `vn_version: 2`; MCP `build_vn_pack`/`get_vn_pack`; `parseScript` now recognises `N:`/`NARRATION:`/`NARRATOR:`, `C<n>`/key/alias speaker tokens, stage directions, and parses `SCENE:` as VN Studio does (first period separates the description; only a 1–4-word known time after the last comma is the time).
- Docs `docs/visual-novel.md` (“The VN pack (v2)”) and `docs/mcp.md`; 31 `tests/vnPack.test.ts` cases and `tests/fixtures/vn-pack/{soother,choice,mystery-puzzle}`.
- Verification: `vitest` 53 files / 679 tests, recovery 1/1; typecheck node+web; eslint clean.

### Book Translator — BTT-23

- New `src/engine/formats/vnPack.ts` (format `vnp`): detection by `vn/pack.json` + `vn/text/*.json` before the legacy `vn`; canonical pack hash; strict pack/catalog/alias validation; catalog-value IR with stable block keys; `<1>Name (expression):</1>` context for spoken lines; v2 brief note; deterministic QA (key parity, one line, non-empty, no structural labels/IDs, inline tags, pack hash); byte-identical bundle export (`edition.json`, `vn/pack.json`, `vn/text/<lang>.json`, `catalog.json`); `localizeNames` via catalog values.
- Legacy `formats/vn.ts`: kept marker bytes must be identical after translation; CLUE/EVIDENCE prose translated with IDs kept; PUZZLE/END TESTIMONY kept whole; TESTIMONY witness localised.
- Docs/README/CLI/MCP updated; `DocumentIR.meta.sourceHash` carries the pack hash; export report adds catalog/lang/keys/warnings.
- Verification: `vitest` 25 files / 360 tests; typecheck node+web; eslint clean. Live: real pack `analyze_file` = `vnp`, 425 blocks, 14 chunks; `get_translation_task` contains only catalog values with the v2 note.

### VN Studio — VNO-46

- New `src/engine/vn/pack.ts`: pack/catalog validation, canonical/source hashes, `VnBook` + primary `Edition`, asset IDs (`backgroundId`, `cueKey`) from the template, `matchPlace` fallback for `placeKey: null`, `aliasKey` name tags, synthetic reference checks, edition key/value validation, primary-edition consistency.
- `importProject`/preview detect the pack; `vno_add_edition` accepts a catalog JSON or bundle and skips alignment/aligner/asset jobs; `vno_sync_editions`; pack metadata/staleness in settings; lint primary/stale checks; `editionLangs` accepts any `langSchema` code.
- UI: Croatian `Clues`/`Accuse`/`Submit`/`Hint`/`Give Up`, English fallbacks; optional `sceneTitles` through Edition → game-data → runtime; edition languages included in voice planning/build; `vno_puzzle_check_text {lang}`; MCP instructions now say HTML5 web engine.
- Verification: `vitest` 78 files / 1071 tests (final idle rerun; one scheduler concurrency test flaked once under load and passed on the rerun); typecheck node+web; eslint clean. Live soother: import 7 chapters/15 scenes/9 characters/8 places, no warnings; all 15 scenes reproduce the existing `backgroundId`s; hr edition `matched 381, missing [], extra []`, keyCount 424; assets 53 → 53 IDs/versions/files; build `ok` no placeholders; lint `ok` 381 English + 381 Croatian blocks; `game-data` has en+hr, 15 scene titles, `Skip: Preskoči`, `Clues: Tragovi`, 10 backgrounds all present.

### Hub — HUB-16

- `.claude/tickets/HUB-16-vn-pack/{plan.md,contract.md}` (canonical cross-repo schema, IDs, hashes, invariants), `ROADMAP.md` row, `README.md` pipeline/tool table, `make-visual-novel` skill (pack flow; EPUB is a reader artifact; UI stays VN Studio’s; HTML5 player launch replaces the stale Ren’Py step), `runs/hub16-vn-pack.md`.
- Verification: contract fixture check (template/catalog keys/hashes) on all three fixtures; hub `hub.ps1` build/start of VN Studio + Book Translator; live MCP import/edition/build/lint as above; user play pending.

### Deviations and decisions

- The first pack exposed that `parseScript` took the whole `SCENE:` line as place/time. Fixed in SCP-45 and fixtures/real pack regenerated.
- Two live scenes (`ch02.s01`, `ch03.s01`) have SCENE text that changed since the old soother project was imported. The live pack was given `dragon_path` (plus a `Dragon Path` place entry) and `singing_dragons_chorus` so the existing backgrounds are reused; the compiler’s place matcher is not changed for this book-specific migration.
- The live project’s `editions/hr.json` was empty and LM Studio/Strata are down, so the live Croatian catalog was extracted from the Croatian EPUB Book Translator produced earlier (381/381 beats, 0 fallbacks). Book Translator’s new adapter is proven by tests and a live `analyze_file`/task; a full live translation through it is the next production run.
- No asset files were regenerated; manifest prompt metadata may differ because the pack’s scene description is richer.
- VNO’s full suite had one unrelated scheduler concurrency flake; rerun on an idle machine before merge.

### Commit status

Committed and pushed on 2026-10-25:

| Repo | Branch | Commit |
|---|---|---|
| hub | `HUB-16_vn-pack` | `d090a01` |
| scriptorium | `SCP-45_vn-pack` | `ec5d6ad` |
| book-translator | `BTT-23_vn-pack` | `ccf23b1` |
| visual-novels-orchestrator | `VNO-46_vn-pack` | `bde84ca` |

Each branch was pushed on 2026-10-25 and merged: hub PR #10 (`b8029e5`), Scriptorium PR #13 (`3a9102b`), Book Translator PR #16 (`5e2938f`), VN Studio PR #20 (`770b694`). HUB-16 moved to Done in the hub roadmap and the live soother game was rebuilt from `master`. The user's play verdict is not separately recorded.
