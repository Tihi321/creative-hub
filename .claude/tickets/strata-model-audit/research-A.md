# Strata model audit (A): scriptorium and book-translator

Question: do the tools that use the local Strata server (http://127.0.0.1:8080/v1) have its model hardcoded, now that Strata serves more than Qwen3.8-Flash-Next?

## Strata now (all confirmed by reading files; server is down, nothing run)
- One model per process, one port (8080). Each `D:\Strata\run-*.bat` starts `serve\server.py --config strata-<name>.json --port 8080`. Six launchers: `run-iq3_s.bat`, `-iq3_s-solo`, `-iq3_s-parallel` (4 slots), `run-unsloth-ud-iq4_xs.bat` (Qwen), `run-deepseek-v4.1-flash-ist-das-2.00bpw.bat` and `run-deepseek-v4.1-flash-ista-das-coder.bat` (DeepSeek). Starting a second one on port 8080 is a conflict, so the user swaps models by restarting. `apps/host/docs/plans/09-multiple-models.md:7` says one model at a time is the default (multi-load only in Expert mode, design host).
- `/v1/models` returns the config's `model_name` as id (`serve/server.py:7773-7790`; `model_name` read at `:9323-9325`, default `qwen3.8-flash-next`). Names now: `qwen3.8-flash-next-iq3_s` (strata-iq3_s*.json), `qwen3.8-flash-next-unsloth-ud-iq4_xs`, `deepseek-v4.1-flash` (both DeepSeek configs).
- The `model` field of a request is NOT checked: `model_for()` just echoes an alias or answers with its own name, "other names are still served" (`server.py:4816-4820`). Only `/v1/load` and `/v1/unload` reject a wrong model (`:7893`). So sending `qwen3.8-flash-next` to a DeepSeek server works and is answered by DeepSeek.
- `reasoning_effort` in a request is consumed by the Strata template layer (`server.py:5222-5239, 5476-5480`); the server also has its own default (`config_effort`). Not run, so how DeepSeek reacts to `none`/`low` is inferred, not tested.
- `/status` gives `concurrency.serving` and `loaded` (tools rely on it); DeepSeek configs set `--max-context 131072`, the same as Qwen (confirmed in the JSON files).

## Scriptorium (C:\projects\Personal\scriptorium, data in ~\Scriptorium)

| file:line | what | class | breaks if model changes? |
|---|---|---|---|
| src/shared/schemas.ts:260 | zod default `fallbacks` includes `strata/qwen3.8-flash-next` | DEFAULT in code, overridable by `config/settings.md` `fallbacks` / Models panel | n: only a seed when settings.md has no `fallbacks`; the id is just a label sent as `model` (Strata ignores it) |
| src/engine/store/migrations.ts:497 | `OLD_DEFAULT_MODELS.strata = 'strata/qwen3.8-flash-next'` | HARDCODED, legacy migration only | n: runs only for old settings that still have `default_strata_model` |
| src/engine/models/registry.ts (:108, :392-411, :505-512) | alias `strata` resolves to first strata row of `fallbacks`; slots read from `GET <base>/status` -> `concurrency.serving`; down when `loaded === false` | DISCOVERED at runtime (slots/loaded); aliases from config | n |
| src/engine/models/router.ts:221, engine.ts:127 | connection refused = mark Strata down, skip to next model | runtime behaviour, no model name | n |
| src/renderer/office/scene.ts:314, store/model.ts:116,130 | label "Strata local", colour by provider id `strata` | cosmetic | n |
| ModelsDialog.tsx:422-438, StatusBar.tsx:12-37, mcp/tools.ts:1072, summary.ts:200 | UI/MCP text mentioning Strata | cosmetic | n |
| seed/config/providers.md:100-115 and ~\Scriptorium\config\providers.md:141-157 | provider `strata`: `base_url http://127.0.0.1:8080/v1`, `discover: false`, `json_schema: false`, `concurrency: auto`, models `qwen3.8-flash-next` (`reasoning_effort: none`, ctx 131072, family qwen) and `qwen3.8-flash-next-low` (`reasoning_effort: low`) | CONFIG only (user data file; seed copied once) | Mostly n. Because `discover: false`, the app never learns the real loaded model. Wire id is ignored, so calls work, but UI/logs/cost/family say "qwen3.8-flash-next" while DeepSeek answers. `extra_body.reasoning_effort` is sent to DeepSeek: behaviour unknown (inferred, not tested). Context 131072 equals DeepSeek's max-context, so n |
| seed/config/providers.md:236 (doc) | states "It ignores the `model` field ... the two ids only differ in `extra_body`" | doc, matches server code | n |
| ~\Scriptorium\config\roles.md (lines 8-57: `strata`; 62-82: `strata/qwen3.8-flash-next-low` for archivist/researcher/checks) | roles name the alias or the concrete `-low` id | CONFIG only | n for the alias. `-low` id is a name coupled to the providers.md row, not to the served model |
| ~\Scriptorium\config\settings.md `fallbacks` | has NO strata row (only deepseek-flash, lmstudio gemma). With `fallback_shared: true` the alias `strata` finds no row | CONFIG | y/behaviour: `strata` alias in roles.md is an unresolved alias in the user's current data (registry.ts:505 `resolve` returns it as is; `unresolvedAliases()` at :508). Verify in the Models panel whether Strata is actually used at all right now. Inferred, not run |
| ~\Scriptorium\books\*\book.md, logs, made.md, chapters history (circuit-breaker, echoes-in-the-deep, rust-and-ruin) | past runs record `strata/...` | data / history | n |
| tests/models.test.ts (56 hits), scheduler.test.ts, migrations.test.ts, features.test.ts, renderer/store.test.ts, renderer/office.spec.ts | use `strata/qwen3.8-flash-next` as fixtures | tests, HARDCODED strings | n (fixtures, no real server) |
| src/renderer/demo/fake.ts | demo data | cosmetic | n |
| docs/design.md, .claude/tickets/SCP-03 etc. | docs | cosmetic | n |

No hit in Scriptorium for model-specific prompt templates, token limits or chat-template flags tied to Qwen. Only `family: qwen` metadata (registry.ts:~597 guesses family from the id string) and the `reasoning_effort` extra_body.

## Book Translator (C:\projects\Personal\book-translator, data in ~\BookTranslator)

| file:line | what | class | breaks if model changes? |
|---|---|---|---|
| src/shared/schemas.ts:115 | zod default `fallbacks` = deepseek-flash, `strata/qwen3.8-flash-next` | DEFAULT in code, overridable by defaults.json / Settings | n (label only) |
| src/engine/dispatcher.ts:588 | `seedFallbacks = ['deepseek/deepseek-flash','strata/qwen3.8-flash-next']` | HARDCODED, used as migration/seed fallback | n unless the user removes it; it is compared against the saved list, then only a seed |
| src/engine/models/registry.ts:135, :527 | same fallback list when none saved | DEFAULT in code | n |
| src/engine/models/registry.ts:633 | `provider === 'strata'` is a known group | HARDCODED provider id, not a model | n |
| src/engine/models/registry.ts:440-460 | slots from `/status`, down when unloaded | DISCOVERED at runtime | n |
| src/renderer/ui/ModelSelect.tsx:19-21 | `BASE_GROUPS = ['paid','strata','lmstudio']`, label "Strata" | HARDCODED group list/labels | n |
| src/renderer/ui/Settings.tsx:392 | text "Strata needs no refresh (128k context, set in its run config)" | cosmetic, but states 128k | n (DeepSeek also 131072) |
| src/engine/store/migrate.ts:13 | `LEGACY_SEED_PROVIDERS` includes `strata` | HARDCODED legacy list | n |
| NewProject.tsx:381,443, ModelsDialog.tsx:193-209, cli.ts:102, serve.ts:71 | UI and comment text | cosmetic | n |
| seed/config/defaults.json:3-11 and ~\BookTranslator\config\defaults.json:4-16, :156 | agentModels glossary/qa use `strata/qwen3.8-flash-next`; translator/proofreader use deepseek first; `groupDefaults.strata = strata/qwen3.8-flash-next`; `context: 131072` | CONFIG only | n for the call (model id ignored); same label/metadata caveat as above |
| seed + ~\BookTranslator\config\providers.md (strata block, ~:98-113) | `base_url http://127.0.0.1:8080/v1`, `discover: false`, `json_schema: false`, ids `qwen3.8-flash-next` (`reasoning_effort: none`) and `-low`. User copy has `concurrency: 1`, not `auto` (the seed has `auto` in a comment only; the user file is fixed to 1, so parallel chapters on Strata are off) | CONFIG only | Same as Scriptorium: `reasoning_effort` behaviour on DeepSeek unknown. `concurrency: 1` is not a model issue but means a 4-slot Strata is not used |
| seed/config/providers.md:218-227 (docs section) | says "Strata is a local Qwen3.8-Flash-Next server", "ids here are only names" | cosmetic doc, outdated | n |
| tests/registry.test.ts (51), router.test.ts (22), dispatcher.test.ts (20), clientOnly.test.ts, pipelineHelpers.ts | fixtures use the strata id | tests | n |
| README.md (9 hits), ROADMAP.md | docs | cosmetic | n |
| ~\BookTranslator\projects\* | not searched in depth | data | open |

No Qwen-specific prompt, template or context-size code found in either repo (grep for qwen / reasoning / thinking in src/engine/models gave only `family` guesses and Gemini thinking tokens).

## Bottom line
- Neither repo hardcodes the served model in a way that blocks a switch. Both set `discover: false` and rely on Strata ignoring the `model` field (confirmed in Strata `serve/server.py:4816-4820`). A DeepSeek Strata is called with `model: "qwen3.8-flash-next"` and answers normally.
- The real couplings are all in user config: provider ids `qwen3.8-flash-next` / `-low`, `family: qwen`, `extra_body.reasoning_effort`, and the labels. They mislead (logs/UI say Qwen) and could mis-set thinking for DeepSeek, but do not fail requests.
- Hardcoded in code: only default/seed fallback strings `strata/qwen3.8-flash-next` (scriptorium schemas.ts:260, migrations.ts:497; book-translator schemas.ts:115, dispatcher.ts:588, registry.ts:135,527), the group list in ModelSelect.tsx:19 and tests.

## What to change (suggestions only)
1. Decide: keep the fixed neutral ids (current design, Strata ignores them) or add a runtime lookup. Option: a provider flag `discover: true` for Strata reading `/v1/models` (Strata returns the real `model_name`), which would show `deepseek-v4.1-flash` in UI/logs. Needs code in both repos' registry; check Strata `/v1/models` output shape (it includes `status` and `meta.n_ctx`).
2. If keeping fixed ids, rename the Strata rows to neutral ones (e.g. `strata/local`, `strata/local-low`) in both providers.md files, roles.md, defaults.json and the code fallback strings, with a migration. Smaller option: leave ids, only fix the docs/labels.
3. Test, with the DeepSeek Strata running, that `reasoning_effort: none` and `low` do what is wanted (server.py:5222-5239 handles it; DeepSeek behaviour untested here) and that `json_schema: false` is still right. If DeepSeek needs different extra_body, add a separate row (e.g. `strata/deepseek-v4.1-flash`) with its own extra_body and `family: deepseek`.
4. Scriptorium: user `settings.md` `fallbacks` has no strata row, so the `strata` alias in `roles.md` may be unresolved; add `strata/qwen3.8-flash-next` (or the new id) to `fallbacks` if Strata should be used.
5. Book Translator: user `providers.md` has `concurrency: 1` for Strata; set `auto` if parallel launchers are used.
6. Update docs saying "Strata is a Qwen3.8-Flash-Next server" (both providers.md, Scriptorium roles.md prose, book-translator Settings.tsx:392 text).

## Open questions
- Does Strata with a DeepSeek model honour `reasoning_effort: none/low`? Not tested (server down).
- Which Strata launcher the user runs day to day; only `strata-iq3_s.log` and others exist as logs, not checked.
- Contents of ~\BookTranslator\projects were not audited.
- Git log in D:\Strata shows only upstream commits (latest `ffa80d73`); no local commit documenting the user's model change was found.
