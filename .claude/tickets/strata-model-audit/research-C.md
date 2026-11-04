# Research C: Strata model audit, Pixel Studio and Chiptune Studio

Question: do Pixel Studio (C:\projects\Personal\pixel-art-generator) and Chiptune Studio (C:\projects\Personal\midi-generator), with their user data ~\PixelStudio and ~\ChiptuneStudio, hardcode the Strata model "qwen3.8-flash-next"?

## Answer
Both use Strata, through a generic OpenAI-compatible provider named `strata` (base_url http://127.0.0.1:8080/v1). Neither repo has a Strata model id in TypeScript code (grep of `src/` for qwen / flash-next / 8080 / strata finds only the reserved provider-name lists, which hold no model id). The model id is CONFIG (providers.md, roles.md, models.md, app.json), seeded from `seed/config/*`. Strata has `discover: false` in both, so models Strata serves now (e.g. DeepSeek) do NOT appear until you add them to providers.md or via Settings > Models. Nothing breaks if Strata serves other ids, unless the id Strata no longer serves is the one that is selected. Both repos have the same structure (confirmed by diff and grep). All claims below are confirmed by reading or grep; nothing was run.

Other LLM wiring (both): LM Studio :1234 (discover true), DeepSeek API, OpenRouter, Ollama, OpenAI, Anthropic, Gemini, ACP proxy :7461, mock (`seed/config/providers.md`; `src/llm/{openaiCompat,anthropic,gemini,registry}.ts`).

## Pixel Studio (pixel-art-generator)
Seed = `seed/config/*` in repo. Live copy = ~/PixelStudio/config/*. `~` = C:\Users\Infplane.

| file:line | what | class | breaks if model changes? |
|---|---|---|---|
| src/** (no hit) | no model id and no 8080 in code | n/a | n |
| src/llm/customProviders.ts:12 | `RESERVED_PROVIDER_IDS` includes 'strata' (provider name only) | HARDCODED name, cosmetic for models | n |
| src/llm/seedMigration.ts:14 | `LEGACY_SEED_PROVIDERS` includes 'strata' (name only) | HARDCODED name | n |
| src/llm/registry.ts:33,426-436 | reads Strata `/status` for concurrency and context; `GET base_url/status` | DISCOVERED at runtime, not model-specific | n |
| seed/config/providers.md:38-55 | provider strata, base_url :8080/v1, models `qwen3.8-flash-next`, `qwen3.8-flash-next-low` (ctx 131072, tools true, extra_body reasoning_effort) | CONFIG (seed, applied to new installs) | y for these two ids if Strata drops them; they are listed with fixed settings |
| seed/config/providers.md:44 | `discover: false` ("Strata answers any model name") | CONFIG | y in effect: new Strata models (DeepSeek) are not listed; the "answers any model name" assumption may no longer hold now Strata serves several models, so an unknown id may 404 or route wrongly (inferred, Strata not checked) |
| seed/config/providers.md:45 | `json_schema: false` for provider | CONFIG | n, but it applies to every model on Strata, DeepSeek included (also false at deepseek:62) |
| seed/config/providers.md:49-55 | `extra_body: {reasoning_effort: none/low}` on the Qwen entries | CONFIG, per model | y/inferred: a DeepSeek model added via Settings gets no extra_body; if Strata forwards unknown fields it is harmless |
| seed/config/roles.md:6 | alias `strata: strata/qwen3.8-flash-next` | CONFIG | n unless a role uses the alias (none does: artist and palette use `[lmstudio]`) |
| ~/PixelStudio/config/roles.md:6,12,15 | same as seed; artist and palette = `[lmstudio]` (Strata is not in any role) | CONFIG | n for roles |
| ~/PixelStudio/config/app.json | `selectedModel: "strata/qwen3.8-flash-next"` (the chat's picked model) | CONFIG (UI choice, changeable in the chat model picker) | y: if Strata stops serving this id the chat fails until you pick another (a picked model goes first; roles fall back only on failure) |
| ~/PixelStudio/config/models.md | `shown` has `strata/qwen3.8-flash-next` (not `-low`); also acp, deepseek (direct API), lmstudio models | CONFIG | n; new Strata models are absent from the dropdown until ticked/added |
| ~/PixelStudio/config/providers.md:38-55 | strata block identical to seed (live copy; differs from seed only by the added acp provider) | CONFIG | as seed |
| src/main/appSettings.ts:19 | `selectedModel` default is `null`, no model default in code | DEFAULT null | n |
| tests/llm/{registry,customProviders}.test.ts, tests/main/agentLlm.test.ts | use qwen/strata strings in fixtures | test only | n (tests use their own fixtures; not run) |
| ~/PixelStudio/chats/*.json | 2 of 3 chat files mention strata (history) | data | n |

## Chiptune Studio (midi-generator)
Same files, same lines. `src/llm/*.ts` have no Strata model id; reserved names at `src/llm/customProviders.ts:12` (list continues on line 12 with 'strata'); `src/llm/registry.ts:33,420-436` reads `/status`. Seed `seed/config/providers.md:38-55`, `roles.md:5-7`, `models.md`.

| file:line | what | class | breaks if model changes? |
|---|---|---|---|
| src/** (no hit) | no model id in code | n/a | n |
| src/llm/customProviders.ts:12 | reserved id 'strata' | HARDCODED name | n |
| seed/config/providers.md:38-55 | strata provider with the same two Qwen ids, `discover: false` (:44) | CONFIG | y for those ids; new models not auto-listed |
| seed/config/roles.md:6 | alias `strata: strata/qwen3.8-flash-next`; composer and theory = `[lmstudio]` | CONFIG | n |
| ~/ChiptuneStudio/config/roles.md | same as seed, Strata not in a role | CONFIG | n |
| ~/ChiptuneStudio/config/app.json | `selectedModel: "strata/qwen3.8-flash-next"` | CONFIG (UI choice) | y if Strata no longer serves it |
| ~/ChiptuneStudio/config/models.md | `shown` has `strata/qwen3.8-flash-next` and `-low` | CONFIG | n; new Strata models not shown |
| ~/ChiptuneStudio/config/providers.md:38-55 | strata block as seed | CONFIG | as seed |
| ~/ChiptuneStudio/config/seed-state.json | only `acp` marked seeded (no overwrite of strata block by seed updates) | CONFIG | n; editing live providers.md is the way, seed edits would not propagate (inferred from file; not read in seedMigrate.ts) |
| tests/llm/registry.test.ts, tests/main/agentLlm.test.ts | qwen/strata fixtures | test only | n |

## What to change (suggestions only)
1. In both live configs set `selectedModel` in `config/app.json` (or pick in the chat model picker) to a model Strata serves now; it is the only place that currently names the old id as active.
2. Add the new Strata models to `~/PixelStudio/config/providers.md` and `~/ChiptuneStudio/config/providers.md` under `strata.models` (id, family, tools, context), or set `discover: true` on strata so `/v1/models` fills the list (then tick them in Settings > Models; discovered models must be ticked in `models.md`). Check first that Strata's `/v1/models` lists real ids, since the `discover: false` comment says Strata "answers any model name".
3. Update the seed (`seed/config/providers.md`, `roles.md` alias) in both repos so new installs match, in a ticket branch in each repo.
4. If a Strata model should back a role, add `strata` or the model ref to `artist`/`palette`/`composer`/`theory` in the live roles.md; today they all use only LM Studio.
5. Tool support and `extra_body` (reasoning_effort) are per-model: set them for any DeepSeek entry added on Strata.

## Open questions
- What Strata's `/v1/models` and `/status` return now (not queried; services not touched).
- Whether Strata still accepts unknown model names (the seed comment assumes it does).
- Whether the live models.md/app.json refer to ids that Strata still serves.
