# HUB-05: *The Hour That Happens Twice* in Croatian

## Goal

A Croatian EPUB of Hartley & Varga book 2 for the user to read, consistent with book 1's Croatian edition (*Bezsatni bog*). Asked by the user on 2026-10-21.

## Background

- Source: Scriptorium book `the-hour-that-happens-twice`, published at 7.61 (`runs/the-hour-that-happens-twice.md`).
- Book 1 was done the same way: Book Translator project `the-clockless-god-hr-2945aa`, every model task done by Claude through the client provider, $0 (steps, glossary terms and lessons in `runs/the-clockless-god.md`, "Croatian translation").
- Since then BTT-10 (`clientOnly`) and BTT-11 (lighter client tasks, the prompt sent once) are merged.

## Decisions

- Made (user): Croatian, done by Claude through the client provider, book 1's glossary carried over.
- Inferred: do it after HUB-02, so the hub's Book Translator runs the BTT-11 build.
- Inferred: same editorial rules as book 1: one past tense (perfect, no aorist in dialogue tags), Dec and Inès use "ti", one word per object and term, French/Latin/Hungarian kept and not flagged as untranslated.

## Steps

- [x] 1. Check `hub.ps1 status`: Book Translator up on the BTT-11 build (HUB-02 step 1).
- [x] 2. Export book 1's glossary (`get_project` / the project's glossary file for `the-clockless-god-hr-2945aa`) to `.claude/temp/hv-glossary-hr.md`: names, places and the series terms (Bratovština Devetog sata, Bezsatni, Zaustavljeni sat, Devetorica, ...).
- [x] 3. `create_project` with the book's folder, `hr`, `clientOnly: true`. `set_brief` in Croatian: the series, the editorial rules above, book 1's glossary as fixed terms, foreign text left as is.
- [x] 4. Work the client tasks with subagents (glossary, translator, proofreader, QA), stop rule "stop when the project leaves translating", as in book 1. Seed the glossary with book 1's terms before translating.
- [x] 5. A final editorial pass by editor subagents with `edit_chunk` (tense, address, terms, the real QA findings, contents page against chapter headings).
- [x] 6. `export_project` to EPUB; copy it to `runs/the-hour-that-happens-twice/the-hour-that-happens-twice.hr.epub`. Check `dc:language hr`, the Croatian title and the word count.
- [x] 7. Log it in `runs/the-hour-that-happens-twice.md` (project id, glossary, chunks, flagged chunks, cost). Anything Book Translator lacked goes to its `ROADMAP.md`.
- [ ] 8. The user reads it. Done only then.

## Acceptance

- All chunks done, none left flagged without a reason.
- Series terms and names match *Bezsatni bog*.
- The user has the EPUB and has read it.
