# The Fig Tree Letter (hub07-flow-test)

Started 2026-10-23. Live check of HUB-07 phase 4: Google Flow as a VN Studio provider (VNO-10, FMM-11), the free part: images and Gemini voices. Music on Chiptune Studio; a Flow Music song (credits) was not asked for. VN Studio master 2f22db1, flow-music-mcp master bb0c023, then `FMM-13_composer-popover` (6452c04) from 11:30.

## Brief

- Idea / theme: an old fisherman gives a woman her grandmother's letter under a fig tree on a Dalmatian island.
- Kind: choices (chapter 1 -> 2 "Read it here" or 3 "Take it to the harbour"; 2 and 3 are endings) · adults
- Languages: en (primary) + hr edition (text written by Claude, `vno_edition_set`, 0 missing)
- Art: illustrated, `art.provider: flow` (Nano Banana 2.1, free) · Music: chiptune (snes, 1 track) · Voices: `voice.provider: flow` (Gemini TTS, free), en + hr

## Ids

| Tool | Id |
|---|---|
| Scriptorium story / book | none (written straight into VN Studio, args `.claude/temp/hub07/create.json`, edition `ed_hr.json`) |
| Book Translator project | none |
| VN Studio project | `hub07-flow-test` (data `C:\Users\Infplane\VisualNovels\projects\hub07-flow-test`) |
| Flow project | `vno-hub07-flow-test` (id 27959310-b15a-453f-bf3d-7e95f45ca54b) |

Model roles of the project (art-director, script-analyst, composer, stage-director, voice-director) on `client/claude-code`: Claude answered the art plan (2 batches), music plan, voice plan and 3 stagings. Voices: Marko `gemini:Algenib`, Nina `gemini:Sulafat`, narrator `gemini:Vindemiatrix` (both languages).

## Log

- 11:00 `hub.ps1 build flow-music-mcp`, `start flow-music-mcp`. `flow_voices`: Gemini voices listed (model gemini-3.8-flash-tts). Created project, hr edition, client models.
- 11:07 Pipeline run 1 (`from: analyse`): art and music plans answered; **generate failed 3 times at once**: "Google Flow is not ready: the Chrome window of flow-music-mcp is not running: run yarn login in C:\projects\Personal<form feed>low-music-mcp". Two VN Studio bugs: the pre-check treats "Chrome not open yet" as signed out, although flow-music-mcp opens Chrome on the first real call (fixed: **VNO-22**); the seeded `flowRepo` has a form feed for `\f` (fixed: **VNO-23**). Both on `VNO-20-23_fixes`.
- 11:09 Worked around by a read-only `flow_assets` call (opens Chrome). `flow_status`: signed in, PRO, **1,050 credits**. Pipeline run 2 (`from: generate`): 11 images made one by one (about 50 s each): 3 backgrounds 16:9, 2 sheets, 5 sprites 9:16 (sheet as reference, cut out with the `key` removal), the full CG 16:9 (with both sheets).
- 11:27 **Cover failed 3 times**: Flow's generation settings popover stayed open over the prompt box (`credit-cost-label` intercepts the click; screenshot `.claude/temp/hub07/peek.png`). flow-music-mcp bug, fixed as **FMM-13** (`closePopover`), rebuilt and restarted at 11:30; `vno_asset_regen cover` then made it first time (live check of FMM-13 passed).
- 11:31 Pipeline run 4 (`from: voice`): voice plan, stagings. en: 9/9 clips. hr: 3 of 9; 6 failed on Gemini's free-tier **daily** quota (HTTP 429, "retry in 21h"), after VN Studio's 10/30/90 s retries per clip. Build: theme classic-dark, 0 placeholders, 1 translation, 0 warnings. Lint clean (9 dialogue blocks).
- 11:45 `flow_status`: **1,050 credits** (unchanged: images are free). `flow_transcribe` of hr clips b003 and b005 gives the edition's exact sentences.

## Checked

- Every image is `engine: flow` from the Flow project; no ComfyUI call. Looked at: the CG (both characters, the letter, the fig tree; faces match the sheets), Nina's surprised sprite (clean cutout, same look as the sheet), backgrounds (empty courtyard afternoon/evening, harbour with bell tower).
- NOT checked: the 6 missing hr clips (rerun `vno_run_pipeline {from: "voice"}` after the quota resets, about 2026-10-24 09:00); Flow Music as the music provider (credits, needs the user's OK); hearing the voices (the user).
- Found for VN Studio's roadmap: when Gemini answers 429 with a retry time of hours (a daily quota), the remaining clips should stop at once instead of three retries each.

## Play (PowerShell)

```
& "C:\projects\Local\renpy\renpy-8.5.3-sdk\renpy.exe" "$env:USERPROFILE\VisualNovels\projects\hub07-flow-test\game"
```

Play both choices (the second from the start again). Croatian: Preferences -> Language -> Hrvatski; only 3 Croatian lines are voiced until the voice rerun. Listen for: the voices fit the characters, the English and Croatian pronunciation.
