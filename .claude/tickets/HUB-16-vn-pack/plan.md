# HUB-16 / SCP-45 / BTT-23 / VNO-46 — Language-independent VN book packs

Approved 2026-10-25. This file is the authoritative plan for the hub ticket; each repo keeps its own plan subset in `.claude/tickets/<ticket>/plan.md`.

## Why this change

The three tools already almost meet the goal, but the seam is the whole book folder:

- **Scriptorium** writes VN chapters as free text (`SCENE:`, `ON SCREEN:`, `NAME (expression):`, narration) with **no scene/beat/character IDs** (`publish/script.ts`, `publish/xhtml.ts`). Its `book.md` has no language or edition concept; `get_script` returns strings only.
- **Book Translator** re-parses that folder into positional blocks `b1…bN`, classifies each line with its own grammar copy (`formats/vn.ts`), and writes a translated copy of the folder. Unmatched lines fall through as “narration” and are translated whole (that is how `On screen:` / `Narration:` labels got translated in the Croatian EPUB screenshots). Its export guard checks the line *kind*, not the kept marker bytes.
- **VN Studio** re-parses the translated folder and pairs it to the original by chapter number, scene index, per-type position and text similarity (`vn/align.ts`), with an LLM `edition-aligner` for leftovers. Editions are already text-only keyed by beat ID (`shared/vn.ts`), and **all images, sprites, sheets, CGs, inserts, music, SFX and ambience are language-free and already reused**. Voice is per language by design. The web player already has a language switcher (VNO-41) and UI strings in `shared/ui-strings.ts` (Croatian complete, English source).

So: assets and UI separation are mostly solved; **structure is not**. Three parsers (Scriptorium, Book Translator, VN Studio) plus a test copy guarantee drift, and translation can move or destroy structure.

## Goal

Every Scriptorium VN book ships a **language-independent pack**: an immutable template with fixed IDs and art descriptions, plus one text catalog per language.
- Translators translate **only the catalog**; the template is never opened by Book Translator.
- VN Studio imports the pack directly, adds translated catalogs by ID, and reuses every generated asset.
- The game UI stays VN Studio’s own (Croatian + English first), never part of the book or its translation.
- Linear VNs, choice VNs and puzzle VNs all use the same pack; existing books can be compiled on demand.

## Success criteria

1. For the existing `soother` and `mystery-puzzle` fixtures, pack import in VN Studio produces a `VnBook` and asset plan **identical** to the legacy folder import (except warnings/uncertain).
2. Translating a pack changes **no byte** of `vn/pack.json`; the translated catalog has exactly the source key set (no missing/extra).
3. `vno_add_edition` on the translated catalog reports `missing: []`, `extra: []`; `assets.json` and every asset file are unchanged and no generate job is queued.
4. A build has `editions.en` and `editions.hr`; switching language changes dialogue, narration, names, chapter/scene titles, choices, endings and puzzle prose, and the Croatian UI labels — not images, music, SFX or ambience.
5. Existing v1 books, projects, folders and tests keep working; existing published books can be compiled with one Scriptorium call.
6. A real existing project (`the-soother-that-fell-into-dragon-land`, 53 assets, en+hr editions) plays in both languages with identical artwork and audio, and the user confirms it.

## Decisions

| # | Decision |
|---|---|
| D1 | **Scriptorium owns the pack.** At publish (and on demand) it compiles the authored chapter folder into `vn/pack.json` + `vn/text/<sourceLang>.json`. Chapters stay the human authoring/review format; no writer-prompt change is needed because IDs are engine-assigned, never model-written. |
| D2 | **IDs are fixed and engine-owned.** Characters: `slugKey(bible name)` (VN Studio’s rule), aliases `<charKey>#<n>`. Places: `slugKey(place)`. Scenes `ch01.s01` (only scenes that have beats), beats `ch01.s01.b001`, choices `"<chapter>:<index>"`, endings `"<chapter>"`, puzzles/clues as today. The narrator is the beat type `narration` (token `N` in the contract); no translated name is ever a structural token. |
| D3 | **Template = structure + art fields.** It holds keys, looks, voice notes, scene place/time/background description, cue descriptions, expression words, branch targets, puzzle cores and `clueAt`. Catalog = the only translatable fields: title, blurb, chapter titles, scene titles, choice texts, endings, character/alias display names, beat text (line/narration) and puzzle names/clue prose. |
| D4 | **VN Studio derives asset IDs**, not Scriptorium: `backgroundId` and `cueKey` stay in VNO’s existing `ids.ts`/`script.ts` logic, applied to the untranslated template. No asset key is computed from translated text. |
| D5 | **Book Translator gets a new v2 adapter.** It reads the pack as read-only and builds its IR from the source catalog only; one block per catalog key, block ID = catalog key. It exports a same-shape target catalog plus a small bundle; it never parses or rewrites chapters. |
| D6 | **VN Studio accepts catalogs by ID.** `vno_add_edition` accepts a catalog JSON file or an edition bundle folder; validation is key-set/ID based and skips `alignEdition`/`edition-aligner` for v2. Legacy folder alignment stays for old books. |
| D7 | **Voice is per language; art is shared.** Images, sheets, sprites, CGs, inserts, music, SFX and ambience are reused automatically. A new edition without voice is silent; voices are generated per language. |
| D8 | **UI stays in VN Studio.** `shared/ui-strings.ts` remains the only UI source; English is the source/fallback and Croatian gets the missing runtime keys. No UI string enters the pack or the catalog. |
| D9 | **Backward compatible.** Existing books get a pack via `build_vn_pack`; existing projects keep working; re-importing a pack into an existing project keeps assets when the IDs match; the v1 Book Translator adapter stays, deprecated. |
| D10 | **One branch per repo**, from `master`: hub `HUB-16_vn-pack`, Scriptorium `SCP-45_vn-pack`, Book Translator `BTT-23_vn-pack`, VN Studio `VNO-46_vn-pack`. |

## Contract v2

The exact field definitions and hash/ID rules are in `contract.md` next to this plan. Summary:

```text
books/<slug>/
  book.md, outline.md, chapters/, bible/, cover-brief.md     # unchanged authoring source
  vn/pack.json                                               # template, never translated
  vn/text/<sourceLang>.json                                  # source catalog

<export>/<slug>.<lang>/
  edition.json                                               # {format:"vn-edition-bundle",version:2,lang,packHash,sourceSlug}
  vn/pack.json                                               # byte-identical copy
  vn/text/<lang>.json                                        # translated catalog
```

- `vn/pack.json`: `format:"vn-pack"`, `version:2`, `packHash`, `book`, `characters`, `places`, `expressions`, `chapters`/`scenes`/`beats`, `puzzles`. Beats are `cast|line|narration|puzzle` with cue **descriptors** (`image:{display,text,key?}|null`, `sfx:{text}|null`, `ambience:{text}|null`); VN Studio turns them into `cg_`/`sfx_`/`amb_` IDs with its own `cueKey`/`backgroundId`.
- `vn/text/<lang>.json`: `format:"vn-text"`, `version:2`, `lang`, `packHash`, `title`, `blurb`, `chapterTitles`, `sceneTitles`, `choiceTexts`, `endings`, `characterNames`, `beats`, `puzzles` — exactly VN Studio's `Edition` shape plus metadata and the two optional fields.
- Invariants: template has no display text; catalog has no structure; catalog key set equals the pack’s expected set; single-line non-empty values; no structural labels introduced; `packHash` covers canonical `pack.json`; `sourceHash` covers authored files; stale hashes warn/reject.

## Work by repo

### Hub — HUB-16 (`HUB-16_vn-pack`)

1. Ticket folder with `contract.md`, `plan.md`, `changelog.md`; HUB-16 row in `ROADMAP.md`.
2. Shared fixtures in `.claude/tickets/HUB-16-vn-pack/fixtures/`: `soother` (linear, cast/looks/cues), a choice variant, `mystery-puzzle` (CLUE/EVIDENCE/PUZZLE/TESTIMONY); copy into the three repos’ tests.
3. `make-visual-novel` skill: publish writes the pack; older books call `build_vn_pack`; translate the **pack** (format `vnp`), never the EPUB for a game edition; `vno_import` uses the pack; catalogs auto-become editions; replace the stale Ren’Py launch step with the HTML5 player; UI stays VN Studio’s.
4. `README.md` pipeline/tool table updates.
5. Live check + `runs/<slug>-vn-pack.md`; optional `scripts/vn-pack-check.mjs`.

### Scriptorium — SCP-45 (`SCP-45_vn-pack`)

1. New `src/engine/publish/vnPack.ts` compiler using `parseScript`, `parseLightBible`, `settleScenePlaces`, `moveTrailingCues`, `checkBranches`, `puzzleProblems`; final VN beats with cues attached, clue/evidence/testimony mapped, IDs assigned; unknown speakers/places synthesized with warnings; source + pack hashes; atomic writes.
2. Publish hook in `pipeline/handlers.ts` for every `script: true` book; `vn_version: 2` in `book.md`.
3. MCP `build_vn_pack {book}` and `get_vn_pack {book}`.
4. Parser hardening: `N:`/`NARRATION:`/`NARRATOR:` as narration; `C<n>`/bible-key speaker tokens; puzzle keywords never speakers. No writer-prompt/seed migration.
5. Key helper matching VN Studio’s `slugKey`, with shared test vectors; collision suffix `_2` + warning.
6. Docs `docs/visual-novel.md` (“The VN pack (v2)”) and `docs/mcp.md`.
7. Tests: fixtures → expected pack/catalog; ID stability; choices/endings; puzzles; aliases; unknown speaker/place; cue attachment; no display text in template; no structure in catalog; MCP.

### Book Translator — BTT-23 (`BTT-23_vn-pack`)

1. New `src/engine/formats/vnPack.ts`, format `vnp` in `shared/ir.ts`, detected before legacy `vn`; hash covers pack + source catalog. `formats/vn.ts` untouched except the safety check.
2. IR from the catalog only, one block per key (`title`, `chapter.1.title`, `choice.1.0`, `ending.2`, `scene.ch01.s01`, `char.petra`, `char.petra#1`, `beat.ch01.s01.b003`, `puzzle.dinner.text.c1`); line beats carry `<1>Petra (worried):</1>` context, dropped on write.
3. Engine-side v2 prompt note; no new prompt files.
4. Deterministic QA: exact key set; non-empty/single-line; no `SCENE|ON SCREEN|NARRATION|CG|INSERT|SFX|AMBIENCE:` at the start; inline tags; untranslated/ratio; pack hash unchanged. Key mismatch = hard export error.
5. Export bundle + bare catalog; `export_project` returns path/lang/keys/warnings.
6. `localizeNames` for v2 = translate `char.*` values; v1 unchanged. Legacy safety: kept prefix bytes identical, CLUE/EVIDENCE/PUZZLE/TESTIMONY recognized.
7. Docs/CLI/MCP updates.
8. Tests: IR, mock pipeline, key parity, template byte-identity, rejections, v1 regression, hash stability, MCP.

### VN Studio — VNO-46 (`VNO-46_vn-pack`)

1. New `src/engine/vn/pack.ts`: validate pack/catalog, build `VnBook` + primary `Edition`, derive asset IDs with existing rules, warnings; `importProject` detects `vn/pack.json`; legacy stays.
2. `vno_add_edition` accepts catalog JSON or bundle; validate pack hash/keys/lang; save edition + report, no align/LLM; add `vno_sync_editions` (or import option) scanning `vn/text/*.json`.
3. Optional `packHash`/`packVersion`/`sourceHash` in project settings; reject mismatched edition; keep `vn.json` primary and `editions/<primary>.json` consistent; lint check.
4. Asset reuse regression: `assets.json` unchanged after edition add; no prompts from catalog.
5. UI: add `Clues`, `Accuse`, `Submit`, `Hint`, `Give Up` to Croatian + English fallbacks; optional `sceneTitles` in Edition/CompiledEdition/game-data and runtime; full switch test. No UI in pack.
6. Voice wiring: edition languages in build voice source and generate choices; document no cross-language voice reuse.
7. `vno_puzzle_check_text` `lang` parameter for edition read-back.
8. Fix 3-letter/hyphenated edition codes; update MCP instructions (“Ren’Py” → web engine); docs.
9. Tests: pack fixture parity with legacy import; catalog edition exact; rejections; template identity; assets unchanged; en+hr build/UI/scene titles; voice; legacy align; real fixture builds.

## Edge cases

- Stale pack/sourceHash → warning; editions kept but marked stale; recompile/re-translate.
- Pack changed (`packHash`) → VNO rejects edition; BT starts a new project.
- Unknown speaker/place → synthetic key, warning, still compiles.
- Empty/multi-line catalog value → SCP refuses write; BT refuses export.
- Structural label in translation → deterministic QA blocks export.
- Choice/alias reorder → positional keys; pack hash changes, edition stale rather than silently re-attached.
- Missing edition beat → build falls back to primary and warns.
- UI language without table → English fallback.
- Legacy folders → v1 path everywhere; EPUB unchanged.
- Puzzles → logic unchanged; translated prose read back in target language.
- RTL/fonts unchanged.

## Tests and acceptance

Per repo: `yarn test`, `yarn typecheck`, `yarn lint` (Scriptorium also `test:recovery`; VN Studio’s full suite).

Cross-repo:
1. Parity on `soother`, `choice`, `mystery-puzzle`: pack import `vn.json` deep-equal to legacy import (minus warnings/uncertain); asset IDs identical; also the real soother book.
2. Translation invariant: pack and non-catalog files byte-identical after a full run; key sets equal; target values non-empty.
3. Edition invariant: adding hr to the existing soother project leaves `assets.json`/files unchanged, no generation, `missing/extra` empty.
4. Build/runtime: en+hr editions, Croatian UI and scene titles; switching changes only text/UI; identical art/audio file set.
5. Legacy: existing tests green; v1 export byte-identical; legacy folder align still works.
6. User plays en+hr, menus/skip, a choice and a puzzle (one failure path).

## Live check

Use `the-soother-that-fell-into-dragon-land` (53 assets, en+hr editions) or `the-clockless-god`.
1. Start only needed services; ask before Scriptorium.
2. `build_vn_pack`; record hashes/files.
3. Snapshot `assets.json` + asset hashes.
4. BT analyze (`vnp`), create hr, translate, export; check template hash/key parity.
5. VNO import pack (same slug) + add hr catalog; `missing/extra` empty; assets unchanged.
6. Build/lint; switch en↔hr; check text/UI only; identical art/audio.
7. User plays both; record in `runs/<slug>-vn-pack.md`.

## Execution and branches

| Phase | Owner | Scope | Branch |
|---|---|---|---|
| P0 | Lead | HUB-16 contract, fixtures, roadmap, skill | `HUB-16_vn-pack` |
| P1 | implementer | Scriptorium compiler/tools/tests/docs | `SCP-45_vn-pack` |
| P2 | implementer | VN Studio pack/edition/UI/voice/tests/docs | `VNO-46_vn-pack` |
| P3 | implementer | Book Translator adapter/QA/export/tests/docs | `BTT-23_vn-pack` |
| P4 | Lead | integration, parity, live check, changelogs | hub branch |

P1–P3 run in parallel against P0 fixtures; P4 after all three. Cut from each repo’s `master` (BTT-23 from `master`, not `BTT-22`). Each repo keeps `.claude/tickets/<ticket>/{plan,changelog}.md`; the hub plan is saved before implementation. Use the `implement` skill’s implementer role and disjoint write scopes.

## Out of scope

- Translating app chrome of Scriptorium/Book Translator; only game UI (hr/en).
- Reusing voices across languages; only language-free assets are shared.
- EPUB structure/locale work.
- VN Studio invoking Book Translator inside its pipeline.
- New puzzle kinds, Android, native review of the other 35 UI languages.
- Migrating v1 projects in place (re-import as pack supported; v1 stays supported).

## Assumptions

- Source books are English for now (`primaryLang: en`).
- Character display names kept by default; `localizeNames` translates catalog values.
- Game UI follows the selected game language via VN Studio’s tables; English fallback, Croatian first complete translation.
- “Reuse generated assets” = art/music/SFX/ambience/CGs/sheets/sprites, not voices.
- The existing soother project’s 53 assets must stay; fix key rules before generating anything if parity fails.
