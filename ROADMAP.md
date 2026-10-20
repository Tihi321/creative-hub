# Roadmap

Gaps found while connecting the tools (2026-10-20). Each item belongs to one repo; fix it there. Most important first.

## All three (client provider)

- **Every task sends the prompt twice.** `get_client_task` / `vno_get_task` return `system` + `user` and also `messages` whenever there are 2 or more messages, which is every task. Send `messages` only when there is more than one user message or an assistant turn. This halves big tasks such as Scriptorium's whole-book rewrite (98k characters).

## Book Translator

- ~~**Script-aware adapter + folder input.**~~ Done on branch `BTT-08_vn-script-adapter` (2026-10-20, not merged yet): a book folder is one project (format `vn`, `src/engine/formats/vn.ts`), one segment per script line, markers/tags/frontmatter keys kept, exported as a mirrored folder; over MCP (`create_project` / `analyze_file` with the folder) and the CLI. A mock run over the soother book aligned in VN Studio with 381/381 beats, 0 missing, 0 extra. Left: a real-model run into Croatian, merging the branch, and the app's New project screen (it picks files only).
- ~~**Only the first-pass translation could be done by the MCP client.**~~ Done on branch `BTT-09_client-provider` (2026-10-20, uncommitted). Provider `client`, the same four tools, `wait_for_progress` / `get_project` show `clientTasks`, and a `translate_with_full_pipeline` prompt. The glossary, proofreader and QA can now be done by Claude too. 240 tests pass. Left: the live run (build, restart, and the session's token fix), then merge.
- **`config/providers.md` is not reloaded while the engine runs.** Adding the client provider, or changing its `context`, took effect only after a restart. Scriptorium reloads it, according to its code (`engine.ts`), but that was not checked live.
- **A client model without `context` defaults to 8,192 tokens,** which sizes the chunks small. Give the client entry `context: 200000` (done in the data folders on 2026-10-20). The seeds should carry it too, in all three repos.
- **The client provider must be added by hand to existing data folders.** Seeds are copied only when missing. The same is true in Scriptorium and VN Studio.
- **Translated bible (optional).** The bible and cover brief are copied untranslated (art reference; names must match the speaker tags). If localised character names are wanted, they would need translated speaker tags and bible names together.

## VN Studio (visual-novels-orchestrator)

- ~~**Story tools over MCP.**~~ Done on branch `VNO-04_story-tools-languages` (2026-10-20, uncommitted): `vno_create_project` makes a project from a story written as JSON; `vno_get_story`, `vno_story_edit` and 14 one-op tools edit book, characters, places, chapters (choices, endings), scenes (place/time/background) and beats (text, speaker, expression, cast). Ids are stable; assets are re-derived, locked and hand-set ones kept. `vno_edition_set` writes another language as JSON. Verified live: a German choice book made only through the tools, plus English and Arabic editions, built and passed Ren'Py lint (8.5.3).
- ~~**Languages.**~~ Done on the same branch: 37 languages (Supertonic's 31 + Book Translator's), more in `config/languages.md`; detection over all of them; any primary language is the default Ren'Py language; `config.rtl` for ar/he/fa; `vno_languages`. Left: the game menus are translated only for Croatian (others stay English unless a `ui` table is added in `config/languages.md`); the built-in DejaVuSans font has no CJK, Hangul, Devanagari or Thai glyphs (the build warns; a per-language font is needed); RTL layout is not mirrored.
- ~~**"Start again" on the end screen crashed the game.**~~ It used `Start()`, which only works from the main menu, so clicking it raised `JumpOutException` (found by the user in quarter-tone-test). Fixed on branch `VNO-06_end-screen-restart` (2026-10-20, uncommitted) with `Jump("start")` and a test. Games built earlier keep the bug until rebuilt.
- **Asset kinds.** No CGs, extra images, SFX, ambience or per-scene music; sprites only in 8 expressions. (`music.json` and `cues.json` now have tools: `vno_set_music`, `vno_set_cues`.)
- ~~**Step-only runs.**~~ `vno_plan` writes the art prompts and the music plan only; `vno_asset_set` sets an asset's prompt, negative, size, engine or seed without generating (the planners then keep it). `vno_run_pipeline from=art` still continues to build.
- **External asset import.** `vno_asset_replace` skips post-processing; add a tool that runs bg-removal/trim/scale on an outside image. No import of outside voice clips.
- ~~**Library path.**~~ `vno_set_library {path}` sets `scriptoriumData`.
- **Restart needed.** The VN Studio engine running for the hub predates VNO-04: `hub.ps1 build vn-studio` was run, but the new tools appear only after `hub.ps1 stop vn-studio` + `start vn-studio`.
- **Non-Latin titles.** Project slugs are ASCII; a title with no Latin letters gives the slug `book` unless `slug` is passed.
- **Studio tokens.** Tokens are not forwarded to Pixel Studio / Chiptune Studio.
- ~~**The MCP client cannot do the model steps.**~~ Done on branch `VNO-05_client-provider` (2026-10-20, uncommitted). Provider `client`; tools `vno_client_tasks` / `vno_get_task` / `vno_submit_task` / `vno_release_task`, with art-critic images sent as image content; `vno_wait` returns when a task waits; per-project `vno_update_settings {models}`. 556 tests pass. Left: the live run (build, restart, reconnect), then merge.
- **A parked job holds its agent.** With `max_parallel` 1, a role works one client task at a time per agent. Hire more agents of the role or raise `max_parallel` to answer several in parallel.
- **Pixel Studio draw loop with the client provider.** `pixel-studio-draw` is multi-turn and limited to `drawTimeoutS` 240, so with `client` it times out. Wanted: a client-friendly draw mode with no timeout per turn. Until then, draw sprites with the pixel-studio MCP and use `vno_asset_replace`.
- **No image path without ComfyUI.** Backgrounds, sheets, sprites (edited from the sheet) and both pixel modes (`pixelProvider: pixel-studio` converts a render, `pixel-studio-draw` copies one) all start with `ctx.comfy.generate` (`assets/generate.ts`). Found in the-soother-that-fell-into-dragon-land (user: "no need for comfy ui"). Being fixed on branch `VNO-07_hand-drawn-art`: `art.provider: hand`, images never generated, art plan skipped, sheets optional.
- **The main menu image is the cover, resized smoothly.** `renpy/images.ts:155` resizes the cover with sharp's default kernel and `fit: cover` to the game resolution: a pixel-art cover gets blurred unless it is exactly 1920x1080, and a portrait cover (the planned size is 1080x1920) is cut to a landscape strip. Use `kernel: nearest` for pixel books, and plan the cover landscape (or keep a separate menu image).
- **Pixel art is built as lossy WebP.** `renpy/images.ts` `encode()` uses `webp({quality: 88})` for every image; chroma subsampling smears pixel-art edges. The only switch is the global `imageFormat` in `config/renpy.md`. Fixed on branch `VNO-07_hand-drawn-art` (c23bfb3): lossless WebP for pixel projects.
- **The analysis can add assets after the art is done.** A `time` the script-analyst gives a scene changes its background id (`bg_<place>_<time>`), and a new expression adds a sprite; on a hand-drawn book that asset then has no file (with VNO-07 it waits instead of going to ComfyUI). The analyst should be told which times and expressions already have art.
- **Model jobs that do no model work still wait for a model slot.** Analyse with 0 items and stage with `byHand` cues are examples (`scheduler.ts:300-336`).

## Scriptorium

- **Waiting.** No `wait_for_book` tool; the story slug becomes a book slug later. (Hub workaround: `scripts\wait-book.ps1`.)
- **Absolute paths.** `get_book` paths are relative and `factory_status` does not report the data folder.
- **Parsed script.** No tool returns a chapter as parsed JSON (the shape suggested in `docs/visual-novel.md`).
- **Full book run over MCP never verified** (SCP-07).
- ~~**No way for the MCP client to do the writing.**~~ Done on branch `SCP-08_client-provider` (2026-10-20, uncommitted). A provider `client` (model `client/claude-code`) parks requests for an MCP client. Tools: `list_client_tasks` / `get_client_task` / `submit_client_task` / `release_client_task`. Per-book models: `add_story {models}`, `set_book_model`, and `role_models` in book.md. 300 tests pass. Left: the live run (it needs a restart of Scriptorium, which resumes the factory), then merge.
- ~~**Rejected books can't be rescued.**~~ `reopen_book {book, mode: rewrite|review, chapters?}` on the same branch: one more round (`extra_rounds` in book.md).
- ~~**Series.**~~ Done on branch `SCP-09_series` (2026-10-20, commit 33c224b, not merged): series files, an order gate (a later book waits for the earlier one to be published), earlier books in the prompts, MCP tools `list_series` / `get_series` / `add_series` / `update_series`, and a Series panel in the Library. Used live for book 1 of *The Hartley & Varga Mysteries* (`runs/the-clockless-god.md`): the series section showed up in the pitch, outline and chapter prompts as designed. Book 2 (the gate, the carry-over) is not tried live yet.
- **`add_story {models}` does not reach `start_book`.** The editor-in-chief's start job runs before `book.md` exists, so it used the global role list (a free OpenRouter model), not `client/claude-code` (found live, the-clockless-god). Apply the idea's `role_models` to `start_book` too.
- **Check notes reach the writer as a summary only.** A continuity check with verdict `revise` puts only its first paragraph into the rewrite task ("Fix the phone/photographs problem"), not the numbered problems that the review file holds (found live, the-clockless-god ch11). Pass the whole check text, or its numbered list.
- **Odd word target in check rewrites.** A rewrite of a 3,100-word chapter asked for "about 4091 words" (ch11, the-clockless-god). The number does not match the chapter or the format (1,500-3,000).
- **Clearing a book model on a published book is refused.** `set_book_model {model: null}` refuses published books, so `role_models` keeps the client model after the run (found live, the-local-patch). Removing an entry should be allowed at any stage.
- **No second life for a published book.** `reopen_book` takes only rejected books. A published book that should get one more round, for example on chapters the last round did not touch, has no tool.
- **A pin is not exclusive.** `assign_agent` makes an agent prefer its book, but other agents of the role still take the book's jobs after about 20 s. Use `set_book_model` to keep a book on one model.

## Pixel Studio (pixel-art-generator)

- `import_image` caps at 512x512 and reads no WebP; `new_document` replaces the current document; no tool to switch the current document; one shared session for all clients.
- No expression-set tool, no text/9-slice/UI-element support (textbox, buttons).
- **Drawing a full background is slow by hand.** `draw_grid` is capped at 64x64, there is no polygon, gradient/dither or bitmap-text tool, and line + `flood_fill` leaks or leaves gaps. Workaround in the hub: `scripts/pxcanvas.py` composes the picture in code and sends it as `draw_grid` tiles. Wanted: `draw_polygon`, `draw_gradient {stops, dither}`, a bulk `draw_image`/`set_layer_pixels` that takes a whole layer, and a tiny pixel font.
- **`render_preview` and every drawing tool act on the one current document**, shared by all clients: two agents drawing at once overwrite each other (the hub script takes a file lock). Tools should take a `document` id the way `export_png` does.

## Chiptune Studio (midi-generator)

- `compose_track` has no motif/leitmotif input, no variation mode, no intro. (Hand-writing a track with `write_melody` + `wrap` per channel works well: four 16-bar NES tracks in the soother run.)
- No SFX, stingers or ambience. Headless port only by `--port` (no env var).

## comfy-mcp (ComfyUI MCP server)

- **Subgraph workflows.** Most of ComfyUI's saved template workflows (Qwen-Image 2.1, Z-Image, Krea 2, BiRefNet, MiniMax, YuE2) put their nodes in a subgraph; `run_workflow` refuses them with a hint to use Export (API). Expanding subgraphs in the UI-to-API converter would make every saved workflow runnable.
- **More speech engines.** Only `chatterbox-multilingual` has a mapping (no Croatian). F5, IndexTTS-2 (Croatian-capable), Qwen3-TTS and the rest of the TTS Audio Suite need an API export plus a `.map.yaml` in `comfy-mcp/workflows`.
- **Qwen-Image 2.1 Turbo edit.** Not an engine: its template uses ManualSigmas + SamplerCustomAdvanced instead of KSampler, so it needs its own graph.
- **Jobs live in memory.** A restart forgets job ids (written files stay).

## Hub

- `hub.ps1 start <id> -Window` added (2026-10-20, commit 4c474a4, SCP-09): Electron apps start with their window and keep the MCP server on (`--mcp`). Run live for Scriptorium: the window opened and MCP answered (37 tools), but the `start` command itself never returned or printed anything. A guess, not verified: the windowed child keeps the caller's console handles.
- `hub.ps1 call` has a 15 s HTTP timeout and JSON depth 10: long tools (`vno_build`, `vno_lint`, `vno_plan` with wait) time out unless called with `wait: false` + `vno_wait`.
- Auto-start: VN Studio could start the studios itself (VNO-02 `next-steps.md` §2.1); until then `hub.ps1 start`.
- Not yet verified end to end: a full idea → published book → VN build → played game.
