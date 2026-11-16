---
status: done
request: REQ-0028
repos: [creative-hub]
branch: HUB-37_hub-leftovers
updated: 2026-11-16
---

# HUB-37 Hub leftovers

## Scope

1. Re-sync the Codex skill copy `.agents/skills/make-visual-novel/SKILL.md` with `.claude/skills/make-visual-novel/SKILL.md` (it lagged: HUB-33 music lines and others). Kept Codex differences: `client/Codex`, the `- id: Codex` line, "Codex aborts". Other mirrored skill, `make-video`, already differs only by the Codex wording.
2. `scripts/hub.ps1` `Get-Health`: decode a byte[] `Content` (response without a JSON Content-Type) as UTF-8 before `ConvertFrom-Json`, so Model and Notes are filled.
3. `.claude/temp/ash-and-brass/call.py` (uncommitted temp script): reconfigure stdout and stderr to utf-8.

## Acceptance

- A diff of source and mirror for each skill shows only the Codex wording differences.
- A HttpListener stub with no Content-Type still gives Model and Notes through `Get-Health`; `hub.ps1 status` still runs.
- `call.py` prints characters outside cp1252 on Windows.
- ROADMAP.md has a HUB-37 row, Done.
