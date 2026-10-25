# HUB-17 — Children's picture books (VN Studio VNO-47, Scriptorium SCP-46)

Approved 2026-10-25. Branches: hub `HUB-17_picture-books`, VN Studio `VNO-47_picture-books`, Scriptorium `SCP-46_picture-books`, all from `master`.

## Sažetak (HR)
Slikovnica = jedan ilustrirani prizor s likovima u slici + kratak tekst ispod, okretanje stranica. Nema spriteova, nema tekstualnog okvira preko slike, nema CG/insert mašinerije. Lanac ostaje isti: Scriptorium napiše tekst (novi format `kids-picture-book`) → VN pack → VN Studio generira slike/muziku/glas i gradi HTML5 knjigu. Peppa PDF je samo referenca za izgled; ne kopiramo tekst ni likove. Rezultat: HTML5 knjiga (bez PDF-a).

## Goal and success criteria

Picture books are a first-class output of the hub, simpler than visual novels: **one full-page illustration with the characters drawn into it, one to three short sentences below, page turns**. The chain stays Scriptorium → VN pack (v2) → VN Studio → HTML5 build, so translations, music, voices and the existing UI keep working.

1. A project whose book is `kids-picture-book` (or `presentation: "picture-book"`) imports with `presentation: "picture-book"` and plans **one page illustration per scene**, no `sprite_*` and no `cg_*` assets; only internal character-sheet references (hidden, for likeness) remain from the character assets.
2. Page prompts draw the characters **into** the illustration: style + place + scene description + the scene's cast with their looks, no "empty environment" wording and no people/animals ban in the negative.
3. The built HTML5 book renders one page per scene: illustration on top (contained, nothing cropped), text below in the theme's font/colours, page counter, prev/next, click/tap and arrow keys; no sprites, name box, quick menu, scene title or VN textbox.
4. Language switch re-renders the current page's caption and UI labels; save/load returns to the same page; the last page shows "The End" with restart.
5. Scriptorium writes `kids-picture-book` books: one chapter, 12–16 pages-as-scenes, narration-only page text, `ON SCREEN:` naming who is in the picture, no cue lines; publishing writes the v2 pack; `get_script` and `get_vn_pack` work unchanged; the format reaches existing data folders through a start migration.
6. VN behaviour is unchanged (existing 1000+ VN Studio tests, Scriptorium tests, typecheck and lint green).
7. A real Croatian picture book (12–14 pages, Flow or ComfyUI art, Supertonic narration + a bicycle-bell SFX) is built, opened in the browser in `game/index.html`, and **the user plays it**; verdict recorded in `runs/<slug>.md`.

## Decisions

| # | Decision |
|---|---|
| D1 | **Presentation is a book property.** `VnBook.presentation?: 'visual-novel' \| 'picture-book'` (optional → old `vn.json` parses). New imports store it explicitly from `presentationForFormat(format)`; `presentationOf(book)` = the field, else derived. Overridable by `book.update { presentation }` and `vno_create_project { presentation }`. No project setting, no data-folder migration. |
| D2 | **One page = one scene.** Pages are scenes; page count = scene count. No new beat type and no page entity. Page text = the scene's `narration` beats (and `line` beats as `Name: text`), localized through the edition. |
| D3 | **One illustration per page = the scene's `backgroundId`, made unique per scene.** In picture-book books `backgroundId` is `bg_<chapter>_<scene>` (e.g. `bg_ch01_s01`) from a new `pictureBookBackgroundId(sceneId)`; place/time no longer dedupe pictures. Outside picture books the existing place+time rule is untouched. |
| D4 | **No on-screen character assets, but keep reference sheets.** `deriveAssets` plans no `sprite_*`, no expression variants and no `cg_*` in picture books. `sheet_<char>` stays as an internal reference (never drawn in the book) because a children's book needs the same child on every page; page illustrations with cast use the edit engine with the sheets as refs (the existing CG-with-characters rule). |
| D5 | **Picture-book prompts.** `fallbackPrompt('background')`, `describeAsset` and `ensureFraming` branch on presentation: page prompt = style + place looks (people kept) + scene description (people kept) + `peopleClause` (names, looks, left-to-right) + time + "children's picture book illustration, full-bleed, no text, no lettering". `fallbackNegative` drops `person, people, character, creature, animal` for pages and keeps/extends the text bans. Both the fallback and the art-director path are covered so a model cannot reintroduce the empty-background rule. |
| D6 | **The player gets a second rendering mode.** `GameData.presentation` (missing = visual novel); body class `vno-picturebook`; a new page layer; the VN DOM stays but is hidden. Page turn crossfades; no typewriter; no chapter title card before page 1. |
| D7 | **Page navigation is page-based.** Click/tap on the illustration or caption → next page; `→`/Space/Enter → next; `←`/PageUp → previous; swipe left/right on touch; Esc → main menu. Last page → ending card ("The End", Start again / Main Menu). Choices and endings still work if a book has them. Quick Save on every page turn (so the menu's Load resumes); full Save/Load screens stay on VN projects only. |
| D8 | **Read-aloud reuses existing clips.** If a page's text beats have voice clips in the current edition, they play in order when the page appears; a small replay button repeats them. No new voice pipeline; a voice plan with no speaking characters yields the narrator only. |
| D9 | **Scriptorium format `kids-picture-book`** with `script: true` and a new `picture_book: true` flag, kind `juvenile-visual-novel`, ages 3–6, 150–900 words, 1 chapter, `read_aloud: true`, `research: false`. It is **only picked when the story fixes it** (same rule as `puzzles`/`screenplay`), never chosen at random by the editor-in-chief. Page grammar = the existing VN grammar (no parser change): `SCENE: <place>, <time>. <what the picture shows>`, then `ON SCREEN:` (who is in the picture), then 1–3 narration lines (the words under the picture). No speaker lines, no `CG:`/`INSERT:`/`---`. |
| D10 | **Prompt variants with `_pb` suffix**: `writer/draft_chapter_pb.md`, `writer/rewrite_chapter_pb.md`, `line-editor/review_pb.md`, `humanizer/humanize_chapter_pb.md`, `architect/outline_pb.md`; `promptTaskFor` prefers `_pb` over `_vn`. The pack compiler, catalog and Book Translator need **no change** (pack v2, `book.format = kids-picture-book`). |
| D11 | **Backward compatible.** Old `vn.json` files, old game-data.json files and every VN path keep working; the only structural change to VN output is the optional `presentation` field. |
| D12 | **Branches from `master`**: hub `HUB-17_picture-books`, VN Studio `VNO-47_picture-books`, Scriptorium `SCP-46_picture-books`. |

## Data model and API changes

- `src/shared/vn.ts` (VN Studio): `PRESENTATIONS = ['visual-novel','picture-book']`, `PICTURE_BOOK_FORMATS = ['kids-picture-book']`, `presentationForFormat(format)`, `isPictureBook(bookOrFormat)`, optional `presentation` on `vnBookSchema`; `storySummary` reports it.
- `src/engine/vn/ids.ts`: `pictureBookBackgroundId(sceneId)`; `backgroundIdFor(presentation, sceneId, placeKey, placeText, time)`.
- `src/engine/vn/story.ts`: create/apply ops honour presentation; `book.update` accepts `presentation`; changing presentation recomputes every scene's `backgroundId` and marks all backgrounds for re-prompt.
- `src/engine/vn/script.ts`, `pack.ts`, `import.ts`, `fixes.ts`: scene construction uses `backgroundIdFor(...)`; in picture-book mode `keepArt` (nearest-time background rescue) is skipped.
- `src/engine/assets/derive.ts`: picture-book asset plan (pages + cover + music + sfx/ambience + voiceRefs; sheets as references; no sprites/cgs); page prompt/negative helpers.
- `src/engine/vn/agents/art-director.ts`: `describeAsset`/`ensureFraming`/`planArt` picture-book branch.
- `src/engine/game/emit.ts`: `GameData.presentation`; `buildGameData` sets it. No per-page text field.
- `src/engine/game/player-runtime.ts`: HTML nodes, CSS, JS page mode (D6–D8).
- `src/engine/game/lint.ts`: picture-book checks — page with no illustration = error; page with no text = warning; sprite/CG entries or image cues in a picture book = warning; statistics say "pages".
- `docs/protocol.md`, `docs/mcp-guide.md`, `README.md`: `presentation`, page model, page commands/controls.
- `src/shared/ui-strings.ts`: Croatian for `Next`, `Previous`, `Page {} of {}`, `Read aloud` (English is the fallback).
- Scriptorium `src/shared/schemas.ts`: `picture_book` flag; `handlers.ts`: `_pb` prompt selection, picture-book note instead of the VN cue note, pb excluded from `formatsForKind` and from `adapt.ts`; `store/migrations.ts` + `dataFolder.ts`: `migratePictureBooks` appends the seed format entry; `seed/config/formats.md`: the format; five new `_pb` prompts; `yarn seed:hashes`; `docs/visual-novel.md` ("Picture books") and `docs/mcp.md`.

## Page layout (built game, 1920×1080 stage)

- Image band: 0–800 px, `object-fit: contain`, centred, `--vno-color-bg` matte; a missing image shows the build placeholder.
- Caption band: 800–1080 px, `--vno-color-bg`/`--vno-color-text`, text font `--vno-font-text`, 64 / 56 / 48 px by caption length (≤120 / ≤240 / more), line-height 1.45, max-width 1500 px, vertically centred; emphasis kept as HTML.
- Footer in the caption band: `‹` · "Page N of M" · `›`; a replay (🔊) button when the page has clips. Existing language switcher top-right; a Menu button top-left.
- Crossfade 300–400 ms (theme `fade`), no animation with `prefers-reduced-motion`.
- Nothing else from the VN stage is visible: sprites, CG layer, name box, textbox, quick menu, scene title.

## Work by repo

### VN Studio — VNO-47 (`VNO-47_picture-books`)
1. Schema/helpers (D1, D3), import from pack and legacy folder set presentation; `vno_create_project` + `book.update` accept it.
2. Asset plan and prompts (D4, D5): no sprites/cgs; unique page ids; page prompts and negatives; internal sheets.
3. Player (D6–D8): `generateIndexHtml` nodes, `generatePlayerCss` `.vno-picturebook` rules, `generatePlayerJs` `renderPage()/nextPage()/prevPage()/pageCaption()/playPageVoice()`, presentation branch in `playScene`/`advance`/`switchLanguage`/`refreshActiveScreens`/save-load/end card; fast-path guards so VN code paths are unchanged.
4. Lint (D9 checks).
5. UI: BookPage "Picture book" pill, ScenesTab page preview (image + caption, page counter, prev/next across scenes, sprite/slot/expression controls hidden, place/time/music/ambience/text and cast-list editing kept), LookTab note and hidden sprite-only settings, Scenes tab labelled "Pages".
6. Docs + MCP guide + README.
7. Tests: `ids`, `assets` derive/negative/prompt, `art-director` describe/ensureFraming, pack import fixture, `buildGameData`, player runtime (HTML/CSS/JS strings + fake-DOM flow: page 1 → page 2 → end card, language switch, save/load, no sprite `<img>`), lint, `story` ops, one fixture `tests/fixtures/books/picture-book/` (pack with 3 pages).
8. `yarn test`, `yarn typecheck`, `yarn lint`, `yarn build:engine` green; regression check on an existing VN fixture.

### Scriptorium — SCP-46 (`SCP-46_picture-books`)
1. `picture_book` flag; format entry (D9) with page-wise guidance; `_pb` prompts (writer, rewrite, line editor, humanizer, architect) and `promptTaskFor` selection; picture-book note in the draft/rewrite prompts; exclude pb from random format picking and from `adapt_book`.
2. Migration adding `kids-picture-book` to an existing `config/formats.md`; new prompts arrive as missing seed files; `yarn seed:hashes`.
3. Docs.
4. Tests: flag parsing and the seed entry; `_pb` selection; migration append + idempotence; a picture-book fixture publishes a pack with `book.format = kids-picture-book`, 12–16 scenes, no cue images/sounds, page captions only in the catalog; `get_script`/`get_vn_pack` on it; `yarn test`, `yarn typecheck`, `yarn lint`, `yarn build` green.

### Hub — HUB-17 (`HUB-17_picture-books`)
1. `.claude/tickets/HUB-17-picture-books/{plan,changelog}.md`; per-repo plan notes; HUB-17 row in `ROADMAP.md`.
2. `make-visual-novel` skill: a "Picture books" section (how to start one with `format: kids-picture-book` or a hand-written `vno_create_project` story, what is planned, page text rules, how to review pages, how to build and play, read-aloud, translation through the pack, the look-reference-only rule for the Peppa PDF).
3. `README.md` chain/tool table: picture books as an output of VN Studio + the Scriptorium format.
4. Live production and `runs/<slug>.md`; the user plays.

## Edge cases and failure modes

- A page with no text (cast only) → picture-only page, lint warning, player shows the image.
- A page with no illustration → build placeholder + lint error; the page still renders.
- Missing edition beat → primary text (existing `compileEditions` fallback).
- `image` cues, `puzzle` beats or sprites in a picture-book project → ignored by the player, lint warnings; the format prompts forbid them.
- Presentation changed on an existing project → background ids recomputed; old background assets become orphaned (kept), new pages need generation; assets are never deleted.
- Re-import keeps assets because `bg_ch01_s01` ids are deterministic.
- Very long caption → smaller step, no scrolling; RTL caption follows `dir` from the edition.
- Old `vn.json`/`game-data.json` without `presentation` → visual novel.
- Scriptorium started before SCP-46 is built → `add_story {format: "kids-picture-book"}` fails "unknown format"; rebuild and restart, or add the format entry by hand.
- Flow signed out / ComfyUI down → existing errors and autostart behaviour; prefer Flow for the production (free, ~50 s/image).
- Two characters in one illustration can merge (VNO-34): the prompt names each person with looks and a side; regenerate a bad page with another seed.

## Tests and verification

- Unit/integration per repo as listed above; VN Studio full suite, typecheck, lint; Scriptorium full suite, typecheck, lint.
- Static check that a VN fixture's game-data differs only by the new optional field.
- Live: `hub.ps1 check`; `add_story {format: kids-picture-book}`; `wait_for_book`; `get_vn_pack` (format, scenes); `vno_import`; `vno_update_settings` (art provider Flow, music, voice hr Supertonic); `vno_run_pipeline`; `vno_build` + `vno_lint` clean; open `~\VisualNovels\projects\<slug>\game\index.html`; page through all pages, switch language, reload the page and press Load.
- The user's verdict is the acceptance; it is written in the run log.

## Prerequisites and risks

- **The shell was broken at planning time**: `pwsh` failed with `SetNamedSecurityInfoW failed (Win32 5): grantWrite(C:\projects\Personal\creative-hub)`. Fixed before implementation with the `diagnose-windows-sandbox-acl` skill (grant verified on 2026-10-25; recovery files in `C:\projects\Personal\creative-hub-acl-recovery`).
- Services: vn-studio (pipeline), flow-music-mcp signed in **or** ComfyUI free, VibeTTS MCP for narration; Scriptorium is started only with the user's approval (it resumes the factory).
- The picture-book player is new code inside a 2,300-line generated JS string: escape backticks/`${}` carefully and cover it with the fake-DOM tests.
- No visual regression suite: the user must look at the pages.

## Out of scope

PDF/print export, EPUB picture book, speech bubbles/comic panels, OCR or reuse of the Peppa PDF's text/characters, Book Translator changes, puzzles/quiz inside picture books, Android.

## Assumptions

- The Peppa PDF is a look reference only (user-confirmed).
- Output is the HTML5 page-turn book; no PDF (user-confirmed).
- Scriptorium writes picture books end to end (user-confirmed).
- Picture books are linear, one chapter, Croatian first (English edition optional via the pack catalog).
- Reference character sheets are acceptable because they are internal and never shown in the book; if the user wants zero character assets, that is a one-line follow-up ticket (art plan without sheets, weaker likeness consistency).

## Delivered (2026-10-25)

Status: implemented and verified on hub `HUB-17_picture-books`, VN Studio `VNO-47_picture-books`, Scriptorium `SCP-46_picture-books`; **committed and pushed** (`d768077`, `a67c831`, and the hub commit). Two live productions built and opened: "The Bell and the Bicycle" (watercolour) and "The Snail and the Salad" (flat cartoon); the user's play verdicts are pending. Details in `changelog.md` next to this plan and in the two run logs.

- D1-D3 done: `presentation`, `presentationForFormat`/`presentationOf`/`isPictureBook`, `bg_ch01_s01` page ids, import/create/`book.update`, VN behaviour unchanged.
- D4-D5 done: one page image per scene, internal `sheet_*` only, no sprites/CGs, page prompts keep/named people, picture-book negatives, art-director cannot reintroduce the empty-background rule (11 new VN Studio tests).
- D6-D8 done: `GameData.presentation`, page layer (0-800 illustration, 800-1080 caption, counter, prev/next, click/tap, arrows, swipe, Esc, language re-render, quick save per turn + Load, read-aloud, localized end card); fake-DOM tests.
- D9-D10 done: `kids-picture-book` format + `picture_book` flag, `_pb` prompts, never picked at random, `adapt_book` refusal, start migration, 703 Scriptorium tests.
- D11 done: old `vn.json`/game-data.json parse, all VN suites green.
- D12 done: branches from `master` as named above.

Live verification: two productions, each 12 pages, en + hr, built with 0 placeholders and lint clean. *The Bell and the Bicycle*: pipeline run 2 (39 jobs, 0 failed), 12 page images, 4 reference sheets, a cover, one chiptune track, 34 narration clips per language, Croatian catalogue `runs/the-bell-and-the-bicycle/vn-text-hr.json`. *The Snail and the Salad*: 30 jobs, 0 failed, 12 page images, 3 sheets, a cover, one chiptune track, 37 clips per language, Croatian catalogue `runs/the-snail-and-the-salad/vn-text-hr.json`. Games at `C:\Users\Infplane\VisualNovels\projects\<slug>\game\index.html`.

Two live bugs were found and fixed in SCP-46: `castOf` now splits `ON SCREEN:` on commas and semicolons (the writer used semicolons, so every page imported with only Lana in the first run), and `settleScenePlaces` keeps a comma-rich picture sentence after the SCENE line's first full stop. Other deviations: Croatian catalogue translated by hand (no Book Translator run), picture-book Load resumes the quick save directly, `.gitattributes` fixture EOL rule, and the hub `ELECTRON_RUN_AS_NODE` launcher fix.
