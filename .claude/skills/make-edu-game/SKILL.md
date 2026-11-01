---
name: make-edu-game
description: Turn a topic into a playable educational game (quiz arena, encyclopedia explorer, MindMaze castle, RPG quest, language role-play, detective / escape room) by driving Edu Studio over MCP - a team of roles researches the topic into a sourced fact base, writes articles and items with explanatory feedback, checks the facts, makes pictures, music and voices through the hub's generators, builds a file:// game and plays it with an autoplay bot. Use when the user asks for an educational game, a quiz, a course, a language-learning game, a study game or an Encarta/MindMaze-style game. For a story, a visual novel or a picture book use make-visual-novel; for a film use make-video.
---

# Make an educational game

The hub is `C:\projects\Personal\creative-hub`. Edu Studio is `C:\projects\Personal\edu-game-studio` (public repo `Tihi321/edu-game-studio`), MCP on port 7463, data in `~\EduGames`. Its own guide is the source of truth: `docs\mcp-guide.md` in that repo (also served as the MCP resource `edu-studio://guide`); the player contract is `docs\player.md`.

## 0. Before you start

1. `pwsh -File scripts\hub.ps1` (status). Start the studio with `pwsh -File scripts\hub.ps1 start edu-studio`. If the tools are missing from your list, the server was down when the session began: start it, then ask the user to reconnect (`/mcp`) or call tools through `pwsh -File scripts\hub.ps1 call edu-studio <tool> '<json>'`.
2. Never start Scriptorium for this (it resumes its whole book factory). A long frame story is optional (`story: scriptorium`) and is skipped when Scriptorium is down.
3. Open a run log `runs/<slug>.md` (copy `runs/_template.md`): the course slug, every decision, what you checked.
4. Agree briefly, only if the user did not say: topic, audience and age, language(s) (a language course has `targetLang` and `cefr`), length (`format`: `quick` 2 units, `standard` 4, `deep` 6, or for a language course `language-a1|a2|b1|b2`, chosen from `cefr`; C1 and C2 are not available), shells, who does the model work (default: you, $0, `model: "client/claude-code"`).
   Language courses: `languages: ["hr","en"]` makes two editions in one run (a translator step with the client model), `targetLang: "de"` for German. Verb units hold `conjugation` items (typed forms; umlaut and ss tolerance such as Maedchen / Strasse, no typo tolerance for forms; a missing umlaut is wrong). B2 is a reading course: reader view with tap-to-gloss, vocabulary cards harvested from the texts, and writing/speaking only as self-check cards with a model answer (no auto-grading).
5. Voices: the hub's voice rule applies. Gemini TTS has a free quota of 10 requests a day; Croatian goes first on Google voice, English and the rest on local VibeTTS when the quota would be exceeded. Edu Studio's voice step (`media.voice.provider: auto`) applies the rule itself and counts the quota; do not start VibeTTS unasked. German listening clips go to local VibeTTS (Gemini's 10 requests cannot cover a course) and narration is off by default for language courses; run `edu_voice_status` first to see which providers read `de`.
6. Flow credits (images, songs) are spent only when the course sets `media.art.provider: flow` or music through Flow Music; agree a budget first (default 150) and keep the default free providers (ComfyUI, Pixel Studio, Chiptune Studio).

## 1. Make the course

```
edu_run_pipeline {brief: {topic, audience, age, sourceLang, targetLang?, cefr?, format?, units?, shells: ["quiz-arena","encyclopedia","mindmaze","rpg"], story: "frame"|"none", model: "client/claude-code"}}
```

The pipeline enables the quiz arena, encyclopedia, MindMaze and RPG shells (automatic layouts); role-play and detective need authored sections (`edu_course_edit` on `shells.config.roleplay` / `.detective`, see `docs\player.md`), so they are recorded and not enabled.

With `client/claude-code` every model call waits for you: loop `edu_get_task` -> do the role's work exactly as the task text says (JSON only) -> `edu_submit_task {taskId, text}` until `edu_wait {slug}` says the run is done or blocked. Research: search the web yourself and answer with short paraphrased excerpts attributed to named pages; every fact needs a source; the fact-checker must pass. `edu_status {slug}` shows every step, failures and what to do next.

## 2. Check and play

- `edu_lint {slug}` must have 0 errors (warnings: read them; a PLACEHOLDER_ASSET warning means a picture or clip is a stand-in).
- The pipeline's playtest runs the autoplay bot; to rerun it by hand: `node scripts\play.mjs courses\<slug>\build --mode perfect|wrong|random --shell <id>` in the studio repo (needs Playwright Chromium).
- Open `~\EduGames\courses\<slug>\build\index.html` (works from `file://`). **A production is done only when the user has played it.** Say what you verified and what you did not (real audio, touch, a human playing).

## 3. After the first build

- Pictures, music, voice: `edu_asset_plan`, `edu_music_plan`, `edu_voice_plan` and their generate tools (see the guide: "Pictures", "Music and sound effects", "Voice"); placeholders stand in when a generator is down and `edu_asset_generate` replaces them later.
- Editions (a second UI/text language): translate only the course text catalog with Book Translator (the same seam as the VN pack, HUB-16); build the edition and run the bot on it.
- Later features, each documented in the repo: speaking practice (`docs\speaking.md`), Android app (`edu_android_prepare`), classroom mode (`edu_class_assign`, `edu_class_report`), live multiplayer quiz on the LAN (`edu_live_start`, which asks before opening the LAN).

## Rules

- Nothing private goes into the repo (it is public): no keys, no `~\EduGames` data.
- Every run ends with a DONE / NOT DONE / UNTESTED list.
