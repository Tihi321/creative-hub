---
status: done
request: REQ-0031
repos: [creative-hub, api-acp-proxy, pixel-art-generator, visual-novels-orchestrator, edu-game-studio, scriptorium, midi-generator]
branch: HUB-44_pending-ideas
updated: 2026-11-22
---

# HUB-44 The pending ideas of REQ-0030, planned: small builds in six repos, three hub.ps1 fixes, one round of rebuilds, live steps and live checks

Source: the handoff `C:\projects\Personal\creative-hub\.claude\tickets\HUB-44-pending-ideas\handoff.md` (42 ids, P-01 to P-42). The user's words (2026-11-22): "i want handoff for all pening ideas as i want to implement them just in new session". This plan triages all 42, plans the code in each repo's own ticket, and merges every live step into one round.

Every item was checked on 2026-11-22 against master: creative-hub ab71ba7, pixel-art-generator 5778801, visual-novels-orchestrator 12ee5c5, edu-game-studio 7d93579, cartoon-studio 5635447, scriptorium 980e415, midi-generator 9981150. Strata's source `D:\Strata\terminal\serve\server.py` was read. Nothing was started, stopped, built or called; the live data folders were only read (the 8 queued VN job files listed, seed and live prose diffed with `git diff --no-index`).

Decisions that bind this plan (the user, 2026-11-22): P-15 "Guard, then test" (the guard now; Strata's Pixel row becomes `vision: true` only if three live vision runs in a row finish, as a later, separate change); P-17 "Build, default off"; P-31 "Yes, with a backup"; P-23 "Yes, to the Recycle Bin". Director defaults shown with this plan: P-18 New chat unchanged; P-19 no change; `edu_stop_now` unchanged; P-39 DONE (the `.bak-HUB-*` backups went to the Recycle Bin on 2026-11-22).

## Triage (all 42)

Verdicts: IN (built by the ticket named), NO CHANGE (evidence given), LIVE (a step of this plan's live round), USER'S EYES (only a person can read it), DONE, OUT (not in this build, reason given).

| id | idea (short) | verdict | ticket | reason (verified 2026-11-22) |
|---|---|---|---|---|
| P-01 | Gufo status tiles; Gufo vision flag from `input_modalities` | OUT (build); LIVE (probe) | AAP-51; K8 | no Gufo endpoint is known; probe P1 (GET only) first, then AAP-51's plan maps only what Gufo answers |
| P-02 | refresh Strata's model list and vision flag at Strata ready | IN | AAP-51 | subject to `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-51-pending-ideas\plan.md` |
| P-03 | VRAM "GB" computed as GiB | IN | AAP-51 | as above |
| P-04 | export `spark()` and test it | IN | AAP-51 | as above |
| P-05 | reason texts and dots on the Monitor | IN | AAP-51 | as above |
| P-06 | outside Llama server's model id from `/props` | IN | AAP-51 | as above |
| P-07 | the render-error state: check what remains | NO CHANGE (code); USER'S EYES | AAP-51; K9 | AAP-49 built the render-error notice; AAP-51's plan has no change; only the window look is open (K9) |
| P-08 | two `applySettings` calls skip `refreshLocalSettings` | IN | AAP-51 | as above |
| P-09 | `readText` caps the body only after reading | IN | AAP-51 | as above |
| P-10 | a JSON answer on Strata's or Llama's port shown as a model | IN | AAP-51 | as above |
| P-11 | Usage page inline sizes from script | IN | AAP-51 | as above |
| P-12 | build gate for a llama-server without `--metrics` | OUT | AAP-51 | both installed builds support the flag; low value |
| P-13 | Strata `/v1/telemetry`, `/v1/status` as Monitor sources | NO CHANGE (closed) | AAP-51 | HUB-43 row 2a: every number is already in `/metrics` |
| P-14 | small proxy leftovers (D40, D41, D42) | IN | AAP-51 | subject to that plan |
| P-15 | Strata as Pixel's vision model | IN (guard, part A); LIVE (K5); part B after K5 | PAR-25 | K3 run 1 redrew one 16-row grid about 18 times to `max_steps`: a "same picture twice: stop" guard (`src/llm/agent.ts:324-379`); the seed row and a migration only after three vision runs in a row finish, as PAR-25 part B with its own go-ahead (B1) |
| P-16 | steer a run's first step to a warm Strata slot | OUT | - | a design is needed: see "P-16: what a design needs" below |
| P-17 | slimmer tool list, `agentToolSet: 'no-files'` | IN | PAR-25 | optional key in `config/app.json` (`src/main/appSettings.ts:7-33`), default `all`; the system prompt says which guide tools are off, so the guide does not contradict the mode; live run K6 |
| P-18 | New chat aborts a running MCP run | NO CHANGE | - | the director's default; documented (Pixel `README.md:50`, `src/renderer/state/chat.ts:133-141`) |
| P-19 | `before-quit` does not wait for the chat save | NO CHANGE | - | the director's default; only a window closed mid-run loses that chat; headless waits (`src/main/headless.ts:127`) |
| P-20 | event buffer drops early usage; one extra Strata request | NO CHANGE | - | run totals come from the `done` event (`src/main/agentMcp.ts:116-124`), not the 200-event buffer; the extra request is most likely a JSON repair or schema-less retry (`src/llm/json.ts:50-55,66-79`) or a router retry (`src/llm/router.ts:102-149`): the step count does not count those; K5 records Strata's request count per run (see Discoveries) |
| P-21 | `stripTextNegations` never exercised live | IN (a log line) + LIVE | VNO-73; K4 | the stripped prompt is drawn (`src/engine/vn/handlers.ts:596-598`) but nothing records a removal: VNO-73 logs it; K4 reads it if the critic writes "no text" |
| P-22 | the lost final full stop | IN | VNO-73 | `src/engine/assets/derive.ts:61` empties the last kept clause's separator, so "A street. No text." becomes "A street" |
| P-23 | 8 queued VN job files that never finish | LIVE | K2 | 8 files in `C:\Users\Infplane\VisualNovels\jobs\queued` (7 `hub07-flow-test--*--r2`, 1 `hub08-13-autostart--vn.build--regen-sfx_bell--r4`), `jobs\running` empty; removing a queued file under the running engine is safe (K2) |
| P-24 | `vno_wait` progress events instead of the 240 s cap | OUT | - | small in code (`src/engine/mcp/server.ts:35` would pass the handler's `extra` to `callTool`, `tools.ts:399`, and `vno_wait`, `tools.ts:345-351`, would send `notifications/progress`), but useless unless the client sends a `progressToken` and resets its idle timer on progress (the MCP SDK client's `resetTimeoutOnProgress` is off by default); neither can be verified from VN's code, and the 240 s cap with a repeated call already works |
| P-25 | Edu's and Cartoon's critics redraw from a revised prompt? | IN (Edu); NO CHANGE (Cartoon); LIVE (K4) | EGS-76 | Edu appends "Correct this: <note>" with the critic's `fix` to the positive prompt (`src/engine/edu/pipeline-handlers.ts:855-858`, `src/engine/assets/generate.ts:301`) and its seed asks for "no text in the picture" (`seed/prompts/art-critic/review.md:17`): EGS-76 changes the prompt and strips text negations from a fix. Cartoon never redraws from a review (`src/engine/pipeline/handlers.ts:578-606`, `media.ts:41-60,175-181`; `GenerateClipArgs` has no fix field, `clips.ts:238-250`) |
| P-26 | Gufo by health URL in autostart; `edu_stop_now`; Edu revise count | OUT / NO CHANGE | - | Gufo URL: OUT until K8 gives the endpoint; `edu_stop_now` pauses the whole queue (`src/engine/mcp/tools.ts:152-160`, `engine.ts:267-276`), unchanged (director's default); 6 revise verdicts but 3 sent: `countsAsRevise` sends a non-must-pass revise only below `revise_below` 7 (`src/engine/review/scoring.ts:144-149`; HUB-39 log line 50 gives relevance 7 for the three unsent) |
| P-27 | Edu and Cartoon live checks after their rebuilds | LIVE | K1, K3, K4 | (a) prompts refreshed on start, (b) English critic notes, (c) ComfyUI free on an empty reply, (d) the Gufo-aware autostart check |
| P-28 | Edu `yarn test` flake | IN (a check) | EGS-76 | three full runs recorded; a fix only if a cause shows (`tests/pipeline.test.ts` has no timer or sleep) |
| P-29 | Cartoon NEVER_STARTED comment omits Gufo | NO CHANGE | - | Gufo is not a service in `services.json` and `canStart` refuses anything outside `KNOWN_SERVICES` (`['comfyui']`, cartoon-studio `src/engine/studios/autostart.ts:19,122-123`); the comment (`:20`) is right; Gufo is a GPU holder (`:28-32`) |
| P-30 | Edu and Cartoon live prose | LIVE | L1-L3 | read-only diffs today: Edu live `providers.md` prose differs from the seed's (6 hunks; live says "no vision", lacks the ACP and Inkling lines); Cartoon live `providers.md` (3 hunks, older "(Strata, LM Studio)" text, no ACP proxy section) and `settings.md` (3 lines naming `strata` where the seed names `acp`); Edu `roles.md`, `settings.md` and Cartoon `roles.md`, `autostart.md` equal |
| P-31 | full Scriptorium re-chunk | LIVE | K7 | the user's yes with a backup |
| P-32 | stale `index\engine.lock` (pid 19260) | LIVE (Scriptorium word only) | K10 | proved only by a Scriptorium start |
| P-33 | three Strata sentences dropped from live `providers.md` | NO CHANGE | - | the backups are in the Recycle Bin (not found on disk); judged from the seeds and Strata's code: "loading 1 to 3 minutes, `loaded: true`" and "context must match `--max-context`" are still in VN's seed (`seed/config/providers.md:243,246`; `/health` `loaded`, `server.py:6946`; prompts checked against `max_context`, `server.py:5092-5104`); "one model per process" is VN's `:242` and Scriptorium's "one model at a time" (`:253,260`); "the model field is ignored" is not exactly true (`server.py:4190-4195` serves any name; `/v1/load` refuses an unknown one, `:7112-7113`), and since HUB-38 apps talk to the proxy, which routes by id. Nothing worth putting back |
| P-34 | Scriptorium reading its new prose | LIVE (Scriptorium word only) | K10 | it reads them only on start |
| P-35 | small Scriptorium items | IN (3 of 5) | SCP-69 | `lms load` example names the embedding model (`seed/config/providers.md:315`); adapt test reads `book.md` right after the slug dir appears (`tests/adapt.test.ts:433-434`); `yarn test <file>` runs everything (`package.json:16`). `splitLong` max 1 and the emoji-only drop: NO CHANGE (SCP-69 table) |
| P-36 | the start-time lock removal on a real lock | LIVE | K1 | real stale locks today: Edu 25460, Cartoon 10856, Pixel 32952 (Scriptorium 19260 in K10) |
| P-37 | `Clear-StaleLock` only tested under pwsh 7 | IN | HUB-44 H1 | `hub.ps1` already needs PowerShell 7: `-SkipHttpErrorCheck` (`scripts/hub.ps1:113,186,536`) does not exist in Windows PowerShell 5.1; nothing runs it with `powershell.exe` (grep over `C:\projects\Personal`); so `#Requires -Version 7.0` makes it refuse 5.1 up front |
| P-38 | a distinct "time has no zone" message | IN | HUB-44 H2 | a zoneless or out-of-range lock time falls through to the generic "held by running pid ... left" (`scripts/hub.ps1:463-481`) |
| P-39 | `.bak-HUB-*` backups in the live folders | DONE | - | sent to the Recycle Bin on 2026-11-22 (the director) |
| P-40 | `start` shows another pid for acp-proxy than `status` | IN | HUB-44 H3 | `start` prints the `cmd.exe` launcher's pid (`Start-Detached`, `scripts/hub.ps1:299-315,412-413`); `status` shows the port's owner (`Get-Owner`, `:123-129,268`), which `stop` walks up from (`:513-521`); status is right; start will print both |
| P-41 | Genesis perf test margin | IN | MDI-21 | `tests/core/synth/genesis.test.ts:612` says 3.0-3.2 s; unloaded about 1.4 s, so 4 s catches about 3x |
| P-42 | UNTESTED lists (proxy window and others) | USER'S EYES | K9 | the list for the user to read in the proxy window; the rest goes to the checks named in K9 |

## Tickets (ids checked in the handoff, section 1, and again in each repo's `ROADMAP.md` and `.claude/tickets` on 2026-11-22)

| ticket | repo | branch | plan | order |
|---|---|---|---|---|
| AAP-51 | api-acp-proxy | `AAP-51_pending-ideas` | `C:\projects\Personal\api-acp-proxy\.claude\tickets\AAP-51-pending-ideas\plan.md` (another planner) | any |
| PAR-25 | pixel-art-generator | `PAR-25_repeat-guard-tool-set` (part A); `PAR-25_strata-vision` (part B, only after B1) | `C:\projects\Personal\pixel-art-generator\.claude\tickets\PAR-25-repeat-guard-tool-set\plan.md` | any; part B after the live round |
| VNO-73 | visual-novels-orchestrator | `VNO-73_negation-full-stop` | `C:\projects\Personal\visual-novels-orchestrator\.claude\tickets\VNO-73-negation-full-stop\plan.md` | before EGS-76 if possible (EGS-76 copies its function) |
| EGS-76 | edu-game-studio | `EGS-76_critic-fix-negations` | `C:\projects\Personal\edu-game-studio\.claude\tickets\EGS-76-critic-fix-negations\plan.md` | after VNO-73, or applies the same fix itself |
| SCP-69 | scriptorium | `SCP-69_small-leftovers` | `C:\projects\Personal\scriptorium\.claude\tickets\SCP-69-small-leftovers\plan.md` | any |
| MDI-21 | midi-generator | `MDI-21_perf-margin` | `C:\projects\Personal\midi-generator\.claude\tickets\MDI-21-perf-margin\plan.md` | any |
| HUB-44 | creative-hub | `HUB-44_pending-ideas` | this file | H1-H4 any time; the live round after every merge |

No ticket: cartoon-studio (P-25 and P-29 need no change; P-27 and P-30 are live steps) and book-translator (no item). CTS-59 and BTT-38 stay free.

Notes every worker gets: the proxy runs from api-acp-proxy's `dist/` and VN Studio from its `out/`; both may be RUNNING: no build on a branch there (tests, typecheck, lint only). Pixel, Edu and Cartoon run from `out/` when up: no build on a branch either. `%APPDATA%\api-acp-proxy\settings.json` is never edited. Bash: `export PATH="/c/Users/Infplane/AppData/Roaming/fnm/aliases/default:$PATH"` first (`fnm exec yarn` fails). Backslashes and regexes go through the Edit or Write tool, never a Bash heredoc. CRLF working trees: no line-ending flips. Tests per test-discipline, each new test shown failing first. Live data folders under `C:\Users\Infplane\` are only touched by this plan's live round, with a backup beside each edited file.

## P-16: what a design needs (OUT of this build)

K4 of HUB-43 showed that inside a run Strata reuses about 99% of the prompt from step 2, but a new run's first step reused 0 tokens in 3 of 4 runs (about 70 s of prefill for 34,300 tokens) because it lands on whichever of Strata's 4 slots is free, and the conversation cache never restored (14 parks, 0 restores). A design would need: (1) whether Strata can be told which slot or cached prefix to use; the one lever found in its code is the request field `strata_prefix` (`D:\Strata\terminal\serve\server.py:5151-5170`, engine `pin=N` at `:1329-1335`), which pins a shared prefix's checkpoint so it is never evicted, but it is ignored for any request with images (`:5168-5170`, every vision step has one) and it is not known whether a pin serves every slot or only one; (2) whether the proxy passes an unknown body field through to Strata (Pixel could send it in the row's `extra_body`, `seed/config/providers.md:141`); (3) a measurement over several back-to-back runs of the first step's `reused` in Strata's `/metrics` `requests[]`, with and without the field. That is a probe and a proxy question first, not a Pixel build; see Extra ideas.

## Hub tasks (branch `HUB-44_pending-ideas`)

The hub has no test suite. Line numbers are from master ab71ba7; find each place by its text. Checks for H1-H3 use a copy of the script in `.claude/temp/hub44/` with a fake service (as HUB-43 H1), never a real app.

**H1 `scripts/hub.ps1` needs PowerShell 7 (P-37).**
- Line 22 (the blank line before `param(`, `:23`): add `#Requires -Version 7.0` on its own line.
- Header: after line 4 add `# Needs PowerShell 7 (pwsh): it uses Invoke-WebRequest -SkipHttpErrorCheck and pwsh 7's ConvertFrom-Json dates; Windows PowerShell 5.1 refuses to run it.`
- Check: `powershell.exe -NoProfile -File scripts\hub.ps1 status` prints the `#requires` error, runs nothing and exits non-zero (record the exit code); `pwsh -NoProfile -File scripts\hub.ps1 status` runs as before (read-only).

**H2 A distinct message for a lock time that cannot be read (P-38).** In `Clear-StaleLock` (`:432-485`), inside `if ($AtStart) {` (`:457`):
- After `$began = $null; $t = $null` (`:461`) add `$why = if (-not $stamp) { 'it has no time' } else { $null }`.
- In the stamp branch (`:463-473`): when `$stamp` is a `[datetime]` of Kind `Unspecified`, or a `[string]` that does not match the zoned pattern (`:467`), set `$why = "its time $stamp has no zone"`; in the `catch` (`:470`) set `$why = "its time $stamp could not be read"`; when the plausible-range check (`:472`) clears `$t`, set `$why = "its time $stamp is outside 2001-2100"`.
- The `left` line (`:481`) becomes `Write-Host "$($s.id): lock $path held by running pid $lockPid ($($p.ProcessName)), left$(if ($why) { ": $why, so pid reuse cannot be told" })"`. A lock whose time is known and earlier than the process start (`:475`) prints as today (no `$why`).
- The comment (`:458-460`) gains: "The left line says why when the time is missing or unknown."
- Check (dry run, below): case (d) lock `{"pid": <running node pid>, "startedAt": "2026-01-01T00:00:00"}` (no zone) prints "...left: its time 2026-01-01T00:00:00 has no zone, so pid reuse cannot be told" and the file stays; HUB-43's cases (a) dead pid removed, (b) zoned time before the process start removed, (c) zoned time after it left without a reason, still pass.

**H3 `start` prints the pid `status` shows (P-40).**
- `:413` becomes `Write-Host "$($s.id): started (launcher pid $procId), waiting for port $($s.port)..."`.
- `:423`, on success: `$o = Get-Owner $s (Get-Listener $s.port)`; print `"$($s.id): up at $(...) (pid $($o.Pid))"` when `$o -and $o.Pid`, else the line as today. `Get-Owner` is the function `status` uses (`:256,268`), so both show the same pid.
- Check (dry run): `start fake` prints "started (launcher pid A)" and "up at ... (pid B)" with A the `cmd.exe` and B the `node` that listens; then `status` (of the temp copy) shows Pid B for `fake`.

Dry run for H2 and H3 (touches no app): copy `scripts/hub.ps1` to `.claude/temp/hub44/scripts/hub.ps1`; write `.claude/temp/hub44/server.js` (`require('http').createServer((q,r)=>r.end('ok')).listen(65014)`) and `.claude/temp/hub44/services.json` with one service `{ "id": "fake", "port": 65014, "http": "http://127.0.0.1:65014/", "managed": true, "repo": "<abs .claude/temp/hub44>", "data": "<abs .claude/temp/hub44/data>", "lock": "engine.lock", "start": { "kind": "exe", "path": "<abs node.exe of the fnm default alias>", "args": ["<abs server.js>"] } }` (plus any other top-level key the script reads from the real file). Run `pwsh -File .claude/temp/hub44/scripts/hub.ps1 start fake` then `... status` then `... stop fake` for each lock case (a)-(d); for (b)-(d) start a background `node -e "setTimeout(()=>{},120000)"` and use its pid. Record the printed lines in the changelog. Kill the background node; delete `.claude/temp/hub44`. Parse check: `pwsh -NoProfile -Command "$null = [System.Management.Automation.Language.Parser]::ParseFile('scripts/hub.ps1', [ref]$null, [ref]$e); $e"` prints nothing.

**H4 `ROADMAP.md`.** Row 37 after row 36 (line 48), same columns:
`| 37 | HUB-44 | The pending ideas of REQ-0030 (proxy: AAP-51's Monitor and settings leftovers; Pixel: a run that redraws the same picture stops, optional no-files tool set, Strata as vision model only after three live runs; VN: the final full stop of a stripped prompt, a log line for stripped revisions; Edu: critic fixes without text negations; Scriptorium: small leftovers and a full re-chunk; Chiptune: perf test margin; hub.ps1 needs pwsh 7, says why a lock time is unknown, start shows the port owner's pid; live prose of Edu and Cartoon; the 8 stale VN job files) (.claude/tickets/HUB-44-pending-ideas/plan.md, REQ-0031) | api-acp-proxy (AAP-51), pixel-art-generator (PAR-25), visual-novels-orchestrator (VNO-73), edu-game-studio (EGS-76), scriptorium (SCP-69), midi-generator (MDI-21), hub | one round of rebuilds, live steps and checks, each with the user's go-ahead; K10 only on the user's word to start Scriptorium | Planned |`
And the repo table's ACP proxy row (line 128): after "AAP-48, AAP-49 for HUB-43" add "; AAP-51 for HUB-44".

Check for H1-H4: `git diff --stat` shows only `scripts/hub.ps1` and `ROADMAP.md` (plus this ticket's `changelog.md`); the checks above.

## The live round (after every repo ticket is merged; in this order; EVERY step needs the user's go-ahead at run time)

Run log: `C:\projects\Personal\creative-hub\runs\hub-44-pending-ideas.md` (ids, times, commands, outputs, tokens, verdicts, and every deviation). Temp files: `C:\projects\Personal\creative-hub\.claude\temp\hub44-live\`, deleted at the end on the user's word.

Local models only, 0 USD: no paid or cloud model, no Flow, no ElevenLabs, no Gemini. One local model on the GPU at a time; ComfyUI and Inkling share GPU memory; Strata is never started by hand while the proxy holds a local model. A step that loads another local model ends with a tiny chat on the Strata id so the proxy holds Strata again. SVC = starts, stops or restarts a service; GPU = loads a model or uses ComfyUI.

Tiny chats (files written with the Write tool, sent with `curl -s http://127.0.0.1:8787/v1/chat/completions -H "Content-Type: application/json" -d @<file>`, plus the proxy's key header only if the proxy asks for one; never print a key): `tiny-strata.json` = `{"model":"strata/qwen3.8-flash-next-unsloth-ud-iq4_xs","messages":[{"role":"user","content":"Reply with the word OK."}],"max_tokens":50,"reasoning_effort":"none"}`; `tiny-inkling.json` = the same with `"model":"llama/inkling-2-mini"`, no top-level `reasoning_effort` and `"chat_template_kwargs":{"reasoning_effort":"none"}`.

### P0 Preconditions (no go-ahead needed: read-only)

- `pwsh -File scripts\hub.ps1 status`: record every row. Expected from the last round: acp-proxy, comfyui, vn-studio, vibetts up, Strata held by the proxy; Scriptorium, Edu, Cartoon, Pixel, Chiptune, Book Translator down. Anything else: stop and ask.
- `curl -s http://127.0.0.1:8787/healthz`: every provider `active` 0. VN `C:\Users\Infplane\VisualNovels\jobs\running` empty.
- SHA-256 of `%APPDATA%\api-acp-proxy\settings.json` (hash only; it was `1130D968...A8BBA592` on 2026-11-22). Again at the end: must be unchanged.
- The lock files, content recorded: `C:\Users\Infplane\EduGames\engine.lock` (pid 25460), `C:\Users\Infplane\CartoonStudio\state\engine.lock` (10856), `C:\Users\Infplane\PixelStudio\engine.lock` (32952), `C:\Users\Infplane\Scriptorium\index\engine.lock` (`{"pid":19260,"started":"2026-11-21T20:30:48.246Z"}`), `C:\Users\Infplane\VisualNovels\engine.lock` (the running VN's); for each pid, whether a process with it runs now.

### R Rebuilds (SVC; no GPU)

- R1 Proxy (only when AAP-51 is merged): `pwsh -File scripts\hub.ps1 stop acp-proxy`; `pwsh -File scripts\hub.ps1 build acp-proxy` (`npm run build` in the repo); `pwsh -File scripts\hub.ps1 start acp-proxy`. The proxy runs from `dist/`, so it is stopped before the build and started after it. A Strata the proxy started stops with it. Record the start's lines (H3: launcher pid and owner pid) and compare with `status`. Then `tiny-strata.json` (Strata loads, 1 to 3 minutes). Then AAP-51's own live checks, exactly as its plan lists them (for example P-02's image request right after the proxy start), recorded here.
- R2 VN Studio (VNO-73): when `jobs\running` is empty: `pwsh -File scripts\hub.ps1 stop vn-studio`; `pwsh -File scripts\hub.ps1 build vn-studio` (`yarn build:engine`); `pwsh -File scripts\hub.ps1 start vn-studio`. VN runs from `out/`, so it is stopped first. VN's lock: `stop` removes it after the kill once its pid is gone (`scripts/hub.ps1:523`), so the start finds none; record both lines. Then `vno_status {}` answers.
- R3 Pixel and Edu builds (both down): `pwsh -File scripts\hub.ps1 build pixel-studio edu-studio`. Cartoon: no build. It has no ticket in HUB-44, and its last build is current: `out\engine\index.js` was written 2026-11-22 20:11:01 +01:00 (HUB-43 R4), after cartoon-studio master's last commit 5635447 (2026-11-22 19:39:22 +01:00; the last commit touching `src`, `seed` or `package.json` is 18:45:07). At run time the worker checks it again the same way (`(Get-Item out\engine\index.js).LastWriteTime` against `git log -1 --format=%cI`); if master moved past the build, `pwsh -File scripts\hub.ps1 build cartoon-studio` is added before K1. Scriptorium and Chiptune: no build (SCP-69 and MDI-21 change only prose and tests).

### L Live data steps (P-30; Edu and Cartoon down; no GPU)

Rules (as HUB-43 L1): copy the file to `<file>.bak-HUB-44` first; prose only (everything after the second `---` line), found by its text; front matter untouched (SHA-256 of everything up to and including the second `---` line, same before and after); keep line endings and encoding (the live file's CR as it has it); a script (in `.claude/temp/hub44-live/`) that refuses unless the live front matter parses and the seed's prose is read whole; verify with `git diff --no-index --ignore-cr-at-eol -U0 <file>.bak-HUB-44 <file>` and that the new prose equals the seed's (CR stripped). Recompute each diff at run time and show it in the run log before writing.
- L1 `C:\Users\Infplane\EduGames\config\providers.md`: prose becomes the prose of `C:\projects\Personal\edu-game-studio\seed\config\providers.md` (6 hunks today).
- L2 `C:\Users\Infplane\CartoonStudio\config\providers.md`: prose becomes that of `C:\projects\Personal\cartoon-studio\seed\config\providers.md` (3 hunks today).
- L3 `C:\Users\Infplane\CartoonStudio\config\settings.md`: prose becomes that of `C:\projects\Personal\cartoon-studio\seed\config\settings.md` (3 lines today: `acp` where live says `strata`).
Passes when each diff shows only prose lines and the front-matter hashes are unchanged.

### K1 Starts: stale locks and refreshed prompts (P-36, P-27a; SVC, no GPU)

Order: Pixel, then Cartoon, then Edu (Edu may start Pixel and Chiptune itself, `KNOWN_SERVICES` in edu `src/engine/studios/autostart.ts:19`; Pixel goes first so its start is the hub's).
1. Before: the lock content and pid liveness (P0) and SHA-256 of Edu's `prompts\art-critic\review.md` and Cartoon's `prompts\frame-critic\clip-review.md`, `frames.md`, `frames-3d.md`.
2. `pwsh -File scripts\hub.ps1 start pixel-studio`; `... start cartoon-studio`; `... start edu-studio`. Record every printed line.
3. After: each lock file holds the new pid (compare with `status`); the three prompts now equal their seeds with CR stripped (Edu's seed after EGS-76; Cartoon's with the "Write `notes` and the `problems` in English" line).
Passes when each start printed "removed its stale lock (pid N)" for its dead pid (or, if a pid was reused, "...started after the lock"), each app came up, and the prompts were refreshed. A prompt not refreshed: record the hash and `.seed-hashes.json` line, no hand edit.
Pixel's real instance is stopped after this step (`pwsh -File scripts\hub.ps1 stop pixel-studio`, record the stop's lock line); Edu and Cartoon stay up for K3 and K4.

### K2 The 8 queued VN job files to the Recycle Bin (P-23; no SVC, no GPU)

Safe under the running engine, from the code: the scheduler reads `queued/` each tick (`src/engine/queue/scheduler.ts:311`); `JobStore.list` skips a file that is gone (`src/engine/queue/jobs.ts:43-66`, `read` returns null); `claim` returns null on ENOENT (`:92-101`); VN's own `clearQueue` deletes queued files while the engine runs (`src/engine/vn/service.ts:750-753`). So VN keeps running.
1. List `C:\Users\Infplane\VisualNovels\jobs\queued` and `jobs\running`. Refuse (stop and ask) unless `queued` holds exactly these 8 and `running` none of them: `hub07-flow-test--vn.build--all--r2.md`, `hub07-flow-test--vn.lint--all--r2.md`, `hub07-flow-test--vn.pipeline.summary--all--r2.md`, `hub07-flow-test--vn.stage--all--r2.md`, `hub07-flow-test--vn.voice.generate--en--r2.md`, `hub07-flow-test--vn.voice.generate--hr--r2.md`, `hub07-flow-test--vn.voice.plan--all--r2.md`, `hub08-13-autostart--vn.build--regen-sfx_bell--r4.md` (8 today; another file there is left alone).
2. Record each file's size and SHA-256, then send each to the Recycle Bin: `Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('<path>', 'OnlyErrorDialogs', 'SendToRecycleBin')`.
3. After: the 8 are gone from `queued`; `vno_status {slug: "hub07-flow-test"}` and `{slug: "hub08-13-autostart"}` answer (record their step states; the plan does not edit `pipeline.json`).
Passes when exactly those 8 are in the Recycle Bin and VN still answers.

### K3 ComfyUI free on a real ComfyUI; the Gufo-aware autostart (P-27c, P-27d; GPU: ComfyUI only)

- Edu: MCP `edu_comfy_free {}` (edu `src/engine/mcp/tools.ts:139`); passes on a success result (ComfyUI's `/free` answers 200 with an empty body; `freeMemory` checks only `response.ok`, `src/engine/comfy/client.ts:175-178`).
- Cartoon: `tools/list` (`pwsh -File scripts\hub.ps1 check cartoon-studio`); if a tool frees ComfyUI, call it the same way; else UNTESTED until a real Cartoon job (its `freeMemory` is `src/engine/comfy/client.ts:175-182`, used by `kind-switch.ts:48,68`).
- P-27d: with ComfyUI already up, the GPU-holder check (Edu `autostart.ts:275-278,341-347`, Cartoon `:28-32,340-347`) is never reached; record "UNTESTED: ComfyUI was up" unless ComfyUI happens to be down at K1 (then record what Edu's log says about Strata on 8080).

### K4 Critic checks (P-21, P-25, P-27b; GPU: ComfyUI plus Inkling; if practical)

GPU order: `tiny-inkling.json` first (the proxy switches from Strata to Inkling), then the image work, then `tiny-strata.json` at the end. Box: 45 minutes.
- VN (P-21, VNO-73's log line): as HUB-43 K2 (`runs\hub-43-open-ideas.md`, its R2 + K2 section), with a throwaway project `hub44-signs-check`: a market-street background with review on, `vno_asset_generate {only: [<bg id>], force: true}`, `vno_wait {timeoutSeconds: 240}` (repeat while it runs). Read the art-critic's and the book's log for "art-critic's revised prompt for <id>: text negations removed before the redraw" and the drawn version prompts (`vno_asset_list`). Passes for P-21 when a logged removal is followed by a drawn prompt without any "no text / no letters / no signs / no captions / without any text" clause; if the critic approves or writes no negation, P-21 stays UNTESTED (record what it wrote). Then `vno_comfy_free {}`, `vno_delete_project {slug: "hub44-signs-check", confirm: true}`, and check no `hub44-signs-check--*` job file is left.
- Edu (P-25, EGS-76; P-27b English notes): Edu has no tool that reviews one picture (its tools: `edu_asset_list/plan/generate/set/select/replace/lock`, `tools-media.ts`); the review runs inside the course pipeline (`art_review`, `media.ts:510-534`). Only if `tools/list` shows a way to run `art_generate` and `art_review` for one throwaway course without the rest of the pipeline (or the user agrees to a small throwaway course through the pipeline, box 30 minutes): record each review's `notes`, `problems[].fix` (English? positive?) and the next round's prompt (`edu_asset_list`), then delete the course the way Edu's tools allow. Otherwise P-25 Edu and P-27b stay UNTESTED, with the reason.
- Cartoon: no redraw from a review exists (triage P-25): nothing to check.

### K5 Strata as Pixel's vision model: three runs in a row (P-15, PAR-25 part A; SVC, GPU: Strata)

Precondition: the proxy holds Strata (`tiny-strata.json` answered after K4).
1. Temp data folder `.claude\temp\hub44-live\pixel` with a copy of `C:\Users\Infplane\PixelStudio\config` only; in the copy: `vision: true` on the `acp` row `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, and `roles.md` `artist: [local]` only (no paid fallback can answer); `app.json` without `agentToolSet` (`all`).
2. Temp headless Pixel: `node_modules\electron\dist\electron.exe . --mcp-only` in `C:\projects\Personal\pixel-art-generator` with `PIXEL_STUDIO_HOME` = that folder and `PIXEL_STUDIO_MCP_PORT=7467`, without `ELECTRON_RUN_AS_NODE`, its output to `.claude\temp\hub44-live\pixel.out.log`. Client: a small JSON-RPC script `.claude\temp\hub44-live\mcp.mjs` (as HUB-43's `hub43-live/mcp.mjs`) against `http://127.0.0.1:7467/mcp`. The real Pixel folder is not touched: record its newest file time before and after.
3. `list_models`: the Strata model with `vision: true`, `tools: false`, `local: true`; `unavailable` count recorded.
4. Three runs, back to back, each: `new_document` 16x16 (argument names from `tools/list`), then `start_agent_run {text: "Draw a small red mushroom with white spots on its cap and a pale stem, centred on this 16x16 canvas, with a dark outline. Use the document's palette."}`, `get_agent_run` every 10 s until it ends; Strata `GET http://127.0.0.1:8080/metrics` before and after each run (`totals.requests`, `requests[]`). Record per run: runId, state, steps, wall time, usage in / cached / out, whether an event says "Stopped: this step left a picture the run had already drawn, so the drawing is kept as it is." (PAR-25's `REPEAT_STOP_TEXT`), Strata requests counted versus steps (P-20), the first step's prompt and reused tokens, and `export_png` at scale 16 to `.claude\temp\hub44-live\` (look at each picture).
5. Image proof, if the log allows: on the proxy's Strata page (the server's output log; `local-servers.ts:255-260` keeps it) look for `[strata] images: the image encoder started` (`D:\Strata\terminal\serve\server.py:4290`, printed when an elastic encoder starts for its first picture, `:4340`) during the runs. Seen: the previews reached Strata's encoder. Not seen (an always-on encoder prints nothing per picture): record "not provable from the log".
Passes when all three runs end `completed` (by the model's `done` or by the guard; the run log states which) with no 4xx and no paid model. K5's verdict goes to B1.

### K6 The `no-files` tool set (P-17; GPU: Strata)

Same temp Pixel; in the temp `config\app.json` add `"agentToolSet": "no-files"` (a temp copy: no backup needed); restart the temp Pixel (it reads app.json per run, but a restart rules out a cache). One run as K5 step 4. Record the first step's prompt tokens (Strata `/metrics` `requests[]`) against K5's (about 34,300), and the run's state. Passes when the run ends `completed` and the first prompt is smaller by about the characters PAR-25's changelog measured divided by 4 (within a quarter). Then stop the temp Pixel (kill its process tree), check 7467 is free, delete `.claude\temp\hub44-live\pixel`.

### K7 The full Scriptorium re-chunk (P-31; no SVC; the proxy's embedding server on 8083)

From the code (scriptorium master 980e415): `npm run engine -- reindex` is `yarn build:engine && node out/engine/index.js reindex ...` (`package.json` `engine`); `src/engine/index.ts:49-52` returns from `main()` after `reindexLibrary` before `initDataFolder` (`:69`), `acquireEngineLock` (`:78`), `new Engine` (`:86`), `engine.start` (`:98`), the folder watcher (`:99`), the MCP server (`:108`) and the heartbeat (`:116`): no scheduler, no job, no book factory, no chat model. `reindexLibrary` (`src/engine/cli.ts:78-93`) neither takes nor checks `index\engine.lock`; it calls only the embedding model (`acp/llama/nomic-embed-text-v1.5` from `config\roles.md:3`, through the proxy at 8787). It has no full-rebuild flag: unchanged files are skipped by hash (`src/engine/memory/index.ts:159-162`), so a full re-chunk needs the index file deleted. It prints `index/library.sqlite: N file(s) indexed, N unchanged, N removed. {"files":..,"chunks":..,"dim":..}` and one line per file (`cli.ts:88-90`); an embedding error throws and exits 1 (`[engine] fatal`), so "failed 0" means exit code 0.
1. Scriptorium down (`hub.ps1 status`, no process under `C:\projects\Personal\scriptorium`); never start it. List `C:\Users\Infplane\Scriptorium\index\`.
2. Backup: `Copy-Item C:\Users\Infplane\Scriptorium\index\library.sqlite C:\Users\Infplane\Scriptorium\index\library.sqlite.bak-HUB-44` (and `-wal`/`-shm` files if any exist); SHA-256 of both equal.
3. Counts before, read-only on the backup, with `.claude\temp\hub44-live\chunks.mjs` (written with the Write tool; `node:sqlite` `DatabaseSync(<path>, {readOnly: true})`, run with `fnm exec --using default node`): `select count(*) from files`; `select count(*) from chunks`; separator-only `select count(*) from chunks where trim(text, '-*_ ' || char(9,10,13)) = ''` (55 expected); longest `select file, length(text) from chunks order by length(text) desc limit 5` (1,790 expected).
4. Delete `C:\Users\Infplane\Scriptorium\index\library.sqlite` (and its `-wal`/`-shm`); the backup stays.
5. Bash: `export PATH="/c/Users/Infplane/AppData/Roaming/fnm/aliases/default:$PATH"; cd /c/projects/Personal/scriptorium && npm run engine -- reindex --data C:/Users/Infplane/Scriptorium` (forward slashes: backslashes are stripped). Record the whole output, exit code and wall time (HUB-40 did 35 files in about 20 s; about 1,449 files now: roughly 15 minutes, not measured).
6. Counts after, read-only on the new file, as step 3.
Passes when the exit code is 0, `files` after equals `files` before (or each difference is a listed file), separator-only chunks 0, the longest chunk at most 1,800 characters, and the chunk count is recorded. On a failure: delete the partial `library.sqlite`, copy the backup back, check its SHA-256, record.

### K8 Gufo probe P1 (P-01; GPU: Gufo; GET only)

Needs the user to load a Gufo model through the proxy window (it unloads Strata; minutes). Then, GETs only: `curl -s -o - -w " %{http_code}" http://127.0.0.1:8081/health`, then the same for `/metrics`, `/v1/status`, `/props`, `/slots`, `/v1/models`. Record each status code, the JSON keys (not the values of anything that looks like a key or path), and whether `/v1/models` has `architecture.input_modalities`. The record goes to AAP-51's planner (that plan maps only what Gufo answers) and decides P-26's health URL. End with `tiny-strata.json` (the proxy switches back to Strata).

### K9 For the user's eyes (P-42, P-07)

Ask the user to open the proxy window and read, against `runs\hub-43-open-ideas.md` (section "What the Monitor and About pages should show") and AAP-51's own list: the Monitor (sparklines, thinking tokens column, conversation-cache tile, render-error notice, the "started outside the app" label under Model and State), About, Requests, and whatever AAP-51 changed (P-03 unit, P-05 reason texts and dots, P-06 outside Llama id). Record the user's words. Items of P-42 that stay as they are: polling while hidden (not measurable from outside); the Pixel window's agent wiring, `stop_agent_run` mid-drawing, `continueChat: true`, the 30-minute limit and L1 in the Pixel window (no check planned); sprite-review items of HUB-39 (one sample only; `frames-3d` contact sheet, cloud-to-Inkling failover, VN sprite approval with two images); an outside Llama.cpp server and the unsloth build with `--metrics`. The byte-level image proof is K5 step 5; Edu and Cartoon after the rebuild are K1, K3, K4; the hub's lock removal is K1.

### K10 Only on the user's explicit word to start Scriptorium (P-34, P-32; director's default: not in this round)

Not part of the round's go-ahead: Scriptorium resumes its whole book factory and may use paid models (`services.json` warning). Only when the user says to start Scriptorium, and after K7:
1. Before: `index\engine.lock` content and whether pid 19260 runs.
2. `pwsh -File scripts\hub.ps1 start scriptorium -Force`: record the lock line ("removed its stale lock (pid 19260)") and the new lock.
3. `pwsh -File scripts\hub.ps1 logs scriptorium`: no error about `roles.md`, `providers.md` or `settings.md` (P-34); `pwsh -File scripts\hub.ps1 check scriptorium` lists its tools.
4. The user says how long it stays up; by default `pwsh -File scripts\hub.ps1 stop scriptorium` right after step 3 (record the stop's lock line).

### B1 PAR-25 part B go or no-go

Show the user K5's three results (states, steps, whether the guard ended a run, the pictures). Only on all three `completed` and the user's go: PAR-25 part B (its plan, "Part B"), merged, then `pwsh -File scripts\hub.ps1 build pixel-studio`; the live `C:\Users\Infplane\PixelStudio\config\providers.md` gets `vision: true` from the migration at Pixel's next start (first copy the file to `providers.md.bak-HUB-44`; after the start, `git diff --no-index` shows only that line and `seed-state.json` lists `acp-strata-vision-v1`). On fewer than three: part B is not done; record why.

### End of round

`pwsh -File scripts\hub.ps1 stop edu-studio cartoon-studio` (they were down before; record the stop's lock lines); `hub.ps1 status` compared with P0; the proxy holds Strata; settings.json SHA-256 unchanged; `.claude\temp\hub44-live` deleted on the user's word.

## Acceptance criteria

| # | criterion | proof |
|---|---|---|
| H-1 | `hub.ps1` refuses Windows PowerShell 5.1 and runs on pwsh 7 | H1 check |
| H-2 | a lock left at start says why when its time is missing, zoneless or out of range | H2 dry run (a)-(d) |
| H-3 | `start` shows the same pid as `status` | H3 dry run; R1's start against `status` |
| H-4 | ROADMAP row 37 and the proxy repo row | `git diff ROADMAP.md` |
| H-5 | each repo ticket meets its own plan | the six repo plans (AAP-51 by its planner) |
| H-6 | Edu's and Cartoon's live prose equal their seeds, front matter untouched | L1-L3 diffs and hashes |
| H-7 | stale locks of Pixel, Cartoon and Edu removed by a real start; prompts refreshed | K1 |
| H-8 | the 8 stale VN job files are in the Recycle Bin, VN still answers | K2 |
| H-9 | a stripped revised prompt is logged and drawn without text negations (if the critic writes one) | K4 |
| H-10 | three vision runs on Strata end `completed`; `no-files` finishes with a smaller first prompt | K5, K6 |
| H-11 | the full re-chunk: exit 0, no separator-only chunk, longest at most 1,800 | K7 |
| H-12 | Gufo's endpoints recorded | K8 |
| H-13 | the user read the proxy window | K9 |

## UNTESTED (until the round runs, and after it where said)

- Every L, K and R step until the user says go; K10 until the user's word to start Scriptorium; B1 until K5.
- P-27d (the GPU-holder branch of autostart) while ComfyUI stays up.
- P-25 Edu and P-27b if Edu offers no single-picture review (K4).
- P-21 if the critic never writes a text negation (K4).
- The byte-level image proof if Strata's encoder is not elastic (K5 step 5).
- The `hub.ps1` lock removal with pid reuse on a real app (cannot be made on purpose).

## Questions for the user (each answered by a director's default, confirmed with the plan approval)

1. L1-L3: Edu's `providers.md` and Cartoon's `providers.md` and `settings.md` get the seed's whole prose. Default: yes.
2. B1: a run the guard ends (`completed`) counts toward three in a row; the run log says how many. Default: yes.
3. P-17: `no-files` drops the 10 file tools (not 13). Default: 10.
4. P-37: `#Requires -Version 7.0`. Default: yes.
5. K4 Edu critic check only if `tools/list` offers a shorter way than a whole course; else UNTESTED. Default: yes.
6. K10 (Scriptorium start) is not in this round. Default: not in this round.
