---
status: approved
request: REQ-0026
repos: [creative-hub]
branch: HUB-36_allowpartial-skill-note
updated: 2026-11-16
---
# HUB-36: the make-visual-novel skill says what to do when `export_project` refuses

Request: `REQ-0026` (`.claude/director/requests/REQ-0026-extra-ideas-from-ash-and-brass.md:29`, "one sentence on Book
Translator's `allowPartial` export refusal in the make-visual-novel skill (both copies)"). Source of the behaviour: Book
Translator BTT-31 (`C:\projects\Personal\book-translator\.claude\tickets\BTT-31-retry-and-export\`, merged at `efef8d6`),
whose plan flagged this sentence as a hub follow-up (`plan.md:44`).

What BTT-31 does (checked in the book-translator repo): `export_project` refuses while any block a chunk covers has no
translation (a `failed`, `pending` or in-progress chunk, or no chunks yet). The error starts with `export refused:`
(`src/shared/protocol.ts:13`, `EXPORT_REFUSED`) and names the chunks and the block count. `allowPartial: true` exports
anyway, leaves those blocks in the source language and adds a warning. `retry_chunk {projectId, index}` returns at once;
`wait_for_progress` follows it (`src/engine/mcp/server.ts:259-267`).

## Scope

Two sentences in the `make-visual-novel` skill, section "2. Translate (optional)", in both copies:

> If `export_project` answers an error that starts with `export refused:`, it names the chunks that still have
> untranslated blocks: `retry_chunk` each one (one at a time, `wait_for_progress` until it is done before the next), then
> export again. Pass `allowPartial: true` only when the user accepts those blocks staying in the source language.

Placed once, as a sub-bullet right after the EPUB bullet (line 107) so it covers both the EPUB export (line 107) and the
VN edition export (step 2, line 111); step 2 gets a short pointer `(refused: see above)` after `export_project {...}`.
The wording is model-neutral, so it is the same text in both copies.

Plus one row `HUB-36` in `ROADMAP.md`.

## Out of scope

- Any code change in Book Translator (BTT-31 is merged; its MCP INSTRUCTIONS already say it, `server.ts:26`).
- The other hub skills (`make-video`, `make-edu-game`, `make-cartoon`): they do not call `export_project`.
- Re-syncing the rest of the Codex mirror: `.agents/skills/make-visual-novel/SKILL.md` lags the source (it lacks the
  HUB-33 music lines, around source lines 122-127). Only the HUB-36 sentences are added to it here; a full re-sync is a
  separate item, noted in the run report, not done.
- `AGENTS.md` (the Codex mirror of `CLAUDE.md`), `README.md`, `services.json`.
- A live run of a translation that gets refused.

## Files to touch

| File | Role | Change |
|---|---|---|
| `C:\projects\Personal\creative-hub\.claude\skills\make-visual-novel\SKILL.md` | **Source** (the Claude Code copy; every later skill change, HUB-25/26/33, landed here) | the sub-bullet after line 107; the pointer in step 2, line 111 |
| `C:\projects\Personal\creative-hub\.agents\skills\make-visual-novel\SKILL.md` | **Codex mirror**, hand-copied from the source in HUB-21 (`6449c04`, "Codex mirrors"); not generated, no sync script exists (`scripts/` has none); differs from the source only by `client/Codex` for `client/claude-code` and the missing HUB-33 lines | the same two edits at the same lines (107, 111), same text |
| `C:\projects\Personal\creative-hub\ROADMAP.md` | hub roadmap | row 29 after the HUB-35 row (line 40) |

No copy under `~/.claude/skills` (checked: `~/.claude/skills/make-visual-novel` does not exist; only `make-pdf`,
`make-video` match `make-*` there) and none under `~/.codex/skills` or `~/.agents/skills`.

## Tasks

1. **Source skill.** Input: `.claude/skills/make-visual-novel/SKILL.md:105-118`, the text above. Output: the sub-bullet
   under the line-107 bullet and the pointer in line 111. Keep the file's style (backticked tool names, short sentences,
   no colon before a list).
2. **Codex mirror.** Input: task 1's diff, `.agents/skills/make-visual-novel/SKILL.md:107, :111`. Output: the same two
   edits, identical text. Check: `diff` of the two files shows no new differences beyond the existing ones (the
   `client/Codex` lines and the HUB-33 block).
3. **Roadmap row.** Input: `ROADMAP.md:39-40` (rows 27-28). Output, after line 40:

   ```
   | 29 | HUB-36 | The make-visual-novel skill (both copies) says that Book Translator's `export_project` refuses a project with untranslated blocks (`export refused:` names the chunks): `retry_chunk` them one at a time, pass `allowPartial: true` only when the user accepts source-language blocks (`.claude/tickets/HUB-36-allowpartial-skill-note/plan.md`, REQ-0026) | hub (`.claude/skills/make-visual-novel/SKILL.md`, `.agents/skills/make-visual-novel/SKILL.md`) | BTT-31 (merged) | Done (2026-11-16): skill text only; not exercised in a run |
   ```

   (The worker writes the Status cell as it stands when the ticket closes.)

## Acceptance criteria

No tests (skill text and a roadmap row).

| # | Criterion | Proven by |
|---|---|---|
| A1 | Both copies have the sentences in section 2, after the EPUB bullet, with `export refused:`, `retry_chunk` one at a time, and `allowPartial: true` only on the user's OK | `grep -n "export refused:" .claude/skills/make-visual-novel/SKILL.md .agents/skills/make-visual-novel/SKILL.md` (one hit each, same line number) |
| A2 | Step 2 (VN edition) points to it | read line 111 in both copies |
| A3 | The mirror gained no other difference | `diff` of the two copies before and after: the same hunks (`client/Codex` lines, HUB-33 block), none added |
| A4 | `ROADMAP.md` has the HUB-36 row in the 6-column format of rows 27-28 | read `ROADMAP.md:39-41` |

## Live checks (UNTESTED)

- **L1 (UNTESTED)** the next production that translates with Book Translator and meets a refused export: the agent
  retries the named chunks one at a time and asks the user before `allowPartial: true`. Record it in that run's
  `runs/<slug>.md`. Not run in this ticket.

## Commit plan

Branch `HUB-36_allowpartial-skill-note` from `master` (the user's OK to branch is part of the director's go). One commit:

```
HUB-36: make-visual-novel says what to do when export_project refuses

Both skill copies (.claude source, .agents Codex mirror) and the roadmap row.
```

with the attribution line. Then `changelog.md` in this folder and plan `status: done` in a second commit
`HUB-36: close the ticket files`. Merge and push only when the user asks.
