# Parallel Image Generation (Flow & ComfyUI): HUB-15 check C4

Started 2026-10-23 20:41. HUB-15 C4: Flow image jobs run in their own lane alongside ComfyUI jobs (VNO-28), live check.

## Ids

- Flow project: `the-trap-room-at-the-lanterna` (mystery puzzle visual novel, 4 chapters, 63 assets, `C:\Users\Infplane\VisualNovels\projects\the-trap-room-at-the-lanterna`).
- ComfyUI project: `hub08-13-autostart` (linear children visual novel, 1 chapter, 8 assets, `C:\Users\Infplane\VisualNovels\projects\hub08-13-autostart`).
- Temp files: `.claude/temp/c4/` (raw status captures `status-parallel-*.json`, `status-flow-*.json`, `status-comfy-*.json`, job files `job-*.md`).

## Decisions

- Flow art provider enabled on `the-trap-room-at-the-lanterna`: `art.provider: flow` (free Nano Banana illustrations, `max_credits: 0`).
- ComfyUI project: `hub08-13-autostart` (`art.provider: null`, qwen-image-2.1) selected as the tiny already-imported project, generating forced background and cover images (`bg_harbour_night`, `cover`).
- Flow image credits pre-agreed; recorded before run (`flow_status`: signed in, plan PRO, 858 credits).
- Full pipeline run for Flow project (`vno_run_pipeline { slug: "the-trap-room-at-the-lanterna", from: "generate" }`) to complete game build and lint for user playability.

## Timeline

- 20:29 Service readiness check: `vn-studio` (7459), `comfyui` (8188), `comfy-mcp` (7460), `flow-music-mcp` (7462) all verified up. Started `pixel-studio` (7457) via `hub.ps1 start pixel-studio`.
- 20:30 `flow_status`: signed in, plan PRO, 858 credits.
- 20:39 `vno_update_settings`: updated `the-trap-room-at-the-lanterna` to `art.provider: "flow"`.
- 20:41 `vno_run_pipeline` enqueued for `the-trap-room-at-the-lanterna` (run 2, from `generate`).
- 20:41 `vno_asset_generate` enqueued for `hub08-13-autostart` (run 7, force: true, `only: ["bg_harbour_night", "cover"]`).
- 20:41:36 - 20:42:20 `the-trap-room-at-the-lanterna` ran `music_01` (ACE-Step on ComfyUI) on the default slot while running `sheet_inspector_nada_ferluga` on Flow (`lane: flow`).
- 20:42:30 **First parallel image capture (#1)**: Flow image job `the-trap-room-at-the-lanterna--vn.assets.generate--sheet_luka_bencic--r2` and ComfyUI image job `hub08-13-autostart--vn.assets.generate--bg_harbour_night--r7` both verified `running` simultaneously on `art-director-default`.
- 20:42:30 - 20:45:48 Continuous parallel execution captured across **19 polling intervals** (every 10-11 seconds):
  - Flow jobs active: `sheet_luka_bencic`, `sheet_bruno_orsini`, `sheet_mira_valenti`.
  - ComfyUI jobs active: `bg_harbour_night` (v3), `cover` (v2).
- 20:45:56 ComfyUI project completed its image generation: `hub08-13-autostart` step `generate` status `done` (`bg_harbour_night` v3, `cover` v2).
- 20:50:07 Flow project completed all 63 assets (42 Flow images, 3 ACE-Step music tracks, 10 ACE-Step ambiences, 8 skipped SFX).
- 20:50:18 Staging completed: 4 chapters staged.
- 20:50:40 Game build completed cleanly: built `C:\Users\Infplane\VisualNovels\projects\the-trap-room-at-the-lanterna\game` (theme noir, 0 placeholder images, 0 translations, 8 skipped-sfx warnings).
- 20:50:41 Ren'Py lint completed: clean (`ok: true, messages: []`), 311 dialogue blocks, 4,878 words, 33 screens. Full run completed with 71 jobs done, 0 failed.

## Checks

| Check | Result | Evidence |
|---|---|---|
| VNO-28: Flow image jobs run in their own lane and do not block or wait behind ComfyUI | **verified** | 19 consecutive raw `vno_status` captures (`.claude/temp/c4/status-parallel-*.json`) show Flow image job `sheet_luka_bencic` (then `sheet_bruno_orsini`, `sheet_mira_valenti`) and ComfyUI image job `bg_harbour_night` (then `cover`) in state `running` at the exact same timestamp.<br>Job markdown files on disk confirm both claimed by `agent: art-director-default`, with Flow job possessing `lane: flow` and ComfyUI job possessing `lane: null`. |
| ComfyUI project images only | **verified** | `hub08-13-autostart` generated `bg_harbour_night` (v3) and `cover` (v2); stopped at image stage (`tail: false`), no unprompted rewrites or story changes. |
| Flow project build & lint | **verified** | Game built at `C:\Users\Infplane\VisualNovels\projects\the-trap-room-at-the-lanterna\game` (theme noir, 0 placeholders, 8 expected sfx warnings); lint clean (311 dialogue blocks, 4,878 words, 33 screens). Ready for user playthrough. |
| Flow image credit economy | **verified** | Pre-run credits: 858. Post-run credits: 858 (0 credits spent; Nano Banana Flow images are free). |
| Image quality & consistency | **verified** | Inspected generated character sheets via `read_file` (`sheet_inspector_nada_ferluga`, `sheet_luka_bencic`, `sheet_bruno_orsini`, `sheet_mira_valenti`). Characters match bible descriptions (Nada's round spectacles, silver-streaked knot, plum dress, grey coat; Luka's flat cap, tweed jacket, freckles, camera; Bruno's waxed moustache, scarlet-lined cape; Mira's sequined dress, veil). No corrupted frames or broken aspect ratios. |

## Evidence Excerpts

### Concurrent Status Capture (`status-parallel-20261023-204230.json`)

```json
{
  "timestamp": "2026-10-23T20:42:32.0392949+02:00",
  "flow_status": {
    "jobs": { "queued": 64, "running": 1, "done": 6, "failed": 0 },
    "running": [
      {
        "id": "the-trap-room-at-the-lanterna--vn.assets.generate--sheet_luka_bencic--r2",
        "task": "vn.assets.generate",
        "unit": "sheet_luka_bencic"
      }
    ]
  },
  "comfy_status": {
    "jobs": { "queued": 2, "running": 1, "done": 21, "failed": 1 },
    "running": [
      {
        "id": "hub08-13-autostart--vn.assets.generate--bg_harbour_night--r7",
        "task": "vn.assets.generate",
        "unit": "bg_harbour_night"
      }
    ]
  }
}
```

### Job Frontmatter on Disk (`jobs/running/`)

Flow job (`the-trap-room-at-the-lanterna--vn.assets.generate--sheet_luka_bencic--r2.md`):
```yaml
---
kind: job
id: the-trap-room-at-the-lanterna--vn.assets.generate--sheet_luka_bencic--r2
book: the-trap-room-at-the-lanterna
task: vn.assets.generate
role: art-director
unit: sheet_luka_bencic
lane: flow
agent: art-director-default
---
```

ComfyUI job (`hub08-13-autostart--vn.assets.generate--bg_harbour_night--r7.md`):
```yaml
---
kind: job
id: hub08-13-autostart--vn.assets.generate--bg_harbour_night--r7
book: hub08-13-autostart
task: vn.assets.generate
role: art-director
unit: bg_harbour_night
lane: null
agent: art-director-default
---
```

## Credits

| Provider | Before | After | Spent |
|---|---|---|---|
| Flow (Nano Banana images) | 858 | 858 | 0 (free tier) |
| Flow Music | 13,169 | 13,169 | 0 (ACE-Step ComfyUI used) |

## Bugs & Observations

- No bugs in VNO-28 lane scheduling. Laned jobs and non-laned jobs share the agent runtime concurrently as designed without deadlock or slot starvation.
- Informational notice: `the-trap-room-at-the-lanterna` logged 8 expected warnings for SFX beats ("no SFX engine: import a file (vno_asset_import), skipped") because `sound.sfxEngine` was unset (`""`).
- Ren'Py lint and build output clean.

## Not Verified

- Interactive playthrough of all puzzle deduction branches in Ren'Py runtime (pending user verdict in C6).
