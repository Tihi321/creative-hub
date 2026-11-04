# Strata model audit (B): do the tools hardcode the Strata model?

Question: do visual-novels-orchestrator (VN Studio), edu-game-studio (Edu Studio), creative-hub and the make-* skills hardcode the Qwen3.8-Flash-Next model of the local Strata server? Server was down; read-only audit, nothing run.

## Strata now (confirmed, files in D:\Strata)
- One model per process, always port 8080 (`D:\Strata\run-*.bat` -> `serve\server.py --engine strata --config <json> --port 8080`). Scripts: run-iq3_s.bat, run-iq3_s-solo.bat, run-iq3_s-parallel.bat, run-unsloth-ud-iq4_xs.bat, run-deepseek-v4.1-flash-ist-das-2.00bpw.bat, run-deepseek-v4.1-flash-ista-das-coder.bat.
- `model_name` in the configs (what `/v1/models` reports as `id`, serve/server.py:7773-7780): `qwen3.8-flash-next-iq3_s` (the 3 iq3_s scripts), `qwen3.8-flash-next-unsloth-ud-iq4_xs`, `deepseek-v4.1-flash` (both DeepSeek scripts, same id).
- `--max-context 131072` in all configs. Thinking is on by default; `reasoning_effort: "none"` or `enable_thinking:false` turns it off (docs/DEEPSEEK41.md:124, server.py:5476), so the thinking switch is model-agnostic.
- Scripts named in the VN/Edu docs (run-iq2_xs.bat, run-coder-iq1_m.bat) no longer exist in D:\Strata (inferred: stale docs).

## Verdict
No source file bakes the Strata model id into logic that cannot be changed from config. The id lives in (a) a built-in default string in `schemas.ts` / `seedMigrations.ts`, used only if settings.md has no `fallbacks`; (b) the seeded and user `config/providers.md`, `settings.md`, `roles.md`. Because `discover: false` and Strata ignores the request `model` field (per the docs, not re-verified in server.py), the id the apps send is effectively a label: a DeepSeek-loaded Strata still answers to `strata/qwen3.8-flash-next`. It works but is mislabeled. What could matter is listed at the end.

## visual-novels-orchestrator
| file:line | what | class | breaks if model changes? |
|---|---|---|---|
| src/shared/schemas.ts:137,144 | `BUILTIN_FALLBACKS` / `BUILTIN_GROUP_DEFAULTS.strata = 'strata/qwen3.8-flash-next'` | DEFAULT in code; overridden by `fallbacks` / `group_defaults` in config/settings.md (or the Models page) | n (only if the id is removed from providers.md: then the ref has no row) |
| src/engine/store/seedMigrations.ts:100,118 | same string as fallback in an old-settings migration | DEFAULT in code, one-time migration | n |
| src/engine/studios/autostart.ts:21 | `NEVER_STARTED = ['scriptorium','strata']` | HARDCODED by service id `strata` (not by model) | n |
| src/engine/studios/autostart.ts:336-340 | ComfyUI not started while the `strata` registry entry answers its health URL | HARDCODED guard by service id; fires for any model on 8080 | n for logic; assumes any Strata model hogs the GPU (true for all now installed) |
| src/engine/models/registry.ts:396-417 | `concurrency: auto` reads `GET <base>/status` (`concurrency.serving`, `loaded`, `auto_load`) | DISCOVERED at runtime | n |
| src/engine/models/customProviders.ts:11 | `strata` is a reserved provider id | HARDCODED id | n |
| src/engine/engine.ts:116,178; summary.ts:79; router.ts:213 | comments / local-server health checks keyed on `concurrency: auto` | DISCOVERED / cosmetic | n |
| src/renderer/ui/ModelsPage.tsx:390,410,411 | labels ("Strata's -low for the checks") | cosmetic | n |
| seed/config/providers.md:104-119 (user copy ~/VisualNovels/config/providers.md:121-136) | provider `strata`, base_url http://127.0.0.1:8080/v1, `discover:false`, `json_schema:false`, models `qwen3.8-flash-next` (reasoning_effort none) and `-low` (low), `family: qwen`, `context: 131072` | CONFIG only | y if a model with another context is loaded: `context` must equal `--max-context` (all 6 configs are 131072 now: ok). `family: qwen` use not traced. `json_schema:false` was chosen on Qwen behaviour, untested on DeepSeek |
| seed/config/providers.md:196-206 | Strata section: "Qwen3.8-Flash-Next", 84 GB IQ3_S, keep only nomic loaded in LM Studio, stale iq2_xs scripts | doc | cosmetic; VRAM advice is Qwen-quant specific |
| seed/config/roles.md:5-19 (user copy same) | roles use alias `strata`; line 17 names `strata/qwen3.8-flash-next-low` | CONFIG only | only if the id is renamed in providers.md |
| seed/config/settings.md:5 (user copy) | `fallbacks` has `strata/qwen3.8-flash-next` | CONFIG only | same |
| seed/config/autostart.md:23 | text | doc | n |
| tests/autostart.test.ts:28,158,295 | strata entry on 8080, never-started, ComfyUI guard | test fixture | n |
| tests/models.test.ts, custom-providers.test.ts, seed-migrations.test.ts, scheduler.test.ts | grep hits for strata / default id (not read line by line) | tests | fail only if the built-in default string changes |
| docs/mcp-guide.md:175,211; README.md:10,45,105-112 | docs | cosmetic | n |

## edu-game-studio
Same engine code copy: src/shared/schemas.ts:202,209 (built-in defaults `strata/qwen3.8-flash-next`), src/engine/store/seedMigrations.ts:100,118, src/engine/studios/autostart.ts:21,336 (ComfyUI guard), registry.ts:399-401, customProviders.ts:11, ModelsPage.tsx:395-416. Classes and answers identical to the VN table.
| file:line | what | class | breaks? |
|---|---|---|---|
| seed/config/providers.md:104-119 (user ~/EduGames/config/providers.md:104-119) | provider `strata`, same models, context 131072 | CONFIG only | as VN: `context` must match |
| seed/config/roles.md (user copy lines 37, 39) | `strata/qwen3.8-flash-next-low` named directly (researcher, fact-checker); other roles use alias `strata` | CONFIG only | an id rename needs these 2 lines edited |
| seed/config/settings.md:5 | fallbacks entry | CONFIG only | as above |
| seed/config/providers.md:249-259, roles.md:56,78-79 | text "Qwen3.8-Flash-Next"; rationale "a model family different from the paid writers" | doc | cosmetic, but with DeepSeek loaded the diversity argument is gone (paid default is `deepseek/deepseek-flash`) |
| scripts/studio-shots.mjs | grep hit (not read) | cosmetic (inferred) | n |

## creative-hub
| file:line | what | class | breaks? |
|---|---|---|---|
| services.json:145-153 | entry `strata`, name "Strata (Qwen3.8-Flash-Next server)", port 8080, health `/health`, start = `D:\Strata\run-iq3_s.bat` | CONFIG; start script is Qwen-specific | y: `hub.ps1 start strata` always loads Qwen IQ3_S, never DeepSeek. Health check is model-agnostic |
| README.md:44 | "Qwen3.8-Flash-Next server, first model choice of Scriptorium and Book Translator" | cosmetic | n |
| README.md:25; scripts/hub.ps1:7 | generic mention; not in default start set | cosmetic | n |
| .claude/skills/make-visual-novel/SKILL.md:16,159,160 | generic Strata start hints, GPU clash with ComfyUI | cosmetic | n |
| ~/.claude/skills/make-* ; ROADMAP.md; .mcp.json | no hit for strata / qwen3.8 | none | n |

## Behaviour that could break with a different or bigger model
1. `context: 131072` in providers.md must equal Strata's `--max-context`; matches now, edit (seed and user copies) if a bigger-context model is loaded.
2. VRAM: no code checks memory; the only guard is "no ComfyUI while Strata answers". A DeepSeek pack's size vs the 84 GB Qwen quant is unverified.
3. Thinking flags are `extra_body.reasoning_effort` in providers.md; Strata honours them for DeepSeek (docs), so fine.
4. Usage/cost logs and UI show `strata/qwen3.8-flash-next` whichever model ran (inferred from `discover:false` and Strata ignoring `model`).
5. `json_schema:false` and `family: qwen` are Qwen-era choices, untested on DeepSeek.
6. `hub.ps1 start strata` launches only run-iq3_s.bat.

## What to change (suggestions only)
- Nothing is required for it to work. For clean labels: add neutral ids (e.g. `strata/default`, `strata/default-low`) in providers.md, settings.md, roles.md of both seeds and both user dirs, and change the two built-in default strings (schemas.ts, seedMigrations.ts) in each repo.
- If DeepSeek on Strata should be a deliberate choice: add model rows with `family: deepseek` and the right `context`; note one model per process on one port.
- services.json: make the start script selectable (or add a second entry such as `strata-deepseek`); rename "Qwen3.8-Flash-Next server" in services.json:146 and README.md:44.
- Refresh the stale Strata section text (iq2_xs / coder-iq1_m scripts, 84 GB advice) in both seed providers.md files; user copies are kept if edited, so edit those by hand.
- Optional: use `discover: true` so the real id from `/v1/models` appears.

## Open questions
- Does server.py really ignore the request `model` field (docs say so; not found in code here)?
- Is `family: qwen` used to choose prompts or behaviour? Not traced.
- VRAM of the DeepSeek packs vs Qwen IQ3_S.
- Test files other than autostart.test.ts were only listed by grep.
