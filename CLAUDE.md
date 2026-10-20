# Creative hub

This folder connects the user's creative tools (Scriptorium, Book Translator, VN Studio, Pixel Studio, Chiptune Studio, VibeTTS, ComfyUI, LM Studio, Strata). `README.md` is the map; `services.json` is the registry.

- For any request to make a book, translation, art, music, voices or a visual novel from an idea, use the `make-visual-novel` skill.
- Check and start services with `scripts\hub.ps1` (status, start, stop, build, logs). Never start Scriptorium without asking: it resumes its whole book factory and may spend on paid models.
- Keep one log per production in `runs/<slug>.md` with every id and decision, so another session can resume.
- When a tool lacks something the chain needs, write it in `ROADMAP.md` under that repo. Change a tool's code only in its own repo, on a branch named after a ticket in that repo's style (e.g. `VNO-04_story-tools`).
- Adding a tool: `services.json`, `.mcp.json`, the README table, the skill, the roadmap.
- Record what was verified and what was not. A production is done only when the user has played it.
