# Creative hub

The starting point for making books, translations, art, music, voices and visual novels with the local tools on this PC. Each tool is its own repo and app with its own MCP server. This folder holds the map, the MCP config, the start/stop script, and the workflow skill that chains them.

Give Claude an idea or theme in a session opened here and say what you want (for example "make a choice visual novel about a lighthouse keeper's daughter, pixel art, chiptune music"). The `make-visual-novel` skill (`.claude/skills/make-visual-novel/SKILL.md`) runs the chain.

```
idea / theme
   │
   ▼
Scriptorium ──► book folder (script + bible + outline + vn/pack.json + vn/text/en.json)
   │                                                        │
   │  └─► screenplay (short film, cartoon; get_screenplay) ──► make-video skill ──► Flow (images, video, voices) ──► assembled video
   │                                                        ├─► Book Translator: reader EPUB (32 languages)
   │                                                        └─► Book Translator: VN pack text catalog ──► edition ──► VN Studio
   ▼                                                        ▼
VN Studio: analyse ► art ► music ► generate ► voice ► stage ► build ► lint ──► HTML5 visual novel (PC; hr/en UI, any edition text)
               │         │            │           │
               │         │            │           └── VibeTTS (Kokoro / Supertonic)
               │         │            └── ComfyUI (Qwen-Image, BiRefNet, ACE-Step) / Pixel Studio
               │         │                (standalone CGs, edits, cutouts, music, speech: comfy-mcp)
               │         └── Chiptune Studio or ComfyUI music (Chiptune Studio also makes SFX and ambience)
               │     art, voices and music can also come from Google Flow (flow-music-mcp)
               │     a story can stop for a logic puzzle (puzzle beats, code-made and proved)
               └── LLMs: LM Studio, Strata, paid APIs (per repo config/roles.md), or Claude Code itself (`client` provider, see the skill)
```

The VN pack (HUB-16) is the translation seam: `vn/pack.json` is the fixed template (IDs, looks, scene and cue descriptions, puzzle logic), `vn/text/<lang>.json` is the only translatable text. Book Translator translates that catalog only; VN Studio imports the pack by ID and reuses every image, music and SFX from the original. Menus, Skip, settings and the language switcher are VN Studio's own `ui-strings.ts` (English source, Croatian table), never part of the book.

## The tools

| Id | What | Repo | Port / MCP | Data folder | Run headless |
|---|---|---|---|---|---|
| `scriptorium` | Writes books, series and newspaper articles (incl. visual-novel scripts with CG/INSERT/SFX/AMBIENCE lines and aliases, book-to-VN adaptations, screenplays via `get_screenplay`) with ~17 agent roles, a humanizer pass on every chapter, and the language-independent VN pack (`vn/pack.json` + text catalog) | `C:\projects\Personal\scriptorium` | 7341 `/mcp` | `~\Scriptorium` | `electron . --headless` (or `yarn headless`, no covers) |
| `book-translator` | Translates EPUB/DOCX/MD/TXT/PDF and the VN pack text catalog (template stays byte-identical; editions are keyed by ID) | `C:\projects\Personal\book-translator` | 47811 `/mcp`, Bearer token | `~\BookTranslator` | `node out/engine/index.js headless` |
| `vn-studio` | Book folder or VN pack → HTML5 visual novel; imports by ID, editions reuse every image/music/SFX, Croatian/English UI with a live language switch; drives the tools below, can use Flow as art/voice/music provider, builds puzzle beats | `C:\projects\Personal\visual-novels-orchestrator` | 7459 `/mcp` | `~\VisualNovels` | `node out/engine/index.js --mcp-only` |
| `pixel-studio` | Pixel-art editor: import/convert, palettes, draw, export | `C:\projects\Personal\pixel-art-generator` | 7457 `/mcp` | `~\PixelStudio` | `electron . --mcp-only` |
| `chiptune-studio` | Chiptune/MIDI composer: compose, render ogg/wav/mp3, MIDI | `C:\projects\Personal\midi-generator` | 7458 `/mcp` | `~\ChiptuneStudio` | `electron . --mcp-only` |
| `vibetts` | Text to speech (Kokoro English, Supertonic 31 languages) | `C:\projects\Personal\vibe-tts-flow` | 7723 `/mcp` | `D:\Programs\VibeTTS` (installed app, autostarts) | tray app; or `python -m vibetts --mcp-only` |
| `comfyui` | Image, music and TTS models (plain HTTP API; `comfy-mcp` and VN Studio drive it) | Comfy Desktop | 8188 HTTP | `%LOCALAPPDATA%\Comfy-Desktop\ComfyUI-Installs\Infplane\ComfyUI` | its venv `python -s ComfyUI\main.py --port 8188 ...` (see `services.json`; the Desktop launcher needs a click) |
| `comfy-mcp` | MCP for ComfyUI: images (Z-Image, Qwen-Image 2.1, Krea 2), Qwen edits, BiRefNet cutouts, music (ACE-Step, YuE2, MiniMax), speech (Chatterbox), saved workflows | `C:\projects\Personal\comfy-mcp` | 7460 `/mcp` | `.\output\comfy` (default; every tool takes an absolute `out`) | `node out/index.js --out <dir>` |
| `lmstudio` | Local LLMs + `nomic-embed-text-v1.5` (Scriptorium RAG) | LM Studio | 1234 `/v1` | `~\.lmstudio` | `lms server start` |
| `strata` | Qwen3.8-Flash-Next server, first model choice of Scriptorium and Book Translator | `D:\Strata` | 8080 `/v1` | `D:\Strata-data` | `D:\Strata\run-iq3_s.bat` |
| `acp-proxy` | OpenAI-compatible API over the Codex, Antigravity and Claude agents (subscription logins); an `openai-compat` provider for Scriptorium and Book Translator | `C:\projects\Personal\api-acp-proxy` | 7461 `/v1` | `%APPDATA%\api-acp-proxy` | `node dist/index.js` with `PROXY_PORT=7461`, `PROXY_IGNORE_SAMPLING=1` |
| `flow-music-mcp` | Google Flow and Flow Music in its own Chrome: images, video, characters, voices, songs (MP3/WAV/M4A), plus local narration, assembly and captions | `C:\projects\Personal\flow-music-mcp` | 7462 `/mcp` (Chrome CDP 9334) | `~\.flow-music-mcp` | `node dist/index.js`; sign in once with `yarn login` |

All Electron/Node repos use Node 24 through `fnm` and yarn 4. MCP servers listen on 127.0.0.1 only. Each data folder can be used by one engine at a time (`engine.lock`): if the desktop app is open, its MCP server is the one on that port, and a headless start of the same tool fails.

Docs inside the repos: Scriptorium `docs/mcp.md` and `docs/visual-novel.md` (the script format and "The VN pack (v2)"); Scriptorium `docs/screenplay.md` (the screenplay format); VN Studio `docs/mcp-guide.md` (incl. "Puzzles") and `docs/protocol.md` (the VN data contract and editions); Pixel Studio and Chiptune Studio `docs/llm-guide.md`; Book Translator, VibeTTS and comfy-mcp `README.md`. The cross-repo pack contract is `.claude/tickets/HUB-16-vn-pack/contract.md`.

## Running it

```powershell
pwsh -File scripts\hub.ps1                     # status of everything
pwsh -File scripts\hub.ps1 setup               # once: Book Translator MCP token (user env var)
pwsh -File scripts\hub.ps1 setup -EnableVibeTts  # once: turn on the VibeTTS MCP server (restarts the tray app)
pwsh -File scripts\hub.ps1 start               # default set: vn-studio, pixel-studio, chiptune-studio, book-translator, vibetts, comfyui, comfy-mcp, lmstudio
pwsh -File scripts\hub.ps1 start scriptorium -Force   # resumes the book factory: it writes every open idea
pwsh -File scripts\hub.ps1 start scriptorium -Force -Window   # with its window (Electron apps), MCP still on
pwsh -File scripts\hub.ps1 stop                # stops the engines the hub started (not your apps)
pwsh -File scripts\hub.ps1 build vn-studio     # rebuild a repo after pulling or editing it
pwsh -File scripts\hub.ps1 logs vn-studio
pwsh -File scripts\hub.ps1 check               # real MCP handshake + tool count per server
pwsh -File scripts\hub.ps1 call vn-studio vno_status '{"slug":"my-book"}'   # call any tool without a Claude MCP link
pwsh -File scripts\wait-book.ps1 -Story <story-slug>   # fallback when the MCP link is down; otherwise scriptorium wait_for_book {slug}
```

Scriptorium, VN Studio and Book Translator can hand their model work to the Claude session instead of a model: the `client` provider, with the tools `get_client_task` / `submit_client_task` (`vno_get_task` / `vno_submit_task` in VN Studio). How to use it is in the skill, under "Doing the model work yourself".

VN Studio starts Pixel Studio, Chiptune Studio and ComfyUI itself when a job needs them (it reads `services.json` and waits up to `startTimeout`). It never starts Scriptorium, Strata, VibeTTS or LM Studio, and not ComfyUI while Strata answers. Off: `enabled: false` in `~\VisualNovels\config\autostart.md`, or `VNO_AUTOSTART=0`. Their output goes to `logs\<id>.out.log` / `.err.log` after a `--- started by VN Studio ... ---` line. `hub.ps1 stop` stops them; a hard kill of VN Studio leaves them running. A desktop app that holds the data folder makes the started copy exit; the job says why.

VN Studio can also use Google Flow through flow-music-mcp (`art`, `voice` and `music` provider `flow`, `vno_studios_status` shows it). Auto-start does not cover flow-music-mcp: `hub.ps1 start flow-music-mcp` first. Flow Music songs spend credits.

`.mcp.json` registers all eight MCP servers for Claude sessions opened in this folder (all over HTTP). A server that is down when the session starts stays disconnected until you reconnect it with `/mcp` or restart the session.

## Folder

- `services.json`: the registry `hub.ps1` reads (ports, start commands, warnings).
- `.mcp.json`: MCP servers for Claude.
- `.claude/skills/make-visual-novel/`: the end-to-end workflow.
- `.claude/skills/make-video/`: screenplay to assembled video through Scriptorium and Flow.
- `scripts/`: `hub.ps1`, `wait-book.ps1` (fallback for `wait_for_book` when the MCP link is down), `video-plan.mjs` (credit estimate and `max_credits` per call for a video; with `video-plan.test.mjs` and `fixtures/`; test: `fnm exec --using=24 node --test`).
- `runs/<slug>.md`: one log per production (ids, decisions, what was checked). `runs/<slug>/` holds books written by hand and translated editions.
- `ROADMAP.md`: the hub's tasks in order (live checks, productions, features across tools; each `HUB-NN` has a plan in `.claude/tickets/`), and where each tool's own `ROADMAP.md` lives.
- `logs/`: output of engines started by `hub.ps1` (not tracked).
- `output/comfy/`: default output folder of `comfy-mcp` (not tracked).

## Adding a tool

1. Give it an MCP server (Streamable HTTP on 127.0.0.1, like the others) and a headless start.
2. Add it to `services.json`, `.mcp.json` and the table above.
3. Add the step to the skill, note its limits in a `ROADMAP.md` in its repo, and add that repo to the table in the hub's `ROADMAP.md`.
