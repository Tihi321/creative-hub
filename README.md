# Creative hub

The starting point for making books, translations, art, music, voices and visual novels with the local tools on this PC. Each tool is its own repo and app with its own MCP server. This folder holds the map, the MCP config, the start/stop script, and the workflow skill that chains them.

Give Claude an idea or theme in a session opened here and say what you want (for example "make a choice visual novel about a lighthouse keeper's daughter, pixel art, chiptune music"). The `make-visual-novel` skill (`.claude/skills/make-visual-novel/SKILL.md`) runs the chain.

```
idea / theme
   │
   ▼
Scriptorium ──► book folder (script + bible + outline) ──► Book Translator (EPUB, 32 languages)
   │                                                        │ (VN edition: en/hr, see ROADMAP)
   ▼                                                        ▼
VN Studio: analyse ► art ► music ► generate ► voice ► stage ► build ► lint ──► Ren'Py game (PC, Android)
               │         │            │           │
               │         │            │           └── VibeTTS (Kokoro / Supertonic)
               │         │            └── ComfyUI (Qwen-Image, BiRefNet, ACE-Step) / Pixel Studio
               │         │                (standalone CGs, edits, cutouts, music, speech: comfy-mcp)
               │         └── Chiptune Studio or ComfyUI music
               └── LLMs: LM Studio, Strata, paid APIs (per repo config/roles.md), or Claude Code itself (`client` provider, see the skill)
```

## The tools

| Id | What | Repo | Port / MCP | Data folder | Run headless |
|---|---|---|---|---|---|
| `scriptorium` | Writes books (incl. visual-novel scripts) with ~16 agent roles | `C:\projects\Personal\scriptorium` | 7341 `/mcp` | `~\Scriptorium` | `electron . --headless` (or `yarn headless`, no covers) |
| `book-translator` | Translates EPUB/DOCX/MD/TXT/PDF | `C:\projects\Personal\book-translator` | 47811 `/mcp`, Bearer token | `~\BookTranslator` | `node out/engine/index.js headless` |
| `vn-studio` | Book → Ren'Py visual novel; drives the tools below | `C:\projects\Personal\visual-novels-orchestrator` | 7459 `/mcp` | `~\VisualNovels` | `node out/engine/index.js --mcp-only` |
| `pixel-studio` | Pixel-art editor: import/convert, palettes, draw, export | `C:\projects\Personal\pixel-art-generator` | 7457 `/mcp` | `~\PixelStudio` | `electron . --mcp-only` |
| `chiptune-studio` | Chiptune/MIDI composer: compose, render ogg/wav/mp3, MIDI | `C:\projects\Personal\midi-generator` | 7458 `/mcp` | `~\ChiptuneStudio` | `electron . --mcp-only` |
| `vibetts` | Text to speech (Kokoro English, Supertonic 31 languages) | `C:\projects\Personal\vibe-tts-flow` | 7723 `/mcp` | `D:\Programs\VibeTTS` (installed app, autostarts) | tray app; or `python -m vibetts --mcp-only` |
| `comfyui` | Image, music and TTS models (plain HTTP API; `comfy-mcp` and VN Studio drive it) | Comfy Desktop | 8188 HTTP | `%LOCALAPPDATA%\Comfy-Desktop\ComfyUI-Installs\Infplane\ComfyUI` | its venv `python -s ComfyUI\main.py --port 8188 ...` (see `services.json`; the Desktop launcher needs a click) |
| `comfy-mcp` | MCP for ComfyUI: images (Z-Image, Qwen-Image 2.1, Krea 2), Qwen edits, BiRefNet cutouts, music (ACE-Step, YuE2, MiniMax), speech (Chatterbox), saved workflows | `C:\projects\Personal\comfy-mcp` | 7460 `/mcp` | `.\output\comfy` (default; every tool takes an absolute `out`) | `node out/index.js --out <dir>` |
| `lmstudio` | Local LLMs + `nomic-embed-text-v1.5` (Scriptorium RAG) | LM Studio | 1234 `/v1` | `~\.lmstudio` | `lms server start` |
| `strata` | Qwen3.8-Flash-Next server, first model choice of Scriptorium and Book Translator | `D:\Strata` | 8080 `/v1` | `D:\Strata-data` | `D:\Strata\run-iq3_s.bat` |

All Electron/Node repos use Node 24 through `fnm` and yarn 4. MCP servers listen on 127.0.0.1 only. Each data folder can be used by one engine at a time (`engine.lock`): if the desktop app is open, its MCP server is the one on that port, and a headless start of the same tool fails.

Docs inside the repos: Scriptorium `docs/mcp.md` and `docs/visual-novel.md` (the script format VN Studio reads); VN Studio `docs/mcp-guide.md`; Pixel Studio and Chiptune Studio `docs/llm-guide.md`; Book Translator, VibeTTS and comfy-mcp `README.md`.

## Running it

```powershell
pwsh -File scripts\hub.ps1                     # status of everything
pwsh -File scripts\hub.ps1 setup               # once: Book Translator MCP token (user env var)
pwsh -File scripts\hub.ps1 setup -EnableVibeTts  # once: turn on the VibeTTS MCP server (restarts the tray app)
pwsh -File scripts\hub.ps1 start               # default set: vn-studio, pixel-studio, chiptune-studio, book-translator, vibetts, comfyui, comfy-mcp, lmstudio
pwsh -File scripts\hub.ps1 start scriptorium -Force   # resumes the book factory: it writes every open idea
pwsh -File scripts\hub.ps1 stop                # stops the engines the hub started (not your apps)
pwsh -File scripts\hub.ps1 build vn-studio     # rebuild a repo after pulling or editing it
pwsh -File scripts\hub.ps1 logs vn-studio
pwsh -File scripts\hub.ps1 check               # real MCP handshake + tool count per server
pwsh -File scripts\hub.ps1 call vn-studio vno_status '{"slug":"my-book"}'   # call any tool without a Claude MCP link
pwsh -File scripts\wait-book.ps1 -Story <story-slug>   # wait for a Scriptorium book to be published
```

Scriptorium, VN Studio and Book Translator can hand their model work to the Claude session instead of a model: the `client` provider, with the tools `get_client_task` / `submit_client_task` (`vno_get_task` / `vno_submit_task` in VN Studio). How to use it is in the skill, under "Doing the model work yourself".

`.mcp.json` registers all seven MCP servers for Claude sessions opened in this folder. A server that is down when the session starts stays disconnected until you reconnect it with `/mcp` or restart the session.

## Folder

- `services.json`: the registry `hub.ps1` reads (ports, start commands, warnings).
- `.mcp.json`: MCP servers for Claude.
- `.claude/skills/make-visual-novel/`: the end-to-end workflow.
- `scripts/`: `hub.ps1`, `wait-book.ps1`.
- `runs/<slug>.md`: one log per production (ids, decisions, what was checked). `runs/<slug>/` holds books written by hand and translated editions.
- `ROADMAP.md`: what is missing in each tool, found while connecting them.
- `logs/`: output of engines started by `hub.ps1` (not tracked).
- `output/comfy/`: default output folder of `comfy-mcp` (not tracked).

## Adding a tool

1. Give it an MCP server (Streamable HTTP on 127.0.0.1, like the others) and a headless start.
2. Add it to `services.json`, `.mcp.json` and the table above.
3. Add the step to the skill, and note its limits in `ROADMAP.md`.
