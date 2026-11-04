# HUB-26 Strata model discovery: tools follow whichever model Strata runs

Status: plan, not started. Written 2026-11-04 from the audit in `.claude/tickets/strata-model-audit/research-{A,B,C}.md` and a re-read of the code (line numbers below were checked on `master` of every repo on 2026-11-04).

Reading used: the requests in this plan are the full reading (discovery, per-model settings, `hub.ps1` variants, config gaps, user-data migration), in all six tool repos plus the hub. It is not a docs-only relabel.

## Scope

1. The six tools ask Strata which model it runs and show the real name, while roles, settings and app files name only a neutral ref (`strata/default`, `strata/default-low`) that survives a model switch. One shared contract (C1 below).
2. Per-model settings for Strata, kept by model id (prefix match), for Qwen and DeepSeek: `family`, `context`, `json_schema`, `extra_body`, plus `tools`/`vision` in Pixel/Chiptune.
3. `hub.ps1 start strata <variant>` picks the `D:\Strata\run-*.bat`; `services.json` records the variants; `hub.ps1 status` shows the loaded model.
4. Config gaps: Scriptorium user `settings.md` has no Strata fallback row (verified: `~\Scriptorium\config\settings.md:9-11` lists only `deepseek/deepseek-flash` and `lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic`, so the `strata` alias in `~\Scriptorium\config\roles.md:8-57` resolves to nothing); Book Translator user `providers.md:115` has `concurrency: 1` (seed: `auto`); stale Strata docs in every seed `providers.md` (dead `run-iq2_xs.bat` / `run-coder-iq1_m.bat`, 84 GB advice, "Qwen3.8-Flash-Next server"); the same wording in `creative-hub/README.md:44` and `services.json:146`.
5. One seed migration per repo that moves the user's data copy onto the contract; the old refs keep working through aliases, so history and project files need no rewrite.
6. A probe script and live checks against the Qwen and the DeepSeek Strata (the user starts Strata).

## Out of scope

- Strata itself (`D:\Strata`): no change to `server.py`, configs or `.bat` files. Multi-model Strata (Expert mode) is not supported.
- Sending the real model id as the request's `model`: the wire id stays the row id (`default`, `default-low`). Strata answers any name with the loaded model (`D:\Strata\serve\server.py:4815-4819` `model_for`), so this is cosmetic and would touch every call site.
- Correcting a request's family from the response's `model` field (the one-request window after a switch, see C1 rule 8).
- Rewriting history and per-project data: `~\Scriptorium\books\*\book.md` usage counts, `~\VisualNovels\jobs\done\*`, `~\BookTranslator\projects\*\project.json` (48 files) keep `strata/qwen3.8-flash-next`; the legacy aliases (C1 rule 6) resolve them.
- The old one-time migrations that still write the legacy ref (`scriptorium/src/engine/store/migrations.ts:497`, `visual-novels-orchestrator` and `edu-game-studio` `src/engine/store/seedMigrations.ts:100,118`). They run before the new migration, which then renames the ref.
- `C:\projects\Personal\new-noddy` (it has the same stale Strata seed section at `seed/config/providers.md:118-124`, and is not one of the six tools). Candidate for a later replay.
- VRAM measurement of the DeepSeek packs, LM Studio, ComfyUI guard logic (`autostart.ts:336-340` keys on the service id and stays right for any model).
- Assigning Strata to new roles in Pixel Studio / Chiptune Studio (their roles use `[lmstudio]` and stay so).

## C1. The shared contract (written once; every task references it)

### C1.1 providers.md shape (every repo's seed; Pixel/Chiptune add `tools: true` on the rows)

```yaml
  - id: strata
    kind: openai-compat
    local: true
    base_url: http://127.0.0.1:8080/v1
    api_key_env: STRATA_API_KEY   # optional: only sent if set
    concurrency: auto             # as many as the running Strata serves (its /v1/status)
    discover: true                # ask Strata which model it runs (GET /v1/models, and `model` of /v1/status)
    json_schema: false
    models:                       # the refs roles and settings use; each stands for whatever model Strata has loaded
      - id: default               # thinking off
        loaded: true
        aliases: [qwen3.8-flash-next]
        context: 131072           # used until Strata has answered once
        extra_body: { reasoning_effort: none }
      - id: default-low           # thinking on low, for the checks
        loaded: true
        aliases: [qwen3.8-flash-next-low]
        context: 131072
        extra_body: { reasoning_effort: low }
    profiles:                     # settings per model Strata may run, matched by id prefix; not refs, not in pickers
      - id: qwen3.8-flash-next    # matches qwen3.8-flash-next-iq3_s and qwen3.8-flash-next-unsloth-ud-iq4_xs
        family: qwen
        context: 131072
      - id: deepseek-v4.1-flash
        family: deepseek
        context: 131072
```

New schema fields (each repo's providers schema: `scriptorium`/`book-translator`/`visual-novels-orchestrator`/`edu-game-studio` `src/shared/schemas.ts` `providerModelSchema` (~:25-43) and `providerEntrySchema` (~:35-81); `pixel-art-generator`/`midi-generator` `src/llm/config.ts` (~:20-52)):
- model row: `loaded: boolean` (default false), `aliases: string[]` (default []).
- provider: `profiles: [{ id, family?, context?, max_output?, json_schema?, extra_body?, tools?, vision? }]` (default []).
- model row and profile: `json_schema?: boolean` (overrides the provider's for that model).

### C1.2 Resolution rules

1. **Loaded id L.** Per provider that has at least one `loaded: true` row: L is `model` of `GET <base_url>/status` (the call `syncServerSlots` already makes; Strata returns `"model": svc.model` there, `server.py:5443`), and at discovery the first entry of `GET <base_url>/models` without `alias_of` (`server.py:7777-7787`). The registry keeps L per provider id across config reloads (like `serverSlots`), in memory only. An empty `data` list (model unloaded, `server.py:7786`) or no answer leaves L as it was.
2. **Profile K** for L: the profile whose `id` equals L (case-insensitive), else the longest profile `id` that L starts with; else none.
3. **Each `loaded` row V** (`strata/default`, `strata/default-low`) becomes, once L is known:
   - `servedId = L` (new optional field on `ModelInfo`);
   - `family = K.family ?? guessFamily(L)` (existing `guessFamily`, `scriptorium/src/engine/models/registry.ts:592`; `deepseek` and `qwen` are in every repo's list);
   - `context = K.context ?? <n_ctx from /v1/models meta.n_ctx> ?? V.context`;
   - `jsonSchema = V.json_schema ?? K.json_schema ?? provider json_schema`;
   - `extraBody = { ...K.extra_body, ...V.extra_body }` (the variant's thinking level wins over the profile);
   - Pixel/Chiptune also `tools = K.tools ?? V.tools`, `vision = K.vision ?? V.vision`.
   With L unknown (Strata has not answered since the app started): `servedId` undefined, the row's own `family` (default `unknown`), `context`, `extra_body`.
4. **The `-low` variant** is only a second `loaded` row with another `extra_body`; it follows L exactly like `default`. No other variants are built in; a user may add more `loaded` rows.
5. **Aliases in the engine repos** (Scriptorium, Book Translator, VN Studio, Edu Studio): the existing kind alias `strata` = the first `strata/...` row of `fallbacks` (`registry.ts` `aliasMap`, Scriptorium :460-472) now finds `strata/default`. Roles that want thinking on low name `strata/default-low`. Pixel/Chiptune: `roles.md` `aliases.strata: strata/default`, plus `strata-low: strata/default-low`.
6. **Legacy refs.** `getModel(ref)` and `resolve(ref)` map `strata/<alias>` to its `loaded` row through the row's `aliases` (`strata/qwen3.8-flash-next` -> `strata/default`, `strata/qwen3.8-flash-next-low` -> `strata/default-low`). Aliases are not listed as models (no duplicates in pickers).
7. **Discovery on a `loaded` provider adds no models**: it only sets L (and n_ctx). The Models dialog's per-provider list (`listProviderModels`, Scriptorium `registry.ts:276`) shows the `loaded` rows with L. A `picked` entry in `models.md` for that provider is skipped at load. Pixel/Chiptune: `dropMissing` (`pixel-art-generator/src/llm/registry.ts:254-258`) never drops a `loaded` row.
8. **Model switch.** When a status check returns another L, the registry re-applies rule 3 to the `loaded` rows in place (the `ModelInfo` objects stay the same, so the router's lists and `r.model.family` at `scriptorium/src/engine/pipeline/handlers.ts:903` see the new values), returns it in the result of `syncServerSlots` (new `served` changes list next to the slot changes) and the engine logs `models: strata now serves <L> (was <old>)` and sends its models-changed event to the UI. A request that started in the window before the next check keeps the old family label (accepted).
9. **Strata down.** Unchanged from today: `concurrency: auto` marks it `down` when `/status` does not answer or says `loaded: false` without `auto_load` (`registry.ts:392-441`), and jobs skip it while another model is left. L and the derived settings stay (shown as "last seen"); the UI shows `Strata: not running (last: <L>)` or `Strata: not running` when L was never seen.
10. **Display.** Every model summary sent to the UI and to MCP gets `served?: string` (Scriptorium `src/engine/summary.ts:150-165`, BT `src/engine/dispatcher.ts:185-200`, VN/Edu `src/engine/summary.ts`, Pixel/Chiptune `src/main/llm.ts` overview). Pickers show `Strata: <L>` and `Strata: <L>, thinking low`; usage/cost rows keep the ref (`strata/default`) and add `served` where the repo writes a per-call row.
11. **json_schema per model**: the router passes `jsonSchema: model.jsonSchema` in the chat request (`router.ts` call: Scriptorium :185-193, VN/Edu :177-185, Pixel/Chiptune :118-128); `openaiCompat.ts` uses `req.jsonSchema ?? this.opts.jsonSchema` (Scriptorium/BT/VN/Edu :74, Pixel/Chiptune :141).

### C1.3 Neutral refs everywhere

The seed `roles.md`, `settings.md` `fallbacks`, BT `defaults.json`, Pixel/Chiptune `roles.md`/`models.md`, and the code defaults name only `strata/default` / `strata/default-low` / the `strata` alias:
- `scriptorium/src/shared/schemas.ts:260`, `book-translator/src/shared/schemas.ts:115`, `book-translator/src/engine/dispatcher.ts:588`, `book-translator/src/engine/models/registry.ts:135,527`, `visual-novels-orchestrator/src/shared/schemas.ts:137,144`, `edu-game-studio/src/shared/schemas.ts:202,209`.

### C1.4 Migration contract (same rule in every repo, in that repo's own migration mechanism)

Migration id `strata-loaded-v1` (Scriptorium and BT: a `migrateStrataLoaded` function, they have no id list). Runs once; never re-adds what the user removed.
- `config/providers.md`, provider `strata`: if it has no `loaded` row, add the two seed `loaded` rows (with their `aliases`) and the seed `profiles`, set `discover: true`; remove a model row whose id is now an alias (`qwen3.8-flash-next`, `qwen3.8-flash-next-low`), keep every other row and every other key. If the user deleted the `strata` provider, do nothing. BT only: a numeric `concurrency` on `strata` becomes `auto` (requested, see Scope 4).
- Ref rename, exact strings only: `strata/qwen3.8-flash-next-low` -> `strata/default-low`, `strata/qwen3.8-flash-next` -> `strata/default`, in `config/roles.md`, `config/settings.md` `fallbacks` (and `last_resort_model`), BT `config/defaults.json` (`agentModels`, `fallbacks`, `groupDefaults`), Pixel/Chiptune `config/roles.md` aliases, `config/models.md` `shown`, `config/app.json` `selectedModel`.
- A file that is missing or does not parse is skipped and not recorded (existing rule, VN `seedMigrations.ts:10-14`).

## Files and modules per repo

The model layer exists in two copies, measured with `diff --strip-trailing-cr` of `registry.ts`:
- **engine family** `src/engine/models/{registry,router,openaiCompat}.ts`, `src/shared/schemas.ts`: `visual-novels-orchestrator` vs `edu-game-studio` 17 lines differ; `scriptorium` vs `visual-novels-orchestrator` 116; `scriptorium` vs `book-translator` 365 (BT has `defaults.json` groups and its own `dispatcher.ts`). `openaiCompat.ts` Scriptorium vs BT: 4 lines.
- **llm family** `src/llm/{registry,router,openaiCompat,config}.ts`: `pixel-art-generator` vs `midi-generator` 39 lines. Engine vs llm: 708 lines (different discovery: `installed`/`dropMissing`, `source`, `shown`, `tools`/`vision`).
- Migrations differ per repo: VN/Edu `src/engine/store/seedMigrations.ts` (`SEED_MIGRATIONS` list with ids, `applySeedMigrations` :173, called from `dataFolder.ts:121`); Scriptorium `src/engine/store/migrations.ts` functions called from `dataFolder.ts:110-120`; BT `src/engine/store/migrate.ts` (`migrateProviders` :109, called from `dataFolder.ts:85`); Pixel `src/llm/seedMigration.ts`, Chiptune `src/llm/seedMigrate.ts` (161 diff lines between them), called from `src/llm/setup.ts:26`.

| repo | ticket | branch | code | seed | tests to extend (one test per behaviour) |
|---|---|---|---|---|---|
| visual-novels-orchestrator (VN Studio) | VNO-60 | `VNO-60_strata-model-discovery` | `src/shared/schemas.ts` (:39-76 schema, :137,144 defaults); `src/engine/models/registry.ts` (load :159-245, discover :350-395, syncServerSlots :396-445, aliasMap/resolve, getModel); `src/engine/models/router.ts:177-185`; `src/engine/models/openaiCompat.ts:74` and `listedModel` (read `meta.n_ctx`); `src/engine/summary.ts`; `src/engine/engine.ts:211` (log + event on served change); `src/renderer/ui/ModelsPage.tsx:390-411` (label); `src/engine/store/seedMigrations.ts` (new entry) | `seed/config/providers.md:104-119` block, :196-206 docs; `seed/config/roles.md:17`; `seed/config/settings.md:5` | `tests/models.test.ts:119` (status/down test: add the served model and a switch); `tests/seed-migrations.test.ts` (one case) |
| edu-game-studio (Edu Studio) | EGS-60 | `EGS-60_strata-model-discovery` | same files as VN (`schemas.ts:202,209`; `engine.ts:238`; `ModelsPage.tsx:395-416`) | `seed/config/providers.md:104-119`, :249-259 docs; `seed/config/roles.md:37,39` and the rationale text :56,78-79 ("a family different from the paid writers" is false when DeepSeek runs on Strata: say so); `seed/config/settings.md:5` | `tests/models.test.ts:75`; `tests/seed-migrations.test.ts` |
| scriptorium | SCP-52 | `SCP-52_strata-model-discovery` | `src/shared/schemas.ts` (:25-81, :260); `src/engine/models/registry.ts` (:130-245 load, :347-388 discover, :396-441 syncServerSlots, :460-480 aliasMap/resolve, :445 getModel); `router.ts:185-193`; `openaiCompat.ts:74, 237-249`; `src/engine/summary.ts:150-165`; `src/engine/engine.ts:244-262` (log + event); `src/renderer/.../ModelsDialog.tsx:422-438`, `StatusBar.tsx:12-37`; `src/engine/mcp/tools.ts:1072` (`check_servers` shows `served`); `src/engine/store/migrations.ts` + `dataFolder.ts:119` | `seed/config/providers.md:100-115`, :230-241 docs; `seed/config/roles.md:44-49`; `seed/config/settings.md:11` | `tests/models.test.ts:111`; `tests/migrations.test.ts` (one case) |
| book-translator | BTT-24 | `BTT-24_strata-model-discovery` | `src/shared/schemas.ts` (:29-64, :115); `src/engine/models/registry.ts` (:135, :209-300, :393-440, :441-500, :527, :554-569); `src/engine/dispatcher.ts:185-200` (served in models), :588; `openaiCompat.ts:74`; the chat call (find where `extraBody` is passed, as in `router.ts`); `src/renderer/ui/ModelSelect.tsx:19-21` label, `Settings.tsx:392` text ("128k context, set in its run config" -> "context from Strata"); `src/engine/store/migrate.ts` + `dataFolder.ts:85` | `seed/config/providers.md:98-113`, :218-227 docs; `seed/config/defaults.json:3-11` | `tests/registry.test.ts:357` (down/up test); `tests/dataFolder.test.ts` (one migration case) |
| pixel-art-generator (Pixel Studio) | PAR-17 | `PAR-17_strata-model-discovery` | `src/llm/config.ts:20-52`; `src/llm/registry.ts` (load :160-250, dropMissing :254-258, discover :310-395, syncServerSlots :420-460, resolve); `src/llm/router.ts:118-128`; `src/llm/openaiCompat.ts:141`; `src/main/llm.ts` overview (served) and refresh :228-255; Settings > Models / chat picker label; `src/llm/seedMigration.ts` + `setup.ts:26` | `seed/config/providers.md:38-55` (+ docs section), `seed/config/roles.md:6`, `seed/config/models.md` | `tests/llm/registry.test.ts:152` (installed-models test: a `loaded` row survives and follows L); `tests/llm/customProviders.test.ts` (where `migrateProviders` is tested: one case) |
| midi-generator (Chiptune Studio) | MDI-12 | `MDI-12_strata-model-discovery` | same as Pixel; migration in `src/llm/seedMigrate.ts` | same seed files | `tests/llm/registry.test.ts` (same test as Pixel); its migration test where `migrateProviders` is tested |
| creative-hub | HUB-26 | `HUB-26_strata-model-discovery` | `services.json:144-155`; `scripts/hub.ps1` (`Select-Services` :39-50, `Start-Service1` :105-167, `Show-Status` :62-83, usage comment :7); new `scripts/strata-probe.mjs`; `README.md:44`; `.claude/skills/make-visual-novel/SKILL.md:159`; `ROADMAP.md` row | n/a | none (PowerShell; checked by the commands in AC-H) |

Each tool repo also gets its ticket row in its own `ROADMAP.md`, in that file's style, and `.claude/tickets/<ID>-strata-model-discovery/plan.md` pointing at this plan.

## Tasks for workers

All tool tasks implement C1 exactly; none of them changes C1. A worker that finds C1 impossible in its repo stops and reports instead of inventing a variant.

### T0 (hub, lead) Roadmap row and per-repo ticket folders
- Inputs: this plan.
- Outputs: row 20 in `creative-hub/ROADMAP.md`: `| 20 | HUB-26 | Strata model discovery: the six tools follow whichever model Strata runs (neutral refs strata/default, -low; per-model profiles), hub.ps1 start strata <variant> (.claude/tickets/HUB-26-strata-model-discovery/plan.md) | scriptorium (SCP-52), book-translator (BTT-24), visual-novels-orchestrator (VNO-60), edu-game-studio (EGS-60), pixel-art-generator (PAR-17), midi-generator (MDI-12), hub | user starts Strata (Qwen, then DeepSeek) | Planned |`. Branches created from `origin/master` in each repo (check `git status` clean first; every repo was clean on `master` on 2026-11-04).

### T1 (reference A) visual-novels-orchestrator, VNO-60
- Inputs: C1; files in the table.
- Outputs: C1.1 schema fields; C1.2 rules 1-11 in `registry.ts`/`router.ts`/`openaiCompat.ts`/`summary.ts`/`engine.ts`/`ModelsPage.tsx`; C1.3 seed and defaults; C1.4 migration `strata-loaded-v1` in `SEED_MIGRATIONS`; seed docs (T7 text); two tests (AC-1, AC-3); `yarn typecheck` (or the repo's) and the full test suite green.
- Contract with others: its diff is the replay source for T2, T3, T4. Keep the change in the files listed so the bundle replays cleanly. Write `.claude/tickets/VNO-60-strata-model-discovery/changelog.md` with the C1 rule -> file:line map.

### T2 (replay of T1) edu-game-studio, EGS-60
- Inputs: T1's branch, via the `replay-ticket` skill (bundle of T1).
- Outputs: as T1 for Edu; seed roles text fix (table).
- Note: `replay-ticket` names the target branch after the source branch (its step 3.2). Create `EGS-60_strata-model-discovery` first and tell the implementer to use it, or the house rule (branch named after the repo's own ticket) is broken.

### T3 (replay of T1, adapted) scriptorium, SCP-52
- Inputs: T1 bundle; Scriptorium's own migration style (`migrations.ts` functions).
- Outputs: as T1; `check_servers` MCP output shows `served`; migration function `migrateStrataLoaded` registered in `dataFolder.ts` after `migrateFallbacks` (:119).
- Never start the Scriptorium app or its factory. Tests only (`tests/models.test.ts`, `tests/migrations.test.ts`).

### T4 (replay of T1, adapted) book-translator, BTT-24
- Inputs: T1 bundle; BT's `defaults.json` groups and `migrate.ts`.
- Outputs: as T1; `defaults.json` refs; the `concurrency` -> `auto` part of the migration; `Settings.tsx:392` text.

### T5 (reference B) pixel-art-generator, PAR-17
- Inputs: C1; files in the table. Read T1's changelog for wording, not its code (the registry differs by 708 lines).
- Outputs: C1 in the llm family, including `tools`/`vision` from profiles and the `dropMissing` exemption; `app.json` `selectedModel` and `models.md` `shown` renames in the migration; tests (AC-1, AC-3); `yarn typecheck` and tests green.
- Contract: replay source for T6.

### T6 (replay of T5) midi-generator, MDI-12
- Inputs: T5 bundle via `replay-ticket` (same branch-name note as T2). Migration lives in `src/llm/seedMigrate.ts`.

### T7 (hub) services.json variants, hub.ps1, probe, docs
- `services.json` `strata` entry: `name` "Strata (local LLM server, one model at a time)"; keep `start` = `run-iq3_s.bat` (VN/Edu `autostart.ts` read `start`; their schema is `.passthrough()`, `autostart.ts:56-77`, so a new key is safe); add
  `"variants": { "iq3_s": "D:\\Strata\\run-iq3_s.bat", "iq3_s-solo": "D:\\Strata\\run-iq3_s-solo.bat", "iq3_s-parallel": "D:\\Strata\\run-iq3_s-parallel.bat", "iq4_xs": "D:\\Strata\\run-unsloth-ud-iq4_xs.bat", "deepseek": "D:\\Strata\\run-deepseek-v4.1-flash-ist-das-2.00bpw.bat", "deepseek-coder": "D:\\Strata\\run-deepseek-v4.1-flash-ista-das-coder.bat" }, "defaultVariant": "iq3_s"`; `note`: "Uses most of the GPU memory whichever model it runs; one model per process on 8080. hub.ps1 start strata <variant>."
- `hub.ps1`: in `Select-Services` (:39-50), a token that is not a service id and follows a service with `variants` is that service's variant (unknown token: throw listing the service ids and that service's variants). `Start-Service1` (:105) takes the variant and uses `variants.<v>` as the `console` path (default `defaultVariant`, i.e. today's behaviour). Usage comment :7-10: add `start strata deepseek`. `Show-Status` (:62): for a service whose health answer has `model`, print it (Strata `/health` returns `model` and `loaded`, `server.py:7742-7745`).
- `scripts/strata-probe.mjs` (node, no deps): against `http://127.0.0.1:8080`, prints PASS/FAIL per request: GET `/health`, `/v1/status` (has `model`, `concurrency.serving`), `/v1/models` (first id without `alias_of`); then the requests the tools send: (a) streamed chat, `stream_options.include_usage`, `extra_body` `reasoning_effort: none` (all tools); (b) same with `low` (the checks); (c) a JSON-shaped answer without `response_format` (every tool, `json_schema: false`); (d) a tool-call request with one `tools` function, `reasoning_effort: none` (Pixel/Chiptune artist/composer); (e) one with `response_format: json_schema` (to record whether the profile may set `json_schema: true`; informational). For (a) checks that no reasoning text came back (`reasoning_content` empty) and the answer is non-empty; for (b) that it answered. Output saved by the caller to `runs/`-style notes, not by the script.
- Docs: `README.md:44` row ("local LLM server (Qwen or DeepSeek, one at a time); start with `hub.ps1 start strata [variant]`"); `.claude/skills/make-visual-novel/SKILL.md:159` (`hub.ps1 start strata [variant]`).
- Seed doc text for T1-T6 (each repo adapts paths, Edu keeps `<your Strata folder>`): Strata serves one model per process on 8080, chosen by the `run-*.bat` you start (list the six from `D:\Strata`); the tools ask it which one (`/v1/status`) and use `profiles` for its settings; `strata/default` and `strata/default-low` follow it; add a profile when you install a new model; Strata takes most of the GPU memory with any of them, so keep only the nomic embedding model in LM Studio and no ComfyUI while it runs; `context` in a profile must match the config's `--max-context` (131072 for all six now); remove the iq2_xs / coder-iq1_m / 84 GB / 48 GB lines.

### T8 (lead, after merge) User data
See "User-data migration".

### T9 (lead + user) Live checks
See "Live checks needing the user".

## Order and parallelism

1. T0, then three parallel lanes:
   - Lane A: T1 (VN, reference) -> when its tests pass and the lead reviewed the diff: T2, T3, T4 in parallel through `replay-ticket` (Edu is a near copy; Scriptorium and BT are close copies with their own migration code, so give their implementers the "adapted" notes above).
   - Lane B: T5 (Pixel, reference) -> T6 (Chiptune) through `replay-ticket`.
   - Lane C: T7 (hub). Its probe is needed before T9.
2. Why VN first: it is the middle of the engine family (116 lines from Scriptorium, 17 from Edu), it has the cleanest migration mechanism (`SEED_MIGRATIONS` with ids), and it can be started for a live check without risk (unlike Scriptorium).
3. Lanes A and B share only C1, so they run at the same time.
4. T8 after each repo's branch is merged. T9 after T7 and at least T1 and T5; the full live round after all six.

## User-data migration

The repos' own seed migrations (C1.4) do the work when each app starts. Per data folder:

| folder | what changes | how it runs |
|---|---|---|
| `~\VisualNovels\config` | `providers.md:121-136` strata block; `roles.md:17`; `settings.md:5` | VN Studio start (`strata-loaded-v1`) |
| `~\EduGames\config` | `providers.md:104-119`; `roles.md:37,39`; `settings.md:5` | Edu Studio start |
| `~\BookTranslator\config` | `providers.md:110-126` (and `concurrency: 1` -> `auto`); `defaults.json:4-16,156` | Book Translator start |
| `~\PixelStudio\config` | `providers.md:38-55`; `roles.md:6`; `models.md:12`; `app.json:2` | Pixel Studio start |
| `~\ChiptuneStudio\config` | `providers.md:38-55`; `roles.md:6`; `models.md:11-12`; `app.json:2` | Chiptune Studio start |
| `~\Scriptorium\config` | `providers.md:141-157`; `roles.md:62-82` | Scriptorium never starts without the user's yes. Apply the migration without the factory: `npm run engine -- probe --model strata/default` in the Scriptorium repo runs `initDataFolder` (all migrations, `cli.ts:14-17`) and sends one request to Strata only; ask the user before running it. |

Manual step (not a migration, because a migration must not re-add a row the user removed): add `strata/default` to `~\Scriptorium\config\settings.md` `fallbacks` (verified missing, :9-11), via the Models panel or the file, at the position the user picks (open question 1). Until then the `strata` alias in its `roles.md` stays unresolved, as today.

Before T8: back up each `config` folder to `creative-hub/.claude/temp/HUB-26-backup/<app>/` and close the app (a running app holds its data folder). Not touched: project and history files (Out of scope); the legacy aliases resolve them.

## Acceptance criteria

| id | criterion | proved by |
|---|---|---|
| AC-1 | With `/v1/status` answering `model: deepseek-v4.1-flash`, `strata/default` has `servedId` `deepseek-v4.1-flash`, family `deepseek`, extra_body `{reasoning_effort: none}`, and `strata/default-low` `{reasoning_effort: low}`; a switch to `qwen3.8-flash-next-iq3_s` gives family `qwen` (prefix profile) on the same objects; Strata down keeps L and marks the provider down; `getModel('strata/qwen3.8-flash-next-low')` is `strata/default-low`; discovery adds no `strata/<real id>` model | one extended registry test per repo (table column "tests to extend"); in Pixel/Chiptune the same test also shows the `loaded` row survives `dropMissing` |
| AC-2 | The seed configs load and every role resolves to a model with the new block | the existing seed-config tests (Scriptorium `tests/models.test.ts:42`, Pixel `tests/llm/registry.test.ts:46`, BT `tests/registry.test.ts:14`, VN/Edu seed tests), unchanged, still green |
| AC-3 | The migration turns the old user block and refs into C1 once, keeps a user's extra Strata row, does nothing when the strata provider was deleted; BT `concurrency: 1` becomes `auto` | one migration test per repo (table) |
| AC-4 | Typecheck and the full test suite pass in each repo | each repo's `typecheck` and `test` scripts (Node through `fnm exec --using default` if `node` is not on PATH) |
| AC-5 | No stale Strata text left | `grep -rn "run-iq2_xs\|coder-iq1_m\|84 GB\|Qwen3.8-Flash-Next server\|server for Qwen3.8" */seed/config creative-hub/README.md creative-hub/services.json` over the six repos: no hit |
| AC-H1 | `hub.ps1 start strata nope` fails with the variant list and starts nothing; `hub.ps1 start strata` with Strata already up prints "already up" (port check first, :106) | run by the worker (no GPU load: the bad variant throws before any start; the second needs Strata up, else skip) |
| AC-H2 | `hub.ps1 start strata deepseek` opens a console running `run-deepseek-v4.1-flash-ist-das-2.00bpw.bat`; `hub.ps1 status` shows `strata ... deepseek-v4.1-flash` | live, the user runs it (L1) |
| AC-L1 | DeepSeek accepts every request the tools send | `node scripts/strata-probe.mjs` all PASS for (a)-(d) with DeepSeek loaded (L2); (e) recorded |
| AC-L2 | The apps show the real model and still work after a switch | L3 to L5 |

## Live checks needing the user

Strata takes most of the GPU memory: only the user starts or stops it, and nothing else heavy runs meanwhile (no ComfyUI, only the nomic model in LM Studio). The DeepSeek config allows up to an hour to get ready (`engine_ready_s: 3600` in `D:\Strata\strata-deepseek-v4.1-flash-ist-das-2.00bpw.json`): wait for `/health` `loaded: true`.

- **L1** (user): `pwsh -File scripts\hub.ps1 start strata deepseek`, wait for `loaded: true`, then `hub.ps1 status`. (AC-H2)
- **L2** (lead, Strata DeepSeek up): `node scripts/strata-probe.mjs`; save the output in `runs/hub-26-strata.md`. If (a) still returns reasoning text or (b) fails, stop: add the needed `extra_body` to the `deepseek-v4.1-flash` profile (for example `chat_template_kwargs: { enable_thinking: false }`, which Strata also reads, `server.py:5232-5234` and `D:\Strata\docs\DEEPSEEK41.md:124`) in every seed and re-run. Repeat L2 later with the Qwen IQ3_S Strata (user restarts it with `hub.ps1 start strata`) to confirm no regression.
- **L3** (lead, VN Studio, safe to start): `hub.ps1 start vn-studio`; Models page shows `Strata: deepseek-v4.1-flash`; `npm run engine -- probe --model strata/default` and `--model strata/default-low` from the repo answer; one small text job (for example the `vn.analyse` of an existing production) runs on Strata.
- **L4** (lead): Edu Studio, Book Translator (a short glossary job on a test project), Pixel Studio and Chiptune Studio (one chat message each with `Strata: deepseek-v4.1-flash` picked, which uses tools): each shows the real name and answers.
- **L5** (user switches Strata to Qwen while VN Studio runs): within about 10 s the Models page shows `qwen3.8-flash-next-iq3_s`, the log has `strata now serves ...`, and the next job runs.
- **L6** (only with the user's explicit yes): Scriptorium. Default is the CLI probe from the user-data table, which does not start the factory. Starting the app is the user's call.
- Record in `runs/hub-26-strata.md` what was verified and what was not; the ticket is done when the user has used the apps on the DeepSeek Strata.

## Open questions for the user

1. ANSWERED yes (user; manual step in T8): add `strata/default` as the second row (between `deepseek/deepseek-flash` and LM Studio, as the seed has it)? With `fallback_shared: true` every role then uses Strata when it runs.
2. Variant names for `hub.ps1 start strata <variant>`: `iq3_s` (default), `iq3_s-solo`, `iq3_s-parallel`, `iq4_xs`, `deepseek`, `deepseek-coder`. Keep these? ANSWERED: names kept.
