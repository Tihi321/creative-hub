# HUB-26 check (integration, deep)

Checked 2026-11-04 by the checker, read-only, on the ticket branches: creative-hub `HUB-26_strata-model-discovery` b6d9559, visual-novels-orchestrator `VNO-60_…` 9d0d173, edu-game-studio `EGS-60_…` 8a61553, scriptorium `SCP-52_…` 96042eb, book-translator `BTT-24_…` 7a646bf, pixel-art-generator `PAR-17_…` f095e5b, midi-generator `MDI-12_…` 4ebe843. Nothing started (no app, engine, probe, Strata or factory), no user data touched, nothing fixed or committed.

VERDICT: PASS with unchecked items (no FAIL; live criteria unchecked; low-severity gaps below)

## Commands run

- Each tool repo, yarn via `PATH=<fnm default alias dir>:$PATH`: `yarn typecheck` then `yarn test`.
- creative-hub: `pwsh -NoProfile -File scripts/hub.ps1 start strata nope`; `fnm exec --using default node --check scripts/strata-probe.mjs`; `JSON.parse(services.json)`.
- AC-5 grep (below).
- In-memory repro of the `resolve()` gap with tsx (scratchpad script `repro-resolve.mts`): loads each repo’s `seed/config` read-only, swaps the fallbacks list in memory, prints the shared-order role list. Writes nothing.

## Tests

| repo | typecheck | tests |
|---|---|---|
| visual-novels-orchestrator | exit 0 | 88 files, 1149 passed |
| edu-game-studio | exit 0 | 91 files, 519 passed |
| scriptorium | exit 0 | 58 files, 720 passed + test:recovery 1 passed |
| book-translator | exit 0 | 25 files, 364 passed |
| pixel-art-generator | exit 0 | 50 files, 530 passed |
| midi-generator | exit 0 | 79 files, 1186 passed |

## Acceptance criteria

| # | criterion | verdict | evidence |
|---|---|---|---|
| AC-1 VN | served DeepSeek gives family deepseek, extra_body none/low; switch to qwen3.8-flash-next-iq3_s gives qwen on the same objects; down keeps L and marks down; legacy -low ref; discovery adds no strata/<id> | PASS | `tests/models.test.ts:119-169` (legacy `toBe(low)` :154, model keys :158, `toBe(row)` :162, `down: true, served` :167); green |
| AC-1 Edu | same | PASS | `tests/models.test.ts:101-124`; its registry diff has the same +/- lines as VN |
| AC-1 Scriptorium | same (+ avoidFamily) | PASS | `tests/models.test.ts:112-163` |
| AC-1 BT | same (+ kept across reload) | PASS | `tests/registry.test.ts:357-398` (:375-377, :384-394) |
| AC-1 Pixel | same + `loaded` row survives `dropMissing`, tools/vision from profile | PASS (documented deviation: no provider-down state; `concurrency: 1` and L kept instead) | `tests/llm/registry.test.ts:202-240` (listModels :218, legacy :224, switch :228-232, down + reload :235-239) |
| AC-1 Chiptune | same as Pixel | PASS (same deviation) | `tests/llm/registry.test.ts:190-260` identical to Pixel; llm +/- diffs identical |
| AC-2 all six | seed configs load, every role resolves | PASS | existing seed-config tests in the green suites (Scriptorium `models.test.ts:42`, VN/Edu `models.test.ts:47`, BT `registry.test.ts:14`, Pixel/Chiptune `registry.test.ts:46`) |
| AC-3 VN | migration once, keeps own row, deleted provider untouched | PASS | `tests/seed-migrations.test.ts:154-190` (rows :180, profiles :182, roles/settings renamed :183-184) |
| AC-3 Edu | same | PASS | `tests/seed-migrations.test.ts:169` |
| AC-3 Scriptorium | same (+ last_resort_model, CRLF, comments) | PASS | `tests/migrations.test.ts:341-387` (second run and removed row change nothing :381-383, no strata :386) |
| AC-3 BT | same + `concurrency: 1` becomes `auto` | PASS | `tests/dataFolder.test.ts:167-215` (`concurrency: "auto"` :203, once :212) |
| AC-3 Pixel | same + models.md `shown`, app.json `selectedModel` | PASS | `tests/llm/customProviders.test.ts:214-245` (shown :230, app.json :231), deleted provider :240 |
| AC-3 Chiptune | same | PASS | `tests/llm/customProviders.test.ts:118,144` |
| AC-4 | typecheck + full suite per repo | PASS | table above |
| AC-5 | no stale Strata text | PASS | `grep -rn "run-iq2_xs\|coder-iq1_m\|84 GB\|Qwen3.8-Flash-Next server\|server for Qwen3.8"` over the six `seed/config` + `creative-hub/README.md` + `services.json`: no hit (grep exit 1). `48 GB` also absent. |
| AC-H1a | `hub.ps1 start strata nope` throws with the variant list, starts nothing | PASS | exit 1, `Unknown variant "nope" for "strata". Variants: iq3_s, iq3_s-solo, iq3_s-parallel, iq4_xs, deepseek, deepseek-coder (default: iq3_s). Services: …`; port 8080 not listening before or after. The throw is in `Select-Services` (`hub.ps1:54`), which the `foreach` at `:297` evaluates in full before any `Start-Service1`. |
| AC-H1b | `start strata` with Strata up prints "already up" | UNCHECKED | Strata not running. Code: the port check is the first line of `Start-Service1` (`hub.ps1:128`), before the variant block (`:134-140`). |
| AC-H2 | `start strata deepseek` opens the DeepSeek console; status shows the model | UNCHECKED (live, L1) | code: variant path `hub.ps1:134-140`, `Get-HealthModel` `:75-81`, `Model` column `:94`; all six `D:\Strata\run-*.bat` exist |
| AC-L1 | DeepSeek accepts every tool request | UNCHECKED (live, L2) | `scripts/strata-probe.mjs` passes `node --check`; covers /health, /v1/status, /v1/models, (a)-(d) required, (e) informational |
| AC-L2 | apps show the real model and survive a switch | UNCHECKED (live, L3-L5) | labels typechecked only (VN/Edu `ModelsPage.tsx:23-36`, Scriptorium `ModelsDialog.tsx:24-37`, `StatusBar.tsx:32`, BT `ModelSelect.tsx:4`, Pixel/Chiptune `src/main/llm.ts:78-82`) |
| hub T7 | services.json variants + defaultVariant, start kept; README, SKILL, ROADMAP row 20 | PASS | services.json parses; 6 `variants`, `defaultVariant: iq3_s`, `start.path` `run-iq3_s.bat` (`services.json:150-156`); README `:44`; SKILL `:159`; ROADMAP row 20 |
| per-repo roadmap row + ticket plan | | PASS | each tool `ROADMAP.md` names its ticket; `.claude/tickets/<ID>-strata-model-discovery/{plan,changelog}.md` tracked in all six |

## Seams (C1 the same everywhere)

| seam | verdict | evidence / difference |
|---|---|---|
| Seed `strata` block (C1.1) | PASS | The `strata` blocks of all six `seed/config/providers.md` match key for key: rows `default`/`default-low`, `loaded: true`, aliases `[qwen3.8-flash-next(-low)]`, `context: 131072`, `discover: true`, `json_schema: false`, `concurrency: auto`, profiles `qwen3.8-flash-next` (qwen, 131072) and `deepseek-v4.1-flash` (deepseek, 131072). Only comments differ (BT "optional;" and "its /status"; Pixel/Chiptune json_schema comment). Pixel/Chiptune add `tools: true` per row, as C1.1 says. |
| extra_body per row | PASS | `{ reasoning_effort: none }` on `default`, `{ reasoning_effort: low }` on `default-low`: in all six seeds and in all migration constants (VN/Edu `seedMigrations.ts` `STRATA_LOADED_ROWS`, Scriptorium `migrations.ts:558-561`, BT `migrate.ts` same constants; Pixel/Chiptune clone the seed rows). No profile has `extra_body` (L2 may add one for DeepSeek). |
| Resolution (rules 1-11) | PASS | VN and Edu registry diffs have the same +/- lines; Pixel and Chiptune llm diffs too. Scriptorium and BT carry the same `profileFor`/`setServed`/`applyServed`. Every router passes the per-model json_schema (`jsonSchema: model.jsonSchema`), and every `openaiCompat.ts` uses `req.jsonSchema ?? this.opts.jsonSchema`. All six log `now serves <L> (was <old>)`. |
| Neutral refs (C1.3) | PASS | No `strata/qwen3.8-flash-next` is left in any `src` outside migrations and comments. The seeds use `strata/default(-low)` or the alias: BT `defaults.json:3-11`, VN `roles.md:17` and `settings.md:5`, Edu `roles.md` and `settings.md`, Pixel/Chiptune `roles.md` (`strata` and `strata-low`). |
| Migration id | PASS (documented forms) | VN/Edu: three `SEED_MIGRATIONS` entries, `strata-loaded-v1`, `strata-loaded-roles-v1` and `strata-loaded-settings-v1`, one file each (documented). Scriptorium: `migrateStrataLoaded` without an id, idempotent by its condition (the plan allows "no id list"; documented). BT: a function that records `strata-loaded-v1` in `config/seed-state.json` `migrations` (documented). Pixel/Chiptune: `strata-loaded-v1` in `seed-state.json`. |
| Ref rename rules | PASS | Exact strings, `-low` first. VN/Edu/Scriptorium: every YAML scalar of `roles.md` and `settings.md`, so `last_resort_model` too. BT: quoted-string replace over all of `defaults.json` (agentModels, fallbacks, groupDefaults). Pixel/Chiptune: a bounded regex in `roles.md` and `models.md`, and `app.json` `selectedModel` (`seedMigration.ts:226-234`). |
| Never re-add what the user removed | PASS | VN/Edu/BT/Pixel/Chiptune: the id is recorded. Scriptorium: it acts only while an old row is there and no `loaded` row is (`migrations.ts:612-614`); its rename runs at every start but only renames. |

Differences, judged:

1. Scriptorium adds the loaded rows only while an old row is present; VN/Edu/BT/Pixel add them whenever there is no `loaded` row. Documented, and justified: Scriptorium has no id record.
2. Pixel/Chiptune add the seed `profiles` only when the user has no `profiles` key; VN/Edu/Scriptorium/BT add each missing profile id. Not documented. Harmless: no file from before HUB-26 has `profiles`.
3. BT turns a numeric `concurrency` into `auto` even when loaded rows exist. Documented.
4. Pixel/Chiptune have no provider-down state and log with `console.info` instead of sending an event. Documented.
5. Pixel/Chiptune `discover()` returns `found: 1` for Strata; the engine repos return `found: 0` with `served`. Cosmetic, not documented.
6. The Pixel/Chiptune migration renames the `strata` alias but does not add `strata-low` to a user `roles.md`. C1.4 does not ask for it, and no role uses it.

## resolve() gap (from the Scriptorium worker’s report)

Confirmed in the VN, Edu and BT code. Low severity.

- **Code.** VN `registry.ts:597-599`, Edu `:600-602` and BT `:663-666` pass an alias’s fallback row through unchanged. So with `fallbacks: [..., strata/qwen3.8-flash-next, ...]`, `resolve("strata")` returns the old ref. Scriptorium `registry.ts:603-606` maps it to `strata/default`, and so does Pixel/Chiptune `resolve` (`registry.ts:592-594`).
- **Repro** (in memory; seed roles; `fallback_shared: true`; role director `[paid, strata, lmstudio]`):
  - VN and Edu `roleModelRefs`: `["deepseek/deepseek-flash","strata/default","lmstudio/…","strata/default"]`.
  - BT `orderRefs`: `[…,"strata/default","lmstudio/…","strata/qwen3.8-flash-next"]`.
  - Scriptorium: the same list without the duplicate.
- **Effect: none on routing.** The router dedups after resolving: VN/Edu `router.ts:111-117` (`seen` on the resolved refs), BT `router.ts:96-99` (resolves, then dedups). A job gets Strata once. The duplicate shows only in the raw role list, and `roleDefaults` reads only `[0]` (VN/Edu `summary.ts:88-95`).
- **When it can happen after the migrations:** only when the fallbacks list names the old ref while providers.md already has the `loaded` rows:
  - The user types the old ref by hand into `settings.md` (VN/Edu) or `defaults.json` (BT) after the migration ran.
  - In VN/Edu, only `config/settings.md` is restored from a backup (for example `creative-hub/.claude/temp/HUB-26-backup/`). The migration id stays recorded in `<data>/.seed-hashes.json`, which is outside `config/`, so the rename does not run again.
- **When it cannot happen:**
  - A restore of the whole `config/` in VN/Edu: the old real rows come back with the old refs, so they are consistent and there is no gap. BT keeps its state in `config/seed-state.json`, so a whole-config restore makes the migration run again.
  - Project, job and history files (BT `project.json` ×48, VN `jobs/done`): they name concrete refs. Those resolve through `aliasRefs`, and a concrete ref takes the place of the row of its kind in the shared order.
  - The old `settings-fallbacks-v1` (VN/Edu `seedMigrations.ts:130-149`): it runs earlier in the same list, so the rename sees what it wrote.
  - A missing or unparseable file: it is skipped and not recorded, so the migration runs again at the next start.
- **Suggestion (not done):** port the two-line Scriptorium `resolve` to VN, Edu and BT so all four match.

## Other findings

- LOW, doc: `midi-generator/seed/config/providers.md:256` says "**Pixel Studio** asks it which one it runs …" in the Chiptune Studio seed (left over from the replay). It should say Chiptune Studio.
- INFO: `Show-Status` in `hub.ps1` now calls `Get-HealthModel` (3 s timeout) for every listening service with `http`, not only Strata (`hub.ps1:94`). Harmless, but a slow service makes `status` slower.
- Pending by plan (not code): T8 user data. The Scriptorium `settings.md` still needs `strata/default` added by hand. Each app migrates its own folder at its next start; Scriptorium only through the CLI probe, with the user’s yes.

## Stray / untracked files

- `visual-novels-orchestrator/.claude/tickets/VNO-60-strata-model-discovery/replay-bundle.md`: the known replay scratch file.
- `pixel-art-generator/.claude/tickets/PAR-17-strata-model-discovery/replay-bundle.md`: the same kind of file, not in the brief.
- `creative-hub/.claude/tickets/strata-model-audit/research-{A,B,C}.md`: the REQ-0015 audit, untracked.
- No other untracked or modified files in the seven repos after the test runs.

## Not covered by any piece

These are live or user steps by plan:
- The live DeepSeek check of request item 2 (L2).
- T8 user-data migration, including the manual Scriptorium fallback row (request item 4, first part).
- AC-H2, AC-L1 and AC-L2.

## Changed but not asked for

All documented in the changelogs:
- VN/Edu/Scriptorium/BT: extra summary fields `thinking` and `followsServer`, and a `served` field on the spend event.
- BT: the `engine models` CLI shows `served` (`cli.ts:33`), and `contextLength` resolves legacy refs.
- Pixel/Chiptune: `syncServerSlots` also polls a non-`auto` provider that has loaded rows.

## Extra ideas from the pieces

None recorded: the REQ-0016 "Extra ideas" section is empty, and none of the six changelogs has an `Extra ideas:` line.
