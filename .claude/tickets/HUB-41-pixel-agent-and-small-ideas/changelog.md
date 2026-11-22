# Changelog HUB-41

## 2026-11-22 HUB-41 hub tasks H1-H3 (documentation only)

Branch `HUB-41_pixel-agent-and-small-ideas` (creative-hub, from master 2941ac4).

- `ROADMAP.md`: rows 31-33 last cell now carry the recorded outcomes; new row 34 (HUB-41).
- `.claude/tickets/HUB-40-extra-ideas/plan.md`: N1 names `force: true`; N2 path in the reindex command uses forward slashes, with a note.
- `CLAUDE.md` (line 11), `services.json` (line 156), `README.md` (line 39): Pixel Studio has no local vision model; pixel-studio row lists the four MCP tools.

Verification: `git diff` shows only these lines; `services.json` parses; `grep -rn "Pixel's vision rows" CLAUDE.md services.json README.md` prints nothing.
Not done (out of scope for this run): L1-L3 live data, K1-K2 live checks, the repo tickets.
Commit status: committed on the branch (not merged, not pushed).
