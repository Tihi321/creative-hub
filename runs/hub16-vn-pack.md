# HUB-16 — VN pack v2 integration run

Started 2026-10-25. Ticket: `.claude/tickets/HUB-16-vn-pack/` (`plan.md`, `contract.md`).

## Branches

- hub `HUB-16_vn-pack` (from `master`)
- Scriptorium `SCP-45_vn-pack` (from `master`)
- Book Translator `BTT-23_vn-pack` (from `master`, not from `BTT-22`)
- VN Studio `VNO-46_vn-pack` (from `master`)

## What “done” means

- A Scriptorium book folder has `vn/pack.json` + `vn/text/en.json`; the template holds IDs/looks/scene and cue descriptions/puzzle logic, the catalog holds only display text.
- Book Translator translates the catalog and writes a byte-identical template copy + `vn/text/hr.json`; key sets match exactly.
- VN Studio imports the pack (parity with the legacy import), adds the hr catalog by ID (`missing/extra` empty), and reuses every existing asset with no generation job.
- The build plays en and hr; switching changes text/UI only; Croatian puzzle labels and scene titles show.
- Legacy v1 books, projects and tests still pass.
- The user plays both languages.

## Live check target

`~/VisualNovels/projects/the-soother-that-fell-into-dragon-land` — 53 assets (10 backgrounds, 9 sheets, 29 sprites, 4 music, 1 cover), editions `en`+`hr`, 7 chapters, 9 characters, 8 places, no CGs/SFX/puzzles. Use the `mystery-puzzle` fixture for CLUE/EVIDENCE/PUZZLE/TESTIMONY coverage.

## Status

- [x] Plan + contract saved; four branches cut; three implementers ran.
- [x] Hub roadmap/skill/README updated for the pack and the current HTML5 player.
- [x] SCP-45: pack compiler, publish hook, `build_vn_pack`/`get_vn_pack`, narrator/key tokens, SCENE first-period/time fix, key helper, docs. `yarn test` 53 files / 679 tests + recovery 1; typecheck and lint green.
- [x] BTT-23: `vnp` adapter, catalog-only IR, v2 prompt note, deterministic QA, byte-identical template, bundle export, legacy harden. `vitest` 25 files / 360 tests; typecheck and lint green. Live: `analyze_file` on the real pack = `vnp`, 425 blocks, 14 chunks; `get_translation_task` shows only catalog values (`title`, `blurb`) with the v2 note.
- [x] VNO-46: pack reader (`matchPlace` fallback), catalog editions, `vno_sync_editions`, pack meta/staleness, scene titles, Croatian UI keys, voice edition languages, docs. `vitest` 78 files / 1071 tests (one scheduler test flaked under full load; passes alone), typecheck and lint green.
- [x] Canonical fixtures refreshed after the SCENE/expression fixes; BTT and VNO canonical tests green.
- [x] Real soother pack installed (`~/Scriptorium/books/the-soother-that-fell-into-dragon-land/vn/`), re-imported with no warnings: 7 chapters, 15 scenes, 9 characters, 8 places; all 15 scene `backgroundId`s match the assets the project already had.
- [x] HR catalogue (381/381 text beats, 15 scene titles, 8 choices, 3 endings) added by `vno_add_edition`: `matched 381, missing [], extra [], keyCount 424, warnings []`.
- [x] Asset snapshot before/after: 53 assets, 53 files, same IDs, versions, selection and file hashes; no generation job.
- [x] Build: `ok`, no placeholders, `translated: ["croatian"]`; lint: `ok`, `381` English blocks and `381` Croatian blocks. `game-data.json` has `en`+`hr`, 15 scene titles, `Skip: Preskoči`, `Clues: Tragovi`, 10 backgrounds with all files present.
- [x] Final VNO full suite on an idle run: 78 files / 1071 tests passed; typecheck node+web and eslint clean.
- [ ] User plays en+hr (opened `…\game\index.html`; verdict pending).

## Deviations / notes

- **SCENE parsing:** the first pack exposed that Scriptorium took the whole `SCENE:` line as place/time. Fixed in `parseScript` (first period splits the description; the last comma is a time only when it is 1–4 known time words) and recompiled.
- **Two live scene keys hand-patched:** the current book's `ch02.s01` and `ch03.s01` SCENE text differs from the old project's import (`A path through Dragon Land` / `Grassy hill…` vs `Path through Dragon Land` / `Singing Dragons' Chorus`). The pack was given `dragon_path` (and a `Dragon Path` place entry) and `singing_dragons_chorus` so the existing `bg_dragon_path_morning` and `bg_singing_dragons_chorus_day` files are reused. All other 13 scenes resolved through the new SCENE parse/`matchPlace`.
- **HR text source:** the project's `editions/hr.json` was empty, and LM Studio/Strata are down. The live HR catalogue was extracted from the Croatian EPUB Book Translator produced earlier (381/381 beats mapped, 0 fallbacks); Book Translator's new adapter is proven by 360 tests and the live `analyze_file`/task above. A full live HR translation with the adapter is the next production run.
- **Assets:** manifest prompts may differ from the old descriptions (the pack's scene description is richer), but no asset ID, version, selection or file changed and no image was regenerated.
- **VNO full suite:** the first full run had one unrelated scheduler concurrency test (`3 books x parallel reviews…`) fail under load; the final idle rerun passed all 78 files / 1071 tests, so it is recorded as a flake, not a regression.

