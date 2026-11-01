# HUB-25 research: Kindle and PDF book export

## Question
Can the user export choice books (numbered sections, "turn to 56") and linear picture/illustrated books for Kindle and as PDF; what exists, where does the data live, who should own it, which formats and libraries?

## Answer
- HUB-25 is free (ROADMAP.md rows end at HUB-23; HUB-24 exists only as a ticket folder). **confirmed**
- **Partly exists.** Scriptorium already builds an EPUB 3 per book and mails it to a Kindle by SMTP. Choice stories get hyperlinked chapters ("What do you choose?" list, "The End" plus link back). **confirmed**
- **Missing:** (a) PDF anywhere; (b) gamebook-style numbered sections ("turn to 56"), because the current EPUB links by chapter and has no section numbers; (c) any images in the EPUB except the cover and a decorative ornament; (d) a way to export VN Studio books, which hold the pictures and the translations; (e) fixed-layout picture books. **confirmed** (no pdf writer in any of the three repos' deps).
- **Recommended owner: VN Studio** for the numbered-section, picture and PDF export (it has the images, per-language editions, `sharp`). Reuse Scriptorium's EPUB code as the pattern, not a dependency. Scriptorium keeps its prose EPUB and Send to Kindle. **inferred**
- WebSearch was not available in this session, so the Amazon guidance in section 4 is from my own knowledge, **unverified**. A ticket must re-check it first.

## Path through the code

### 1. Existing exports
- creative-hub: no export feature. `.claude/skills/make-visual-novel/SKILL.md:107` only covers the Scriptorium EPUB as input to Book Translator; `:103` says a PDF is never an input. `services.json` has no export entry. **confirmed**
- Scriptorium (`C:\projects\Personal\scriptorium`):
  - `src/engine/publish/epub.ts` `buildEpub` (JSZip): EPUB 3, nav, cover, title page, one xhtml per chapter, CSS. `EpubChapter.choices {text,to}` and `.ending` exist (lines 6-22).
  - `src/engine/publish/xhtml.ts:226` `choicesHtml`: links `chapter-NN.xhtml`; ending links back to chapter 1.
  - `src/engine/publish/kindle.ts`: nodemailer sends the `.epub` to the Kindle address (SMTP settings). Not exposed over MCP (`docs/mcp.md:3,119`).
  - `src/engine/pipeline/books.ts:349` `choiceLinks` maps outline chapter numbers to positions.
  - Tests that touch it: `tests/art.test.ts`, `tests/pipeline.test.ts`, `tests/rewrites.test.ts`.
  - Deps: jszip, nodemailer; no PDF library. **confirmed**
- Book Translator: reads EPUB/DOCX/PDF (`pdfjs-dist`), exports translated EPUB (`src/engine/publish/epub.ts`). No choices or pictures. **confirmed** (file list; I did not read its code line by line)
- VN Studio (`visual-novels-orchestrator`): builds a web player and an Android build (`docs/android.md`); no EPUB/PDF code; deps are `sharp`, `zod`, `yaml`, no zip or PDF library. Its ROADMAP has no export item. **confirmed**

### 2. Data
- Scriptorium books: `~/Scriptorium/books/<slug>/`, chapters as markdown, `outline.md` frontmatter holds the branch map (`books.ts:257`). Formats `gamebook`, `choice-visual-novel`, `kids-choice-book`, `kids-visual-story`, `kids-choice-visual-story` exist (`docs/design.md:767`); `picture_book: true` flag in `src/shared/schemas.ts`. No illustrations are made in Scriptorium. **confirmed**
- Branch rules (`src/engine/pipeline/branches.ts`): at most 3 choices (`MAX_CHOICES`); a choice must lead to a **later** chapter (`to > n`, bad ones dropped), a chapter without choices is an ending, every chapter reachable from chapter 1, at least 2 endings. So the graph is a DAG: **no loops, no dead links**. **confirmed**
- VN Studio: `~/VisualNovels/projects/<slug>/vn.json` (`src/shared/vn.ts`): `kind: linear|choice`, `presentation: visual-novel|picture-book`, `chapters[] {n, title, choices[{text,to}], ending, scenes[]}`, scene `{id, backgroundId, description, beats[]}`, beats are `line` / `narration` / `cast` / `puzzle`. Text lives in `editions/<lang>` (`Edition`: `beats` id->text, `choiceTexts` keyed `"<ch>:<idx>"`, `endings`, `chapterTitles`, `characterNames`). A picture book = one scene per page, one illustration per page = `backgroundId` (`bg_<ch>_<scene>`), caption = narration beats (`docs/protocol.md:71-75`). **confirmed**
- Pictures: `projects/<slug>/assets/<assetId>/` (versioned folders); `buildGame` takes `resolveAsset(id)` for the selected version (`src/engine/game/build.ts:24-35`); `sharp` resizes (`game/images.ts`). A visual novel's sprites are separate from the background; the export would use background (+ CG) only. **confirmed**
- Puzzles in puzzle VNs cannot be printed; export should skip them with a warning. **inferred**

## 3. Owner
- VN Studio: images, editions (so Croatian/English/German exports come free), picture-book presentation, linear and choice kinds. It already imports Scriptorium packs (VNO-46). One export code path covers both book types.
- Scriptorium: only the text-only gamebook (no pictures). Optional: add numbered sections to its EPUB. Not the main path.
- Book Translator: no.
- Hub: only the doc/skill step ("export for Kindle") and a live check. **inferred**

## 4. Kindle format (UNVERIFIED, WebSearch unavailable; re-check before building)
- Amazon's Send to Kindle takes EPUB (it converts), and has done since 2022; MOBI is no longer accepted. KDP prefers EPUB or KPF. Internal hyperlinks between xhtml files and via a nav/TOC work in reflowable EPUB. Images work (JPEG/PNG, keep each under a few MB).
- Picture books: reflowable EPUB with one image per page works but pages flow with the text. A true page-per-picture book needs **fixed-layout EPUB** (`rendition:layout pre-paginated`, viewport meta per page) or Kindle Create's KPF "Kids book" mode. Fixed layout works on Kindle apps and Fire; on e-ink Kindles support is partial. Linear VN = reflowable EPUB with images is the safe default.
- Numbered gamebook on a Kindle: each section is an anchor, each choice an `<a href="#s56">` or a link to a per-section file. Kindle's "Back" navigates after a jump. **inferred** from general EPUB behaviour.
- Decision for the plan: target **EPUB 3 reflowable** (choice books and linear VNs), fixed-layout as an optional flag for picture books; **no KPF** (needs Amazon's closed tools). Check the user's Kindle model.

## 5. Libraries
- EPUB: JSZip (already in Scriptorium and Book Translator; add to VN Studio, or copy the small `buildEpub` pattern). No new EPUB package needed.
- PDF options in VN Studio (no PDF lib today):
  - Electron `webContents.printToPDF`: the app already ships Electron 44, so no new dependency and CSS page layout, but the engine runs headless in plain node (`start: out/engine/index.js --mcp-only`, `services.json`), so it would need an Electron helper or the main process. Risk.
  - `pdf-lib` or `pdfkit`: pure node, works headless, manual layout; needs a font for Croatian diacritics (embedding a TTF; VN Studio already has `fonts/`). Links in PDF: pdf-lib can add link annotations, so "turn to 56" can be a clickable jump.
  - Recommendation: **pdfkit or pdf-lib** for headless; decide in the ticket after a 1-page spike with a Croatian string. **inferred**
- Images: `sharp` (present) to convert webp to JPEG and resize to ~1200 px wide.

## 6. Gamebook numbering
- Chapters are the nodes; the sections should be one per chapter (or one per scene if a chapter is long; start with the chapter).
- **Shuffle vs order:** a true gamebook shuffles so the reader cannot read ahead. Since choices only go forward, an in-order export lets the reader guess "next number = next story". Use a **deterministic shuffle** (seeded from the slug) with section 1 fixed as the start; offer `order: shuffled|in-order`. The same numbers must be used in EPUB and PDF (a stored `sections` map is the single source). **inferred** design.
- **Validation before export (cheap, must have):** every `choice.to` is an existing chapter; every chapter reached from 1; a section with no choices is an ending ("The End", plus "turn to 1 to play again"); no duplicates. Scriptorium's `checkBranches` and VN Studio's import warnings (`vn.ts` `warnings`) already guarantee most of this; the exporter should still check and fail loudly.
- Loops: not possible now (forward-only). If a future book allows them, no change is needed except not assuming a DAG when checking reachability.
- Merge points (several choices to one chapter) are fine: the section shows once; its number is cited from every source.
- Reading text, not "choice 1/2": print "If you choose to open the door, turn to 56." Use the choice text from the edition.
- PDF page numbers: a section number is not a page number. Easiest: PDF = one section per page-start (or put the section number in bold at each section start and a page footer); links are clickable jumps; also print "turn to section 56", not "page 56". Say so in the ticket. **inferred**

## Reproduction
Not a bug. Verified by reading only; no service started, nothing run.

## What the plan needs
- Files: VN Studio `src/engine/` new `export/` module (section map, epub writer, pdf writer), MCP tool `export_book {slug, format: epub|pdf, lang, mode: gamebook|linear, order}` in `src/engine/mcp/` + protocol message + `docs/mcp-guide.md`; UI button optional.
- Tests (vitest, existing style; only these matter):
  1. Section map: every choice target maps to a number, start is 1, endings have none, shuffle is deterministic and a bijection.
  2. EPUB output (unzip in the test): every `href="#sN"`/file link resolves; images listed in the manifest exist; mimetype first and stored.
  3. PDF: opens, page count > 0, contains "turn to" with a number that exists (extract text or check link annotations); one Croatian-diacritics case.
  4. A broken choice target fails the export with a clear message.
  No UI tests, no snapshot of whole files.
- Verification outside tests: open the EPUB in Kindle Previewer or send it to the user's Kindle; the user plays it (hub rule: done only when the user has read it).

## Risks
- Kindle behaviour is unverified (no web access); fixed layout on e-ink; image size limits.
- Headless engine cannot use Electron print; picking the PDF library decides the layout effort.
- Fonts and diacritics (Croatian) in PDF; RTL languages (the VN has `rtlLanguages`) are hard in pdfkit.
- Section numbers must be identical across EPUB and PDF and reproducible after a re-export (seeded shuffle; same seed stored).
- A VN with sprites and dialogue is not a book; "linear VN" export should be text + one background per scene, and say which beats are dropped (cast, puzzle, cues).
- Voice and music are lost; fine.
- The Scriptorium EPUB link is by chapter file, which is fine for Kindle; do not break it.
- Rights: only the user's own books (PDF is not an input rule stays).

## Open questions
1. Which Kindle device / app does the user use (e-ink or Fire/app)? Decides fixed layout.
2. Shuffle by default or in order? (Proposed: shuffled, with a switch.)
3. One section per chapter or per scene?
4. Should Scriptorium's own EPUB also get numbered sections for text-only gamebooks?
5. Include the cover and the CGs/inserts, or only the scene background?
6. Which languages: export per language edition (proposed, yes)?

## Proposed tickets
Hub: **HUB-25** "Book export for Kindle and PDF" (plan `.claude/tickets/HUB-25-book-export-kindle-pdf/plan.md`), a ROADMAP row after HUB-23/24, depends on VNO tickets below. Next free ids: VNO-52, SCP-49 (VNO-51 and SCP-48 are the latest in the ROADMAPs; verify).

1. **VNO-52 Export model and gamebook sections** (VN Studio). Reads `vn.json` + edition into an ordered export model; section numbering (seeded shuffle or in order), choice resolution, validation. Done: tests 1 and 4 pass; MCP `export_book {format:"json"}` or a dry-run returns the section map.
2. **VNO-53 EPUB export** (VN Studio). Reflowable EPUB 3 for a linear book and for a choice book, with `#section` links, nav, cover, one JPEG per scene, ending and "play again" links. Done: test 2 passes; the file opens in Kindle Previewer/epubcheck with no errors; link check on a real project (Clockless God both variants, a picture book).
3. **VNO-54 PDF export** (VN Studio). Spike library, then same model to PDF with section headers, clickable "turn to N", images, footer; Croatian verified. Done: test 3 passes; the user opens a real PDF.
4. **VNO-55 Fixed-layout picture-book EPUB** (VN Studio, optional, only if the Kindle supports it). Done: opens on the user's device, else dropped.
5. **SCP-49 Numbered sections in Scriptorium EPUB** (Scriptorium, optional). Text-only gamebooks get the same numbering and Send to Kindle gets a PDF/EPUB choice. Only if open question 4 is yes; reuse by copying, since the repos are separate.
6. **Hub step** (HUB-25 itself): update `make-visual-novel` skill with "export for Kindle/PDF", live check with one choice book and one picture book sent to the user's Kindle; user verdict recorded in `runs/`.
