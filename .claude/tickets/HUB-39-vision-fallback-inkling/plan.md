---
status: done
request: REQ-0030
repos: [creative-hub, visual-novels-orchestrator, edu-game-studio, cartoon-studio]
branch: HUB-39_vision-fallback-inkling
updated: 2026-11-22
---

# HUB-39 Vision fallback: the critics get Inkling through the ACP proxy in place of LM Studio

Follow-up to HUB-38 (`.claude/tickets/HUB-38-acp-for-all/plan.md`, its "Vision roles that stay" table). The user approved this scope (2026-11-21): the local entry of three vision critics becomes `acp/llama/inkling-2-mini` (ACP proxy, `http://127.0.0.1:8787/v1`) in place of `lmstudio`. LM Studio is not installed on this PC. The entry before it in each list stays as it is.

| app | role | today | after |
|---|---|---|---|
| VN Studio | `art-critic` | `[paid, lmstudio]` | `[paid, acp/llama/inkling-2-mini]` |
| Edu Studio | `art-critic` | `[gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, lmstudio]` | `[gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, acp/llama/inkling-2-mini]` |
| Cartoon Studio | `frame-critic` | `[client/claude-code, lmstudio]` | `[client/claude-code, acp/llama/inkling-2-mini]` |

Reading built: the narrow one the user approved. Seed, prose, the critic's token cap and tests in the three repos; the live config of the three data folders by the hub; one live review through each app. No proxy change, no new guard code.

## What the code says (answers to the planning questions; where I looked)

**Today the `lmstudio` entry gives none of the three critics a model.** The alias resolves to the `lmstudio` row of `fallbacks` in `config/settings.md`, a text model: VN `lmstudio/gemma-4-e4b-it-ultra-uncensored-heretic`, Edu and Cartoon `lmstudio/gemma-4-e4b-it`. None has `vision: true`, so the vision filter (`router.ts:118` in all three) drops it. The VN seed test says it outright (`visual-novels-orchestrator/tests/models.test.ts:81`: the art-critic resolves to `deepseek/deepseek-flash` and that gemma row, neither a vision model). So this ticket does not swap one working fallback for another. It gives the critics their first working local model.

1. **Nested `extra_body`: works in all three, nothing to change.** The schema is `z.record(z.string(), z.unknown())` (`src/shared/schemas.ts:39` VN and Edu, `:41` Cartoon). The registry copies `m.extra_body` as it is (`registry.ts:241/278` VN, `:244/281` Edu and Cartoon). The router passes it (`router.ts:184`), and `openaiCompat.ts:65-71` spreads it into the body at the top level, so `chat_template_kwargs` goes out as a nested object. In YAML, `none` is a string. One catch: `body.max_tokens` is set after the spread (`openaiCompat.ts:72`), so an `extra_body.max_tokens` is overwritten by the call's own cap. It cannot carry the token limit.
2. **Token cap and timeout.** The cap is set per call, in the critic code: VN `src/engine/vn/agents/art-critic.ts:45` `maxTokens: 1200`, Edu `src/engine/edu/media.ts:516` `maxTokens: 1500`, Cartoon none (`pipeline/tasks.ts:289` passes `maxTokens` only when the task gives one, and the frame-critic tasks never do, so no `max_tokens` is sent). No per-model row field raises a call's cap: `max_output` is only a ceiling used for the cost estimate (`budget/spend.ts:117`). The smallest change is the constant: VN 1200 to 2000, Edu 1500 to 2000. This is harmless for cloud models: it is a ceiling; Gemini 2.5 Flash, Edu's first choice, counts its thinking inside it, so it gains; and the budget reserve grows by under $0.002 per call. Cartoon stays uncapped; its live check records the tokens used. The timeout is per provider client, 15 minutes by default (`openaiCompat.ts:77`), and none of the three sets another (`registry.ts:377-386` VN, `:380` Edu and Cartoon). The proxy's own limit is 900 s. That is at least 5 minutes, so nothing to change.
3. **Images: always JPEG, never webp.** Each app converts with sharp. VN `art-critic.ts:22-25`: JPEG q85, at most 1024 px, 1 image, or 2 for a sprite (its sheet first, `:50-51`). Edu `media.ts:502`: JPEG q82, at most 768 px, always 1 image. Cartoon `pipeline/tasks.ts:220-223`: JPEG q86, at most 1568 px, 1 contact sheet (12 frames, or 6 for a clip) plus one sheet per cast member in the shot (`handlers.ts:595,603`, `media.ts:59`), so often 3 to 6 images. Untested and covered by live checks: 2 images (VN, check K2), 768 px with Edu's larger answer (K3), and 3 or more images at 1568 px, which may come close to Inkling's 32768 context (K4).
4. **GPU contention: a real risk, documented and checked, no guard code.** The guard (`studios/autostart.ts:335-342`, the same lines in all three) only refuses to start ComfyUI while Strata answers on 8080. When the critic runs, ComfyUI is already up because it just made the image, so the guard never acts here, and adding 8082 would not change that. It stays the existing HUB-38 follow-up idea. What actually happens:
   - VN queues a review job right after each generate job (`handlers.ts:542-561`). The scheduler can run the next generate job (a sprite after its sheet) at the same time as the review of the previous one, so ComfyUI's image model and Inkling sit in GPU memory together.
   - Edu reviews after all pictures are made (`edu/pipeline.ts:608-613`), then makes the revised pictures with ComfyUI while Inkling is still loaded (the proxy does not unload an idle model, and that is out of scope).
   - ComfyUI's `freeBeforeDispatch` (false in all live `comfy.md`) frees ComfyUI's own cache before a job. It does not lower the peak with Inkling resident.

   The handling: say it in the hub docs and seeds (the hub rule "no ComfyUI while a local model is loaded" now has a known exception), and measure it in K2 and K3 (`/system_stats` VRAM, ComfyUI errors). If image jobs fail, open a follow-up (a proxy idle unload, or freeing ComfyUI before a local review). Decision D2.
5. **When the fallback fires, and the cost.** The router moves to the next model on a non-retryable error, after 2 retries of a 429, 5xx or timeout, on a daily-limit 429, a context error or a budget refusal (`router.ts:145-238`). The scheduler waits for a busy provider rather than switch (`scheduler.ts:352-357`).
   - **VN: Inkling is not a fallback, it is the only vision model.** `paid` is `deepseek/deepseek-flash`, which has no vision, so the filter drops it. Every review runs on Inkling unless a project sets `models.art-critic` (three projects set `client/claude-code`). Review is off by default (`src/shared/vn.ts:335`), and all 20 live projects have `art.review: false`. A project that turns it on costs about 2 minutes per image, up to 3 tries per image (`REVIEW_RETRIES = 2`, `handlers.ts:64`). Each review job holds an `acp` slot, and the critic agent has `max_parallel: 1`, so reviews run one at a time.
   - **Edu: the same, and the review is on by default.** No `GEMINI_API_KEY` or `ANTHROPIC_API_KEY` exists on this PC (user and machine environment, and the credential store targets: checked), so both cloud entries are unavailable and Inkling is the first model used. `media.art.review` defaults to true (`src/shared/media.ts:111`). So every Edu course with pictures, unless its `course.md` `models` names a model for the art-critic (or `*`), reviews every picture on Inkling, one after another, for up to 2 rounds (`max_rounds: 2`). `suncev-sustav` has 20 pictures: about 35 to 40 minutes per round, plus a GPU switch (about 20 s) and the switch back to Strata (about 55 s) on the next local text request. This is the cost the user must accept (D1). `suncev-sustav` itself is not affected: its `models: "*": client/claude-code` sends the critic to the client.
   - **Cartoon: never fires on its own.** `client/claude-code` is always available (`registry.ts:356-360`) and its request waits until a client answers (`models/client.ts`: no timeout, only an abort). The scheduler waits rather than switch. Inkling is reached only when the user puts it first (the agent's `model`, the Models page) or switches the client provider off.
   - No path makes the fallback fire once per asset after a cloud failure, because in VN and Edu no cloud vision model is usable to begin with.
6. **Live config: a seed change does not reach an existing folder.** Seed config is copied only into a new folder. The seed migrations (`src/engine/store/seedMigrations.ts`) are one-time id'd edits, and HUB-38 used one only for the port. As in HUB-38, the hub edits the three live folders after the repo tickets merge (L1-L3, `*.bak-HUB-39` backups). No repo gets a migration.
7. **Cartoon `frame-critic`.** The second entry is reached only as described in 5. Its prompts (`prompts/frame-critic/clip-review.md`, `frames.md`, `frames-3d.md`) and its answer (`review` schema: `verdict`, four `scores`, `notes`, `problems`) differ from VN's, and it sends several images, so it needs its own live check (K4). The check forces Inkling with the agent's `model` (backed up, then restored), because the role list can never reach it while the client is on.

## Scope

1. Three repo tickets (VNO-68, EGS-72, CTS-55):
   - seed `config/providers.md`: the two Inkling rows get the `extra_body` of contract V1;
   - seed `config/roles.md`: the critic list of V2, and its prose;
   - the critic's token cap of V3 (VN, Edu);
   - the existing seed tests updated;
   - ROADMAP row.
2. Hub code (this branch):
   - `CLAUDE.md` line 11;
   - `services.json` `lmstudio` note;
   - `README.md` line 76;
   - `.claude/skills/make-visual-novel/SKILL.md` and `.agents/skills/make-visual-novel/SKILL.md` line 163;
   - `ROADMAP.md` row 32.
3. Live data L0-L3 (the hub, after the three repo tickets are merged and the user approves).
4. Live checks K0-K5 (GPU, user's go-ahead).

## Out of scope

- Pixel Studio's vision rows, Scriptorium, Book Translator, Chiptune Studio.
- Any proxy code or proxy setting (`settings.json` stays: 900 s, llama `maxConcurrent: 1`).
- Removing LM Studio code, the `lmstudio` provider rows, or the `lmstudio/gemma…` row of `fallbacks` (it stays the target of the `lmstudio` alias, which no role names any more).
- A cloud vision model first for VN or Edu (D1 alternative only), changing `art.review` or `media.art.review` defaults.
- The autostart ComfyUI-versus-local-LLM guard (8081, 8082): stays the HUB-38 follow-up idea (answer 4).
- Unloading Inkling after a review, freeing ComfyUI before a review (follow-up only if K2 or K3 fail on memory).
- `llama/inkling-2-mini-dspark` as any default (it needs another llama.cpp build).
- A per-model token-cap field in the model layer.

## Contracts (single source; the repo plans copy them verbatim)

### V1 The Inkling rows of the `acp` provider (seed and live, all three apps)

The two existing rows, in place, with one key added each (no other key changes; dspark gets it too so a hand pick of it does not think at length, it stays no default):

```yaml
      - id: llama/inkling-2-mini
        family: inkling
        context: 32768
        vision: true
        extra_body: { chat_template_kwargs: { reasoning_effort: none } }
      - id: llama/inkling-2-mini-dspark
        family: inkling
        context: 32768
        vision: true
        extra_body: { chat_template_kwargs: { reasoning_effort: none } }
```

Why this key: `chat_template_kwargs` is the only field that reaches Inkling's chat template (the proxy forwards it since AAP-42). Top-level `reasoning_effort` or `enable_thinking` have no effect on Inkling. Thinking gets shorter but cannot be switched off.

### V2 The critic lists

- VN `config/roles.md`: `art-critic: models: [paid, acp/llama/inkling-2-mini]`
- Edu `config/roles.md`: `art-critic: models: [gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, acp/llama/inkling-2-mini]`
- Cartoon `config/roles.md`: `frame-critic: models: [client/claude-code, acp/llama/inkling-2-mini]`

Always the full ref, never the alias `acp`: that alias stands for LOCAL (the Strata text model, no vision). No other role names `lmstudio` or Inkling. The `fallbacks` of `config/settings.md` do not change.

### V3 Critic token cap and timeout

| app | call | cap today | cap after | request timeout |
|---|---|---|---|---|
| VN | `reviewImage`, `src/engine/vn/agents/art-critic.ts:45` | 1200 | 2000 (every model) | 15 min client default (`openaiCompat.ts:77`), unchanged |
| Edu | `reviewRound`, `src/engine/edu/media.ts:516` | 1500 | 2000 (every model) | 15 min, unchanged |
| Cartoon | `runRoleTask` for `frame-critic`, `src/engine/pipeline/tasks.ts:289` | none sent | none sent (unchanged) | 15 min, unchanged |

The measured range for VN's prompt is 586 to 1157 completion tokens, and 2000 was safe in 6 of 6 tests. The repair round (`pipeline/llm.ts` `chatJson`) uses the same cap and sends the images again.

### V4 Wording (seeds and hub docs say the same thing)

"The critic's local model is `acp/llama/inkling-2-mini` through the ACP proxy (HUB-39): about 2 minutes per review, thinking kept short with `chat_template_kwargs`, and the proxy switches the GPU from Strata to Inkling (about 20 s) and back (about 55 s). It shares GPU memory with ComfyUI's image model while a run makes pictures."

## Ticket map

Free ids, confirmed 2026-11-21:
- creative-hub: last ticket HUB-38 (ROADMAP row 31, `.claude/tickets`, no `HUB-39` branch).
- visual-novels-orchestrator: last VNO-67 (folders up to VNO-67, branches VNO-63 to VNO-67 including `VNO-65_elevenlabs-later` with no folder, no VNO-68 anywhere).
- edu-game-studio: last EGS-71 (ROADMAP has EGS-68 to EGS-71, no EGS-72 folder or branch).
- cartoon-studio: last CTS-54 (ROADMAP table, folder; no CTS-55).

All four repos are on master with a clean tree.

| id | repo | branch | one line | depends on |
|---|---|---|---|---|
| VNO-68 | visual-novels-orchestrator | `VNO-68_vision-fallback-inkling` | art-critic `[paid, acp/llama/inkling-2-mini]`, Inkling `extra_body`, cap 2000 | none |
| EGS-72 | edu-game-studio | `EGS-72_vision-fallback-inkling` | art-critic third entry Inkling, Inkling `extra_body`, cap 2000 | none |
| CTS-55 | cartoon-studio | `CTS-55_vision-fallback-inkling` | frame-critic `[client/claude-code, acp/llama/inkling-2-mini]`, Inkling `extra_body` | none |
| HUB-39 | creative-hub | `HUB-39_vision-fallback-inkling` | docs, ROADMAP; then L0-L3 and K0-K5 | L and K: the three repo tickets merged |

Repo plans:
- `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-68-vision-fallback-inkling\plan.md`
- `C:\projects\Personal\edu-game-studio\.claude\tickets\EGS-72-vision-fallback-inkling\plan.md`
- `C:\projects\Personal\cartoon-studio\.claude\tickets\CTS-55-vision-fallback-inkling\plan.md`

Order:
1. The three repo tickets and H1-H4, in parallel (no shared files).
2. After the merges and the user's approval: L0-L3.
3. K0-K5, each with the user's go-ahead.

## Hub tasks (branch `HUB-39_vision-fallback-inkling`)

Inputs are this plan and the files named below. The outputs are the edited files. Contract: the wording of V4, and the role lists of V2 as written.

- **H1 `CLAUDE.md` line 11.** Replace the sentence "LM Studio is not installed and nothing needs it; the vision roles that still name `lmstudio` have no local fallback until a vision model through the proxy is checked." with "LM Studio is not installed and nothing needs it. The VN and Edu art-critic and the Cartoon frame-critic use `acp/llama/inkling-2-mini` as their local model (HUB-39; about 2 minutes per review, and it shares GPU memory with ComfyUI); Pixel's vision rows still name `lmstudio` and have no local model." Nothing else in the file changes. This is the user's instruction file: the plan's approval covers only this edit.
- **H2 `services.json` `lmstudio.note` (line 158).** Replace "The vision roles that still name `lmstudio` (VN and Edu art-critic, Cartoon frame-critic, Pixel's vision rows) have no local fallback until a vision model through the proxy is checked." with "The VN and Edu art-critic and the Cartoon frame-critic use `acp/llama/inkling-2-mini` through acp-proxy (HUB-39); only Pixel's vision rows still name `lmstudio` and have no local model." Check that it is still valid JSON (`node -e "JSON.parse(require('fs').readFileSync('services.json','utf8'))"`).
- **H3 `README.md` line 76.** Append: "Exception (HUB-39): the art-critics of VN and Edu and Cartoon's frame-critic use `acp/llama/inkling-2-mini`, so while a run makes and reviews pictures, Inkling and ComfyUI's image model share the GPU; if ComfyUI runs out of memory, free it (`vno_comfy_free`, `edu_comfy_free`) or turn the review off for that run." Both copies of make-visual-novel `SKILL.md`, line 163: after "at the same time as image generation", add " (with `art.review` on, the art-critic runs Inkling through the proxy right after each image: free ComfyUI if it runs out of memory)". The two copies get the same text (HUB-37 rule).
- **H4 `ROADMAP.md`.** Row 32 after HUB-38: `| 32 | HUB-39 | Vision fallback: VN and Edu art-critic and Cartoon frame-critic get \`acp/llama/inkling-2-mini\` (thinking kept short with \`chat_template_kwargs\`) in place of the unusable \`lmstudio\` entry; critic cap 2000 tokens (.claude/tickets/HUB-39-vision-fallback-inkling/plan.md, REQ-0030) | visual-novels-orchestrator (VNO-68), edu-game-studio (EGS-72), cartoon-studio (CTS-55), hub | GPU checks with the user's go-ahead | Planned |`

The hub has no test file. Check: `git diff` shows only these lines, and `services.json` parses.

## Live data changes (after the three repo tickets are merged and the user approves; the hub does them, never a repo ticket)

**L0 Stop and back up.** If VN Studio, Edu Studio or Cartoon Studio is running, stop it (`pwsh -File scripts\hub.ps1 stop vn-studio edu-studio cartoon-studio`, a service stop: the user's go-ahead). Then copy each file below next to itself as `<name>.bak-HUB-39` before editing it. The `.bak-HUB-38` files stay. The way back is the `.bak-HUB-39` files. Only the YAML front matter changes, and one prose bullet in each `roles.md`.

| # | file | key | old | new |
|---|---|---|---|---|
| L1 | `C:\Users\Infplane\VisualNovels\config\providers.md` | `acp.models` row `llama/inkling-2-mini` (line 209) and `llama/inkling-2-mini-dspark` (line 213) | no `extra_body` | `extra_body: { chat_template_kwargs: { reasoning_effort: none } }` after `vision: true` (V1) |
| L1 | `C:\Users\Infplane\VisualNovels\config\roles.md` | `roles.art-critic.models` (line 11) | `[paid, lmstudio]` | `[paid, acp/llama/inkling-2-mini]` |
| L1 | same, prose | the `art-critic` bullet (line 31) | "...(a Qwen-VL in LM Studio, Claude or Gemini)." | the `art-critic` bullet of the merged seed `visual-novels-orchestrator\seed\config\roles.md`, copied as it is |
| L2 | `C:\Users\Infplane\EduGames\config\providers.md` | rows `llama/inkling-2-mini` (line 174), `llama/inkling-2-mini-dspark` (line 178) | no `extra_body` | as L1 |
| L2 | `C:\Users\Infplane\EduGames\config\roles.md` | `roles.art-critic.models` (line 25) | `[gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, lmstudio]` | `[gemini/gemini-2.5-flash, anthropic/claude-sonnet-4-5, acp/llama/inkling-2-mini]` |
| L2 | same, prose | the bullets that name the art-critic's LM Studio (the "After a role's local server entries" and "The art-critic must be a vision model" bullets) | as is | the same two bullets of the merged seed `edu-game-studio\seed\config\roles.md` |
| L3 | `C:\Users\Infplane\CartoonStudio\config\providers.md` | rows `llama/inkling-2-mini` (line 170), `llama/inkling-2-mini-dspark` (line 174) | no `extra_body` | as L1 |
| L3 | `C:\Users\Infplane\CartoonStudio\config\roles.md` | `roles.frame-critic.models` (line 19) | `[client/claude-code, lmstudio]` | `[client/claude-code, acp/llama/inkling-2-mini]` |
| L3 | same, prose | the paragraph "Every role starts on `client/claude-code`..." (its `lmstudio` sentence) | as is | the same paragraph of the merged seed `cartoon-studio\seed\config\roles.md` |

The line numbers were read on 2026-11-21. Find each row by its id first: if the live file has changed since, the id decides, not the line number. After L1-L3, start the apps that were running (a service start: the user's go-ahead).

**Verify (no GPU).** `git diff --no-index <file>.bak-HUB-39 <file>` for each of the six files shows only the lines above. Then each app's model view: VN Models page or `vno_status`, Edu `edu_status`, Cartoon `cts_status`. The critic's list shows `acp/llama/inkling-2-mini` as usable (no "not a vision model", no "disabled"), and the Inkling row shows its `extra_body`. Edu `edu_status` on a course with `media.art.review: true` and no course model for the critic no longer says "no model with vision is available".

## Live checks (each needs the GPU and the user's go-ahead at run time)

GPU = loads a model onto the GPU; SVC = starts or stops a service. Record each result in `runs/hub-39-vision-checks.md` (ids, times, tokens, verdicts, VRAM readings), so another session can resume. The answer of each review is in the app's own files; the tokens are in `logs\spend\2026-11.md` of each data folder (columns `tokens_out`, `ms`).

| # | what | how | passes when |
|---|---|---|---|
| K0 | preflight (SVC) | `pwsh -File scripts\hub.ps1 status`. acp-proxy, comfyui, vn-studio, edu-studio and cartoon-studio up, or start them (`hub.ps1 start acp-proxy comfyui vn-studio edu-studio cartoon-studio`). `curl http://127.0.0.1:8787/v1/models` lists `llama/inkling-2-mini`; `curl http://127.0.0.1:8787/healthz` shows llama `max_concurrent: 1`; `curl http://127.0.0.1:8188/system_stats`: note `vram_free`. | all listed |
| K1 | Inkling answers with the V1 body (GPU: Strata to Llama switch) | one curl chat to `llama/inkling-2-mini` with `chat_template_kwargs: {reasoning_effort: "none"}`, `max_tokens: 200`, text only | 200 with text; header `x-acp-proxy-ignored-params` does not list `chat_template_kwargs` |
| K2 | VN, the real path, 1 and 2 images, ComfyUI next to Inkling (GPU) | `vno_create_project` with a 1-scene story (1 character with `expressions: ["neutral"]`, 1 place) and `settings: {art: {review: true}}`. No `models` for the art-critic, so the V2 list decides. Write the prompts by hand with `vno_asset_set` (no art-director call, so Strata is not loaded). Then `vno_asset_generate {slug}` and `vno_wait`. ComfyUI makes the sheet, the sprite and the background, and the critic reviews each one; the sprite review sends 2 images (sheet first). Read `/system_stats` `vram_free` while Inkling is loaded and an image job runs. | every review job is done, on `acp/llama/inkling-2-mini` (the job log names it); each review is approved, or rejected with a revised prompt, and none is "could not run"; `tokens_out` < 2000 in every spend row; no ComfyUI out-of-memory error, and each image job after Inkling loaded finishes (note its time) |
| K3 | Edu, the real path (GPU, long: about 20 pictures) | copy the folder `C:\Users\Infplane\EduGames\courses\suncev-sustav` to `...\courses\hub39-critic-check`. In the copy's `course.md`, replace `models: "*": client/claude-code` with `models: { art-director: client/claude-code }`, so the session answers the art plan itself and the critic follows V2. `edu_run_pipeline {slug: "hub39-critic-check", restart: true, from: "art"}`. Answer the art-director tasks with `edu_get_task` / `edu_submit_task`. When `edu_status` shows the last `art_review` round done, `edu_stop_now` (no music, no build). | `art_review` is done, not skipped, and names Inkling; every picture has a verdict in `pipeline/reviews/art_review-k1.json`; `tokens_out` < 2000; no "did not return valid JSON twice"; the round-2 pictures (if any) are made with Inkling still loaded and no ComfyUI out-of-memory error |
| K4 | Cartoon, 3 or more images at 1568 px (GPU) | copy `C:\Users\Infplane\CartoonStudio\series\pilot` to `...\series\hub39-critic-check`. Back up `C:\Users\Infplane\CartoonStudio\agents\frame-critic-felix-ostrander.md` (as `.bak-HUB-39`) and set its `model: acp/llama/inkling-2-mini`. `cts_clip_review {series: "hub39-critic-check", episode: "ep00-pilot", clip: "hero"}`, `cts_wait`. Then restore the agent file from its backup at once. | the job is done on Inkling; `episodes/ep00-pilot/reviews/clip-hero-<n>.json` in the copy is a valid `cts.review/1`; note the number of images, the input tokens (spend row `tokens_in`) against the 32768 context, and `tokens_out` (there is no cap: say if it is above 3000) |
| K5 | restore Strata (GPU: Llama to Strata switch) | one curl chat to `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, `max_tokens: 20`, `reasoning_effort: "none"` | 200; `/healthz` shows strata as the loaded local model |

Not covered by these checks: images with real defects (whether Inkling catches a real flaw: K2 and K3 only show that verdicts are valid and plausible), the Blender `frames-3d` contact-sheet review (K4 runs the clip review, which uses the same `runRoleTask` path and the same images), and a review that fails over from a cloud model. Mark each UNTESTED in the run log.

If K2 or K3 fails on memory: stop, record it, and ask the user (D2). Do not change code in this ticket.

## Decisions for the user

1. **D1 In VN and Edu, Inkling is effectively the critic's first model, not a fallback.** VN's `paid` has no vision. Edu's Gemini and Claude have no API key on this PC. VN reviews only when a project turns `art.review` on (all 20 projects are off). Edu reviews by default, so every Edu course with pictures and no course model for the critic spends about 2 minutes per picture and round on Inkling (about 35 to 40 minutes for 20 pictures), plus GPU switches. Recommend: accept; a session that wants speed sets the critic to `client/claude-code` in `course.md` `models` as today. Alternative: also add a vision-capable cloud model first (needs a key: a paid API, outside this scope).
2. **D2 ComfyUI and Inkling share GPU memory during a picture run.** Recommend: accept, document it (H3) and measure it in K2 and K3; if image jobs fail, open a follow-up (a proxy idle unload of Inkling, or freeing ComfyUI before a local review). Alternative: plan that follow-up now, before any live use.
3. **D3 The throwaway check data** (`VisualNovels\projects\<K2 slug>`, `EduGames\courses\hub39-critic-check`, `CartoonStudio\series\hub39-critic-check`). Recommend: keep it until you have looked at the reviews, then delete it on your word (a delete, confirmed then). Alternative: delete it right after the checks.

## Steps for the user

- U1 Approve this plan and answer D1 to D3 (or accept the recommendations).
- U2 Go-ahead at run time for L0 (stopping the apps), the restart after L3, and each of K0 to K5 (GPU or SVC).
- U3 Optional: look at two or three K2 or K3 verdicts and say whether they are sensible. The checks prove only that the answers are valid.
