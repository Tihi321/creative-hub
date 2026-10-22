# HUB-08 changelog

2026-10-22. Tool work: VN Studio VNO-11 (branch `VNO-10-19_hub-roadmap`).

- VN Studio starts Pixel Studio, Chiptune Studio and ComfyUI when a job needs them, using the commands in the hub's `services.json` (`seed/config/autostart.md`).
- Hub (commit 170ee2e): the skill and the `_about` in `services.json`. Notes: `hub-notes.md`.

Verified: the VN Studio tests.
Not verified: the live check (a job that starts a stopped studio). It runs after the VN Studio PR is merged.
