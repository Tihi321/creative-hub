# HUB-25 changelog

## 2026-11-02 - HUB-25 implementation run: VN Studio book export (EPUB + PDF, gamebook for choice stories) and Scriptorium text-only gamebook (EPUB + PDF)

Everything is uncommitted. Each repo's working tree holds all its tickets stacked, and the tree is checked out on the last branch. The branches all point at master's commit, because nothing is committed.

### PDF spike (VNO-54 step 0)
- **Throwaway:** `visual-novels-orchestrator/.claude/temp/pdf-spike/spike.mjs`.
- **Libraries tried:** pdfkit 0.20.2, and pdf-lib 1.17.1 with @pdf-lib/fontkit.
- **Font:** Lora (SIL OFL), from `themes/parchment/fonts`, which is already in the VN Studio repo and already shipped.
- **Result:** both libraries pass in PdfCraft.
  - `text_extract` returns "Čovjek šapće: žaba, đak, ćevap, ŠĐŽČĆ" intact.
  - `link_list` shows the internal link going to page 2.
  - Both run headless in plain node.
- **Choice: pdfkit.** It has automatic wrapping and page flow (sections run up to 2,500 words), named destinations through `goTo`, an outline, JPEG embedding, font subsetting, and Title and Lang metadata. pdf-lib would need all of these written by hand.
- **Gotchas found:**
  - With `continued`, a link leaks onto the next fragment unless it is ended with `goTo: null`.
  - `outline.addItem` targets the current page.
  - Centred `continued` text overprints (found later, on real output).
- The full record is in `creative-hub/.claude/temp/hub25/spike-result.md`, copied into `VNO-54-pdf-export/plan.md`.

### visual-novels-orchestrator
- **VNO-52** (`VNO-52_export-model`):
  - New `src/engine/export/sections.ts` holds the shared algorithm (verbatim core) and the stored map in the sibling `projects/<slug>/export.json`: reuse, stale detection, `renumber`.
  - New `src/engine/export/phrases.ts` (en/hr), `validate.ts` (missing target, unreachable chapter, ending with choices, missing text) and `model.ts` (`ExportBook` for the gamebook, linear and picture-book modes, with warnings for dropped content).
  - New `src/engine/mcp/tools-export.ts` adds `vno_export_book`, registered in `src/engine/mcp/tools.ts`, with a sentence in the `server.ts` INSTRUCTIONS and an "Export a book" section in `docs/mcp-guide.md`.
  - `tests/export-model.test.ts`, the ROADMAP entry, and the ticket plan.
- **VNO-53** (`VNO-53_epub-export`):
  - New `src/engine/export/images.ts`: colour JPEG at about 1000 px, a grey option, and the cover with a title band.
  - New `src/engine/export/epub.ts` (`buildEpub`, `writeEpubFile`): mimetype stored first, numbers-only nav for gamebooks, `section-NNN.xhtml#sN` links, and a warning above 40 MB.
  - `format:'epub'` is wired into the tool.
  - `scripts/export-probe.ts` writes the Kindle probe: `yarn tsx scripts/export-probe.ts [out] [en|hr]`.
  - `tests/export-epub.test.ts`; `jszip` added; docs, ROADMAP and plan.
- **VNO-54** (`VNO-54_pdf-export`):
  - New `src/engine/export/pdf.ts` (`buildPdf`, `writePdfFile`): A5, cover, big section number, picture, text, the label linked to `s<N>`, footer "section N" / "odlomak N", one bookmark "Start: section 1".
  - `format:'pdf'` is wired into the tool.
  - `tests/export-pdf.test.ts`; `pdfkit` and `@types/pdfkit` added; the font licence note in `docs/mcp-guide.md`; ROADMAP and plan.
  - **Orchestrator fixes after the PdfCraft check:**
    - Footers were off by one page, because pdfkit's first page fires no `pageAdded`.
    - The centred restart line overprinted.

### scriptorium
- **SCP-49** (`SCP-49_gamebook-epub`):
  - New `src/engine/publish/sections.ts` holds the same verbatim core, `planSections` with the sibling `books/<slug>/gamebook.json`, and `gamebookPhrases`.
  - `epub.ts` gets the `gamebook` option. With it absent the output is unchanged, which a hash test checks over the unzipped entries.
  - `xhtml.ts` gets `gamebookChoicesHtml` and `sectionFile`; `choicesHtml` is untouched.
  - `pipeline/books.ts` gets the `buildEpubFile(slug, {gamebook})` option, which writes `out/<slug>-gamebook.epub`.
  - `engine.ts` and `shared/protocol.ts` get the `buildGamebook` command and `sendToKindle {gamebook}`.
  - `tests/gamebook.test.ts`, the `docs/design.md` row, ROADMAP and plan.
  - **Orchestrator alignment with VN Studio:** the link covers "section N" (not the bare number), and the Croatian separator is ", ".
- **SCP-50** (`SCP-50_gamebook-pdf`):
  - New `src/engine/publish/pdf.ts` (pdfkit, Lora).
  - `BookStore.buildGamebookPdf` writes `out/<slug>-gamebook.pdf`, and the `buildGamebookPdf` engine command calls it.
  - The `resources/fonts/` folder holds Lora and its OFL licence, and is added to `files` in `electron-builder.config.cjs`; the font is credited in `ATTRIBUTION.md`.
  - `tests/gamebook-pdf.test.ts`, the `docs/design.md` row, ROADMAP and plan.
  - **Orchestrator fixes:**
    - The centred restart line.
    - The footer now reads "section N" / "odlomak N", as in VN Studio.

### Deviations
- **No commits**, as the brief said. The per-ticket branches are stacked and the tree is on the last one. To land them, commit each ticket's files in turn on its branch: VNO-52, then cut VNO-53 from it, and so on. `ROADMAP.md`, `docs/mcp-guide.md`, `package.json`, `yarn.lock` and `tools-export.ts` (VN Studio), and `ROADMAP.md`, `docs/design.md`, `books.ts`, `engine.ts` and `protocol.ts` (Scriptorium) carry hunks from more than one ticket.
- **Order:** SCP-49 ran in parallel with VNO-52. Both copied one canonical core that the orchestrator had first checked against the golden vector. The spike ran before SCP-50, as the plan says. VNO-55 stays deferred.
- **TypeScript:** both cores add `!` on the swap line because of `noUncheckedIndexedAccess`. The algorithm is unchanged, and the first 54 lines of the two files are byte-identical.
- **Croatian ending wording** ("Kraj." / "Idi na odlomak 1 za novi početak.") is inferred. The user gave only "idi na odlomak N".
- **Not added:**
  - `vncli export`
  - a UI button
  - an MCP tool in Scriptorium
  - the PDF as a Kindle attachment (`kindle.ts` hardcodes `.epub`)
  - the hub ROADMAP row and skill step, which wait for the merge, as the plan says
- **Duplicate run:** a harness signal said the first background workers had stopped while they were still running, so a second worker ran VNO-53 and SCP-50 at the same time for a few minutes. The final state was reviewed and verified as a whole.

### Verification
- **VN Studio:**
  - `yarn typecheck`: clean.
  - `yarn lint`: 1 error, the pre-existing `scripts/shot-game.mjs:111` no-empty on master.
  - `yarn test`: 86 files and 1140 tests pass on the third full run. The two earlier full runs each had one unrelated 15 s timeout (`vn-pipeline`, then `puzzles`), and both pass alone.
- **Scriptorium:**
  - `yarn typecheck`: clean.
  - `yarn lint`: 5249 errors, all from the untracked local `release/win-unpacked` build output.
  - `eslint . --ignore-pattern "release/**"`: clean.
  - `yarn test`: 57 files and 717 tests, and recovery 1 of 1.
- **Golden vector:** the same values are asserted in both repos, and the orchestrator recomputed them independently.
- **PdfCraft on real output (copies of projects):**
  - VN clockless-god-2 en: 120 pages, 21 links, one bookmark, correct footers.
  - VN snail hr: 13 pages, diacritics intact.
  - Scriptorium clockless-god-2 hr: 95 pages, 21 links, "Početak: odlomak 1", "idi na odlomak" found 19 times, diacritics intact.
- **V1:** the VN PDF reused `export.json` byte-identical to the one the EPUB wrote. The 16 PDF destinations equal the map.
- **Not run:**
  - epubcheck: not installed.
  - Any EPUB reader or the Kindle.
  - The MCP tool through a running server (the handler was called directly).
  - Packaged builds finding the fonts.
  - Scriptorium in the app (never started).

### Follow-ups
- Kindle live check: steps 1 to 5 in plan.md, starting with the probe `visual-novels-orchestrator/.claude/temp/kindle-probe/probe-gamebook.epub`.
- Hub ROADMAP row and skill step after the merge.
- VNO-55 if the probe passes and the user wants it.
- The PDF as a Kindle attachment in Scriptorium.
- The ending text in clockless-god-2's data reads "sad: Dec loses his day..." and is printed as given: a data question for the user.

Commit status: **uncommitted** in both repos.

## Polish: Scriptorium UI entry (2026-11-02)

The checker found the engine commands `buildGamebook`, `buildGamebookPdf` and `sendToKindle {gamebook}` had no UI, so the user could not export a gamebook and live check 4a was blocked.

- `src/shared/protocol.ts`: `BookSummary.gamebook?: boolean`, set when the book has branch data.
- `src/engine/summary.ts`: sets `gamebook: true` for a non-article book with `books.branchMap(slug)`.
- `src/renderer/ui/BookCard.tsx`: for `!article && book.gamebook`, three buttons next to Send to Kindle: "Gamebook EPUB" (`buildGamebook`), "Gamebook PDF" (`buildGamebookPdf`) and "Send gamebook to Kindle" (`sendToKindle` with `gamebook: true`, same sending state and status). The default buttons are unchanged. Test ids: `card-gamebook-epub`, `card-gamebook-pdf`, `card-kindle-gamebook`.
- No test added: the only BookCard tests are Playwright specs in the demo, and the demo has no branching book. A spec would need a demo fixture plus a browser run, which was out of scope.
- Checks: `yarn typecheck` clean; `eslint . --ignore-pattern "release/**"` clean; `yarn test` 57 files and 717 tests pass, recovery 1 of 1.
- Not done: the engine builds the file only when the user clicks, and "Send gamebook to Kindle" needs the EPUB built first (no auto-build, no disabled state when the file is missing). Not started in the app. Still uncommitted.

## Status list

- DONE: SCP-49 gamebook EPUB (engine, protocol, tests).
- DONE: SCP-50 gamebook PDF in Scriptorium (engine, protocol, tests) and the VN Studio PDF.
- DONE: Scriptorium UI entry for gamebook EPUB, PDF and Send to Kindle (polish above).
- DONE: typecheck, lint (with `release/**` ignored) and tests in both repos, as listed above.
- NOT DONE: the PDF as a Kindle attachment in Scriptorium (follow-up). A BookCard test for the new buttons (reason above).
- UNTESTED: the new buttons in the real app (Scriptorium never started); the Kindle live check (plan steps 1 to 5, including 4a); epubcheck; any EPUB reader or the Kindle; the MCP tool through a running server; packaged builds finding the fonts; the user playing or reading the output.

## Merged 2026-11-02

- visual-novels-orchestrator master `525e7b2` (VNO-52, VNO-53, VNO-54).
- scriptorium master `bb4c094` (SCP-49, SCP-50).
- Hub step done: `make-visual-novel` skill step 8 (book export). Kindle live check by the user is still pending.
