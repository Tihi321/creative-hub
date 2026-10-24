# Creative hub

This folder connects the user's creative tools (Scriptorium, Book Translator, VN Studio, Pixel Studio, Chiptune Studio, VibeTTS, ComfyUI, LM Studio, Strata). `README.md` is the map; `services.json` is the registry.

- For any request to make a book, translation, art, music, voices or a visual novel from an idea, use the `make-visual-novel` skill.
- For a short film, cartoon or video from an idea or a book, use the `make-video` skill.
- Video spends Flow credits: agree a budget first (default 150 per production); `scripts/video-plan.mjs` keeps the estimate and each call's `max_credits`.
- Check and start services with `scripts\hub.ps1` (status, start, stop, build, logs). Never start Scriptorium without asking: it resumes its whole book factory and may spend on paid models.
- Keep one log per production in `runs/<slug>.md` with every id and decision, so another session can resume.
- `ROADMAP.md` holds the hub's tasks: live checks, productions and features that span two or more tools, each a `HUB-NN` ticket with a plan in `.claude/tickets/HUB-NN-<name>/plan.md`, done one by one. A gap that touches only one tool goes in that tool's own `ROADMAP.md`, in its repo. Change a tool's code only in its own repo, on a branch named after a ticket in that repo's style (e.g. `VNO-04_story-tools`).
- Adding a tool: `services.json`, `.mcp.json`, the README table, the skill, the roadmap.
- Voice allocation (Google Voice Gemini TTS vs local VibeTTS): Gemini TTS free tier limit is 10 requests/day. If voice lines for a language exceed the remaining free quota, use local voice (VibeTTS). Always prefer Croatian on Google Voice over English. If both languages are needed and together exceed the free tier for that day, generate only Croatian on Google Voice and use local VibeTTS for English.
- Record what was verified and what was not. A production is done only when the user has played it.
