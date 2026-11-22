# HUB-40 extra ideas: live steps

Date: 2026-11-22. Plan: `.claude/tickets/HUB-40-extra-ideas/plan.md`. The user approved "Yes, both" to: rebuild VN, Edu and Cartoon Studio, and sync the live `roles.md` prose. Nothing was started or stopped: `hub.ps1 status` showed vn-studio, edu-studio and cartoon-studio down before the build. No model was called. Nothing committed.

## Builds (`pwsh -File scripts\hub.ps1 build vn-studio edu-studio cartoon-studio`, runs `fnm exec --using=24 cmd /c yarn build:engine` per repo)

Exit code 0, about 11 s in total, log `.claude/temp/hub40-build.log`. Repo heads checked on master before the build: visual-novels-orchestrator 2b6906b, edu-game-studio e7854ff, cartoon-studio 2f08645. The build did not launch any app.

| app | result | `out/engine/index.js` written |
|---|---|---|
| vn-studio | OK (a vite "dynamic import will not move module" warning for `src/shared/puzzle.ts`, no error) | 2026-11-22 13:27:00 |
| edu-studio | OK | 2026-11-22 13:27:05 |
| cartoon-studio | OK (the same kind of warning for `src/engine/images/comfy.ts`) | 2026-11-22 13:27:08 |

## L1: live `roles.md` prose

Files are LF with no BOM (before and after). Written by `.claude/temp/hub40-live/sync.cjs` (reads and writes bytes as UTF-8, replaces whole lines found by their text with the matching seed line). Backups, made before the edit with `cp -p`; the `.bak-HUB-38` and `.bak-HUB-39` files are untouched:
- `C:\Users\Infplane\VisualNovels\config\roles.md.bak-HUB-40`
- `C:\Users\Infplane\EduGames\config\roles.md.bak-HUB-40`

| place | result |
|---|---|
| VN: "The aliases `paid`, `strata` and `lmstudio`" paragraph (file line 25) | changed to the seed paragraph |
| Edu: aliases paragraph (line 51) | changed |
| Edu: `researcher` bullet (line 56) | changed |
| Edu: "Writers and designers" (77), "Researcher and fact-checker" (78), "Other reviewers and the playtester" (79), "After a role's ..." (80) | changed |
| Cartoon | nothing (as planned) |

Every place matched one-to-one; the live text differed from the seed only in the stale Strata / LM Studio wording, so nothing was skipped.

Verification:
- `git diff --no-index <file>.bak-HUB-40 <file>`: VN `@@ -25 +25 @@` (1 line); Edu `@@ -51 +51 @@`, `@@ -56 +56 @@`, `@@ -77,4 +77,4 @@` (6 lines). Nothing else.
- Front matter (up to and including the second `---`): VN lines 1-20, sha256 prefix a4a16d3bbf0bc440 before and after; Edu lines 1-46, b721e4f4da8a6134 before and after. Identical.
- Sizes: VN 2658 -> 2980 bytes, Edu 8297 -> 8368 bytes. CR bytes 0, first bytes `---` (unchanged).
- Prose diff against the seeds (after the second `---`): no difference for VN and for Edu.
- Not done: the apps were not restarted (they were not running); L1 is UNTESTED in the real app.

## Still open

- L2 (prompt refresh check, needs the apps started): compare the live prompts with the new seeds (VN `art-critic/review_image.md`, Edu `art-critic/review.md`, Cartoon `frame-critic/clip-review.md`, `frames.md`, `frames-3d.md`); copy over after a `.bak-HUB-40` only if the app lists "update available".
- N1: VN sprite review on Inkling in `hub39-critic-check` (`sprite_mara_neutral`); passes if no grey-background rejection and the `problems` are English (GPU, user's go-ahead).
- N2: Scriptorium re-index with `npm run engine -- reindex --data C:\Users\Infplane\Scriptorium`, Scriptorium closed, embedding server on; deleting `index\library.sqlite` for a full re-embed is a second decision for the user.
- N3: Strata thinking without `reasoning_effort`: two curl calls to the proxy (with and without `reasoning_effort: none`), compare `reasoning_content` and `completion_tokens` (GPU, may switch the proxy model).
- N4: Pixel MCP for the artist agent (idea 16) and Pixel's vision rows (idea 32): the user decides whether to plan them.

## Live checks 2026-11-22

User go-ahead "Yes, run checks" (start the proxy, ComfyUI and VN Studio; run the sprite re-review and the Strata check). Worker session, 13:30-13:39 +01:00. Only local models through the proxy were called (Inkling, Strata). No paid or cloud model, no Flow, no ElevenLabs, no Gemini. Nothing committed; no repo code, seed or config changed.

### Preflight (13:30-13:31)

- `hub.ps1 status` before: only vibetts up; acp-proxy, comfyui, vn-studio, strata (8080) down; 8082 down (no local model loaded).
- Started by this session: `hub.ps1 start acp-proxy comfyui vn-studio` -> acp-proxy pid 29216 (status shows electron 26412), comfyui (python 17472), vn-studio (node 2248). All three answered.
- `/healthz`: status ok, all providers active 0 / queued 0. The proxy needs no API key (requests without one answered).
- `/v1/models` lists `llama/inkling-2-mini` (vision true), `llama/inkling-2-mini-dspark`, `llama/nomic-embed-text-v1.5`, `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`.
- ComfyUI 0.45.0, `/system_stats` vram_total 107,090,132,992, vram_free 106,757,337,088 (nothing loaded).

### L2 (VN only)

- Live `C:\Users\Infplane\VisualNovels\prompts\art-critic\review_image.md` (written 13:30:51, at VN Studio start) equals the seed `visual-novels-orchestrator\seed\prompts\art-critic\review_image.md` (repo 2b6906b), byte for byte after CR strip (both have no CR, 1469 bytes). It contains "flat mid-grey backing that is not part of the picture" (line 19) and "Write `problems` and `revisedPrompt` in English." (line 23). Seed refresh worked: PASS. No hand copy, no `.bak-HUB-40` needed.
- Read-only: `VisualNovels\config\providers.md` lines 209-218: both Inkling rows still have `extra_body: { chat_template_kwargs: { reasoning_effort: none } }`. `roles.md` front matter: `art-critic: models: [paid, acp/llama/inkling-2-mini]` (`paid` = deepseek/deepseek-flash, no `vision`, so the vision-only routing skips it; no DeepSeek call happened, see spend).
- Edu and Cartoon prompts: not checked (their apps were not started).

### N1 VN sprite re-review on Inkling

- Project `hub39-critic-check`, asset `sprite_mara_neutral` (prompt unchanged since K2 attempt 3, `promptByHand`, ref `sheet_mara`). `vno_asset_generate {only: [sprite_mara_neutral], force: true}` (force needed: the asset already had files) -> job `hub39-critic-check--vn.assets.generate--all--r2`.
- `hub39-critic-check--vn.assets.generate--sprite_mara_neutral--r2`: 13:31:50-13:34:59, 189.8 s, qwen-image-2.1-edit, background removed, `v4.webp`. No model call. No ComfyUI error.
- `hub39-critic-check--vn.assets.review--sprite_mara_neutral--r2`: 13:34:59-13:36:10, model `acp/llama/inkling-2-mini` (cold load of Inkling included), prompt version d04d05b3 (job file 4057bd7c), tokens 1165 in / 393 out, 70.7 s. Verdict `{"approved": true, "problems": [], "revisedPrompt": null}`. One review, no retry.
- Spend row `VisualNovels\logs\spend\2026-11.md` 2026-11-22T13:36:10: art-critic-default, acp, llama/inkling-2-mini, 1165/393, 0 USD. The only VN model call today.
- My own look at `v4.webp`: single full-body Mara, red short hair with hair clip, green hooded raincoat, black socks, brown buckled boots, clean transparent cut-out, no text or border, same character as `sheet_mara/v1.png`. Approval is right.
- ComfyUI lowest vram_free 87,179,585,536 (13:33:01, edit model loaded while generating); 105,538,440,704 after the job. No ComfyUI error.
- N1: PASS (no grey-background rejection). The "notes in English" half is not exercised: the approval has no problems and no revised prompt.

### N3 Strata thinking without `reasoning_effort`

| call | time | HTTP | seconds | reasoning_content | completion_tokens | reasoning_tokens | prompt_tokens | answer |
|---|---|---|---|---|---|---|---|---|
| without `reasoning_effort` | 13:36:55 | 200 | 68.08 (includes the Llama -> Strata switch) | present, 108 chars ("We need to respond to user ... final answer OK.") | 32 | 27 | 58 | "OK" |
| with `"reasoning_effort":"none"` | 13:38:03 | 200 | 0.30 | absent | 2 | 0 | 18 | "OK" |

- Finding: yes, Strata thinks by default when a caller omits `reasoning_effort` (27 reasoning tokens for a one-word answer; none with `none`).
- Seeds (read-only): every `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` row under `acp` in the seed `providers.md` of scriptorium, book-translator, visual-novels-orchestrator, edu-game-studio, cartoon-studio, pixel-art-generator and midi-generator has `extra_body: { reasoning_effort: none }`; the disabled direct `strata` providers have `default` (none) and `default-low` (low, for checks, on purpose). The live `providers.md` of all seven data folders (BookTranslator, CartoonStudio, ChiptuneStudio, EduGames, PixelStudio, Scriptorium, VisualNovels) also have it on their one Strata row. No caller without it found in the seeds; the code refs (Scriptorium `cli.ts:26` default ref, Book Translator `defaults.json`) resolve to those rows. Inferred, not traced in each app's request code. No follow-up opened.

### End state (13:39)

- `POST http://127.0.0.1:8188/free {"unload_models":true,"free_memory":true}` -> HTTP 200; queue empty; vram_free 106,009,006,080.
- Strata is the loaded local model: 8080 health 200 (hub.ps1: strata pid 13608, qwen3.8-flash-next-unsloth-ud-iq4_xs); 8082 down; 8083 (embeddings) down.
- `/healthz` status ok, every provider active 0 / queued 0.
- Left running: acp-proxy 8787, comfyui 8188, vn-studio 7459 (started by this session), strata 8080 (started by the proxy), vibetts (was up). No queue was paused.
- Throwaway project kept: `C:\Users\Infplane\VisualNovels\projects\hub39-critic-check` (sprite now at v4, selected, approved).

### UNTESTED

- English notes from the VN critic on a rejection (no rejection happened).
- L2 for Edu `art-critic/review.md` and Cartoon `frame-critic/*.md` (apps not started).
- One sample only: whether Inkling still sometimes rejects the grey backing over several sprites.

## N2 Scriptorium re-index 2026-11-22

Plain `reindex` (the user approved: "scriptorium ok recommendation"; the full delete-and-rebuild was not done).

- Code check: `src/engine/cli.ts:78-91` `reindexLibrary` only loads the registry, `MemoryService.reindexAll()` (`memory/service.ts:33`) -> `reindex()` (`memory/index.ts:316-333`: collects markdown files, `upsert` skips files whose hash is unchanged, chunks and embeds the new ones, removes rows of vanished files). `index.ts:48-51` dispatches it before the engine lock, scheduler, MCP server and job queue. No chat model call.
- Config: `roles.md` `embeddings: acp/llama/nomic-embed-text-v1.5`; `providers.md` `acp` `base_url: http://127.0.0.1:8787/v1`. Scriptorium was down (hub.ps1 status; no Scriptorium process; `index/engine.lock` pid 19260 is stale, not running). Probe `POST /v1/embeddings` returned a 768-long vector.
- Build: `yarn build:engine` (part of `npm run engine`), from `C:\projects\Personal\scriptorium` on master 8cec567, tree clean before and after. A first attempt with backslashes in `--data` failed on a bad path (ENOENT, nothing written); the second used `C:/Users/Infplane/Scriptorium`.
- Backup: `C:\Users\Infplane\Scriptorium\index\library.sqlite.bak-HUB-40` (50,438,144 bytes; no -wal/-shm existed).
- Time: about 20 s including the build. Log: `.claude\temp\hub40-reindex\reindex.log`. Exit 0, no failing files.

| | files | chunks | chunks > 1800 chars | chunks with no letter/digit | longest chunk | size |
|---|---|---|---|---|---|---|
| before | 1448 | 6720 | 0 | 55 | 1790 | 50,438,144 |
| after | 1449 | 6707 | 0 | 55 | 1790 | 50,610,176 |

- Embedded 35 files, 1414 unchanged (skipped), 0 removed, 0 failed. dim 768.
- The 55 no-letter/digit chunks are all still there: they sit in unchanged files that keep their old chunks. Only the full rebuild (delete `library.sqlite`) would remove them; the user decides that if search results look off.
- End state: proxy `/healthz` ok, every provider active 0 / queued 0; Strata 8080 answers (qwen3.8-flash-next-unsloth-ud-iq4_xs); nothing started; Scriptorium still down. Nothing committed.


## Throwaway check data deleted 2026-11-22

The user said the throwaway HUB-39 check copies can go ("we do not need test copies"). Deleted exactly three:

- VN Studio project `hub39-critic-check` (18 files, 7.5 MB): through the running app (`vno_delete_project`, after `vno_status` showed 0 queued and 0 running jobs).
- Edu Studio course copy `C:\Users\Infplane\EduGames\courses\hub39-critic-check` (145 files, 47.5 MB): `Remove-Item -LiteralPath ... -Recurse -Force`; port 7463 was closed. No reparse points inside.
- Cartoon Studio series copy `C:\Users\Infplane\CartoonStudio\series\hub39-critic-check` (265 files, 81.0 MB): same way; port 7465 was closed. No reparse points inside.

Originals untouched (file count and bytes, before and after): Edu `suncev-sustav` 149 files / 47,395,092 bytes both times; Cartoon `pilot` 264 files / 81,030,809 bytes both times.

No data-folder index file listed the copies. The run logs and ticket records still mention the name as history, and no `.bak-HUB-*` file was touched.
