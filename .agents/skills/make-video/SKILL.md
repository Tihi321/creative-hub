---
name: make-video
description: Turn a story idea or a published book into a short film or cartoon (1 to 3 minutes, MP4) by chaining the user's local tools over MCP - Scriptorium writes the screenplay (shots, voice-over, music cues), scripts/video-plan.mjs makes the shot plan, the cost estimate and the timeline, and flow-music-mcp makes keyframes, character voices, an animatic, the video shots (Flow credits), music and the final assembly. Use when the user asks for a short film, a cartoon, an animated story, a video or a trailer from an idea or a book. For a book, translation, art, music or a playable visual novel use make-visual-novel instead.
---

# Make a short film or cartoon

The hub is `C:\projects\Personal\creative-hub`. `README.md` there maps every repo, port and data folder; `services.json` is the machine-readable registry. The chain:

```
idea / published book
   -> Scriptorium: screenplay format (scenes, shots, dialogue, voice-over, music cues)  -> get_screenplay (JSON)
   -> scripts/video-plan.mjs: shot plan, cost estimate, budget left, flow_assemble timeline
   -> flow-music-mcp: keyframes (free) > voices (free) > animatic (free) > video shots (credits) > music > flow_assemble > captions
   -> MP4 in runs/<slug>/video/, watched by the user
```

Why it runs from a skill and not an app: video costs credits, so the budget is agreed first and Codex looks at every still before money is spent. The planner script keeps the money math and the timing exact and testable (`node --test` in the hub, no dependencies).

Run the script as `fnm exec --using=24 node scripts\video-plan.mjs <cmd> runs\<slug>\video [flags]` (Node is not on PATH in a plain shell). `plan`, `estimate`, `keyframes`, `voices`, `next`, `record`, `timeline` are described at the top of the file.

## 0. Before you start

1. `pwsh -File scripts\hub.ps1` (status). Start what the run needs: `pwsh -File scripts\hub.ps1 start flow-music-mcp`. Scriptorium is never started without asking: it resumes its whole factory and may spend on paid models. Ask the user first, run `list_stories {status: open}` and say what would start. A Scriptorium build older than SCP-17 has no screenplay formats and no `get_screenplay`: build the branch that has them (`hub.ps1 build scriptorium`), then stop and start it.
2. `flow_status`: signed in, credits left, `upload_rights`. If it has a hint (not signed in, Chrome down), tell the user and stop. If an MCP tool is missing from your tool list, the server was down when the session started: start it and ask the user to reconnect (`/mcp`); until then call any tool through `pwsh -File scripts\hub.ps1 call <service> <tool> '<json>'` (a tool call gets 660 s; only `flow_wait` caps its `timeout_seconds` at 50, so poll it for long jobs).
3. Open a run log: `runs/<slug>.md` from `runs/_template.md`, with its Video block filled in. Write every id (story, book, Flow project, media ids via `plan.json`), each decision, each credit spent, and what you checked. A later session resumes from this file.
4. Agree the brief only for what the user did not say. Defaults (already approved): a `short-film` (`cartoon` for an animated look, `kids-cartoon` for ages 3 to 8), 60 to 90 seconds and 10 to 15 shots, aspect 16:9 (9:16 when the user says vertical), voices dubbed with free Gemini voices, Flow video model Omni 1.1 Flash 720p, **budget 150 Flow credits** (a budget agreed once is not asked about again; ask only when a shot would go over it), at most one retake per shot, music as Flow Music instrumentals (at most two cues, each song costs credits: ask before each one unless the user said to go ahead), captions burned in for voice-over shorts after the user OKs the transcript.
5. Agree who writes the screenplay: Codex through the client provider (`models: {architect: "client/Codex", writer: "client/Codex"}`, $0, reviewers on the app's models) or the app's models. See "Doing the model work yourself" in the `make-visual-novel` skill for the client task loop.

## 1. The screenplay (Scriptorium)

A. From an idea: `add_story {title, premise, plot?, characters?, format: "short-film" | "cartoon" | "kids-cartoon", models?}`. From a published book: `adapt_book {book, format, title?, notes?, models?}` (the book is compressed into the format's runtime). Screenplay formats are never picked for a story with no topic: always give `format`. Put the look of the film in the brief's Style (`vertical` there makes the aspect 9:16) and, for a cartoon, the look of each character in a few concrete words (colours, shape, one thing that makes them easy to recognise): every keyframe is drawn from the bible looks.

Wait with `wait_for_book {book}` (or `pwsh -File scripts\wait-book.ps1`), working the client tasks if you write. Read the finished text once: every scene has shots, places match the bible, runtime in the format's range (60 to 180 s; kids 45 to 120 s), the spoken words fit their shots (about 2.5 words a second).

Then `get_screenplay {book}` and save the JSON as `runs/<slug>/video/screenplay.json` (Write tool; the result is long, write it as it is).

B. Without Scriptorium: write `screenplay.json` yourself in the shape of `docs/screenplay.md` in the Scriptorium repo (`C:\projects\Personal\scriptorium\docs\screenplay.md`): `slug, title, format, aspect, style, runtimeSeconds, characters [{name, looks, voice}], places [{name, looks}], music [{id, description, from, to}], chapters [{n, title, scenes [{id, place, time, background, shots [{id, framing, move, seconds, continuous, action, cast [{name, look}], sfx, title, lines [{speaker, delivery, text, kind}]}]}]}]`. Ids are `ch01.s01.sh02`; `kind` is `dialogue`, `voice-over` or `off-screen`; a title card is a shot with `title` set and `framing: "title"`.

Keep the screenplay file in the hub's run folder: it is the input of every later step.

## 2. Plan and dry run (nothing is spent)

`video-plan.mjs plan runs\<slug>\video --budget 150 --balance <credits from flow_status>` (add `--model omni-360p` for a cheaper test, `--aspect 9:16` to override). It writes `plan.json` and prints the dry run: every shot with its length (raised to 4, 6, 8 or 10 s to hold its lines), the credits per shot (`seen` = quoted by Flow, `guessed` = pro rata; 720p Omni seen: 4 s = 7, 6 s = 10, 8 s = 12, 10 s = 15), the total, a 25% retake reserve, the Flow video budget, the Flow Music budget (a separate balance: song credits are in `musicSpent`, never in the video `spent`; `--music-budget N`, default 10), and warnings (dialogue longer than its shot, more than 3 people in a shot, `continuous` shots made as normal shots, runtime outside the format's range).

Show the user the numbers in a few lines. The default budget is already agreed: go on if the total with the reserve fits, otherwise shorten the film (cut shots in the screenplay and plan again with `--force`), use `--model omni-360p`, or ask. `plan.json` is the state of the whole production: edit it by hand (a voice, a prompt, a shot length) and run `estimate` again.

## 3. Cast (free)

One Flow project per production: use `project: "<slug>"` with `create_project: true` on the first call. For each main character `flow_character {name, describe: <bible looks, full body>, voice: <the Gemini voice from plan.json voices>, project, out: <video dir>}`. The portrait is saved in `<out>\_cast\<name>.jpeg`: Read each one and redo a bad one with `flow_character_edit`. The characters are then references as `asset:<name>`.

## 4. Keyframes (free)

`video-plan.mjs keyframes <dir>` prints the `flow_generate` scenes: one image per shot (style, place looks, framing, action, cast looks; the shot's characters as `reference_images`; an `insert` shot has no cast and no references unless its text names a character; a title card prompt drops the style's "no text" and asks for the title). Run them in batches of 4 to 6 (`flow_generate {scenes, project, out: <dir>\keyframes, name: "kf", wait}`; each is a paced job, so poll `flow_wait` until finished; never regenerate a scene whose job still runs). Images are free (`max_credits: 0`).

Read **every** keyframe file. Redo the ones with wrong faces, wrong clothes, text in the picture, extra people or a drifting style (a short prompt change, then the same scene again). Do not spend a credit on a shot before its keyframe is good. For each shot record the media id and file: `video-plan.mjs record <dir> <shot id> '{"keyframe":{"media_id":"<id>","file":"<absolute path>"}}'`. Title cards are keyframes too (the title is the only text in the picture).

## 5. Voices (free)

`video-plan.mjs voices <dir>` prints one `flow_narrate` call per spoken line: `engine: "gemini"`, the character's fixed voice, `format: "wav"`, `style` from the delivery (voice-over and Narrator lines always get "as a voice-over narrator", with the delivery after it), `out: <dir>\voices`, `name: <shot id>-l<n>`. A Gemini 429 says "rate limited": wait about a minute. You cannot listen to them: check each file's length with ffprobe (`ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 <file>`) and use `flow_transcribe` on one or two lines to check the words. Record per shot, lines in order: `record <dir> <shot id> '{"voices":[{"file":"...","seconds":2.4}, ...]}'`. A line much longer than its shot gets a warning in `timeline`: shorten the text in `plan.json` and make it again.

## 6. Animatic (free) and the OK

`video-plan.mjs timeline <dir> --animatic` writes `assemble.json` (keyframes held for each shot's time with a slow zoom, the voices placed at their moments, the free music if any). Call `flow_assemble` with its contents (`out` is already the run's `out` folder; the result lists the `timeline`). Check the film with ffprobe (duration about the plan's runtime, one video and one audio stream) and extract a frame or two.

Give the user the MP4 path (PowerShell form: `Start-Process '<path>'`) and the numbers: runtime, shots, estimated credits, budget. The user watches it and OKs the film, or asks for changes (edit `plan.json` or the screenplay, redo keyframes or lines, make the animatic again). **Nothing is paid before this OK.**

## 7. Video shots (credits)

Loop, one shot at a time:

1. `video-plan.mjs next <dir>`. It prints the shot, its estimate and `max_credits` = min(ceil(estimate x 1.25), budget left, `FLOW_MUSIC_MCP_MAX_CREDITS`, default 50), and the `flow_generate_scene` to use. If it says `budget reached`, stop and ask the user: do not raise the cap yourself.
2. `flow_generate {scenes: [<that scene>], project, out: <dir>\clips, name: "clip", wait: 25}`. The scene is `type: video` with `first_frame: asset:<keyframe media id>`, the motion prompt ("no speech, ambient sound only: ..."), `model`, `duration`, `resolution`, `aspect_ratio` and `max_credits`. The call waits up to 25 s, then returns job ids: use `flow_wait` until finished. A refused quote (over `max_credits`) spends nothing: read why before trying again.
3. Check the clip: extract a frame near the start and the end (`ffmpeg -ss <t> -i <clip> -frames:v 1 <png>`, Read it) and ffprobe the length. Same face, same place, no text, no wrong motion. At most one retake per shot (`next <dir> --retake <shot id>`, a different prompt or `first_frame`).
4. `video-plan.mjs record <dir> <shot id> '{"clip":{"file":"<path>","credits":<credits spent from the job>}}'`. Recording the same file twice counts once. Write the credits in the run log.

Flow shows "high demand" sometimes: wait a few minutes and try once; no blind retry loops. `continuous` shots are made as normal keyframe shots in this version.

## 8. Music

For each `music` cue of `plan.json`: ask the user, then `music_generate {instrumental: true, sound: <cue description>, format: "wav", out: <dir>\music, name: <cue id>}` (credits: about 5 a song, measured), or comfy-mcp `generate_music` (free, ACE-Step) when the user prefers. Record `record <dir> music:<cue id> '{"file":"<path>","credits":<n>}'`. A film with no music is fine.

## 9. Assemble

`video-plan.mjs timeline <dir>` (final): video shots trimmed to their shot length, title cards as stills, the voices placed 0.3 s into their shots, music cues from their shot ranges, `clip_volume` 0.3 (the clips' own sound under the voices), `duck: true`. Call `flow_assemble` with `assemble.json`. Check with ffprobe (duration, streams) and look at a few frames. A shot without a clip uses its keyframe and the script says so: finish the clips first unless the user wants that.

Captions (voice-over shorts, after the user OKs): `flow_transcribe {file: <final.mp4>}`, show the words to the user, then `flow_captions` (style `clean`).

## 10. Finish

- Give the user the MP4 path in PowerShell form. Only the user says the film is done. Ask how the pictures, voices, music and timing worked and write the answer in the run log.
- Update `runs/<slug>.md`: files, ids, credits before and after (`flow_status`), what was checked and what was not.
- A tool limit you hit that a code change would fix goes into that tool's own `ROADMAP.md` (Scriptorium for the screenplay text, flow-music-mcp for generation and assembly). A fix that needs two or more tools goes into the hub's `ROADMAP.md` as a new `HUB-NN` task.

## Things that go wrong

- Flow high demand, or a tile that fails: wait and try once more. Never regenerate a scene whose job still runs.
- "refused: quote above max_credits": nothing was spent. Check the live quote in the message; if the shot is dearer than estimated, fix the table `PRICES` at the top of `scripts/video-plan.mjs` (mark it `seen`).
- `hub.ps1 call` gives a tool call 660 s; only `flow_wait` caps `timeout_seconds` at 50: use the `wait` argument of the Flow tools and poll `flow_wait`.
- A Flow tool is missing after a server start: reconnect with `/mcp`.
- Faces drift between shots: put the character's looks in the keyframe prompt of every shot (the plan does), keep the portrait as `asset:<name>` reference, and use the keyframe as `first_frame`. Characters used as references were verified only for simple cases.
- A Gemini voice sounds wrong for a character: change its voice in `plan.json` `voices` and make its lines again (`voices` prints the calls).
- Out of credits: stop, record the state in the run log, tell the user.

## Not in this version

Speech inside the Flow clip (lip sync), `continuous` shots chained with `flow_continue`, several languages, choices or episodes. Dubbed Gemini voices and keyframe-first shots are the design (HUB-11 decisions D7 and D8).
