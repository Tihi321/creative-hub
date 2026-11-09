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
