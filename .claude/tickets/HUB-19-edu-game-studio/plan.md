# HUB-19: Edu Game Studio, an engine for educational games

Status: plan agreed in its shape 2026-10-29 (answers at the bottom); waiting for the go-ahead to implement.

## What the user asked (2026-10-29)

A new repository, built like VN Studio and Scriptorium, that turns a topic into a playable, good-looking educational game: language learning or any subject. It has its own team of roles, as Scriptorium does. It uses the hub's generators (Scriptorium for story, ComfyUI / Pixel Studio / Flow for art, Chiptune Studio / ComfyUI / Flow for music, voices). It offers several game styles: interactive quizzes, RPG, and Encarta-era games such as MindMaze. It has an MCP server so Claude can drive it the way it drives VN Studio. The plan has to be verifiable, and the UI must not be boring.

**Scope (full reading):** a whole studio app (engine + MCP + desktop UI + game player), built in phases. The first usable milestone is a pilot course, built by the studio from a topic and played by the user (phase 4). Every phase ends in something that can be checked.

**"Use your engine":** we use our own code only. The engine core is copied from VN Studio, which itself copies Scriptorium's. The player is our own runtime: DOM/CSS, plus Canvas 2D where a map needs it, the same approach as VN Studio's `player-runtime.ts`. No Phaser, Godot, Unity, Ren'Py or other game engine.

## What we reuse (from the code maps, 2026-10-29)

VN Studio (`C:\projects\Personal\visual-novels-orchestrator`) has a core that is not VN-specific, and we copy it:

- **Engine and jobs.** `src/engine/{models,queue,budget,logs,store}/*`, `agents/agents.ts`, `pipeline/{llm,prompts}.ts` and `transport.ts`. Jobs are markdown files that move through `jobs/{queued,running,done,failed}`. The scheduler has `register(task, handler)`, and `engine.lock` keeps one engine per data folder.
- **Models and roles.** Providers are openai-compat (LM Studio, Strata, acp, DeepSeek, OpenRouter), anthropic, gemini and `client` (Claude does the model work through `get_task` / `submit_task`). `config/roles.md` maps each role to models with fallbacks, plus budget caps.
- **MCP.** `src/engine/mcp/{http,server,stdio,relay,controller,config}.ts`: Streamable HTTP on 127.0.0.1 with a Host/Origin allow-list, and every tool written as `def(name, desc, zod, run)`.
- **Generators.**
  - `studios/{mcp-http,autostart,launch,config}.ts` reach Pixel Studio, Chiptune Studio and Flow, and autostart services from `services.json`.
  - `comfy/*` drives ComfyUI images, music and TTS.
  - `voice/comfy-tts.ts`.
  - `assets/{postprocess,palettes,manifest}.ts` and `themes/load.ts`.
- **App shell.** The Electron shell (`src/main`, `src/preload`), `shared/{md,schemas,languages,translit,protocol}.ts`, and `ui-strings.ts` (hr/en UI).
- **Puzzle generator.** `src/shared/puzzles/` (murdle, knights, testimony, logic, quiz), with a seeded PRNG, `verify()` (exactly one solution, solvable without guessing) and a read-back of the prose. We copy it unchanged for escape-room and detective rooms.

From Scriptorium (`C:\projects\Personal\scriptorium`) we reuse the role model and the non-fiction pipeline:

- The `researcher` and `fact-checker` roles. The fact-checker must pass.
- The `factbase/` folder of facts with sources, `[n]` citations, and Tavily, Brave, Wikipedia or client search.
- Review JSON `{verdict, scores, notes, problems}` with `threshold`, `max_rounds` and `must_pass` (in `quality.md`).

The studio does not copy Scriptorium's book pipeline. It calls Scriptorium over MCP when a game needs a story: the frame narrative of an RPG or a role-play dialogue. Its VN pack can be imported as a story layer.

Prior art on this PC:

- `lang-combat` is a German text adventure in which you act by typing German, and each floor unlocks one grammar point. Its ideas go into the language shells.
- `factory-school` is a course with XP, ranks, quizzes and simulators kept in localStorage.

## What makes learning games work (research summary)

These are the design rules every game shell has to follow. The lint and the playtester role check them.

1. **Retrieval practice (testing effect).** Answering beats re-reading, so every unit ends in recall, not recognition only.
2. **Spaced repetition.** Missed items come back on a schedule (FSRS or SM-2), within a game and across sessions. Progress is saved locally.
3. **Interleaving and variation.** Item types are mixed, and the same fact is asked in two or more forms (choice, cloze, ordering, map).
4. **Immediate, explanatory feedback.** A wrong answer shows why it is wrong, and each distractor has its own explanation written from a real misconception. A right answer adds one extra fact (the curiosity hook).
5. **Intrinsic integration.** The learning is the core mechanic, not a gate in front of it (Habgood and Ainsworth, *Zombie Division*). The RPG attack is the answer, and the castle door is the question.
6. **Mastery and flow.** Difficulty adapts, with about 70 to 85 % success as the target. A unit unlocks the next one at mastery, and boss rounds mix the earlier units.
7. **Self-determination (autonomy, competence, relatedness).** The player chooses a path, sees visible progress (map, codex, mastery stars), and characters react to them. XP, streaks and badges are used lightly, because rewards for their own sake crowd out interest.
8. **Multimedia (Mayer) and dual coding.** Each fact gets one picture, and narration is short with text alongside it. Nothing is decorative and off-topic.
9. **Language-specific.** Comprehensible input pitched just above the learner's level (i+1), with vocabulary in context and not in lists. Listening comes through TTS in the target language. Learners produce language by typing (as in lang-combat) and later by speaking. CEFR levels are used throughout.
10. **Curiosity and exploration (Encarta, Carmen Sandiego, Oregon Trail).** An encyclopedia you can browse, with links, a timeline and a map; the game sends you back into it for answers.

## Game shells (what the player can be)

All shells read one course contract, so one course can be played in several shells.

| Shell | Inspired by | Core loop |
|---|---|---|
| **Quiz arena** | Kahoot, quiz shows | Rounds of mixed items: timer, combo, boss round, review of misses |
| **MindMaze castle** | Encarta MindMaze | Walk a castle of rooms; each door is a question; the topic decides the wing; characters in the rooms; the throne room at mastery |
| **Encyclopedia explorer** | Encarta | Articles with images, audio, timeline and map; hidden "collectibles" and scavenger hunts that send you into the articles |
| **RPG quest** | Pokémon / JRPG battles | Tile map, NPCs with dialogue (story by Scriptorium), turn battles where moves are answers, quests per unit |
| **Detective / escape room** | Carmen Sandiego, Murdle | Proven logic puzzles (the copied generator) where clues are facts from the course |
| **Language role-play** | lang-combat, Duolingo stories | Dialogue scenes: answer by choosing or typing in the target language; listening; vocabulary garden with spaced repetition |

Item kinds shared by every shell:

- multiple choice, true/false and multi-select;
- cloze (fill the gap), typed answer with tolerant matching (accents, typos, synonyms), and match pairs;
- order and timeline, sort into groups, and a map hotspot or labelled image;
- listening (TTS clip, pick or type what you heard) and a flashcard with spaced repetition;
- crossword and word search, built by code.

## Roles (Scriptorium-style team)

| Role | Does |
|---|---|
| director | Picks the next job, keeps the course brief |
| curriculum-designer | Learning objectives (Bloom level), prerequisite graph, units, CEFR level for languages |
| researcher | Sourced notes into `factbase/` (copied from Scriptorium) |
| subject-expert | Writes the encyclopedia articles from the fact base, with citations |
| item-writer | Writes the items for each objective, at least two forms per fact |
| misconception-designer | Distractors from real misconceptions, one explanation per distractor |
| explainer | Feedback, worked examples, hints, "did you know" hooks |
| language-coach | Vocabulary and grammar scope by level, natural target-language phrasing, accepted answers |
| fact-checker | Every item and article checked against the fact base. **Must pass** |
| game-designer | Picks the shells, maps units to levels, rooms and quests, and sets rewards and difficulty |
| narrative-designer | Frame story and characters. Hands longer stories to Scriptorium over MCP |
| art-director / art-critic | Image plans and a check with a vision model (copied from VN Studio) |
| composer, voice-director | Music per area and mood; TTS for narration and listening items |
| playtester | Plays the built game through the bot as simulated learners and reports flow, difficulty and dead ends |
| accessibility- and child-safety-reviewer | Contrast, keyboard play, reading level; child-safety reviewer for kids' courses. **Must pass** |
| publisher | Scores against the threshold and builds the game |

Each role maps to models in `config/roles.md`, exactly as in the other apps. With the `client` provider, Claude can do all the model work at no cost.

## Architecture

- **New repository** at `C:\projects\Personal\edu-game-studio`, on GitHub as `Tihi321/edu-game-studio`. Stack as VN Studio: Electron 44, React 19, zustand, TypeScript strict, zod 4, Vitest, ESLint, Node 24 via fnm, and Yarn 4.
- **Data folder** `~/EduGames`, with `config/`, `agents/`, `prompts/<role>/<task>.md`, `courses/<slug>/`, `jobs/` and `logs/`.
- **Course contract** `src/shared/course.ts`:
  - `course/pack.json` is the template: ids, objectives, the prerequisite graph, items with answer keys, shells, assets and cues.
  - `course/text/<lang>.json` is the only translatable text, so Book Translator can translate it the same way it translates the VN pack (HUB-16).
  - Answer keys are language-neutral wherever possible: indexes, ids, numbers.
- **Pipeline** (`src/engine/edu/pipeline.ts`):

  ```
  brief → research → curriculum → articles → items → fact-check → explain
        → game design → story → art → music → voice → assemble → build → lint → playtest → publish
  ```

- **Player runtime** `src/engine/game/` is our own DOM/CSS + Canvas 2D runtime:
  - It emits `index.html`, `player.js`, `player.css` and `game-data.js`, and works over `file://`, as VN Studio's does.
  - Shells are plugins on a `window.EduEngine` hook: `registerShell`, `registerItemKind`.
  - Progress and the spaced-repetition queue are kept in localStorage, with export and import.
  - Every interactive element has a `data-testid`, so the bot and Playwright can drive it.
- **MCP** on port **7463** (the next free port after flow-music-mcp's 7462). It has the same tool families as VN Studio, prefixed `edu_*`:
  - `edu_create_course`, `edu_course_edit`, `edu_item_add/update`;
  - `edu_run_pipeline`, `edu_status` / `edu_wait`;
  - `edu_get_task` / `edu_submit_task`;
  - `edu_build`, `edu_lint`, `edu_playtest`;
  - `edu_asset_*`, `edu_voice_*`, `edu_add_edition`.

  `docs/mcp-guide.md` is served as `edu-studio://guide`.
- **Look.** A design pass up front (phase 2) with the frontend-design skill. Every shell gets its own visual theme on top of shared tokens: castle stone and torchlight for MindMaze, parchment and brass for the encyclopedia, pixel art for the RPG, chalkboard for the quiz arena. Motion (transitions, combo bursts, page turns) respects `prefers-reduced-motion`. The studio UI follows the same tokens, not the 13 px grey panel style of VN Studio.

## Phases and tickets

The repo's tickets are `EGS-NN`, branches `EGS-NN_<what>` cut from `master`, one commit per ticket, and `.claude/tickets/EGS-NN-<what>/plan.md` in the new repo. Cross-tool work stays here as HUB-19.

Each phase lists **checks**: the commands and observations that prove it is done. A phase is not done until every check passes and the result is recorded in `runs/hub19-edu-studio.md`.

### Phase 0: repository and skeleton (`EGS-01`)

1. Create `Tihi321/edu-game-studio` on GitHub (visibility per the user's answer) and clone it into `C:\projects\Personal\`.
2. Copy VN Studio's generic core (the list above), strip the VN parts, rename it (app name, `window.edustudio`, `edu_` tools, port 7463, `~/EduGames`), and add a README, ROADMAP, `docs/design.md` and AGENTS.md.

**Checks:**

- `yarn install && yarn typecheck && yarn lint && yarn test` all pass. The copied unit tests for queue, router, budget, client and MCP are kept green.
- `yarn build:engine && node out/engine/index.js --mcp-only` starts. `pwsh -File scripts\hub.ps1 check` (after phase 7's registration, or by calling the MCP directly) shows a real handshake and the tool count.
- `yarn dev` opens the desktop window.

### Phase 1: course contract, player runtime and bot (`EGS-02` to `-04`)

No language model in this phase: everything is code and hand-written fixtures.

1. `course.ts` with zod schemas, the pack and text catalog, and a validator.
2. The player runtime with the quiz arena shell and all item kinds. Spaced-repetition scheduler in pure TypeScript.
3. `edu_lint`, a native lint over `game-data.json`:
   - every item has exactly one key, or a complete accepted set;
   - distractors are distinct and none equals the key;
   - every objective has two or more item forms;
   - every asset exists and every string has text in each edition;
   - the prerequisite graph has no cycles, and every unit is reachable;
   - no placeholders are left.
4. **Autoplay bot** (`scripts/play.mjs`, using Playwright Chromium headless). It plays a built game from the answer key, in three runs:
   - (a) perfect play reaches the end;
   - (b) all-wrong play shows each explanation and the review queue;
   - (c) a seeded random learner finishes within the expected step count.

   It saves screenshots of each screen.
5. Golden fixtures: `tests/fixtures/courses/` with a solar-system course (en and hr) and a Croatian A1 greetings course.

**Checks:**

- Unit tests cover every item kind's checker, tolerant matching (č/c, typos within Levenshtein 1), and the spaced-repetition intervals.
- The bot passes all three runs on both fixtures with 0 console errors. Lint is clean, and a broken fixture fails lint with the expected codes.

### Phase 2: design system and the studio UI (`EGS-05`)

1. Design tokens and the four shell themes, done with the frontend-design skill.
2. Studio pages:
   - Library;
   - Course, with tabs Brief, Curriculum, Encyclopedia, Items, Game, Assets, Voice, Editions, Build and Playtest;
   - Models, Agents, Generators and Settings, copied from VN Studio.

**Checks:**

- A screenshot set from the bot and Playwright of each studio page and each shell at desktop and mobile width, sent to the user for a look.
- Keyboard-only play passes in the bot. An axe-core run in Playwright shows 0 serious contrast violations.

### Phase 3: roles and the content pipeline (`EGS-06` to `-08`)

1. Copy the role engine and the research, fact base and fact-checker from Scriptorium.
2. Seed the agents and prompts for the content roles in the table above, with `quality.md` must-pass: fact-checker, child-safety and accessibility.
3. `edu_run_pipeline` from a brief (`topic`, audience, level, languages, shells, length) up to `explain`.

**Checks:**

- Unit tests with the `mock` provider run the whole pipeline on a fixture brief to a valid pack. A fact-check `revise` result loops back to a rewrite and passes in round 2. A forced must-pass failure stops the publish.
- A live run with the `client` provider (Claude does the work, $0): a 3-unit course on a topic the user picks. Every item cites a fact-base entry, and lint is clean.

### Phase 4: pilot (`EGS-09`)

The first real course is a history and geography course, for example Ancient Rome or European capitals. It is built only through the MCP and played in the quiz arena, then again in the encyclopedia explorer once that shell exists.

**Check:** a full production log in `runs/<slug>.md`, the bot passes, lint is clean, and **the user plays it**. The pilot is done only after that.

### Phase 5: more shells (`EGS-10` to `-14`, one ticket per shell)

The shells are built in this order:

1. encyclopedia explorer (it suits the history and geography pilot);
2. MindMaze castle;
3. RPG quest (the frame story from Scriptorium over MCP);
4. language role-play with the vocabulary garden.

Detective / escape room (the copied puzzle generator, proved) comes after these four.

**Check per shell:**

- The bot drives a fixture course through the shell (perfect, wrong and random runs). Shell-specific lint passes: every room is reachable, every door's question exists, the quest graph can be finished, and puzzles are proved unique.
- Screenshots go to the user.

### Phase 6: media (`EGS-15` to `-17`)

1. **Art:** the art-director plans images, made by ComfyUI, Pixel Studio (RPG tiles and sprites) or Flow, and checked by the art-critic.
2. **Music:** Chiptune Studio (RPG and castle), ComfyUI ACE-Step or Flow Music.
3. **Voice:**
   - narration, and listening items in the target language;
   - the hub's voice rule applies: Gemini TTS for Croatian within the 10-a-day free quota, VibeTTS or ComfyUI TTS for the rest.

**Checks:**

- With the fakes from VN Studio's tests, the unit tests generate each asset kind.
- Live: one course gets all its assets. 0 placeholders in the build, `edu_lint` clean, the bot plays with audio on (no media errors), and the user listens and looks.

### Phase 7: hub wiring (HUB-19)

1. Add the studio to `services.json` (port 7463, headless start, autostart of the studios it needs), `.mcp.json`, and the README table.
2. Add a skill `.claude/skills/make-edu-game/SKILL.md`, the CLAUDE.md line, the hub ROADMAP, and editions through Book Translator (course text catalog).

**Checks:**

- `hub.ps1 check` lists the studio with its tool count.
- A new Claude session in the hub makes a course from one sentence through the skill.
- Book Translator translates a course catalog to a second language, the edition builds, and the bot passes on it.

### Later (not in this plan)

- Speaking practice through VibeWhisper (speech recognition).
- Android through Capacitor (lang-combat already has the setup).
- Teacher or classroom mode, and multiplayer quiz.

## Verification summary

| What | How | Where it runs |
|---|---|---|
| Code correctness | Vitest, typecheck, eslint | every ticket |
| Content correctness | Answer-key lint, fact-checker must-pass with citations, proved puzzles | pipeline, `edu_lint` |
| Playability | Autoplay bot: perfect, all-wrong and random learner runs; 0 console errors | every build, CI |
| Looks | Screenshot sets (desktop and mobile), axe-core contrast | phases 2 and 5, sent to the user |
| Integration | MCP handshake, `hub.ps1 check`, skill run from a fresh session | phase 7 |
| Real use | The user plays the pilot and each new shell | phases 4 and 5 |

Every run ends with a DONE / NOT DONE / UNTESTED list.

## Open questions for the user

## The user's answers (2026-10-29)

- **Repository:** `Tihi321/edu-game-studio`, **public**. The app is called Edu Studio and its tickets are `EGS-NN`.
- **Pilot:** history and geography. The exact topic is chosen at phase 4.
- **Shells after the quiz arena:** all four (MindMaze castle, encyclopedia explorer, RPG quest, language role-play), in the order of phase 5.
- **Platform:** PC browser, mobile-friendly. The layout scales to a phone screen; an Android app comes later.

Because the repository is public, nothing private goes into it: no keys, no `~/EduGames` data, no personal paths in the docs beyond the hub's.
