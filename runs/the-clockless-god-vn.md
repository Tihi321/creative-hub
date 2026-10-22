# The Clockless God: visual novel adaptations

Started 2026-10-21.

## Brief

- Source: *The Clockless God* (`the-clockless-god`, published at 7.73), adapted with the new script writer (SCP-11).
- The user asked for two versions:
  - **with choices**: `choice-visual-novel`, with meaningful detective choices, the book ending as the canon true ending, and 2-3 short alternative endings;
  - **linear**: `visual-novel`, faithful.
- Who writes: Claude does the editor-in-chief, architect and writer work through the client provider, with subagents per book. The reviewers and the humanizer run on Scriptorium models.
- Art, music and voices: a later production in VN Studio.

## Ids

| Tool | Id |
|---|---|
| Scriptorium book (choices) | `the-clockless-god-2` (published, 7.57) |
| Scriptorium book (linear) | `the-clockless-god-3` (published, 7.5) |
| VN Studio project (linear) | `the-clockless-god-3` (built, lint clean, 0 placeholders) |
| VN Studio project (choices) | `the-clockless-god-2` (built, lint clean, 0 placeholders) |
| Book Translator (linear VN, hr) | `the-clockless-god-3-hr-ac0756` (done, 37 chunks, 0 flagged) |
| Croatian VN folder | `runs\the-clockless-god\the-clockless-god-3.hr\` (edition `hr` of VN Studio `the-clockless-god-3`, 1221/0/0 aligned, built, lint ok) |

## Log

- 2026-10-21 Scriptorium was restarted on the SCP-12 build (SCP-10/11/12) with `-Window`. The migrations added the humanizer role and agent, the article formats and the Newspaper topics. MCP reports 39 tools.
- 2026-10-21 `adapt_book {book: the-clockless-god, format: choice-visual-novel, notes, models}` made `the-clockless-god-2`; then, at the user's request, `format: visual-novel` made `the-clockless-god-3`. Both are at the pitch stage.

- 2026-10-21 Writing: one Claude subagent per book, each handing over to a fresh agent after 6 tasks. Notes for each successor are in `.claude/temp/live/the-clockless-god-{2,3}-notes.md`.
- **Linear (`the-clockless-god-3`): published at 7.5** after 2 rounds: enjoyment 8, genre fit 8, structure 8, originality 9, prose 7, continuity 6, mechanics 6.
  - 9 chapters, each adapting 2 source chapters, about 2,000-2,500 words each (over the 1,667 target; never flagged).
  - The REMITTERE decode is on screen in ch7; the HUIT hook and "Get your coat." are in ch9.
  - The humanizer, round 2 on the SCP-13 build: ch3 was kept humanized. The guards refused ch1, ch5 and ch7 (length more than 10% off, or a "new name"). One refusal was a **false positive**: "Hz" counted as a new name.
  - Before SCP-13 the humanizer had chopped some chapters into fragments (ch6, ch8). The rewrites restored them.
  - ch2 has 13 speech lines without an expression. That is valid script grammar (the expression is optional).
- 2026-10-21 VN Studio started. `vno_import {source: the-clockless-god-3}` worked: 9 chapters, 21 characters, 22 places, linear, en.
  - Warnings: the speaker VOICE (the hooded Vaulmont in ch3) has no sprite, which is right for a hidden voice; **24 scenes have a place that matches no bible place**.
  - Before generating art: line up the scene places with the bible's places (`vno_scene_update`), or improve the adapter so it reuses bible place names (ROADMAP).


- 2026-10-21 **Choices (`the-clockless-god-2`): published at 7.57** after 2 rewrite rounds: enjoyment 8, genre fit 9, prose 8, originality 9, continuity 6, mechanics 6, structure 6. It has 16 chapters (about 26k words) and 6 writer agents worked on it. The choice map is in `.claude/temp/live/the-clockless-god-2-notes.md`:
  - 3 choice points: ch4 (lamps), ch7 (the tea), ch9 (Pichon);
  - the true ending is ch13;
  - the alternative endings are ch14 "Caught by the Brotherhood" (the face is seen, then lost on the bridge), ch15 "Dec Stopped" and ch16 "The Miracle at None" (the bank calls in the atelier's loan).
- From the 2nd round on, the humanizer ran on `deepseek/deepseek-flash` with the SCP-13 prompts (switched at the user's request; see the ROADMAP).
- **Defect fixed by hand after publication:** `chapters/ch-09.md` ended with 3 paragraphs of leaked task instructions ("Write the improved chapter. ..."). A writer agent's answer file still held them, and Scriptorium accepted the submission.
  - They were removed from `ch-09.md`, from `out/the-clockless-god-2.epub` (chapter-09.xhtml patched, `mimetype` kept first) and from the reader (`node out/engine/index.js rebuild-reader`).
  - The originals are in `.claude/temp/scp-backup/`.
- Still open in the published text:
  - ch12, the "Already on R" detail;
  - ch13, quai des Orfèvres against rue du Bastion;
  - some speaker lines without an expression (valid; VN Studio uses neutral);
  - one em dash in the blurb.
- 2026-10-21 `vno_import {source: the-clockless-god-2}` worked: choice, 16 chapters, 21 characters, 24 places. Warnings: speakers RADIO, VOICE and HOODS have no sprite (on purpose); **58 scenes have a place that matches no bible place** (line them up before the art).

- 2026-10-21 Scriptorium was reloaded on the latest SCP-13 build (5c93340). All repos are clean; Book Translator BTT-10 was merged by the user.
- 2026-10-21 **Bible places lined up** (`.claude/temp/vn/places.py`, one `vno_story_edit` per project):
  - **Linear:** 24 scenes repointed and 9 new places with full looks: rue des Gravilliers, the old railway tunnel, the room at Le Balancier, the track to Combe-Noire, the cheese cellar, the holding cell, a serious restaurant, the Debt Clock chamber and the Clockmaker's Cell.
  - **Choices:** 58 scenes repointed and 8 new places, which add a school courtyard and the valley road at night; the crypt and the Debt Clock chamber already existed.
  - Both projects now have **0 unmatched scenes**. The only warnings left are the voice-only speakers VOICE, RADIO and HOODS, which have no sprite on purpose.
- 2026-10-21 User's choices for the VN production: **illustrated art** (ComfyUI qwen-image 2.1; BiRefNet cut-outs), **ACE-Step music** (5 tracks), **voices off**.
  - The VN Studio text roles of both projects (script-analyst, composer, stage-director) are set to `deepseek/deepseek-flash` by `vno_update_settings {models}`. Strata is down, and the local LM Studio model would compete with ComfyUI.
  - LM Studio's models were unloaded (`lms unload --all`); they reload on demand. ComfyUI and comfy-mcp were started; the GPU has about 108 GB free.
- 2026-10-21 `vno_run_pipeline {slug: the-clockless-god-3}` (run 1). The linear VN goes first; its characters and the places they share are to be reused for the choice VN.

- 2026-10-21 **Art direction changed** after the first sheet came out gritty watercolour, muddy and torn.
  - The user chose **clean hand-drawn**, like the classic 1990s point-and-click adventures: `art.stylePrompt` on both projects.
  - 49 planned prompts were restyled by `vno_asset_set` (`.claude/temp/vn/restyle.py`).
  - The 7 old-style sheets were regenerated through comfy-mcp and set with `vno_asset_replace` before any sprite was made (`gen_sheets.py`). VN Studio runs jobs oldest first, so a regen job would have run after the sprites.
  - La Taupe's prompt now says "young woman"; her first sheet read as male.
- 2026-10-21 Scriptorium was stopped and LM Studio's models unloaded, to free memory. ComfyUI ran qwen-image 2.1 at about 1-2 minutes per image on the AMD 8060S (about 108 GB of GPU memory).
- 2026-10-21 **Linear VN built.** 132 jobs, 0 failed:
  - assets: 14 sheets, 60 backgrounds, 67 sprites, cover, 5 ACE-Step tracks;
  - staging, build, and Ren'Py lint ok (1,221 dialogue blocks, about 17k words), 0 placeholders.
  - Fixed by hand (comfy-mcp, then `vno_asset_replace` and `vno_asset_lock`):
    - the cover: Inès had brown curly hair in a bun, and the cover was portrait, which the menu crops. It is now a **landscape** key art of Dec and Inès at Roux's clock window under the eclipse;
    - `bg_pont_de_sully_day` had a stray figure.
  - Rebuilt; lint clean.
  - The build only notes VOICE (the hidden speaker, no sprite, on purpose).
- 2026-10-21 Choice VN:
  - The alias characters `the_bald_man` (60 cast lines), `the_young_man_in_grey` (6) and `declan_hartley` (1) were remapped to Kessler, Fabien and Dec, and the aliases removed (`vno_story_edit`).
  - Reused from the linear VN (`copy_assets.py`): 13 sheets, 61 sprites, the cover, 5 music tracks, and 28 backgrounds mapped by place.
  - Only the choice VN's own art is generated: Vey, Lassalle, Zoltán, the old lady in the fur hat, Madame Ferré, a few extra expressions, Pichon's office, the priory, the school courtyard.
  - Its analysis ran on strata, with an LM Studio fallback (gemma), not on the DeepSeek models set for the project: check `vno_update_settings {models}` against the run.

- 2026-10-21 **Choice VN built.** 64 jobs, 0 failed. Lint ok: 1,257 dialogue blocks, about 19k words, **12 choice menus**. 0 placeholders. The build notes RADIO, VOICE and HOODS as ad hoc characters with no sprite, on purpose.
- Spot check: the old lady in the fur hat is good. Brother Anselm Vey came out as a young man in a waistcoat, which showed the real fault, a **wrong cast**:
  - In ch4 s5 (the chapel), the names Inès reads in the ledger had become cast beats, putting Kessler, Roux, Vey and then Lassalle on screen.
  - In ch14 s3, "the silver-haired man" (Vaulmont) was cast as Zoltán, with 4 people on screen.
  - Fixed: the ledger beats keep Inès, Dec and La Taupe on screen; the extra cast beats were removed; ch14 now shows Dec, Vaulmont and Inès. Vey, Lassalle and Zoltán no longer appear (their assets are orphaned). Rebuilt; lint clean.
  - The linear VN was checked too: those characters are never on screen there.
- 2026-10-21 The user played the **linear VN: "clockless god works"**.

Play:
- Linear: `& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\the-clockless-god-3\game"`
- Choices: `& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\the-clockless-god-2\game"`

### 2026-10-22 HUB-02 setup (Book Translator live check, steps 2-5 setup)

- Engine: book-translator rebuilt from master 2a21970, headless, MCP http://127.0.0.1:47811/mcp (a stale `engine.lock` was removed first: pid reuse). Driven with `scripts\hub.ps1 call book-translator <tool> '<json>'` or `@file.json` (use forward slashes in paths inside the JSON; a backslash path breaks the parser).
- Step 2 seed migration: `~\BookTranslator\config\seed-state.json` exists (11 providers: anthropic, client, custom, deepseek, gemini, lmstudio, mock, ollama, openai, openrouter, strata). The log has **no** "added ... from the seed" line, so nothing was added (the line is only written when something migrated). `providers.md` mtime is still 2026-10-20 15:37, so the start did not touch it; there is no pre-start copy to diff, so "unchanged" rests on the mtime (sha256 022243565e4f0ca7e45a40bafd2a641e0be3390272be64a745bcb367e5ccb4df).
- Step 3 reload: backup `.claude/temp/hub02/providers.md.bak` (same hash). Added model `client/hub02-test-model` (context 12345): `list_models` showed it within 5 s, no restart; log `models: config changed on disk, providers and models reloaded`. Restored: gone within 5 s. Broken YAML (`providers: [ {id: x,` and `- nope: : :` in the frontmatter): `list_models` still returned the 10 old models and the log had `[warn] models: config/providers.md ... could not be read, keeping the previous providers: ... bad YAML frontmatter (Nested mappings are not allowed ...)`. A milder break (junk lines appended after the providers list) was tolerated and logged as a normal reload with the same 10 models; noted only. File restored byte-exact after each test, final sha256 equals the backup.
- Step 4: `list_models` shows `client/claude-code` with context 200000 (providers.md sets `context: 200000` explicitly, so this does not prove the code default; the README says the default is 200000).
- Step 5 setup: VN folder `C:\Users\Infplane\Scriptorium\books\the-clockless-god-3` (book.md, outline.md, chapters/ch-01..09, bible/bible.md, cover-brief.md). `create_project {sourcePath, targetLanguage: "hr", clientOnly: true, localizeNames: false}` gave project **the-clockless-god-3-hr-ac0756**, format `vn`, 11 sections (book.md, outline.md, 9 chapters), all four agents on `client/claude-code`. The arg is `targetLanguage`, not `targetLang`.
- Brief: Croatian, `.claude/temp/hub02/brief.txt` (series, book 1 editorial rules: perfekt only, no aorist; Dec and Inès "ti" from chapter 4 as in book 1; one word per object/term; French/Latin/Hungarian kept and not flagged; VN script keywords and speaker tags kept; twist masculine form; character list). Glossary: book 1's project `the-clockless-god-hr-2945aa` still exists (44 terms); the 41 that occur in the VN folder were seeded with `update_glossary` (dropped: "None", a false match for the English word, and terms with 0 hits). File `.claude/temp/hub02/glossary.json`.
- `start_translation` done; status `glossary`, 1 task waiting. One `get_client_task {project}`: keys taskId, meta, system (4821 chars), user (23843), schema, output, maxTokens, leaseMinutes 30; **no `messages`**; the system text is not repeated in the user text. Released with `release_client_task` (not answered). The chunk count is unknown until the glossary passes finish (`chunking` is null; book 1 had 14 passes, then 62 chunks).
- Not done here: translation tasks, export (step 6), VN Studio (step 7).

### 2026-10-22 HUB-02 finish (step 5 end, steps 6-8)

- Translation: project `the-clockless-god-3-hr-ac0756` status `done`, 37 chunks (1,500-token budget), glossary 194 terms, every agent answered by Claude ($0). 14 chunks came back `flagged` (4, 9, 12, 13, 15, 19, 21, 27, 28, 29, 32, 33, 34, 36).
- **Flags were all false alarms**: every major issue was `untranslated` ("identical to the source") on lines kept on purpose: `VII de IX`, `Basszus.`, `Istenem.`, `Vaulmont.`, `R.`, `REMITTERE.`, `Inès!`, `Dec.` / `Hm?`, Dec's deliberate bad French (b155), `Un. Deux. Trois... Huit. Neuf.`, `Oh, putain.`, `Mutuo datum. Reddetur.`, the Latin maker's mark, the French ledger lines (b417-420) and the ALS162 test log (b638-640). Cause: Book Translator's QA counts the VN speaker tag as words, so a short kept line passes the ">= 3 words" test (new BTT item). The minor issues were the automatic glossary substring check missing inflected forms ("Da" matched "da", 39 times), plus one real one (b10, below).
- Book Translator note: `edit_chunk` marks the chunk `done` and **empties its QA issue list**. The 5 flagged chunks with nothing to fix (9, 15, 19, 21, 34) were cleared by re-saving one flagged segment unchanged. Now 37/37 `done`, 0 flagged.
- **Editorial pass** (`edit_chunk`, 36 segments in 24 chunks; backup of the chunks before it: `.claude/temp/hub02/final/chunks-backup/`, payloads `.claude/temp/hub02/final/calls/`):
  - Lock wheels `kolut*` -> `kotačić*` (glossary, book 1): b8, b10, b12 (outline), b324, b325, b328, b344, b612, b617, b619, b621, b624. b325 also "prečka padne" -> "luk se otpusti" (book 1's shackle); b612 "cilindar" -> "valjak" (cilindar is the cylinder lock).
  - The watch's alphabet rings -> `prstenovi`, as book 1 ("devet sitnih ugraviranih prstenova"): b6, b22 ("devet abecednih prstenova"), b301, b349. No "kolut" is left in the export.
  - Vey: b624 Veyeve, b627 Veyeva -> Veyjeve/Veyjeva. Kept the script's "Anselme" spelling.
  - Book 1 uses "madame Ferré" (lower case mid-sentence) and "atelijer": b1245 "Gospođa Ferré" -> "Madame Ferré"; atelje -> atelijer in b14, b16, b20, b26, b27, b29 (outline), b109, b845, b944.
  - "u zajam" -> "na zajam": b223, b1086. The motto gloss as book 1 ("Ono što je dano na zajam, oprostiti o devetom satu."): b961, b1198 (they differed from each other).
  - Others: b10 "kako su izgubili radnju" -> "kako je izgubio radnju" (QA, real); b8 "dugovat će vam dan" -> "ti" (as b23 and b359); b587 "Mlađa sestra" -> "Sestrica" (Vey's lock is the older one); b739 "Rouxovi crteži" -> "nacrti" (glossary); b768 "stanu sve postaje" -> "svi kolodvori"; b877 "ima tragove" -> "ima tragova"; b1139 "Ormar iza tebe!" -> "Kućište, iza tebe!" (one word for the cabinet).
  - Full read of all 1,313 segments: no aorist (grep plus read), narration in perfekt; outline summaries are in the present, like the English. Address consistent: Dec and Inès "vi" on Monday (b156-158, b214-216), "ti" from Tuesday on the atelier stairs (b234 "Da ti se zahvalim", b235 "Kako si me našao?"); Pichon, Clothilde, Vaulmont "vi"; Roux "ti" to Dec; Morel and Inès "ti". "Naš je restaurator" masculine kept.
- Step 6 `export_project` -> `C:\Users\Infplane\BookTranslator\projects\the-clockless-god-3-hr-ac0756\output\the-clockless-god-3.hr`, copied to `runs\the-clockless-god\the-clockless-god-3.hr\` (`diff -r` identical). 11 text files + bible + cover brief (the export does not carry `brief.md`, `chapters/history/`, `out/`, `reviews/`, which VN Studio does not need). Checked against `~/Scriptorium/books/the-clockless-god-3` (`.claude/temp/hub02/final/structdiff.py`): every file has the same line count (ch1-ch9: 170, 171, 199, 159, 176, 166, 191, 163, 203), 0 differences in `SCENE:`/`ON SCREEN:`/`---`/speaker tags (tag and expression); `bible/bible.md` and `cover-brief.md` byte-identical to the English. `ON SCREEN:` lines stay English (names and looks), as localizeNames is off.
- Step 7 `vno_add_edition {slug: the-clockless-god-3, source: runs\the-clockless-god\the-clockless-god-3.hr, lang: hr}` (job `...--vn.edition.add--hr--r9`) and `vno_align_report`: **1221 matched, 0 missing, 0 extra**. Warnings: "the translated bible has 19 characters, the primary has 22", "no translated name for The bald man / The young man in grey" (aliases in the project, not in the bible; harmless with English names). The place map takes Croatian SCENE text for some places and odd matches for others (`the_forester_s_house` -> "Les Bréviaires", `the_pantheon` -> "Okno ispod kripte Panthéona"); SCENE captions are not shown in the game, so no visible effect.
- Build (cheap: voices off, 121/121 assets ready, no new assets): `vno_build` ok (job r10), translated: `croatian`; messages: VOICE has no sprite (on purpose), "edition hr: no text for name of the_bald_man; name of the_young_man_in_grey". `vno_lint` ok: 1,221 blocks in English and **1,221 in the Croatian translation** (15,579 words). Ren'Py UI strings are partly translated (Započni, Učitaj, Postavke, Jezik; 46 of 87 screen strings still English).
- Play in Croatian: the same command as the English game, then Postavke/Preferences -> Language -> **Hrvatski** (`vn_languages = [(None, "English"), ("croatian", "Hrvatski")]`, default English):
  `& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\the-clockless-god-3\game"`
- Not verified: the Croatian game has not been played (by anyone); the `localizeNames: true` export path was not exercised.

## Checked

- 2026-10-21 The user played both VNs: the linear one ("clockless god works") and the choice one ("it is ok"). **Production done.**

- what was looked at or played, by whom

## Left to do

- ~~The user plays the choice VN.~~ Done 2026-10-21: "i played it it is ok".
- The user plays the linear VN in Croatian (edition `hr` built 2026-10-22; Preferences -> Language -> Hrvatski).
- Optional: a Croatian edition of the choice VN (`the-clockless-god-2`), Android builds, voices.

-
