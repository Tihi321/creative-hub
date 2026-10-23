# HUB-02 to HUB-13: the hub roadmap, run in one go

Asked by the user on 2026-10-22: every tool repo's own roadmap is done and merged, so run the hub's `ROADMAP.md` (everything that spans the project), on a single branch per repo, one ticket per commit.

## Checked before starting (2026-10-22)

- All tool repos are on `master` with their roadmap branches merged: scriptorium a8cf243 (SCP-19), book-translator 2a21970 (BTT-13/14), visual-novels-orchestrator 81abb9e (VNO-17/18), pixel-art-generator 7e43181 (PAR-07-13), midi-generator 1a6ef78 (MDI-05), comfy-mcp 5ce3126 (CMC-03-06), api-acp-proxy e7dfc02 (AAP-10), flow-music-mcp fd55686 (FMM-04-10).
- vibe-tts-flow has uncommitted VTF-09 (Higgs Audio v3) work by the user. Not touched. VibeTTS is running but its MCP (7723) does not answer, so VN voice steps go last.
- Left open in a tool roadmap that needs two tools: midi-generator "VN Studio does not call `compose_sfx`". It becomes **HUB-13** (VN Studio `VNO-19`), and also answers HUB-03's "where does the SFX file come from".

## User decisions (2026-10-22)

- Scriptorium may be started; Claude does the model work (client provider for writer/architect, reviewers on Scriptorium's own models). Check `factory_status` right after a start and pause ideas nobody asked for.
- Every open question in HUB-06, HUB-07, HUB-08, HUB-10 and HUB-11: take the plan's recommendation.
- Credits: spend up to the plans' caps without asking (HUB-07 Flow Music `flowMusicMaxSongs` 4 per project; HUB-11 first video 150 Flow credits). The free animatic still comes first.
- HUB-02: `localizeNames` off (English names in the Croatian VN edition).
- VibeTTS: proceed; voices last, after the user's VTF-09 lands.

## Branches (one per repo)

| Repo | Branch | Tickets (one commit or more each, `<TICKET>: <what>`) |
|---|---|---|
| creative-hub | `HUB-02-13_roadmap-tasks` | HUB-12, HUB-02, HUB-03, HUB-04, HUB-05, HUB-06, HUB-13, HUB-08, HUB-07, HUB-10, HUB-11 (hub parts: scripts, skills, docs, run logs, roadmap) |
| visual-novels-orchestrator | `VNO-10-19_hub-roadmap` | VNO-16, VNO-19, VNO-11, VNO-10, VNO-12, VNO-13, VNO-14, VNO-15 |
| scriptorium | `SCP-16-18_hub-roadmap` | SCP-16, SCP-17, SCP-18 |
| flow-music-mcp | `FMM-11-12_hub-roadmap` | FMM-11, FMM-12 |

- Tool branches live in **git worktrees** next to the repo (`C:\projects\Personal\<repo>-wt`), because the hub runs each tool from its main checkout (`out/`, `dist/`), which must stay on `master` for the live checks.
- Each tool ticket gets `.claude/tickets/<TICKET>-<name>/plan.md` (its part of the hub plan) and `changelog.md` in its repo, and its row in that repo's `ROADMAP.md`.
- No push, PR or merge until the code is done and tested; then one PR per repo.

## Order

Stream A, the hub (live checks on the master builds):

1. HUB-12 `hub.ps1` start/call fixes (needed to drive the tools with `hub.ps1 call` while the MCP links are down).
2. HUB-02 Book Translator live check + Croatian VN edition.
3. HUB-03 VN Studio live check: test game `vno-media-test` (up to the play; SFX from Chiptune Studio `compose_sfx` imported by hand until VNO-19 lands).
4. HUB-04 Scriptorium live check + `wait_for_book` in the skill.
5. HUB-05 *The Hour That Happens Twice* in Croatian.

Streams B, C, D, the code (in parallel with A, sequential inside each repo):

- VN Studio: VNO-16 (HUB-06) → VNO-19 (HUB-13) → VNO-11 (HUB-08) → VNO-10 (HUB-07, after FMM-11) → VNO-12 → VNO-13 → VNO-14 → VNO-15 (HUB-10).
- Scriptorium: SCP-16 (HUB-06) → SCP-17 (HUB-11) → SCP-18 (HUB-10 phase 4, after VNO-13 fixes the puzzle data).
- flow-music-mcp: FMM-11 (HUB-07) → FMM-12 (HUB-11).

Then the hub parts of HUB-06, 13, 08, 07, 10, 11 (skills, docs, `scripts/video-plan.mjs`), and the live runs and productions once the tool branches are merged and rebuilt.

## HUB-13: VN Studio makes SFX and ambience with Chiptune Studio (VNO-19)

- From midi-generator's `ROADMAP.md` ("Open"): `sound.sfxEngine: "chiptune"` calls Chiptune Studio's `compose_sfx` (with `path`) for `sfx_` sounds, and for `amb_` ambience when the ambience engine is set to chiptune.
- VN Studio: the new engine value in `shared/vn.ts` / config schema, the call through the existing Chiptune MCP client, tests with a fake client, docs (`docs/mcp-guide.md` "Pictures and sounds"), `ROADMAP.md` row.
- midi-generator: the "Open" item moves to done (docs only, on `MDI-06_vn-sfx-done` if a commit there is wanted, else noted in the hub).
- Hub: the skill says which `sfxEngine` to use; HUB-03's SFX can come from it.

## Done when

Every ticket's checklist is ticked with a `changelog.md` beside its plan, the hub `ROADMAP.md` rows move to "Done", and every production has been played or watched by the user (hub `CLAUDE.md`).
