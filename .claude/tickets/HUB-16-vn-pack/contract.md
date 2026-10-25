# VN pack v2 — contract

Canonical cross-repo contract for HUB-16 / SCP-45 / BTT-23 / VNO-46. The hub file is authoritative; copies live in each repo’s ticket folder. A change here is a version bump.

## 1. Files

Source book (Scriptorium data folder, `books/<slug>/`):

```text
vn/pack.json                  # template: structure, IDs, art fields. Never translated.
vn/text/<sourceLang>.json     # source catalog: display text only.
```

Translated edition (Book Translator output / hand-off folder):

```text
<slug>.<lang>/
  edition.json                # {format:"vn-edition-bundle",version:2,lang,packHash,sourceSlug}
  vn/pack.json                # byte-identical copy of the source pack
  vn/text/<lang>.json         # translated catalog
```

A catalog file alone (`vn/text/<lang>.json`) is also a valid `vno_add_edition` source.

## 2. Versions and hashes

- `pack.json`: `format:"vn-pack"`, `version:2`.
- Catalog: `format:"vn-text"`, `version:2`.
- Bundle: `format:"vn-edition-bundle"`, `version:2`.
- Readers reject any other `version`; unknown optional fields are ignored.
- `packHash` = SHA-256 of **canonical JSON** of the `pack.json` object with the `packHash` key removed. Canonical JSON = object keys sorted recursively, arrays in order, `JSON.stringify` with no whitespace, UTF-8. Implement the same helper in Scriptorium and VN Studio; the catalog carries the result and VN Studio rejects a mismatch.
- `sourceHash` = SHA-256 over the authored script files, each as `relpath + "\0" + file bytes + "\0"`, in this order: `outline.md`, `bible/bible.md`, `bible/puzzles.md` (when present), `cover-brief.md` (when present), then `chapters/*.md` sorted by the first number in the file name. **`book.md` is not in the hash**: Scriptorium writes cover fields into it after the pack is built, which would make every pack stale by design. A change to `book.md` alone (title, blurb, author, format) needs a republish/`build_vn_pack`; the publish hook does it. A mismatch means the pack is stale: warn, do not use silently.
- The pack file is written pretty-printed (2 spaces) for diffs, but `packHash` always uses canonical JSON.

## 3. IDs

### Characters and places

Use VN Studio’s `slugKey` (`src/engine/vn/ids.ts`): transliterated ASCII, lowercase, non-alphanumerics to `_`, leading non-letter prefixed `x_`; non-Latin text gets a short hash suffix. Never a translated name.

Shared test vectors (both repos must agree):

| Name | Key |
|---|---|
| `Petra` | `petra` |
| `Mango` | `mango` |
| `Petra's House` | `petra_s_house` |
| `Šime` | `sime` |
| `The Bald Man` | `the_bald_man` |

- Collision: append `_2`, `_3`, … in bible order and warn.
- Aliases: `aliasKeys` are `<charKey>#<1-based index>` in the bible’s `Aliases:` order. Their display text lives in the catalog under the same key.

### Scenes and beats

- Chapters come from the chapter files in numeric order; `n` is the chapter number.
- A scene is a `SCENE:` line (or `##` heading) that has at least one beat after it. Scenes with no beat are omitted.
- `scene.id = ch<NN>.s<NN>` (`ch01.s01`), numbered only over scenes that have beats.
- `beat.id = <scene.id>.b<NNN>` (`ch01.s01.b001`), numbered over beats in the scene in order.
- A **beat** is exactly one of `cast`, `line`, `narration`, `puzzle`. `CG`/`INSERT`/`SFX`/`AMBIENCE`/`END CG` are **not** beats: they attach to the next beat as cue fields. `---` sets `breakBefore` on the next scene, not a beat.
- This is the same numbering VN Studio’s legacy importer produces; pack import must reproduce it exactly.

### Choices, endings, puzzles

- Choice key `${chapterN}:${choiceIndex}` in outline order (0-based).
- Ending key `${chapterN}` for an `isEnding` chapter.
- Puzzle keys and clue/evidence/testimony ids are exactly those of `bible/puzzles.md` (`[A-Za-z0-9_-]+`).

## 4. `vn/pack.json` (template)

```json
{
  "format": "vn-pack",
  "version": 2,
  "packHash": "sha256:…",
  "book": {
    "slug": "the-lighthouse-letters",
    "format": "visual-novel",
    "kind": "linear",
    "primaryLang": "en",
    "genre": "Mystery",
    "style": "Moody, rain-soaked…",
    "author": "Mara Quill",
    "coverBrief": "A lighthouse at dusk…",
    "sourceHash": "sha256:…"
  },
  "characters": [
    {"key":"petra","looks":"Seventeen, small and wiry…","voice":"short sentences, dry jokes","aliasKeys":["petra#1"]}
  ],
  "places": [
    {"key":"harbour_wall","name":"Harbour wall","looks":"A long stone pier at dusk…"}
  ],
  "expressions": ["neutral","happy","worried"],  "chapters": [
    {
      "n": 1,
      "isEnding": false,
      "choices": [{"index":0,"to":2},{"index":1,"to":3}],
      "scenes": [
        {
          "id": "ch01.s01",
          "placeKey": "harbour_wall",
          "placeText": "The harbour wall",
          "time": "dusk",
          "description": "Rain needles the grey water…",
          "breakBefore": false,
          "beats": [
            {"id":"ch01.s01.b001","type":"cast","cast":[{"charKey":"petra","look":"soaked raincoat"}]},
            {"id":"ch01.s01.b002","type":"narration","ambience":{"text":"waves on stone, a far foghorn"}},
            {"id":"ch01.s01.b003","type":"line","speakerKey":"petra","expression":"worried","aliasKey":"petra#1"},
            {"id":"ch01.s01.b004","type":"narration","image":{"display":"insert","key":"pocket_watch","text":"A pocket watch, stopped at 9:10."}},
            {"id":"ch01.s01.b005","type":"puzzle","puzzle":"dinner"}
          ]
        }
      ]
    }
  ],
  "puzzles": [
    {
      "key": "dinner",
      "kind": "murdle",
      "data": { "…": "VN Studio puzzle core, unchanged" },
      "chapter": 2,
      "clueAt": {"c1":"ch01.s01.b002","c2":"ch01.s02.b004"},
      "links": {"s1":{"type":"character","key":"petra"}},
      "onFail": {"mode":"retry"},
      "hints": true,
      "verified": {"unique":true,"deducible":true,"score":1,"textChecked":true,"by":"vno_puzzle_generate"}
    }
  ]
}
```

Rules:

- `book.format` is the Scriptorium format id; `book.kind` is `linear` or `choice`. `primaryLang` is the language of the source catalog.
- `expressions` is **optional and omitted by Scriptorium**: raw bracket words can be multi-word and only VN Studio has the canonical expression table. A reader without it uses its standard expression set, exactly like the legacy importer.
- `characters[].looks`/`voice`, `places[].looks`, `book.style`/`coverBrief` are art/writing references: English, never translated.
- `characters` have no display name; the catalog’s `characterNames` supplies it. `places[].name` is a bible reference only, not shown by the game (scene display text comes from `sceneTitles`).
- `scenes[].description` is the background prompt material: the first narration after `SCENE:` plus the bible place looks. VN Studio uses it as given. Legacy folder import builds a different description, so parity comparisons ignore the description text (and the synthesized `speakerLabel` below) while requiring identical IDs, text, beat kinds and asset IDs.
- `time` is the canonical time string after the last comma (`dusk`, `the following Thursday, dawn`); `placeText` is the place as written (untranslated reference).
- A `line` beat has no display label in the template. When the source spoke under an alias, set optional `aliasKey` (`petra#1`); VN Studio then uses `characterNames[aliasKey]` as the name tag. Without it, VN Studio uses `characterNames[speakerKey]`. This keeps alias reveals working without putting a name into the template.
- Beat cue fields:
  - `image`: omitted = unchanged; `null` = hide the picture; object = show `full` or `insert` with `text` and optional `key`. With `key`, VN Studio uses `cg_<key>`; without, it derives `cg_<cueKey(text)>`. Use `key` for `EVIDENCE:` items.
  - `sfx`: omitted = none; object = play once with `text`.
  - `ambience`: omitted = unchanged; `null` = stop; object = start looped with `text`.
- `line.expression` is the raw bracket word or `neutral`; `rawExpression` is set when it is not canonical. Scriptorium passes the word through; VN Studio canonicalizes as today.
- Unknown speakers get a synthetic character (`speaker_1`, `speaker_2`, … in first-seen order) with `looks:""`; unknown places keep `placeKey: null` + `placeText` (never a synthetic place). Both are warnings, not fatal.
- An `ON SCREEN:` entry that is not a bible character or alias (a prop, a page, a crowd, a whole sentence) is **not** a cast entry and not a synthetic character: it is dropped with a warning. Only actual speakers get synthetic characters.
- `puzzles[].data` is the core exactly as supplied; `clueAt` maps every clue id to the beat id that shows it; `chapter` is the chapter with the `PUZZLE:` beat. `names`/`text` live in the catalog.
- Every `line`/`narration` beat id must have a catalog entry. Every `puzzle` beat must name a puzzle entry. Every `cast.charKey`/`speakerKey` must exist; a scene’s `placeKey` is null when the place is not in the bible (VN Studio falls back to `placeText` for the background).

## 5. `vn/text/<lang>.json` (catalog)

Exactly VN Studio’s `Edition` plus metadata:

```json
{
  "format": "vn-text",
  "version": 2,
  "lang": "en",
  "packHash": "sha256:…",
  "title": "The Lighthouse Letters",
  "blurb": "A keeper’s daughter…",
  "chapterTitles": {"1":"The Late Boat","2":"…"},
  "sceneTitles": {"ch01.s01":"The harbour wall, dusk"},
  "choiceTexts": {"1:0":"Wait at the harbour wall","1:1":"Row out to find him"},
  "endings": {"4":"bittersweet: the boat is found, empty"},
  "characterNames": {"petra":"Petra","petra#1":"the keeper's girl","mango":"Mango"},
  "beats": {"ch01.s01.b002":"Rain needles…","ch01.s01.b003":"He said he'd be back."},
  "puzzles": {"dinner":{"names":{"s1":"Colonel Ash"},"text":{"c1":"…","murder":"…"}}}
}
```

Rules:

- This is the **only** translatable document. Keys are opaque and must never be renamed.
- Required keys: `format`, `version`, `lang`, `packHash`, `title`, every chapter title, every choice text, every ending text, every character/alias name, every line/narration beat text, every puzzle name/clue text. `blurb` and `sceneTitles` are optional but emitted by Scriptorium.
- Values are single line, non-empty; inline markdown emphasis (`*x*`, `**x**`) is allowed and must round-trip.
- No structural text: a value must not begin with `SCENE:`, `ON SCREEN:`, `NARRATION:`, `CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, `CLUE:`, `EVIDENCE:`, `PUZZLE:`, `TESTIMONY:` (case-insensitive), and must not contain a beat/scene id.
- An unknown key is an error. A missing key is an error. No extra keys.

## 6. Ownership

| Concern | Owner |
|---|---|
| Structure, IDs, template, source catalog | Scriptorium |
| Translation of catalog values | Book Translator |
| `backgroundId`, `cg_`/`sfx_`/`amb_` keys, images/sounds catalogs, asset prompts and files | VN Studio |
| Voice files (per language), music/SFX/ambience files | VN Studio (generation), shared across editions except voice |
| Game UI strings, menus, skip, settings, language switch | VN Studio `shared/ui-strings.ts` and `player-runtime.ts` |
| Edition pairing, storage, build | VN Studio |

## 7. What is translated, and what is not

| Translated (catalog) | Never translated (template) |
|---|---|
| book title, blurb | slug, format, genre, style, author |
| chapter titles | chapter numbers, choices’ `to`, endings’ chapter |
| scene titles | scene ids, place keys, time, background description |
| choice texts, ending texts | puzzle keys, cores, `clueAt`, `onFail`, `hints` |
| character and alias display names | character/place keys, looks, voice notes |
| line/narration text | expressions, cast looks, cue descriptions |
| puzzle display names, clue/statement/evidence prose | `EVIDENCE:` keys, ids, logic |

## 8. Invariants for verification

1. SHA-256 of `vn/pack.json` is unchanged by a translation run.
2. The target catalog key set equals the source key set exactly.
3. Every catalog value is single-line and non-empty; no structural label at the start.
4. VN Studio pack import and legacy folder import produce the same `VnBook` and asset IDs for the fixtures, except the pack’s richer `scene.description` and the synthesized `speakerLabel` (both documented above). Adding the pack to an existing project must not change asset IDs, versions or files; prompt metadata may be refreshed from the richer description, but no generation job runs.
5. Adding an edition never touches `assets.json` or asset files.
6. UI strings never appear in the pack or catalog; asset IDs never appear in the catalog.
7. A stale `sourceHash`/`packHash` is reported, never ignored.
