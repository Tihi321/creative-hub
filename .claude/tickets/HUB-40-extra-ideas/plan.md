---
status: in-progress
request: REQ-0030
repos: [creative-hub, scriptorium, book-translator, visual-novels-orchestrator, edu-game-studio, cartoon-studio, pixel-art-generator, midi-generator, api-acp-proxy]
branch: HUB-40_extra-ideas
updated: 2026-11-22
---

# HUB-40 Extra ideas of REQ-0030: triage and the small fixes that are still valid

The user said "you can implement all extra ideas with what you recommend". The ideas are the 40 lines under `## Extra ideas` of `.claude/director/requests/REQ-0030-acp-for-all.md` (lines 96-135). Each was checked against today's master of its repo (2026-11-22; the line numbers in the ideas were often stale, the ones below are verified). Context: HUB-38 and HUB-39 plans, `HUB-39-vision-fallback-inkling/discoveries.md`, `runs/hub-39-vision-checks.md`.

Reading built: the narrow one. Only the ideas marked BUILD, each as the smallest change that fixes it; no new features.

## Scope

1. Eight repo tickets, one plan each (each plan stands alone):
   - scriptorium SCP-66 `C:\projects\Personal\scriptorium\.claude\tickets\SCP-66-extra-ideas\plan.md`
   - book-translator BTT-37 `C:\projects\Personal\book-translator\.claude\tickets\BTT-37-extra-ideas\plan.md`
   - visual-novels-orchestrator VNO-69 `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-69-extra-ideas\plan.md`
   - edu-game-studio EGS-73 `C:\projects\Personal\edu-game-studio\.claude\tickets\EGS-73-extra-ideas\plan.md`
   - cartoon-studio CTS-56 `C:\projects\Personal\cartoon-studio\.claude\tickets\CTS-56-extra-ideas\plan.md`
   - pixel-art-generator PAR-20 `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-20-extra-ideas\plan.md`
   - midi-generator MDI-19 `C:\projects\Personal\midi-generator\.claude\tickets\MDI-19-extra-ideas\plan.md`
   - api-acp-proxy AAP-44 `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-44-extra-ideas\plan.md`
2. Hub code on branch `HUB-40_extra-ideas`: `scripts/hub.ps1`, `services.json`, `README.md`, `ROADMAP.md`, `.claude/tickets/HUB-38-acp-for-all/changelog.md` (tasks H1-H4).
3. Live data L1-L2 (the hub, after the repo merges and the user's go-ahead).
4. Checks that need a running service or the user (N1-N4), listed with the exact command; run only on the user's go-ahead.

Ticket ids are the next free ones (checked 2026-11-22 in each `ROADMAP.md`, `.claude/tickets` and `git branch -a`): HUB-39, SCP-65, BTT-36, VNO-68, EGS-72, CTS-55, PAR-19, MDI-18, AAP-43 are the last used. All tickets are independent; they can run in parallel.

## Out of scope

- Ideas marked NO CHANGE, DONE ALREADY or NEEDS USER below (nothing built for them, except the commands written down in N1-N4).
- A Pixel Studio MCP tool for the artist agent (idea 16: needs new engine work, see its sketch).
- Pixel Studio's vision rows (idea 32, Pixel part).
- Any change to `%APPDATA%\api-acp-proxy\settings.json` (the user's own settings), to a book's `models:` map, or to job history.
- Starting Scriptorium (never), Strata by hand, or any GPU job without the user's go-ahead.
- Re-indexing Scriptorium's library (N2).

## Triage (all 40 ideas, in file order; REQ-0030 lines 96-135)

| # | idea (short) | verdict | ticket | reason (verified 2026-11-22) |
|---|---|---|---|---|
| 1 | midi-generator genesis perf test 3000 ms | BUILD | MDI-19 | `tests/core/synth/genesis.test.ts:612` `expect(dt).toBeLessThan(3000)`; measured 3014-3172 ms, so every run fails; best of 2 renders under 4000 ms |
| 2 | ModelsPage help text names Strata | BUILD | VNO-69, EGS-73, CTS-56 | VN `ModelsPage.tsx:408,428,429`; Cartoon `:413,433,434`; Edu has the same text at `:413,433,434` (not in the idea, same fix) |
| 3 | Edu `cli.ts` probe default is paid DeepSeek | BUILD | EGS-73 | `src/engine/cli.ts:24` `['deepseek/deepseek-flash']`; `LOCAL_MODEL` exists in `src/shared/schemas.ts:224`; VN and Cartoon already use it; help `index.ts:29` follows |
| 4 | Cartoon `index.ts` help "from Strata" | BUILD | CTS-56 | `src/engine/index.ts:26`; VN `:28` has the right wording |
| 5 | hub.ps1 `requires` cycle, `-Window` script-wide | BUILD | HUB-40 H1 | `scripts/hub.ps1:340-346` recurses with no guard; `:358` tests `$Window` for every service, required ones included |
| 6 | Stale `D:\Strata\run-*.bat` paths in seeds | BUILD | BTT-37, VNO-69, PAR-20, MDI-19 | the scripts are in `D:\Strata\terminal` (checked on disk): BT `providers.md:269`, VN `:245` (not 243), Pixel `:291`, Chiptune `:293`; Edu (`<your Strata folder>`), Scriptorium and Cartoon are fine |
| 7 | Edu seed settings.md `-low` prose | BUILD | EGS-73 | `seed/config/settings.md:21` (not 16-18) says the checks name Strata's `-low` model; no seed role names one since EGS-71; `:16` still lists `strata` as a kind example |
| 8 | Port 7461 as a sample URL in tests | BUILD | VNO-69, EGS-73 | pure samples (a custom provider `acp-proxy-home`; the 7461 migration acts only on id `acp`): VN `tests/custom-providers.test.ts:54,61,67,107,113`, Edu `:49,55,95,101`. The 7461 in the migration tests stays (it is the old address under test) |
| 9 | Old folder without `acp` gets it enabled with local rows | NO CHANGE | - | intended since HUB-38 (acp is every app's only route to LLMs); `providers-acp-v1` copies the seed row; every live data folder already has an `acp` row, so it is a no-op here |
| 10 | Scriptorium seed `lmstudio` chat rows, `discover: true` | BUILD | SCP-66 | `seed/config/providers.md:69-99`; the live data step left lmstudio `enabled: false`, `discover: false`, only the nomic row, and `embeddings: acp/llama/nomic-embed-text-v1.5` with an acp nomic row; the seed still embeds through LM Studio (`seed/config/roles.md:3`), which is not installed |
| 11 | Autostart GPU check should see Gufo 8081 and Llama 8082 | BUILD (Gufo only) | VNO-69, EGS-73, CTS-56 | `src/engine/studios/autostart.ts:335-342` (same in all three) checks only `strata`; Gufo's models are big text models like Strata's. Llama 8082 is left out on purpose: it serves only Inkling, which HUB-39 K2/K3 ran beside ComfyUI with no error, and blocking ComfyUI while Inkling is loaded would stop VN/Edu from making pictures after a review |
| 12 | The hub ticket folder has no changelog.md | BUILD | HUB-40 H3 | `.claude/tickets/HUB-38-acp-for-all/` has none (HUB-39 has one) |
| 13 | BT doc comment of `defaultsSchema` above `LOCAL_MODEL_REF` | BUILD | BTT-37 | `src/shared/schemas.ts:129` |
| 14 | BT test compares against the constant | BUILD | BTT-37 | `tests/dispatcher.test.ts:961` `toEqual([...DEFAULT_FALLBACKS])` cannot catch a wrong constant |
| 15 | Stale portable proxy `D:\Programs\ACP-Proxy` auto-started | NO CHANGE | - | read-only look: the folder holds only `ACP-Proxy-Portable-0.1.0-x64.exe` (2026-11-21 21:28); no shortcut in the user or common Startup folder (only RustDesk), no HKCU/HKLM Run or RunOnce entry, no scheduled task, no running process from that folder. Nothing starts it; nothing to delete |
| 16 | Pixel MCP cannot run the artist agent or list models (C7) | NEEDS USER | - | not a thin wrapper: the MCP server only carries the drawing tools (`src/main/mcp.ts`, host from `ToolBridge`), the `AgentRunner` and `LlmService` exist only in the windowed app (`src/main/agentIpc.ts:40`, Electron `BrowserWindow` emit), and headless mode (`src/main/headless.ts:79`) has neither. Sketch: create `LlmService` and `AgentRunner` in both modes, give the MCP host an `emit` that buffers events per run, and add `agent_send {text, model?}` (returns a run id), `agent_status {runId}` (state, last events, result) and `models_list` (from `llm.overview()`); about 4 files plus tests. User decides whether C7 is worth that |
| 17 | Proxy usage `reasoning_tokens` 0 with reasoning present | BUILD | AAP-44 | `src/providers/local-openai.ts:231` takes `thoughtTokens` only from upstream `completion_tokens_details`, which llama-server does not send, so `src/usage.ts:14` reports 0 |
| 18 | nomic GGUF context 2048, larger needs rope flags | BUILD (2048 part only) | AAP-44 | verified from the file's own metadata (`D:\LlamaCpp\models\nomic-ai\nomic-embed-text-v1.5-GGUF\nomic-embed-text-v1.5.Q4_K_M.gguf`: `nomic-bert.context_length = 2048`, `embedding_length = 768`); the rope-scaling claim is not in the metadata and was not verified, so it is not written |
| 19 | Restart the embed server when file, port or context changes | BUILD | AAP-44 | `src/electron/main.ts:312-317` saves and refreshes settings but leaves a running `embed` process on its old args and port; `embedHost.ensureRunning` (`:166`) then returns early |
| 20 | "Used by" entry for the embedding file | BUILD | AAP-44 | `src/renderer/llama-models.ts:83` `usedBy` looks only at profiles; called at `llama-view.ts:255` |
| 21 | AAP-43 discoveries.md still says 512 tokens | BUILD | AAP-44 | `.claude/tickets/AAP-43-local-embeddings/discoveries.md:2`; resolved by `-c ctxSize*maxConcurrent` (`src/llama-args.ts:62`) |
| 22 | Assert the 768 dimension | BUILD | AAP-44 | `local-openai.ts` `embed` checks only that vectors are non-empty numbers; a wrong file would make Scriptorium drop its whole index (`ensureDim`, `memory/index.ts:102-111`). Setting `dimensions` default 768, 0 = not checked |
| 23 | Embedding port not checked against 8787 | BUILD | AAP-44 | `src/settings.ts:336-339` compares with gufo, strata and llama ports only |
| 24 | Scriptorium chunker has no hard cap | BUILD | SCP-66 | `src/engine/memory/index.ts:34-56`: a paragraph > 1800 chars is cut only at `.!?`, so an unpunctuated run stays one chunk; the embedder takes 2048 tokens. Cap 1800 chars |
| 25 | Junk `---` chunks from separators | BUILD | SCP-66 | front matter is stripped (`parseMd`, `:249`), but chapters keep scene breaks `---` (e.g. 6-8 per chapter in `books/the-clockless-god-3/chapters`); a lone `---` becomes a chunk at a long-paragraph border. Drop paragraphs with no letter or digit |
| 26 | Files changed since 2026-11-16 stale in the index | NEEDS USER | - | needs a reindex of `~\Scriptorium` with the proxy's embedding server up; Scriptorium must never be started without asking (N2) |
| 27 | services.json `lmstudio` `start` points at missing `lms.exe` | BUILD | HUB-40 H2 | `services.json:157`; `~\.lmstudio\bin\lms.exe` does not exist; `startWhenSilent` (`:154`) only makes sense with a start |
| 28 | `inkling-2-mini-dspark` profile points at a missing file | NO CHANGE | - | the user's settings (`%APPDATA%\api-acp-proxy\settings.json`, read only) now give both profiles `ggml-org/Inkling-2-Mini-GGUF/Inkling-2-Mini-IQ4_NL.gguf` (on disk), dspark keeps `unsloth/.../mmproj-F16.gguf` and `dspark-Inkling-2-Mini-Q8_0.gguf` (both on disk). The repo presets (`src/settings.ts:134-149`) are self-consistent defaults for any machine |
| 29 | Profile label "(Q8_0, vision)" and hf `quant` do not match the disk | NO CHANGE | - | user's settings: label is now "Inkling 2 Mini (Q4_0, vision)" for an IQ4_NL file, and both `hf.quant` still say `Q8_0` / `UD-Q8_K_XL`; `hf` is only used by "Find on Hugging Face" when a file is missing. The user's file, not the repo's; reported, not changed |
| 30 | `reasoning_effort: none` does not stop Inkling's thinking | DONE ALREADY | HUB-39 | V1 sends `chat_template_kwargs: { reasoning_effort: none }` (VN/Edu/Cartoon seeds `providers.md:175-181`); K1 PASS |
| 31 | Critic cut-off answers need max_tokens headroom | DONE ALREADY | HUB-39 | VN `art-critic.ts:45` and Edu `media.ts:516` ask 2000; K2-K4 max 1467 |
| 32 | `lmstudio` in the vision role lists of VN, Edu, Cartoon, Pixel | DONE ALREADY (VN, Edu, Cartoon); NEEDS USER (Pixel) | HUB-39 | VN/Edu/Cartoon name `acp/llama/inkling-2-mini`. Pixel's alias `lmstudio` (`seed/config/roles.md:6`, "tools and vision, for the model picker") would need Inkling in JSON-action mode with images: the user picks, and it needs a live check |
| 33 | Inkling needs `extra_body` inside `chat_template_kwargs`; llama rows carry none | DONE ALREADY (VN, Edu, Cartoon); NO CHANGE (the other four) | HUB-39 | in Scriptorium, BT, Pixel and Chiptune no role names Inkling (listed, not default) |
| 34 | Strata thinks when a caller omits `reasoning_effort`? | NEEDS A RUNNING SERVICE | - | needs the proxy and a Strata load (GPU); command in N3 |
| 35 | Misleading `lmstudio` seed comment ("add a vision model you have in LM Studio") | BUILD | VNO-69, EGS-73, CTS-56 | `seed/config/providers.md:80-83` in all three |
| 36 | Edu has no test of `roleModelRefs('art-critic')` | BUILD | EGS-73 | `tests/models.test.ts:58` checks only the raw list; one assertion after `:59` |
| 37 | Cartoon ROADMAP CTS-55 "Planned" | BUILD | CTS-56 | `ROADMAP.md:95` says Planned and "Live check UNTESTED (hub K4)"; merged (`9105b04`) and K4 PASS |
| 38 | Live `roles.md` prose still pre-HUB-38 | BUILD | HUB-40 L1 | diffed live prose against the seeds: VN one paragraph, Edu three blocks; Cartoon already the same |
| 39 | VN art-critic false-rejects sprites on grey | BUILD | VNO-69 | `art-critic.ts:23` flattens on `#808080`, `seed/prompts/art-critic/review_image.md:18` asks for "plain light background". Edu flattens on white (`media.ts:502`) and its prompt asks for no background: no mismatch. Cartoon flattens on grey (`tasks.ts:221`) but its prompts never ask for a background colour; the pose sheets are references: no mismatch |
| 40 | Pin the language of the critic notes | BUILD | VNO-69, EGS-73, CTS-56 | no critic prompt names a language (VN `review_image.md`, Edu `art-critic/review.md`, Cartoon `frame-critic/clip-review.md`, `frames.md`, `frames-3d.md`); one sentence each |

The live prompt files of VN, Edu and Cartoon are the same as their seeds and are recorded in each folder's `.seed-hashes.json`, so `initDataFolder` replaces them with the new seed version on the next app start (`src/engine/store/seedRefresh.ts`). No hand edit of live prompts is planned; L2 only checks it.

## Files and modules to touch (hub only)

| file | line (verified) | change |
|---|---|---|
| `scripts/hub.ps1` | 12 (header), 317-366 (`Start-Service1`), 328-329 (comment) | H1 |
| `services.json` | 147-159 (`lmstudio`) | H2 |
| `README.md` | 44 (table row `lmstudio`), 65 (comment line) | H2 |
| `.claude/tickets/HUB-38-acp-for-all/changelog.md` | new | H3 |
| `ROADMAP.md` | new row 33 after row 32 (line 44) | H4 |

Do not touch the uncommitted HUB-39 files in the working tree (`.claude/tickets/HUB-39-vision-fallback-inkling/events.jsonl`, `plan.md`, `discoveries.md`, `runs/hub-39-vision-checks.md`): they belong to the director; leave them out of the HUB-40 commit.

## Tasks for workers (hub, branch `HUB-40_extra-ideas`)

**H1 `scripts/hub.ps1`: a cycle guard for `requires`, `-Window` only for the services named on the command line, and no start command.**
- `function Start-Service1($s)` becomes `function Start-Service1($s, [string[]]$Chain = @(), [bool]$Named = $true)`.
- At the top of the function: if `$Chain -contains $s.id`, print `"$($s.id): requires cycle $(($Chain + $s.id) -join ' -> '), skipped"` in yellow and `return`.
- The `requires` loop (lines 340-346) calls `Start-Service1 $rs ($Chain + $s.id) $false`.
- Line 358 `if ($Window) {` becomes `if ($Window -and $Named) {`. The "-Window has no effect" line (366) then prints only for a named service.
- After the variant block (after line 354): if `-not $st` (no `start` in services.json), print `"$($s.id): no start command in services.json; start it yourself"` and `return` (today it would wait `WaitSeconds` for nothing).
- Comment at lines 328-329: "A service whose start is safe to repeat (LM Studio's `lms server start`) is started again" becomes "A service whose start is safe to repeat (`startWhenSilent` in services.json) is started again".
- Header line 12: append "; -Window applies only to the services named, not to the ones they require".
- The two callers in the `switch` (`'start'`) stay `Start-Service1 $s` (defaults: named).
- Check: `pwsh -NoProfile -Command "$null = [System.Management.Automation.Language.Parser]::ParseFile('scripts/hub.ps1', [ref]$null, [ref]$e); $e"` prints nothing. Then a dry run that starts nothing: copy the script to `.claude/temp/hub40/scripts/hub.ps1` and write `.claude/temp/hub40/services.json` with two services `{ "id": "a", "port": 65011, "requires": ["b"], "start": { "kind": "none" } }` and `{ "id": "b", "port": 65012, "requires": ["a"], "start": { "kind": "none" } }` (plus `"services"` wrapper; ports that nothing listens on); run `pwsh -File .claude/temp/hub40/scripts/hub.ps1 start a -Window -WaitSeconds 1`. Expected: "a: requires b", "b: requires a", "a: requires cycle a -> b -> a, skipped", one "a: -Window has no effect" line and none for b, then two "not listening after" lines and a status table. Delete `.claude/temp/hub40` afterwards (it is scratch).

**H2 `services.json` and `README.md`: LM Studio has no start command.**
- `services.json` `lmstudio` entry: remove the `"startWhenSilent": true,` line (154) and the `"start": {...}` line (157). Keep every other field and the `note` as it is.
- `README.md:44`, last cell of the `lmstudio` row: `` `lms server start` `` becomes `none (not installed)`.
- `README.md:65`: "a port that listens while the service's http URL does not answer shows as `no-http` (e.g. LM Studio's app with its API server off); `start <id>` fixes LM Studio (`startWhenSilent`)" becomes "a port that listens while the service's http URL does not answer shows as `no-http`; `start <id>` repeats the start of a service marked `startWhenSilent`, and reports the others".
- Check: `node -e "JSON.parse(require('fs').readFileSync('services.json','utf8'))"` (Node under fnm: in Bash `export PATH="/c/Users/Infplane/AppData/Roaming/fnm/aliases/default:$PATH"`); `pwsh -File scripts\hub.ps1 status` still lists `lmstudio` (status is read-only, starts nothing); `grep -n "lms.exe\|lms server" services.json README.md scripts/hub.ps1` finds nothing.

**H3 `.claude/tickets/HUB-38-acp-for-all/changelog.md` (new).** A short record in the style of `.claude/tickets/HUB-39-vision-fallback-inkling/changelog.md`: the repo tickets of HUB-38 with their merge commits (read `git log --oneline --merges -3` in each repo: api-acp-proxy AAP-42 and AAP-43, scriptorium SCP-65, book-translator BTT-36, visual-novels-orchestrator VNO-67, pixel-art-generator PAR-19, midi-generator MDI-18, edu-game-studio EGS-71, cartoon-studio CTS-54) and the hub commit `16713ea`; the live data steps and checks as REQ-0030's Log and the `.bak-HUB-38` files record them (list only what is recorded there; write UNTESTED for any check the log does not mark as passed). Only facts found in those sources, no new claims.

**H4 `ROADMAP.md` row 33** (after row 32, same columns):
`| 33 | HUB-40 | Extra ideas of REQ-0030: hub.ps1 cycle guard and -Window scope, LM Studio start removed, stale prose (Strata paths, -low, LM Studio comments), probe and test fixes, Scriptorium seed and chunker, autostart sees Gufo, critic prompts (VN sprite on grey, notes in English), proxy embedding guards and reasoning_tokens (.claude/tickets/HUB-40-extra-ideas/plan.md, REQ-0030) | scriptorium (SCP-66), book-translator (BTT-37), visual-novels-orchestrator (VNO-69), edu-game-studio (EGS-73), cartoon-studio (CTS-56), pixel-art-generator (PAR-20), midi-generator (MDI-19), api-acp-proxy (AAP-44), hub | none | Planned |`

The hub has no test suite. Check: `git diff` shows only these files; `services.json` parses; the H1 dry run output as described.

## Live data steps (after the repo tickets merge; each with the user's go-ahead; the hub does them, never a repo ticket)

**L1 Live `roles.md` prose (idea 38).** Prose only; the YAML front matter stays byte for byte.
- If VN Studio or Edu Studio runs, stop it first (`pwsh -File scripts\hub.ps1 stop vn-studio edu-studio`, a service stop: go-ahead). Copy each file to `<file>.bak-HUB-40` before editing (the `.bak-HUB-38` and `.bak-HUB-39` files stay).
- `C:\Users\Infplane\VisualNovels\config\roles.md`: the paragraph that starts "The aliases `paid`, `strata` and `lmstudio` stand for" (prose line 5, file line 25 on 2026-11-22) becomes the same paragraph of `C:\projects\Personal\visual-novels-orchestrator\seed\config\roles.md` (it starts "The aliases `paid`, `acp` and `lmstudio`"), copied as it is.
- `C:\Users\Infplane\EduGames\config\roles.md`, four places, each replaced by the matching text of `C:\projects\Personal\edu-game-studio\seed\config\roles.md`: the "The aliases `paid`, `strata` and `lmstudio`" paragraph (file line 51); the `researcher` bullet (line 56, "Checks and notes use Strata with thinking on `low`."); and the four bullets at lines 77-80 ("Writers and designers ...", "Researcher and fact-checker ...", "Other reviewers and the playtester ...", "After a role's Strata and LM Studio entries ...").
- `C:\Users\Infplane\CartoonStudio\config\roles.md`: nothing (its prose equals the seed's).
- Verify: `git diff --no-index <file>.bak-HUB-40 <file>` shows only those prose lines; then a prose diff against the seed (the awk in this plan's research: print everything after the second `---`, strip CR) shows no difference. Find each place by its text, not the line number. Restart the apps that were running (go-ahead).

**L2 Prompt refresh check (ideas 39, 40).** After VNO-69, EGS-73 and CTS-56 are merged and the three apps rebuilt (`hub.ps1 build vn-studio edu-studio cartoon-studio`) and restarted (go-ahead): compare each live prompt with its new seed (CR stripped): `VisualNovels\prompts\art-critic\review_image.md`, `EduGames\prompts\art-critic\review.md`, `CartoonStudio\prompts\frame-critic\clip-review.md`, `frames.md`, `frames-3d.md`. Equal = the seed refresh worked. If one differs and the app's seed notes list it as "update available", copy the seed file over it after a `.bak-HUB-40` backup, and record that in the run log.

Record L1, L2 and N1-N4 in `runs/hub-40-extra-ideas.md` (ids, times, results).

## Checks that need a running service or the user (not built; run only on the user's word)

- **N1 VN sprite review on Inkling (GPU, idea 39).** After L2: in the K2 throwaway project `C:\Users\Infplane\VisualNovels\projects\hub39-critic-check`, regenerate and review `sprite_mara_neutral` (`vno_asset_generate {slug: "hub39-critic-check", only: ["sprite_mara_neutral"]}`, `vno_wait`). Passes when the review no longer rejects for the grey background, and its `problems` are English.
- **N2 Scriptorium re-index (idea 26).** With the user's go-ahead only, Scriptorium closed, and the proxy's embedding server enabled: `npm run engine -- reindex --data C:\Users\Infplane\Scriptorium` from `C:\projects\Personal\scriptorium` after SCP-66 is merged and built. A plain `reindex` embeds only new and changed files, and those get the new chunk borders (no `---` chunks, long runs capped). Unchanged files keep their old chunks; nothing is duplicated or invalidated, the index is just mixed. To get the new borders everywhere, delete `C:\Users\Infplane\Scriptorium\index\library.sqlite` first (the index is a rebuildable cache), which embeds the whole library again through the proxy. That is a second, separate decision for the user (time on the GPU, never a paid model). It embeds through `acp/llama/nomic-embed-text-v1.5`. It never starts the book factory, but it writes `~\Scriptorium\index\library.sqlite`: the user decides.
- **N3 Strata thinking without `reasoning_effort` (idea 34; GPU: may switch the proxy from Llama to Strata).** Two calls, then compare `choices[0].message.reasoning_content` and `usage.completion_tokens`:
  `curl -s http://127.0.0.1:8787/v1/chat/completions -H "content-type: application/json" -d "{\"model\":\"strata/qwen3.8-flash-next-unsloth-ud-iq4_xs\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the word OK.\"}],\"max_tokens\":200}"`
  and the same body with `,\"reasoning_effort\":\"none\"` added. (Add `-H "Authorization: Bearer <key>"` only if the proxy has `server.apiKey` set.) Thinking is on by default when the first answer has `reasoning_content` or many more completion tokens than the second. If so, every caller already sends `reasoning_effort: none` on the strata rows (the seeds' `extra_body`); write the finding in the run log and open a follow-up only if a caller without it is found.
- **N4 Pixel MCP for the artist agent (idea 16) and Pixel's vision rows (idea 32).** The user decides whether to plan them (sketch in the triage table).

## Acceptance criteria and the test that proves each

| # | criterion | proof |
|---|---|---|
| A1 | `hub.ps1 start` stops at a `requires` cycle with a message and never recurses forever | H1 dry run output |
| A2 | `-Window` affects only the services named on the command line | H1 dry run: one "-Window has no effect" line, for `a` only |
| A3 | A service without `start` is reported, not waited for | H1: `start lmstudio -WaitSeconds 1` prints "no start command" at once (lmstudio is not running; nothing is launched) |
| A4 | `services.json` has no `lms.exe` and parses; README says so | H2 checks |
| A5 | HUB-38 has a changelog that cites only recorded facts | review against REQ-0030 Log and the repos' merge commits |
| A6 | ROADMAP row 33 present | `git diff ROADMAP.md` |
| A7 | Live `roles.md` prose equals the seeds, front matter unchanged | L1 diffs |
| A8 | Each repo ticket passes its own plan's criteria | the repo plans |

## What stays UNTESTED

- N1-N4 until the user says go (the prompt change is proven only by tests and text until N1 runs).
- The `-Window` behaviour with a real Electron service (the dry run uses fake services).
- Each repo plan lists its own UNTESTED items (Electron wiring of AAP-44's embed restart, the desktop pages, live app runs).
