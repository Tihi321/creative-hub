---
status: in-progress
request: REQ-0030
repos: [creative-hub, api-acp-proxy, scriptorium, book-translator, visual-novels-orchestrator, pixel-art-generator, midi-generator, edu-game-studio, cartoon-studio]
branch: HUB-38_acp-for-all
updated: 2026-11-21
---

# HUB-38 ACP for all: every app reaches every LLM, local ones included, through the ACP proxy

User request (verbatim): "update all repositores, added support for acp proxy for gufo, strata so we do not need to use llm, added support in acp for llama as well and we have model inkling,  we can focus on acp for all now".

Reading built: the full one. Every app that calls an LLM (Scriptorium, Book Translator, VN Studio, Pixel Studio, Chiptune Studio, Edu Studio, Cartoon Studio) gets its chat models from provider `acp` (`http://127.0.0.1:8787/v1`): the cloud agents as today plus `gufo/*`, `strata/*` and `llama/*`. The direct LM Studio (1234) and Strata (8080) providers stay in the code and are switched off in config, with two documented exceptions (Scriptorium embeddings until AAP-43, and the vision roles).

Inputs: `REQ-0030`, `research-proxy.md`, `research-apps.md` (this folder). Each repo ticket has its own self-contained plan (paths in the ticket map). The contracts C1 to C6 below are the single source; the repo plans copy them verbatim.

## Scope

1. Proxy (api-acp-proxy): AAP-42 forwards `reasoning_effort` and `chat_template_kwargs` to the local servers (thinking off again for the local roles); AAP-43 adds `POST /v1/embeddings` with `llama/nomic-embed-text-v1.5` on its own small llama-server beside the chat model.
2. Seven app repos: seeds and code defaults move to `acp` (C1, C2), the stale port 7461 becomes 8787 (C5), Strata (and, where nothing needs it, LM Studio) is `enabled: false` in the seed (C4), Inkling is listed and never a default (C1). Scriptorium also treats `gufo/`, `strata/`, `llama/` models behind the proxy as on this machine for `no_local_fallback` (SCP-65).
3. Hub: `services.json` (acp-proxy runs the desktop app from the repo and is in the default set; LM Studio leaves the default set; Strata variant paths fixed; Scriptorium `requires`), `scripts/hub.ps1` (electron `built` folder, `--hidden` and `-Window`, `requires`), README, CLAUDE.md, AGENTS.md, the skills (both copies of make-visual-novel, make-cartoon), `scripts/strata-probe.mjs` header, ROADMAP row.
4. Live data (after the user approves, section "Live data changes"): the proxy's `settings.json` and the seven data folders, with backups.
5. Live checks (section "Acceptance"), each marked when it loads a model onto the GPU or starts a service.

## Out of scope

- Moving any vision role off its current provider (decision 5). Listed with the check that would move it, below.
- Tools / function calling for local models, `stop` support, structured output (grammar) for local models, `reasoning_effort` mapping for the ACP agents (Codex, Claude), Responses API reasoning items, llama-server router mode, idle unload of a local model. (Checked: no app sends `stop`; grep of the seven `src` trees finds no `stop` request field.)
- Deleting the LM Studio or Strata provider code, their UI, their tests, or the `lmstudio`/`strata` provider rows (rows stay, switched off).
- Rewriting job history, logs or run logs that name old refs (VN Studio's old refs are only in `log.md` and `pipeline.json` error text: confirmed, nothing to migrate).
- A stable `strata/default` alias in the proxy (decided against, see Decisions D7).
- Downloading or installing anything (llama-server, Inkling files, Gufo Flash-Next, the nomic file): user steps.
- Starting Scriptorium's factory. Its only live check is the CLI `probe` (no factory).
- vibe-tts-flow, comfy-mcp, flow-music-mcp: no chat LLM (research, not re-checked).
- The ComfyUI-versus-local-LLM GPU check in VN/Edu/Cartoon autostart (still looks at Strata on 8080 only; Gufo 8081 and Llama 8082 are not seen). Recorded as a follow-up idea.

## Decisions

Binding (the user, 2026-11-21):

1. **Old providers: disable, keep code.** Config, seeds and defaults move to `acp` (`base_url http://127.0.0.1:8787/v1`) with `gufo/…`, `strata/…`, `llama/…` ids. LM Studio (1234) and Strata (8080) stay in the code, switched off.
2. **Repos:** Scriptorium, Book Translator, VN Studio, Pixel Studio, Chiptune Studio, Edu Studio, Cartoon Studio, the hub, and the proxy where it must change.
3. **Inkling:** `llama/inkling-2-mini` and `llama/inkling-2-mini-dspark` are listed in every app, never a default. Not runnable on this PC yet (no `D:\LlamaCpp\bin`, profile files missing: confirmed on disk).
4. **Embeddings:** a proxy ticket (AAP-43) serves the same nomic-embed-text-v1.5 so Scriptorium's index stays valid. Until it is merged and live-checked, Scriptorium's `embeddings:` stays on LM Studio as the one documented exception.
5. **Vision roles keep their current provider:** VN `art-critic`, Edu `art-critic`, Cartoon `frame-critic`, Pixel's vision rows. Listed below with the live check that would let each move.
6. **Proxy process:** the hub runs the desktop ACP Proxy app (the only build with the local-model coordinator), not the headless node. Its `settings.json` is the single place for caps, timeout, body size and bare aliases. `hub.ps1` no longer starts Strata or LM Studio by default.

Made in this plan (each also an open question below where the user may prefer otherwise):

- **D7 No proxy alias; exact ids.** The proxy lists `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` (the `model_name` of both `D:\Strata\terminal\strata-unsloth-ud-iq4_xs*.json`: confirmed). Apps use that exact id. Saved refs are rewritten once in the data (C3: 24 Scriptorium `book.md`, 9 Book Translator `project.json`; counted 2026-11-21, the research's "about 50" was a count of files with `role_models`, not of files with local refs). A proxy alias would not remove the app-side rewrite (`strata/x` must become `acp/strata/x` anyway), so it buys nothing.
- **D8 One local text model for the whole hub:** `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` (called LOCAL below). The proxy holds one local model on the GPU at a time across gufo, strata and llama, and a switch takes minutes; two apps on two local models would thrash. Gufo and Llama ids are listed, not defaults, and no fallback list names a second local model. Model on disk: `D:\Strata-data\models\unsloth-UD-IQ4_XS\` (confirmed).
- **D9 Strata under the proxy runs the `-parallel` bat with `maxConcurrent: 4`** (the hub's old default variant, `"parallel": 4` in its json: confirmed), so local throughput matches the old `concurrency: auto` of 4.
- **D10 Thinking passthrough (AAP-42).** The apps' local rows send `reasoning_effort: none` (Scriptorium note: thinking on made a 500-word story take 3.5 min instead of 25 s on LM Studio's Qwen). The proxy today forwards only `model, messages, stream, max_tokens` (`src/providers/local-openai.ts:166`: confirmed), so every local request would think. AAP-42 forwards it.
- **D11 Strata `-low` refs fold into LOCAL** (one proxy id cannot carry two `extra_body` variants). The checks that used `strata/default-low` run with thinking off.
- **D12 Proxy runs from the repo** (`node_modules\electron\dist\electron.exe .` with `dist/electron/main.js`; both exist: confirmed), like the hub's other Electron apps. It uses the same `%APPDATA%\api-acp-proxy\settings.json` (`main.ts:40-42`: confirmed). The portable exe extracts to `%TEMP%` on each start and lags master.

## Open questions (recommendation first)

- **Q1 AAP-42 (thinking passthrough) in or out?** Recommend in: small, and without it every local role thinks. Out: drop AAP-42, keep `extra_body` rows (harmless), accept slower local roles.
- **Q2 Strata `-low` checks with thinking off (D11)?** Recommend accept. Alternative: after AAP-42, give LOCAL `reasoning_effort: low` in Scriptorium and Edu only (all their roles then think a little).
- **Q3 Strata `-parallel` with `maxConcurrent 4` (D9)?** Recommend yes. Alternative: keep the solo bat and 1 (slower, less VRAM).
- **Q4 Proxy from the repo (D12) or the portable exe?** Recommend the repo. Alternative: `kind exe` with `C:\projects\Personal\api-acp-proxy\release\ACP-Proxy-Portable-0.1.0-x64.exe` (stale until rebuilt).
- **Q5 Scriptorium `requires: ["acp-proxy", "lmstudio"]`** so `hub.ps1 start scriptorium -Force` also brings up LM Studio for embeddings until AAP-43 is live. Recommend yes; alternative: start LM Studio by hand.
- **Q6 Pixel and Chiptune agents on LOCAL in JSON-action mode** (today LM Studio's 27B with native tool calls). Recommend yes (D8). Alternative: `acp/gufo/Qwen3.8-27B` (same 27B family as before, but a GPU switch whenever another app uses LOCAL).
- **Q7 Proxy `maxBodyBytes`:** keep 20971520 (live) rather than the hub env's 8388608, since the vision critics send images. Recommend keep 20 MiB.
- **Q8 Scriptorium archivist under `fallback_shared: true`:** `acp/antigravity/gemini-4-hydrogen` and LOCAL are both kind `acp`, so hydrogen takes the LOCAL row's place and the archivist loses its local fallback (`registry.ts:629-647` rule). Recommend accept (DeepSeek stays as the paid row). Alternative: a second LOCAL-kind row is not possible without a second provider; leave as is.
- **Q9 Gufo `flash-next-q4`** has no model folder (confirmed). Recommend listing it anyway (vision candidate) and installing it later (user step U4), or the user says drop it from C1.

## Contracts (single source; every repo plan copies them verbatim)

### C1 The `acp` provider every app ships (seed and live)

```yaml
  - id: acp
    name: ACP proxy
    kind: openai-compat
    enabled: true
    local: true
    base_url: http://127.0.0.1:8787/v1
    concurrency: 4            # Scriptorium live: 8; Edu and Cartoon: 2 (as today)
    json_schema: false
    discover: true
    discover_skip: [ qwen-image, nomic-embed ]   # image and embedding models answer chat with 400; only where the schema has discover_skip
    models:
      # ... the app's existing cloud rows (codex/*, antigravity/*, claude/*) stay as they are ...
      # Local models through the proxy (HUB-38). One local model is loaded at a time across gufo, strata and llama;
      # a request for another one waits until the proxy has switched (minutes). LOCAL is the strata row.
      - id: strata/qwen3.8-flash-next-unsloth-ud-iq4_xs
        family: qwen
        context: 131072
        extra_body: { reasoning_effort: none }
      - id: gufo/Qwen3.8-27B
        family: qwen
        context: 32768
        extra_body: { reasoning_effort: none }
      - id: gufo/deepseek4
        family: deepseek
        context: 16384
        extra_body: { reasoning_effort: none }
      - id: gufo/flash-next-q4
        family: qwen
        context: 32768
        vision: true
        extra_body: { reasoning_effort: none }
      - id: llama/inkling-2-mini
        family: inkling
        context: 32768
        vision: true
      - id: llama/inkling-2-mini-dspark
        family: inkling
        context: 32768
        vision: true
```

Per-app variants: Pixel Studio and Chiptune Studio add `tools: false` to every local row (JSON-action mode; the proxy answers a request with tools to a local model with 400 `model_not_capable`). Where an app's schema rejects a key (`vision`, `discover_skip`, `extra_body`), drop that key for that app and say so in its changelog. Contexts: Strata `--max-context 131072` (its json), Gufo and Llama from their profile args (`--context` / `ctxSize`), as in the proxy's settings.

### C2 Defaults

- LOCAL = `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`. Every role, fallback row, picker default and code default that named `strata/default`, `strata/default-low`, the alias `strata`, or an LM Studio chat model now names LOCAL, the alias `acp` (VN, Edu, Cartoon: `acp` = the first `acp` row of `fallbacks`, which is LOCAL), or `local` (Pixel and Chiptune `roles.md` alias).
- `fallbacks` rows: the row that was `strata/default` becomes LOCAL; a `lmstudio/<chat model>` row is removed, except in VN, Edu and Cartoon where it stays as the target of the `lmstudio` alias for the vision role (`fallback_shared: false` there, so the row adds no model to other roles).
- No default ever names a `gufo/*` or `llama/*` model.

### C3 Saved-ref rewrite (data only, once)

Exact whole-token replacement, values only:

| old ref | new ref |
|---|---|
| `strata/default`, `strata/default-low`, `strata/qwen3.8-flash-next`, `strata/qwen3.8-flash-next-low` | LOCAL |
| `lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic`, `lmstudio/gemma-4-e4b-it`, `lmstudio/google/gemma-4-e4b`, `lmstudio/nail-qwen3.6-35b-a3b-mtp`, `lmstudio/tiel-coder-35b-a3b-mtp`, `lmstudio/ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp`, `lmstudio/poolside/laguna-s-2.1` | LOCAL |
| `lmstudio/minicpm-v-4.7-35b-a3b` | LOCAL in Scriptorium (text only); unchanged elsewhere |

### C4 Old providers

| app | `strata` row | `lmstudio` row |
|---|---|---|
| Scriptorium | `enabled: false` | enabled; models reduced to `text-embedding-nomic-embed-text-v1.5`; `discover: false` (embeddings only, until AAP-43 live; then `enabled: false`) |
| Book Translator | `enabled: false` | `enabled: false` (already off live) |
| VN Studio | `enabled: false` | unchanged (vision: `art-critic`) |
| Pixel Studio | `enabled: false` | unchanged (vision rows `ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp`, `google/gemma-4-e4b`) |
| Chiptune Studio | `enabled: false` | `enabled: false` |
| Edu Studio | `enabled: false` | unchanged (vision: `art-critic`) |
| Cartoon Studio | `enabled: false` | unchanged (vision: `frame-critic`) |

### C5 Port 8787

Every seed, doc, placeholder and test that says `http://127.0.0.1:7461/v1` says `http://127.0.0.1:8787/v1`. VN Studio, Cartoon Studio, Pixel Studio and Chiptune Studio get a one-time seed migration `acp-port-8787-v1` that rewrites only that exact value of the `acp` row's `base_url` in `config/providers.md`, the same rule as Book Translator `src/engine/store/migrate.ts:328-348` (VN and Cartoon: an entry in `src/engine/store/seedMigrations.ts`, the list that holds `providers-acp-v1`; Cartoon has that file: the research said it had none, checked). Edu has no 7461 in its seed or code (only in the live prose, L7) and gets no migration.

### C6 What the proxy offers the apps (after AAP-42, AAP-43)

- `reasoning_effort` (string) and `chat_template_kwargs` (object) in a chat request to `gufo/*`, `strata/*`, `llama/*` are sent upstream as they are. Other sampling fields stay dropped; `tools` stays 400.
- `POST /v1/embeddings` `{ model: "llama/nomic-embed-text-v1.5", input: string | string[] }` answers the OpenAI shape `{ object: "list", data: [{ object: "embedding", index, embedding: number[768] }], model, usage }`; it runs beside the chat model (never evicts it). The client adds nomic's `search_document: ` / `search_query: ` prefixes itself (Scriptorium does, `registry.ts:385`).

## Ticket map

Next free ids confirmed on 2026-11-21 from each repo's ROADMAP.md, `.claude/tickets` and branches. **The research was out of date for the proxy:** AAP-40 (`AAP-40_llama-model-picker`) is in progress in a dirty working tree, so the proxy tickets are AAP-42 and AAP-43.

| id | repo | branch | one line | depends on |
|---|---|---|---|---|
| AAP-42 | api-acp-proxy | `AAP-42_local-thinking` | forward `reasoning_effort` / `chat_template_kwargs` to local servers | AAP-40 and AAP-41 (playground redesign, another session's ticket) merged (same working tree) |
| AAP-43 | api-acp-proxy | `AAP-43_local-embeddings` | `/v1/embeddings` + llama `embedding` profile on its own port beside the chat model | AAP-40 and AAP-41 (playground redesign, another session's ticket) merged, and AAP-42 merged (shares `settings.ts`, `local-openai.ts`, `local-servers.ts`, `electron/main.ts`) |
| SCP-65 | scriptorium | `SCP-65_acp-for-all` | seeds and defaults to acp; per-model on-device rule for proxy local models; probe default | none |
| BTT-36 | book-translator | `BTT-36_acp-for-all` | seeds and defaults to acp | none |
| VNO-67 | visual-novels-orchestrator | `VNO-67_acp-for-all` | seeds/defaults to acp; 7461 to 8787 migration | none |
| PAR-19 | pixel-art-generator | `PAR-19_acp-for-all` | seeds/defaults to acp (JSON-action rows); 7461 to 8787 migration | none |
| MDI-18 | midi-generator | `MDI-18_acp-for-all` | as PAR-19 | none |
| EGS-71 | edu-game-studio | `EGS-71_acp-for-all` | seeds and defaults to acp | none |
| CTS-54 | cartoon-studio | `CTS-54_acp-for-all` | seeds/defaults to acp, acp on in seed; 7461 to 8787 migration | none |
| HUB-38 | creative-hub | `HUB-38_acp-for-all` | services.json, hub.ps1, docs, skills, roadmap; then live data and checks | code: none; live data L1-L8: the seven app tickets merged; L2b: AAP-43 merged and C9 passed |

Repo plans: `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-42-local-thinking\plan.md`, `...\AAP-43-local-embeddings\plan.md`, `C:\projects\Personal\scriptorium\.claude\tickets\SCP-65-acp-for-all\plan.md`, `C:\projects\Personal\book-translator\.claude\tickets\BTT-36-acp-for-all\plan.md`, `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-67-acp-for-all\plan.md`, `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-19-acp-for-all\plan.md`, `C:\projects\Personal\midi-generator\.claude\tickets\MDI-18-acp-for-all\plan.md`, `C:\projects\Personal\edu-game-studio\.claude\tickets\EGS-71-acp-for-all\plan.md`, `C:\projects\Personal\cartoon-studio\.claude\tickets\CTS-54-acp-for-all\plan.md`.

Order:

1. In parallel (separate repos, no shared files): SCP-65, BTT-36, VNO-67, PAR-19, MDI-18, EGS-71, CTS-54, and the HUB-38 code tasks H1 to H7. None needs the proxy tickets: the `extra_body` rows are harmless before AAP-42.
2. Proxy, one after the other in its single working tree: AAP-40 and AAP-41 (not ours) merge, then AAP-42, then AAP-43.
3. Hub-only, after the user approves and step 1 is merged: live data L0 to L8, then checks C1 to C8.
4. After AAP-43 is merged and the user has done U2 and U5: check C9 (embedding parity), then L2b (Scriptorium embeddings to the proxy, LM Studio off in Scriptorium) and H8 (drop `lmstudio` from Scriptorium `requires`).
5. After U2/U3 (Inkling installed): check C10 (Inkling answers). After U4: Flash-Next can be checked the same way.

## Hub tasks (branch `HUB-38_acp-for-all`)

- **H1 `services.json`**
  - `acp-proxy`: `name` "ACP Proxy (one OpenAI-compatible API for every model: the Codex, Antigravity and Claude agents and the local Gufo, Strata and Llama.cpp models)"; `default: true`; `start` becomes `{ "kind": "electron", "args": [".", "--hidden"], "built": "dist" }` (no `env`: settings.json is the single place, decision 6); `build` stays `npm run build`; `note` rewritten: "Provider `acp` (base_url http://127.0.0.1:8787/v1, json_schema false) of all seven apps; their only route to LLMs, local ones included (HUB-38). The desktop app (run from the repo, tray, `--hidden`) is the only build that starts and switches the local servers (Gufo 8081, Strata 8080 with `D:\Strata\terminal\run-unsloth-ud-iq4_xs-parallel.bat`, Llama.cpp 8082): one local model on the GPU at a time, a switch takes minutes, the request waits. Caps, timeout (900000), body size, `listBareAliases: false`, per-provider `maxConcurrent` (codex 4, antigravity 3, claude 2, strata 4, gufo 1, llama 1) are in `%APPDATA%\api-acp-proxy\settings.json` or its Server page, never in env here. The headless `node dist/index.js` cannot start local models. Local models: no tools, `response_format` is prompt-only, `reasoning_effort` passes (AAP-42), embeddings `llama/nomic-embed-text-v1.5` (AAP-43). Antigravity through it breaks clause 6 of Antigravity's terms: the user accepted that risk (2026-10-22)."
  - `lmstudio`: `default: false`; `name` "LM Studio (Scriptorium's nomic embeddings until AAP-43; vision critics' local models)"; `note`: "Not a chat provider any more (HUB-38): apps reach local LLMs through acp-proxy. Still used by Scriptorium's embeddings (`lmstudio/text-embedding-nomic-embed-text-v1.5`) until AAP-43 is live, and by the vision roles that keep it (VN and Edu art-critic, Cartoon frame-critic, Pixel's vision rows). `hub.ps1 start scriptorium` starts it (requires). Do not load a chat model in it while the proxy runs one."
  - `strata`: `start.path` and every `variants` value move from `D:\Strata\run-*.bat` to `D:\Strata\terminal\run-*.bat` (the old paths do not exist: confirmed; the four bats are in `D:\Strata\terminal`); `note`: "The ACP proxy starts Strata itself on an `acp/strata/*` request (providers.strata.command in its settings.json). Start it by hand only to diagnose (scripts/strata-probe.mjs) and only when the proxy has no local model loaded: a hand-started Strata is passed through but never stopped by the proxy, so a gufo or llama request would load a second model beside it."
  - `scriptorium`: add `"requires": ["acp-proxy", "lmstudio"]` (Q5).
  - `_about`: add one sentence: "`requires` lists ids that `hub.ps1 start` starts first."
- **H2 `scripts/hub.ps1`**
  - Header comment line for `start`: "start the default set (not scriptorium, not strata, not lmstudio)".
  - `Start-Service1`, `electron` branch: the built folder is `$st.built` when set, else `out` (`if (-not (Test-Path (Join-Path $repo $built)))`, message names it).
  - `-Window` for electron: also strip `--hidden`; add `--mcp` only when the original args had `--headless` or `--mcp-only`.
  - `requires`: right after the `$s.warning -and -not $Force` gate passes, start each id in `$s.requires` with `Start-Service1` (skip unknown ids with a yellow line; a service already up says so as today).
  - No change to `Show-Status`, `Get-Health` (the proxy's `/healthz` notes keep working).
- **H3 `README.md`**: line 25 "LLMs: the ACP proxy (`acp`: local Gufo, Strata and Llama.cpp models, and the Codex, Antigravity and Claude subscriptions), paid APIs (per repo config/roles.md), or Claude Code itself (`client` provider, see the skill)"; table rows `lmstudio` (purpose "Scriptorium's nomic embeddings until AAP-43; the vision critics' local models"), `strata` (purpose "local LLM server, started by the ACP proxy on request; by hand only to diagnose", start `D:\Strata\terminal\run-unsloth-ud-iq4_xs-parallel.bat`), `acp-proxy` (purpose "the only LLM route of all seven apps, local models included (HUB-38); one local model at a time", start "`electron . --hidden` from the repo (desktop app; settings in its settings.json)"); line 59 default set "vn-studio, pixel-studio, chiptune-studio, book-translator, edu-studio, vibetts, comfyui, comfy-mcp, acp-proxy" (check the list against `default: true` in services.json after H1); one new paragraph after line 76: "Every app reaches LLMs through the ACP proxy. A local model (Gufo, Strata, Llama.cpp) is loaded by the proxy on the first request that names it and stays loaded; one at a time on the GPU; the first request after a switch can wait minutes. Do not run image generation in ComfyUI while a local model is loaded."
- **H4 `CLAUDE.md` and `AGENTS.md` line 3**: the tool list replaces "LM Studio, Strata" with "the ACP proxy (local Gufo, Strata and Llama.cpp models)". CLAUDE.md gets one bullet after the `hub.ps1` bullet: "Every app reaches every LLM through the ACP proxy (`acp`, port 8787), local models included (HUB-38). LM Studio stays only for Scriptorium's embeddings (until AAP-43) and the vision roles; never load a chat model in LM Studio or start Strata by hand while the proxy holds a local model." (These are the user's instruction files: the plan's approval covers this edit; nothing else in them changes.)
- **H5 skills**: `.claude/skills/make-visual-novel/SKILL.md` and its mirror `.agents/skills/make-visual-novel/SKILL.md` (same text, only the Codex wording differs, HUB-37 rule): line 12 default set as in H3; line 16 "the apps' own models (through the ACP proxy: the local Gufo/Strata/Llama models or the Codex, Antigravity, Claude subscriptions; or paid APIs), or **you**"; line 18 heading "Doing the model work yourself (no local model, $0)"; line 162 "Scriptorium or Book Translator jobs fail with model errors: no model answered. Check `hub.ps1 status` (acp-proxy up) and `curl http://127.0.0.1:8787/healthz`; the first request to a local model can wait minutes while the proxy loads it. Scriptorium's embeddings need LM Studio until AAP-43 (`hub.ps1 start lmstudio`). Then `scriptorium.check_servers`."; line 163 "... and do not run a local model through the proxy at the same time as image generation". `.claude/skills/make-cartoon/SKILL.md` line 14: "Strata is not running during ComfyUI work (shared memory)" becomes "No local model runs through the ACP proxy during ComfyUI work (shared memory): keep the roles on `client/claude-code`". make-edu-game and make-video: no mention (checked), unchanged.
- **H6 `scripts/strata-probe.mjs`**: header comment line 3 adds "Strata now runs under the ACP proxy (HUB-38), which starts it on port 8080; this probe talks to 8080 directly, for diagnosis." No logic change.
- **H7 `ROADMAP.md`**: row 31 after HUB-37: `| 31 | HUB-38 | ACP for all: every app reaches every LLM, local Gufo/Strata/Llama models included, through the ACP proxy; LM Studio and Strata providers switched off (code kept); Inkling listed, not default; proxy thinking passthrough and embeddings (.claude/tickets/HUB-38-acp-for-all/plan.md, REQ-0030) | api-acp-proxy (AAP-42, AAP-43), scriptorium (SCP-65), book-translator (BTT-36), visual-novels-orchestrator (VNO-67), pixel-art-generator (PAR-19), midi-generator (MDI-18), edu-game-studio (EGS-71), cartoon-studio (CTS-54), hub | the user installs llama-server, Inkling and the nomic file; GPU checks with the user's go-ahead | In progress |`, and the "Each tool's own roadmap" ACP proxy row "text only (not needed by the hub)" becomes "AAP-42, AAP-43 for HUB-38; local-model follow-ups (tools, stop, router mode)".
- **H8 (after C9 and L2b)**: remove `lmstudio` from Scriptorium's `requires`; `lmstudio` note drops the embeddings sentence.

## Live data changes (applied only after the user approves; each app stopped first, backup first)

L0 Backup. For every file below, copy it next to itself as `<name>.bak-HUB-38` before editing (never into a repo: the proxy's settings.json holds login method ids). Scriptorium books: zip the 24 `book.md` files that C3 touches to `~\Scriptorium\backup-HUB-38-books.zip`; Book Translator: the 9 `project.json` to `~\BookTranslator\backup-HUB-38-projects.zip`. The way back is the `.bak` files plus the app code, which still has both providers.

Stop first (each a service stop: the user's go-ahead): the proxy (stopping it stops its Gufo server, live on 8081 with `qwen-image-2.1` at 17:35 today), book-translator, vn-studio, edu-studio, pixel-studio, chiptune-studio, cartoon-studio if running. Scriptorium is not running and is not started. Edits are plain text edits of YAML front matter / JSON; nothing else in the files changes.

| # | file | key | old | new |
|---|---|---|---|---|
| L1 | `%APPDATA%\api-acp-proxy\settings.json` | `server.listBareAliases` | `true` | `false` |
| L1 | same | `server.timeoutMs` | `300000` | `900000` |
| L1 | same | `server.maxBodyBytes` | `20971520` | `20971520` (kept, Q7) |
| L1 | same | `providers.codex.maxConcurrent` | absent (global 4) | `4` |
| L1 | same | `providers.antigravity.maxConcurrent` | absent (global 4) | `3` |
| L1 | same | `providers.claude.maxConcurrent` | absent (global 4) | `2` |
| L1 | same | `providers.strata.command` | `D:\Strata\terminal\run-unsloth-ud-iq4_xs.bat` | `D:\Strata\terminal\run-unsloth-ud-iq4_xs-parallel.bat` (Q3) |
| L1 | same | `providers.strata.maxConcurrent` | `1` | `4` (Q3) |
| L2 | `~\Scriptorium\config\providers.md` | `acp` | C1 without local rows, concurrency 4 | C1 (local rows, `discover_skip: [ qwen-image, nomic-embed ]`), `concurrency: 8` |
| L2 | same | `lmstudio.models` / `discover` | 7 rows / `true` | only `text-embedding-nomic-embed-text-v1.5` (family nomic, embedding true) / `false` |
| L2 | same | `strata.enabled` | absent (on) | `false` |
| L2 | `~\Scriptorium\config\roles.md` | roles `editor-in-chief, idea-generator, architect, writer, publisher` | `[paid, strata, lmstudio]` | `[paid, acp]` |
| L2 | same | `developmental-editor, line-editor, copy-editor, beta-reader, child-safety-reviewer, read-aloud-reviewer` | `[strata, lmstudio, paid]` | `[acp, paid]` |
| L2 | same | `continuity-checker, originality-checker, fact-checker, researcher` | `[strata/default-low, lmstudio, paid]` | `[acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs, paid]` |
| L2 | same | `archivist` | `[acp/antigravity/gemini-4-hydrogen, strata/default-low, lmstudio, paid]` | `[acp/antigravity/gemini-4-hydrogen, acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs, paid]` |
| L2 | same | `embeddings` | `lmstudio/text-embedding-nomic-embed-text-v1.5` | unchanged until L2b |
| L2 | `~\Scriptorium\config\settings.md` | `fallbacks` | `deepseek/deepseek-flash, strata/default, lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic` | `deepseek/deepseek-flash, acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` |
| L2 | `~\Scriptorium\books\*\book.md` (24 files) | `role_models` values | C3 old refs | C3 new refs |
| L2b | `~\Scriptorium\config\providers.md` (after AAP-43 + C9) | `acp.models` | — | add `- id: llama/nomic-embed-text-v1.5`, `family: nomic`, `embedding: true` |
| L2b | `~\Scriptorium\config\roles.md` | `embeddings` | `lmstudio/text-embedding-nomic-embed-text-v1.5` | `acp/llama/nomic-embed-text-v1.5` |
| L2b | `~\Scriptorium\config\providers.md` | `lmstudio.enabled` | absent (on) | `false` |
| L3 | `~\BookTranslator\config\providers.md` | `strata.enabled` | absent (on) | `false` |
| L3 | same | `acp.models` | cloud rows | + C1 local rows (`discover_skip` if supported) |
| L3 | `~\BookTranslator\config\defaults.json` | `agentModels.glossary`, `.qa` | `["strata/default", "deepseek/deepseek-v4-flash"]` | `["acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs", "deepseek/deepseek-v4-flash"]` |
| L3 | same | `agentModels.translator`, `.proofreader` | `["deepseek/deepseek-v4-flash", "strata/default"]` | `["deepseek/deepseek-v4-flash", "acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs"]` |
| L3 | same | `groupDefaults` | `{"paid": "deepseek/deepseek-v4-flash", "strata": "strata/default"}` | `{"paid": "deepseek/deepseek-v4-flash", "acp": "acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs"}` (BTT-36 confirms the `acp` group key works; if not, keep the key name the code expects) |
| L3 | `~\BookTranslator\projects\*\project.json` (9) | `settings.agentModels.{glossary,translator,proofreader,qa}[]` | `strata/qwen3.8-flash-next` | LOCAL |
| L4 | `~\VisualNovels\config\providers.md` | `acp.base_url` | `http://127.0.0.1:7461/v1` | `http://127.0.0.1:8787/v1` |
| L4 | same | `acp.models` | cloud rows | + C1 local rows |
| L4 | same | `strata.enabled` | absent | `false` |
| L4 | `~\VisualNovels\config\roles.md` | `director, art-director` | `[paid, strata, lmstudio]` | `[paid, acp]` |
| L4 | same | `art-critic` | `[paid, strata, lmstudio]` | `[paid, lmstudio]` (vision, decision 5) |
| L4 | same | `script-analyst, composer, stage-director, voice-director` | `[strata, lmstudio, paid]` | `[acp, paid]` |
| L4 | same | `edition-aligner` | `[strata/default-low, lmstudio, paid]` | `[acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs, paid]` |
| L4 | `~\VisualNovels\config\settings.md` | `fallbacks[1]` | `strata/default` | LOCAL (rows 0 and 2 unchanged) |
| L5 | `~\PixelStudio\config\providers.md` | `acp.base_url` | 7461 | 8787 |
| L5 | same | `acp.models` | cloud rows (`tools: false`) | + C1 local rows with `tools: false` |
| L5 | same | `strata.enabled` | absent | `false` |
| L5 | `~\PixelStudio\config\roles.md` | `aliases` | `lmstudio: …ista-daslab…`, `strata: strata/default`, `cloud`, `claude` | `local: acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, `lmstudio: lmstudio/ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp` (vision), `cloud`, `claude` (`strata` alias removed) |
| L5 | same | `artist`, `palette` | `[lmstudio]` | `[local]` |
| L5 | `~\PixelStudio\config\app.json` | `selectedModel` | `strata/default` | LOCAL |
| L5 | `~\PixelStudio\config\models.md` | `shown` | `…, lmstudio/lfm2.5-24b-a2b, lmstudio/nail-qwen3.6-35b-a3b-mtp, lmstudio/tiel-coder-35b-a3b-mtp, strata/default` | drop those four; add LOCAL, `acp/gufo/Qwen3.8-27B`, `acp/gufo/deepseek4`, `acp/llama/inkling-2-mini`, `acp/llama/inkling-2-mini-dspark`; keep the `minicpm-v` entries, acp cloud and deepseek |
| L6 | `~\ChiptuneStudio\config\providers.md` | `acp.base_url`, `acp.models`, `strata.enabled` | as L5 | as L5 |
| L6 | same | `lmstudio.enabled` | absent | `false` |
| L6 | `~\ChiptuneStudio\config\roles.md` | `aliases`; `composer`, `theory` | as L5; `[lmstudio]` | `local: LOCAL` (drop `strata`, keep `lmstudio` alias text, unused); `[local]` |
| L6 | `~\ChiptuneStudio\config\app.json` | `selectedModel` | `strata/default` | LOCAL |
| L6 | `~\ChiptuneStudio\config\models.md` | `shown` | `…lmstudio/* (4), strata/default, strata/default-low` | drop those six; add the five acp local ids as L5 |
| L7 | `~\EduGames\config\providers.md` | `acp.models`; `strata.enabled` | cloud rows; absent | + C1 local rows; `false` |
| L7 | same, prose | the `acp` paragraph naming `http://127.0.0.1:7461/v1` (line 254) | 7461, "off by default" | 8787, "on" |
| L7 | `~\EduGames\config\roles.md` | the 13 roles `[paid, strata, lmstudio]` | as is | `[paid, acp]` |
| L7 | same | `researcher, fact-checker` | `[strata/default-low, lmstudio, paid]` | `[acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs, paid]` |
| L7 | same | `accessibility-reviewer, child-safety-reviewer, playtester` | `[strata, lmstudio, paid]` | `[acp, paid]` |
| L7 | same | `art-critic` | `[gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, lmstudio]` | unchanged (vision) |
| L7 | `~\EduGames\config\settings.md` | `fallbacks[1]` | `strata/default` | LOCAL |
| L8 | `~\CartoonStudio\config\providers.md` | `acp.enabled`, `acp.base_url`, `acp.models` | `false`, 7461, as is | `true`, 8787, + C1 local rows |
| L8 | same | `strata.enabled` | absent | `false` |
| L8 | `~\CartoonStudio\config\roles.md` | seven roles `[client/claude-code, strata, lmstudio]` | as is | `[client/claude-code, acp]` |
| L8 | same | `frame-critic` | `[client/claude-code, strata, lmstudio]` | `[client/claude-code, lmstudio]` (vision) |
| L8 | `~\CartoonStudio\config\settings.md` | `fallbacks[1]` | `strata/default` | LOCAL |

C3 rewrite for L2 and L3: a script in `C:\projects\Personal\creative-hub\.claude\temp\hub38-rewrite-refs.mjs` (Node, no deps) reads each file, replaces only whole tokens from the C3 table (regex `(?<![\w/.-])<old>(?![\w/.-])`) inside the YAML front matter (`book.md`) or `settings.agentModels` (`project.json`, parsed and re-serialised with the file's indentation), prints a count per file and refuses to write a file it cannot parse. Dry run first; the counts must match 24 books / 9 projects (2026-11-21 counts); write only after the dry run is read.

After L1: start the proxy (`hub.ps1 start acp-proxy`, a service start: go-ahead). After L2 to L8: start the apps that were running.

## Acceptance

GPU = loads a model onto the GPU; SVC = starts or stops a service. Both need the user's go-ahead at run time. Scriptorium is never started; its check is the CLI `probe`.

| # | criterion | check |
|---|---|---|
| C1 | proxy settings applied | GET `/v1/models`: no bare ids (no `gpt-6-luna` without prefix); `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, `gufo/*`, `llama/*` listed. GET `/healthz`: `codex 4, antigravity 3, claude 2, strata 4, gufo 1, llama 1` max_concurrent. (SVC for the restart) |
| C2 | hub starts the proxy and no direct local server | `hub.ps1 start` (SVC): acp-proxy up or "already up"; no line for lmstudio or strata; after it, nothing listens on 1234 or 8080 unless the user started it. `hub.ps1 variants strata`: four rows, Exists `yes`. `hub.ps1 start acp-proxy -Window` opens the window (or is "already up"). |
| C3 | every app lists the acp local models and Inkling, defaults point at LOCAL | per app, its model list (Scriptorium `probe` discovery line; BTT, VN, Edu, Cartoon status/models MCP tool or Models page; Pixel/Chiptune Settings > Providers): the six C1 local ids present; the role defaults / selectedModel resolve to LOCAL; no default names gufo/llama. No GPU. |
| C4 | thinking off reaches the local model (AAP-42) | one curl chat to `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` with `reasoning_effort: "none"`, `max_tokens: 200`: answer with empty or no `reasoning_content`, response header `x-acp-proxy-ignored-params` does not list `reasoning_effort`. GPU (loads Strata) |
| C5 | Scriptorium answers through LOCAL without the factory | `npm run engine -- probe --model acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs --data C:\Users\Infplane\Scriptorium` (yarn/npm with the fnm default alias dir on PATH): a streamed sentence, cost `0 (local)`, and the embedding line from LM Studio (until L2b). GPU (Strata already loaded by C4: no switch); LM Studio must be up (SVC). |
| C6 | engine-lineage app end to end (Book Translator) | one chunk of a throwaway project (`hub.ps1 call book-translator` create + translate one short paragraph, `agentModels` all LOCAL): status done, the job log names `acp/strata/...`. GPU (no switch if Strata is loaded). |
| C7 | JSON-action app end to end (Pixel Studio) | one artist request through MCP (or the chat) with LOCAL: the artwork changes, no 400 `model_not_capable` in the proxy log. GPU (no switch). Chiptune: same with one `composer` request (UNTESTED if skipped). |
| C8 | old refs gone, backups present | the C3 dry-run after L2/L3 reports 0 remaining old refs; every `.bak-HUB-38` file and both zips exist. |
| C9 | embedding parity (AAP-43) | for three fixed strings (`search_document: The lighthouse keeper counted ships.`, `search_query: who counted ships`, `search_document: Rain on the salt line.`) the vectors from LM Studio (`lmstudio/text-embedding-nomic-embed-text-v1.5`) and the proxy (`llama/nomic-embed-text-v1.5`) have dimension 768 and cosine similarity >= 0.999 each. Loads two small embedding models (GPU, small); LM Studio up (SVC). Then `probe` again after L2b: the embedding line comes from acp. |
| C10 | Inkling answers (after U2, U3) | one curl chat to `llama/inkling-2-mini` (and `-dspark` if installed), `max_tokens: 100`: 200 with text. GPU (switch from Strata to Llama: minutes). |

Tests in the repo tickets are listed in their plans (test-discipline: one test per behaviour, extend existing tests). The hub changes have no test file; C2 is their check.

## Vision roles that stay (decision 5) and the check that would move each

| role | today | candidate through the proxy | live check before moving it |
|---|---|---|---|
| VN `art-critic` | `[paid, lmstudio]` (vision filter keeps LM Studio's vision model; minicpm-v-4.7-35b-a3b is VN's configured vision row) | `acp/llama/inkling-2-mini` or `acp/gufo/flash-next-q4` | after U2/U3 (or U4): run the art-critic on 3 known images of a test project (1 good, 2 with a set flaw) with the candidate and with the LM Studio model; the candidate must give the same pass/revise verdicts and answer within the 15 min request timeout including the switch |
| Edu `art-critic` | `[gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, lmstudio]` | same | the same 3-image check through Edu's art-critic |
| Cartoon `frame-critic` | `[client/claude-code, lmstudio]` | same, after `client/claude-code` | one contact sheet with a known off-model pose: the candidate names it |
| Pixel vision rows (`lmstudio/ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp`, `lmstudio/google/gemma-4-e4b`, `minicpm-v` in the picker) | LM Studio | `acp/llama/inkling-2-mini` (C1 row has `vision: true`, `tools: false`) | one chat with an attached image in Pixel through the acp row: the answer describes the image; JSON-action mode works with an image |

Ideas found while planning (not planned): the Strata config has `--vision` and an mmproj (`D:\Strata\terminal\strata-unsloth-ud-iq4_xs.json`), and `D:\Gufo\models\qwen27-q4\mmproj-BF16.gguf` exists, but the proxy refuses images to Strata and the Gufo Qwen27 profile has `vision: false` and no `--mmproj`. Either would give the critics a local vision model without a GPU switch (a proxy follow-up).

## Research claims checked (2026-11-21)

Confirmed: the live `/v1/models` list and `/healthz` caps (gufo/strata/llama `max_concurrent: 1`); the 8787 listener is `ACP Proxy.exe` (pid 18408) from `%TEMP%`; settings.json `listBareAliases: true`, `timeoutMs: 300000`, `maxBodyBytes: 20971520`; no `/v1/embeddings`; the local upstream body carries only `model, messages, stream, max_tokens`; `D:\LlamaCpp\bin` and `D:\Gufo\models\flash-next-q4` missing; the 7461 seeds in VN, Pixel, Chiptune, Cartoon; Scriptorium `on_device` excludes `acp`.

Wrong or out of date in the research:
- Latest proxy ticket is AAP-40 (in progress, dirty tree), not AAP-39; the proxy tickets here are AAP-42 and AAP-43.
- AAP-41 was taken by another session (`AAP-41-playground-redesign`, created 2026-11-21 17:42) while this plan was written; the proxy tickets here are AAP-42 and AAP-43.
- `services.json` Strata paths `D:\Strata\run-*.bat` do not exist; the four bats are in `D:\Strata\terminal\` (the proxy's path is the right one).
- Cartoon Studio has `src/engine/store/seedMigrations.ts` (research: none).
- Saved local refs: 24 Scriptorium `book.md` files (not about 50) and 9 Book Translator `project.json`; VN projects hold them only in logs (no migration needed).
- `stop` is not sent by any app (grep of the seven `src` trees), so it is no blocker.
- The proxy restarted since the research (uptime 984 s at 17:35) and its Gufo server is up on 8081 serving `qwen-image-2.1`.
- Strata runs with `--vision` and an mmproj, and Gufo's `qwen27-q4` folder has `mmproj-BF16.gguf`; the proxy just does not offer vision for them (idea above).
- LM Studio's nomic file is not in `~\.lmstudio\models` (bundled with the app; user step U5).

## Steps for the user

- U1 Approve this plan and answer Q1 to Q9 (or accept the recommendations).
- U2 Install the llama.cpp build: ACP Proxy app > Llama.cpp page > install the managed build (source unsloth, backend rocm-gfx1151, into `D:\LlamaCpp\bin`). Needed for Inkling and for AAP-43's embeddings.
- U3 Inkling files: on the Llama.cpp page (AAP-40) use "Use found files" so `inkling-2-mini` points at the `Inkling-2-Mini-IQ4_NL.gguf` + `mmproj-Inkling-2-Mini-Q8_0.gguf` already in `D:\LlamaCpp\models\ggml-org\Inkling-2-Mini-GGUF\`, or download the Q8_0 + BF16 mmproj; `inkling-2-mini-dspark` needs `unsloth/Inkling-2-Mini-GGUF/Inkling-2-Mini-UD-Q8_K_XL.gguf` (missing; drafter and mmproj are there).
- U4 (optional) Gufo Flash-Next: install `flash-next-q4` with Gufo (`D:\Gufo\models\flash-next-q4` is missing), or tell the planner to drop it from C1.
- U5 For AAP-43: find LM Studio's nomic file (LM Studio > My Models > nomic-embed-text-v1.5 > Show in folder; it is not under `~\.lmstudio\models`: checked) and copy it to `D:\LlamaCpp\models\nomic-ai\nomic-embed-text-v1.5-GGUF\` keeping its file name. The same file is what keeps the index valid.
- U6 Go-ahead at run time for each SVC/GPU check and for stopping the proxy and the apps before L1 to L8.
- U7 Play nothing: this is not a production. Say when a vision move (table above) is wanted.
