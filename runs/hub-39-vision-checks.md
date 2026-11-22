# HUB-39 live checks K0-K5 (vision critic on Inkling)

Plan: `.claude/tickets/HUB-39-vision-fallback-inkling/plan.md`. User go-ahead "Yes, run checks" (2026-11-21). Worker session, started 2026-11-21 23:58 +01:00.

## K0 preflight

- 23:58 `hub.ps1 status`: up: acp-proxy (8787), strata (8080, qwen3.8-flash-next-unsloth-ud-iq4_xs), vibetts. Down: comfyui, vn-studio, edu-studio, cartoon-studio (and scriptorium, not touched).
- 23:59 started by this session: `hub.ps1 start comfyui vn-studio edu-studio cartoon-studio` -> all four up (comfyui pid 2424, vn 19720, edu 25460, cartoon 10856 per status).
- `/v1/models` lists `llama/inkling-2-mini` (vision true) and `llama/inkling-2-mini-dspark`.
- `/healthz`: status ok, llama `max_concurrent: 1`.
- ComfyUI `/system_stats` (no model loaded, Strata loaded): AMD Radeon 8060S, vram_total 107,090,132,992, vram_free 106,757,337,088 (unified memory; ROCm figure). ComfyUI 0.45.0.
- K0: PASS.

## K1 Inkling with the V1 body

- 00:00:11-00:00:31 (2026-11-22): curl chat `llama/inkling-2-mini`, `chat_template_kwargs: {reasoning_effort: "none"}`, `max_tokens: 200`, text only -> HTTP 200 in 19.97 s (includes the Strata -> Llama switch). Answer "A ripe banana is yellow, often with brown spots." prompt 25 / completion 79 tokens (reasoning_content present, short; `reasoning_tokens: 0` reported).
- Response headers: no `x-acp-proxy-ignored-params` header at all (so `chat_template_kwargs` not listed).
- After: 8080 (Strata) not answering, 8082 (llama) health 200. ComfyUI vram_free unchanged at 106,757,337,088 (ROCm figure does not show llama-server's use; inferred: the number reflects only torch's view).
- K1: PASS.

## K2 VN, real path

- Project `hub39-critic-check` (`C:\Users\Infplane\VisualNovels\projects\hub39-critic-check`), created 00:00:5x with `vno_create_project` (1 character `mara`, 1 place `harbour` dusk, book expressions `["neutral"]`, `settings.art.review: true`, no project `models`). `vno_status` models `{}`.
- Prompts by hand with `vno_asset_set` for `sheet_mara`, `sprite_mara_neutral`, `bg_harbour_dusk` (no art-director call). Cover and 3 music assets exist with empty prompts; NOT generated.
- 00:01:04 `vno_asset_generate {only: [sheet, sprite, bg]}` -> job `hub39-critic-check--vn.assets.generate--all--r1`.
- VRAM sampler (15 s) in the session scratchpad `vram.log`.

| time | job | model | tokens_in | tokens_out | ms | verdict |
|---|---|---|---|---|---|---|
| 00:02:53-00:03:59 | review sheet_mara r1 | acp/llama/inkling-2-mini | 863 | 310 | 66257 | approved, no problems |
| 00:04:42-00:05:35 | review bg_harbour_dusk r1 | acp/llama/inkling-2-mini | 854 | 407 | 52780 | approved, no problems |
| 00:07:55-00:09:45 | review sprite_mara_neutral r1 (2 images, sheet first) | acp/llama/inkling-2-mini | 1045 | 982 | 109697 | rejected: "background is solid medium gray, not the plain light/white background requested"; revisedPrompt identical to the original |

- Image jobs (qwen-image-2.1): sheet 108.5 s (00:01:04, before Inkling was used by the app; Inkling already resident from K1); bg 108.9 s (00:02:53-00:04:42, ran while the sheet review ran on Inkling: overlap); sprite (qwen-image-2.1-edit) 00:04:42-00:07:55, overlapped the bg review. No ComfyUI error.
- VRAM (ComfyUI system_stats vram_free, ROCm, 107.09 GB total): 106.76 GB before; 91.06 GB with qwen-image loaded + Inkling; lowest so far 86.42 GB (00:05:53, sprite edit model + Inkling).
- My own look: sheet = red short hair, green raincoat, brown boots, front + side, white bg: approve is right. bg = stone quay, fishing boats, orange/purple dusk, no people; but rather photo-like, not "anime": approve is acceptable (usable). Sprite v1 = a clean single cut-out of Mara (276x972, alpha). The app flattens transparent sprites on #808080 before sending (`art-critic.ts:23`), while the prompt (`prompts/art-critic/review_image.md:18`) asks for "plain light background": the rejection describes the pixels correctly but is a false rejection caused by the app; the revised prompt is unchanged, so the retry cannot fix it.
- Sprite retries: attempt 2 review 00:13:11-00:14:18, in 1045 / out 671 / 67150 ms, rejected ("Background is solid gray instead of the requested plain white/light background"); attempt 3 review -00:19:03, in 1067 / out 671 / 79258 ms, rejected (same reason; revised prompt adds "plain pure white background with no gray backdrop"). Sprite v2 and v3 made by ComfyUI with Inkling resident, no error. Review job `hub39-critic-check--vn.assets.review--sprite_mara_neutral--r1` total: 3 calls, 3157 in / 2324 out, 667.6 s. v3 (viewed by me, flattened on grey as the critic sees it): same Mara as the sheet, single full-body figure, clean cut-out: a usable sprite, so all three sprite rejections are false.
- 00:19:06 all 7 jobs done, 0 failed. Lowest vram_free in K2: 86,423,009,280 (00:05:53). No ComfyUI error, no "could not run".
- Reviews: 5 Inkling calls, 5 valid JSON verdicts of 5; seconds per review 52.8 / 66.3 / 109.7 / 67.2 / 79.3 (mean 75 s); max tokens_out 982 (< 2000).
- K2: PASS on the plan's criteria (verdict quality for sprites: false rejections, see above).

## K3 Edu, real path

- 00:2x copied `C:\Users\Infplane\EduGames\courses\suncev-sustav` to `...\courses\hub39-critic-check` (the copy's pack.json still says id/slug `suncev-sustav`; left as is).
- course.md `models`: deviation from the plan's `{art-director: client/claude-code}`: I listed every role except `art-critic` as `client/claude-code` (20 roles), so that no later stage (composer, voice-director, reviewers...) can reach a paid or local text model if the run goes past `art_review`. The art-critic has no course model, so the V2 list decides, as the plan wants.
- 00:24 `edu_run_pipeline {restart: true, from: art}` -> run 3, job `hub39-critic-check--art_plan--all--r3`. I answered the art_plan task (`...art_plan--all--r3#1`) with the run-2 plan (same 20 pictures, prompts without the engine's style words): "20 picture(s) planned, 0 new, 20 kept from earlier".
- art_generate r3: "0 picture(s) made, 20 already there" (the 20 run-2 pictures). So round 1 reviews existing pictures; ComfyUI only works again if the critic rejects some (round 2).
- Correction of the times above (from the job log): art_plan answered 00:20:34; `hub39-critic-check--art_review--all--r3` started 00:20:34 (agent art-critic-felix-ostrander, first model acp/llama/inkling-2-mini).
- My own look (round 1): `img-article-a-u1-1` revise "only seven planets": I count 7 planets, and the order/sizes are off too: verdict right. `img-article-a-u3-1` revise "the big striped giant also wears large rings, looks like a second Saturn": true, Jupiter is drawn with Saturn-like rings: verdict right (a real factual flaw). `img-item-u2-q4` pass "two Earths with parallel axes, left tips toward the Sun, right tips away; white margins": matches the picture: verdict right. `img-article-a-u2-1` pass (Earth, tilted axis, Moon, Sun): not viewed.
- Round 1 (`art_review` r3, k1) ran 00:20:34-00:52:53: 20 Inkling calls, all 20 pictures have a verdict in `pipeline/reviews/art_review-k1.json` (14 pass, 6 revise; the file's `revise` list holds 3: a-u1-1, quiz-arena bg-u1, bg-u2, all relevance 6; the other three revise verdicts had relevance 7: inferred that a score threshold picks which are redone). tokens_in 1141-1417; tokens_out 352-1467 (max 1467 < 2000); ms 46218-160080 (mean about 98 s). No "did not return valid JSON twice".
- More of my own look: `img-quiz-arena-bg-u2` revise "the grey Moon is missing entirely": true (Earth top right, stars, no Moon): verdict right. Oddity: the `img-rpg-hero` notes are written in Serbian-flavoured South Slavic ("dete", "belom"), not English or Croatian.
- 00:52:53 job `hub39-critic-check--art_generate-k2--all--r3` (ComfyUI makes the 3 revised pictures with Inkling resident). vram_free 105.54 GB before (ComfyUI idle), 90.85 GB at 00:53:20 while generating.
- `art_generate-k2` r3: 00:52:53-00:57:31, 277.6 s for 3 pictures (about 92 s each), Inkling resident the whole time, no ComfyUI error. vram_free during it 90.28-90.85 GB.
- `art_review-k2` r3: 00:57:31-01:02:09, 3 Inkling calls: in 1417/1328/1330, out 1217/652/571, ms 134820/75609/67825. All 3 pass (`pipeline/reviews/art_review-k2.json`). My look at `img-quiz-arena-bg-u2` v2: Earth lower left, grey Moon upper right, empty middle: pass is right.
- 01:02:09 `music_plan` r3 parked as a client task (composer = client/claude-code): not answered. 01:02:2x `edu_stop_now {drop: true, slug: hub39-critic-check}` -> paused: true, stopped, dropped. NOTE: this pauses the whole Edu queue; I left it paused (resume with `edu_resume_all`). No music, voice or build job ran.
- K3 totals: 23 Inkling reviews, 23 valid verdicts of 23, max tokens_out 1467, mean about 97 s per review, lowest vram_free 90.28 GB (K3 window), no ComfyUI error, no "did not return valid JSON twice". Whole check 00:20-01:02 (42 min).
- K3: PASS.
- K4 prep (no GPU): 00:3x copied `C:\Users\Infplane\CartoonStudio\series\pilot` to `...\series\hub39-critic-check` (its bible.json still says slug `pilot`).

## K4 Cartoon clip review on Inkling

- 01:02:36 backup `C:\Users\Infplane\CartoonStudio\agents\frame-critic-felix-ostrander.md.bak-HUB-39` (SHA-256 4e7fe470a5b274f906f3145d696571b8406bd64d78e81c190c28512a6590f507, same as the original). Set `model: acp/llama/inkling-2-mini` (was empty).
- 01:02:41 `cts_clip_review {series: hub39-critic-check, episode: ep00-pilot, clip: hero}` -> job `hub39-critic-check--clip_review--ep00-pilot-hero--r1`; job log: first model acp/llama/inkling-2-mini.
- 01:02:49 agent file restored from the backup (copy back) while the job ran (the model is chosen at job start). SHA-256 after restore 4e7fe470...590f507 = backup. Backup file kept, nothing deleted.
- 01:06:08 done: 1 call, tokens_in 4575 (14 % of the 32768 context), tokens_out 936 (no cap; below 3000), 205.4 s. `episodes/ep00-pilot/reviews/clip-hero-2.json` is `schema: cts.review/1`, verdict pass, scores style 4 / onModel 4 / action 3 / safety 5, 2 problems (frame 3 puff too big; frames 1-2 and 4-5 near identical).
- Images sent: the six-frame sheet `episodes/ep00-pilot/video/review/hero-sheet.png` (1440x540) plus the pose sheets of the clip's cast (fido, lana): 3 images (inferred from `media.ts:45-59` and the two `cast/*/sheet.png`; not counted on the wire).
- My own look at hero-sheet.png: flat 2D cutout, Lana (pigtails, peach dress, yellow apron), Fido (cream, brown ears, blue collar), a big white puff in frame 3, frames 4-5 near the same: the notes match the picture; "the puff covers part of Lana's face/body" is overstated (it covers the table between them). Pass is right.
- K4: PASS. (note) Not tested: 3+ images at 1568 px for a Blender series (`frames-3d`); this canvas series sent 3 images.

## Before K5: ComfyUI freed

- 01:06 `vno_comfy_free` -> lane error "Unexpected end of JSON input" (ComfyUI `/free` answers 200 with an empty body; inferred that VN's client expects JSON). Then `POST http://127.0.0.1:8188/free {unload_models, free_memory}` -> HTTP 200; vram_free 106,009,006,080, queue empty.

## K5 restore Strata

- 01:06:52-01:08:00 curl chat `strata/qwen3.8-flash-next-unsloth-ud-iq4_xs`, `max_tokens: 20`, `reasoning_effort: "none"` -> HTTP 200 in 67.5 s (Llama -> Strata switch), answer "OK." (15 in / 3 out).
- After: 8080 health 200, 8082 not answering; `hub.ps1 status`: strata up, pid 39508, model qwen3.8-flash-next-unsloth-ud-iq4_xs. `/healthz` status ok, all providers idle (it does not name the loaded local model; the loaded model is read from 8080/8082 and hub.ps1).
- K5: PASS.

## Model calls in this session (spend rows dated 2026-11-22)

- VisualNovels: 5 x art-critic acp llama/inkling-2-mini. EduGames: 23 x art-critic acp llama/inkling-2-mini, 1 x art-director client/claude-code (answered by this session). CartoonStudio: 1 x frame-critic acp llama/inkling-2-mini. Plus the K1 (Inkling) and K5 (Strata) curls through the proxy. Nothing went to a paid or cloud model.

## End state (01:08)

- Up: acp-proxy 8787, strata 8080, embeddings 8083 (answers), comfyui 8188 (no model loaded, freed), vn-studio 7459, edu-studio 7463, cartoon-studio 7465, vibetts. 8082 (llama) down.
- Started by this session: comfyui, vn-studio, edu-studio, cartoon-studio (left running).
- The Edu queue is PAUSED (side effect of `edu_stop_now`); `edu_resume_all` resumes it (its queue is empty).
- K4 agent file restored, SHA-256 equal to `.bak-HUB-39` (backup kept).
- Throwaway data (kept for the user, D3): `C:\Users\Infplane\VisualNovels\projects\hub39-critic-check`, `C:\Users\Infplane\EduGames\courses\hub39-critic-check` (run 3, stopped at music_plan), `C:\Users\Infplane\CartoonStudio\series\hub39-critic-check`.

## UNTESTED

- Images with real defects beyond what these pictures had (K3 caught 6 real flaws in 20; K2 sprite rejections were false).
- The Blender `frames-3d` contact-sheet review, and a Blender clip review at 1568 px with 3+ cast sheets.
- A review that fails over from a cloud model to Inkling.
- VN with 2 images on a sprite that the critic approves (all 3 sprite attempts were rejected for the grey flattening).
