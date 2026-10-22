# HUB-06: Scriptorium writes VN Studio's media lines and bible aliases

Status: plan, not started. Written 2026-10-22.

## Goal

Scriptorium's visual novel scripts carry the lines VN Studio (VNO-08) reads: `CG:`, `INSERT:`, `SFX:`, `AMBIENCE:` and `END CG`. Each bible character entry gets an `Aliases:` sentence. `ON SCREEN:` names only characters, never props. Then VN Studio builds a game with CGs, inserts, sound effects and ambience from a Scriptorium book with no hand edits to the script or bible.

The code work is in Scriptorium, ticket **SCP-16**, branch **`SCP-16_vn-media-lines`**, cut from `master` (46e5e8a). The hub part is the live check and the doc updates.

## Scope

In scope (Scriptorium):
- The VN prompts: `outline_vn`, `draft_chapter_vn`, `rewrite_chapter_vn`, `humanize_chapter_vn`, `review_vn`.
- The adaptation texts in `src/engine/pipeline/adapt.ts` (the script writer, SCP-11).
- The outline schema and the light bible writer: an `aliases` list per character, written as an `Aliases:` sentence.
- One shared cue grammar (regexes) in `src/engine/publish/xhtml.ts`, used by the EPUB and reader layout, `get_script`, the humanizer guard and the place fixer.
- `get_script` JSON: cue beats, character `aliases`, `alias` on lines and cast entries.
- A short note to every reviewer of a script book: cue lines are not prose.
- The tighten retry keeps cue lines.
- `yarn seed:hashes`, tests, docs (`docs/visual-novel.md`, `docs/mcp.md`, `docs/design.md`), the MCP tool description.

In scope (hub):
- A contract check with a hand-made book folder (no Scriptorium needed).
- A live run: adapt a short story, import into VN Studio, build, lint, the user plays it.
- `SKILL.md`, `ROADMAP.md`, a run log.

Out of scope:
- Any VN Studio code change. See "Does VN Studio need a change?" below. A companion VNO ticket is proposed, not part of SCP-16.
- A `MUSIC:` script line. VN Studio has none; scene music stays the stage director's job.
- Long (structured-bible) script books. No VN format is `long`, so only the light bible is changed.
- Book Translator. It already keeps `CG:` and similar as a speaker tag and translates the text after it (see Risks).
- Seed `config/formats.md` guidance. Existing data folders never get config changes, so the rules live in the prompts (which migrate) and in engine-side notes.
- Word counts. Cue lines count as words; that is a few percent at most.

## Decisions already made

1. The line syntax is fixed by VN Studio's importer (VNO-08 phase 6). Scriptorium writes to it; it does not invent its own.
2. Aliases are written as an `Aliases:` sentence in the character's bible entry (VNO-08 follow-up, Scriptorium `ROADMAP.md` line 24).
3. `ON SCREEN:` is for characters only. Props go to `INSERT:` or narration.
4. Branch `SCP-16_vn-media-lines` from Scriptorium `master`.
5. Restarting Scriptorium resumes its whole factory and may spend on paid models. It needs the user's go-ahead.
6. From VNO-08: SFX have no default engine. A sound effect without a file is skipped in the build with a warning until a file is imported (`vno_asset_import`) or `sound.sfxEngine` is set. Ambience uses the music engine (ACE-Step).
7. From VNO-08: VN Studio merges two bible entries into one person only when one entry names the other. So one bullet per person is the rule.
8. A production is done only when the user has played it (hub CLAUDE.md).

## Decisions inferred (change any of them before implementing)

1. **Limits per chapter**, said in the prompts: at most 2 `CG:`, at most 2 `INSERT:`, at most 4 `SFX:`. `AMBIENCE:` at most once per scene. Reason: every CG and insert is a generated image, and every SFX needs a file.
2. **Aliases come from the outline JSON**: `characters[].aliases: string[]`. The engine writes the sentence, not the model. That keeps the sentence in the exact form VN Studio parses.
3. **The Aliases sentence goes before `Voice:`**: `- **Kessler**: <looks, who>. Aliases: the bald man, Brother Kessler. Voice: <voice>`. VN Studio splits looks and voice at `Voice:`, so an alias list after it would land in the voice text.
4. **Alias cleanup in the engine**: drop full stops inside an alias (`Dr. Vey` becomes `Dr Vey`), drop an alias equal to the character's own name, drop an alias equal to another character's name or alias (VN Studio would merge the two people), dedupe, at most 5, each at most 40 characters (the speaker label limit of `LINE`).
5. **Do not add a second Aliases sentence** when the description already has `Aliases:`.
6. **`get_script` gets a new beat type** `{ type: 'cue', cue: 'cg' | 'insert' | 'sfx' | 'ambience', text: string | null }` (`null` = `CG: none`, `END CG`, `AMBIENCE: none`). One script line stays one beat, like `break`. The alternative (cue fields on the next beat, as VN Studio stores them) is easy to add later.
7. **Cue lines do not end a scene's `background`** in `get_script`. `AMBIENCE:` right after `SCENE:` is the normal place for it.
8. **EPUB and reader** show a cue as a small italic note: `Picture: ...`, `Close-up: ...`, `Sound: ...`, `Ambience: ...`. `CG: none`, `END CG` and `AMBIENCE: none` are not shown.
9. **Humanizer guard**: the cue lines must keep their kinds and order (like speakers). Their text is not compared; the prompt asks to keep it word for word.
10. **Scriptorium copies VN Studio's regex verbatim**, Croatian keywords too, so both tools read the same lines. Book content stays English.

## The exact line formats (VN Studio, master 7ff8a2d)

From `C:\projects\Personal\visual-novels-orchestrator\src\engine\vn\script.ts`:

```ts
/** A cue line: `CG: ...`, `INSERT: ...`, `SFX: ...`, `AMBIENCE: ...` (Croatian `SLIKA`, `ZVUK`, `ATMOSFERA`); `CG: none` and `END CG` hide the picture. */
export const CUE_RE = /^\**\s*(CG|SLIKA|INSERT|SFX|SOUND|ZVUK|AMBIENCE|ATMOSFERA)\s*:\s*\**\s*(.*?)\s*\**$/iu
export const END_CG_RE = /^\**\s*(?:END\s+CG|KRAJ\s+SLIKE)\s*\**$/iu
```

How `parseChapterScript` uses them (checked after `SCENE`, before `ON SCREEN` and speaker lines):
- `CG:` / `SLIKA:` adds an image with `display: 'full'`; `INSERT:` the same with `display: 'insert'`. `CG: none` (also `ništa`, `nista`) hides it. The cue goes on **the next beat** of the scene.
- `AMBIENCE:` / `ATMOSFERA:` adds an ambience sound; `AMBIENCE: none` stops it.
- `SFX:`, `SOUND:`, `ZVUK:` add a sound effect.
- An empty cue text is ignored.
- A cue with no beat after it in its scene is dropped: `chapter N: a CG line at the end of a scene has no beat after it in its scene: dropped`.
- The catalogue key is the first four content words of the text:

```ts
const CUE_STOP = new Set(['the', 'a', 'an', 'of', 'in', 'at', 'on', 'to', 'and', 'with', 'by', 'for', 'from', 'u', 'na', 'i', 's', 'sa', 'iz', 'za', 'od'])
/** The catalogue key of a cue description: its first four content words (`The ledger page lies open on the desk` -> `ledger_page_lies_open`). */
export function cueKey(text: string): string { ... .slice(0, 4) ... }
```

  So the same picture shown twice needs the same opening words, and two different pictures need different opening words.

What the game does (`src/engine/renpy/emit.ts`):
- A CG stays on screen until `CG: none` / `END CG`, or until the next `SCENE` (the `scene` statement clears it). It is shown with `zorder 50`, over the sprites.
- An ambience loops until another `AMBIENCE:` or `AMBIENCE: none`. It carries on into the next scenes of the chapter. It stops at the end of the chapter.
- An SFX plays once when its beat starts.

Props in `ON SCREEN:` (`classifyOnScreen`, same file): a line with a `:` or ` / `, an entry of more than 5 words (a leading article not counted) or with `.;!`, or a first entry starting with `a|an|the|over|on|in|at|under|beside|na|u|iznad` that is not exactly a character name or alias, becomes narration and a scene hint. Nobody is cast.

Aliases, from `src/engine/vn/aliases.ts` and `bible.ts`:

```ts
/** An explicit list: `Aliases: the bald man, Rusty.` / `Also: ...`. */
const ALIAS_LIST = /\b(?:aliases|alias|also|nadimci|nadimak)\s*:\s*([^.\n]+)/iu
// split on: /[,;]|\s+(?:or|ili)\s+/i
const VOICE = /\b(?:voice|glas)\s*:\s*/i   // bible.ts: looks = text before it, voice = text after it
const BULLET = /^\s*[-*+]\s+\*\*(.+?)\*\*\s*:?\s*(.*)$/
```

Also accepted: a quoted name after `calls him/her/them`, `known as`, `also called`, `called`, `nicknamed`, `a.k.a.` (`ALIAS_AFTER`). The list stops at the first full stop, so an alias must not contain one. A speaker label or an `ON SCREEN` entry that equals an alias (normalised) maps to that character, and the game shows the alias as the name tag.

## Does VN Studio need a change?

- **For the build: no.** Every line above is already read, planned, generated and emitted by VNO-08 (merged, master 7ff8a2d).
- **For "no hand edits": one small change is recommended.** A CG from an imported script has no `characters` (`parseChapterScript` sets only `{ key, description, display }`). So the art director gets no character looks, and the CG is drawn without the character sheets as references. The faces in a CG may not match the sprites. Today the fix is a hand edit per CG (`vno_image_set {slug, key, characters}`). Proposed companion ticket in VN Studio: **`VNO-16_cg-characters-at-import`**: in `parseChapterScript`, set `characters` on a new image to the bible characters whose name or alias appears in the cue text (at most 3), plus a test in `tests/vn-import.test.ts`. Write it into `C:\projects\Personal\visual-novels-orchestrator\ROADMAP.md` either way. See open question 1.
- **Optional, later:** a `MUSIC:` script line. Not needed: the stage director picks scene music.
- **Housekeeping:** the hub's VN Studio `out/` may predate the VNO-08 merge (hub `ROADMAP.md` "Rebuild and restart"). The live check rebuilds it first.

## Open questions for the user

1. **CG faces.** Do VNO-16 (CG characters at import) before the live run, or accept CGs drawn from their description only for this test? Recommended: do VNO-16 first; it is small.
2. **Who does the model work in the live run?** Default: Claude through the client provider for architect, writer and humanizer (`adapt_book {models}`), reviewers on Scriptorium's own models, as in the Clockless God run. Or all on Scriptorium's models (may spend).
3. **SFX files.** VN Studio needs a file per sound effect. For the test: import 2 or 3 files you have, or let the hub make short clips (comfy-mcp `generate_music`, a few seconds), or accept "skipped" warnings for SFX. Default: make 2 or 3 clips with comfy-mcp and import them; the rest stay skipped and logged.

## Scriptorium steps (branch `SCP-16_vn-media-lines`)

Setup notes:
- Node is only on PATH through fnm: `fnm env --use-on-cd | Out-String | Invoke-Expression` first (Scriptorium CLAUDE.md).
- The Scriptorium working copy is on `SCP-15_roadmap` with an untracked `ROADMAP.md`. Cut the branch from `master`: `git switch master`, `git pull`, `git switch -c SCP-16_vn-media-lines`. The untracked `ROADMAP.md` comes along. Do not commit it on SCP-16.
- Ticket folder for the changelog: `C:\projects\Personal\scriptorium\.claude\tickets\SCP-16-vn-media-lines\` (same style as SCP-14). This plan stays in the hub.

### Phase 0: baseline

- [ ] Run `yarn test`, `yarn typecheck`, `yarn lint` on the new branch. Write the counts down (SCP-14 ended at 39 files, 501 tests). Note any flaky test before changing code.

### Phase 1: one cue grammar, read everywhere

- [ ] `src/engine/publish/xhtml.ts`: export `CUE` and `END_CG`, copied verbatim from VN Studio's `CUE_RE` and `END_CG_RE`, with a comment naming the source file. Export a helper `cueOf(line): { cue: 'cg' | 'insert' | 'sfx' | 'ambience'; text: string | null } | null`:
  - `null` when the line is not a cue;
  - `SLIKA` is `cg`; `SOUND` and `ZVUK` are `sfx`; `ATMOSFERA` is `ambience`;
  - `none` / `ništa` / `nista` (for CG, INSERT, AMBIENCE) and `END CG` / `KRAJ SLIKE` give `text: null`;
  - an empty text (`CG:` and nothing) gives `text: ''`. VN Studio consumes such a line and does nothing, so callers skip it: no beat, no HTML.
- [ ] `scriptToXhtml` (same file): check `cueOf` after `SCENE` and before `CAST`/`LINE`, as VN Studio does. Render `<p class="vn-cue"><span class="vn-label">Picture:</span> ...</p>` (`Close-up:` for insert, `Sound:`, `Ambience:`). Write nothing for a `null` text.
- [ ] `src/engine/publish/epub.ts` (CSS next to `p.vn-cast`, line 43): add `p.vn-cue` (small, grey, italic) and its `.vn-label`. Check `src/engine/publish/reader.ts` for its own CSS and add the same there if it has one.
- [ ] `src/engine/publish/script.ts`, `parseScript`:
  - add `| { type: 'cue'; cue: 'cg' | 'insert' | 'sfx' | 'ambience'; text: string | null }` to `ScriptBeat`;
  - check `cueOf` before `CAST` and `LINE`, so `CG:` is never a speaker named "CG";
  - a cue beat does not end `background` (keep the flag; collect background while the scene has no beat other than cue beats).
- [ ] `src/engine/publish/script.ts`, `parseLightBible`:
  - characters get `aliases: string[]`;
  - `looks` ends at the first of ` Aliases: ` or ` Voice: `;
  - aliases: the text after `Aliases:` up to the first full stop, split as VN Studio does (`/[,;]|\s+(?:or|ili)\s+/i`), trimmed, quotes stripped, deduped.
- [ ] `parseScript(body, bibleNames)`: take the bible characters with aliases (new optional parameter, keep the old signature working). A speaker or cast name that equals an alias gives `speaker`/`name` = the bible name and `alias` = the alias as the bible writes it. Types: `{ type: 'line'; speaker; expression; text; alias?: string }`, cast entries `{ name; look; alias?: string }`.
- [ ] `src/engine/pipeline/series.ts`, `lightBibleEntries`: fill `aliases` from an `Aliases:` sentence (same parse), so a light-bible source book carries its aliases into an adaptation.
- [ ] `src/engine/pipeline/humanizerHandlers.ts`:
  - `scriptStructure` returns `cues: string[]` too: the cue kinds in order, with `:none` for a null text (`['ambience', 'sfx', 'cg', 'cg:none']`). Cue lines are no longer counted as speakers (today `LINE` matches `CG: ...` as a speaker "CG");
  - `humanizeProblem` refuses a script whose `cues` changed, with the reason `script lines changed` (the existing wording);
  - `fragmentShare(text, true)` leaves cue lines out of the narration count.
- [ ] `src/engine/pipeline/scriptPlaces.ts`: no logic change. `placeDescriptions` uses `parseScript(...).background`, which now skips cue lines. Add a test for that.
- [ ] Tests:
  - `tests/script.test.ts`: every cue form (`CG:`, `INSERT:`, `SFX:`, `SOUND:`, `AMBIENCE:`, `CG: none`, `END CG`, `AMBIENCE: none`, `**CG:** ...` with bold marks); a cue is never a speaker; `AMBIENCE:` right after `SCENE:` keeps the background; `parseLightBible` reads `Aliases:` before `Voice:`; an alias speaker gives the bible name and `alias`; the old example still parses the same.
  - A new `describe('scriptToXhtml')` (in `tests/script.test.ts` or a new `tests/xhtml.test.ts`): a cue renders as `vn-cue`, not `vn-speaker`; `END CG` renders nothing.
  - `tests/humanizer.test.ts`: `scriptStructure` lists cues; a version that drops, adds or reorders a cue line is refused; a reworded cue text is accepted.
  - `tests/series.test.ts` (or `adapt.test.ts`): `lightBibleEntries` reads aliases.

### Phase 2: aliases in the bible

- [ ] `src/engine/pipeline/handlers.ts`, outline handler (around line 561): `characters: z.array(z.object({ name, description, voice, aliases: z.array(z.string()).default([]) }))`.
- [ ] Add `aliases?: string[]` to the `OutlineCharacter` types in `src/engine/pipeline/adapt.ts` (line 196), `src/engine/pipeline/handlers.ts` (`withBriefCharacters`, line 1259) and `src/engine/pipeline/series.ts` (`withSeriesBible`, line 173). Pass the list through unchanged.
- [ ] A helper `cleanAliases(name, aliases, otherNames)` (in `src/engine/pipeline/scriptPlaces.ts`, or a new `src/engine/pipeline/scriptBible.ts`): inferred decision 4.
- [ ] The light bible line (handlers.ts line 637), for `fmt.script` only: `- **Name**: <description>[ Aliases: a, b.][ Voice: ...]`. Make sure the description ends with a full stop before the sentence. Skip when the description already has `Aliases:` (decision 5).
- [ ] `withSourceBible` (`adapt.ts`): a source entry's `aliases` (long bible: `BibleEntry.aliases`; light bible: from phase 1) go into the script character's `aliases`, merged with the architect's.
- [ ] Tests:
  - `tests/adapt.test.ts` "is seeded from the source cast and places": a source with aliases gives a script bible line with `Aliases:` before `Voice:`.
  - A unit test for `cleanAliases`: full stops removed, own name dropped, another character's name dropped, dedupe, the cap.
  - `tests/pipeline.test.ts` (or `novel.test.ts`, where a VN outline is mocked): an outline answer with `aliases` writes the sentence; without it nothing changes.

### Phase 3: prompts and engine notes

Keep every example cue line in a prompt **under 40 characters**. The leak guard (`pipeline/leak.ts`, `MIN_LENGTH = 40`) treats a longer prompt sentence found in an answer as leaked instructions, and a leak in the middle fails the job.

- [ ] `seed/prompts/architect/outline_vn.md`: ask for `"aliases"` per character: other names the script will use for the person (a description the narration uses before the name is known, a title, a nickname), as the script writes them; `[]` when none. Never another character's name. One entry per person: never list one person twice. Add `"aliases": []` to the JSON example.
- [ ] `seed/prompts/writer/draft_chapter_vn.md`: after the ON SCREEN rules, add the picture and sound lines. Proposed text (plain, short):

  ```
  Pictures and sounds, each on its own line:
  CG: a picture over the whole screen
  INSERT: a thing or a page shown up close
  SFX: one sound effect
  AMBIENCE: a background sound that loops
  END CG ends the picture. AMBIENCE: none stops the sound.

  - Put a picture or sound line right before the line it goes with. Never make it the last line of a scene or of the chapter.
  - CG: at most two per chapter, for the moments that matter most. Say who (bible names), doing what, and where, in one sentence. It stays until END CG or the next SCENE.
  - INSERT: a letter, a sign, a page, a photo or an object the reader must see. At most two per chapter. Put what it says in a narration line after it.
  - ON SCREEN is only for characters. Never put a thing, a page or a crowd in it.
  - SFX: a single sound the story needs (a door, a shot, a phone). At most four per chapter.
  - AMBIENCE: once, right after the SCENE line, when the place has a steady sound. It plays on into the next scenes, so write a new AMBIENCE, or AMBIENCE: none, when the sound changes or stops.
  - The same picture again: copy its CG line word for word. Two different pictures start with different words.
  - A speaker may be one of the character's aliases from the bible, in capitals (THE BALD MAN:), until the story gives the name.
  ```
- [ ] `seed/prompts/writer/rewrite_chapter_vn.md`: keep the cue lines unless a note asks to change them; a short version of the rules above (one paragraph); same alias rule.
- [ ] `seed/prompts/humanizer/humanize_chapter_vn.md`: add the cue lines to "The grammar of the script" and to the first "What to do" rule: keep every CG, INSERT, SFX, AMBIENCE and END CG line word for word, in the same place.
- [ ] `seed/prompts/line-editor/review_vn.md`: cue lines are picture and sound cues for the game. Check only their form: own line, right before the line they go with, not at a scene's end, within the limits. `ON SCREEN` names only characters. A speaker label may be an alias from the bible. Do not ask for more cues.
- [ ] `src/engine/pipeline/adapt.ts`, `intro`:
  - `outline`: "If the source calls a character by another name (a nickname, a title, a description before the name is known), put it in aliases, and never give that person a second entry."
  - `draft`: "Use the picture and sound lines of the script format: a CG for the source's key moments, an INSERT for the letters and objects the story turns on."
  - `rewrite`: keep the cue lines.
- [ ] `src/engine/pipeline/handlers.ts`, `tighten` (line 281): the script text becomes "Cut narration lines and minor lines, and keep every SCENE, ON SCREEN, CG, INSERT, SFX and AMBIENCE line and every plot beat".
- [ ] `src/engine/pipeline/handlers.ts`, review handler (after line 831): for `fmt.script`, `appendToPrompt(messages, SCRIPT_CUES_NOTE)`. Text: "Lines that start with CG:, INSERT:, SFX: or AMBIENCE:, and END CG lines, are picture and sound cues for the visual novel app. They are not text the reader sees: do not review them as prose." Put the constant next to `placesBlock` in `scriptPlaces.ts`.
- [ ] Run `yarn seed:hashes`. Commit `src/engine/store/seedHistory.ts` with the prompts. `tests/migrations.test.ts` fails otherwise. The old seed hashes stay listed, so `migrateSeedPrompts` upgrades a data folder whose VN prompts were never edited.
- [ ] Tests:
  - `tests/adapt.test.ts`: the outline intro mentions aliases; the draft intro mentions CG and INSERT.
  - `tests/rewrites.test.ts` or `tests/lengths.test.ts`: the tighten message for a script names the cue lines.
  - `tests/reviews.test.ts`: a script book's review prompt has the cue note; a prose book's does not.
  - `tests/humanizer.test.ts` "a visual novel uses the script prompt": add a cue line to the mocked chapter; an answer that drops it keeps the original.
  - `tests/leak.test.ts`: a chapter that contains the prompt's example cue lines is not cut (they are under 40 characters).

### Phase 4: MCP and docs

- [ ] `src/engine/mcp/tools.ts` (`get_script`, line 299): the description names `cue` beats, `aliases` on characters and `alias` on lines and cast entries.
- [ ] `docs/visual-novel.md`:
  - grammar table: rows for `CG:`, `INSERT:`, `SFX:` / `SOUND:`, `AMBIENCE:`, `CG: none` / `END CG`, `AMBIENCE: none`, in the order they are checked;
  - the regex block: add `CUE` and `END_CG`;
  - the bible example: a character with `Aliases:` before `Voice:`; the rule "one bullet per person";
  - the chapter example: an `AMBIENCE:`, an `SFX:`, an `INSERT:` and a `CG:` with `END CG`;
  - "Reading it as a player": how long a CG and an ambience last, the next-beat rule, the dropped trailing cue;
  - "What is guaranteed": cue lines and aliases are asked of the model, not guaranteed;
  - the JSON shape: a `cue` beat, `aliases`, `alias`;
  - "In Scriptorium": the prompts now cover the cue lines; reviewers get the cue note.
- [ ] `docs/mcp.md` line 73: the same additions for `get_script`.
- [ ] `docs/design.md`: a Decisions row "VN media lines (SCP-16)" with the decisions above, and a History line dated the day of the work.
- [ ] `C:\projects\Personal\scriptorium\.claude\tickets\SCP-16-vn-media-lines\changelog.md`: commits, what changed, deviations, verification, follow-ups (SCP-14 style).

### Phase 5: verify and hand over

- [ ] `yarn test` (all green; compare with the Phase 0 count), `yarn typecheck`, `yarn lint`.
- [ ] `yarn seed:hashes` again: no diff.
- [ ] Optional: `yarn test:ui` (no UI change expected).
- [ ] One commit per phase, `SCP-16: <what>`, ending with the co-author line. Push `origin/SCP-16_vn-media-lines`. Do not merge: the user merges.
- [ ] Not done in SCP-16: starting the engine on `~/Scriptorium`. That is the hub step below.

## Hub steps

Hub doc edits go on a hub branch `HUB-06_scriptorium-vn-media-lines`. The hub working copy is on `HUB-01_roadmaps-to-repos` with uncommitted changes: ask the user how to handle them before switching. Do not mix the two.

### H1: contract check, no Scriptorium needed

- [x] `pwsh -File scripts\hub.ps1` (status). If VN Studio's `out/` predates master 7ff8a2d: `hub.ps1 build vn-studio`, `hub.ps1 stop vn-studio`, `hub.ps1 start vn-studio`, then `/mcp` reconnect. Result: Done: vn-studio up on 7459 from master 81abb9e (includes VNO-08), so no rebuild.
- [x] Write a tiny book folder by hand in `runs/hub-06-media-lines/book/` (Scriptorium layout: `book.md` with `script: true`, `outline.md`, `bible/bible.md`, `chapters/ch-01.md`), using the new `docs/visual-novel.md` example: one character with `Aliases:`, a speaker line under the alias, one of each cue line, a prop that would once have been `ON SCREEN:`. Result: Done: `runs/hub-06-media-lines/book/` written (alias Kessler, one of each cue except `CG: none`, prop as INSERT).
- [x] `vno_import {source: <absolute folder>}`. Check: no "has no beat after it" warning, no speaker `CG`/`SFX`, `vno_get_story` lists the `images` (one full, one insert), the `sounds` (sfx and ambience), the alias on the character, and the alias line mapped to it. Result: Done: imported as `hub-06-media-lines`, `warnings: []`; images 1 full + 1 insert (no `characters`, VNO-16 absent), sounds 1 sfx + 1 ambience, alias on Kessler, THE BALD MAN mapped to kessler, no speaker CG/SFX.
- [x] Log it in `runs/hub-06-media-lines.md` (copy `runs/_template.md`). Result: Done: `runs/hub-06-media-lines.md`.

### H2: live run with Scriptorium (needs the user's go-ahead)

- [ ] Ask the user: start Scriptorium on the SCP-16 build? It resumes the factory: `list_stories {status: open}` first, and say what would run.
- [ ] Build from the SCP-16 branch (or master after the user merges): `pwsh -File scripts\hub.ps1 build scriptorium`, then `pwsh -File scripts\hub.ps1 start scriptorium -Force` (`-Window` if the user wants to watch).
- [ ] Check the start log (`hub.ps1 logs scriptorium`): `migrateSeedPrompts` lines for `prompts/architect/outline_vn.md`, `writer/draft_chapter_vn.md`, `writer/rewrite_chapter_vn.md`, `humanizer/humanize_chapter_vn.md`, `line-editor/review_vn.md`. A prompt the user edited is not upgraded: compare it with the seed and ask before copying.
- [ ] Adapt a short published book. Recommended: `the-lighthouse-that-kept-lists` (4 chapters, about 5,900 words; an island lighthouse and lists, so sea ambience, a foghorn SFX and list inserts fit). `adapt_book {book: "the-lighthouse-that-kept-lists", format: "visual-novel", title: "The Lighthouse That Kept Lists (VN)", models: <per open question 2>}`.
- [ ] Work the client task loop if Claude writes; else `wait_for_book`. Log every id in the run log.
- [ ] Before VN Studio, check the book:
  - `get_script {book}`: count `cue` beats per chapter (CG at most 2, INSERT at most 2, SFX at most 4); no cue is the last beat of a scene; no line beat with speaker `CG`, `SFX`, `INSERT` or `AMBIENCE`;
  - `read_book_file {book, file: "bible"}`: every character is one bullet; `Aliases:` comes before `Voice:`; no alias names another character;
  - grep the chapters: no `ON SCREEN:` line that is a prop.
- [ ] VN Studio: `vno_import {source: <book slug>}`. Expect `images` and `sounds` in the preview, aliases kept on their characters, no "dropped" cue warnings, no alias-merge report (there should be nothing to merge).
- [ ] If VNO-16 is not done: list the CGs and decide with the user whether to set `characters` by hand (`vno_image_set`). Log it as a hand edit.
- [ ] SFX files per open question 3: make or pick 2 or 3 clips, `vno_asset_import` them. Log which SFX stay skipped.
- [ ] `vno_update_settings` (illustrated art by default), `vno_run_pipeline {slug}`, then `vno_wait` in a loop. Review `cg_*` assets and the cover. `vno_build`, then `vno_lint` (clean).
- [ ] Give the user the play command (PowerShell form from the skill). The user plays it. Ask about CGs, inserts, ambience and SFX. Write the answer in the run log.

### H3: hub docs

- [ ] `.claude/skills/make-visual-novel/SKILL.md`:
  - step 1A: Scriptorium VN scripts (from SCP-16) carry `CG:`, `INSERT:`, `SFX:`, `AMBIENCE:` lines and `Aliases:` in the bible;
  - step 1B (book folder written by hand): the same lines are allowed;
  - step 3: after `vno_import`, check `images`/`sounds`; SFX need a file (`vno_asset_import`) unless `sound.sfxEngine` is set; CG characters (until VNO-16).
- [ ] `ROADMAP.md` (hub): the item is done or what is left. Scriptorium `ROADMAP.md` line 24: mark done (that file is untracked and belongs to `SCP-15_roadmap`; edit it there, not on SCP-16). VN Studio `ROADMAP.md`: the VNO-16 item if not done, and the `MUSIC:` line idea.
- [ ] `README.md`: no change expected (the doc pointers stay the same).

## Risks

- **Models skip or misuse cue lines.** The line editor checks form only; nothing fails a book for having no cues. The live check measures how often they appear.
- **A cue at a scene's end** is dropped by VN Studio with a warning. The prompts forbid it; the H2 check counts them. An engine-side fix (move a trailing cue before the scene's last beat) is possible later.
- **CG key collisions.** Two CGs with the same first four content words become one image. The prompt asks for different opening words.
- **Humanizer refusals.** A humanizer that drops a cue line is refused, and the chapter keeps its pre-humanizer text. Watch the job results in H2.
- **Book Translator** keeps `CG:` as a tag and translates the description. VN Studio's edition import parses cue lines as cues (not beats), so alignment should hold, and editions reuse the original's pictures. Not tested here; test it with the next translated VN edition.
- **Leak guard.** Long example lines in a prompt can be flagged as leaks when a model copies them. Keep examples under 40 characters (Phase 3).

## Done when

- SCP-16 is pushed with green `yarn test`, `yarn typecheck`, `yarn lint`, and no `yarn seed:hashes` diff.
- H1 passes.
- H2: a Scriptorium adaptation imports into VN Studio with CGs, inserts, ambience and SFX cues and no script or bible hand edits, builds, lints clean, and the user has played it.
- The run log says what was verified and what was not.
