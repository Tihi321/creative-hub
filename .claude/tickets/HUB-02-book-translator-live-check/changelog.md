# HUB-02 changelog

2026-10-22, branch `HUB-02-13_roadmap-tasks`, commit fac90cb. Run log: `runs/the-clockless-god-vn.md`.

- Book Translator live check (BTT-11) on master 2a21970: a VN book folder through the full pipeline on the client provider (`clientOnly`). Claude did all the model work; $0 spent.
- The Croatian VN edition of *The Clockless God*: project `the-clockless-god-3-hr-ac0756`, 37 chunks, `localizeNames` off, with an editorial pass. The QA flags were cleared and the edition exported to `runs/the-clockless-god/the-clockless-god-3.hr/`.
- `vno_add_edition`: 1221 lines matched, 0 missing, 0 extra. Built and linted in VN Studio.

Verified: the export, the alignment, the build and the lint.
Not verified: the user playing the Croatian edition. 46 of 87 UI strings are still in English (VN Studio follow-up).
Found: BTT-15 (false "untranslated" flags on VN lines), BTT-16 (the glossary pass overwrites the brief), BTT-17 (substring glossary matching), BTT-19 (a stale lock with a reused pid) and BTT-20 (client-loop ergonomics). All are in Book Translator's ROADMAP (PR #12, merged).
