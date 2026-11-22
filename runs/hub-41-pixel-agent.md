# HUB-41 Pixel's artist agent over MCP: live steps and checks

Date: 2026-11-22, 15:30-15:53 +01:00. Plan: `.claude/tickets/HUB-41-pixel-agent-and-small-ideas/plan.md` (L1-L3, K1, K2). The user approved "Yes, run all" (three live prose edits with backups, the Pixel Studio and VN Studio rebuild with a VN restart, K1 headless with the stop tool, K2 in a throwaway project deleted at the end; local models only). Worker session. Only local models through the proxy were called (Strata, Inkling). No paid or cloud model, no Flow, no ElevenLabs, no Gemini. Nothing committed; no repo code or seed changed.

Repo heads (master): pixel-art-generator 2e0d3fc (PAR-21 and PAR-22 merged), visual-novels-orchestrator 0f360c3 (VNO-70 merged), edu-game-studio be16f1b, scriptorium b6071c9.

## Preflight (`hub.ps1 status`, 15:30)

Up: vn-studio (node 2248), vibetts, comfyui (17472), strata 8080 (Qwen3.8-Flash-Next), acp-proxy (26412). Down: scriptorium, edu-studio, pixel-studio, cartoon-studio and the rest. No process had `Scriptorium`, `PixelStudio` or `EduGames` in its command line.

Locks found:
- `C:\Users\Infplane\PixelStudio\engine.lock`: present, stale (pid 29116, headless, started 2026-11-04; pid not running). The plan asks for "does not exist"; Pixel was not running, so L1 went ahead. Not deleted.
- `C:\Users\Infplane\Scriptorium\index\engine.lock`: pid 19260 (2026-11-21), not running (known stale lock). Not deleted.
- `C:\Users\Infplane\EduGames\engine.lock`: pid 25460 (2026-11-21), not running. Not deleted.

## L1-L3: live prose

Script `.claude/temp/hub41-live/edit.cjs` (reads and writes bytes as UTF-8, keeps BOM and line ending, finds each place by its text, refuses unless exactly one line matches). Dry run first, then the real run. Backups made with `cp -p` before the edit (none existed; older `.bak-HUB-*` untouched):
- `C:\Users\Infplane\PixelStudio\config\roles.md.bak-HUB-41`
- `C:\Users\Infplane\Scriptorium\config\roles.md.bak-HUB-41`
- `C:\Users\Infplane\EduGames\config\settings.md.bak-HUB-41`

| step | file | change | `git diff --no-index -U0` | checks |
|---|---|---|---|---|
| L1 | PixelStudio `config\roles.md` (LF, no BOM) | deleted `  lmstudio: lmstudio/ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp` (line 6) | `@@ -6 +5,0 @@` only | 1252 -> 1187 bytes; `config\app.json` `selectedModel` = `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`; K1 `list_models` has no `error`. (Front matter changes by design: the deleted line is in it.) |
| L2 | Scriptorium `config\roles.md` (CRLF, no BOM, 88 CR kept) | line 86 "Embeddings: the local nomic model in LM Studio ..." -> the seed line 51 (through the ACP proxy, `acp/llama/nomic-embed-text-v1.5`, AAP-43 ...) | `@@ -86 +86 @@` only | front-matter sha256 047996689d58061e before and after; 3315 -> 3456 bytes. Scriptorium down; not started |
| L3 | EduGames `config\settings.md` (LF, no BOM) | lines 16, 18, 21 -> the seed's paragraphs | `@@ -16 +16 @@`, `@@ -18 +18 @@`, `@@ -21 +21 @@` only | front-matter sha256 850ebd1e124df0ea before and after; prose after the second `---` (CR stripped) equals the seed; 3004 -> 2961 bytes. Edu down; not started |

All three old texts matched the plan one to one (word diff: L3 16 "LM Studio" -> "ACP proxy", "`strata`" -> "`acp`"; 18 adds "`acp` the first ACP proxy row (the local model, EGS-71)" and "(the provider is off)"; 21 drops the Strata `-low` sentence and "such as that one without a Strata row", "`strata`" -> "`acp`"). Nothing skipped.

## Builds and the VN restart

`pwsh -File scripts\hub.ps1 build pixel-studio vn-studio`: exit 0 (log `.claude/temp/hub41-live/build.log`). Pixel: electron-vite main/preload/renderer built (the usual zod comment and chunk-size warnings). VN: `yarn build:engine` OK (the known `puzzle.ts` dynamic-import warning).

VN restart: `VisualNovels\jobs\queued` and `running` were empty and every project's pipeline was done, so no job was running. `hub.ps1 stop vn-studio` (pid 2248), `hub.ps1 start vn-studio` -> node 25848, 7459 answered at once.

## K1 Pixel's artist over MCP on Strata

`hub.ps1 start pixel-studio` at 15:38:28 (headless, electron 32952; it started over the stale lock and rewrote it). The `pixel-studio` MCP tools loaded with ToolSearch on the first try (no HTTP fallback needed).

- `list_models`: no `error`; `defaultModel` and `selectedModel` `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`; that model `tools: false`, `vision: false`, `local: true`; `unavailable: 11`. The `lmstudio/ista-daslab...` model is still listed as a provider row (`shown: false`), as expected: only the alias went. PASS.
- `new_document {16, 16, "hub41-artist", "pico-8"}` -> doc2.
- Run 1 `start_agent_run` (mushroom text, new chat) -> runId `47ea6e07-fa40-4c5b-a216-9266096f5ff4`, model `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, chatId ff9e62d3-1fec-4f7f-937a-cd69548e0eb6.
  - 14:38:52.853Z -> 14:40:20.392Z UTC: 87.5 s wall. `state: completed`, 4 steps (of 25), every `step` event `mode: "json"`.
  - Steps: 1 `draw_grid` 16x16 (isError false, touched x=1 y=1 w=13 h=14); 2 `render_preview` scale 16 (isError false, image); 3 `read_grid` (isError false); 4 reply "Verifying pixels via grid." and done. No tool errors.
  - `usage` per step (input/output): 34,292/273, 34,612/32, 34,738/29, 35,140/284. Total 138,782 in, 0 cached, 618 out. `costUsd` 0.
  - **First step input tokens: 34,292** (Strata's tokenizer). The render_preview step grew the input by only 126 tokens: Strata is `vision: false` here, so the preview image did not reach the model.
- `render_preview {scale: 8}` and `export_png` -> `C:\projects\Personal\creative-hub\.claude\temp\hub41\mushroom.png` (I added `scale: 16`, 256x256, for a readable record).
- My look at the picture: a recognisable mushroom. Red (#ff004d) dome cap with a few small white and peach spots and brown (#ab5236) shading pixels along its lower rim, black outline round the cap; a peach (#ffccaa) stem with light grey shading on its right side and base, black outline on its left and bottom. Flaws: it sits about 1-2 px left of centre (x 1-13 of 16), the cap is a little lopsided, the white spots are few and irregular, and the stem's right outline is grey rather than black. Good enough for "a mushroom-like drawing"; not a polished sprite.
- Steps 3-7: PASS.
- Stop tool: run 2 `start_agent_run {"text": "Draw a small green tree on this canvas."}` -> runId `c7e158ff-1669-4642-adbe-f506f6a7c77e` (Strata), started 14:40:35.996Z; about 20 s later (proxy showed Strata active 1) `stop_agent_run` -> `stopped: true`, `state: aborted`, `stoppedBy: "mcp"`, no `timedOut`, 1 step, usage 0/0, cost 0, ended 14:41:00.705Z (24.7 s). `get_agent_run` shows the same. The run drew nothing (it was still in step 1's model call); the canvas showed only the mushroom. The proxy's Strata `active` was 0 by 15:41:06. PASS.
- `hub.ps1 stop pixel-studio` at 15:41:10: stopped (32952). `engine.lock` is left behind after the stop (pid 32952, not running): see Discoveries.
- K1 total about 3 minutes (box 40).

B (the plan's 24,000 rule): the first prompt is 34,292 tokens, above 24,000 and above Inkling's 32,768 context on its own, before any image, history or reply. B stands: Inkling cannot serve Pixel's artist in JSON-action mode. No Inkling-for-Pixel check needed.

## K2 One VN review on a picture built to be rejected

acp-proxy, comfyui and vn-studio were up. ComfyUI vram_free before: 106,009,006,080 of 107,090,132,992. Critic list in `VisualNovels\config\roles.md`: `art-critic: models: [paid, acp/llama/inkling-2-mini]`.

1. `vno_create_project` `hub41-reject-check` (en, `art.review: true`) -> assets: 1 background, 1 cover, 3 music.
2. `vno_asset_list` background: `bg_square_noon` (prompt empty, engine qwen-image-2.1).
3. `vno_asset_set` the crowd prompt (`promptByHand: true`, 1664x928).
4. `vno_asset_generate {only: [bg_square_noon]}` -> job `hub41-reject-check--vn.assets.generate--all--r1`. `vno_wait` 900 s was cut by the client's 300 s MCP idle limit (no harm; I followed with `vno_status` and `vno_wait` 240 s).
   - `hub41-reject-check--vn.assets.generate--bg_square_noon--r1`: 15:41:27-15:43:25, 118.4 s, qwen-image-2.1, v1.webp. No model call (the art-director log: 0 calls).
   - `hub41-reject-check--vn.assets.review--bg_square_noon--r1`: 15:43:25-15:51:33, model `acp/llama/inkling-2-mini`, prompt_version 4057bd7c (job file) / d04d05b3 (log header), 3 calls, 2,856 in / 2,019 out, 0 USD, 488.0 s (includes two regenerations).

| attempt | image | spend row | tokens in/out | seconds | verdict | `problems` | `revisedPrompt` | English |
|---|---|---|---|---|---|---|---|---|
| 1 | v1: 11 people in coats in a line before the fountain | 15:45:17 | 952/792 | 111.2 | rejected | "Background asset contains a crowd of people; a background should be empty and fill the whole image." | "A small cobbled village square with a stone fountain at noon, no people, anime visual novel background, fills the whole image" | yes |
| 2 | v2: empty square, fountain, hanging shop sign with lettering on the right | 15:48:50 | 944/688 | 108.7 | rejected | "A hanging shop sign with lettering/emblem appears on the right-side building; the prompt asks for no signs/stray words." | "A small cobbled village square with a stone fountain at noon, no people, anime visual novel background, fills the whole image, no text, no letters, no signs, no captions, no borders" | yes |
| 3 | v3: empty square, fountain left, a sign reading like "DWEIN" on the left building | 15:51:33 | 960/539 | 61.9 | rejected (final) | "Stray sign with letters/text on the left building (\"MOET\"-like)" | "A small cobbled village square with a stone fountain at noon, no people, no signs, anime visual novel background, fills the whole image, no text, no letters, no captions, no borders" | yes |

   Spend rows in `VisualNovels\logs\spend\2026-11.md`: art-critic-default, hub41-reject-check, acp, llama/inkling-2-mini, 0.000000 USD each. No DeepSeek row (paid skipped for vision).
   My own look: v1 clearly has a crowd (right to reject); v2 has a hanging sign with lettering at the top right of the centre (right); v3 has a lettered sign on the left building (right, though the text reads more like "DWEIN" than "MOET"). All three rejections are correct.
5. `vno_asset_list` after: `review: {status: rejected, note: "Stray sign with letters/text on the left building (\"MOET\"-like)"}`, selected v3, prompt = the critic's last revised prompt.
6. `vno_comfy_free {}` -> `{"results":[{"lane":"http://127.0.0.1:8188","ok":true}]}`. PASS (VNO-70; it failed with "Unexpected end of JSON input" before). vram_free afterwards 106,009,006,080.
7. `vno_delete_project {slug: hub41-reject-check, confirm: true}` -> deleted; `vno_list_projects` does not list it; the folder `VisualNovels\projects\hub41-reject-check` is gone. The three job files stay in `VisualNovels\jobs\done\` (the delete does not touch the job history).

K2: PASS (rejections with problems, all English, all on Inkling at 0 USD, free ok, project gone). About 10.5 minutes (box 25).

## End state (15:53)

- Proxy back on Strata: a tiny chat to `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` with `reasoning_effort: none` at 15:51:54: HTTP 200, "OK", 16/2 tokens, 62.3 s (the Inkling -> Strata switch). 8080 answers (Strata, loaded, pid 37680); 8082 down.
- `/healthz`: status ok, every provider active 0, queued 0.
- ComfyUI: memory freed (vno_comfy_free ok; vram_free 106,009,006,080).
- Running: vn-studio (25848, new build), comfyui, acp-proxy, strata, vibetts. Stopped: pixel-studio. Never started: Scriptorium, Edu Studio, Cartoon Studio. No queue was paused.

## UNTESTED

- L1 in the Pixel window (only headless ran); L2 in Scriptorium (not started; it reads roles on its next start); L3 in Edu Studio (not started).
- The Pixel window's wiring of the agent tools (a run started from MCP while the window is open, shown in its chat).
- `stop_agent_run` while a run is between steps or mid-drawing (this stop came during the first model call, so "what it drew stays as one undo step" was not exercised with real pixels).
- `continueChat: true`, and the 30-minute timeout path.
- Whether the Strata request behind a stopped run is really cancelled at the server or finishes in the background (the proxy showed active 0 within 6 s, which suggests it was cancelled).
