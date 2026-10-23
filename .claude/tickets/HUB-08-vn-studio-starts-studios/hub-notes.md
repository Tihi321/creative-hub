# HUB-08: what the hub docs should say (from VNO-11, commit a8aed71 on VNO-10-19_hub-roadmap)

- services.json `_about`: VN Studio reads this file to start pixel-studio, chiptune-studio and comfyui (fields id, repo, port, mcp, http, managed, warning, startTimeout, start {kind, path, cwd, args, env}); keep them. Kinds other than electron and exe are ignored for these three.
- README "Running it": VN Studio starts Pixel Studio, Chiptune Studio and ComfyUI itself when a job needs them (waits up to startTimeout); never Scriptorium, Strata, VibeTTS or LM Studio; not ComfyUI while Strata answers. Off: `enabled: false` in ~\VisualNovels\config\autostart.md or VNO_AUTOSTART=0. Output appended to logs\<id>.out.log/.err.log after `--- started by VN Studio ... ---`. hub.ps1 stop stops them; a hard kill of VN Studio leaves them running. A desktop app holding the data folder makes the started copy exit; the job reports why.
- Skill section 0 step 1: VN Studio starts those three on demand; hub.ps1 start still works and shows failures sooner.
- ROADMAP: VN Studio row; Done line.
- Live check notes: autostart.md reaches ~\VisualNovels\config only after an engine restart on the new build; log lines `autostart <id>: down, starting ...` / `up after N s`; registry default C:\projects\Personal\creative-hub\services.json; close the Pixel and Chiptune desktop apps first.
