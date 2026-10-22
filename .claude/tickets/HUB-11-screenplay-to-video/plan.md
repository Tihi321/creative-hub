# HUB-11: Screenplay → video

Planned 2026-10-22. Not implemented. Implement phase by phase with the global `implement` skill, one phase (one repo branch) at a time.

## Goal

Turn a story idea, or a published book, into a short video the user watches:

```
idea / published book
   │
   ▼
Scriptorium: screenplay format (scenes, shots, dialogue, voice-over, music cues) ──► get_screenplay (JSON)
   │
   ▼
hub skill make-video + scripts/video-plan.mjs (shot plan, cost estimate, budget, timeline)
   │
   ▼
flow-music-mcp: keyframes (free) ► voices (free) ► animatic (free) ► video shots (credits) ► music ► flow_assemble ► captions
   │
   ▼
MP4 in runs/<slug>/video/, watched by the user
```

## Scope

In:
- Scriptorium: screenplay formats, prompts, a parser and `get_screenplay`; `adapt_book` also adapts a book to a screenplay.
- flow-music-mcp: the assembly features a screenplay needs (stills, clip trims, music cues, ducking).
- Hub: the `make-video` skill, a small planner script with unit tests, a run-log template section, README/CLAUDE.md/ROADMAP lines.
- One first production, watched by the user.

Out:
- A new "video studio" app or service (see decision D1).
- Choices or branching videos. Episodes or series of videos. Long films (over about 5 minutes).
- Lip-synced dialogue spoken inside the Flow clip (open question Q3; dubbed voices in v1).
- Flow's own Scenes timeline, Publish to YouTube, the Studio web panel.
- The humanizer on screenplays (decision D5).
- Translations of the video (later: captions in another language, Gemini voices in Croatian after FMM-10 checks it).

## Decisions made

| # | Decision | Why |
|---|---|---|
| D1 | **The hub skill runs the production**, not a new tool. A new skill `make-video` drives the MCP tools (like `make-visual-novel`), with one small Node script `scripts/video-plan.mjs` for the parts that must be exact: shot plan, cost estimate, budget left, and the `flow_assemble` timeline. | Smallest thing that works. Every step already has a tool. Video costs credits, so a person must OK the budget and Claude must look at the stills before money is spent: an unattended "studio" would hide that. The script keeps the money math and the timing testable. A video studio app is worth it only after a few productions show what repeats. |
| D2 | **No new model role.** The screenplay writer is the writer, architect and line editor with `_sp` prompts, as the VN script writer is (SCP-11 uses `_vn` prompts, no own role). Asked as Q1. | No new agent to hire, no migration of roles.md, the per-book `models` work as they are. |
| D3 | **Screenplay formats carry `script: true` and a new flag `screenplay: true`.** `script` gives them what scripts already have: `SCENE:` places matched to the bible, the tighten text, adaptation through `adapt_book`, the script layout in EPUB and reader. `screenplay` picks the `_sp` prompts, the cue lines and `get_screenplay`. | Reuses the most code. VN Studio lists only its own VN format ids (`vn/reader.ts:75`), so it never offers a screenplay book. |
| D4 | **A sibling tool `get_screenplay`**, not a wider `get_script`. `get_script` refuses a screenplay book and names `get_screenplay`. | The JSON has shots, not beats. VN Studio and the skill keep a stable `get_script`. |
| D5 | **Humanizer off for the screenplay formats** (`humanize: false` in formats.md). | Shot lines are technical, dialogue is short, and the `_vn` guard counts lines in a way that would refuse cue edits. Revisit after the first production. |
| D6 | **Screenplay formats are never picked for a topic-less idea**, only when fixed (add_story `format`, adapt_book) or by a topic of kind `video` / `juvenile-video`. The seed's `## Videos` topics are all switched off. | `formatsForKind(null)` returns every non-article format today (`handlers.ts:101`): the factory would start writing screenplays from generated ideas. |
| D7 | **Dialogue is dubbed** in v1: every line (dialogue and voice-over) is a free Gemini voice (`flow_narrate engine gemini`), one fixed voice per character. Shot prompts ask for "no speech, ambient sound only", and the clips' own sound plays low (clip_volume about 0.3). Asked as Q3. | Free, exact words, same voice every time. In-shot speech is not verified for exact words and would redo paid shots. |
| D8 | **Keyframe first, then video.** Every shot first gets a free Nano Banana keyframe with the shot's characters as references; the paid video uses it as `first_frame: asset:<media_id>`. | Keeps faces and places consistent, lets Claude and the user check every shot for free, and uses only verified paths (asset frames need no upload). |
| D9 | **A free animatic before any credit is spent**: keyframes held for each shot's time + voices (+ music if free) through `flow_assemble`. The user OKs it and the budget. This is the dry run in practice; the script's estimate is the dry run on paper. | The user sees the film before paying for it. |
| D10 | **Budget per production** lives in `runs/<slug>/video/plan.json` (`budget.credits`, `spent`). Each paid call gets `max_credits = min(ceil(estimate x 1.25), budget left, FLOW_MUSIC_MCP_MAX_CREDITS)`. When the next shot does not fit, the skill stops and asks. | The per-call cap exists; the per-production budget does not. Keeping it in the hub needs no flow-music-mcp change. |
| D11 | **`continuous` shots are made as normal keyframe shots in v1.** `flow_continue` / `chain_previous` come in once flow-music-mcp FMM-08 (video identity) and FMM-09 (local frame upload, `chain_previous`) are verified. | Both are on its roadmap as unverified. |
| D12 | **Ticket ids.** Scriptorium `SCP-17_screenplay-writer`. flow-music-mcp **`FMM-12_assemble-timeline`**, not FMM-05: FMM-04 to FMM-10 are already planned there and FMM-11 is HUB-07's VN Studio hooks (`flow-music-mcp/.claude/tickets/FMM-04-10_roadmap-tasks/plan.md`; FMM-05 is jobs-and-recovery). Hub `HUB-11_screenplay-video`. | No clash with the existing ticket list. |

## Open questions for the user (with my recommendation)

1. **Q1 Role.** Reuse the writer, architect and line editor with `_sp` prompts (recommended), or hire a separate `screenwriter` role with its own agent and model chain?
2. **Q2 Formats.** Recommended three: `short-film` (live-action look, 1-3 min), `cartoon` (animated look, 1-3 min), `kids-cartoon` (ages 3-8, 1-2 min, gentle). Aspect 16:9 by default, 9:16 when the brief says "vertical". Want others (music video, explainer, trailer)?
3. **Q3 Dialogue.** Dubbed Gemini voices for every line (recommended for v1, free), or speech inside the Flow clip (lip sync, credits per retake, words not guaranteed)?
4. **Q4 Music.** Flow Music instrumental per `MUSIC:` cue, at most two per short, asked before each song (recommended; cost per song is still unmeasured, FMM-06), or free ACE-Step through comfy-mcp?
5. **Q5 Model and budget for the first production.** Recommended: 60-90 s, 10-15 shots, Omni 1.1 Flash 720p if FMM-09 has verified 720p (else 360p, which is verified), budget 150 credits of the ~1,010. One retake per shot at most.
6. **Q6 First story.** Recommended: adapt *The Lighthouse That Kept Lists* (published short story, warm comedy, Dalmatian island) to `short-film`, which tests the adaptation path. Or an original idea of yours.
7. **Q7 Who writes the screenplay.** Claude as the client writer and architect (`models: {architect, writer: client/claude-code}`, $0), reviewers on the app's models (recommended). This needs a Scriptorium restart, which resumes its factory: OK to restart when phase 3 starts?
8. **Q8 Captions.** Burn captions into the final film (`flow_captions`, style `clean`)? Recommended: yes for voice-over shorts, after you OK the transcript.

## The screenplay format

A screenplay book is a book folder like a visual novel (`book.md`, `bible/bible.md` with looks, `chapters/ch-NN.md`, `outline.md`). A chapter is a **sequence** of the film. The body is read line by line, in this order:

| Line | Pattern | Meaning |
|---|---|---|
| Break | `---` | Fade to black between scenes |
| Scene | `SCENE: <place>, <time>` (or `## <place>`) | A new scene. Place matches the bible's `## Places` |
| Shot | `SHOT (<spec>): <what we see>` | A new shot, one clip. `spec` is a comma list: framing (`extreme wide`, `wide`, `medium`, `two-shot`, `close-up`, `extreme close-up`, `over-the-shoulder`, `pov`, `insert`), camera move (`static`, `pan`, `tilt`, `push-in`, `pull-out`, `tracking`, `handheld`, `orbit`, free words allowed), duration `Ns` (4-10), and the flag `continuous` (picks up exactly where the last shot ended) |
| On screen | `ON SCREEN: Name (look), ...` | Who is in frame, from this shot on, until the next `ON SCREEN` |
| Music | `MUSIC: <mood, instruments, tempo>` / `MUSIC: stop` | A music cue starts at the shot it is in (or the next shot) / ends after the shot it is in |
| Sound | `SFX: <sound>` | A sound in the current shot (goes into the clip prompt) |
| Title | `TITLE: <text>` | A title card, its own 3 s shot |
| Voice-over | `NARRATOR: words` or `NAME (V.O.): words` | Voice-over, not seen speaking |
| Line | `NAME (delivery): words` (`(O.S.)` = off screen) | Dialogue, as in the VN grammar |
| Action | anything else | Added to the current shot's description (before the first shot of a scene: the scene's background) |

Rules for the writer: every scene has at least one `SHOT`; a shot is one continuous camera take of 4-10 s; one to three short spoken lines per shot; the spoken words fit the shot (about 2.5 words a second); present tense; one name per character everywhere.

Example:

```text
SCENE: The harbour wall, dusk
Rain needles the grey water. The lighthouse beam sweeps over the boats.
MUSIC: slow solo piano, melancholic, sparse
SHOT (extreme wide, static, 6s): The pier at dusk, a small figure at its far end, the beam passing over her.
NARRATOR: Every evening, Mara waited for the last boat.
SHOT (medium, slow push-in, 4s): Mara grips the rusted rail, rain running off her hood.
ON SCREEN: Mara (soaked yellow raincoat, worried)
SFX: wind, rain on oilskin
MARA (worried): He said he'd be back before the lamp was lit.
SHOT (medium two-shot, static, 6s): Tomas skids to a stop beside her, out of breath, grinning.
ON SCREEN: Mara (startled), Tomas (out of breath, grinning)
TOMAS (grinning): Did you miss me?
MARA (annoyed): You're *late*.
MUSIC: stop
```

`get_screenplay {book, chapter?}` returns (shape, short):

```json
{
  "slug": "...", "title": "...", "format": "short-film", "aspect": "16:9", "style": "...",
  "runtimeSeconds": 16,
  "characters": [{ "name": "Mara", "looks": "...", "voice": "..." }],
  "places": [{ "name": "Harbour wall", "looks": "..." }],
  "music": [{ "id": "m1", "description": "slow solo piano, melancholic, sparse", "from": "ch01.s01.sh01", "to": "ch01.s01.sh03" }],
  "chapters": [{ "n": 1, "title": "...", "sourceChapters": [1, 2], "scenes": [{
    "id": "ch01.s01", "place": "The harbour wall", "time": "dusk", "background": "Rain needles ...",
    "shots": [{
      "id": "ch01.s01.sh02", "framing": "medium", "move": "slow push-in", "seconds": 4, "continuous": false,
      "action": "Mara grips the rusted rail, rain running off her hood.",
      "cast": [{ "name": "Mara", "look": "soaked yellow raincoat, worried" }],
      "sfx": ["wind, rain on oilskin"], "title": null,
      "lines": [{ "speaker": "Mara", "delivery": "worried", "text": "He said he'd be back before the lamp was lit.", "kind": "dialogue" }]
    }]
  }] }]
}
```

`kind` is `dialogue`, `voice-over` or `off-screen`. A shot without a duration gets 4 s (6 s when its lines need it). Dialogue before any `SHOT` in a scene opens a `medium` 4 s shot. The parser is lenient like the VN one: an unknown line is action.

## Phase 1: Scriptorium screenplay writer (`SCP-17_screenplay-writer`)

Repo `C:\projects\Personal\scriptorium`. Branch `SCP-17_screenplay-writer` from up-to-date `master` (the working copy is on `SCP-15_roadmap` now; do not carry its changes over). Follow the repo's CLAUDE.md: `docs/design.md` Decisions row and History, `yarn seed:hashes` after editing seed prompts, `data-testid` on controls, the demo engine `renderer/demo/fake.ts` if the panel changes.

Checklist:
- [ ] **Format flags.** `src/shared/schemas.ts` format entry: `screenplay: boolean` (default false) and `runtime: [min, max] seconds` (optional). Book frontmatter gets `screenplay: true` beside `script: true` (`handlers.ts:426`).
- [ ] **Formats.** `seed/config/formats.md`: `short-film`, `cartoon`, `kids-cartoon` (Q2), each `script: true`, `screenplay: true`, `humanize: false`, `max_rounds: 1`, `chapters: [1, 3]`, words about `[400, 2000]` (kids `[300, 1200]`, `[1, 2]`), `runtime` `[60, 180]` (kids `[45, 120]`), reviewers `[continuity-checker, developmental-editor, line-editor, beta-reader]` (+ child-safety for kids), guidance text. Explain `screenplay` and `runtime` in the file's body.
- [ ] **Topics.** Kinds `video` and `juvenile-video` in `TOPIC_KINDS` (`src/engine/store/topics.ts:7`), `ui/Topics.tsx`, the `add_topic` enum (`src/engine/mcp/tools.ts`). A `## Videos` section in `seed/topics.md`, all rows off.
- [ ] **Migration.** `migrateScreenplay(dataDir, seedDir)` in `src/engine/store/migrations.ts`, like `migrateNewspaper`: append the three formats when their ids are missing and the `## Videos` section when absent; idempotent; keep line endings; log changes. Wire it in `initDataFolder`.
- [ ] **Format choice.** `formatsForKind(formats, null)` (`handlers.ts:101`) leaves out `screenplay` formats (D6). `start_book` (`handlers.ts:372-377`): a topic-less story that fixes a screenplay format may use it (same rule as the article line); the adaptation sentence says "screenplay" for a screenplay format instead of "visual novel script".
- [ ] **Prompt variant.** `variant()` (`handlers.ts:1151`): `_sp` for `screenplay` (before `_vn`). `loadPrompt` (`src/engine/pipeline/prompts.ts:29`): `_sp` falls back to the plain prompt (never to `_vn`).
- [ ] **Prompts** (new seed files, copied to data folders by the seed): `architect/outline_sp.md` (chapters as sequences with runtime, characters with concrete looks and a voice note, places with looks; same JSON as `outline_vn.md`), `writer/draft_chapter_sp.md` and `writer/rewrite_chapter_sp.md` (the grammar above, the shot rules, the runtime share of the chapter, `{{format_name}}`, places block), `line-editor/review_sp.md` (shot form, lines fit shots, voices, runtime, cinematic clarity: every shot drawable as one picture). Then `yarn seed:hashes`.
- [ ] **Tighten text** (`handlers.ts:277-288`): for a screenplay, "cut action and minor lines, keep every SCENE, SHOT, ON SCREEN and plot beat".
- [ ] **Adaptation.** `Engine.adaptBook` (`src/engine/engine.ts:790`) accepts any enabled `script` format (screenplay included; error text lists both kinds); premise text names the medium. `src/engine/pipeline/adapt.ts`: the intro and review lines name the medium from the format ("a short film screenplay" / "a visual novel script") and, for a screenplay, ask to compress the source into the runtime. `adapt_book` description in `tools.ts:474` lists the screenplay formats.
- [ ] **Parser.** New `src/engine/publish/screenplay.ts`: `parseScreenplay(body, bibleNames)` → scenes with shots (shape above), `musicCues(chapters)`, `runtimeOf(...)`. Reuse `placeAndTime`, `castOf` (export them from `script.ts`), `LINE`, `SCENE`, `CAST` from `xhtml.ts`. Cue keywords (`SHOT`, `MUSIC`, `SFX`, `TITLE`) are tested before `LINE`, because `LINE` would read `SHOT (wide): ...` as a speaker.
- [ ] **Layout.** `src/engine/publish/xhtml.ts` `scriptToXhtml`: with `screenplay`, render `SHOT`, `MUSIC`, `SFX`, `TITLE` as cue lines (not as speakers). Pass the flag from `pipeline/books.ts:396,500`, `epub.ts`, `reader.ts`.
- [ ] **MCP.** `get_screenplay {book, chapter?}` in `src/engine/mcp/tools.ts` (any stage, like `get_script`); `get_script` refuses `screenplay: true` books and points to it. `aspect`: `9:16` when the brief or style says vertical, else `16:9`.
- [ ] **UI.** The book card button (`src/renderer/ui/BookCard.tsx`) "Adapt to visual novel" becomes "Adapt to script"; the Script writer panel's format select lists the screenplay formats too. Demo engine and `tests/renderer/scriptwriter.spec.ts` updated.
- [ ] **Docs.** New `docs/screenplay.md` (the contract: files, grammar, JSON, what is guaranteed, adaptation), `docs/mcp.md` (`get_screenplay`, `adapt_book`), `docs/visual-novel.md` (one line: `screenplay: true` books are not visual novels), `docs/design.md` Decisions row "Screenplay writer" + History, `ROADMAP.md` (the Planned item moves to done, follow-ups added).

Tests (vitest, `tests/screenplay.test.ts` unless noted):
- Parser: the example above gives 1 scene, 3 shots, cast carried, music cue m1 from sh01 to sh03, `runtimeSeconds` 16; `SHOT` never parsed as a speaker; `NARRATOR` and `(V.O.)` give `voice-over`, `(O.S.)` gives `off-screen`; a shot without duration gets 4 s, or 6 s when its lines need it; dialogue before any SHOT opens an implicit shot; bible names are applied; unknown lines become action.
- `variant` returns `_sp`; `loadPrompt` falls back from `_sp` to plain.
- `formatsForKind(null)` excludes screenplay formats; a topic-less story that fixes `short-film` starts as `short-film`.
- `migrateScreenplay` adds the formats and the section once, keeps CRLF, changes nothing on a second run.
- `adaptBook` with `short-film` creates the story; with a non-script format it is refused (extend `tests/adapt.test.ts`).
- `get_screenplay` and the `get_script` refusal (extend `tests/mcp.test.ts`).
- End to end on mock providers: a `short-film` story runs to `published`, the EPUB lays out cue lines, `get_screenplay` parses it (pattern of `tests/newspaper.test.ts`).
- `scriptToXhtml` with `screenplay` renders cue lines (extend `tests/script.test.ts`).

Acceptance:
- `yarn typecheck`, `yarn lint`, `yarn test` (compare any failure against master: there are known timing flakes), `yarn test:ui`, `yarn build` all pass.
- The seed-hash test passes.
- No live run in this phase (the live screenplay is written in phase 3).

## Phase 2: production step

Two branches. They can be built in parallel with phase 1: phase 2 is tested with a hand-written `get_screenplay` JSON fixture.

### 2a. flow-music-mcp `FMM-12_assemble-timeline`

Repo `C:\projects\Personal\flow-music-mcp`. Branch from up-to-date `master`, stacked on the newest merged or open FMM ticket that touches `src/flow/assemble.ts` / `local-tools.ts` (FMM-04 brings vitest; FMM-10 runs `flow_assemble` live). Add FMM-12 to the umbrella list in `.claude/tickets/FMM-04-10_roadmap-tasks/plan.md`. Write `.claude/tickets/FMM-12_assemble-timeline/plan.md` from this section. No credits: everything here is local ffmpeg.

What flow-music-mcp is missing for a screenplay:

| Need | Today | Where |
|---|---|---|
| Stills as shots (animatic, title cards) | Must be turned into clips by hand ("ffmpeg -loop 1 ...") | FMM-12 |
| Trim a clip to the shot's length | Whole clips only | FMM-12 |
| Several music cues at set times, with fades | One `music` file looped over the whole film | FMM-12 |
| Music lower while someone speaks | Fixed `music_volume` | FMM-12 (`duck`) |
| Assembly with music and several voice lines, `dir` + `out` | Never run | FMM-10 (FMM-12 runs it too if FMM-10 is not done) |
| `first_frame: asset:<id>` for a keyframe made in the same project | Works (verified with assets) | none |
| Characters as `reference_images` of an image | Implemented, not verified with a character | phase 2 free check, note in its ROADMAP |
| Local `first_frame`, `chain_previous` | Not verified | FMM-09 (not needed in v1, D11) |
| A stable id for a finished video (for `flow_continue`) | Found by title, titles repeat | FMM-08 (not needed in v1, D11) |
| 720p, Veo | Quoted, never generated | FMM-09 (Q5) |
| Cost of a Flow Music song | Unknown | FMM-06 (Q4) |
| A quote without generating (dry run) | None; the quote is checked at Start | Not needed: the hub script estimates, the live quote guards each shot. Optional later `flow_quote`. |

Checklist:
- [ ] `flow_assemble` `clips` items may be a path (as now) or an object: `{file, from?, to?}` (trim a video) or `{image, seconds, zoom?}` (a still held for `seconds`, optional slow zoom-in; silent audio). `src/flow/assemble.ts` (`AssembleOptions`, the filter graph) and the zod schema in `src/flow/local-tools.ts`.
- [ ] `music_cues: [{file, at, until?, volume?, fade_in?, fade_out?}]`: each cue starts at `at`, loops or is cut to `until` (default: the film's end), fades (defaults 1.5 s in, 2 s out). Replaces `music` when given; `music` stays for a single bed.
- [ ] `duck: true` (default false): music ducks under the voice track (`sidechaincompress` keyed on the voice). Without voice it does nothing.
- [ ] The result lists each placed clip with its start time (`timeline: [{index, file, at, seconds}]`), so the caller can check the voice timing.
- [ ] Pure helpers (the filter-graph builder, clip-time math) in a module with no side effects; vitest tests for them: still + trimmed clip + video concat times; two music cues with fades; duck on/off; a `voice_lines` + `music_cues` graph.
- [ ] Live, free: assemble 3 stills + 1 trimmed video + 2 music cues + 4 voice lines (Gemini or Windows voices, local test audio) with `dir` + `out`; check with ffprobe (duration, streams) and by ear on one listen by the user if they want.
- [ ] README tool table, CLAUDE.md "Verified", ROADMAP (tick FMM-10 assembly items if run here; "Later → Screenplay → video" points to the hub ticket), `changelog.md`.

Acceptance: `yarn build`, `yarn test` pass; the live assembly above produces a playable MP4 with the cues at the right times (ffprobe + one waveform or `astats` check per cue start).

### 2b. Hub `HUB-11_screenplay-video`

Repo `C:\projects\Personal\creative-hub`. Branch `HUB-11_screenplay-video` from up-to-date `master` (the working copy is on `HUB-01_roadmaps-to-repos` with uncommitted edits to the skill, CLAUDE.md, README and ROADMAP: merge HUB-01 first, or stack on it and say so in the PR).

**`scripts/video-plan.mjs`** (Node 24, no dependencies; run as `fnm exec --using=24 node scripts/video-plan.mjs <cmd> <run dir>`). It reads and writes `runs/<slug>/video/`:
- `plan <dir> [--budget N] [--model omni-720p|omni-360p|veo-lite|veo-fast] [--aspect 16:9|9:16]`: reads `screenplay.json` (the `get_screenplay` output), writes `plan.json`: one entry per shot (`id`, `seconds` raised to the next of 4/6/8/10 when its lines need it, keyframe prompt, video prompt, `refs` = up to 3 characters in the shot, `lines` with the character's voice, estimate), title cards as stills, music cues, a voice per character (from a fixed Gemini voice list, by the bible's voice note and gender words, overridable in `plan.json`), `budget {credits, spent: 0}`. Prints the dry run: shots, runtime, credits per shot and total, a 25% retake reserve, the budget and the last known balance. Warnings: dialogue longer than its shot after raising, more than 3 people in a shot, `continuous` shots (made as normal shots, D11), runtime outside the format's range.
- `estimate <dir>`: prints the dry run again from `plan.json` (after hand edits).
- `next <dir>`: the next shot to make, with its `max_credits` (D10), or "budget reached".
- `record <dir> <shot id> <json>`: stores a result (keyframe media id and file, clip file, credits spent, voice files) and updates `spent`.
- `timeline <dir> [--animatic]`: writes `assemble.json`, the `flow_assemble` arguments: `clips` in order (keyframe stills with `seconds` for the animatic, video clips trimmed to `seconds` otherwise, title cards as stills), `voice_lines` (`at` = shot start + 0.3 s, lines in a shot one after another with 0.25 s gaps, durations from ffprobe when present, else 2.5 words/s; `max_seconds` for dialogue), `music_cues` from the cues' shot ranges, `clip_volume` 0.3, `duck: true`, `output_name` `animatic` or `final`.
- Price table at the top of the file, each price marked `seen` or `guessed`: Omni 1.1 Flash 360p 4 s = 4 (seen), 720p 8 s = 12 (seen as x2 = 24), other durations pro rata (guessed), Veo 3.1 Lite 10, Fast 20, Quality 100 per 8 s clip (seen as quotes); images, Gemini and Windows voices, assembly 0. Update it when FMM-09 measures more.

**`scripts/video-plan.test.mjs`** (`node --test scripts/`), with `scripts/fixtures/screenplay-harbour.json` (the example above as `get_screenplay` JSON):
- shot durations raised to fit lines; the estimate total for 360p and 720p; the retake reserve; warnings for long dialogue and >3 people;
- `next` gives `max_credits = min(ceil(est x 1.25), budget left, cap)` and "budget reached" when it does not fit;
- `record` adds to `spent`, idempotent for the same shot and file;
- `timeline` voice `at` times, music cue times, still vs clip entries, animatic vs final.

**`.claude/skills/make-video/SKILL.md`** (new). Steps:
0. Before: `hub.ps1` status; `hub.ps1 start flow-music-mcp`; `flow_status` (signed in, credits, upload rights); open `runs/<slug>.md` from the template; agree the brief (format, aspect, length, dialogue mode, music source, video model, credit budget; defaults from Q2-Q5).
1. Screenplay. A: Scriptorium `add_story {format: short-film|cartoon|kids-cartoon, ...}` or `adapt_book {book, format}`, with Claude as client writer if agreed; wait with `wait_for_book` (or `scripts/wait-book.ps1`); then `get_screenplay {book}` saved to `runs/<slug>/video/screenplay.json`. B (no Scriptorium): write `screenplay.json` yourself in the same shape.
2. Plan and dry run: `video-plan.mjs plan`; show the user the estimate; agree the budget. Nothing is spent.
3. Cast (free): one Flow project per production (`project: <slug>`, `create_project: true`); `flow_character_create` per main character from the bible looks, with the same voice name as its Gemini voice.
4. Keyframes (free): `flow_generate` images, one per shot (style + place looks + framing + action + cast looks; `reference_images` = the shot's characters as `asset:<name>`); Read each image; regenerate bad ones; `record` media ids.
5. Voices (free): `flow_narrate engine gemini` per line, voice per character, `style` from the delivery; `record` files.
6. Animatic (free): `video-plan.mjs timeline --animatic`, `flow_assemble` with `assemble.json`; the user watches it and OKs the film and the budget, or asks for changes (edit `plan.json`, redo keyframes or lines).
7. Video (credits): loop `next` → `flow_generate {type: video, first_frame: asset:<keyframe media id>, prompt: motion + "no speech, ambient sound only: <sfx>", model, duration, resolution, aspect_ratio, max_credits}` → `record`; one shot at a time; check a frame of each clip (extract with ffmpeg and Read it); at most one retake per shot; stop and ask when `next` says the budget is reached. Log every credit in the run log.
8. Music: per cue `music_generate {instrumental: true, sound: <cue>, format: "wav"}` after asking (credits), or comfy-mcp `generate_music` (free); `record`.
9. Assemble: `video-plan.mjs timeline`, `flow_assemble`; optional captions (`flow_transcribe` → user OKs the words → `flow_captions`).
10. Finish: give the user the MP4 path (PowerShell form); only the user says it is done; update the run log and any tool roadmap.
Plus "Things that go wrong": Flow high demand (wait, no blind retries), a refused quote (over `max_credits`: nothing spent), the 15 s `hub.ps1 call` timeout (use `wait` + `flow_wait`), a missing tool after a server start (`/mcp`).

**Other hub files:**
- [ ] `CLAUDE.md`: "For a short film, cartoon or video from an idea or a book, use the `make-video` skill." Credits rule: video spends Flow credits, agree a budget first.
- [ ] `README.md`: the chain diagram gets the video branch; Scriptorium's row says "screenplays"; `scripts/` lists `video-plan.mjs`.
- [ ] `runs/_template.md`: a "Video" block (format, aspect, model, budget, spent, Flow project, plan path).
- [ ] `ROADMAP.md`: "Plans across tools → Screenplay → video" points to this ticket and its phases; the Scriptorium and flow-music-mcp rows list SCP-17 and FMM-12.
- [ ] `make-visual-novel` SKILL.md: one line pointing to `make-video` for videos.

Acceptance for phase 2 (no credits, no Scriptorium restart):
- `node --test scripts/` passes.
- With flow-music-mcp FMM-12 built and running: the fixture screenplay goes through steps 2-6 of the skill: plan and estimate printed, 3-4 keyframes and the voices made for free, an animatic MP4 assembled, `spent` is 0. Characters as image references are checked once here (free) and the result goes into flow-music-mcp's CLAUDE.md.

## Phase 3: the first production

Branch: none new for code; the run log and run files are committed on `HUB-11_screenplay-video` (or a follow-up branch if HUB-11 is merged by then).

Needs the user's go-ahead for: the Scriptorium restart (Q7), the credit budget (Q5), each Flow Music song (Q4).

- [ ] Build and restart: `hub.ps1 build scriptorium` (with SCP-17 merged or checked out), stop and start it with the user's OK, reconnect `/mcp`; `hub.ps1 build flow-music-mcp` with FMM-12, start it.
- [ ] `runs/<slug>.md` from the template; brief agreed (Q2-Q6, Q8).
- [ ] Screenplay: `adapt_book {book: the-lighthouse-that-kept-lists, format: short-film, models: {architect, writer: client/claude-code}}` (or the agreed story). Claude answers the client tasks; reviewers run on app models. Published; `get_screenplay` saved. Check: every scene has shots, runtime in range, places match the bible.
- [ ] Steps 2-6 of the skill: estimate shown, animatic made, the user watches it and OKs the budget.
- [ ] Step 7: the video shots within the budget; credits before and after recorded in the run log (`flow_status`).
- [ ] Step 8: music, asked per song.
- [ ] Step 9: the final MP4 (and captions if agreed).
- [ ] The user watches it. Their verdict goes in the run log. Limits found go to each tool's `ROADMAP.md`.

Acceptance: a finished MP4 in `runs/<slug>/video/`, spent ≤ budget, the run log has every id (story, book, Flow project, media ids via `plan.json`, files, credits), and the user has watched it.

## Verification summary

| What | How | Spends |
|---|---|---|
| Scriptorium parser, formats, migration, MCP, adaptation, layout | vitest + Playwright, `yarn typecheck/lint/test/test:ui/build` | nothing |
| flow-music-mcp assembly | vitest; one local ffmpeg run checked with ffprobe | nothing |
| Hub planner | `node --test scripts/` | nothing |
| Free path (keyframes, voices, animatic) | the fixture through skill steps 2-6 | nothing (Flow images and Gemini voices are free) |
| Screenplay written by Scriptorium | phase 3, after the user's OK to restart (factory resumes) | $0 with the client writer; app models for reviews |
| Video shots, music | phase 3, within the agreed budget, asked per song | Flow credits (budget, default 150), Flow Music credits |
| The film is good | the user watches it | |

Not verifiable by Claude: how the film looks and sounds as a whole, and how the new Scriptorium button and panel look. The user checks those.

## Status

- [ ] Phase 1 SCP-17 (Scriptorium)
- [ ] Phase 2a FMM-12 (flow-music-mcp)
- [ ] Phase 2b HUB-11 (hub skill and planner)
- [ ] Phase 3 first production, watched by the user
