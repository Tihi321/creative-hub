# HUB-38 research: how each repo is wired to LLMs (2026-11-21)

## Question

Before planning "every creative-hub app reaches all LLMs, local ones included, only through the ACP proxy (`acp`, http://127.0.0.1:8787/v1)": how is each repo and its data folder wired to LLMs today, and what would have to change?

Method: read seeds, live config and code; one read-only `curl` of `http://127.0.0.1:8787/v1/models` and `/healthz` (the proxy is running now). No service started, no file changed. Keys: none printed. `~` = `C:\Users\Infplane`. "confirmed" = read or run, with path:line; "inferred" = reasoned, said so.

## Answer (short)

- Seven apps call an LLM: Scriptorium, Book Translator, VN Studio, Pixel Studio, Chiptune Studio, Edu Studio, Cartoon Studio. vibe-tts-flow, comfy-mcp, flow-music-mcp call no chat LLM (flow-music-mcp calls Gemini only for TTS audio, `flow-music-mcp/src/flow/gemini.ts:36`).
- All seven share one engine lineage: same provider model (`providers.md` / registry), same ids `lmstudio`, `strata`, `ollama`, `acp`. Almost all of the direct-provider coupling is **config** (provider rows, role lists using the aliases `strata` / `lmstudio`, `fallbacks`, saved per-book/project refs). Code that only works with the direct providers is the LM Studio loader/discovery and the Strata `loaded`-row logic, which can stay dormant.
- `acp` is enabled in 6 of 7 live configs (Cartoon: disabled). The live `acp` base_url is the stale port 7461 in VN Studio, Pixel Studio, Chiptune Studio and Cartoon Studio; Scriptorium, Book Translator and Edu Studio use 8787. The seeds of VN, Pixel, Chiptune and Cartoon still ship 7461 and have no migration to 8787 (Scriptorium and Book Translator have one).
- **Three hard blockers for "only through acp", not config problems** (confirmed from the proxy):
  1. The proxy has **no `/v1/embeddings`** (`api-acp-proxy/src/server.ts:509-513` routes only models, chat/completions, images generations/edits, responses, mcp; `rg embed` finds nothing in README/ROADMAP/src). Scriptorium's RAG embeddings (`lmstudio/text-embedding-nomic-embed-text-v1.5`) cannot move without a proxy change. Only Scriptorium embeds.
  2. A request **with tools** to `gufo/*`, `strata/*`, `llama/*` is answered 400 `model_not_capable` (`api-acp-proxy/README.md:81`). Pixel Studio and Chiptune Studio agents use tool calling on their LM Studio/Strata models today; via acp they must use rows with `tools: false` (JSON-action mode, already how the seeded acp rows are set).
  3. **Vision**: image input reaches only `gufo/flash-next-q4` and `llama/inkling-2-mini*` (`vision:true` in the live `/v1/models`); Strata answers 400 `unsupported_content` (README:161). The art/frame critics and Pixel's vision models today use LM Studio `minicpm-v-4.7-35b-a3b` / `ista-daslab-qwen3.8-27b`.
- The proxy runs **one local server at a time across gufo, strata and llama** and a request for another server stops the running one (README:170), and it never starts a server automatically except the Gufo/Llama auto-switch on a request naming a model (README:139, 159, 170). Model ids differ: proxy lists `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, not `strata/default` (live `/v1/models`).

## Proxy facts used (confirmed)

- Live `GET /v1/models` (2026-11-21): codex/*, antigravity/*, claude/*, `gufo/Qwen3.8-27B`, `gufo/flash-next-q4` (vision), `gufo/deepseek4`, `gufo/qwen-image-2.1(-turbo)` (kind image), `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, `llama/inkling-2-mini`, `llama/inkling-2-mini-dspark` (both vision). `/healthz` 200. No embedding model listed. (Bare aliases like `gpt-6-luna` are also listed, although `services.json` sets `PROXY_LIST_BARE_ALIASES: "0"`: the running instance was not started by hub.ps1 or the setting differs. Inferred.)
- Proxy accepts `response_format` json_schema (README:314) but every app sets `json_schema: false` on `acp`; ids are prefixed (`acp/gufo/flash-next-q4`).
- Proxy default port 8787 (README:72, 94). Strata launcher the proxy uses: `D:\Strata\terminal\run-unsloth-ud-iq4_xs.bat` (README:129); the hub's services.json uses `D:\Strata\run-*.bat`. Different folders (open question).

---

## 1. Scriptorium (`C:\projects\Personal\scriptorium`, data `~\Scriptorium`)

Git: branch master, dirty only by untracked `.claude/tickets/REQ-0004..0010-*` and `plan.md`. Latest ticket SCP-64 (`SCP-64_leftovers`, merged 2026-11-16); style `SCP-NN_slug` branch, `.claude/tickets/SCP-NN-slug/`; also `REQ-00NN` request tickets from the hub. ROADMAP.md:89-96.

**1. LLM use / providers / defaults.** Yes, the biggest user. Live `~\Scriptorium\config\providers.md`: `acp` (enabled: true, 8787, local, json_schema false, discover, concurrency 4; lines 6-33; models codex/gpt-5.6-luna, -terra, gpt-6-luna, antigravity/gemini-3.8-flash, 4-argon, 4-hydrogen with context 45000, claude/claude-sonnet-5), `client`, `deepseek`, `openrouter`, `anthropic`, `gemini`, `lmstudio` (108-143), `strata` (144-173), `ollama` (disabled, 174-182), search providers. Roles (`~\Scriptorium\config\roles.md`): writer-type roles `[paid, strata, lmstudio]`; reviewers `[strata, lmstudio, paid]`; checks/researcher `[strata/default-low, lmstudio, paid]`; archivist `[acp/antigravity/gemini-4-hydrogen, strata/default-low, lmstudio, paid]` (the only acp use); humanizer `[deepseek/deepseek-flash, paid]`. `settings.md`: `fallbacks` = deepseek-flash, strata/default, lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic; `fallback_shared: true`; `lmstudio_parallel 2, context 131072, ttl 28800`. Seed equivalents: `seed/config/providers.md:52-122`, `seed/config/roles.md`. Per-book data: 52 book files carry `role_models`/`no_local_fallback`; saved refs in books include `strata/qwen3.8-flash-next(-low)` (thousands of hits in jobs/books), `lmstudio/nail-qwen3.6-35b-a3b-mtp`, `lmstudio/google/gemma-4-e4b`, `lmstudio/minicpm-v-4.7-35b-a3b` (counts from `grep -rh -o` over `~\Scriptorium\books`). Agent files `~\Scriptorium\agents\*.md`: `model:` empty (one `null`), so no per-agent pins.

**2. Direct-provider references.**
- Code that only works with the provider (confirmed): `src/engine/models/openaiCompat.ts:17-19,124-161,188-198` (LM Studio loader via `lms`/REST, `/api/v0/models` context); `registry.ts:46-47,110-117,220,239,383-385,411,438,480` (load_models, lms path, loaded windows, LM Studio concurrency from `/api/v1/models`); Strata `loaded` rows/profiles/`/status` concurrency (`registry.ts` ~450-480, `openaiCompat.ts:225-241`, `engine.ts:245,280`); migrations `src/engine/store/migrations.ts:513-645` (strata rows, old defaults); `schemas.ts:38-108,287-303` (`load_models`, `load_context`, `lmstudio_*` settings, default `fallbacks` naming strata and lmstudio); `src/engine/cli.ts` + `index.ts:29` `probe` uses LM Studio and embeds one string; `engine.ts:1062-1064,1525-1541` settings commands.
- Config only: provider rows, aliases `strata` / `lmstudio` in roles/settings, `fallbacks`, saved book refs (`strata/qwen3.8-flash-next` resolves by alias to `strata/default`, `registry.ts:603-604`).
- UI: `src/renderer/ui/ModelsDialog.tsx` (12 hits), `Settings.tsx`, `StatusBar.tsx` (server status for Strata/LM Studio), `renderer/demo/*`.
- Tests: 13 files (e.g. `tests/models.test.ts`, `tests/helpers.ts`, `tests/scheduler.test.ts`, `tests/migrations.test.ts`, `tests/customProviders.test.ts`).
- Docs: `CLAUDE.md:15-16`, `AGENTS.md:14`, `README.md`, `docs/design.md`, `docs/mcp.md:100`, `seed/config/providers.md` sections "Strata", "The ACP proxy".
- Special acp logic: `registry.ts` `on_device` (acp is excluded from "runs on this machine" by default, `schemas.ts:89`, seed providers.md `on_device` text) feeding `no_local_fallback`; `engine.ts:325-345` polls the proxy for exhausted providers (`proxyId` prefix check); SCP-62/63 proxy backoff. **Risk**: if local models are served through acp, `on_device` is false for them, so `no_local_fallback` books would treat them as not local (inferred from the rule at `schemas.ts:89`).

**3. Embeddings (confirmed).** `config/roles.md:3` `embeddings: lmstudio/text-embedding-nomic-embed-text-v1.5` (schema `schemas.ts:148-149`). It is its own key, independent of chat roles: `registry.embeddingModel()` (`registry.ts:662-664`) looks the ref up in the model table; `registry.embed()` (`666-684`) calls `client.embedWithPrefix` for ids matching `/nomic/i` (adds `search_document: ` / `search_query: ` prefixes, only when the provider is `local`, `registry.ts:385`) else `client.embed`, which POSTs `<base_url>/embeddings` (`openaiCompat.ts:164-178`). So the embeddings provider can be pointed at any provider/model by one line of roles.md, if that provider has an embedding model in its list (`embedding: true`, live providers.md:141-143). Callers: `memory/service.ts` (available/ready, down-state per provider), `memory/index.ts` (sqlite-vec, `ensureDim` drops and rebuilds the index when the dimension changes, lines 100-111; live index folder `~\Scriptorium\index` 49 MB), `pipeline/handlers.ts:322`, `pipeline/longHandlers.ts:189-200` (chapter indexing waits with `ServerDownError` when embeddings are down), `research/context.ts`, MCP `factory_status` (`mcp/tools.ts:182`). An embedding model other than nomic means a full re-index of all books. The proxy cannot serve it (no `/v1/embeddings`). Work needed on the proxy side, or leave embeddings on LM Studio (or another embeddings server) as a documented exception. Embedding the nomic model also needs LM Studio running: `services.json:147-157` note and ROADMAP.md (hub) line 105 (HUB-34: LM Studio API off stalled a book at embeddings).

**4. Vision / structured output.** Scriptorium sends no images (seed providers.md "It is text only: no vision"; `vision:true` only on `client` models). Structured output: roles send a JSON schema; `json_schema: false` on deepseek, openrouter, strata, acp (not on lmstudio, which therefore gets `response_format` json_schema). Moving the Strata/LM Studio roles to `acp/...` keeps `json_schema: false` (live acp row), i.e. prompt plus repair, same as Strata today. `acp` rows carry `context: 45000` for antigravity only (prompt truncation at ~192,000 chars, REQ-0009).

**5. Starts/expects a local server.** Scriptorium itself starts LM Studio models (`load_models: true`, `lms load`, `registry.ts:110-117`, `openaiCompat.ts:124-161`). It never starts Strata or LM Studio's server. The hub never starts Scriptorium (CLAUDE.md). `hub.ps1 start` default set includes `lmstudio` (`services.json:154`, `startWhenSilent`).

**6. Git/ticket.** See above.

**Work needed: code (embeddings, via proxy or a documented exception) plus config (roles/fallbacks/saved refs, remove or disable lmstudio and strata rows).** A pure-config move of chat roles is possible today.

---

## 2. Book Translator (`book-translator`, data `~\BookTranslator`)

Git: master, clean. Latest ticket BTT-35 (`BTT-35_strict-tool-keys`, merged); style `BTT-NN_slug`, `.claude/tickets/BTT-NN-slug/`.

**1. LLM use.** Yes. Live `~\BookTranslator\config\providers.md`: `client` (enabled), `deepseek` (enabled), openai, openrouter, anthropic, gemini (all disabled), `lmstudio` (lines 102-109, **enabled: false**), `strata` (110-139, no enabled flag so on), `ollama` (disabled), `custom` (disabled, base_url `http://localhost:8080/v1`, lines 149-155), `acp` (enabled: true, 8787, lines 159-167 and models), mock. `defaults.json`: `agentModels` glossary `[strata/default, deepseek/deepseek-v4-flash]`, translator and proofreader `[deepseek/deepseek-v4-flash, strata/default]`, qa `[strata/default, deepseek/deepseek-v4-flash]`; `groupDefaults` paid=deepseek-v4-flash, strata=strata/default; `lmstudio {parallel 4, ...}`. Seed: `seed/config/defaults.json` (glossary/translator/proofreader `[strata/default, deepseek-flash]`, qa adds `strata/default-low` and gemini-2.5-flash last; `fallbacks`), `seed/config/providers.md:89-142` (acp **disabled** in the seed, line 137, 8787).
Saved projects (`~\BookTranslator\projects\*\project.json`, 25 projects): refs seen: `strata/qwen3.8-flash-next` x36 (9 projects), `deepseek/deepseek-v4-flash` x36, `acp/antigravity/gemini-3.8-flash` x12, `-4-argon` x24, `-4-hydrogen` x6, `acp/claude/claude-sonnet-5` x6. No lmstudio refs in projects.

**2. Direct-provider refs.** Code: `src/engine/models/openaiCompat.ts:17-19,124-198`, `registry.ts:43-47,107-112,145-164,282-364,408-545,751-756` (`groupOf` special-cases ids `strata` and `lmstudio` at 756), `config.ts:29` (group aliases), `serve.ts:71`, `cli.ts:103`, `dispatcher.ts:267`, `store/migrate.ts:329-348` (7461->8787 migration, so the old port is fixed here), `schemas.ts`. Config only: defaults.json/providers.md rows. UI: `ModelsDialog.tsx`, `ModelSelect.tsx`, `Settings.tsx`, `NewProject.tsx`. Tests: 9 files (`registry.test.ts`, `router.test.ts`, `openaiCompat.test.ts`, `dataFolder.test.ts`, ...). Docs: `README.md:3,47,61,67-73,95-97` (LM Studio and Strata notes), ROADMAP BTT-24/25.

**3. Embeddings.** None used (only the generic `embed` in `openaiCompat.ts:164` and mock).

**4. Vision/structured output.** JSON for glossary/QA: `json_schema: false` on strata/deepseek/acp. No vision.

**5. Local servers.** Loads LM Studio models only when the provider is enabled (it is off live). Never starts Strata (README:70 tells the user to start it).

**6.** See header.

**Work needed: config only** (defaults.json agentModels/groupDefaults, saved project refs `strata/...`, enable/disable provider rows; the acp row is already on, 8787). Optional code: none required.

---

## 3. VN Studio (`visual-novels-orchestrator`, data `~\VisualNovels`)

Git: master, clean. Latest ticket VNO-66 (`VNO-66_music-variety`); style `VNO-NN_slug`, `.claude/tickets/VNO-NN-slug/` (older ones use a dash after the number). 

**1. LLM use.** Yes. Live `~\VisualNovels\config\providers.md`: client, deepseek, openrouter, anthropic, gemini, `lmstudio` (84-120; models incl. `minicpm-v-4.7-35b-a3b` vision, qwen, gemma), `strata` (121-150), `ollama` (disabled), `acp` (161-168: **enabled: true, base_url `http://127.0.0.1:7461/v1` (stale: the proxy is on 8787)**; models listed, context 1000000 for antigravity). Roles (`config/roles.md`): director, art-director, art-critic `[paid, strata, lmstudio]`; script-analyst, composer, stage-director, voice-director `[strata, lmstudio, paid]`; edition-aligner `[strata/default-low, lmstudio, paid]`. `settings.md`: fallbacks deepseek-flash, strata/default, lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic; `fallback_shared: false`; `scriptoriumData: ~/Scriptorium`. Project data refs (`~\VisualNovels\projects`): `lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic` (~23), `strata/qwen3.8-flash-next` (~16), `lmstudio/minicpm-v-4.7-35b-a3b` (7). Seed `seed/config/providers.md:140-147`: acp **disabled, 7461**; seed doc line 198 says 7461; `README.md:110` says 7461. No 7461->8787 migration (only `providers-acp-v1` which adds the seed row if missing, `src/engine/store/seedMigrations.ts:100-108`).

**2. Direct-provider refs.** Code (provider-specific): LM Studio loader/discovery and Strata loaded rows in `src/engine/models/{openaiCompat,registry,router,types}.ts`, `engine.ts:116,178,220,642-674,823-825`, `summary.ts:83` (local servers panel: Strata and LM Studio), `cli.ts:27` (probe defaults to `lmstudio/gemma-4...` and `deepseek/deepseek-flash`), `store/seedMigrations.ts` (Strata rows), `studios/autostart.ts:20-21,336-338` (never starts Strata; does not start ComfyUI while Strata answers on 8080, via `services.json` entry `strata`). `scripts/prod-status.mjs`, `scripts/prod-watch.mjs` match the grep (not read; inferred model/status helpers). UI `ModelsPage.tsx`, `renderer/store/store.ts`. Tests: 10 files (`models.test.ts`, `scheduler.test.ts`, `autostart.test.ts`, `seed-migrations.test.ts`, ...). Docs: README, docs/mcp-guide.md, docs/protocol.md, repositories.md, ROADMAP.

**3. Embeddings.** None.

**4. Vision / structured output.** The `art-critic` role needs a `vision: true` model (seed roles.md text; providers.md:99 lmstudio minicpm, plus anthropic/gemini/openrouter vision rows, `client` with `vision: true`). Its list is `[paid, strata, lmstudio]`; the paid default deepseek has no vision, so in practice the vision filter picks LM Studio minicpm or a cloud vision row (inferred from the filter rule in seed text). Through acp only `gufo/flash-next-q4`, `llama/inkling-2-mini*` and cloud models take images; the acp rows in the live config have no `vision: true` (providers.md 161-195), so the art-critic would skip acp today. `json_schema: false` on strata/deepseek/acp.

**5. Starts a server.** Autostart reads `C:\projects\Personal\creative-hub\services.json` (`~\VisualNovels\config\autostart.md`) to start pixel-studio, chiptune-studio, comfyui. It never starts LM Studio/Strata/Scriptorium. Touches `services.json` ids `strata` and `lmstudio` only for the ComfyUI-vs-Strata GPU check.

**6.** See header.

**Work needed: config only** (fix the acp port 7461 -> 8787, add `vision: true` to the proxy's vision models, retarget roles/fallbacks/project refs). Code only if the Strata-answering check in autostart should look at the proxy's Strata instead of 8080 (inferred: the Strata process still listens on 8080 when the proxy starts it, so the check likely still works).

---

## 4. Pixel Studio (`pixel-art-generator`, data `~\PixelStudio`)

Git: master, clean. Latest ticket PAR-18 (`PAR-18_strata-iq3s-removal`); style `PAR-NN_slug`.

**1. LLM use.** Yes: one chat agent `artist` plus `palette`. Live `~\PixelStudio\config\roles.md`: aliases `lmstudio: lmstudio/ista-daslab-qwen3.8-27b-gsq-rco-unsloth-mtp`, `strata: strata/default`, `cloud: deepseek/deepseek-flash`, `claude: anthropic/claude-sonnet-5-5`; roles `artist: [lmstudio]`, `palette: [lmstudio]` (so LM Studio is the only default, no fallback). `config/app.json`: `selectedModel: strata/default`. Live `providers.md`: lmstudio (10-37, `load_models`, qwen rows with `tools: true`, `vision: true` on ista-daslab and gemma-4-e4b), strata (38-66, tools true), deepseek, openrouter, **acp (115-149, enabled: true, base_url 7461, all models `tools: false`)**, ollama (disabled), openai, anthropic, gemini, mock; `lmstudio_parallel 1, context 131072, ttl 60` at the top. `models.md` `shown:` includes acp/antigravity/gemini-3.8-flash, acp/codex/gpt-6-luna, lmstudio models, strata/default. Seed: `seed/config/providers.md:127` acp at 7461; ROADMAP.md:27,34 (PAR-14/15).

**2. Direct-provider refs.** Code: `src/llm/openaiCompat.ts:17-310` (LM Studio load/unload via lms/REST, `/api/v0/models` capabilities), `registry.ts` (load, discovery filtering embeddings/draft, Strata rows, `lmstudio_*`, app-level context override line 157/575), `config.ts:26-89`, `seedMigration.ts:14,147-160` (LEGACY_SEED_PROVIDERS, strata rename), `customProviders.ts:12` (reserved ids), `modelChoices.ts`, `main/appSettings.ts`, `main/llm.ts`, `shared/agent.ts`, UI `SettingsDialog.tsx`, `renderer/state/chat.ts`. Tests: 7 files (`tests/llm/*`, `tests/main/agentLlm.test.ts`, and acp 7461 in `customProviders.test.ts`). Docs: ROADMAP; seed providers.md.

**3. Embeddings.** None (`registry.ts:569` comment: "there are no embedding models").

**4. Vision / structured output / tools.** The `artist` agent uses **tool calling** for models with `tools: true`, JSON-action mode otherwise (roles.md text; `shared/agent.ts`). The router only falls back to models with the same tool and vision support as the first (roles.md). The live default is LM Studio qwen with `tools: true`: through the proxy `gufo/*`/`strata/*`/`llama/*` with tools are 400 (README:81), so the agent would have to run in JSON-action mode (`tools: false`). Vision: LM Studio rows `vision: true` for image input in chat; via proxy only `acp/gufo/flash-next-q4` or `acp/llama/inkling-2-mini`.

**5. Local servers.** Loads LM Studio models itself. Starts nothing else.

**6.** See header.

**Work needed: config + possibly code.** Config: acp port, role lists (`artist`, `palette`), `selectedModel`, add `acp/gufo/*` rows with `tools: false`, `vision: true` where the proxy has it. Code: only if an agent should keep native tool calls on local models (proxy refuses tools) — not needed if JSON-action mode is acceptable (behaviour change: quality/speed unverified).

---

## 5. Chiptune Studio (`midi-generator`, data `~\ChiptuneStudio`)

Git: master, clean. Latest ticket MDI-17 (`MDI-17_yarnrc-trim`); style `MDI-NN_slug`.

Wired the same as Pixel Studio (same `src/llm/*` lineage). Live `~\ChiptuneStudio\config\roles.md`: aliases lmstudio (`ista-daslab-qwen3.8-27b...`), strata (`strata/default`), cloud, claude; roles `composer: [lmstudio]`, `theory: [lmstudio]`; `app.json` `selectedModel: strata/default`. Live `providers.md` has lmstudio (10-37), strata (38-66), acp (115-149, **enabled: true, 7461**, `tools: false` rows), ollama disabled, others. `models.md` shown: acp/antigravity/gemini-3.8-flash, acp/codex/gpt-6-luna, lmstudio models, strata/default(-low). Seed `seed/config/providers.md:119` acp 7461, ROADMAP.md:16,20. Direct refs in code: `src/llm/{openaiCompat,registry,config,seedMigrate,setup,modelChoices,customProviders}.ts`, `main/{appSettings,llm}.ts`, `shared/agent.ts`, `renderer/state/chat.ts`, `SettingsDialog.tsx`; tests 9 files incl. `tests/e2e/acp-live.spec.ts` (hardcodes proxy 7461, gated by `ACP_LIVE=1`). No embeddings. Tools: `composer` agent uses tool calling (roles.md); same proxy restriction as Pixel (no tools on local models). Vision: not needed for composer/theory (inferred from role text).

**Work needed: config + possibly code**, as Pixel Studio (port, roles/selectedModel, `tools: false` rows; test/doc port 7461 strings).

---

## 6. Edu Studio (`edu-game-studio`, data `~\EduGames`)

Git: master, clean. Latest ticket EGS-70 (`EGS-70_music-variety`); style `EGS-NN_slug`; `.claude/tickets/EGS-NN-slug/`.

**1. LLM use.** Yes (about 22 roles). Live `~\EduGames\config\roles.md`: most roles `[paid, strata, lmstudio]`; researcher, fact-checker `[strata/default-low, lmstudio, paid]`; accessibility-reviewer, child-safety-reviewer, playtester `[strata, lmstudio, paid]`; `art-critic: [gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, lmstudio]`. Course-level and agent-level model overrides come first (roles.md text: course, then agent, then list); the courses/agents folders hold no explicit lmstudio/strata/acp refs (grep found none). Live `settings.md`: fallbacks deepseek-flash, strata/default, `lmstudio/gemma-4-e4b-it`; `fallback_shared: false`. Live `providers.md`: deepseek, openrouter, anthropic, gemini, lmstudio (72-103), strata (104-129), ollama (disabled), **acp (144-151, enabled: true, base_url 8787)**, client, search. Seed acp is **8787** (`seed/config/providers.md:144`, EGS-68).

**2. Direct-provider refs.** Code: same engine files as VN Studio (`src/engine/models/*`, `engine.ts`, `store/seedMigrations.ts`, `summary.ts`), plus **`registry.ts:615-645` (`localFallbackRefs`, EGS-68): for a role naming Strata or LM Studio (providers that are `local` and not client/mock/acp), the engine inserts `acp` then an OpenRouter free model right after them** (commit e5de41e). `studios/autostart.ts:20-21,336-338` same Strata/ComfyUI GPU check. `src/engine/index.ts:29` probe text. Tests: 9 files (`tests/models.test.ts`, `roles-config.test.ts`, ...). Docs: README, docs/protocol.md, docs/mcp-guide.md, docs/player.md.

**3. Embeddings.** None; research notes are ranked by shared words (`src/engine/research/notes.ts:83,236`).

**4. Vision / structured output.** `art-critic` needs `vision: true`: its list is gemini-2.5-flash, claude-sonnet-4-5, then lmstudio (vision filter). Edu images go through `json_schema: false` providers except lmstudio.

**5. Local servers.** Autostart (ComfyUI, Pixel, Chiptune) via `registry: ../creative-hub/services.json` (relative path, `~\EduGames\config\autostart.md`). Never starts Strata/LM Studio.

**Work needed: config only** (roles/fallbacks), and optionally code: `localFallbackRefs` already prefers acp after local servers; if the local providers are removed, that logic is inert (inferred).

---

## 7. Cartoon Studio (`cartoon-studio`, data `~\CartoonStudio`)

Git: master, clean. Latest ticket CTS-53 (`CTS-53_renderer-default-docs`); style `CTS-NN_slug` (some merges as `CTS-NN: ...`).

**1. LLM use.** Yes, but by default through Claude Code as the model: every role in live and seed `roles.md` is `[client/claude-code, strata, lmstudio]` ("No role names a paid model"). `settings.md`: fallbacks `client/claude-code`, `strata/default`, `lmstudio/gemma-4-e4b-it`. Live `providers.md`: lmstudio (72), strata (104), ollama, **acp (140-147, enabled: false, base_url 7461)**, client. Seed acp: 7461 (`seed/config/providers.md:144`). UI placeholder text `http://127.0.0.1:7461/v1` hardcoded in `src/renderer/ui/ModelsPage.tsx:84,309` and `src/engine/models/customProviders.ts:48`. Cartoon has no `seedMigrations.ts` (no `providers-acp-v1` equivalent found; `rg` for acp in src shows only protocol/schemas/customProviders/registry). Inferred: an existing data folder does not get new seed rows automatically.

**2. Direct-provider refs.** Same engine files as VN/Edu (`src/engine/models/*`, `engine.ts`, `summary.ts`, `autostart.ts:20-21,336-338`), UI `ModelsPage.tsx`. Tests: 2 files (`tests/seed.test.ts`, one more). Docs: README, docs/provenance.md.

**3. Embeddings.** None.

**4. Vision.** `frame-critic` needs a model that takes images (seed roles text, providers.md:80-83, `client` models `vision: true`). Currently `client/claude-code` first, then Strata/LM Studio (no vision rows listed unless added).

**5. Local servers.** Autostart: ComfyUI only (`~\CartoonStudio\config\autostart.md`), registry `../creative-hub/services.json`.

**Work needed: config only** (enable acp at 8787, role lists after `client/claude-code`), seed change for port (7461 -> 8787).

---

## 8. vibe-tts-flow, comfy-mcp, flow-music-mcp (no chat LLM)

- `vibe-tts-flow`: no LLM provider. `higgs.py` `llm_decoder` is the on-device TTS model, not an API. Git master, clean; latest ticket VTF-09; style `VTF-NN_slug` branch (some commits `NO-TASK:`).
- `comfy-mcp`: no LLM. `src/mcp/tools.ts:185` only mentions "an LLM server" in the `free_memory` description (frees VRAM for it). Git master, clean; latest CMC-08 (`CMC-08_local-patches`).
- `flow-music-mcp`: Gemini used only for TTS (`src/flow/gemini.ts:36` `generateContent`; engine `gemini`/`elevenlabs` in `local-tools.ts:108`). Not an OpenAI chat path, so it cannot go through the proxy as is (inferred: the proxy has no audio endpoint, `server.ts:509-513`). Git master, clean; latest FMM-21 (`FMM-21_eleven-retries`).
- None of the three needs work for HUB-38.

## 9. The hub (`creative-hub`)

Git: master, clean. Latest ticket HUB-38 (this one; HUB-37 was `HUB-37_hub-leftovers`); style `HUB-NN_slug`, `.claude/tickets/HUB-NN-slug/`.

- `services.json:146-158` `lmstudio`: port 1234, `http: .../v1/models`, `startWhenSilent: true`, `default: true`, start `lms.exe server start`, note "used by Scriptorium (RAG needs nomic-embed-text-v1.5), Book Translator and VN Studio". `services.json:159-172` `strata`: 8080 `/health`, `default: false`, variants (iq4_xs-parallel default, iq4_xs, deepseek, deepseek-coder) from `D:\Strata\run-*.bat`. `services.json:173-189` `acp-proxy`: 8787 `/healthz`, `default: false`, `managed: true`, node `dist/index.js` with env (PROXY_LIST_BARE_ALIASES 0, TIMEOUT 900000, concurrency 4/4/3/2). Its note says acp serves "all five apps" and mentions "flow-mcp's panel also used 8787 and is retired".
- `scripts/hub.ps1`: `start` default set includes lmstudio (README.md:59); `start strata <variant>` via `variants` (hub.ps1:7-9,43,328-345); `startWhenSilent` handling (hub.ps1:328-337, HUB-34). Status checks the Strata `/health` model/loaded (hub.ps1:180-183). `scripts/strata-probe.mjs` probes Strata at 8080 directly (HUB-26 tool).
- `README.md:25,44,45,59,65,76` mention LM Studio/Strata (service table, default set, VN autostart "never starts ... Strata, LM Studio"). `ROADMAP.md:32` (HUB-26 Strata), `:105` (HUB-34 LM Studio embeddings stall). `CLAUDE.md:3`, `AGENTS.md:3` list LM Studio and Strata among the tools. Skills: `make-visual-novel/SKILL.md:12,16,18,162,163` (LM Studio / Strata choices, "Start LM Studio or Strata"), `make-cartoon/SKILL.md:14` (a line matching the grep). `make-video` and `make-edu-game` do not mention them. `.mcp.json` has no LLM entries (all MCP servers of tools; the acp proxy is not listed; I read the first 40 lines only).
- Hub tickets with earlier work: `HUB-09-acp-proxy-wiring`, `HUB-26-strata-model-discovery`, `strata-model-audit`, `external-llm-jobs`.

---

## Summary table

| repo | uses LLM | acp enabled (live) | direct local providers still referenced | embeddings | work needed |
|---|---|---|---|---|---|
| scriptorium | yes (17 roles) | yes, 8787; only archivist uses it | lmstudio + strata in every role, fallbacks, ~50 books, jobs; lmstudio loader code | **yes**: nomic via LM Studio (`roles.md:3`); proxy has no `/v1/embeddings` | **code** (proxy embeddings or exception) + config |
| book-translator | yes (4 agents) | yes, 8787 (seed: off) | strata first in glossary/qa (live), 9 projects `strata/...`; lmstudio provider off | none | config only |
| visual-novels-orchestrator | yes (8 roles) | yes but **port 7461 (stale)** | lmstudio + strata in all roles, fallbacks, project refs; lmstudio vision model for art-critic | none | config only (+ port fix in seed; vision rows for acp) |
| pixel-art-generator | yes (artist, palette) | yes but **port 7461** | lmstudio is the only default (`artist`, `palette`); `selectedModel strata/default`; tool calling on local models | none | config + maybe code (proxy refuses tools for local models; JSON-action mode) |
| midi-generator | yes (composer, theory) | yes but **port 7461** | same as Pixel | none | config + maybe code (same) |
| edu-game-studio | yes (about 22 roles) | yes, 8787 | lmstudio + strata in every role/fallbacks; `localFallbackRefs` puts acp after them | none | config only |
| cartoon-studio | yes (8 roles, client first) | **no** (enabled: false), port 7461 | strata + lmstudio as fallbacks after `client/claude-code` | none | config only (+ seed port) |
| vibe-tts-flow | no | n/a | none | no | none |
| comfy-mcp | no | n/a | none | no | none |
| flow-music-mcp | Gemini TTS only | n/a | none | no | none |
| creative-hub | no (registry, docs, skills) | `acp-proxy` service entry exists, 8787, not in default set | `lmstudio` (default set, startWhenSilent), `strata` (variants), README, skills, strata-probe | no | config/docs: services.json, README, skills; optional `default`/variants changes |

## What the plan will need (options, not decisions)

1. Proxy gaps (api-acp-proxy repo, ticket style `AAP-NN_slug`, latest AAP-39): `/v1/embeddings` for the nomic model (Scriptorium only); tools on local models (Pixel/Chiptune) or accept JSON-action mode; `strata/default`-style stable refs or a client-side alias mapping (the apps' `loaded` rows assume one stable ref); vision flags in `/v1/models` (already there: `vision` field), which the apps' discovery must read (inferred: `openaiCompat.ts` `listModelInfo` reads capabilities, not verified for the `vision` field of the proxy).
2. Per-app config migration is the same four edits everywhere: fix/enable `acp` (8787), add or discover the `gufo/*`, `strata/*`, `llama/*` rows (with `tools:false`/`vision` flags), rewrite role lists and `fallbacks` that use the `strata`/`lmstudio` aliases, and rewrite saved per-book/project/job refs (Scriptorium books, Book Translator projects, VN Studio projects).
3. Deciding whether to delete or only disable the `lmstudio`/`strata` rows (disable is safe: `enabled:false` is supported, Book Translator already has lmstudio off live; delete may be re-added by seed migrations in VN/Edu (`providers-acp-v1` adds only `acp`, inferred not re-adding others) and by Pixel/Chiptune `seed-state.json` which records offered providers).
4. Seeds and migrations: change seed `acp` port 7461 -> 8787 in VN, Pixel, Chiptune, Cartoon and docs (`visual-novels-orchestrator/README.md:110`, seed providers.md:198, `pixel-art-generator/seed/config/providers.md:127,238`, `midi-generator/seed/config/providers.md:119,223`, Cartoon seed 144 + `ModelsPage.tsx:84,309` + `customProviders.ts:48`), tests and e2e specs that hardcode 7461 (`midi-generator/tests/e2e/acp-live.spec.ts`, `pixel-art-generator/tests/e2e/acp-live.spec.ts`), plus an 7461->8787 migration like Scriptorium `migrations.ts:403-422` and Book Translator `migrate.ts:329-348`.
5. Hub: `services.json` (lmstudio `default: true`, strata variants and how `hub.ps1 start strata` relates to the proxy-managed Strata `D:\Strata\terminal\...`), README rows, skill text, `strata-probe.mjs`, the ComfyUI-vs-Strata GPU check in VN/Edu/Cartoon autostart (still valid if Strata keeps port 8080).
6. Tests per repo to adjust: Scriptorium 13 files, BTT 9, VN 10, Pixel 7, Chiptune 9, Edu 9, Cartoon 2 (mostly mock providers named lmstudio/strata; many need no change if the provider code stays).

## Risks

- Embeddings (Scriptorium) and tool calling (Pixel, Chiptune) cannot be moved to the proxy without proxy changes or a behaviour change; a nomic switch re-indexes the whole library (`memory/index.ts:105`).
- The proxy runs one local server at a time and a switch can take many minutes (README:159, 170); apps that fire parallel requests to different local models (Scriptorium reviewers, checks) would queue (`switchWaitMs` 30 min, then 503 `local_model_busy`). Concurrency `auto` from Strata's `/status` is lost; acp is a fixed `concurrency: 4`.
- `on_device` / `no_local_fallback` semantics in Scriptorium break for local models served by acp (acp is treated as not on this machine).
- Per-book and per-project refs and job history hold `strata/qwen3.8-flash-next(-low)` and `lmstudio/...` (thousands of rows); roles that fail to resolve are skipped with a log once (settings.md text).
- Stale 7461 ports in live VN/Pixel/Chiptune/Cartoon configs mean the "acp enabled" there is probably not working today (inferred: the proxy answers on 8787, I did not probe 7461).
- Proxy refuses tools/MCP/web search on local models (`model_not_capable`) and image input to Strata (400).
- Terms risk for Antigravity through ACP is documented (Scriptorium seed providers.md, hub ROADMAP "Antigravity models and the ACP proxy") — relevant only for cloud models, not for the local ones.

## Open questions

1. Proxy embeddings: add `/v1/embeddings` (route to LM Studio, or a gufo/llama embeddings profile) or keep Scriptorium's embeddings on LM Studio as the one direct exception? Does the user want LM Studio kept at all (it also holds the nomic model and the vision models)?
2. Is `strata/default` (a stable ref that follows the loaded model) needed through the proxy, or do apps use the exact id (`strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`) / the `gufo/...` ids? Roles and saved refs assume the stable ref (HUB-26).
3. Pixel/Chiptune agents: accept JSON-action mode (no tools) for local models through acp?
4. Vision: which model should be the art-critic/frame-critic/Pixel vision default through the proxy (`acp/gufo/flash-next-q4`, `acp/llama/inkling-2-mini`)? Do the apps' discovery code read the proxy's `vision` field (not verified; I read `seed` text and the registry filter only)?
5. Which proxy Strata launcher is correct (`D:\Strata\terminal\run-unsloth-ud-iq4_xs.bat` in proxy README:129 vs `D:\Strata\run-*.bat` in `services.json`)? Should `hub.ps1 start strata` keep existing, now that the proxy starts local servers on request?
6. Is the running proxy started by hub.ps1 (env `PROXY_LIST_BARE_ALIASES=0`) or from its app? The live list shows bare aliases.
7. Should `lmstudio`/`strata` rows be removed or kept disabled (`enabled: false`)? Does the VN/Edu `providers-acp-v1` or another seed migration re-add removed providers in existing data folders (I read only the acp one)? Cartoon has no seed migration at all (inferred).
8. Cartoon Studio: keep `client/claude-code` first and only change the local fallbacks, or also enable acp (`enabled: false` today)?
9. `visual-novels-orchestrator/scripts/prod-status.mjs` and `prod-watch.mjs` matched the grep (strata/lmstudio/8080 terms); not read.
10. The hub `.mcp.json` below line 40 and `strata-model-audit`, `external-llm-jobs` hub tickets not read.
11. Edu ROADMAP/EGS-68 `localFallbackRefs` and the proxy's local models: acp is inserted only "when it is on and lists a model" (`registry.ts:638`): confirm behaviour when strata/lmstudio are removed (inferred inert).
12. The proxy's Gufo flash-next vision profile and Strata exist; untested: a real run of any app against `gufo/*` or `strata/*` through the proxy (not run, only the model list was read).
