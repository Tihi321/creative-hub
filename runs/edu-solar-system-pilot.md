# Edu pilot: solar system (Sunčev sustav), kids 8-10

Started 2026-10-31. Skill: make-edu-game. Tip build: edu-game-studio worktree `edu-game-studio-egs19` (EGS-19_android, c4c5294).

## Brief

- Topic: Solar system. Audience: kids 8-10. Content language: Croatian (sourceLang hr); UI Croatian/English (editions: hr, en).
- Length: 3 units (format quick, units: 3). Shells: quiz-arena, encyclopedia, mindmaze, rpg. Story: none.
- Art: ComfyUI + Pixel Studio (RPG). Music: chiptune (snes) + ComfyUI as the plan says. Voices: OFF (media.voice.enabled false; no Gemini TTS, no VibeTTS).
- Models: client/claude-code ($0), answered by the session. No paid models, no Flow credits. Scriptorium never started.

## Services

- Old main-checkout engine (EGS-14, pid 30656, port 7463) was killed by pid (the claim that it was not in services.json was wrong, see Correction).
- Rebuilt player/live/engine in egs19; started `node out/engine/index.js --mcp-only` on 7463 (log .claude/temp/edu-engine.log), data ~/EduGames.
- Started via hub.ps1: pixel-studio (7457), comfyui (8188), comfy-mcp (7460). chiptune-studio (7458) was already up.
- ~/EduGames/config/providers.md search_order set to [client-search, wikipedia] (was tavily first: possibly paid). Helper: .claude/temp/edu.mjs (JSON-RPC to MCP, since the tools are not in this session).

## Ids

| What | Id |
|---|---|

## Log

- 2026-10-31 pipeline started: slug suncev-sustav run 1, job suncev-sustav--plan--all--r1 (brief .claude/temp/brief.json, voice off, music chiptune snes)
- Found: ~/EduGames/agents only had director-default.md (the starter staff is copied only while agents/ does not exist, by design in dataFolder.ts); first run failed at factbase (no researcher). Copied seed/agents/*.md (cp -n) and restarted run with retry/restart from research.
- Research via WebFetch of NASA Science pages + Wikipedia Apollo 11 (sun, planets, earth, moon, jupiter, saturn, uranus, neptune, pluto, asteroids, comets); submitted as client-search results for 6 research jobs
- curriculum (u1 Sunce i osam planeta, u2 Zemlja i Mjesec, u3 Divovi, patuljci i drugi putnici; 49 facts f1-f49, 12 sources); run 2
- articles (a-u1-1,a-u2-1,a-u3-1), items (10/10/11) written by me from facts; now distractors
- distractors + fact_check done by me (fact-check pass, accuracy 9, self-review since client provider)
- explain + design done (shells all 4, round 5, boss 8, timer 40). Note: design prompt says 'shells the player has today: quiz-arena' (stale text, harmless). Now art_plan.
- art_plan done (20 pictures). First art_generate: all 20 placeholders because ComfyUI had died (hub start earlier showed up, died ~16:25; engine autostart also refused: 'Strata is running and uses most of the GPU'). Restarted comfyui via hub.ps1 at 16:30 (pid 14136); will run edu_asset_generate to replace placeholders.
- music_plan done (9 snes chiptune tracks + 5 sfx, generated OK by Chiptune Studio); accessibility + child-safety reviews passed (by me)
- pipeline published (score 8.57), run 2; playtest bot 5/5 pass; lint 0 errors/20 PLACEHOLDER warnings. Next: generate real pictures
- 2026-10-31 asset_generate (job suncev-sustav--asset_generate--qmvwkbeemzm--r0): 15 of 20 pictures made by ComfyUI (qwen-image-2.1, ~1.7 min each); the 5 RPG ones (img-rpg-tiles, hero, npc-1..3) are still placeholders: ComfyUI stopped answering (301 s) on the tileset and was unreachable after. Pixel Studio was never reached for the RPG art.
- STOPPED on the coordinator's request. The engine I started (egs19, pid via engine.lock) was stopped.

## State at stop

- Course slug `suncev-sustav` in ~/EduGames/courses/suncev-sustav (pipeline run 2, stage published, score 8.57). Done: plan, research (6 notes, 49 facts f1-f49), curriculum, articles, items (31), distractors, fact_check pass, explain, design, art_plan (20), music_plan + music_generate (9 snes tracks + 5 sfx, all real), accessibility + child-safety pass, build, lint (0 errors, warnings only PLACEHOLDER_ASSET), bot playtest 5/5 pass, publish, summarize. Voices skipped by choice. All model tasks answered by me (client/claude-code), $0; research pages fetched with WebFetch from NASA Science and Wikipedia.
- Partial build (before the 15 new pictures were rebuilt in): ~/EduGames/courses/suncev-sustav/build/index.html (needs `edu_build {slug, force:true}` to carry the new pictures).
- Prepared, NOT applied: English edition text in .claude/temp/en-text.json (314 strings, citations reused from hr, accepted answers). Apply with edu_course_edit {slug, patch:{languages:["hr","en"]}, text:{en:<en-text.json minus lang>}} then rebuild, lint and rerun bot.
- UNTESTED: any human play, real audio, English edition, RPG shell with real art.

## Resume

1. Start ComfyUI (`scripts\hub.ps1 start comfyui`; it died twice, Strata shares the GPU) and the engine: `cd C:\projects\Personal\edu-game-studio-egs19; fnm exec --using=24 node out/engine/index.js --mcp-only` (port 7463). Helpers in .claude/temp: edu.mjs (call a tool), sub.sh (submit a task).
2. `edu_asset_generate {slug}` (makes only the 5 missing RPG pictures, needs Pixel Studio 7457 up), apply English edition, `edu_build {slug, force:true}`, `edu_lint`, bot: `node scripts\play.mjs courses\suncev-sustav\build --mode perfect` in the egs19 repo.

## Bugs / notes seen

- Starter staff in ~/EduGames/agents is copied only when agents/ does not exist (by design): upgrading from an older data folder left only director-default, and the pipeline then failed at factbase with "no researcher". Workaround cp -n seed/agents/*.md. Maybe worth a startup warning.
- ComfyUI process died twice mid-run (not an edu-studio bug); engine's own autostart refused: "Strata is running and uses most of the GPU".
- The game-designer prompt still says the player has only quiz-arena (stale text).
- `edu_asset_generate {kind:"image"}` errors "media.music.enabled is false" (kind must be an asset kind or music/sfx; message misleading).
- Pipeline `editions` step is skipped (languages beyond sourceLang need Book Translator, down).
- (Wrong, see Correction below: edu-studio is in services.json.)

## Resume session 2026-11-01

- Edu checkout C:\projects\Personal\edu-game-studio switched from EGS-14_detective to master (fb26927); player/live/engine rebuilt with vite (yarn absent). Engine started by `hub.ps1 start edu-studio` (hub-managed; 50 MCP tools). Also started: comfyui 8188, comfy-mcp 7460, pixel-studio 7457, book-translator 47811, chiptune-studio 7458. Scriptorium not started. Strata (8080) was already running; left alone (ComfyUI still worked).
- Note: services started from a sandboxed shell die when the call ends; start them with the sandbox off. `hub.ps1` status is flaky for slow endpoints (showed down while up); confirm with curl.
- `edu_asset_generate`: the 5 RPG pictures (tiles, hero, npc-1..3) made by ComfyUI qwen-image-2.1 (not Pixel Studio); 0 placeholders left, all 20 pictures real.
- English edition applied (`edu_course_edit`, 314 strings from .claude/temp/en-text.json, written by me, not Book Translator; languages [hr, en]); pending 0.
- `edu_build {force:true}` ok; `edu_lint` 0 errors, 0 warnings. Bot (quiz-arena): perfect 23/23, wrong 0/15, random 0.9, 0.75, 0.55 all reach the end; encyclopedia, mindmaze, rpg perfect + random 0.75 all finished; console and media errors 0 (20 images, 14 audio files loaded). English checked by hand with Playwright (lang-en shows the English title and units, no page errors).
- Build: C:\Users\Infplane\EduGames\courses\suncev-sustav\build\index.html
- UNTESTED: human play, real audio heard, touch, full English playthrough (only the title/map screens were read), picture quality (not looked at).

## Correction

The earlier note "The hub does not register edu-studio" and the Services line about it being missing from services.json were wrong: edu-studio is in services.json (port 7463, managed) and hub.ps1 starts it from master. That earlier state only reflected an older checkout.
