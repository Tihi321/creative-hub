# HUB-44 handoff: all pending ideas left over from REQ-0030 "ACP for all"

Written 2026-11-22 for a new session. Read-only inspection; no code, config or live data changed; nothing started; no model called; nothing committed.

Files read: `C:\projects\Personal\creative-hub\.claude\director\requests\REQ-0030-acp-for-all.md` (Extra ideas, lines 172-259, and Log lines 340-396); HUB-40 to HUB-43 ticket folders (plan triage tables, questions, discoveries, attention) and HUB-39 / HUB-41 / HUB-42 discoveries, all under `C:\projects\Personal\creative-hub\.claude\tickets\`; run logs `C:\projects\Personal\creative-hub\runs\hub-39-vision-checks.md`, `hub-40-extra-ideas.md`, `hub-41-pixel-agent.md`, `hub-42-pending-ideas.md`, `hub-43-open-ideas.md` (UNTESTED lists, Corrections); AAP-47, AAP-49, AAP-50, PAR-22, PAR-24, VNO-72 and other per-repo ticket changelogs and discoveries; the hub `CLAUDE.md`, `ROADMAP.md`, `services.json`, `README.md` (grep); `C:\Users\Infplane\.claude\CLAUDE.md`. Plus read-only git in the nine repos.

## 1. Start here

- This is the list of every idea from the "ACP for all" director work (request REQ-0030, hub tickets HUB-38 to HUB-43, all done, merged, pushed) that has no build yet. The user said: "i want handoff for all pening ideas as i want to implement them just in new session".
- REQ-0030's file `C:\projects\Personal\creative-hub\.claude\director\requests\REQ-0030-acp-for-all.md` is local only and never committed (`.claude/director/` is never committed). Its `## Extra ideas` section is the master list; its `## Outcome` section is still empty and the request is open until the user closes it.
- Rules from `C:\Users\Infplane\.claude\CLAUDE.md`: plans go to `.claude/tickets/<ticket>/plan.md` (this folder has none yet: the new session writes it); implementing a plan goes through the global `implement` skill; the `director` skill was used for REQ-0030; end every run with every requested item marked DONE, NOT DONE (with the reason) or UNTESTED. Temp files go to `.claude/temp/`. Tests follow the `test-discipline` skill. Node: if `node` is not on PATH use `fnm exec --using default <cmd>`, but see trap 2 for yarn.
- Next free ticket ids (verified from `ROADMAP.md`, `.claude/tickets` and `git branch -a` in each repo; the highest used is shown): HUB-44 (this folder; HUB-43 last), AAP-51 (AAP-50 last), PAR-25 (PAR-24), VNO-73 (VNO-72), EGS-76 (EGS-75), CTS-59 (CTS-58), SCP-69 (SCP-68), MDI-21 (MDI-20), BTT-38 (BTT-37).

## 2. State of the system (verified 2026-11-22 by read-only git; services not probed)

Repo heads, all on `master`, local master equals `origin/master` in all nine:

| repo (under `C:\projects\Personal\`) | head | worktree |
|---|---|---|
| creative-hub | ccfe4d5 before this handoff's own commit | clean |
| api-acp-proxy | 9f23c3a | clean (the two AAP-43 state files were committed on 2026-11-22 on the user's word) |
| scriptorium | 980e415 | clean |
| book-translator | 83f75c4 | clean |
| visual-novels-orchestrator | 12ee5c5 | clean |
| edu-game-studio | 7d93579 | clean |
| cartoon-studio | 5635447 | clean |
| pixel-art-generator | 5778801 | clean |
| midi-generator | 9981150 | clean |

- Ticket branches (`*_extra-ideas`, `AAP-4x_*`, ...) are kept locally and not pushed.
- What runs: do not start or stop anything. Check with `pwsh -File C:\projects\Personal\creative-hub\scripts\hub.ps1 status`. At the end of the last live round (2026-11-22 20:15, per `runs\hub-43-open-ideas.md`) these were up: acp-proxy (new build), comfyui, vn-studio (new build), vibetts, and Strata (loaded by the proxy). Down: Scriptorium, Edu Studio, Cartoon Studio, Pixel Studio, Chiptune, Book Translator. This may have changed (the machine can restart).
- Ports: proxy 8787, Strata 8080, Gufo 8081, Llama.cpp 8082 (Inkling), embeddings 8083 (starts on demand; it answered an embeddings probe in HUB-40 N2), ComfyUI 8188, VN Studio 7459, Pixel Studio 7457 (MCP), Edu 7463, Cartoon 7465.
- Local models: one local model on the GPU at a time. Default local model id: `acp/strata/qwen3.8-flash-next-unsloth-ud-iq4_xs` (Strata, 131,072 context, images yes, thinks when a caller omits `reasoning_effort`, so every Strata row sends `none`). Inkling is `acp/llama/inkling-2-mini` (32,768 context, vision, the art/frame critic model, about 1 to 2 minutes per review). Embeddings `acp/llama/nomic-embed-text-v1.5` (768 dimensions).
- The proxy runs from `api-acp-proxy\dist\` and VN Studio from `visual-novels-orchestrator\out\`. Both were rebuilt and restarted on 2026-11-22 so they carry AAP-44 to AAP-50 and VNO-69 to VNO-72. Pixel, Edu and Cartoon were rebuilt but are not running.
- The proxy settings file `%APPDATA%\api-acp-proxy\settings.json` SHA-256 was `1130D96801D1F646694975F790F7A2BB45606EE78C64652759726868A8BBA592` at the end of the live round (hash only; never print the file).

## 3. The pending ideas

Source tags: REQ = Extra ideas line number in REQ-0030; H43 = `runs\hub-43-open-ideas.md`; D43 = `HUB-43-open-ideas\discoveries.md`; D42, D41, D40, D39 likewise. Sizes are as the sources give them; "not recorded" means no source sized it.

### 3.1 api-acp-proxy (14 items)

**P-01 Gufo status tiles on the Monitor, and cross-check a Gufo profile's vision flag from `architecture.input_modalities`.** Source: REQ 248, 243; HUB-43 plan triage rows 1d and 4, probe P1. Known: no Gufo endpoint is known; the proxy only probes `/v1/models` (`src/settings.ts:15`); no docs in `D:\Gufo\v0.35.0`; Gufo was not running in any check. Probe P1 (GET only, once the user loads a Gufo model through the proxy): `curl -s -o - -w " %{http_code}" http://127.0.0.1:8081/health`, then `/metrics`, `/v1/status`, `/props`, `/slots`, `/v1/models`; record status codes, JSON keys and whether `/v1/models` has `architecture.input_modalities`. For Llama the cross-check was judged no change (profile vision and `--mmproj` come from the same fields). Smallest version: record the probe, then map only what Gufo answers. Depends on a running Gufo model (a GPU switch, minutes). Size: not recorded. Proof: probe output, then a unit test with the recorded sample and a live look at the window.

**P-02 Refresh Strata's model list and vision flag when the proxy starts or Strata becomes ready.** Source: REQ 258; D43 #11; H43 Corrections. Known: right after a proxy restart, before Strata's first load, `GET /v1/models` shows the Strata model with no `vision` flag and `acceptsImages` is false, so an image request in that window goes without its image (not tested live). Correction recorded in H43: once Strata is loaded the proxy lists it with `vision: true` (the earlier "never vision" reading was taken before the load). Smallest version: refresh the list at Strata ready. Depends on: nothing running for the unit test; a proxy restart and Strata load for the live check. Size: not recorded. Proof: test that fails on the old code (image request before first load keeps its image), then a live image request right after a proxy start.

**P-03 VRAM shown as "GB" but computed as GiB.** Source: REQ 258; D43 #12. Known: the Monitor showed 63.2 "GB" of 64.0 "GB" from 67,884,810,240 bytes. Smallest version: change the unit label to GiB or convert. Size: tiny. Proof: a unit test of the formatter; read the window.

**P-04 Export or move `spark()` and give it a small test.** Source: REQ 252; D43 #7. Known: `spark()` is in `src/renderer/monitor-view.ts`, not exported; its flat-line rules were only verified by extracting the shipped function (AAP-49/50 changelogs). Size: tiny. Proof: the new test must fail against a broken `spark()`.

**P-05 Reason texts and dots on the Monitor.** Source: REQ 253, 255; D43 #5. Parts: (a) a "no prompt read yet" reason on Strata's Prefill tile (AAP-50 polish 1 added it for Llama only); (b) single isolated sparkline points drawn as dots; (c) a passing `/metrics` failure on a llama-server that has `--metrics` shows "restart the model for speed" but should say it needs `--metrics`; (d) a thinking-token count estimated from the reasoning text shows without the approximate mark. Size: tiny each. Proof: unit tests on the view mapper where possible; the rest needs a person to read the window.

**P-06 An outside Llama server has no model id on the Monitor.** Source: REQ 255. Known: an outside Strata shows its id (K5 data), an outside Llama has none to show; `main.ts:560-575` is the outside-server path. Smallest version: read the alias from llama-server's `/props` (`model_alias` exists, per AAP-50). Not recorded whether the code already does this. Proof: unit test with a recorded `/props`; live check needs a hand-started llama-server (not planned).

**P-07 A distinct state after a render error: check what remains.** Source: REQ 242. AAP-49 built a notice when a reading could not be shown (D42 / AAP-49 changelog: "render-error notice"). What the user sees was not seen in the window (UNTESTED). Task: confirm it matches the idea ("no engine data" state), then close or finish. Size: tiny.

**P-08 Two `applySettings` calls skip `refreshLocalSettings`.** Source: D43 #6, `src/electron/main.ts:612` and `:621`. Effect: the terms acknowledgement leaves cached provider settings stale until the next save. Size: tiny. Proof: unit test if the function is testable; otherwise read the code.

**P-09 `readText` caps the body only after reading it.** Source: D43 #4, `src/local-monitor.ts`. Only the timeout bounds the read. Smallest version: cap while streaming. Size: tiny to small.

**P-10 A program on Strata's or Llama's port that answers JSON is shown as a loaded model.** Source: D43 #3. The proxy already sends requests, and the Strata key, to that port. Smallest version: check the server's identity before showing the model. Size: small.

**P-11 The Usage page sets inline sizes from script.** Source: D42 #5; AAP-47 discoveries; `src/renderer/usage-view.ts:167` and `:231` (`style.height` / `style.width`). Suggested: CSS classes or `progress` elements. Out of scope in AAP-49. Size: small. Proof: grep for `style.` in the file; a look at the Usage page.

**P-12 Build gate for a llama-server that does not know `--metrics`.** Source: AAP-50 plan, Out of scope. Both installed builds (b12613, unsloth b12588) support it; a custom build that refuses the flag fails to start with llama-server's own message in the launcher log. Size: small; value is low unless the user installs another build.

**P-13 Strata's `/v1/telemetry` and `/v1/status` as later Monitor sources.** Source: REQ 239. HUB-43 triage row 2a said NO CHANGE (every number a tile would use is already in `/metrics`); REQ still says "pending". Needs only the user's decision to close.

**P-14 Small proxy leftovers from checker notes (not triaged).** D40: if `servers.stop("embed")` throws, the save handler returns `ok:false` though settings were applied (`src/electron/main.ts:319`); a provider built without dimensions skips the dimension check (`src/providers/local-openai.ts:361`). D42: Strata ready with its provider off shows a dash for the model; `/v1/models` now marks Strata `vision: true`, so a client that picks vision models from the list could start choosing Strata (check which clients filter by vision). D41: AAP-45's "an mmproj fix leaves `hf` alone" is proven by reading code, not by an assertion. Sizes: tiny each.

### 3.2 pixel-art-generator (6 items)

**P-15 Strata as Pixel's vision model.** Source: REQ 256, 235; D43 #9; H43 K3. Known: Strata's `/health` says `images: true`; Pixel's Strata row has `vision: false` in the seed and live. Live check K3 (temp data folder, `vision: true` on the Strata row, same 16x16 mushroom text): run 1 hit `max_steps` after 25 steps, 220.6 s, about 1.05 M input tokens, redrawing the same 16-row grid with `clear_cel`+`draw_grid`+`render_preview` about 18 times; run 2 completed in 19 steps, 127.4 s. With vision off a run takes 4 steps and about 78 to 87 s. Whether the preview image reaches Strata is likely (the model stops calling `read_grid`) but not proven byte for byte; `hasImage` comes from the tool result. Smallest version, in this order: (1) a "same grid twice: stop" guard; (2) Strata row `vision: true` in the seed and live data with a migration. Depends on: user decision, a Pixel build (headless `--mcp-only` in a temp folder via `PIXEL_STUDIO_HOME` and `PIXEL_STUDIO_MCP_PORT`), Strata loaded. Size: medium. Proof: unit test that a repeated identical grid ends the run; repeat the K3 runs (at least 3 vision runs, all must finish) and verify the image delivery from Strata's request log if possible.

**P-16 Steer a run's first step to a warm Strata slot, or warm Strata's conversation cache.** Source: REQ 257; D43 #10; H43 K4. Known: inside a run about 99% of the prompt is reused from step 2; the first step of 3 of 4 new runs reused 0 tokens and paid about 70 s of prefill for 34,300 tokens (one reused 34,250 of 34,271); Strata's conversation cache never restored (14 parks, 8 evictions, 0 restores); reuse across runs depends on which of Strata's 4 slots takes step 1. Not recorded how to steer to a slot. Size: not recorded (a design is needed). Proof: first-step `reused` in Strata's `/metrics` `requests[]` over several back-to-back runs.

**P-17 Slimmer tool list for JSON-action mode (`agentToolSet: 'no-files'`).** Source: REQ 221, 249; HUB-43 triage row 12 and question 2. Known: 71 tools, the JSON-action instructions are 99,843 characters plus a 20,041-character guide that names 69 of the tools; an optional setting in `config/app.json` (`'all' | 'no-files'`, default `all`, read through `readAppSettings` in `src/main/appSettings.ts`) would drop 12 file and export tools: 17,349 characters, about 4.3k tokens, about 14% per step; it contradicts the guide text. K4 showed little saving on steps 2+ (already reused) and about 9 s of 70 s on a cold first step. HUB-43's recommendation was to wait for K4; K4 is done. The user's decision is still pending. Size: "too large" in HUB-42, small for the optional setting (HUB-43). Proof: a run in `no-files` mode finishes the mushroom task; the first-step prompt token count drops by about 4.3k.

**P-18 The window's New chat button aborts a running MCP run.** Source: D41 #3; HUB-43 question 3 (recommended: leave it; alternative: disable the button while a run goes, a one-line UI change). Documented in the README (line 50); code `src/renderer/state/chat.ts:133-141`. A user decision. Size: tiny.

**P-19 `before-quit` does not wait for the agent's chat save.** Source: D42 #9, `src/main/index.ts:178`. Real only when the window is closed mid-run (that chat is lost; the drawing is kept); headless already waits (`headless.ts:127`). Triage: NO CHANGE; REQ still lists it. Needs Electron to test. Size: small.

**P-20 The per-run event buffer drops early steps' usage; one unexplained extra Strata request.** Source: D43 #14. Known: the buffer holds 200 events, 50 per run; in K3 run 1 Strata counted 26 requests for 25 steps (one extra request of about 34,300 tokens, not explained). Suggested action in the source: none for now. Size: not recorded.

Also UNTESTED in Pixel (cross-repo list in 3.8): the Pixel window's wiring of the agent tools and view sync; `stop_agent_run` in the middle of drawing; `continueChat: true`; the 30-minute limit.

### 3.3 visual-novels-orchestrator (6 items)

**P-21 `stripTextNegations` never exercised live.** Source: H43 K2 and UNTESTED. In the live check the critic wrote a positive revision ("plain", "blank", "shuttered"), so the sanitiser had nothing to strip. Proof needs a rejection where the critic writes "no text". Size: a live check only.

**P-22 Forms it still keeps, and the lost final full stop.** Source: REQ 254, 246; D43 #8; VNO-72 changelog; D42 #11. Kept on purpose: "no text on the walls", "a street and no text" without a comma, "a shop sign with no text", "no people", "no borders". Known bug: "A street. No text." becomes "A street" (the full stop goes with the last clause). Code: `src/engine/assets/derive.ts` `TEXT_NEGATION` / `stripTextNegations`. Smallest version: keep the final full stop when the removed last clause ended with one. Size: tiny. Proof: extend `tests/assets-derive-manifest.test.ts`; the new expectation must fail before the fix.

**P-23 The 8 queued job files from 2026-10-23 that never finish.** Source: REQ 259; D43 #13. Known: `C:\Users\Infplane\VisualNovels\jobs\queued` holds files named `hub07-flow-test--*` (r2) and `hub08-13-autostart--vn.build--regen-sfx_bell--r4`; their dependencies never finish; they survive restarts and did not start. Suggested: clear or report them. Deleting live data needs the user's go-ahead (and a backup per the rules in section 4). Size: tiny.

**P-24 `vno_wait` progress notifications instead of the 240 s cap.** Source: HUB-43 plan Out of scope; D42 #15. Known: a wait over 300 s is cut by the MCP idle limit because no progress events are sent; VNO-72 capped every tool wait at 240 s (`WAIT_LIMIT_MS`). Size: not recorded (medium guess: needs MCP progress plumbing).

**P-25 Do Edu's and Cartoon's critics redraw from a revised prompt the same way as VN's?** Source: REQ 237 follow-up. HUB-41 K2 and HUB-43 K2 only exercised VN. Not recorded whether Edu or Cartoon feed `revisedPrompt` back and whether they draw lettered signs. Needs a read of their code first, then a live check (ComfyUI plus Inkling on the GPU).

**P-26 Small items from checker notes.** D40: Gufo is probed by a bare TCP connect to 8081 in the autostart check of VN, Edu and Cartoon (`src/engine/studios/autostart.ts`), so any process on 8081 holds back ComfyUI autostart; suggested: probe by Gufo's health URL (see P-01 for the endpoint question). D39: `edu_stop_now` pauses the whole Edu queue (user decision whether a per-course stop is wanted); Edu's `art_review-k1.json` had 6 revise verdicts but 3 in its revise list (probably a score threshold, unconfirmed). Sizes: not recorded.

### 3.4 edu-game-studio and cartoon-studio (4 items)

**P-27 Live checks never run after their rebuilds.** Source: H43 R4 and UNTESTED; EGS-75 and CTS-57 changelogs; HUB-40 L2. Both were rebuilt on 2026-11-22 20:10 and never started in this session. Open: (a) the refreshed critic prompts in the live data folders (Edu `art-critic/review.md`, Cartoon `frame-critic/*.md`) after the first start; (b) English critic notes (Edu `img-rpg-hero` once came back in Serbian-flavoured wording; HUB-41 K2 proved English notes only on VN); (c) ComfyUI free on an empty reply against a real ComfyUI (Edu `edu_comfy_free`, Cartoon `freeBeforeDispatch`/`kind-switch.ts`); (d) the Gufo-aware autostart check (Gufo 8081 only; Llama 8082 left out on purpose). Starting an app starts its own services; ask first, and never start Scriptorium (not these two, but note the rule). Size: live checks.

**P-28 Edu: `yarn test` flake.** Source: D41 #11. `tests/pipeline.test.ts` failed in a first full run (4 files failed), not reproduced by two later runs (530 of 530 passed); suspected load. Suggested: run the full suite a few times. Size: tiny.

**P-29 Cartoon: NEVER_STARTED comment omits Gufo.** Source: D40, `cartoon-studio/.../autostart.ts:21`. Cosmetic. Size: tiny.

**P-30 Edu and Cartoon: live prose.** Source: HUB-41 L3 done for Edu settings; HUB-42 and HUB-43 prose steps done for Scriptorium, VN, Edu providers, Pixel. Not recorded: whether Cartoon's live `providers.md` was compared with its seed after HUB-42 (HUB-40 said Cartoon roles prose already matched). Check, with diff, before assuming anything. Size: tiny.

### 3.5 scriptorium (5 items)

**P-31 The full re-chunk: delete the index and re-embed the whole library.** Source: ROADMAP row 33; run log `hub-40-extra-ideas.md` N2. Known: only the plain re-index ran (35 files embedded, 1,414 unchanged, 0 failed, about 20 s, backup `C:\Users\Infplane\Scriptorium\index\library.sqlite.bak-HUB-40`). The index has no chunk over 1,800 characters (longest 1,790) but 55 separator-only (`---`) chunks remain in unchanged files; a full rebuild would remove them and apply the chunker cap to every file. A user decision (GPU time and deleting the index). Command: `npm run engine -- reindex --data C:/Users/Infplane/Scriptorium` with forward slashes (backslashes are stripped). Do not start Scriptorium (reindex runs before the scheduler and jobs, per code reading). Size: about 20 s per 35 files, so the full library is longer (not recorded). Proof: chunk count, no `---`-only chunks, longest chunk, failed files 0.

**P-32 The stale `index\engine.lock`.** Source: REQ 229; D43. `C:\Users\Infplane\Scriptorium\index\engine.lock` has pid 19260 (dead, dated 2026-11-21). Decision in HUB-42: hub clears it; the start-time removal (`Clear-StaleLock`) has not run on a real lock (see P-36). Task: confirm after the next legitimate Scriptorium start only. Never start Scriptorium without asking.

**P-33 Three Strata operating sentences were dropped from the live `providers.md`.** Source: D43 #15. Dropped by the whole-prose sync because the seed no longer has them: one model per process and the model field ignored; context must match max-context; loading takes 1 to 3 minutes, with `loaded: true` on health. Kept in `C:\Users\Infplane\Scriptorium\config\providers.md.bak-HUB-43` and `C:\Users\Infplane\VisualNovels\config\providers.md.bak-HUB-43`. Decision: are they still true and worth putting back in the seeds? Size: tiny.

**P-34 Scriptorium reading its new prose (`roles.md`, `providers.md`, `settings.md`) is untested.** Source: H43 UNTESTED. It reads them on its next start; Scriptorium has not been started since. Starting needs the user's word.

**P-35 Small Scriptorium items.** D40: `splitLong` loops forever for max 1 with text starting with an emoji (private, called only with 1800, not reachable); a long emoji-only or punctuation-only run is dropped from the index after a hard cut (keep or log it); the `lms` load examples in `seed/config/providers.md:315` use the embedding model with `-c 32768 --parallel 4` (cosmetic); `tests/adapt.test.ts` "starts without asking the editor-in-chief" failed once with ENOENT under load. D41: `yarn test <file>` does not run a single file (use `npx vitest run <file>`). Sizes: tiny each.

### 3.6 creative-hub (5 items)

**P-36 The start-time lock removal never ran on a real lock.** Source: H43 "Every hub.ps1 start and stop", UNTESTED; D43. `hub.ps1 start` now runs `Clear-StaleLock -AtStart` (dead pid, or a pid that started after the lock's time, is removed). Dry runs only. Real stale locks exist now: Scriptorium 19260, Edu 25460, Cartoon 10856, Pixel 32952 (all dead pids). The first real start of Edu, Cartoon or Pixel proves it. VN's own lock (pid 21468, node) was left alone correctly. D43 #16: VN wrote its lock 5.7 s after its process start this time (the script comment says 2.9 s); the rule is unaffected.

**P-37 `Clear-StaleLock` is only tested under PowerShell 7.** Source: D43 #2. Windows PowerShell 5.1 would take the string branch, not exercised. Either test it under 5.1 or document that the hub runs on pwsh 7 only. Size: tiny.

**P-38 A distinct "time has no zone" message in the lock cleanup.** Source: REQ 253; HUB-43 changelog. A zoneless time is left alone silently. Size: tiny.

**P-39 `.bak-HUB-*` backup files in the live data folders.** Many exist, for example `C:\Users\Infplane\EduGames\config\providers.md.bak-HUB-42`, `...\Scriptorium\config\providers.md.bak-HUB-43`, `...\Scriptorium\index\library.sqlite.bak-HUB-40`. Keep or clean: a user decision. Delete only on the user's word.

**P-40 hub.ps1 pid shown by `start` for acp-proxy differs from `status`.** Source: D40 (scribe). `start` printed pid 29216 while `status` showed electron pid 26412; probably launcher versus app process. Confirm which pid `status` should track. Size: tiny.

### 3.7 midi-generator and book-translator (1 item)

**P-41 Genesis perf test margin.** Source: D40; REQ 172 (built as MDI-19). Unloaded, a Genesis render takes about 1.4 s, so the 4 s limit catches about a 3x slowdown, not the 2x the plan claimed. Suggested: state the real margin in the test (comment). Size: tiny. Book-translator has no pending item.

### 3.8 Cross-repo untested items (1 group)

**P-42 UNTESTED lists of the run logs.** Nothing here has proof beyond the lines named:
- The proxy window itself: Monitor, About and Requests pages, sparklines, thinking tokens column, the conversation-cache tile, the render-error notice, the "started outside the app" label under Model and State, polling while hidden. Only a person can read it. The expected values were computed from the same mappers and are listed in `runs\hub-43-open-ideas.md` (section "What the Monitor and About pages should show"). Pass of the user's own words: the user still has to look ("look at the proxy window" was left for the user).
- Byte-level proof that a preview image reaches Strata (see P-15).
- Pixel window wiring of the agent tools and view sync; `stop_agent_run` mid-drawing; `continueChat: true`; the 30-minute limit.
- Edu and Cartoon after their rebuild (P-27); L1 in the Pixel window (only headless ran).
- `hub.ps1 start` lock removal on a real app (P-36).
- Sprite review: only one sample (HUB-40 N1), `frames-3d` Blender contact-sheet review, review failover from a cloud model to Inkling, VN sprite approval with two images (all from `runs\hub-39-vision-checks.md`).
- Outside Llama.cpp server and the unsloth build with `--metrics`; per-slot `n_ctx` with `-np` auto was read live on Inkling (32,768, correct).

Pending-count summary: api-acp-proxy 14, pixel-art-generator 6, visual-novels-orchestrator 6, edu-game-studio and cartoon-studio 4, scriptorium 5, creative-hub 5, midi-generator and book-translator 1, cross-repo 1 group. Total 42 ids (P-01 to P-42).

Already done, do not re-propose: Strata images and cached tokens through the proxy (AAP-46); hf.quant/mmproj/draft fix (AAP-45); sparklines, thinking tokens, conversation cache tile, outside Strata and Llama server, render-error notice, apiKey cache (AAP-49); `--metrics` and Inkling speed and the Llama context fix (AAP-50); tests typechecked, usage guards, flaky test fixed (AAP-48); Pixel agent tools over MCP, `model: ""`, stop flags, `openChat` race, saved-chat idle wait (PAR-22 to PAR-24); VN critic prompts (mid grey, English notes), wider negation stripping, 240 s waits, no `--` in slugs, `vno_delete_project` removes job files (VNO-69 to VNO-72); `freeMemory` on an empty reply in VN, Edu, Cartoon; kind switch uses it (CTS-58); reindex lists files (SCP-68); live prose of all apps equal to the seeds (HUB-40 L1, HUB-41 L1-L3, HUB-42 L1-L5, HUB-43 L1-L2); the plain Scriptorium re-index; `stop_agent_run` cancels the Strata request (proven in H43 K3: `client_disconnect_cancels` 0 to 1, request `finish: cancel`); Strata thinks by default when `reasoning_effort` is omitted (HUB-40 N3). Decided no change: stale portable proxy `D:\Programs\ACP-Proxy` (nothing starts it), the `inkling-2-mini-dspark` profile and label mismatch (the user's settings, not the repo), local paths in MCP results, stale turn-stack entry, `send()` assigning `current` late, the "acp provider added to old folders" migration.

## 4. Decisions the user already made that still bind

- Scriptorium is never started without asking (hub CLAUDE.md: it resumes its whole book factory and may spend on paid models).
- No paid or cloud model without asking (every live round so far used only Strata and Inkling at 0 USD). Video spends Flow credits only on an agreed budget; ElevenLabs and Gemini stay inside their free quotas.
- No force-push. When asked to commit or push with no branch named while on the default branch, ask whether to commit there or on a new branch; never create a branch silently. Commit messages by Bash heredoc `git commit -F - <<'EOF'` with a blank line after the subject, ending with the attribution line the session's reminder gives.
- Request files under `.claude/director/` are never committed.
- Live data edits need a backup beside the file (the pattern is `<file>.bak-HUB-NN`) and the user's go-ahead each time. The user's wording for the live rounds: "Yes, run checks", "Yes, run all", "All if them, if there is nothing else to fix".
- Throwaway check data is deleted only on the user's word: "you can delete throaway checks, we do not need test copies" (2026-11-22) covered the three `hub39-critic-check` copies only. The throwaway folders of later checks were deleted by the checks' own steps.
- The proxy's `%APPDATA%\api-acp-proxy\settings.json` is never edited by a build or a ticket; no ticket adds a setting without the user's say.
- Plans first, then the user's yes: the user's words were "Approve as recommended", "Yes, approve all", "Yes", "Merge and push", "Yes commit all". Live steps and live checks each need a go-ahead at run time. The user decided: "yes mcp tool for artist agent" (built), "yes vision rows lm studio recomendation" (read by the director as removing the dead alias, not moving to Inkling, because Inkling's 32,768 context is smaller than the artist's first prompt of 34,292 tokens), "scriptorium ok recommendation" (plain re-index only).
- Never rewrite a book's `models:` history. One local model on the GPU at a time. Never start Strata by hand while the proxy holds a local model (K5 did, with the proxy stopped, and restored it).
- Local model rule: no paid fallback may answer a local-only check (HUB-43 K3 set `artist: [local]` in a temp copy of the config).
- Final summaries mark every item DONE / NOT DONE / UNTESTED.

## 5. Traps this work hit

1. Backslashes and `\n` written through Bash heredocs get stripped here. Use the Edit or Write tool for regexes and Windows paths.
2. Working trees are CRLF while git stores LF; do not cause line-ending flips in a commit. `fnm exec yarn` and `fnm exec npm` fail: put the fnm default alias dir on PATH (`export PATH="/c/Users/Infplane/AppData/Roaming/fnm/aliases/default:$PATH"` in Bash).
3. No builds in api-acp-proxy or visual-novels-orchestrator while their apps run from `dist/` or `out/` (tests, typecheck and lint only on a branch); Pixel and Cartoon also run from `out/` when up. Rebuilds go through `hub.ps1 build` (or the user's own proxy build) and need a go-ahead.
4. `npm run engine -- reindex --data` needs forward slashes in the path.
5. A plan's literal date parsing would have deleted a live app's lock: `ConvertFrom-Json` already returns a `DateTime`, so `[datetime]::Parse` read VN's lock one hour off on pwsh 7.6; a numeric epoch-seconds stamp would be read as 1970. The built code handles DateTime, zoned string and epoch ms.
6. A test assertion that passes on the old code proves nothing: show a new test failing before the fix (AAP-50 polish 2 caught one).
7. `hub.ps1 start` now deletes stale lock files (dead pid, or a live pid that started after the lock's time). `hub.ps1 stop` removes the lock after a kill.
8. `yarn test <file>` in Scriptorium does not run one file: use `npx vitest run <file>`. Edu `yarn test` and the proxy's "does not keep a cancelled turn" test were timing-flaky under full-suite load.
9. Strata thinks when `reasoning_effort` is omitted; every Strata row sends `none`. Inkling needs `chat_template_kwargs: { reasoning_effort: none }` (not top-level). A critic call needs a `max_tokens` of 2000 (a cut-off answer is invalid JSON and costs a repair call).
10. `vno_wait` timeouts over 240 s are cut by the MCP idle limit. `vno_asset_generate {only}` skips assets that already have files: pass `force: true`.
11. Edu's and Cartoon's ComfyUI `/free` returns 200 with an empty body (fixed in all three); `vno_comfy_free` used to fail on it. ComfyUI's `vram_free` (ROCm) does not show llama-server memory.
12. The commit worker's secret scan once stopped on run ids and chat ids (not secrets); confirm with the director and go on.

## 6. Suggested order (a recommendation only)

1. Tiny and safe, unit-testable, no service needed (one proxy ticket AAP-51, one VN ticket VNO-73): P-03, P-04, P-05, P-08, P-09, P-02 (test first), P-22, P-41, P-29, P-37, P-38, P-14, P-35 as small as the new session wants. Prove every new test fails before the fix.
2. Decisions only the user can make, ask in one batch: P-17 (slimmer Pixel tool list), P-18 (New chat), P-31 (full re-chunk), P-39 (keep or clean backups), P-13 (drop the Strata telemetry idea), P-33, P-26 (`edu_stop_now`), P-23 (delete the 8 queued job files).
3. Needs a running service and a go-ahead: P-15 then P-16 (Pixel on Strata, temp data folder), P-21 and P-25 (VN and Edu critic with Inkling), P-27 and P-36 (start Edu, Cartoon, Pixel), P-34 (Scriptorium, only on the user's word). Do the live round once for several tickets, as HUB-43 did.
4. Needs the user's eyes: P-42 proxy window (ask the user to open Monitor, About and Requests), P-07 and the "started outside the app" label.
5. Larger or needing a design last: P-01 (Gufo probe, needs Gufo loaded first), P-16 (warm slot design), P-24 (progress events), P-10, P-11, P-12.
6. Hub work at the end: update `ROADMAP.md` rows for the new HUB-44 ticket, write a `changelog.md` in this folder, and keep a run log in `C:\projects\Personal\creative-hub\runs\hub-44-pending-ideas.md`.

## 7. Sources that disagree or are missing

- REQ lines 239, 240, 241, 250 and 251 still say "decision: pending", but later sources close them: 239 NO CHANGE (HUB-43 row 2a); 240 and 251 done by HUB-43 L1/L2; 241 triaged in HUB-43 rows 11a to 11j (only the New chat and `before-quit` items remain: P-18, P-19); 250 proven in HUB-43 K3. REQ was not updated. Only the lines in this handoff are open.
- `runs\hub-43-open-ideas.md` first says Strata's `/v1/models` entry has no vision flag; its own Corrections section says that was a list read before Strata was loaded. This handoff follows the correction (P-02).
- D43 #16 says VN's lock came 5.7 s after the process start while the script comment says 2.9 s. No change needed.
- Not found: the Gufo endpoints (nothing on disk; P-01); how to steer Pixel's first step to a warm Strata slot (P-16); whether Edu's and Cartoon's critics feed a revised prompt back (P-25); whether the HUB-40 D40 notes (P-14, P-26, P-29, P-35) were already fixed in later tickets; a Cartoon live-prose diff after HUB-42 (P-30); the HUB-44 ticket has no plan.md on purpose.
