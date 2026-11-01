# HUB-25 plan: export a finished VN Studio project as an illustrated book (Kindle EPUB and PDF), with a shuffled-section gamebook for choice stories

**Status: Approved 2026-11-01, build later (next milestone).**

Repos of the work: `C:\projects\Personal\visual-novels-orchestrator` (VN Studio, main path) and `C:\projects\Personal\scriptorium` (text-only gamebook). Next free ids: **VNO-52 to VNO-55** and **SCP-49, SCP-50** (checked 2026-11-01: VN Studio ROADMAP's latest is VNO-51, Scriptorium's is SCP-48; no matching branch or ticket folder exists in either). Hub id **HUB-25** is free (hub `ROADMAP.md` rows end at HUB-23; HUB-24 exists only as an untracked ticket folder, no row). Paths below are relative to the VN Studio repo unless marked `scriptorium/`. Research: `research.md` in this folder; where this plan differs from it, this plan wins (see "Findings that change the research").

Rules every worker follows (VN Studio repo conventions, as in its ROADMAP): branch `VNO-NN_<what>` cut from `master`, one commit per ticket, plan in `.claude/tickets/VNO-NN-<name>/plan.md` (copy the task block from here), a row in `ROADMAP.md`, `yarn typecheck && yarn lint && yarn test` green (Node via `fnm exec --using default yarn ...` if `node` is not on PATH), nothing spends money, no model call, no service started. Do not commit or push unless asked. Scratch files under `.claude/temp/`. Never start Scriptorium.

## Scope (one line per reading, as the global rules ask)

- **Two sources, one style.** (1) VN Studio: illustrated book (below). (2) Scriptorium: a finished Scriptorium choice book exported **with no images** as the same kind of classic multiple-path gamebook (SCP-49, SCP-50). Both use the one numbering algorithm in "Shared section algorithm", so the style matches.
- **VN Studio source:** a finished VN Studio project (`~/VisualNovels/projects/<slug>/vn.json`, its edition for one language, its selected background pictures). The illustrated export belongs to VN Studio.
- **Output:** an illustrated book file, per language edition: **reflowable EPUB 3** (for the e-ink Kindle via Send to Kindle) and **PDF** (any reader).
- **Choice VNs (`kind: choice`) become a gamebook:** shuffled section numbers, one section per chapter, section 1 is the start, "turn to section N" (a tappable link in the EPUB and the PDF). The numbers come from a fixed seed and are **stored** in the project, so the EPUB and the PDF match, and a re-export gives the same numbers.
- **Linear VNs and picture books (`kind: linear`, `presentation: picture-book`) are exported straight through, in order.** Picture book: one picture per page (the scene's illustration plus its narration caption). Linear VN: the chapter's text with one picture per chapter (the first scene's background).
- **Pictures:** the cover plus one picture per section (choice book) or per chapter (linear VN) or per page (picture book). Pictures are converted to JPEG, greyscale-friendly (see "Kindle" below), about 1000 px wide.
- **Dropped, and reported in the export result as warnings:** sprites, CG overlays other than the chosen picture, puzzle beats, cast beats, voice, music, cues. A puzzle VN's puzzle beats cannot be printed: they are skipped with a warning naming the chapter.
- **Fixed-layout picture book EPUB is OPTIONAL (VNO-55), outside the core.** The core is reflowable only.
- **Scriptorium (text only):** choice books with branch data get a **gamebook mode** in the existing EPUB builder and a new PDF writer. Shuffled numbered sections, one per chapter, section 1 = chapter 1, "If you open the door, turn to section 56." as a tappable link in EPUB and PDF, no pictures (the cover stays in the EPUB as today). The **existing EPUB mode (chapter links, "What do you choose?") stays exactly as it is and stays the default**; gamebook is an option. Scriptorium's Send to Kindle can send either. Linear Scriptorium books are not changed.
- **Not built:** KPF/Kindle Create, MOBI/AZW3 output, a UI button (the MCP tool and `vncli` are enough; a button is a flagged follow-up), RTL layout (see risks).

## Findings that change the research

1. **Owners:** VN Studio for the illustrated export; Scriptorium for a text-only gamebook mode (user decision, 2026-11-01, reversing the first correction). Research's optional `SCP-49` is back, now required, plus `SCP-50` for PDF. Scriptorium facts verified by reading only: `src/engine/publish/epub.ts` (`EpubChapter.choices {text,to}`, `.ending`), `xhtml.ts:226` `choicesHtml` (links `chapter-NN.xhtml`), `kindle.ts` (nodemailer), `pipeline/books.ts:349` `choiceLinks`, deps jszip + nodemailer, no PDF library. Scriptorium was never started.
2. **Kindle guidance is now partly verified by WebSearch (2026-11-01):** EPUB is accepted by Send to Kindle since late 2022 and converted by Amazon on upload; size limit is 200 MB on the web upload page and 50 MB in the desktop and mobile apps; the 50 MB email limit is still quoted by some sources. **Not verified** (searches found nothing authoritative): that internal `href` links between xhtml files and to `#anchors` survive the conversion, per-image size limits, and greyscale/e-ink image quality. The old "5 MB per image" figure comes from KindleGen/KDP guidelines and may not apply. VNO-53 treats these as things to test on the real Kindle, not as facts (live check step 2). The internal-link behaviour is the one the whole gamebook depends on, so VNO-53 tests it first with a 3-section probe EPUB (done-criterion there).
3. **Section numbers are stored, not recomputed.** Store them in the project (`vn.json` gets an optional `export.sections` map, or a sibling `export.json`; the worker picks one and records it, preferring a sibling file so `vn.json`'s schema and its round-trip tests are untouched): `{ seed, order: "shuffled"|"in-order", sections: { "<chapterN>": <sectionNo> } }`. A changed story (chapter added, choice retargeted) makes the stored map stale: the exporter detects it (chapter set differs) and says so; it renumbers only on `renumber: true`.
4. **Branch graph is a DAG** (Scriptorium `branches.ts`: choice `to` > `n`, max 3 choices, every chapter reachable, at least 2 endings). VN Studio's own `src/engine/vn/branches.ts` exists; VNO-52 reads it before writing a second check. The exporter still validates and fails loudly, and does not assume a DAG for reachability.
5. **Fonts:** no TTF is bundled in the repo outside `.claude/temp`; the player build fetches/uses fonts (`src/engine/game/fonts.ts`, `tools-lang.ts` `FONT_SOURCES`). The PDF spike (VNO-54) must name a font it can legally embed (Noto Sans or the font `fonts.ts` already resolves; SIL OFL), not assume one.
6. **MCP:** tools are named `vno_*` and registered from `src/engine/mcp/tools-*.ts` with `INSTRUCTIONS` in `server.ts:21` and the guide in `docs/mcp-guide.md`. **Yes, VN Studio's MCP gets an export tool: `vno_export_book`**, so the `make-visual-novel` skill can call it (see VNO-52 and the hub changes). It returns paths, never bytes.

## Shared section algorithm (one spec, two repos)

The repos are separate and have no shared package or workspace, so no import path fits. Both repos implement **this exact algorithm** and carry **the same golden test vector**; a change to either is a change to this spec first. Each repo keeps it in one small pure file (`src/engine/export/sections.ts` in VN Studio, `src/engine/publish/sections.ts` in Scriptorium) with this text in the header.

- Input: `n` (chapters, 1-based, chapter 1 is the start), `seed` (string; default the book slug), `order` (`shuffled` default, or `in-order`).
- `in-order`: chapter k gets section k.
- `shuffled`: `h` = FNV-1a 32-bit of the UTF-8 bytes of `seed` (offset 0x811c9dc5, prime 0x01000193, unsigned 32-bit). PRNG mulberry32 seeded with `h` (`a += 0x6D2B79F5; t = a; t = imul(t ^ t>>>15, t | 1); t ^= t + imul(t ^ t>>>7, t | 61); return ((t ^ t>>>14) >>> 0) / 2^32`). `nums = [2..n]`; Fisher-Yates from the end (`for i = len-1 down to 1: j = floor(rand() * (i+1)); swap(nums[i], nums[j])`). Chapter 1 gets section 1, chapters 2..n get `nums` in order.
- Output: array where index k-1 is the section number of chapter k; a bijection onto 1..n.
- Text: each choice prints as the choice text followed by the link phrase, one rule in one place, the choice text never rewritten: `{choice text} - turn to section N.` (en), and the hr phrase from a small per-language table. Ending: "The End." and "Turn to section 1 to start again." Phrase tables live in each repo; the hr wording is an open question for the user.
- Stored map: `{ seed, order, sections: { "<chapter>": <no> } }`; re-exports reuse it; a differing chapter set is reported stale; `renumber: true` recomputes.
- **Golden vector (computed with this algorithm on 2026-11-01):** `fnv1a32("golden") = 386248004`; `sections("golden", 8) = [1,4,2,8,5,3,7,6]` (chapter 1 -> 1, chapter 2 -> 4, chapter 3 -> 2, chapter 4 -> 8, ...); `sections("clockless-god", 5) = [1,4,3,2,5]`. Both repos test exactly these values.

## Files and modules to touch (by ticket)

### VNO-52 Export model, section numbering, `vno_export_book` (dry run)
- NEW `src/engine/export/model.ts` (reads `VnBook` + one `Edition` + asset resolver into an ordered `ExportBook`: `{ title, lang, mode: 'gamebook'|'linear'|'picture-book', cover, sections[] | pages[], warnings[] }`; a section/page = `{ no, title?, paragraphs[], picture?, choices?: [{ text, toNo }], ending? }`).
- NEW `src/engine/export/sections.ts` (the shared algorithm above, verbatim, plus load/save of the stored map).
- NEW `src/engine/export/validate.ts` (every `choice.to` exists, every chapter reached from chapter 1, an ending has no choices, no duplicate numbers, every chapter has text in the edition; failures throw one clear message naming chapter and choice).
- NEW `src/engine/mcp/tools-export.ts` registering `vno_export_book {slug, lang?, format: 'epub'|'pdf'|'plan', order?: 'shuffled'|'in-order', seed?, renumber?, out?}`; `format: 'plan'` is the dry run (returns mode, section map, picture count, warnings, no file). Wire it in `src/engine/mcp/tools.ts` next to the other `tools-*.ts`; add one sentence to `INSTRUCTIONS` (`server.ts:21`) and an "Export a book" section to `docs/mcp-guide.md`. Optional `vncli export` in `src/engine/vncli.ts` only if a sibling command pattern exists.
- Reads: `src/shared/vn.ts` (`presentationOf`, chapters, scenes, beats), `src/engine/game/build.ts:24-35` (`resolveAsset` pattern), the edition type in `src/shared/vn.ts`.
- Tests: NEW `tests/export-model.test.ts` (see tests).
- Steps: (1) read `branches.ts` and the Edition type; (2) model builder for the three modes (picture book: one page per scene, caption = narration beats; linear VN: lines as "Name: text" paragraphs, narration as plain; choice: chapter text + choices); (3) sections; (4) validate; (5) the tool and guide; (6) tests.
- Done: tests below pass; `vno_export_book {format:'plan'}` on a choice project returns a section map where start = 1 and numbers are a bijection, and the same map twice; typecheck/lint green; ROADMAP row.

### VNO-53 EPUB export (reflowable EPUB 3)
- NEW `src/engine/export/epub.ts` (JSZip: add `jszip` to `package.json`; copy the small structure of Scriptorium's `buildEpub` as a pattern, no dependency on that repo): `mimetype` first and stored, `META-INF/container.xml`, `content.opf` (manifest, spine, `dc:language` = edition language, cover-image property), `nav.xhtml` (TOC), one xhtml per section/chapter/page with `id="s<no>"`, `style.css`, `images/*.jpg`.
- NEW `src/engine/export/images.ts` (sharp: webp/png to JPEG, resize to ~1000 px wide, quality ~80, **greyscale-friendly**: do not convert to grey in the file (the app and Kindle Colour would lose colour); instead do a mild contrast lift and test that a greyscale rendering is still legible, see live check; flag `grayscale: true` on the tool for an optional grey JPEG variant if the user prefers).
- Gamebook layout: each section a separate xhtml file starting with a big bold number ("12"), picture, text, then "If you choose to open the door, turn to section 56." where "section 56" is `<a href="section-056.xhtml#s56">`; the ending shows "The End" and "Turn to section 1 to start again." Linear and picture-book: sequential files, one picture per page, caption below it; nav lists chapters.
- Section order inside the file follows the **number order**, so the reader cannot read ahead by file order; the nav (TOC) lists numbers only, not titles (spoilers), plus "Start: section 1".
- Wire `format: 'epub'` in `tools-export.ts`; output to `projects/<slug>/export/<slug>-<lang>.epub` (or `out`).
- Tests: NEW `tests/export-epub.test.ts`. Probe: a tiny 3-section gamebook EPUB written by `scripts/export-probe.mjs` (or the test fixture) for the Kindle link check.
- Done: tests pass; the output opens in epubcheck if available (record "epubcheck not available" otherwise; do not claim it) and every link and image resolves (test); the **probe EPUB** is what the user sends to the Kindle first (live check step 1); a real project exports (Clockless God choice variant, a picture book, a linear VN) with warnings listed.

### VNO-54 PDF export (spike first)
- Step 0, spike (first, throwaway under `.claude/temp/`, recorded in the changelog): render one page with the Croatian string "Čovjek šapće: žaba, đak, ćevap, ŠĐŽČĆ" and one internal link with **pdfkit** and **pdf-lib** (+ `@pdf-lib/fontkit`) using an embedded OFL TTF; check in PdfCraft (`doc_info`, `text_extract`, `link_list`) that the text extracts with diacritics and the link exists. Decision rule: pick the one that (a) extracts the diacritics intact, (b) supports internal link annotations to a page/named destination, (c) runs headless in plain node. Electron `printToPDF` is rejected up front: the engine runs headless (`--mcp-only`). Record the choice and why in the plan's changelog. If neither passes (b), fall back to a link to the page by destination name.
- NEW `src/engine/export/pdf.ts` (same `ExportBook` model, no second reading of `vn.json`): A5-ish page, one section per page (gamebook) or one page per picture (picture book/linear), big section number at the top, picture, text, "turn to section 56" with a link annotation to that section's page; footer with the page's section number (section number is not the page number, and the text says "section", never "page"); PDF outline/bookmarks: only "Start: section 1" (no spoilers); document title/language metadata.
- Wire `format: 'pdf'`; add the chosen library to `package.json`; bundle/license note for the font in `docs/`.
- Tests: NEW `tests/export-pdf.test.ts`.
- Done: spike recorded; tests pass; PdfCraft opens a real exported PDF, `link_list` shows a link per choice, `text_extract` shows the Croatian text intact; the user opens it (live check step 3).

### SCP-49 Gamebook mode in Scriptorium's EPUB (text only; existing mode unchanged)
- Repo `scriptorium/`. `src/engine/publish/epub.ts` `buildEpub` gets an option `gamebook?: { sections: number[]; lang }` (absent = today's output unchanged for the same input). `src/engine/publish/xhtml.ts` gets `gamebookChoicesHtml` next to `choicesHtml` (do not edit `choicesHtml`). NEW `src/engine/publish/sections.ts` (the shared algorithm and golden vector). Section files are written in number order, `section-NNN.xhtml` with `id="s<N>"`, big number heading, chapter text, then the "turn to section N" links; nav lists numbers only (no chapter titles, spoilers); no images except the existing cover.
- `src/engine/pipeline/books.ts:349` `choiceLinks` maps outline chapter numbers to positions: reuse it for `to`, then map to section numbers. Only books with choices can use the option; others ignore it with a message.
- Entry point: a `gamebook` flag on the publish call that `kindle.ts` and the app's EPUB build share; the worker records which one in the changelog. Send to Kindle is not on MCP (`docs/mcp.md:3,119`); do not add it. Stored map: `~/Scriptorium/books/<slug>/gamebook.json` (sibling file; chapter files and `outline.md` untouched).
- Tests: `tests/gamebook.test.ts` (golden vector; links resolve; the default-mode EPUB for a fixture is unchanged, compared with a hash taken before the change); `tests/pipeline.test.ts`, `tests/art.test.ts`, `tests/rewrites.test.ts` stay green.
- Done: tests; a fixture choice book exports in gamebook mode; the default EPUB is identical; ROADMAP row. **Never start Scriptorium**: use test fixtures and read `~/Scriptorium/books` read-only; the live part is the user's.

### SCP-50 Gamebook PDF in Scriptorium (text only)
- Repo `scriptorium/`. Uses the **same library and font** VNO-54's spike chose, so both PDFs look alike; it waits for that spike result. NEW `src/engine/publish/pdf.ts`: one section per page start, big number, text, link annotations for "turn to section N", footer; `package.json` dependency. Attaching the PDF to the Kindle mail only if it is a one-line change in `kindle.ts`, else a follow-up.
- Tests: `tests/gamebook-pdf.test.ts` (page count, a link per choice, Croatian text intact). Done: tests; the user opens a real PDF (live check 4a).

### VNO-55 (OPTIONAL) fixed-layout picture-book EPUB
- Only after the live check shows the user's Kindle handles it, or if the user later asks for it. `src/engine/export/epub.ts` gets `layout: 'fixed'` for picture books only (`rendition:layout pre-paginated`, a viewport meta per page, full-bleed image page with an overlaid caption or a caption strip); not for gamebooks. Fixed layout on e-ink Kindles is unverified and may be partial.
- Done: opens on the user's Kindle; otherwise the ticket is dropped and the ROADMAP row says so. Excluded from the core and from the HUB-25 done-criteria.

## Tasks for workers

Order: VNO-52 first (it holds the first copy of the shared algorithm; write the golden-vector test first, then SCP-49 copies both). SCP-49 can run in parallel with VNO-53 once VNO-52's `sections.ts` exists; SCP-50 follows VNO-54's spike. VNO-52 first (the model, and the tool every other ticket uses). VNO-53 and VNO-54 both need only VNO-52's `ExportBook` and can then run in parallel (the PDF spike can start at once, as it needs no code from 52; the final PDF writer waits for the model). VNO-55 only if triggered. The hub changes come after VNO-53 and VNO-54 merge.

Contract between tickets: `ExportBook` and `buildSections(...)` from VNO-52; `vno_export_book {slug, lang?, format, order?, seed?, renumber?, out?}` returns `{ path?, format, mode, sections: n, pictures: n, warnings: string[], sectionMap? }`; the section map file is the single source of numbers for both formats.

## Tests (follow the `test-discipline` skill: only these, no near-duplicates, no snapshot of whole files, no UI tests)

1. **Section map** (`tests/export-model.test.ts`): start chapter is section 1; every choice target maps to a number; numbers are a bijection onto 1..N; the shuffle is deterministic for the same seed and different for another; `in-order` gives chapter order; a stored map is reused on re-export and a changed chapter set is reported stale.
2. **Broken story fails loudly** (same file, one test table): a `choice.to` to a missing chapter, and an unreachable chapter, each throw a message naming the chapter.
3. **EPUB structure** (`tests/export-epub.test.ts`, unzip in the test): `mimetype` is the first entry and stored; every `href` (file and `#sN`) resolves to an existing id; every image in the manifest exists; a gamebook's text contains "section <n>" links whose numbers all exist; a picture book has exactly one image per page.
4. **PDF** (`tests/export-pdf.test.ts`): opens (library re-parse), page count equals sections (+ cover), contains a link annotation per choice pointing at an existing page, and the extracted text contains the Croatian diacritics case. If the chosen library has no re-parse, check the raw bytes for the annotations and the embedded font.
5. **Shared vector** (in both repos): the golden values above, nothing more.
6. **Scriptorium** (SCP-49/50): gamebook EPUB links resolve; the default-mode EPUB is unchanged; gamebook PDF has a link per choice and intact Croatian.
7. **Picture/puzzle handling** (one test in the model file): a puzzle beat is skipped with a warning; a missing picture gives a placeholder-free text page with a warning, not a crash.

Everything else (Kindle behaviour, how it looks on e-ink, tap targets) is **not testable in CI** and goes to the live check.

## Verification map

| # | What | Evidence |
|---|---|---|
| V1 | Numbering stable and shared by both formats | test 1 plus: export EPUB then PDF of one project, compare the stored map (same file) |
| V2 | EPUB internally valid | test 3, epubcheck if present (state if not) |
| V3 | PDF text and links | test 4, PdfCraft `text_extract` / `link_list` on a real output |
| V4 | The Kindle reads links and images | live check only (user) |
| V5 | Scriptorium default EPUB mode and Send to Kindle unchanged | SCP-49 unchanged-output test; gamebook is opt-in |
| V6 | Both repos give the same numbers | the golden vector test passes in both repos |
| Z | Repo health | `yarn typecheck`, `yarn lint`, `yarn test` on each ticket branch |

Each ticket's changelog ends with the DONE / NOT DONE / UNTESTED list. UNTESTED until the live check: anything on the real Kindle.

## Live check (hub session; $0; no model work; never start Scriptorium; the user does the Kindle steps)

Preconditions: `pwsh -File scripts\hub.ps1` (status); start only VN Studio's engine if needed (`pwsh -File scripts\hub.ps1 start vn-studio`). No ComfyUI, no voice, no generation: the check reuses existing projects. Open `runs/hub25-book-export.md` (copy of `runs/_template.md`) and record every id, path and verdict.

1. **Probe first.** Export the 3-section probe EPUB (VNO-53) and ask the user to send it with Send to Kindle to the Kindle: do the "turn to section N" links jump, does Back return, do the pictures show on e-ink. Record the answer. If links do not work, stop and revise VNO-53 (fallback: a printed "turn to section N" plus a nav list of all numbers; that changes the product, so ask the user).
2. **Choice book.** Pick the choice variant of *The Clockless God* (or another finished choice project). `vno_export_book {format:'plan'}` first (record the section map, warnings). Export the EPUB (`lang` hr, then en if wanted), the user sends it to the Kindle and plays the first three sections. Check: section 1 is the start, numbers look shuffled, endings say "The End" and offer section 1, pictures readable in greyscale, file size (record it; limit 200 MB web, 50 MB apps).
3. **Picture book.** Export a picture book project as EPUB and send it: one picture per page, caption below, in order.
4a. **Scriptorium text-only gamebook.** The user (not the session) exports a Scriptorium choice book in gamebook mode from the app, EPUB then PDF, and sends the EPUB to the Kindle: same style as the VN Studio book (shuffled numbers, section 1 start, tappable "turn to section N"), no images. The session only reads the produced files. **Scriptorium is never started by the session**; if the app must run, the user starts it, knowing it resumes its book factory.
4. **PDF.** Export the same choice book as PDF and open it (user, and PdfCraft for text/links): the link on "turn to section N" jumps, the numbers equal the EPUB's, Croatian diacritics are right.
5. **Not verified by anyone but the user:** whether it reads well, whether e-ink pictures are good enough, whether the layout suits the user. Mark UNTESTED until the user has read it (a production is done only when the user has played it). If the user wants the fixed-layout picture book, open VNO-55.

## Risks and rollback

- **Kindle behaviour is the biggest risk** (internal links, image conversion, e-ink contrast). Mitigation: the probe EPUB before any real export; the plan names the fallback in live check 1.
- **PDF library or font:** diacritics or links may fail; the spike decides before the writer is built; the PDF ticket can be dropped without touching the EPUB.
- **Stale section map** after the story changes: detect and warn; `renumber: true` is explicit. A stored map means a sent Kindle copy and a later PDF can differ only if the user renumbers.
- **Spoilers:** TOC and PDF bookmarks list numbers only; a stored shuffle seed is not secret.
- **A VN is not a book:** sprites, puzzles, cues, voice, music dropped; warnings say which. Long dialogue VNs make long sections; start with one section per chapter (user decision) and report the longest section's word count in the warnings.
- **RTL languages** (`rtlLanguages` in the VN) and CJK in PDF: not supported in the core; the exporter refuses with a clear message for an RTL edition rather than output wrong text (EPUB may work; test only if the user needs it).
- **Size:** many large pictures; JPEG at ~1000 px keeps books small; warn above 40 MB (under the 50 MB app limit).
- **Two implementations of one algorithm can drift.** Mitigation: the spec above is the source, the golden vector is in both test suites, and a change touches both repos together.
- **Scriptorium risk:** a gamebook edit to `epub.ts` could change the default output. Mitigation: new functions, an unchanged-output test, opt-in flag, Scriptorium never started by the session.
- **Rollback:** every ticket is one commit on its own branch; reverting a commit removes the feature. The change is additive (new `src/engine/export/`, a new MCP tool, one dependency per format, an optional sidecar file in the project). No existing tool, player build or Scriptorium code changes, and `vn.json`'s schema is untouched if the sidecar is chosen. In Scriptorium the gamebook mode is opt-in, so reverting SCP-49/50 leaves the existing EPUB and Kindle path as they were. Removing the sidecar `export.json` resets numbering.

## Hub changes (this repo, `C:\projects\Personal\creative-hub`)

- `ROADMAP.md`: add row **HUB-25** after the HUB-23 row (table format as rows 16 and 17): "VN Studio: export a finished project as an illustrated book for Kindle (EPUB) and PDF; choice stories as a shuffled-section gamebook; tickets VNO-52 to VNO-54 in `visual-novels-orchestrator` (VNO-55 optional fixed layout) and SCP-49/SCP-50 in `scriptorium` (text-only gamebook EPUB and PDF, same numbering); live check with a choice book and a picture book sent to the Kindle", tool column `visual-novels-orchestrator`, needs "VN Studio running; the user's Kindle", status "Open"; plan `.claude/tickets/HUB-25-book-export-kindle-pdf/plan.md`. Mark done only after the live check and the user has read the book on the Kindle. (HUB-24 has no row yet; leave its numbering alone.)
- `.claude/skills/make-visual-novel/SKILL.md`: add a short step after the build: "Export for Kindle or print: `vn-studio.vno_export_book {slug, lang, format: 'epub'|'pdf', order?}`; choice stories become a numbered gamebook ('turn to section N', shuffled with a stored seed, section 1 is the start), linear books and picture books go front to back; first `format: 'plan'` to read the warnings; the user sends the EPUB to the Kindle with Send to Kindle". Say that a Scriptorium choice book can also be exported text-only as a gamebook (EPUB mode `gamebook`, and PDF) with the same numbering, the existing chapter-link EPUB stays the default, and keep line 103's rule (a PDF is never an input to Book Translator).
- `services.json`: **no new entry** (no new service). `.mcp.json`: no change (same `vn-studio` server). `README.md`: if the VN Studio row lists its MCP tools or outputs, add "export to EPUB/PDF"; otherwise no change.
- `runs/hub25-book-export.md`: production log by the live-check session. MEMORY update after the run.

## Answers from the user (2026-11-01)

1. Croatian jump text: "idi na odlomak N", e.g. "Ako ..., idi na odlomak 56."
2. Pictures: colour JPEG.
3. No cover asset: use the first scene's background with the title over it.
4. The section picture is the chapter's first scene (plan default).
5. Fixed-layout picture book (VNO-55) stays optional, decided after the Kindle probe.
