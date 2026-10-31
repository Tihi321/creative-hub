# hub18-ps1-dreamcast, 2026-10-31

Live check of VNO-51 + MDI-11 (unmerged branches, built locally). Details: `.claude/tickets/HUB-18-ps1-dreamcast-music/live-check.md`.

- VN Studio projects (data ~/VisualNovels/projects): `hub18-neon-static` (dreamcast, dreamwave/synthwave/darkwave), `hub18-hollow-memory` (ps1, darkwave/darkwave/sad). Delete with `vno_delete_project` when done.
- Jobs: `hub18-neon-static--vn.pipeline.run--all--r1`, `hub18-neon-static--vn.build--now--r2`, `hub18-neon-static--vn.lint--now--r3`; composer tasks `hub18-neon-static--vn.music.plan--all--r1#1`, `hub18-hollow-memory--vn.music.plan--all--r1#1` (answered by client/claude-code).
- Decision: composer = client/claude-code, art provider hand, to spend nothing.
- Scratch: `.claude/temp/hub18b/` (mcp.mjs helper, cmp-*.ogg chip comparison renders).
- Open: user listens to the six oggs.
