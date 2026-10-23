# HUB-08 changelog

2026-10-23. Live check on VN Studio master 2f22db1 (`runs/hub08-13-autostart.md`, details in `verification.md`): a music job started Chiptune Studio (up after 5.2 s), a pixel background started Pixel Studio (5.7 s), a background regen with ComfyUI stopped started ComfyUI (42.6 s, the long command line with spaces intact); `enabled: false` started nothing and the job failed with "auto-start is off"; logs carry the "started by VN Studio" header. Not checked: `stopOnExit: true`, the Strata guard (Strata was down).

2026-10-22. Tool work: VN Studio VNO-11 (branch `VNO-10-19_hub-roadmap`).

- VN Studio starts Pixel Studio, Chiptune Studio and ComfyUI when a job needs them, using the commands in the hub's `services.json` (`seed/config/autostart.md`).
- Hub (commit 170ee2e): the skill and the `_about` in `services.json`. Notes: `hub-notes.md`.

Verified: the VN Studio tests.
Not verified: the live check (a job that starts a stopped studio). It runs after the VN Studio PR is merged.
