---
name: make-visual-novel
description: Turn an idea or theme into a finished, playable visual novel (linear or with choices) by chaining the user's local tools over MCP - Scriptorium writes the book, Book Translator translates it, VN Studio plans and generates the art, music and voices (through ComfyUI, Pixel Studio, Chiptune Studio and VibeTTS) and builds the Ren'Py game. Use when the user gives a story idea, theme or premise and wants a visual novel, gamebook-style choice novel, illustrated story, or any of its parts (book only, translation, art, music, voices, build), or wants to continue or fix a production in runs/.
---

# Make a visual novel

The hub is `C:\projects\Personal\creative-hub`. `README.md` there maps every repo, port and data folder; `services.json` is the machine-readable registry. Read the README once if anything below is unclear.

## 0. Before you start

1. Run `pwsh -File scripts\hub.ps1` (status). Start what the run needs with `pwsh -File scripts\hub.ps1 start [ids]`. The default `start` brings up vn-studio, pixel-studio, chiptune-studio, book-translator, comfyui, comfy-mcp, lmstudio, vibetts. Scriptorium is never started by default: it resumes its whole factory (it writes every open idea in `~/Scriptorium/ideas`, maybe with paid models). Ask the user before `start scriptorium -Force`.
2. If an MCP tool is missing from your tool list, the server was down when the session started. Start it, then ask the user to reconnect it (`/mcp`) or restart the session. Until then call any tool through the hub: `pwsh -File scripts\hub.ps1 call <service> <tool> '<json args>'` (or `@args.json` for long arguments; it prints the JSON result). `hub.ps1 check` confirms each server answers.
3. Open a run log: `runs/<slug>.md` (copy `runs/_template.md`). Write every id you get (story slug, book slug, translator project id, VN project slug), each decision, and what you checked. A later session resumes from this file.
4. Agree with the user, briefly and only if they did not say: linear or with choices, for adults or children, language(s), art style (illustrated or pixel), voices on or off. Defaults: linear, adults, English, illustrated, voices off.
5. Agree who does the model work: the apps' own models (LM Studio, Strata or paid APIs), or **you**. See "Doing the model work yourself" below.

## Doing the model work yourself (no LM Studio, $0)

Scriptorium, VN Studio and Book Translator have a provider `client` with the model `client/claude-code`. A model request sent to it does not go to any model. It waits until you take it over MCP and answer it, then the app carries on as if a model had answered. Nothing is spent. It needs the branches SCP-08 / VNO-05 / BTT-09 (until merged), built and restarted.

**Setup, once per data folder.** Each app's `config/providers.md` needs the provider. The seed has it disabled, and existing data folders do not get it automatically:
```yaml
- id: client
  kind: client
  local: true
  concurrency: 8
  models:
    - id: claude-code
      vision: true
```

**Choose what you do, per book or project.** Never change the global role lists, or every book waits for you:
- Scriptorium:
  - `add_story {..., models: {writer: "client/claude-code"}}` sets the model from the start. Add `architect`, `editor-in-chief` and the reviewers if you do those too.
  - `set_book_model {book, role, model}` sets it on a running or rejected book. `model: null` removes it.
  - Roles: editor-in-chief, architect, writer, researcher, archivist, and the reviewers (continuity-checker, developmental-editor, line-editor, copy-editor, beta-reader, originality-checker, plus child-safety-reviewer, read-aloud-reviewer and fact-checker in some formats). The publisher makes no model call.
- VN Studio: `vno_update_settings {slug, models: {<role>: "client/claude-code"}}`. Roles: script-analyst, art-director, composer, stage-director, voice-director, edition-aligner, art-critic (it sends images), director. The Pixel Studio draw loop (`pixelProvider: pixel-studio-draw`) times out with `client`: draw sprites yourself with pixel-studio and `vno_asset_replace` instead.
- Book Translator: `create_project` or `update_project_settings` with `agentModels: {translator|glossary|proofreader|qa: ["client/claude-code"]}`. The CLI `translate` refuses such a project.

**The loop.** Run it until nothing waits.

| | Scriptorium | VN Studio | Book Translator |
|---|---|---|---|
| What waits | `list_client_tasks`, `factory_status.clientTasks` | `vno_client_tasks`, `vno_status`, `vno_wait` (returns when a task waits) | `list_client_tasks`, `wait_for_progress` (returns when a task waits) |
| Take one | `get_client_task {book?, role?, task?}` | `vno_get_task {…}` | `get_client_task {project?, role?, task?}` |
| Answer | `submit_client_task {taskId, text}` | `vno_submit_task {…}` | `submit_client_task {…}` |
| Give back | `release_client_task {taskId}` | `vno_release_task {…}` | `release_client_task {…}` |

- A task gives `system`, `user`, an optional `schema` and an `output` rule. Follow `output` exactly: one JSON object matching the schema; or the text only; or, in Book Translator, the `<seg id>` segments with every tag kept.
- A JSON answer is checked when you submit it. `accepted: false` comes with `problems`: fix them and submit again; the task stays yours.
- A task is held for you for 30 minutes, then goes back to waiting. "Task not found" means the job was stopped, answered or restarted: take the next one.
- Answer in the role's voice and to its brief. A writer's chapter must meet the word range in the prompt, and a reviewer must really review (honest scores and verdict), or the quality gate means nothing.
- Big runs: start several subagents, each taking tasks with its own `role` or `book` filter. Tasks are handed out one at a time, so two never get the same one.
- After the run, remove your model from the book or project (`set_book_model ... null`, or settings back), or later work on it waits for ever.

**A rejected Scriptorium book** gets another round with `reopen_book {book, mode: "rewrite" | "review", chapters?}`. That is different from `retry_book`, which is for `failed`. Set `set_book_model` first if you will write the rewrite.

## 1. Write the book (Scriptorium)

Two ways. Pick A unless the user wants it fast or Scriptorium is not available.

**A. Scriptorium writes it** (best quality, slow: tens of minutes to hours).
- `scriptorium.add_story` with `title`, `premise`, `plot`, `characters` [{name, role, description}], `setting`, `style`, and `format`: `visual-novel` (linear), `choice-visual-novel` (choices and several endings), `kids-visual-story` or `kids-choice-visual-story` (ages 6-9). Put the looks of each character and place in `characters[].description` and `setting`: they become the art reference in the bible.
- Series: `add_series {title, premise, characters, setting, style, genre, format}` makes a series (file `~/Scriptorium/series/<slug>.md`); `add_story {..., series}` adds the next book (`series_index` is set automatically; a later book waits until the earlier one is published and gets the earlier books' summaries, cast end-states and open threads in its prompts); `list_series` / `get_series {series}` show the books in order. To let the user watch it write, start it with `pwsh -File scripts\hub.ps1 start scriptorium -Force -Window` (window open, MCP still on).
- **Adapt an existing book** (no new story needed): `adapt_book {book: <published book slug>, format: "visual-novel" | "choice-visual-novel", title?, notes?, models?}`, or the "Adapt to visual novel" button on a published book in Scriptorium's Library. The adaptation keeps the source's plot, cast and looks (the bible is seeded from the source), maps each script chapter to source chapters, skips research, and with choices keeps the book's ending as one canon path. Then go on to step 3 with the adaptation's book slug. Needs Scriptorium SCP-11 (merged after SCP-10).
- Every chapter gets a **humanizer** pass after drafting (role `humanizer`, on by default; `add_story {humanize: false}` turns it off for one book). Set it to `client/claude-code` with `models: {humanizer: ...}` if you do that work yourself.
- Scriptorium also writes **newspaper articles** (formats `article` / `feature-article`, topics in the `## Newspaper` section, published as `out/article.html`; Newspaper tab; `list_articles`). Not part of the VN chain, but the same story/task loop.
- `list_stories {status: open}` first: other open ideas compete with yours (max 3 books in progress).
- The story slug is not the book slug. Run `pwsh -File scripts\wait-book.ps1 -Story <story-slug>` in the background; it prints each stage and ends with the book folder when the stage is `published` (exit 1 on failed or rejected; then `get_book`, `read_book_file notes`, and `retry_book` for failed or `reopen_book` for rejected). If you do the writing yourself (`add_story {models}`), work the task loop instead of only waiting.
- Steer while it writes with `add_book_note {book, text, chapter?}`. Rate the result with `rate_book`.

**B. You write it straight into VN Studio** (minutes, no Scriptorium, no book folder). Write the story as JSON and call `vn-studio.vno_create_project {book, lang?, settings?}`; it returns the project `slug`, and you skip `vno_import` in step 3. The JSON shape, the beat forms and the ids are in `C:\projects\Personal\visual-novels-orchestrator\docs\mcp-guide.md` ("Write the story yourself"). In short:
- `book`: `{title, slug?, genre?, coverBrief?, characters: [{key, name, looks}], places: [{key, name, looks}], chapters: [{title, choices?: [{text, to: <chapter n>}], ending?, scenes: [{place: <key>, time?, description?, beats}]}]}`. Pass `slug` when the title is not in Latin letters.
- Beats: `{cast: ["mara", "tom"]}` (who is on screen from here on, at most three), `{speaker: "mara", expression: "happy", text}`, `{text}` (narration).
- Linear: no chapter has choices. With choices: every chapter has `choices` or is an ending (`ending` text). Chapters are numbered by position.
- The language is detected from the text (or pass `lang`, any code from `vno_languages`).
- Check it with `vno_get_story {slug}`, fix it with `vno_story_edit {slug, ops}` or the one-op tools (`vno_beat_add`, `vno_beat_update`, `vno_scene_update`, `vno_character_set`, `vno_chapter_update` ...). Ids never change: scenes `ch01.s02`, beats `ch01.s02.b003`.
- A book folder in the Scriptorium layout still works too (`runs/<slug>/book/` + `vno_import`): grammar in `C:\projects\Personal\scriptorium\docs\visual-novel.md`, example `...\visual-novels-orchestrator\tests\fixtures\books\soother\`. Use it when Book Translator should translate the script (it reads book folders, not VN Studio projects).

Either way, the bible is what keeps the visuals consistent: every character and place needs a full, fixed description (face, hair, clothes, colours; place layout and light). Use one name per character everywhere. Expressions in speaker brackets should be one of: neutral, happy, sad, angry, surprised, worried, scared, thinking (VN Studio maps others to these).

## 2. Translate (optional)

- **The reader book** (EPUB): `book-translator.create_project {sourcePath: <abs path to books/<slug>/out/<slug>.epub>, targetLanguage}` (add `clientOnly: true` when you do all the model work yourself: glossary, translator, proofreader and QA then go only to `client/claude-code`, nothing outside; needs BTT-10), then `start_translation`, then loop `wait_for_progress` until `done`, then `export_project` (returns the absolute output path). Any of its 32 languages.
- **A story written straight into VN Studio (1B JSON)**: translate the text yourself and write it with `vno_edition_set {slug, lang, title, chapterTitles: {"1": ...}, choiceTexts: {"1:0": ...}, endings: {"2": ...}, characterNames: {key: ...}, beats: {<beat id>: text}}` (the ids come from `vno_get_story`; the result lists what is still missing).
- **The visual novel edition** (VN Studio takes the 37 languages in `vno_languages`): give Book Translator the book folder itself (`~/Scriptorium/books/<slug>` or `runs/<slug>/book/`), never a single `.md` file (the Markdown adapter merges lines and breaks the script).
  1. `book-translator.analyze_file {sourcePath: <abs book folder>, targetLanguage}`: `file.format` must be `vn` (a plain folder is refused). Check the cost estimate.
  2. `create_project {sourcePath: <abs book folder>, targetLanguage}`, `start_translation`, loop `wait_for_progress` until `done`, then `export_project {projectId, outPath: <abs runs/<slug>/book-<lang>>}`. It writes a folder with the same files and the same lines: titles, summaries, choice texts, endings, the blurb, narration, spoken text and the place/time after `SCENE:` are translated; `SCENE:`, `ON SCREEN:` lines, speaker tags with their expressions, `---`, frontmatter keys, `bible/bible.md` and `cover-brief.md` stay as they are. Character names stay (the project's glossary starts with them).
  3. To translate it yourself instead (no app models, nothing spent): `create_project` with `enabledAgents: {glossary: false, proofreader: false, qa: false}`, `prepare_chunks`, then loop `get_translation_task` / `submit_translation`. A spoken line comes as `<1>PETRA (grumpy):</1> words`: keep the tag exactly, translate only the words, in the speaker's grammatical gender. Then `export_project` as above.
  4. `vno_add_edition {slug, source: <the exported folder>, lang}` (`lang` may be left out: it is detected) and check its report (expect `missing: []`, `extra: []`, no warnings); fix single lines with `vno_update_beat`. `get_project` lists any line the export kept in the source language (a "warn: ... the source text was kept" log line).
  - Needs Book Translator from branch `BTT-08_vn-script-adapter` (until it is merged) built with `hub.ps1 build book-translator` and restarted. If `analyze_file` says the folder is unsupported, the running engine is older.

## 3. Make the visual novel (VN Studio)

1. `vno_import {source}`: the Scriptorium book slug (it reads `~/Scriptorium/books`; `vno_set_library {path}` points it elsewhere) or the absolute path of a book folder. Returns the project `slug`. Skip this for a project made with `vno_create_project` (1B).
2. `vno_update_settings {slug, ...}` before generating:
   - `art: {style: "illustrated"}` (ComfyUI, qwen-image-2.1) or `art: {style: "pixel", pixelProvider: "pixel-studio"}` (pixel art through Pixel Studio; `pixel: {width, height}` default 320x180).
   - `music: {provider: "comfy"}` (ACE-Step, orchestral or any genre) or `music: {provider: "chiptune", chip: "nes"|"gb"|"genesis"|"snes"|"pce"}` (Chiptune Studio, the default for pixel books). `tracks` sets how many.
   - `voice: {enabled: true}` only if wanted; then `vno_voice_status`, `vno_voice_plan`, and the user may pick voices with `vno_voice_set`.
   - `theme`: see `vno_themes`.
   - To steer the art and music before anything is generated: `vno_plan {slug, wait: true}` writes the prompts only; then `vno_asset_set {slug, id, prompt}` for any you want to write yourself (kept by later runs), `vno_set_music {slug, menu, chapters: {"1": "music_02"}}` and `vno_set_cues {slug, scenes, casts}` (transitions, who stands left/center/right).
3. `vno_run_pipeline {slug}` (returns job ids at once), then `vno_wait {slug, timeoutSeconds: 240}` in a loop (Claude Code aborts an MCP call that is silent for 300 s, so stay under it), reporting `vno_status` progress to the user. Steps: analyse, art, music, generate, voice, stage, build, lint. Restart from any step with `from`.
4. Review: `vno_asset_list {slug}`. Look at the image files (Read them) for the character sheets (`sheet_<char>`) and the cover first, then sprites and backgrounds. Fix with `vno_asset_regen {id, prompt?, seed?}`, pick an earlier version with `vno_asset_pick`, and `vno_asset_lock` the good ones so a re-run keeps them.
5. Your own assets: make them anywhere and `vno_asset_replace {slug, id, file}` (absolute path, no post-processing: sprites must be transparent PNG/WebP about 972 px tall; backgrounds 1920x1080).
   - Pixel Studio: `import_image {path, palette, maxColors}` on a ComfyUI render, then `export_png {path, width, height}`.
   - Chiptune Studio: `compose_track {mood, chip, bpm, key, bars, seed}` then `render_audio {path, format: "ogg"}` (loops exactly; VN Studio plays the loop). Use one chip, key and instrument set for the whole book, and `save_as_asset` + `place_asset` for a recurring theme.
   - VibeTTS: `synthesize_to_file {text, voice, lang, format}` for extra clips (Kokoro `af_*`/`am_*` English only; `supertonic:F1`-`M5` any language).
   - comfy-mcp (ComfyUI directly): `generate_image {prompt, engine, width, height, out}` for CGs and extra art, `edit_image {prompt, image, out}` to change an existing sprite or CG while keeping the subject, `remove_background {image, out}` for a transparent sprite, `generate_music {tags, engine, seconds, out}`, `generate_speech {text, language, voice_ref, out}`. Pass absolute `out` paths. A call returns the paths, or a job id after its `wait` seconds (default 45); then `wait {job_ids}`.
   - Google Flow and Flow Music are both in **flow-music-mcp** (`hub.ps1 start flow-music-mcp`; one Chrome profile, signed in once with `yarn login` in its repo). flow-mcp is retired.
   - Google Flow (`flow_*`): call `flow_status` first (sign-in, credits, the playbook). Free Nano Banana images for backgrounds, character sheets, CGs and covers: `flow_agent_images {scenes, out}` for a set, `flow_generate` for single shots; `flow_download` for 2K/4K. Then comfy-mcp `remove_background` for sprites. Video, video edits and Flow voices spend credits: ask the user first and pass `max_credits`. Free voices: `flow_narrate` with engine `gemini` (Google AI Studio key: `GEMINI_API_KEY` in flow-music-mcp's `.env`) or `windows`. Local and free: `flow_assemble` (clips + music + voice-over), `flow_transcribe` and `flow_captions` (whisper.cpp installs itself on first use; `flow_speech_setup` shows it).
   - Google Flow Music (`music_*`): `music_generate {sound, lyrics | instrumental: true, title, bpm?, length?, seed?, format: "wav", out}` makes one take in about a minute (48 kHz stereo; WAV about 35 MB for 3 min). Convert to ogg if VN Studio needs it, and `vno_asset_replace` it as a `music_0n`. It **spends Flow Music credits**: ask the user before the first one. `music_status` says if the profile is signed in (`yarn login` in the repo once). Verified end to end 2026-10-22 (instrumental, MP3 and WAV); lyrics, Advanced and Model are not tried yet.
   - **Pixel art with no ComfyUI** (every VN Studio image mode otherwise starts from a ComfyUI render): set `art: {style: "pixel", provider: "hand"}` (VNO-07; on an older engine, replace every image before the pipeline reaches `generate`). Write each image as a Python script with `scripts\pxcanvas.py`: a `Canvas` with shapes, dithered gradients, polygons, hand-written rows and outlines; `Studio().image(...)` / `.sprite(...)` paint it into Pixel Studio as `draw_grid` tiles and export through Pixel Studio, under a lock so several agents can draw at once. Grid 240x135 exported 8x (1920x1080). Sprites: 120 rows (960 px), transparent, bottom-aligned, faces in the top 70 rows (the text box covers the rest). Cover: also 240x135, it becomes the main menu. Example production with a style brief, reference scripts and parallel agents: `runs/the-soother-that-fell-into-dragon-land/art/` (`STYLE.md`). Agents check their work by reading the exported PNG, not `render_preview` (Pixel Studio has one current document for all clients).
   - Music by hand in Chiptune Studio (`new_song`, `write_melody` per channel with `wrap`, `write_drums`, `analyze_song`, `render_audio {loops: 2}`), then `vno_asset_replace` for each `music_0n` and `vno_set_music` for the chapter plan. Keep the `.ctune` projects next to the run.
6. `vno_build {slug}` then `vno_lint {slug}`. The build lists any placeholder assets left. Optional: `vno_android_preflight`, `vno_android_build`.
7. Play. Give the user the PowerShell form, because their terminal is PowerShell: `& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\<slug>\game"`. PowerShell does not expand `%USERPROFILE%`, and with a wrong path Ren'Py quits without a word. In cmd the form is `...\renpy.exe "%USERPROFILE%\VisualNovels\projects\<slug>\game"`. A window titled with the book title means it started. Only the user can say it plays well; ask them, and write the answer in the run log.

## 4. Finish

- Update `runs/<slug>.md`: what was made, where the files are, what was checked, what is left.
- Any tool limit you hit that a code change would fix: add it to that tool's own `ROADMAP.md` (in its repo, listed in the hub's `ROADMAP.md`), with the symptom. If the fix needs two or more tools, add it to the hub's `ROADMAP.md` as a new `HUB-NN` task instead.

## Things that go wrong

- MCP connection refused: the service is down. `hub.ps1 start <id>`, then `hub.ps1 logs <id>` if it does not come up.
- `unknown tool "vno_create_project"` (or another story tool): the running VN Studio is older than VNO-04. `hub.ps1 build vn-studio`, `hub.ps1 stop vn-studio`, `hub.ps1 start vn-studio`, then reconnect it.
- `hub.ps1 call` gives up after 15 s: call `vno_build`, `vno_lint` and other long tools with `wait: false`, then poll `vno_wait {slug, timeoutSeconds: 10}`.
- "engine.lock": another engine (the desktop app or an earlier headless start) already uses that data folder. Use the running one; its MCP is the same port.
- Scriptorium or Book Translator jobs fail with model errors: no model answered. Start LM Studio (`hub.ps1 start lmstudio`) or Strata (`hub.ps1 start strata`), then `scriptorium.check_servers`.
- ComfyUI out of memory: `vno_comfy_free` (or comfy-mcp `free_memory`), and do not run Strata at the same time as image generation.
- Pixel Studio and Chiptune Studio keep one shared document/song for every client: call them one at a time, never in parallel.
