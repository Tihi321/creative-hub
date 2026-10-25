# HUB-17 — changelog

## 2026-10-25 — second live production: *The Snail and the Salad*

On request, a second picture book was written and built end to end with the same code (no new code changes): *The Snail and the Salad*, bright flat-cartoon style. Scriptorium published it on the first round (12 pages, 616 words, 8.79/10, all eight reviewers pass); VN Studio imported it as `presentation: "picture-book"`, generated 12 page illustrations + 3 sheets + a cover with Flow, one chiptune track, 37 narration clips per language (en + hr), and built with **0 placeholders, 0 warnings**, lint clean (12 pages). The Croatian edition is `runs/the-snail-and-the-salad/vn-text-hr.json` (36/36 keys). Opened in the browser for the user; play verdict pending.

- No new code: it exercised the same VNO-47/SCP-46 code, including the two live fixes (the writer's comma-rich SCENE lines survived on disk, and the cast parsed correctly).
- Artifacts: `runs/the-snail-and-the-salad.md`, `runs/the-snail-and-the-salad/vn-text-hr.json`.
- VN Studio and Scriptorium branches were committed and pushed after this production (hashes below); the hub branch carries this entry.

## 2026-10-25 — Children's picture books (VN Studio VNO-47, Scriptorium SCP-46)

Picture books are now a first-class output: Scriptorium writes format `kids-picture-book` (one page per scene, no dialogue or cue lines), publishes the same v2 VN pack, and VN Studio imports it as `presentation: "picture-book"`, plans **one illustration per scene** with the cast drawn in, and builds an HTML5 page-turn book with the text below the picture. A live Croatian production was built and opened in the browser; the user's play verdict is pending.

Branches (from `master`, committed and pushed): hub `HUB-17_picture-books`, VN Studio `VNO-47_picture-books` (`d768077`), Scriptorium `SCP-46_picture-books` (`a67c831`).

### Hub — `HUB-17_picture-books`
- `.claude/tickets/HUB-17-picture-books/plan.md`, this changelog; `ROADMAP.md` HUB-17 row.
- `README.md`: picture books in the chain diagram, the Scriptorium and VN Studio rows, the pack paragraph and the docs list.
- `.claude/skills/make-visual-novel/SKILL.md`: new "Picture books (slikovnice)" section (start, import, settings/art review, build/play, translation, "a PDF is not an input"), plus picture-book notes in the format list, the asset review and the play step.
- `scripts/hub.ps1`: `Start-Detached` now removes `ELECTRON_RUN_AS_NODE` for Electron apps. This agent session exports it, so `hub.ps1 start scriptorium` was running `out/main/index.js` under Node and crashing (`electron.protocol` undefined). Verified: Scriptorium starts and answers MCP.
- `runs/the-bell-and-the-bicycle.md`, `runs/the-bell-and-the-bicycle/vn-text-hr.json` (the Croatian catalogue).

### VN Studio — `VNO-47_picture-books` (28 files changed)
- **Data/presentation:** `src/shared/vn.ts` (`PRESENTATIONS`, `PICTURE_BOOK_FORMATS`, `presentationForFormat`, `presentationOf`, `isPictureBook`, optional `presentation` on `vnBookSchema`); `src/engine/vn/ids.ts` (`pictureBookBackgroundId` `bg_ch01_s01`, `backgroundIdFor`); routed through `script.ts`, `pack.ts`, `import.ts`, `story.ts`, `fixes.ts` (the nearest-time art rescue is skipped in a picture book). Imports store the presentation; `book.update`/`vno_create_project` accept it; changing it recomputes every page id; `storySummary` reports it.
- **Assets/prompts:** `src/shared/…` + `src/engine/assets/derive.ts` (`charactersOnPage`, one page image per scene with the cast's sheets as edit-engine refs, no sprites/CGs, `PAGE_FRAMING`, page prompts keep people, picture-book negatives no longer ban people/animals); `src/engine/assets/generate.ts` (a background with refs is generated from them); `src/engine/vn/agents/art-director.ts` (`describeAsset`/`ensureFraming`/`mergeNegative`/`planArt` cannot reintroduce the empty-background rule).
- **Build/player:** `src/engine/game/emit.ts` (`GameData.presentation`, no sprites/CGs for a picture book); `build.ts`/`images.ts` (pages copied `fit: inside`, never cropped); `src/engine/game/player-runtime.ts` (~544 lines: page layer 0–800 illustration + 800–1080 caption, counter, prev/next, click/tap, arrow keys, swipe, Esc, language re-render, quick save on each page turn + Load resumes the page, read-aloud of the page's clips in order, localized end card; every VN path guarded by `presentation === 'picture-book'`).
- **Lint/MCP/docs/UI:** `src/engine/game/lint.ts` + `src/engine/vn/handlers.ts` (page without illustration = error; page without text, leftover sprites/CGs/image cues = warnings; "pages" statistics); `src/engine/mcp/server.ts`, `src/engine/mcp/tools-story.ts`, `docs/protocol.md`, `docs/mcp-guide.md`, `README.md`; `src/shared/ui-strings.ts` (Croatian Next/Previous/Page {} of {}/Read aloud); `BookPage.tsx`, `ScenesTab.tsx` (page preview), `LookTab.tsx`.
- **Tests:** new `tests/picture-book.test.ts` (11), `tests/fixtures/books/picture-book/` (3-page v2 pack), additions to `vn-ids`, `assets-generate` and the fake-DOM flow in `renpy-template.test.ts` (1087 tests in 79 files).

### Scriptorium — `SCP-46_picture-books` (24 files changed)
- **Format:** `src/shared/schemas.ts` (`picture_book` flag); `seed/config/formats.md` (`kids-picture-book`: script, 3–6, 150–900 words, 1 chapter, read-aloud, page-wise guidance).
- **Pipeline:** `handlers.ts` (`_pb` prompt selection before `_vn`, `PICTURE_BOOK_NOTE` for reviewers, `formatsForKind` never picks a picture book, start override for a story that fixes it); `scriptPlaces.ts` (`PICTURE_BOOK_NOTE`); `prompts.ts` (`_pb` falls back to the plain prompt, never `_vn`); `adapt.ts` + `engine.ts` (`adapt_book` refuses a picture-book format); five `_pb` prompts (`architect/outline_pb`, `writer/draft_chapter_pb`, `writer/rewrite_chapter_pb`, `line-editor/review_pb`, `humanizer/humanize_chapter_pb`); `seedHistory.ts` regenerated; `migrations.ts` + `dataFolder.ts` (`migratePictureBooks`, idempotent, appends the seed entry to an existing `config/formats.md`).
- **Docs:** `docs/visual-novel.md` "Picture books", `docs/mcp.md` (add_story format, adapt refusal).
- **Live bug fixes (found by the production):** `src/engine/publish/script.ts` `castOf` now splits people on top-level commas **and semicolons** (`ON SCREEN: Lana (yellow dress); Mama (apron, bun)` used to become one entry); `src/engine/pipeline/scriptPlaces.ts` `settleScenePlaces` splits a `SCENE:` line at its first full stop **before** place/time parsing, so a comma-rich picture sentence survives; the picture-book guidance and writer prompts now say the people are comma-separated (a semicolon also works). Tests in `script.test.ts`, `rewrites.test.ts`, `trailingCue.test.ts`, `pictureBook.test.ts`.
- **Tests:** `tests/pictureBook.test.ts` (13), `tests/fixtures/vn-pack/picture-book/` (14 pages), additions to `vnPack.test.ts` and `mcp.test.ts` (pack read-back, factory start, adaptation refusal, migration LF/CRLF/idempotence).

### Deviations from the plan
- **Croatian edition without Book Translator.** The pack catalogue was translated by hand and added with `vno_add_edition` (a bare `vn-text` catalogue). The translation seam itself was verified live in HUB-16; this run proves the edition path, not a new translator run.
- **Reference sheets kept** (as D4 decided): they are internal, not shown in the book; the first live plan proved why — the page illustrations need them for likeness.
- **Picture-book Load** resumes the quick save directly (no save screen); VN save/load is unchanged.
- **Build omits sprites and CGs** for a picture book (none are planned) and the legacy `.rpy` files are still written, unused.
- **`.gitattributes`** in Scriptorium: `tests/fixtures/** text eol=lf` (the canonical pack tests compare LF output byte for byte; this checkout is `core.autocrlf=true`). The six existing fixture JSONs are content-identical.
- **Hub `ELECTRON_RUN_AS_NODE`** fix, as above.
- **Production restart:** run 1 was stopped after the cast bug; the project was deleted and re-imported from the rebuilt pack (three free Flow page images discarded).

### Verification
- **VN Studio:** `yarn test` 79 files / **1087 tests passed** (Lead re-run on an unloaded machine, after one timeout when both repos' suites ran concurrently; the isolated file passed 14/14), `yarn typecheck` clean, `yarn lint` clean, `yarn build:engine` exit 0.
- **Scriptorium:** `yarn test` **703 tests** (54 files / 702 + recovery 1; teammate run and Lead re-run exit 0), `yarn typecheck` clean, `yarn lint` clean, `yarn build` exit 0.
- **Live (VN Studio pipeline run 2, 16:25–16:58Z):** analyse/art/music/generate/voice/stage/build/lint all done, 39 jobs 0 failed; 12 page images + 4 sheets + cover + 1 chiptune track; 34 voice clips per language (en, hr); build **0 placeholders, 0 warnings**, 1 translation (hr); lint **clean (12 pages)**.
- **Game opened:** `C:\Users\Infplane\VisualNovels\projects\the-bell-and-the-bicycle\game\index.html` (redirect to `game/game/index.html`), presentation `picture-book`, editions en + hr, `bgPath` per page.
- **Not run:** the user's play/review verdict; the game was not played by the Lead in a real browser beyond opening it.

### Follow-ups and known limitations
- The user plays both books (pages, Croatian switch, read-aloud, Load on the last page) and their verdict goes into the two run logs.
- Page s11 of the first book has four characters (Mama, Lana, Tomo, Kiki); the stage cue schema has three slots, so Kiki is not in the cue's slot list (she is in the art). Harmless for a picture book.
- The generated page filenames follow the existing `bg <id>.webp` convention (a space, not an underscore); the build references them consistently.
- The Scriptorium factory was paused and limited to one book for both runs; `config/factory.md` was restored (`paused: false`, `max_books_in_progress: 10`). The five new `_pb` prompts are committed in SCP-46.
- Out of scope as planned: PDF/print export, EPUB picture book, puzzles/quiz in picture books, Book Translator changes, Android.
- Commit status: **committed and pushed** — VN Studio `VNO-47_picture-books` (`d768077`), Scriptorium `SCP-46_picture-books` (`a67c831`), hub `HUB-17_picture-books` (this commit). PRs were not opened (not asked).
