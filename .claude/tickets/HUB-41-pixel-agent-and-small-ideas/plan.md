---
status: done
request: REQ-0030
repos: [creative-hub, pixel-art-generator, edu-game-studio, visual-novels-orchestrator, midi-generator, scriptorium, api-acp-proxy]
branch: HUB-41_pixel-agent-and-small-ideas
updated: 2026-11-22
---

# HUB-41 Pixel's artist agent over MCP, Pixel's vision rows, Edu lint and the small ideas

The user said on 2026-11-22, word for word: "yes mcp tool for artist agent, yes vision rows lm studio recomendation, edu yarn fixt it, new small ideas, build them now". Context: REQ-0030 (`.claude/director/requests/REQ-0030-acp-for-all.md`, `## Extra ideas`, the eight "(new, ...)" lines), HUB-40 (`.claude/tickets/HUB-40-extra-ideas/plan.md`, N4 and discoveries), HUB-39 (contracts V1-V4), `runs/hub-39-vision-checks.md`, `runs/hub-40-extra-ideas.md`. Every item was checked against today's master of its repo (2026-11-22, read only).

Readings built: the narrow ones. A = four MCP tools on the existing agent (the stop tool added on the user's approval, 2026-11-22), no new agent features. B = the honest outcome: Inkling cannot serve Pixel's vision use, so the dead `lmstudio` alias goes and the seed says why. The small ideas = the smallest change each.

## Items

| item | what | verdict | ticket | reason (verified 2026-11-22) |
|---|---|---|---|---|
| A | Pixel MCP tools for the artist agent | BUILD | PAR-22 | `AgentRunner`/`LlmService` exist only in the window (`src/main/agentIpc.ts:40-46`); headless (`src/main/headless.ts:79`) has neither; the MCP host (`src/main/mcp.ts:274-286`) carries only drawing tools. Four tools: `start_agent_run` (a new conversation unless `continueChat`), `get_agent_run`, `stop_agent_run`, `list_models`. 10 source files (1 new), 3 test files |
| B | Pixel's vision rows `lmstudio` to Inkling | BUILD, but not as a move: the dead alias goes, no local vision model, documented | PAR-21 | no vision role exists; the alias (`seed/config/roles.md:6`) is named by no role. Inkling is `tools: false` (JSON-action mode), whose system prompt is the guide (20,041 chars) plus every tool schema (99,076 chars, measured): about 30,000-40,000 tokens against Inkling's 32768 context, before images and a reply |
| C | Edu `yarn lint` red | BUILD | EGS-74 | one error: `tests/models.test.ts 86:76 no-regex-spaces` (ran `yarn lint` on master e7854ff) |
| D1 | "keep only the nomic embedding model in LM Studio" in seeds | BUILD | VNO-70 (`:245`), EGS-74 (`:296`), PAR-21 (`:291`), MDI-20 (`:293`) | LM Studio not installed. VN and Edu use embeddings only in `engine probe` (`src/engine/cli.ts`), and no seed row is an embedding model; Pixel and Chiptune have no embeddings. The brief's line numbers 248 and 299 are 245 and 296 today |
| D2 | Scriptorium test sample port 7461 | BUILD | SCP-67 | `tests/customProviders.test.ts:64,120`: custom provider `acp-home`, a pure sample (the migration acts only on id `acp`, `src/engine/store/migrations.ts:403-422`) |
| D3 | Scriptorium docs say embeddings go through LM Studio; live `roles.md` prose | BUILD | SCP-67; hub L2 | `README.md:12`, `CLAUDE.md:15,16`, `docs/design.md:511,652` (dated decision rows left as history). Live `~\Scriptorium\config\roles.md:86` (read only today) still "the local nomic model in LM Studio" |
| D4 | Live Edu `settings.md` `-low` prose | BUILD (hub live step) | hub L3 | the live prose differs from the seed in three paragraphs (file lines 16, 18, 21); line 21 is the old `-low` text word for word |
| D5 | stale ROADMAP states | BUILD | HUB-41 H1, VNO-70, EGS-74 | hub rows 31-33 say In progress / Planned / Planned; VNO-68 and EGS-72 say "UNTESTED (hub K2/K3)" though K2, K3 passed; VNO-69 says "UNTESTED (hub N1)" though N1 passed for the grey backing. EGS-73 and CTS-56 stay (their live checks are still untested) |
| D6 | proxy `applyFix` never updates `hf.quant` | BUILD | AAP-45 | `src/renderer/llama-models.ts:72-80`; `hf.quant` feeds "Find on Hugging Face" (`llama-view.ts:398`) |
| D7 | HUB-40 plan N1 needs `force: true` | BUILD | HUB-41 H2 | `.claude/tickets/HUB-40-extra-ideas/plan.md:141`; the N1 run needed it (`runs/hub-40-extra-ideas.md:66`) |
| D8 | one VN review on an image built to be rejected | BUILD (live check) | HUB-41 K2 | N1 approved, so "write problems in English" was never exercised |
| fold-in 1 | Cartoon `autostart.ts:21` `NEVER_STARTED` comment names Strata, not Gufo | NO CHANGE | - | the comment describes the list `['scriptorium', 'strata']`, which is right: Gufo is not a `services.json` service (no `gufo` id), so it cannot be "never started"; Gufo is held back by the GPU check (`GPU_HOLDERS`), not by this list. Adding Gufo to the comment would make it wrong |
| fold-in 2 | VN `vno_comfy_free` fails on ComfyUI's empty 200 | BUILD | VNO-70 | `freeMemory` (`src/engine/comfy/client.ts:175-182`) parses the body with `fetchJson` (`:127`); callers ignore the value. Fix: check the status, do not parse (one function body) plus one test |

## Tickets (ids checked 2026-11-22 in each `ROADMAP.md`, `.claude/tickets`, `git branch -a`: none used)

| ticket | repo | branch | plan | depends on |
|---|---|---|---|---|
| PAR-21 | pixel-art-generator | `PAR-21_vision-rows` | `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-21-vision-rows\plan.md` | none |
| PAR-22 | pixel-art-generator | `PAR-22_mcp-artist-agent` | `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-22-mcp-artist-agent\plan.md` | PAR-21 (cut from the head of `PAR-21_vision-rows` if PAR-21 is not merged yet, else from master after it) |
| EGS-74 | edu-game-studio | `EGS-74_small-ideas` | `C:\projects\Personal\edu-game-studio\.claude\tickets\EGS-74-small-ideas\plan.md` | none |
| VNO-70 | visual-novels-orchestrator | `VNO-70_small-ideas` | `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-70-small-ideas\plan.md` | none |
| MDI-20 | midi-generator | `MDI-20_lm-studio-prose` | `C:\projects\Personal\midi-generator\.claude\tickets\MDI-20-lm-studio-prose\plan.md` | none |
| SCP-67 | scriptorium | `SCP-67_embeddings-docs` | `C:\projects\Personal\scriptorium\.claude\tickets\SCP-67-embeddings-docs\plan.md` | none (never start Scriptorium) |
| AAP-45 | api-acp-proxy | `AAP-45_fix-hf-quant` | `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-45-fix-hf-quant\plan.md` | none |
| HUB-41 | creative-hub | `HUB-41_pixel-agent-and-small-ideas` | this file | L and K: the repo tickets merged |

Order. Pixel: PAR-21 first, then PAR-22. Both add a `ROADMAP.md` row; PAR-21 is seed prose only, so PAR-22 starts from it (from its branch head when it is not merged yet, so the two are built back to back) with no conflict, and PAR-22's README and hub-row text can say that Pixel has no local vision model. The other five repo tickets and the hub tasks are independent and can run beside the Pixel pair.

Last ids used before this plan: HUB-40, SCP-66, VNO-69, EGS-73, CTS-56, PAR-20, MDI-19, AAP-44 (BTT-37 not needed: no Book Translator item).

## Out of scope

- A run queue, new agent behaviour (PAR-22 "Out of scope").
- Moving Pixel to any vision model; the `lmstudio` provider rows of any app; `extra_body` on Pixel's Inkling rows.
- Edu's copy of the `freeMemory` bug; Cartoon's ComfyUI client.
- The rest of the live Scriptorium `roles.md` prose (lines 79, 82-85 are also pre-HUB-38: see Extra ideas); live `providers.md` prose of VN, Edu, Pixel and Chiptune (still the old nomic sentence).
- Starting Scriptorium, any re-index, `%APPDATA%\api-acp-proxy\settings.json`, any paid or cloud model.

## Hub tasks (branch `HUB-41_pixel-agent-and-small-ideas`)

The hub has no test suite. Inputs: this plan and the files named. Find each place by its text; the line numbers are from master 2941ac4.

**H1 `ROADMAP.md` rows 31-33 and a new row 34 (only facts recorded in REQ-0030's Log and the run logs).**
- Row 31 (HUB-38), last cell `In progress` becomes: `Done 2026-11-21: all merged and pushed; live data L2-L8 and L2b applied; C1, C4 and C9, the VN, Edu, Cartoon and Book Translator app checks and the Scriptorium probe passed; the Pixel artist request UNTESTED (HUB-41 K1)`
- Row 32 (HUB-39), last cell `Planned` becomes: `Done 2026-11-22: merged and pushed; live data L0-L3 applied; K0-K5 passed (runs/hub-39-vision-checks.md); UNTESTED: whether Inkling catches real defects, the Blender frames-3d review, a fail-over from a cloud model`
- Row 33 (HUB-40), last cell `Planned` becomes: `Done 2026-11-22: merged and pushed (nine repos); L1 applied; L2 for VN, N1 (grey backing) and N3 passed (runs/hub-40-extra-ideas.md); UNTESTED: L2 for Edu and Cartoon, N1's English notes (HUB-41 K2), N2; N4 became HUB-41`
- New row after row 33:
  `| 34 | HUB-41 | Pixel Studio's artist agent over MCP (start_agent_run, get_agent_run, stop_agent_run, list_models); Pixel has no local vision model (the unused lmstudio alias removed); Edu lint; stale LM Studio embedding prose; vno_comfy_free on an empty reply; the proxy's found-file fix keeps hf.quant; ROADMAP live-check facts; live prose of Scriptorium roles and Edu settings (.claude/tickets/HUB-41-pixel-agent-and-small-ideas/plan.md, REQ-0030) | pixel-art-generator (PAR-21, PAR-22), edu-game-studio (EGS-74), visual-novels-orchestrator (VNO-70), midi-generator (MDI-20), scriptorium (SCP-67), api-acp-proxy (AAP-45), hub | GPU checks with the user's go-ahead | Planned |`

**H2 `.claude/tickets/HUB-40-extra-ideas/plan.md:141` (N1), documentation only.** Old: `` (`vno_asset_generate {slug: "hub39-critic-check", only: ["sprite_mara_neutral"]}`, `vno_wait`) `` New: `` (`vno_asset_generate {slug: "hub39-critic-check", only: ["sprite_mara_neutral"], force: true}`, `vno_wait`; `force` because the asset already has files, without it nothing is generated) ``. Nothing else in that file.

**H3 Hub docs after PAR-21 and PAR-22 (merge this branch only after both).**
- `CLAUDE.md:11` (the user's instruction file; this plan's approval covers only this edit). Old: "; Pixel's vision rows still name `lmstudio` and have no local model." New: "; Pixel Studio has no local vision model (Inkling's 32768 context is smaller than its artist's JSON-action prompt, HUB-41)."
- `services.json:156`, the `lmstudio` `note`. Old: "only Pixel's vision rows still name `lmstudio` and have no local model." New: "Pixel Studio has no local vision model (HUB-41: Inkling's context is too small for its artist prompt)." Check: `node -e "JSON.parse(require('fs').readFileSync('services.json','utf8'))"` (Bash: `export PATH="/c/Users/Infplane/AppData/Roaming/fnm/aliases/default:$PATH"` first).
- `README.md:39`, the `pixel-studio` row, second cell. Old: "Pixel-art editor: import/convert, palettes, draw, export" New: "Pixel-art editor: import/convert, palettes, draw, export; its artist agent over MCP (`start_agent_run`, `get_agent_run`, `stop_agent_run`, `list_models`, PAR-22)".

Check for H1-H3: `git diff` shows only these lines; `services.json` parses.

## Live data steps (after the repo tickets merge; each needs the user's go-ahead at run time; the hub does them)

Rules for all three: copy the file to `<file>.bak-HUB-41` first (older `.bak-HUB-*` files stay); change only what is listed; find each place by its text, not the line number; verify with `git diff --no-index <file>.bak-HUB-41 <file>`; keep the file's line endings and encoding (read and write bytes as UTF-8, as `runs/hub-40-extra-ideas.md:17` did). Record each step in `runs/hub-41-pixel-agent.md`.

**L1 Pixel Studio's roles (after PAR-21).** Pixel Studio closed: `pwsh -File scripts\hub.ps1 status` shows `pixel-studio` down and `C:\Users\Infplane\PixelStudio\engine.lock` does not exist (if it runs, stopping it is a service stop: go-ahead). In `C:\Users\Infplane\PixelStudio\config\roles.md` delete the one front-matter line `  lmstudio: lmstudio/ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp` (line 6 today; the live file has no comment on it). Nothing else. Verify: the diff shows one deleted line; `config\app.json` `selectedModel` is `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` (not the alias); K1's `list_models` shows no `error`.

**L2 Scriptorium's live `roles.md` embeddings line (D3).** Only when Scriptorium is not running (`hub.ps1 status` shows `scriptorium` down; never start it) and no re-index or other worker is using `C:\Users\Infplane\Scriptorium` (ask the director). In `C:\Users\Infplane\Scriptorium\config\roles.md`, prose line 86 today. Old: "- Embeddings: the local nomic model in LM Studio. Strata has no embeddings, so LM Studio keeps nomic loaded while Strata runs." New (the seed's line, `C:\projects\Personal\scriptorium\seed\config\roles.md:51`, copied as it is): "- Embeddings: the local nomic model through the ACP proxy (`acp/llama/nomic-embed-text-v1.5`, AAP-43), on its own small server beside the chat model. Only one local chat model is on the GPU at a time: a request for another one waits for the proxy to switch (minutes)." Front matter untouched: its SHA-256 (everything up to and including the second `---` line) is the same before and after. Verify: the diff shows `@@ -86 +86 @@` only.

**L3 Edu Studio's live `settings.md` prose (D4).** Edu Studio stopped (`hub.ps1 stop edu-studio` if it runs: go-ahead). In `C:\Users\Infplane\EduGames\config\settings.md`, three prose paragraphs, each replaced by the matching paragraph of `C:\projects\Personal\edu-game-studio\seed\config\settings.md`, copied as it is:
- line 16, starts "`fallbacks` is the list of models the pipeline falls back through": the old one says "for example API, API, LM Studio, API" and "(`strata`, `lmstudio`, `client` ...)"; the seed's says "API, API, ACP proxy, API" and "(`acp`, `lmstudio`, `client` ...)".
- line 18, starts "The role lists in `roles.md`, an agent's `model` and a course's `models` can name a kind": the seed's adds "`acp` the first ACP proxy row (the local model, EGS-71)" and "(the provider is off)".
- line 21, starts "- `fallback_shared`:": the old one has "(the checks name Strata's `-low` model, so it takes the Strata row's place)" and "such as that one without a Strata row"; the seed's has neither and says "`paid`, `acp`, `lmstudio`".
Front matter (lines 1-11) untouched (same SHA-256). Verify: the diff shows lines 16, 18, 21 only; a prose diff against the seed (everything after the second `---`, CR stripped) shows no difference. This is wider than "the `-low` prose" of the brief: the other two paragraphs are just as stale, and the clean proof is "prose equals the seed" (as HUB-40 L1).

## Live checks (each needs the user's go-ahead; local models only; no paid or cloud model, no Flow, no ElevenLabs, no Gemini)

GPU = loads a model; SVC = starts or stops a service. Record ids, times, tokens and results in `runs/hub-41-pixel-agent.md`.

**K1 Pixel's artist over MCP on Strata (A, and the number behind B). GPU, SVC.** After PAR-21 and PAR-22 are merged and L1 is done.
1. `pwsh -File scripts\hub.ps1 build pixel-studio` (yarn build of master).
2. `pwsh -File scripts\hub.ps1 status`; start what is down: `pwsh -File scripts\hub.ps1 start acp-proxy pixel-studio` (pixel-studio = headless `electron . --mcp-only`, port 7457). If the user has the Pixel window open instead, use it (same tools; the run then shows in its chat).
3. Over the `pixel-studio` MCP server: `list_models {}`. Passes when: no `error`; `defaultModel` is `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`; that model has `tools: false`.
4. `new_document {"width": 16, "height": 16, "name": "hub41-artist", "palette": "pico-8"}`.
5. `start_agent_run {"text": "Draw a small red mushroom with white spots on its cap and a pale stem, centred on this 16x16 canvas, with a dark outline. Use the document's palette."}` (a new chat is the default): answers at once with `runId` and `model` `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`.
6. `get_agent_run {"runId": "<id>"}` every 60 s until `state` is not `running` (at most 30 minutes, the run's own limit).
7. `render_preview {"scale": 8}` and look at it; `export_png {"path": "C:\\projects\\Personal\\creative-hub\\.claude\\temp\\hub41\\mushroom.png"}` for the record (scratch).
8. The stop tool, on a second short run (same local model): `start_agent_run {"text": "Draw a small green tree on this canvas."}`, wait 20 s, `stop_agent_run {"runId": "<second id>"}`, then `get_agent_run {"runId": "<second id>"}`. Passes when: `stop_agent_run` returns `stopped: true`; `get_agent_run` shows `state` `aborted` and `stoppedBy` `"mcp"` (no `timedOut`). Record what the run drew before the stop (it stays as one undo step).
9. If this session started pixel-studio: `pwsh -File scripts\hub.ps1 stop pixel-studio`.
Passes when (steps 3-7): `state` `completed` (or `max_steps` with a drawing); `step` events show `mode: "json"`; at least one drawing `tool_result` with `isError: false`; `costUsd` 0; the preview shows a mushroom-like drawing. Record steps, wall time, `usage`, and the first `usage` event's `inputTokens` (the real size of the JSON-action prompt in Strata's tokenizer). B stands when that number is 24,000 or more (Inkling's 32768 would leave under 8,800 tokens for every preview image, the history and the thinking replies of up to 25 steps). Below 24,000: write it down and ask the user whether to plan a separate Inkling-for-Pixel check (B's change stays: the alias was dead either way).

**K2 One VN review on an image built to be rejected (D8; VNO-70's `vno_comfy_free`). GPU, SVC.** After VNO-70 is merged and `pwsh -File scripts\hub.ps1 build vn-studio` ran. Start what is down: `hub.ps1 start acp-proxy comfyui vn-studio`. The critic list is `[paid, acp/llama/inkling-2-mini]`; `paid` (DeepSeek) has no vision and is skipped, so only Inkling reviews.
1. `vno_create_project {"book": {"title": "HUB-41 reject check", "slug": "hub41-reject-check", "places": [{"key": "square", "name": "Village square", "looks": "a small cobbled square with a stone fountain"}], "chapters": [{"title": "One", "scenes": [{"place": "square", "time": "noon", "beats": [{"text": "The square is quiet at noon."}]}]}]}, "lang": "en", "settings": {"art": {"review": true}}}`. A new throwaway project, only for this check (not the old `hub39-critic-check`).
2. `vno_asset_list {"slug": "hub41-reject-check", "kind": "bg"}`: the one background id (expected `bg_square_noon`; use the id it returns).
3. `vno_asset_set {"slug": "hub41-reject-check", "id": "<bg id>", "prompt": "A small cobbled village square with a stone fountain at noon, a crowd of ten people in bright coats standing around the fountain and talking, anime visual novel background"}`. Built to be rejected: the critic checks "For a background: no people" (`visual-novels-orchestrator/seed/prompts/art-critic/review_image.md:20`). No art-director call, so Strata is not needed.
4. `vno_asset_generate {"slug": "hub41-reject-check", "only": ["<bg id>"]}`, then `vno_wait {"slug": "hub41-reject-check"}` until the review job is done (up to 3 images and 3 reviews, about 15 minutes).
5. Read the review job's log ("art-critic rejected <id> (attempt n): ..."), `vno_asset_list` (`review` status and note), and the spend rows of `C:\Users\Infplane\VisualNovels\logs\spend\2026-11.md` (model, tokens, 0 USD).
6. `vno_comfy_free {}`: every lane `ok: true` (VNO-70; it failed with "Unexpected end of JSON input" before).
7. Delete the throwaway project: `vno_delete_project {"slug": "hub41-reject-check", "confirm": true}` (permanent; the user allowed deleting throwaway checks, see Questions 2; it runs only as part of K2, which needs the go-ahead), then `vno_list_projects` does not list it.
Passes when: at least one review rejects with one or more `problems`; every `problems` entry and every `revisedPrompt` is in English (read them); every review ran on `acp/llama/inkling-2-mini` at 0 USD; `vno_comfy_free` is ok for every lane; the project is gone. If the first review approves the crowd picture, K2 is "not exercised" and the miss is recorded as a finding about Inkling (not a pass, not a code failure).

## Acceptance criteria

| # | criterion | proof |
|---|---|---|
| H-1 | ROADMAP rows 31-33 carry the recorded outcomes; row 34 added | `git diff ROADMAP.md` against REQ-0030's Log and the two run logs |
| H-2 | HUB-40 N1 names `force: true` | `git diff .claude/tickets/HUB-40-extra-ideas/plan.md` (one line) |
| H-3 | hub docs no longer say Pixel's vision rows name `lmstudio` | `grep -rn "Pixel's vision rows" CLAUDE.md services.json README.md` prints nothing; `services.json` parses |
| H-4 | each repo ticket meets its own plan | the seven repo plans |
| H-5 | L1-L3 change only the listed lines | the `git diff --no-index` checks above |
| H-6 | the artist runs over MCP on a local model in JSON-action mode | K1 |
| H-7 | a rejected review writes English notes; `vno_comfy_free` works | K2 |

## UNTESTED (until the checks run)

- K1 and K2, each until the user says go. The Pixel window's wiring of the agent tools (K1 runs headless unless the window is open).
- The real prompt size behind B (K1 reads it).
- L1-L3 in the running apps (Pixel reads its roles on start; Scriptorium is not started by this plan; Edu on its next start).

## Questions for the user

1. Answered 2026-11-22 (user: 'Approve with both'): a stop tool is added; a new chat is the default over MCP.
2. K2 ends with a permanent delete of its own throwaway project: answered yes by the user's earlier words "you can delete throaway checks, we do not need test copies". The delete still happens only inside K2, which itself needs the go-ahead.
