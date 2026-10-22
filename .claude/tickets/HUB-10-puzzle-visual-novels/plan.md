# HUB-10: Puzzle visual novels

Plan written 2026-10-22. Nothing here is implemented yet.

The idea came from the user and Claude on 2026-10-21. It was in VN Studio's `ROADMAP.md` ("Puzzle visual novels"). That section was moved out of VN Studio on 2026-10-22, so this ticket is now its home. The hub `ROADMAP.md` ("Plans across tools") points here.

## Goal

Visual novels with logic puzzles between story scenes. The player reads a scene, solves a puzzle, and the story goes on, or branches on the result. Kinds wanted:

- Murdle (https://murdle.com/?mode=tutorial): who, with what, where.
- Puzzle Baron logic grids (https://logic.puzzlebaron.com/).
- Knights and Knaves: who lies and who tells the truth.
- Ace Attorney cross-examination: press a statement, or present the evidence that breaks it.

The story, art, music and voices already come from the chain (Scriptorium, VN Studio, the studios). What is new is the puzzle, a play screen for it, and the path from a book to puzzles.

## Scope

In scope:

- A puzzle library: generators and solvers made by code, and Ren'Py play screens.
- VN Studio: a `puzzle` beat in the story JSON, the build and lint, the `vno_puzzle_*` tools, editions (translated clues).
- The flavour step: a model writes names and clues in prose; code checks the prose still means the same constraints.
- Scriptorium: a "mystery with puzzles" format with `PUZZLE:`, `CLUE:`, `EVIDENCE:` and `TESTIMONY:` lines.
- A first production, played by the user.

Out of scope:

- A new engine or a web player. Ren'Py is enough. A separate repo is only worth it for a non-Ren'Py target.
- Puzzles invented by the language model. The model never decides the logic.
- Voice for clue cards (later, if wanted).
- Puzzles that change every playthrough. A story puzzle is fixed when the book is made (see Q3).

## Phases and branches

| Phase | What | Repo | Branch (suggested) |
|---|---|---|---|
| 1 | Proof of concept: a 3×3 Murdle grid in one Ren'Py screen, generator and solver in Python | VN Studio | `VNO-12_puzzles-poc` |
| 2 | VN Studio integration: `puzzle` beat, templates, tools, build, lint, editions | VN Studio | `VNO-13_puzzle-beats` |
| 3 | More puzzle kinds: bigger Murdle, logic grids, Knights and Knaves, testimony | VN Studio | `VNO-14_puzzle-kinds` (one sub-branch per kind if it grows) |
| 4 | Scriptorium format and the chain from a book | Scriptorium, then VN Studio, then the hub skill | `SCP-18_mystery-puzzles`, `VNO-15_puzzle-script-lines`, hub `HUB-1x_puzzle-skill` |
| 5 | A first production | hub (run file), tools as they are | hub `HUB-1x_first-puzzle-vn` |

The numbers after VNO-12 are suggestions. Take the next free number in each repo when the phase starts (already taken by other hub tickets: VNO-10 HUB-07, VNO-11 HUB-08, VNO-16 HUB-06, SCP-16 HUB-06, SCP-17 HUB-11). Each phase can be implemented and merged on its own. Phase 1 needs nothing else. Phase 2 needs phase 1. Phase 3 and phase 4 both need phase 2 and can run side by side. Phase 5 needs phase 2, and phase 4 if the story comes from Scriptorium.

Repo rules that hold for every phase:

- A branch per phase, cut from `master`, named after a ticket in the repo's style. Ticket notes go in that repo's `.claude/tickets/<ticket>/` (a `changelog.md` like VNO-08's).
- Commits as `VNO-12: <what>`, ending with the session's attribution line. Do not push or merge without the user.
- VN Studio: Node through fnm (`fnm env --use-on-cd | Out-String | Invoke-Expression`). Checks are `yarn test`, `yarn typecheck`, `yarn lint`.
- VN Studio: do not run `yarn build:engine`, `yarn engine`, `yarn dev`, `yarn build` or `yarn mcp` on a feature branch. The hub runs this repo's `out/engine/index.js`. Do not stop the engine on port 7459. Never write to `~/VisualNovels`. Test output goes to `.claude/temp/` or `mkdtemp`.
- Scriptorium: never start it without asking the user. After editing `seed/prompts` or `seed/templates`, run `yarn seed:hashes`.
- Ren'Py lint comes from `tests/renpy-integration.test.ts`: the real Ren'Py 8.5.3 SDK at `C:/projects/Local/renpy/renpy-8.5.3-sdk` (`DEFAULT_SDK_PATH`, or `VNO_RENPY_SDK`). Every phase that changes the game output adds a case there.

## Decisions made

These come from the original idea and stand unless the user changes them.

1. **Ren'Py, no new engine.** Screen language draws the grid (✓ / ✗ / blank cells), the suspect × weapon × place board, statement cards with true/false toggles, a court record and a "present" button. Python checks the answer. Labels branch on right or wrong.
2. **It lives in VN Studio.** A new beat kind `puzzle` in the story JSON (`vno_create_project`, `vno_story_edit`), a puzzle library in the Ren'Py templates, and `vno_puzzle_*` tools.
3. **Code makes the puzzle.** A generator plus a solver makes each puzzle and proves two things: it has exactly one solution, and it can be solved by deduction alone, with no guessing. Difficulty is measured from the solver's steps.
4. **The model writes only the flavour.** Names, clues in prose, the story around the puzzle. The solver checks that the prose clues still mean the same constraints.
5. **Scriptorium gets a "mystery with puzzles" format** with `PUZZLE:`, `CLUE:`, `EVIDENCE:` and `TESTIMONY:` lines.
6. **Art reuses VNO-08 asset kinds.** Evidence items are `insert` images (`cg_<key>`), portraits are the character sprites.
7. **First step is a proof of concept**: a 3×3 Murdle grid in one Ren'Py screen, generator and solver in Python, before any work in the tools.

Decisions this plan adds (small, reversible):

8. **Puzzle data is plain JSON-shaped data** (dicts, lists, strings, ints). No classes in saved state. Reason: it goes to and from the engine as JSON, and Ren'Py saves and rollback handle plain data in `default` variables. Objects from an imported module do not take part in rollback.
9. **Python code uses only the stdlib that Ren'Py's own Python has.** The SDK ships Python 3.12.7 (`lib/py3-windows-x86_64/python.exe`). It has `random`, `itertools`, `json`, `dataclasses`, `argparse`, `re`. It does not have `unittest` or `doctest`. So tests are plain functions with `assert` and a ten-line runner.
10. **Deterministic by seed.** `random.Random(seed)` only, never the global `random` and never `renpy.random` inside the library. The same seed gives the same puzzle in the SDK Python and in system Python 3.13.
11. **The puzzle library sits in `templates/puzzles/`, not in `templates/renpy/`.** The game base stays untouched in phase 1, so no current build changes. From phase 2 the build copies `templates/puzzles/game/` into a game only when the book has a puzzle beat (as it writes `vno_fonts.rpy` only when needed).
12. **✓ and ✗ are drawn with `DejaVuSans.ttf`** (it ships with Ren'Py), or as small images. Theme fonts may lack those glyphs.

## Open questions for the user

Phase 1 can start without any answer. Q1 must be answered before phase 2.

- **Q1. Where does the generator and solver live: Python or TypeScript?**
  - *Option A, Python, one copy (recommended).* The package `vno_puzzles` is pure Python. The game imports it from `game/python-packages/` (Ren'Py 8.5 adds that folder to the import path; checked in `renpy/importer.py`). The engine runs the same files at authoring time with the SDK's own Python, as a short subprocess with JSON in and out, like it runs `renpy.exe lint` today. Why: the PoC is already Python, so nothing is thrown away. One solver gives the same steps for difficulty at build time and for hints in the game. The game can work out a hint from the player's own marks. VN Studio already needs the SDK to build, translate and lint, so no new install.
  - *Option B, TypeScript in the engine.* Generator and solver in `src/engine/puzzles/`, tested by vitest, called in-process. The game gets only data: the solution and the solver's step list, plus about 50 lines of Python to check an answer and walk the steps for a hint. Why: the rest of VN Studio is TypeScript with zod and vitest; the tools would work with no SDK. Cost: the PoC's Python solver is rewritten, and two languages describe one puzzle format.
  - Recommendation: A. Switch to B only if the subprocess turns out slow or awkward in phase 2 (the check is that one `vno_puzzle_generate` call returns in under 2 s).
- **Q2. What happens on a wrong answer?** Recommendation: retry as often as the player wants. A hint is offered after 2 wrong accusations. No game over by default. Each puzzle may set `onFail` to jump to a chapter instead (a bad ending in a choice book). Testimony (phase 3) gets Ace Attorney's penalty bar, and an empty bar restarts the cross-examination.
- **Q3. Is a puzzle fixed per book, or new on every playthrough?** Recommendation: fixed. The story text, the translations and the clue art refer to one puzzle. The PoC still has a "new puzzle" button, only for testing.
- **Q4. What does the player have to submit?** Recommendation: only the accusation (who, with what, where), as in Murdle. The grid is the player's own notebook. A fully correct grid could earn a small "perfect" note.
- **Q5. Order of the kinds in phase 3?** Recommendation: bigger Murdle (4×4 with a motive and attribute clues), then Knights and Knaves, then testimony, then Puzzle Baron grids with ordinal clues. The first two reuse the most from the PoC. Testimony is the most story-heavy and needs evidence art.
- **Q6. How does a Scriptorium book get its puzzles?** Recommendation: VN Studio makes the puzzle core (solution and structured clues) with `vno_puzzle_generate`. The hub skill hands it to Scriptorium in the story brief, and Scriptorium keeps it as `bible/puzzles.md`. The outline places the puzzles and the writer plants the clues. Scriptorium stays free of solver code. The other route is a solver inside Scriptorium, which means two copies of the logic.
- **Q7. Grid controls.** Recommendation: a click cycles blank → ✗ → ✓ → blank. A right-click (or long press) sets ✗. A ✓ fills ✗ along its row and column in that block (an "auto-✗" preference, on by default). Plus Undo and Clear.
- **Q8. Grid headers: names only, or pictures?** Recommendation: names in phase 1 and 2. Portraits and item pictures in phase 3, from sprites and insert images that already exist.

## Phase 1: proof of concept (VN Studio, `VNO-12_puzzles-poc`)

Detailed enough to implement now.

### Goal of phase 1

A small Ren'Py game the user can play: a short intro, a 3×3 Murdle puzzle on one screen, an accusation, and a reply for right or wrong. The puzzle is made by a generator and checked by a solver in Python. The user can ask for a new puzzle at easy, medium or hard. Nothing in VN Studio's story, tools or normal build changes.

### Files

All paths are in `C:\projects\Personal\visual-novels-orchestrator`.

New:

```
templates/puzzles/
  README.md                                  what the library is, the data format, how to run its tests
  game/
    python-packages/vno_puzzles/
      __init__.py                            version, public functions: generate, solve, count_solutions, check_accusation, check_marks, hint, clue_text
      model.py                               the puzzle data format, helpers (cell keys, categories, truth of a clue in a solution)
      solver.py                              count_solutions (brute force) and deduce (human-style steps)
      generator.py                           generate(kind, size, seed, band)
      text.py                                canonical English sentences for each clue type, names for the PoC
      play.py                                game-time helpers: check_accusation, check_marks, hint, cycle_mark, auto_cross
      cli.py                                 JSON in and out: generate, solve, check (for tests now, for the engine in phase 2)
    vno_puzzle.rpy                           init python import, the default state, the screens vno_murdle and vno_accuse, label vno_puzzle_play
  poc/
    puzzle_poc.rpy                           the PoC story: label puzzle_poc, intro, call vno_puzzle_play, right/wrong, "another puzzle" menu
tests/puzzles/
  test_vno_puzzles.py                        the Python tests (plain asserts and a small runner)
tests/puzzles.test.ts                        vitest: runs the Python tests with the SDK Python, and the PoC build + real lint
scripts/puzzle-poc.ts                        builds the PoC game into .claude/temp/puzzle-poc/ ; --lint, --play
.claude/tickets/VNO-12-puzzles-poc/
  changelog.md                               files, deviations, verification, the user's play notes
```

Changed:

- `src/engine/renpy/run.ts`: add `sdkPython(sdkPath)`. It returns the SDK's Python for this platform (`lib/py3-windows-x86_64/python.exe`, `lib/py3-linux-x86_64/python`, `lib/py3-mac-universal/python`), or null when it is missing. Add `runSdkPython(sdkPath, args, {input?, timeoutMs?})` next to `runRenpy`, with the same spawn style. Phase 2 reuses both.
- `README.md` (VN Studio): one line under Scripts for `npx tsx scripts/puzzle-poc.ts`.

Not changed in phase 1: `templates/renpy/`, `src/engine/renpy/build.ts`, `emit.ts`, the story schema, the MCP tools.

### The puzzle data (version 1)

Items are abstract ids. Names and text are a separate layer, so the model can rename without touching the logic.

```json
{
  "format": 1, "kind": "murdle", "size": 3, "seed": 1234, "band": "medium",
  "categories": [
    { "key": "suspect", "items": ["s1", "s2", "s3"] },
    { "key": "weapon",  "items": ["w1", "w2", "w3"] },
    { "key": "place",   "items": ["p1", "p2", "p3"] }
  ],
  "solution": { "s1": { "weapon": "w2", "place": "p3" }, "s2": { "weapon": "w1", "place": "p1" }, "s3": { "weapon": "w3", "place": "p2" } },
  "clues": [
    { "id": "c1", "type": "not",    "a": "s1", "b": "p1" },
    { "id": "c2", "type": "either", "a": "w1", "b": ["p1", "p2"] },
    { "id": "c3", "type": "is",     "a": "w3", "b": "s3" }
  ],
  "murder": { "place": "p3", "answer": { "suspect": "s1", "weapon": "w2", "place": "p3" } },
  "difficulty": { "steps": 14, "score": 22, "rules": { "clue": 4, "elim": 6, "last": 2, "either": 1, "trans": 1 } },
  "steps": [ { "rule": "clue", "clue": "c1", "cell": ["s1", "p1"], "value": "no" } ],
  "names": { "s1": "Colonel Ash", "w1": "rope", "p1": "library" },
  "text":  { "c1": "Colonel Ash was not in the library." }
}
```

- The first category is the "person" category. `solution` maps each person to one item of every other category (each item used once).
- A cell is a pair of items from two different categories. It is "yes" when they belong to the same person in the solution.
- Clue types for phase 1:
  - `is(a, b)`: a and b go together.
  - `not(a, b)`: they do not.
  - `either(a, [b1, b2])`: a goes with b1 or b2 (both from one category).
  - The murder clue: "The body was found in the <place>". The answer is the person and the weapon at that place.
- `names` and `text` are filled from `text.py` in the PoC. In phase 2 the model writes them.

### The solver (`solver.py`)

Two parts. Both must agree on every generated puzzle.

1. **`count_solutions(puzzle, limit=2)`**: enumerate every assignment (for 3 categories of n items: (n!)² assignments, 36 for 3×3, 576 for 4×4). Count the ones where every clue is true. Stop at `limit`. This is the proof of uniqueness.
2. **`deduce(puzzle)`**: a grid of cells, each unknown, yes or no. It applies rules one cell at a time and records each step. Rules, in the order it tries them (cheapest first, so the steps read like a person's):
   - `clue`: an `is` clue sets yes, a `not` clue sets no. An `either` clue sets no for every other item of that category.
   - `elim`: a yes in a row of a block sets no on the rest of that row and column.
   - `last`: a row or column of a block with only one unknown and no yes: that cell is yes.
   - `either`: one of the two options of an `either` clue is no, so the other is yes.
   - `trans`: a–b yes and b–c yes gives a–c yes; a–b yes and b–c no gives a–c no.
   - It returns `{ solved, grid, steps }`. `solved` is true only when every cell is known with no guessing. The grid must then equal the solution.
- **Difficulty**: weights `clue 1, elim 1, last 2, either 2, trans 3`. `score` is the sum. Bands for 3×3 are set by rules first, then tuned by score in the PoC:
  - easy: solvable with `clue`, `elim` and `last` only.
  - medium: needs `trans` or `either` at least once.
  - hard: needs `trans` at least three times, and has no `is` clue.
  - Record the real score ranges per band in the changelog after 200 seeds.

### The generator (`generator.py`)

`generate(kind="murdle", size=3, seed, band="medium", max_tries=200)`:

1. `rng = random.Random(seed)`. Shuffle the items into a random solution.
2. Build a pool of every true clue: `not` for every false pair, `either` with the true item plus one false one, and `is` for true pairs (at most one `is` for medium, none for hard).
3. Shuffle the pool. Add clues until `count_solutions == 1`.
4. Make it minimal: try to drop each clue in random order. Keep the drop when the puzzle is still unique and `deduce` still solves it.
5. If `deduce` fails, or the band does not match, try again with the next random state. After `max_tries`, raise an error that names the seed and band.
6. Pick the murder place at random. Fill `murder`, `difficulty`, `steps`, and `names`/`text` from `text.py`.

The PoC names avoid trademarked Clue/Murdle names: suspects Colonel Ash, Doctor Birch, Miss Cole; weapons rope, candlestick, poison; places library, kitchen, garden. `text.py` has one English template per clue type and per category pair ("Colonel Ash was not in the library.", "The rope was either in the kitchen or the garden.", "Whoever had the poison was in the garden.").

### Play helpers (`play.py`)

- `cycle_mark(marks, cell)`: blank → no → yes → blank. `set_mark(marks, cell, v)`.
- `auto_cross(puzzle, marks, cell)`: after a yes, fill no along that row and column of the block (only on blank cells).
- `check_accusation(puzzle, accusation)` → `{ correct, wrong: ["weapon"] }`.
- `check_marks(puzzle, marks)` → the cells that contradict the solution.
- `hint(puzzle, marks)`:
  - When a mark is wrong, it says which one: "Look again at Colonel Ash and the library."
  - Otherwise it gives the first step in `steps` that the grid does not show yet, with its reason. For example: "Clue 2 says the rope was in the kitchen or the garden, so it was not in the library."
  - Deduction steps only add facts, so the first missing step is always a valid next move.

### The Ren'Py side (`vno_puzzle.rpy`)

- `init python:` imports `vno_puzzles`. Keep helper calls thin; the logic stays in the package.
- `default vno_puzzle_state = {}`: per puzzle id, `{ "marks": {}, "struck": [], "history": [], "tries": 0, "hints": 0 }`. Plain dicts made by `default` are rollback-safe and save-safe.
- `screen vno_murdle(p, st)`:
  - modal, full screen, a solid background (the scene shows through a little).
  - Left column, about 640 px: the title, the murder note, the clue list. Each clue is a `textbutton` that strikes itself through when clicked (`st["struck"]`).
  - Right: the grid as one `grid (1+2n) (1+2n)`. Columns: suspects, then places. Rows: weapons, then places. The places × places block is `null`. That gives the usual L-shaped logic grid.
  - Column headers are short names, rotated if needed (`Transform(rotate=270)`).
  - Cells are 96×96 `button`s. `action Function(vno_cycle, ...)`, `alternate Function(vno_set_no, ...)` (right-click and long press). The mark is `text "✓"` / `"✗"` in `DejaVuSans.ttf`. Thicker lines between blocks.
  - Buttons: Hint, Undo, Clear, Accuse. Accuse returns `"accuse"`, Hint returns `"hint"`.
- `screen vno_accuse(p)`: three rows of choices (suspect, weapon, place), using screen variables. "Accuse" is sensitive only when all three are picked. Back returns None.
- `label vno_puzzle_play(pid, p)`: a loop. `call screen vno_murdle`, then:
  - On hint, say the hint with `narrator`.
  - On accuse, check it. Right: `return True`. Wrong: count the try and say so. After 2 wrong tries, offer a hint.
  - The phase 1 behaviour is endless retries, plus a "Give up" button that returns False. Phase 2 makes this per puzzle (Q2).
- After the result, `$ renpy.block_rollback()`, so the player cannot roll back and change the answer. Check how this feels in the PoC.

### The PoC story (`poc/puzzle_poc.rpy`) and harness (`scripts/puzzle-poc.ts`)

- `label puzzle_poc`: three lines of narration (a dinner, a body, three guests). `$ vno_poc = vno_puzzles.generate("murdle", size=3, seed=vno_poc_seed, band=vno_poc_band)`. Then `call vno_puzzle_play("poc", vno_poc)`, a right or wrong reply that names the culprit, and a menu: "Another puzzle (easy / medium / hard)", "The same puzzle again", "Back to the main menu".
- The first puzzle uses seed 1 and medium. "Another" picks a seed with `renpy.random.randint(1, 10**9)`. The seed and band show in a corner, so the user can report a puzzle by its seed.
- With `config.developer` on, a small overlay shows `difficulty` (steps, score, rules), for tuning.
- `scripts/puzzle-poc.ts` (exported `buildPuzzlePoc(dir, sdkPath)`, used by the test too):
  1. `buildGame` with a one-chapter, one-line story made by `buildBook(storyInputSchema.parse(...))`, with placeholders, into `.claude/temp/puzzle-poc/`. This gives the real template, theme, menus and options with no hand-written copy.
  2. Copy `templates/puzzles/game/` into `game/game/`, and `templates/puzzles/poc/puzzle_poc.rpy` next to it.
  3. Overwrite `script.rpy` with `label start:` → `jump puzzle_poc`.
  4. `--lint` runs `lint()`. `--play` runs `run()` (the window opens for the user).
- Run it as `npx tsx scripts/puzzle-poc.ts --lint --play`, as `scripts/comfy-smoke.ts` is run. It does not touch `out/` or `~/VisualNovels`.

### Tests

`tests/puzzles/test_vno_puzzles.py` runs under the SDK Python 3.12 and under system Python 3.13 (`py`). Test functions named `test_*`, a runner that runs them all, prints each failure and exits 1. Cases:

1. **Soundness over many seeds.** Seeds 1 to 200 × easy, medium, hard:
   - every clue is true in the solution;
   - `count_solutions == 1`;
   - `deduce` solves it, and its grid equals the solution;
   - the puzzle is minimal: dropping any one clue breaks uniqueness or deduction;
   - the band rule holds.
2. **Determinism.** The same seed and band give the same JSON (`json.dumps(sort_keys=True)`).
3. **Hand-made puzzles.**
   - A known unique puzzle: the solver's steps match a written list.
   - An ambiguous one: `count_solutions` returns 2.
   - A unique puzzle that needs a guess, if one can be built at 3×3 with these clue types: `deduce` says not solved, so the generator would reject it. If none can be built, say so in the changelog.
4. **Play helpers.**
   - `check_accusation` is right only for the answer.
   - `check_marks` finds a planted wrong mark.
   - `hint` on an empty grid gives step 1. With a wrong mark, it names that cell. On a full correct grid, it says to accuse.
   - `auto_cross` never overwrites a mark.
5. **Text.** Every clue type and category pair has a sentence. No `{` or `[` is left in it (Ren'Py would read `[` as interpolation).
6. **CLI.** `cli.py generate --seed 7 --band hard` prints JSON that loads back and passes the checks of case 1.
7. **Speed.** 100 generations of 3×3 in under 10 s in the SDK Python. Record the real time.
8. **Stdlib only.** Import the package with `-I` in the SDK Python, so nothing from the system site-packages leaks in.

`tests/puzzles.test.ts` (vitest, `describe.skipIf(!sdkPython(sdkPath))`):

- Runs `test_vno_puzzles.py` with `runSdkPython`. Expects exit 0, and shows the output on failure.
- Runs `cli.py generate` and checks the JSON shape with a small inline check (the zod schema comes in phase 2).
- `buildPuzzlePoc` into `.claude/temp/puzzle-poc-it/`, then the real `lint()`. Expects `messages` to equal `[]` and `ok` to be true. Timeout 240 s, like the other integration cases.

`tests/renpy-integration.test.ts` is not changed in phase 1: the game base and the build are untouched, so its 9 cases must still pass as they are.

### Acceptance criteria for phase 1

- `yarn test`, `yarn typecheck` and `yarn lint` pass. The 9 existing Ren'Py lint cases stay clean.
- The Python tests pass under the SDK Python and under system Python.
- 600 generated puzzles (200 seeds × 3 bands) are all unique and solvable by deduction alone.
- The PoC game lints clean (`renpy lint` with no messages).
- `git diff master --stat` shows no change under `templates/renpy/`, nor in `build.ts`, `emit.ts`, `story.ts` or `src/shared/vn.ts`.
- **The user plays the PoC** (`npx tsx scripts/puzzle-poc.ts --play`): at least one puzzle per band, plus a wrong accusation, a hint, undo and a save and load in the middle of a puzzle. The user's notes go in `changelog.md`: is the grid readable, do the clicks feel right, are the hints useful, do the bands feel different. The PoC is done only when the user has played it.
- The changelog records what was verified and what was not, and the measured score ranges per band.

### Risks in phase 1

- **Import path.** `game/python-packages/` is on the path in Ren'Py 8.5.3 (`renpy/importer.py`, `add_python_directory("python-packages/")`). If the import still fails, put the package straight in `game/vno_puzzles/` and record it.
- **Lint does not read `.py` files.** Lint only sees `vno_puzzle.rpy`. Python errors would show at run time. The Python tests and the user's play cover that.
- **Phone layout.** At 1920×1080 the 7×7 grid of 96 px cells is 672 px wide, which is fine. On a small phone check that the cells are still easy to touch. Android packaging of `python-packages` is checked in phase 2, not here.
- **Glyphs.** ✓ and ✗ must render with every theme: use `DejaVuSans.ttf` explicitly.

## Phase 2: VN Studio integration (`VNO-13_puzzle-beats`)

Lighter than phase 1, but concrete about where the code goes. It assumes Q1 = A (Python). With B, `src/engine/puzzles/` holds the TypeScript port instead of the Python bridge, and the game gets only data plus a checker.

### Story data

- `src/shared/puzzle.ts` (new): the zod schema of the puzzle data (format 1 above), shared by the engine and the renderer. The puzzle core (`categories`, `solution`, `clues`, `murder`, `steps`, `difficulty`) is kept apart from the flavour (`names`, `text`, `intro`).
- `src/shared/vn.ts`:
  - `puzzleEntrySchema`: `{ key, kind, data, names, text, links?, onFail?, hints?, verified }`.
    - `links` maps item ids to story keys: a suspect to a character key, a weapon to an image key, a place to a place key. A name then follows a renamed character.
    - `onFail` is `{ mode: "retry" | "continue" | "chapter", to?, maxTries? }`.
    - `verified` is `{ unique, deducible, score, textChecked, by: "vno_puzzles <version>" }`.
  - The book gets `puzzles?: PuzzleEntry[]`, a catalogue like `images` and `sounds`.
  - `puzzleBeatSchema` is `{ id, type: "puzzle", puzzle: key, ...beatCues }`, added to `vnBeatSchema`.
  - Clues planted earlier in the story: a clue may have `at: <beatId>`. That beat then emits `$ vno_clue_found("<key>", "<clueId>")`, and the puzzle screen lists only the clues found (plus the ones with no `at`).
- `src/engine/vn/story.ts`:
  - `beatInputSchema` accepts `{ puzzle: "key" }` (type `puzzle` is inferred).
  - The ops `puzzle.set` (add or change: full data, or `generate: { kind, size, band, seed? }`) and `puzzle.remove` (refused while a beat uses it, unless `force`).
  - `validateBook`: a puzzle beat points to a known key; a puzzle is used by at most one beat; every `at` beat exists and comes before the puzzle beat.
- **Adding a beat type touches about 16 files.** `yarn typecheck` lists them, because a puzzle beat has no `text`. Today they are `assets/derive.ts`, `renpy/emit.ts`, `renpy/stage.ts`, the agents `edition-aligner`, `script-analyst`, `stage-director` and `voice-director`, `vn/align.ts`, `fixes.ts`, `handlers.ts`, `import.ts`, `script.ts`, `service.ts`, `story.ts`, `voice/jobs.ts` and `renderer/lib/book.ts`. Most should skip a puzzle beat. The stage director keeps the cast on screen across it. Voice has no clip for it.

### Python bridge and tools

- `src/engine/puzzles/python.ts`: `runPuzzleCli(cmd, input)` through `runSdkPython`. It sends JSON on stdin, reads JSON from stdout, parses it with the zod schema, and has a 30 s timeout. Without the SDK it returns a clear error ("the puzzle tools need the Ren'Py SDK: set sdkPath in config/renpy.md").
- `cli.py` gets the commands `generate`, `solve` (unique, deducible, steps, score), `check-text` and `render-text`.
- `src/engine/mcp/tools-puzzle.ts` (new), registered next to `tools-story.ts`:
  - `vno_puzzle_generate {kind, size, band, seed?}`: a core plus canonical English clue sentences. Nothing is saved.
  - `vno_puzzle_set {slug, key, data | generate, names?, links?, text?, onFail?}`: the `puzzle.set` op. It runs `solve` first and refuses a puzzle that is not unique and deducible.
  - `vno_puzzle_get {slug, key}`: the data, the canonical text next to the prose, and the steps.
  - `vno_puzzle_check_text {slug, key, readBack}`: the flavour check (below).
  - `vno_puzzle_remove {slug, key, force?}`.
  - The puzzle beat itself goes through `vno_beat_add {sceneId, beats: [{ puzzle: "key" }]}`.
- **The flavour check** ("the solver checks the prose still means the constraints"):
  1. The model (a `puzzle-writer` agent, or the client) writes `names` and one prose `text` per clue from the canonical sentence.
  2. A separate **read-back** call gets only the prose and the list of names. It never sees the structured clue. It writes each clue back as a structured clue (`type`, `a`, `b`), in a closed JSON schema.
  3. `check-text` in Python checks each read-back clue against its original by truth table: over all (n!)² assignments, the two must be true in exactly the same ones. Then it checks that the read-back set still gives one solution, solvable by deduction.
  4. A cheap check comes first: every name in the read-back clue appears in the prose (name or alias).
  5. The result lists the clues that differ. The writer rewrites those, and only a fully passing set sets `verified.textChecked`.
  - The agents go in `src/engine/vn/agents/` (`puzzle-writer.ts`, `puzzle-reader.ts`), with roles in the seed, so the client provider (`client/claude-code`) can do them for free. The read-back task must not include the original clue.

### Ren'Py output

- `src/engine/renpy/build.ts`: when the book has a puzzle beat, copy `templates/puzzles/game/` into the game (not `poc/`), and write `vno_puzzles_data.rpy`: `define vno_puzzle_data = { "<key>": { ... } }`. The names and clue texts are written as `_("...")`, escaped with `escape.ts` (`[`, `{`, `%`), so Ren'Py extracts them for translation and the `text` displayable translates them when shown.
- `src/engine/renpy/emit.ts`, for a puzzle beat:
  ```
      # beat:ch02.s01.b005 puzzle:dinner
      call vno_puzzle_play("dinner", vno_puzzle_data["dinner"])
      if not _return:
          jump ch_05            # only for onFail chapter
  ```
  `retry` loops inside the label. `continue` sets `vno_puzzle_failed["dinner"] = True` and goes on.
- `vno_puzzle.rpy` grows from the PoC: it reads `onFail` and `hints`, shows the clue list from `vno_clue_found`, and shows the linked sprite as a small portrait when one exists.
- `src/engine/renpy/tl.ts` and `translatableStrings`: puzzle names and clue texts become `translate <lang> strings` entries.
- `editionSchema` gets `puzzles?: Record<key, { names, text, intro? }>`, and `syncEdition` keeps it in line.
- `vno_edition_set` accepts it. A translated clue goes through the same read-back check in that language (the read-back model reads the translated prose).
- `templates/renpy/README.md` describes the puzzle library, the way `vno_media.rpy` is described.

### Tests for phase 2

- `tests/vn-puzzle-story.test.ts`: the schema, the ops, validation errors (unknown key, used twice, `at` after the puzzle), the asset follow-up (a link to a new image adds `cg_<key>`).
- `tests/puzzle-python.test.ts`: a contract test. The CLI output parses with `src/shared/puzzle.ts`. `check-text` catches a changed clue ("not" turned into "is", a swapped name, an `either` that lost an option) and passes a faithful paraphrase.
- `tests/renpy-emit.test.ts`: the `call vno_puzzle_play` lines and the `onFail` jump.
- `tests/renpy-integration.test.ts`: a new case, "a book with a puzzle beat, a clue planted earlier, and an HR edition, lint clean". `tl/croatian/` holds the clue strings, and `vno_puzzles_data.rpy` and `python-packages/vno_puzzles/` are in the game. A second build of a book with no puzzle has neither file.
- Check that `vno_android_preflight` passes on the puzzle book, and that the APK contains `python-packages` (manual if the Android SDK is not set up).

### Docs for phase 2

`docs/mcp-guide.md` (a "Puzzles" section and the tools), `docs/protocol.md`, the `INSTRUCTIONS` in `src/engine/mcp/server.ts`, the README tool list, and VN Studio's `ROADMAP.md` (a short entry that points to this hub ticket).

### Acceptance criteria for phase 2

- Over MCP: `vno_create_project` with two scenes and a puzzle beat between them, then `vno_puzzle_set` with `generate`, written prose that passes `vno_puzzle_check_text`, then `vno_build` and `vno_lint` clean.
- The user plays it: the scene, the puzzle, a wrong answer, a right answer, and the next scene. With `onFail: chapter`, the bad ending is reached.
- The Croatian edition shows translated clues.
- All earlier tests and lint cases still pass.

## Phase 3: more puzzle kinds (`VNO-14_puzzle-kinds`)

One kind at a time, each in the same shape: a Python module in `vno_puzzles/` (`kinds/<kind>.py`: generator, solver, text), a screen in `templates/puzzles/game/`, the schema in `src/shared/puzzle.ts`, Python tests, and a Ren'Py integration case. Order as in Q5.

- **a. Murdle, full.** Sizes 3 to 5, and a fourth category (motive). Attribute clues: suspects have traits (tall, left-handed), weapons have traits (heavy, metal), places have traits (indoors). For example: "The person with the heavy weapon was outdoors."
  - Brute force grows to (5!)³ = 1.7 M assignments at 4×5. So `count_solutions` moves to propagation plus backtracking. Brute force stays as a test oracle for small sizes.
  - Murdle's "one suspect lies" variant reuses the Knights and Knaves logic.
- **b. Knights and Knaves.** 2 to 5 speakers.
  - Statements from a small grammar: "X is a knave", "X and Y are the same kind", "at least one of us is a knave", "exactly k of us are knights", and later "Y would say …".
  - Uniqueness: enumerate the 2ⁿ assignments.
  - Difficulty: the number of case splits the solver needs.
  - Screen: statement cards with portraits, a knight/knave toggle per speaker, and Submit.
- **c. Testimony (Ace Attorney).** This kind is authored, then checked, not generated from nothing.
  - Data: statements (text, a `press` follow-up that may add or change a statement), the court record (evidence: name, description, image key; profiles), and structured `claims` on statements and `facts` on evidence (for example `time_of_death = 21:00`).
  - Code finds every claim that clashes with a fact. It demands exactly the intended statement × evidence pair, and no other clash.
  - The prose of statements and evidence goes through the same read-back check as clues.
  - Ren'Py: a testimony loop label, statements in the say window with Press and Present buttons, a court record overlay with the evidence pictures, and a penalty bar (Q2).
  - "Present the evidence that proves X" outside testimony is a small variant.
  - Evidence art is `insert` images (VNO-08).
- **d. Puzzle Baron logic grids.** 3 to 5 categories of 4 to 5 items, with an ordinal category (ages, times, prices). Relational clues: before/after, exactly N apart, neither/nor, "of A and B, one is X and the other is Y". The grid screen scales and scrolls.
- **Shared work:**
  - one hint system;
  - the penalty bar and a "restart the puzzle" game over;
  - a notebook screen with every clue found so far, across scenes;
  - portraits and item pictures in grid headers (Q8).
- **Acceptance per kind:**
  - 200 seeds per band are unique and deducible (or, for testimony, have exactly one clash);
  - a lint-clean integration case;
  - the user plays one puzzle of the kind.

## Phase 4: Scriptorium format and the chain from a book

### Scriptorium (`SCP-18_mystery-puzzles`)

- `seed/config/formats.md`: a new format `mystery-puzzle-visual-novel` (`script: true`, `puzzles: true`), and maybe a choice variant later.
  - Guidance: the outline places the puzzles; the facts fix the solution (culprit, weapon, place, liar); the chapters plant the clues and evidence fairly, before the puzzle that needs them.
- Prompts: `seed/prompts/architect/outline_vn.md` (or a new `outline_vn_puzzle.md`), `writer/draft_chapter_vn.md`, `writer/rewrite_chapter_vn.md`, `line-editor/review_vn.md` and `humanizer/humanize_chapter_vn.md`. Then run `yarn seed:hashes`.
  - The humanizer and the leak guard must leave `PUZZLE:`, `CLUE:`, `EVIDENCE:` and `TESTIMONY:` lines and their ids alone.
- `bible/puzzles.md` (markdown with YAML frontmatter, as Scriptorium keeps all shared data): the puzzle cores handed in with the brief (Q6), with each clue's id and canonical sentence. The `create_story` MCP brief gets a `puzzles` field.
- A deterministic check in the review step: every clue id of a puzzle appears in a `CLUE:` line before that puzzle's `PUZZLE:` line, and every `EVIDENCE:` key used in a testimony is planted before it.
- `src/engine/publish/xhtml.ts`: the EPUB shows a `CLUE:` as a boxed note, an `EVIDENCE:` as an item, and a `PUZZLE:` as "Puzzle: <title>" with the clue list.
- Docs: `docs/visual-novel.md` (the grammar below), and a row in the Decisions table of `docs/design.md`. Then the item leaves `ROADMAP.md`.
- Tests: `tests/adapt.test.ts` style tests for the format, the review check and the EPUB rendering.

### The script lines (both repos, `docs/visual-novel.md`)

```text
CLUE: dinner/c2: The rope was either in the kitchen or the garden, Hartley noted.
EVIDENCE: pocket_watch: A pocket watch, stopped at 9:10, its glass cracked.
PUZZLE: dinner (murdle)
TESTIMONY: Miss Cole
MISS COLE: I was in the garden all evening.
MISS COLE: I never touched the poison.
END TESTIMONY
```

- `CLUE: <puzzle>/<clueId>: <prose>`: the clue is found here. It is shown as a line, and the beat gets `at`.
- `EVIDENCE: <key>: <prose>`: an item goes into the court record. It becomes an `insert` image `cg_<key>`.
- `PUZZLE: <key> (<kind>)`: the puzzle beat.
- `TESTIMONY: <witness>` … `END TESTIMONY`: the statements of a cross-examination, in order. Which statement breaks, and with what, is in `bible/puzzles.md`, never in the text.
- Croatian keywords as for VNO-08 (`TRAG`, `DOKAZ`, `ZAGONETKA`, `SVJEDOČENJE`), so translated books from Book Translator keep working.

### VN Studio (`VNO-15_puzzle-script-lines`)

- `src/engine/vn/script.ts`: regular expressions next to `CUE_RE`, and the parsing of the four lines into beats, `at` fields and the evidence images.
- `src/engine/vn/import.ts`: read `bible/puzzles.md` into the `puzzles` catalogue.
- Editions: a translated book's `CLUE:` lines line up by clue id (`vn/align.ts`).
- Import runs `solve` and the read-back check. A failing clue becomes an import warning that names the chapter, and the hub sends it to Scriptorium as a rewrite note.
- Fixtures: `tests/fixtures/books/mystery-puzzle/` (a small book in the format), and a lint-clean integration case.

### The hub (`HUB-1x_puzzle-skill`)

- `.claude/skills/make-visual-novel/SKILL.md`: a "mystery with puzzles" path:
  1. choose the puzzles;
  2. generate their cores with `vno_puzzle_generate`;
  3. write the Scriptorium brief with `puzzles`;
  4. wait for the book;
  5. import it into VN Studio;
  6. run the read-back check, and send rewrite notes on failure;
  7. art for the evidence;
  8. build, lint, and the user plays.
- `README.md` and `CLAUDE.md` only if the flow changes how the tools are used.

## Phase 5: a first production (hub, `HUB-1x_first-puzzle-vn`)

- A short mystery: 3 to 4 chapters, 2 to 3 puzzles (one Murdle, and after phase 3 one Knights and Knaves or one testimony). A Hartley and Varga case suits it.
- Two routes, depending on phase 4:
  - written straight into VN Studio over MCP (`vno_create_project`), possible after phase 2;
  - or from Scriptorium in the new format, after phase 4.
- `runs/<slug>.md` from `runs/_template.md`, with every id and decision: the puzzle keys, seeds, bands, `verified` results, and read-back failures and fixes.
- Art, music and voice as in earlier productions. Evidence as `insert` images.
- The build and lint must be clean. **The production is done only when the user has played it through**, solving every puzzle and taking at least one wrong path. The user's notes go in the run file, and fixes go into the right repo's `ROADMAP.md`.
- Optional: a Croatian edition, to check translated clues in a real game.

## Verification summary

| Check | How | Phase |
|---|---|---|
| Unique and deduction-only | Python tests over 200 seeds × 3 bands (more per kind in phase 3) | 1, 3 |
| Same puzzle from the same seed | Python test, SDK Python and system Python | 1 |
| Game logic (check, hint, marks) | Python tests | 1 |
| Ren'Py screens parse | the real `renpy lint` on the PoC game, then on built books | 1, 2, 3, 4 |
| Normal builds unchanged | the 9 existing integration cases stay clean; a book with no puzzle has no puzzle files | 1, 2 |
| Prose means the constraints | `check-text` truth-table tests with good and bad paraphrases | 2 |
| Translation | integration case with an HR edition; the Croatian clues shown in game | 2 |
| Script lines | parser tests and a fixture book in the format | 4 |
| Feel and difficulty | **the user plays**: the PoC, the phase 2 book, one puzzle per new kind, the production | 1, 2, 3, 5 |

Each phase's changelog says what was verified and what was not, for example "Android packaging not checked" or "hard band not played by the user".

## Where things go when done

- VN Studio phases: their `.claude/tickets/VNO-1x-*/changelog.md`, and VN Studio's `ROADMAP.md` "Where it stands".
- Scriptorium: `docs/design.md` decisions, and `ROADMAP.md` (the "mystery with puzzles" item closed).
- The hub: this file stays the plan of record. The hub `ROADMAP.md` "Puzzle visual novels" line points here and is updated as phases merge. The production log goes in `runs/<slug>.md`.
