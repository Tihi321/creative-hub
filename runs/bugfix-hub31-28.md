# Bug-fix run after HUB-31 and HUB-28 (HUB-32), 2026-11-09

The user asked: "merge all and in new session fix all bugs". Sources: `.claude/tickets/HUB-31-vehicles-voices/discoveries.md`, the top of its `changelog.md`, and `.claude/tickets/HUB-28-edu-mobile-music/discoveries.md`. Ticket plan: `.claude/tickets/HUB-32-bugfix-hub31-28/plan.md`. Check logs: `.claude/temp/bugfix-hub31-28/{cts,fmm,egs,web}/`.

Cost: $0. No Flow credits, no ElevenLabs calls (not even the one allowed status read), no paid models, no downloads. Scriptorium, Chiptune Studio and the Edu engine were not started.

## Repos, branches and masters

| Repo | Ticket branches (each merged with `--no-ff`, branches pushed) | master after | Pushed |
|---|---|---|---|
| cartoon-studio | CTS-44 `da89e59`, CTS-45 `778988e`, CTS-46 `fb112a1`, CTS-47 `95d6746`, CTS-48 (commit under merge `652c36e`) | `652c36e` | yes |
| flow-music-mcp | FMM-20 `9f52a93` | `894c94a` | yes |
| comfy-mcp | CMC-08 `80921f5` | `4b53fed` | yes |
| edu-game-studio | EGS-64 `8f9b84c`, EGS-65 `fa92f87`, EGS-66 (merge `db4a9e8`), EGS-67 `d3df72f` | `76a15b6` | yes |
| creative-hub-web | WEB-05 `2645c99` | `195efe6` | yes; the push started the Pages deploy (the bridge fix goes live by itself) |
| creative-hub | HUB-32 on `HUB-32_bugfix-hub31-28` | see the hub commit | yes |

No force-push.

## Checks

- **cartoon-studio**, on every ticket branch before its merge:
  - `typecheck`, `lint`, `test`, `test:blender`, `test:e2e`, `build` and `docs:check` all exit 0.
  - `test` went from 59 to 62 tests. `test:blender` ran 21, then 22 from CTS-46 on. `test:e2e` passed 2 each time.
  - On CTS-48, lint first failed on one `no-useless-assignment`; after the fix lint and typecheck passed and the test was rerun.
- **flow-music-mcp:** `typecheck`, `build` and `test` pass (160 tests). The repo has no lint script.
- **comfy-mcp:** `typecheck`, `lint` and `test` (49) pass, and `build` makes `out/index.js` and `out/patches.js`. A live `check` against the real ComfyUI folder reports 2 of 2 applied.
- **edu-game-studio**, per branch:
  - `typecheck`, `lint` and `build` pass.
  - `test` is up to 524. The first run on EGS-64 had one timing flake in `tests/scheduler.test.ts`, which passed on the rerun.
  - `test:e2e` passes 40 tests in 16 files.
- **creative-hub-web:** `check` and `build` pass, `test:unit` 4/4, `test:e2e` 55/55.
- **hub.ps1:**
  - It parses with 0 errors.
  - `hub.ps1 status` printed the table plus "ComfyUI local fixes: 2 of 2 applied".
  - `hub.ps1 comfy-patches` printed both patches as `applied`.

## Services restarted (with hub.ps1)

- flow-music-mcp: restarted for FMM-20. The key is set in its environment, and `check` gives 37 tools.
- cartoon-studio: restarted twice, for CTS-44 to 47 and then CTS-48. No job was queued or running either time. `check` gives 54 tools.
  - After the CTS-48 start, all eight files in `~/CartoonStudio/agents/` match the 3D seed.
  - The prompts in the data folder had already been refreshed from the seed.
- comfy-mcp and ComfyUI: not restarted. The server code did not change, and the node fixes were already in place.

## Decisions

- **CTS-46:** `extent()` now returns true half extents for `box`. The default outline width and the creature-box bevel in `build_character.py` get the old box value back (`_tuned_extent`), so no outline or bevel changes.
  - The agent listed every box part of the mini-vehicles fixture and of pilot 4. All vehicle boxes except the pennant set their own `outline`, so their output is the same whichever way.
  - The fixture house moved from [-9,5] to [-13,6]. The set sheet was rendered in Blender before and after: the house no longer fills the AUTO TWO tile.
- **CTS-45:** a `from` or `retry` run deletes the queued (and stopped, which means requeued) jobs of the reset step and of every later step of that episode. A job that is *running* at that moment is not touched (see Discoveries).
- **CTS-48 (not in the brief; I added it after a check):** CTS-47 changed the personas in `seed/`. The data folder never takes them, because `agents/` is the user's staff once it exists.
  - Fix: a starter agent file that is still exactly an earlier seed version (hashes from git in `SEED_HISTORY`) gets the new text at the next start.
  - An edited agent file is kept, and a fired agent does not come back.
- **FMM-20:**
  - The quota guard reuses a subscription read for 5 s, minus the credits this process spent since. Five lines now make at most 6 reads instead of 10.
  - The after-read is retried 3 times. If every try fails, `remaining_after` is the before value minus the estimate, with `remaining_after_source: "estimate"`.
  - `flow_elevenlabs_status` always reads live.
- **CMC-08 / HUB-32:**
  - The two fixes live in comfy-mcp as text patches: `node out/patches.js check|apply|revert --comfy-dir <ComfyUI>`. The third-party repos were not forked.
  - `hub.ps1 status` warns when a fix is gone, and `hub.ps1 comfy-patches apply` puts it back (then restart comfyui).
  - The flicker fix: status asks again, all at once with a 2 s wait, for the ports it first found down.
- **EGS-66, item 8 (stale client job):** this is by design, not a bug. A job parked for a client model stays in `running/` and is requeued at start, with no model call. The engine start log now names jobs older than 3 days and says how to answer or drop them.

## Data steps still open (the user's data; not done here)

- `~/EduGames`: `deutsch-a1-pilot--summarize--all--r4` is still parked. Answer it (`edu_client_tasks` → `edu_get_task` → `edu_submit_task`), or delete its file from `jobs/queued/` and `running/` while the engine is stopped.
- Once the Edu engine runs the new code, call `edu_run_pipeline {slug}` once per course that got music through the asset tools. `music_*` then flips from skipped to done.
- Existing Edu courses get the default asset alt texts at their next relink (any `edu_asset_plan`, `edu_music_plan` or `edu_asset_generate`).
- The edu games in creative-hub-web `public/play/*` still carry the old player. The clip-stop fix and the panel's remote keys reach users only after a republish (creative-hub-web `publish`). Not run: that is the user's call.
- Two idle `python -` processes from the HUB-31 run (pids 19424 and 36784, started 12:00 and 12:04) are still running. The permission check blocked killing them, so the user has to end them.

## Status per item

| # | Item | Repo / ticket | Status |
|---|---|---|---|
| 1 | Voice-review button in the studio UI | cartoon-studio CTS-44 | DONE; checked in the mocked-bridge browser harness (`studio-shots.mjs`); UNTESTED in the real desktop app with an engine waiting at `voice_review` |
| 2 | Stale final render reused after a resume; a retry cancels queued or stopped later jobs | CTS-45 | DONE (regression test fails before, passes after); a job running at that moment is not cancelled |
| 3 | `build_set.py` CtsError for a kind with no builder | (already on master: `E_SET_INVALID`) | DONE before this run, checked |
| 4 | `tiptoe` in `WALK_KIND` | (already on master: CTS-42, a slow `walk`) | DONE before this run, checked |
| 5 | `extent()` half extents | CTS-46 | DONE; outlines and bevels unchanged on purpose |
| 6 | Compose `build()` resets state | (already on master: CTS-41 `actor.reset()`) | DONE before this run, checked |
| 7 | `set_sheet` docstring size | (already on master) | DONE before this run, checked |
| 8 | Move the house in the mini-vehicles fixture | CTS-46 | DONE (set sheet rendered before and after) |
| 9 | "cutout" wording: personas, pitch and bible prompts, default bible style, clip prompts | CTS-47 + CTS-48 | DONE; the seed and the user's data folder both have the 3D wording; UNTESTED with a real model run |
| 10 | ElevenLabs subscription 429s, `remaining_after` null | flow-music-mcp FMM-20 | DONE with fakes; UNTESTED live (no ElevenLabs calls by rule) |
| 11 | ComfyUI node fixes survive updates | comfy-mcp CMC-08 + hub HUB-32 | DONE; the check runs against the real files (2/2 applied); `apply` tested on fake files only; the warning branch of `hub.ps1 status` UNTESTED (the fixes were in place) |
| 12 | HUB-28: role-play clip keeps playing after leaving the scene | edu-game-studio EGS-64 | DONE (e2e); UNTESTED on a phone; reaches the site only after a republish |
| 13 | HUB-28: bot-detective timeout 120 s → 180 s | EGS-64 | DONE |
| 14 | HUB-28: EGS-60 plan absolute paths | EGS-64 | DONE |
| 15 | HUB-28: TV remote cannot reach the audio-panel sliders or Close | EGS-65 | DONE (Chromium with synthetic keys); UNTESTED on a real TV; needs a republish |
| 16 | HUB-28: Back leaves the game instead of closing the audio panel | EGS-65 + creative-hub-web WEB-05 | DONE (e2e on both sides); the bridge is live through Pages, the player side needs a republish; UNTESTED on a real TV |
| 17 | HUB-28: bridge Library pill covers the Title control | WEB-05 | DONE (position test); not looked at visually |
| 18 | HUB-28: `play.mjs` overflow check misses clipped content and small taps | EGS-67 (`--layout`) | DONE |
| 19 | HUB-28: stale client job requeued at engine start | EGS-66 | DONE as a report in the start log (by design); the parked job itself is NOT DONE (user data step above) |
| 20 | HUB-28: `steps.json` keeps `music_*` skipped | EGS-66 | DONE in code; existing courses NOT DONE until `edu_run_pipeline` runs once per course |
| 21 | HUB-28: asset alt texts missing in other editions | EGS-66 | DONE in code; existing courses get them at the next relink |
| 22 | HUB-28: `hub.ps1 status` flickers to down after a start | hub HUB-32 | DONE; UNTESTED against the original flicker (it did not reproduce here) |
| 23 | HUB-28: fixtures without an audio asset | - | no action (the discovery asked for none) |
| 24 | HUB-28: lmstudio and strata down, so jobs fall back to openrouter | - | NOT DONE: a question for the user (is the fallback wanted?) |
| 25 | HUB-31: C3 grep pattern matches old comments | - | no code fix (a checker reading; the pattern `AIza[0-9A-Za-z_-]{35}` is the suggested one) |
| 26 | HUB-31: empty `GEMINI_API_KEY=` hides the real key | (already on master: FMM-19) | DONE before this run |
| 27 | HUB-31: three idle `python -` processes | - | NOT DONE: killing them was blocked by the permission check (one has exited; two remain) |
| 28 | HUB-31: voice gate, ElevenLabs auditions, budget before series, revise jobs, normaliseWav, car turn and antenna, mcp-guide intro | (already on master: CTS-37 to CTS-42) | DONE before this run |

## Discoveries (not fixed)

- cartoon-studio `src/engine/pipeline/clips.ts:301`: `shot.action.replace(/s+/g, ' ')` is missing a backslash. It replaces runs of the letter "s" with spaces in the keyframe-polish prompt.
- cartoon-studio CTS-45 does not cover a job that is running during a `from` or `retry` run: it may still mark a step done after that step was reset. A guard `state.steps[step].job === ctx.job.id` in `runStep` would close it.
- cartoon-studio `seed/config/roles.md:30` describes the character designer the canvas way, and `docs/contracts.md:53` shows a canvas bible example.
- cartoon-studio `cts_run_pipeline` without `options.renderer` still makes a canvas series.
- cartoon-studio `seed/agents/voice-director-elodie-brandt.md` gives the voice rule without ElevenLabs (Gemini / OmniVoice / Kokoro).
- flow-music-mcp FMM-20:
  - The cache is per process, so credits spent by another instance within the 5 s are not seen.
  - A 429 retry on the TTS POST sends the line again, which might bill twice.
  - If the after-read comes back before the account counter has counted the line, the next guard sees one line too many credits left. The reserve covers this.
- edu-game-studio:
  - The default alt in a new edition is source-language text, which the editions step might later take as already translated.
  - The `rp.scene.back` button returns only to the scene view.
  - `tests/scheduler.test.ts` has a timing flake.
  - `--layout` covers only the screens where the bot calls `overflowCheck`.

## Extra ideas (not built)

- A voice-review note history and an "audition all" list in the Cast view; a studio-shots mode against the real engine.
- Show the 429 count and cache hits in `flow_elevenlabs_status`.
- `overflowCheck` on every screen from the bot core; `edu_status` that shows tool-made music live; a tool to drop a stale client job.
- Move the oak in the mini-vehicles crossing set as well.

## Follow-ups after the user's answers (2026-11-09, evening)

The user said: "you can go fallack to acp proxy then open router yes. We can reprublsh yes, yes refresh music steps, end processes" (relayed by the parent session, which also ended the two idle python processes). Then: bump the Node 20 actions. Still $0.

### What was done

- **Edu Studio started.** `hub.ps1 build edu-studio`, then `start`. The only parked job was a free client job (`client/claude-code`, `paid: false`). The start log printed the new EGS-66 line naming that job as older than 3 days.
- **Edu games rebuilt.** `edu_build` for suncev-sustav, deutsch-roleplay-a1, deutsch-roleplay-b2 and deutsch-a1-pilot: ok, no problems.
  - All four `build/player.js` now have md5 `cbb57a5c...` (was `2f0a8e48...`) and contain the EGS-65 Back handling.
- **WEB-06 (creative-hub-web) republished.** `publish` ran with `--only` for the 4 works.
  - Smoke check ok for all 4. 4 copied, 8 encoded, 105 cached; 434.8 MB of 600 MB.
  - The diff is `player.js` and `builtAt` only.
  - build, check, test:unit and test:e2e (55) pass.
  - Merged to site master `99a6f80` and pushed.
  - Its Pages deploy (run 42705139913) built fine, then hung in `deploy-pages@v4` on `syncing_files` and timed out after 10 min. The re-run hung the same way and was cancelled from the user's account. githubstatus.com said all systems operational.
- **WEB-07 (creative-hub-web).** The Pages workflow moved to Node 24 actions:
  - checkout v7.0.1, setup-node v7.1.0, configure-pages v6.0.0, upload-pages-artifact v5.0.0 and deploy-pages v5.0.1.
  - Breaking changes read: setup-node v5+ caches by itself (`cache: npm` was already set); upload-pages-artifact v4+ leaves out dotfiles, so `include-hidden-files: true` keeps `.nojekyll` and the `.gitkeep` files.
  - Merged to site master `3ce3a75` and pushed. Its run 42707994332 also deploys the WEB-06 content (result below).
- **Other repos' CI.** cartoon-studio, flow-music-mcp, comfy-mcp, edu-game-studio and creative-hub have no GitHub workflows, so there was nothing to bump.
- **The stuck job answered.** `deutsch-a1-pilot--summarize--all--r4` was answered with `edu_client_tasks` → `edu_get_task` → `edu_submit_task` (accepted).
  - The summary was taken from run 4's step list: 4 units, 12 objectives, 4 articles, 38 items, the fact-checks passed, 8 VibeTTS clips, lint clean with 12 warnings, playtest passed, publish score 7.89, and media skipped in that run.
  - The job is now done and `jobs/running/` is empty. The prompt and the answer are in `.claude/temp/bugfix-hub31-28/egs/summarize-*.json`.
- **Music steps refreshed.**
  - deutsch-a1-pilot flipped to `done` by itself when its summarize job finished: "15 sound(s) made through the asset tools".
  - `edu_run_pipeline` on deutsch-roleplay-a1 (12 sounds) and deutsch-roleplay-b2 (10 sounds) flipped both `music_*` steps to `done`. Both calls enqueued no job.
  - suncev-sustav made its music in the pipeline, so its steps were already done.
- **EGS-68 (edu-game-studio) fallback.** A role whose list names Strata or LM Studio now gets the ACP proxy (when it is on and lists a model), then an OpenRouter model at price 0, right after those entries and before the rest of its list.
  - The seed's `acp` row and the custom-provider hints use port 8787.
  - Merged to master `3505ae6` and pushed.
  - Checks: typecheck, lint, test (525), build and test:e2e (40) pass.
  - One unit test covers it. `tests/seed-migrations.test.ts` was updated for the new port.
- **The user's Edu config.** In `~/EduGames/config/providers.md`, `acp` changed from `enabled: false`, port 7461 to `enabled: true`, port 8787. The copy from before is in `.claude/temp/bugfix-hub31-28/egs/providers.md.before`.
  - After an engine restart: "acp 21 found", "openrouter 14 found".
  - A read-only check on the real config: fact-checker and playtester go `lmstudio/gemma-4-e4b-it > acp/gpt-6-luna > openrouter/liquid/lfm-3-1.7b:free > deepseek/deepseek-flash` (Strata down). The director keeps `deepseek/deepseek-flash` first, as its role list says.
- **Other tools' fallback order.** services.json says the ACP proxy is a provider in Scriptorium, Book Translator, VN Studio, Pixel Studio and Chiptune Studio (HUB-09), but whether they try it before OpenRouter when the local servers are down was not checked in their code (see Discoveries below).

### Discoveries from the follow-ups (not fixed)

- No other tool falls back to the ACP proxy after its local servers. In their seed configs: Scriptorium and VN Studio role lists are `[paid, strata, lmstudio]` / `[strata, lmstudio, paid]`, Cartoon Studio `[client/claude-code, strata, lmstudio]`, Pixel Studio and Chiptune Studio `[lmstudio]`. Each has an `acp` provider row, but no role names it, so none of them tries ACP before the paid default or OpenRouter. Book Translator has no `roles.md`. The users' own data configs were not read.
- EGS-68 picks the *first* model each provider lists: ACP gives `acp/gpt-6-luna` (Codex), and OpenRouter's free list gives `openrouter/liquid/lfm-3-1.7b:free`, a 1.7B model, weak for this work. A free OpenRouter row in the settings `fallbacks` (for example `openrouter/google/gemma-4-31b-it:free`, the doc's example) would be taken first. Not set: the user did not name a model.
- Edu Studio roles that start with `paid` (the director and the writers) still go to DeepSeek first. EGS-68 only changes what comes after the local servers.
- The OpenRouter provider also lists a paid model (`openrouter/google/gemini-2.5-flash`, 0.3/2.5 USD per M); EGS-68 never picks it (price 0 only).
- The WEB-06 Pages deploys hung twice in `deploy-pages@v4` "syncing_files" while githubstatus.com was green. The cause was not found; WEB-07's deploy-pages v5.0.1 is the next try.

### Status at the stop (2026-11-09, about 23:10)

The user said: "maybe we should not push anymore for action today if this is issue on github side". So no more pushes that start GitHub Actions today. This session did not cancel or re-run WEB-07's Pages run 42707994332 (it was `in_progress` in `syncing_files` at the stop). It was re-run anyway, outside this session: attempt 1 was cancelled at 22:11:48Z, attempt 2 started at 22:12:11Z (see round 3 for how it ended).

- **Pushed before the stop:**
  - creative-hub-web WEB-06 (`99a6f80`) and WEB-07 (`3ce3a75`). Their Pages deploys are the stuck ones.
  - edu-game-studio EGS-68 (`3505ae6`). It has no Actions workflow, so the push started nothing.
- **Live site at the stop:** the WEB-05 bridge fix is live. The edu games' `player.js` is still the old one (no EGS-64/65 code) until a Pages deploy goes through.
- **Waiting to be pushed tomorrow:**
  - creative-hub, branch `master`: the commit that adds this follow-up section (local only; the hub has no Actions workflow either, held only to keep the day's pushes at zero).
- **Waiting for GitHub, not a push:** a creative-hub-web Pages deploy of `3ce3a75`. Once GitHub syncs again, run the workflow ("Deploy site", `workflow_dispatch`) or let the next push run it. Then check that the live `play/*/player.js` contains `BrowserBack` and that the run has no Node 20 warning.
- **CI bumps in the other repos:** nothing to do. None of them has a `.github/workflows` folder.

| Follow-up | Status |
|---|---|
| Edu fallback: ACP proxy, then OpenRouter (EGS-68) | DONE (pushed; live chain checked read-only; no job has used it yet: UNTESTED with a real job) |
| The user's Edu config: `acp` on at port 8787 | DONE |
| Refresh the music steps | DONE (3 courses; nothing enqueued, $0) |
| Answer the stuck summarize job | DONE (accepted, job done) |
| Republish the edu games (WEB-06) | DONE locally and pushed; NOT DONE live: both Pages deploys hung at GitHub |
| Pages workflow on Node 24 (WEB-07) | DONE and pushed; its deploy UNTESTED (stuck at the stop), so "no Node 20 warning" is not confirmed |
| Node 20 bumps in the other repos | nothing to do (no workflows) |
| End the idle python processes | DONE by the parent session |

## Round 3: "merge all that we can, and fix, we just are not going to have deploy" (2026-11-09, night)

The user's words, relayed by the parent session. Pushes are allowed again; the Pages deploy is not waited for. $0, no ElevenLabs or Flow calls.

### The site

- creative-hub-web master is `3ce3a75` (WEB-06 republish + WEB-07 Node 24 actions), pushed.
- Its Pages run 42707994332 took four attempts (read from the GitHub API):
  - attempt 1 was cancelled at 22:11:48Z;
  - attempt 2 (started 22:12:11Z) failed on the deploy timeout at 22:22:40Z;
  - attempt 3 (22:33:23Z) failed in the deploy job at 22:34:20Z;
  - attempt 4 passed: completed `success`, updated 22:38:39Z.
- Attempt 4's log (2,992 lines) has no "Node.js 20" warning, so WEB-07 removed it.
- **The EGS-64/65 player fixes are live** after attempt 4. The live `play/<game>/player.js` of suncev-sustav, deutsch-roleplay-a1, deutsch-roleplay-b2 and deutsch-a1-pilot contains `BrowserBack`, and its md5 `89154fbb...` equals the published copy in the repo. The WEB-05 bridge fix stays live. Not played on a real TV or phone.

### Fixes from the independent check

| Item | Repo, ticket, commit | Status |
|---|---|---|
| `clips.ts:301` `/s+/g` to `/\s+/g`, `:304` `/\.png$/i` | cartoon-studio CTS-49 `5bba076` | DONE; no test (the polish path needs a fake ComfyUI) |
| A running job cannot mark a reset step done (`markDone` / `noteFailure` check `state.steps[step].job`) | CTS-50 `e323b73` | DONE (regression test); UNTESTED in a live run |
| `seed/config/roles.md` designer line 3D first; `docs/contracts.md` bible example toon 3D | CTS-51 `b46c646` | DONE |
| A new run without `options.renderer` makes a `blender` series | CTS-51 | DONE (old bibles without the field still read as canvas) |
| Voice director names ElevenLabs first (hub voice allocation) | CTS-51 | DONE; the old seed hash is in `SEED_HISTORY`; after an engine restart `~/CartoonStudio/agents/voice-director-elodie-brandt.md` and `config/roles.md` equal the seed |
| Cartoon Studio knows the new `E_ELEVEN_RATE` (a 429 stops the provider like `E_ELEVEN_API`) | CTS-52 `38be85e` | DONE (added because FMM-21 introduced the code) |
| flow-music-mcp after-read: no sleep after the last try, one retry layer, `remaining_after` a plain number | FMM-21 `39b0f0e` | DONE (test) |
| The TTS POST is never resent on a 429 (`E_ELEVEN_RATE`); 429 retries stay on GET | FMM-21 | DONE; retrying the documented "not charged" 429 cases NOT DONE (needs ElevenLabs' docs, not read) |
| `hub.ps1 status` reads the sockets and processes once: 31 s to 4.9 s, a port up on the first pass cannot show down | hub `HUB-32b_status-speed` (merge `7f5c7e5`) | DONE (same states as before) |
| `jobs.ts:18-19` doc comment | edu-game-studio EGS-69 | DONE |
| Negative test: `--layout` fails a build with 20 px buttons | EGS-69 | DONE (passes; it fails on the expected message) |
| CI action bumps in the other repos | - | nothing to do: none has a `.github/workflows` folder |

Checks:
- cartoon-studio: on each of CTS-49 to CTS-52, typecheck, lint, test (62, then 63), test:blender (22), test:e2e (2), build and docs:check all exit 0.
- flow-music-mcp: typecheck, build and test (161) pass.
- edu-game-studio EGS-69: typecheck, lint, test (525), build and test:e2e (41) pass.

Masters after round 3: cartoon-studio `6b92484`, flow-music-mcp `239bc41`, edu-game-studio `3280274`, creative-hub-web `3ce3a75`, comfy-mcp `4b53fed`, creative-hub (this commit). All pushed, no force.

Restarted with `hub.ps1`: flow-music-mcp (FMM-21) and cartoon-studio (CTS-49 to CTS-52, after a rebuild). Nothing was queued in either. Edu Studio still runs the EGS-68 build; EGS-69 changes no engine code.

### Discoveries (round 3, not fixed)

- The CTS-50 guard drops only the bookkeeping: a stale handler still writes its files before its result is dropped.
- A caller that matched `E_ELEVEN_API` for a 429 now gets `E_ELEVEN_RATE`. Cartoon Studio is updated; other callers were not checked.
- `request()` honours Retry-After up to 30 s per GET try, so one status read can hold the ElevenLabs queue for a while.
- The bible schema still defaults a missing `renderer` to `canvas` (on purpose, for old files).

### Extra ideas (not built)

- Abort a job early when its step was reset while it ran.
- A fake-ComfyUI helper so the keyframe polish path can be tested.
- Read ElevenLabs' 429 docs once and retry the TTS POST only for the codes rejected before processing.

## Polish round after the independent check (2026-11-09, night)

The check FAILed one item: the `cts_run_pipeline` description and `docs/pipeline.md` still said the renderer default was canvas. Fixing it turned up a real bug: **CTS-51's blender default did not work.**
- CTS-51 passed `renderer` to `createSeries`, which uses it only to pick the stub style and never writes it into the bible.
- So the stub bible read as canvas, and a run without `options.renderer` still made a canvas series.
- The new test (the CTS-38 test, now run without the option) failed on exactly this before the fix.

| Item | Ticket, commit | Status |
|---|---|---|
| A series the run creates is `blender` unless `options.renderer` is `"canvas"` | cartoon-studio CTS-53 `386de8e` (merge `9c05f8e`) | DONE (the test fails before, passes after) |
| `cts_run_pipeline` description and `docs/pipeline.md`: an existing series keeps its bible's renderer, a new one is blender | CTS-53 | DONE |
| Test: a run without `options.renderer` makes a blender bible and the Blender step list | CTS-53 (CTS-38 test extended, no new near-duplicate) | DONE |
| `seed/config/roles.md` voice director names ElevenLabs first | CTS-53 | DONE; the data folder's copy had the recorded seed hash, so it refreshed by itself: after a rebuild and restart, `~/CartoonStudio/config/roles.md` equals the seed |
| Run log lines on Pages run 42707994332 | hub | DONE (attempts 1 to 4 from the GitHub API; attempt 4 passed at 22:38:39Z, so the player fixes are live) |

Checks on CTS-53: typecheck, lint, test (63), test:blender (22), test:e2e (2), build and docs:check all exit 0.

Masters now: cartoon-studio `9c05f8e`, creative-hub (this commit); the others are unchanged since round 3.

Note: while checking the new test, this session once ran `git stash` / `git stash pop` in cartoon-studio. The stash was popped at once and nothing was lost, but this shared folder's rule says never to stash.

Discoveries (not fixed):
- `createSeries` itself (also used by `cts_series_create`) still writes no `renderer`, so a series made with `cts_series_create` reads as canvas until its first run. A first run without the option keeps it canvas, because the series already exists.
