# HUB-42 The pending extra ideas of REQ-0030: live steps and checks

Date: 2026-11-22. Plan: `.claude/tickets/HUB-42-pending-ideas-and-proxy-monitor/plan.md` ("Live data steps" L1-L5, "Live checks" K1-K4). The user approved "All if them, if there is nothing else to fix"; the plan's questions were answered yes (L1 equal to the seed, L5, K3 through the proxy, the Pixel reorder waits for K4, the hub worker restarts the proxy). Worker session. No model was called. Nothing committed; no repo code or seed changed.

**Rebuilds and K1-K4 postponed on the user's word, 2026-11-22** ("Ok build open idea first": the open ideas get built first, so one rebuild and one round of checks covers everything). Only L1-L5 ran. No `yarn build`, no `hub.ps1 build`, no service stopped, started or restarted.

Repo heads (master) used as seeds: scriptorium 980e415, visual-novels-orchestrator fe42e25, edu-game-studio 7d93579, pixel-art-generator 9429022 (PAR-23 merged; L4's seed line read with `git show master:seed/config/providers.md`). Every seed working tree was clean on master.

## Preflight

`hub.ps1 status`: up vn-studio (node 25848), vibetts, comfyui (17472), strata 8080 (Qwen3.8-Flash-Next, pid 37680), acp-proxy (electron 26412). Down: scriptorium, edu-studio, pixel-studio (7457), cartoon-studio, chiptune-studio and the rest. No process had `Scriptorium` or `PixelStudio` in its command line. No `.bak-HUB-42` existed before.

`%APPDATA%\api-acp-proxy\settings.json` SHA-256 (hashed only, not read or changed): `1130D96801D1F646694975F790F7A2BB45606EE78C64652759726868A8BBA592` at the start and at the end (equal).

## L1-L5: live prose

Script `.claude/temp/hub42-live/edit.cjs` (reads and writes bytes as UTF-8, keeps BOM, line ending and the front matter byte for byte; one-line steps refuse unless exactly one line equals the plan's old text; whole-prose steps refuse unless the live prose lines missing from the seed are exactly the plan's lines and those lines carry the plan's old wording; refuses to overwrite an existing backup). Dry run of all five first, then the real run; the reports are in `.claude/temp/hub42-live/L1.json` ... `L5.json`. Each backup is `<file>.bak-HUB-42` (copied with COPYFILE_EXCL before the write; older `.bak-HUB-*` untouched).

| step | file (line ending) | change | `git diff --no-index -U0 <file>.bak-HUB-42 <file>` | checks |
|---|---|---|---|---|
| L1 | `C:\Users\Infplane\Scriptorium\config\roles.md` (CRLF, no BOM) | prose after the second `---` replaced by the seed's: live 79 (aliases `paid`, `strata`, `lmstudio`), 81-85 (starting choices, including the 2026-11-13 archivist Hydrogen trial line, kept in the backup), 88 (reviewer jobs, "applies from the next job") | `@@ -79 +79 @@`, `@@ -81,5 +81,5 @@`, `@@ -88 +88 @@` only | front-matter sha256 047996689d58061e before and after; prose (CR stripped) equals the seed; 88 CR / 88 LF before and after; 3456 -> 4215 bytes |
| L2 | `C:\Users\Infplane\Scriptorium\config\providers.md` (CRLF) | line 270 "... keep only the nomic embedding model loaded in LM Studio while it runs." -> seed 262 "... no ComfyUI while it runs. The proxy's small nomic embedding server (port 8083) runs beside it." | `@@ -270 +270 @@` only | front-matter sha256 b0d12bacbabcaea0 before and after; 292 CR kept; 16893 -> 16927 bytes |
| L3 VN | `C:\Users\Infplane\VisualNovels\config\providers.md` (CRLF) | line 247, same old line -> VN seed 245 "... no ComfyUI while it runs. Only one local model is on the GPU at a time (gufo, strata and llama through the proxy included)." | `@@ -247 +247 @@` only | front matter 9df9cc936fcd6328 same; 268 CR kept; 17269 -> 17332 bytes. VN Studio running (allowed: prose only, read on start) |
| L3 Edu | `C:\Users\Infplane\EduGames\config\providers.md` (LF) | line 300, same old line -> Edu seed 296 "... no ComfyUI while it runs." | `@@ -300 +300 @@` only | front matter 1b8013404b853712 same; no CR; 23985 -> 23950 bytes. Edu down |
| L4 | `C:\Users\Infplane\PixelStudio\config\providers.md` (CRLF) | line 307 "Tool calling works best ... In LM Studio load the model with a context of at least 32768: ... about 8000 tokens ..." -> PAR-23's seed line 296 ("... at least 65536 (Strata has 131072): ... about 34,000 tokens ... (34,292 measured ..., creative-hub HUB-41)") | `@@ -307 +307 @@` only | front matter e9e33ae226390eb6 same; 307 CR kept; new line equals the master seed line (grep count 1); 12763 -> 12849 bytes. Pixel down (7457), not started |
| L5 | `C:\Users\Infplane\Scriptorium\config\settings.md` (LF) | prose after the second `---` replaced by the seed's: the extra blank line after the H1 dropped, the `## Byline` section added, live 31 (`fallbacks`: "API, API, LM Studio, API", `strata`, `lmstudio`), 33 (kinds `strata`, `lmstudio-2`), 35 ("the three below"), 36 (`fallback_shared`, Strata's `-low`), 42 (example row `lmstudio/gemma-4-e4b-...`), 48 (`last_resort_model`, "a Strata that is not running") | `@@ -19 +18,0 @@` (blank line), `@@ -28,0 +28,4 @@` (Byline), `@@ -31 +34 @@`, `@@ -33 +36 @@`, `@@ -35,2 +38,2 @@`, `@@ -42 +45 @@`, `@@ -48 +51 @@` | front-matter sha256 ff3b9537b2ecdd01 before and after; prose equals the seed; 56 -> 59 LF, no CR; 4616 -> 5159 bytes |

Every live old text matched the plan one to one; nothing skipped. Scriptorium stayed down throughout (it reads these files on its next start).

## Builds, restarts, K1-K4

Not run: postponed on the user's word (see the top). No lock observation (the `hub.ps1 stop vn-studio` with `Clear-StaleLock` did not happen).

Run later, together with HUB-43's (2026-11-22, 19:41-20:15): the rebuilds, restarts and K1-K4 results are in `runs/hub-43-open-ideas.md`.

## End state

Running as before: vn-studio (25848, old build), vibetts, comfyui (17472), strata 8080 (37680, loaded by the proxy), acp-proxy (26412, old `dist/`). Down as before: scriptorium, edu-studio, pixel-studio, cartoon-studio. No queue paused. Proxy settings SHA-256 unchanged.

## UNTESTED

- L1, L2, L5 in Scriptorium (not started); L3 in VN (read on its next start) and Edu (not started); L4 in Pixel (not started).
- Everything of the build and check half: the proxy rebuild and restart, the app rebuilds, the VN restart and the first real `Clear-StaleLock`, K1-K4.
