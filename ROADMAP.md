# Roadmap

The hub connects the tools, so everything that needs them running together lives here: live checks, productions, and features that span two or more tools. Each of those is a ticket with a plan in `.claude/tickets/HUB-NN-<name>/plan.md`, done one by one in the order below. Code changes still happen in each tool's own repo, on a branch named in that repo's style; the plan names it.

Work that touches only one tool is in that tool's own `ROADMAP.md` (table at the end).

## Tasks, in order

| # | Ticket | What | Code in | Needs | Status (2026-10-23) |
|---|---|---|---|---|---|
| 1 | HUB-12 | `hub.ps1 start` returns when piped; deep `call` arguments survive | hub | | Done |
| 2 | HUB-02 | Book Translator live check (BTT-11), with a Croatian VN edition of *The Clockless God* | none | HUB-12 helps | Done: edition aligned 1221/0/0; the user plays it |
| 3 | HUB-03 | VN Studio live check (VNO-08): a test game with CG, insert, SFX, ambience, scene music; Japanese, Arabic and Croatian editions; the user plays it | none | user plays | Done up to the user's play (`vno-media-test`) |
| 4 | HUB-04 | Scriptorium live check (SCP-14), then the skill uses `wait_for_book` | hub | user's go-ahead to start Scriptorium | Done (*The Umbrella Conductor*; `wait_for_book` is in the skill) |
| 5 | HUB-05 | Production: *The Hour That Happens Twice* in Croatian (EPUB) | none | HUB-02; user reads it | Done; EPUB in `runs/the-hour-that-happens-twice/`; the user reads it |
| 6 | HUB-06 | Scriptorium writes VN Studio's new script lines (`CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, `Aliases:`) | scriptorium `SCP-16`, visual-novels-orchestrator `VNO-16` (CG characters at import, recommended) | HUB-03, HUB-04 | H2 done 2026-10-23 up to the user's play: *The Lighthouse That Kept Lists (VN)* adapted by Scriptorium with media lines, imported, built, lint clean (`runs/the-lighthouse-that-kept-lists-vn.md`); some CGs merge two characters (VNO-34) |
| 7 | HUB-13 | VN Studio makes sound effects and ambience with Chiptune Studio (`sound.sfxEngine` / `ambienceEngine: "chiptune"`); from midi-generator's roadmap | visual-novels-orchestrator `VNO-19` | HUB-03 | Live check passed 2026-10-23 (`runs/hub08-13-autostart.md`); the user listens |
| 8 | HUB-08 | VN Studio starts the studios it needs | visual-novels-orchestrator `VNO-11` | HUB-03 | Live check passed 2026-10-23: Chiptune 5.2 s, Pixel 5.7 s, ComfyUI 42.6 s, off switch (`runs/hub08-13-autostart.md`) |
| 9 | HUB-07 | Flow as a VN Studio provider: images, then voices, then music | visual-novels-orchestrator `VNO-10`, flow-music-mcp `FMM-11` | HUB-03, flow-music-mcp's FMM-04 | Images and voices checked live 2026-10-23 (`runs/hub07-flow-test.md`; 12 images, 0 credits; found VNO-22/23/24, FMM-13). Flow Music dropped by the user 2026-10-31. Open: only the 6 hr clips, waiting on Gemini's daily quota; the user plays |
| 10 | HUB-10 | Puzzle visual novels: proof of concept, then VN Studio, then Scriptorium | visual-novels-orchestrator `VNO-12` (proof of concept), then `VNO-13`–`VNO-15`; scriptorium `SCP-18` | HUB-06 for the Scriptorium phase | Phase 5 done 2026-10-23 up to the user's play: *The Winter Garden Clock* (Murdle + Knights and Knaves, proved and read back), Flow images, lint clean (`runs/the-winter-garden-clock.md`) |
| 11 | HUB-11 | Screenplay → video: Scriptorium screenplay writer, Flow production, assembled video | scriptorium `SCP-17`, flow-music-mcp `FMM-12`, hub (`make-video` skill) | HUB-04, HUB-07 | Phase 3 done 2026-10-23 up to the user's watch: 123 s film, 192 Flow credits + 10 Flow Music (`runs/the-lighthouse-that-kept-lists-2.md`, `video/out/final.mp4`) |
| 12 | HUB-15 | Live checks of the merged 2026-10-23 fixes: Scriptorium SCP-26 to 37 with a real model (a VN adaptation, a screenplay, a puzzle mystery), Flow and ComfyUI side by side (VNO-28), the Gemini daily quota (VNO-24, FMM-15), and the user's verdicts on the productions | none planned | the merges of 2026-10-23 | In progress (2026-10-31): C1 to C5 done and verified (`runs/hub15-c4-parallel.md`, `runs/hub07-flow-test.md`, the C1 to C3 run logs); C6 waits on the user's verdicts for HUB-02, 03, 05, 06, 10, 11, 13, 16, 17. Plan: `.claude/tickets/HUB-15-post-merge-live-checks/plan.md`, `handoff.md` |
| 13 | HUB-17 | Children's picture books: a picture-book presentation in VN Studio (one illustration per scene with the cast drawn in, text below, page turns) and the Scriptorium format `kids-picture-book` | visual-novels-orchestrator `VNO-47`, scriptorium `SCP-46` | HUB-16 (pack) | Done 2026-10-25 up to the user's play: *The Bell and the Bicycle* (watercolour) and *The Snail and the Salad* (flat cartoon), 12 pages each, en + hr, builds 0 placeholders and lint clean; `runs/the-bell-and-the-bicycle.md`, `runs/the-snail-and-the-salad.md`, `.claude/tickets/HUB-17-picture-books/`; committed and pushed (`VNO-47` d768077, `SCP-46` a67c831) |
| — | HUB-09 | ACP proxy as a provider in all five apps (Scriptorium, Book Translator, VN Studio, Pixel Studio, Chiptune Studio) | api-acp-proxy `AAP-25` (per-provider cap), pixel-art-generator `PAR-14`, midi-generator `MDI-07` (add-provider UI); packaging `SCP-47`, `VNO-50` | none | Wired 2026-10-27 (branch `HUB-09_acp-everywhere`): proxy restarted with caps (codex 4, antigravity 3), live `providers.md` of all five apps has `acp` enabled with five models, load test in `runs/hub09-acp-load-test.md`. 2026-10-27 later: all five apps pass on acp end to end (Pixel PAR-15 codex 3/3 and gemini 3/3, Chiptune MDI-08 codex 3/3 and gemini 3/3, Scriptorium SCP-48 real 14-job run, AAP-26 hides bare model ids). Branches awaiting PRs: api-acp-proxy `AAP-26` (70e7740), pixel-art-generator `PAR-15_acp-live-ui-check`, midi-generator `MDI-08_acp-live-ui-check`, scriptorium `SCP-48_single-idea-run`, hub `HUB-09_bare-aliases`. Open: merges of AAP-25, AAP-26, PAR-14, PAR-15, MDI-07, MDI-08, SCP-47, SCP-48, VNO-50; Claude provider and three newer models unchecked; art and melodies not reviewed; `.claude/tickets/HUB-09-acp-proxy-wiring/plan.md` |. **Done 2026-10-31:** merged (hub PRs #12 and #13). Claude provider not enabled in proxy; see `.claude/tickets/HUB-09-acp-proxy-wiring/live-check-claude.md` |
| — | HUB-19 | Edu Game Studio | see `.claude/tickets/HUB-19-edu-game-studio/` | none | In progress (resumed 2026-10-31) |

As of 2026-10-25 all three tool repos are on `master` with HUB-16 merged: Scriptorium SCP-45 (PR #13), Book Translator BTT-23 (PR #16), VN Studio VNO-46 (PR #20); hub PR #10. The soother game was rebuilt from `master`.

The code of HUB-06, 07, 08, 10, 11 and 13 is merged (VN Studio PR #11, Scriptorium PR #10, flow-music-mcp PR #5, hub PR #7). Fixes from the 2026-10-23 run sit on branches: Scriptorium `SCP-20-25_fixes` (SCP-20 to 37), Book Translator `BTT-15-20_fixes`, VN Studio `VNO-20-23_fixes` (VNO-20 to 35), flow-music-mcp `FMM-13_composer-popover` (FMM-13 to 16); hub `HUB-06-13_live-checks`.

Each plan has its open questions for the user at the top. When a ticket is done, its plan's checklist is ticked, a `changelog.md` sits next to it, and its row moves to "Done" below.

Still open with no ticket: a native-speaker check of VN Studio's model-written game menus in the 33 languages the user cannot read (HUB-03 covers Croatian).

## Done

- **2026-10-25, HUB-16 language-independent VN packs (merged):** Scriptorium writes the VN pack template + text catalog (`SCP-45`, PR #13), Book Translator translates only the catalog (`BTT-23`, PR #16), VN Studio imports packs and adds catalog editions by ID (`VNO-46`, PR #20), hub contract/skill/roadmap (PR #10). The live soother project rebuilt from `master` with en+hr: 381/381 Croatian beats, 53 assets unchanged, build/lint clean. Details: `.claude/tickets/HUB-16-vn-pack/` and `runs/hub16-vn-pack.md`. The user's play verdict is not separately recorded.
- **2026-10-23, live checks, productions and tool fixes (branches, PRs next):** HUB-07, 08, 13 checked live; productions HUB-06 H2 (lighthouse VN), HUB-10 phase 5 (*The Winter Garden Clock*), HUB-11 phase 3 (first film), each waiting for the user to play or watch. Tool fixes, one commit per ticket: Scriptorium SCP-20 to SCP-37, Book Translator BTT-15 to BTT-20, VN Studio VNO-20 to VNO-35, flow-music-mcp FMM-13 to FMM-16, hub HUB-14 (video planner). Scriptorium config: the retired `:free` fallback replaced by `deepseek/deepseek-flash` (user, 2026-10-23). Images: Google Flow is the default provider in the make-visual-novel skill (user, 2026-10-23).
- **2026-10-22, hub roadmap run (code on branches, PRs next):** HUB-12, HUB-02 to HUB-05 done; HUB-06, 07, 08, 10, 11 and 13 coded (VNO-10 to VNO-16 and VNO-19, SCP-16 to SCP-18 in part, FMM-11, FMM-12, the `make-video` skill). Productions: the Croatian VN edition of *The Clockless God* and *The Hour That Happens Twice* in Croatian (EPUB), model work by Claude, $0. Open: the user plays or reads them, and the live checks after the PRs merge.
- **2026-10-20 to 2026-10-22, all merged to master:** Scriptorium SCP-08 to SCP-14, Book Translator BTT-08 to BTT-11, VN Studio VNO-04 to VNO-08, api-acp-proxy AAP-05, flow-music-mcp FMM-01 to FMM-03, and the hub's FMM-01 to FMM-03 (flow-music-mcp and acp-proxy registered, flow-mcp retired). Every item of the 2026-10-21 fix round is closed in code; the live checks are tasks 2 to 4 above.
- **End to end:** idea → Scriptorium book → VN Studio build → played by the user (*The Clockless God*, linear and choice VNs, `runs/the-clockless-god-vn.md`). Also a series book 2 (`runs/the-hour-that-happens-twice.md`) and a Croatian translation done by Claude through Book Translator (`runs/the-clockless-god.md`).

## Found during the run

Bugs and gaps found on 2026-10-22, in `.claude/tickets/HUB-02-13-roadmap-tasks/followups.md`. All fixed on 2026-10-23 on the fix branches (BTT-15 to BTT-20, SCP-20 to SCP-25, VNO-20 and VNO-21; VNO-21's cause was missing Ren'Py help-screen strings, not stale projects). Not merged yet:

- Book Translator: QA flags kept lines as "untranslated" in VN folders (speaker tag counts as words); the glossary pass overwrites a brief; glossary matching is a case-insensitive substring; an EPUB export keeps the English cover and alt text; a reused pid fools the `engine.lock` takeover; `wait_for_progress` limits; a stopped client's lease stalls the pipeline for 30 min.
- Scriptorium: `title_fixed` ignored; a false story year in rewrite prompts; `log.md` interleaves parallel reviewers; a pitch over 300 words accepted; research tasks for a bedtime story; a packaged `Scriptorium.exe` holds the single-instance lock and `hub.ps1 start` exits silently (hub could name the pid).
- VN Studio: a generate job stays "running" after ComfyUI crashed; partial Croatian UI strings in older projects. (The `Aliases:` sentence left in a character's looks was fixed in VNO-16, cdc82f2.)

## Flow (through flow-music-mcp, since 2026-10-22)

The user has Google Flow (https://flow.google.com/, PRO) and Flow Music (https://www.flowmusic.app/, Google AI Pro, 10,000 credits a month). Both are driven by flow-music-mcp (`hub.ps1 start flow-music-mcp`, port 7462, Chrome CDP 9334). Its `CLAUDE.md` has the UI maps and what was verified.

- Single shots and videos go through Flow's direct composer: the exact prompt, and the live credit quote checked against `max_credits` (default `FLOW_MUSIC_MCP_MAX_CREDITS`, 50) before anything starts. Image sets go through Flow's agent.
- Free: Flow images (Nano Banana), Gemini and Windows voices, assembly, captions. Credits: Flow video, Flow voices, Flow Music songs.
- The user's settings are in flow-music-mcp's `.env`: `FLOW_MUSIC_MCP_UPLOAD_RIGHTS=agree`, the credit cap (50) and the Gemini key.
- Credits after FMM-02's tests (2026-10-22): Flow 1,010 (40 spent).
- flow-mcp (the fork `Tihi321/flow-mcp`, Studio panel on 8787, Chrome 9333) is retired after Flow's redesign and kept as a reference only.

## Antigravity models and the ACP proxy

The user asked (2026-10-22) whether Scriptorium and Book Translator could use their Antigravity (Google) account's models the way the DeepSeek Harness does. **Decision (user, 2026-10-22): no Antigravity login of our own in the apps; use the ACP proxy, accepting the terms risk below. Revived and widened to all five apps on 2026-10-27 (HUB-09, wired).**

- **How the DeepSeek Harness does it:** the plugin `dsh-tool-antigravity` 0.3.6 (`@cortexkit/antigravity-auth-core`, in `~\.dsh\profiles\desktop`) runs its own Google OAuth with Antigravity's client id, calls Google's private Cloud Code endpoints with the Antigravity CLI's User-Agent, and rotates accounts on 429. That is the pattern Google suspends accounts for.
- **The ACP proxy** (`acp-proxy` in `services.json`, port 7461, `PROXY_IGNORE_SAMPLING=1`) runs Google's own signed `agy_acp_server`, so the tokens never leave Google's program. Setup left for the user: install the Antigravity server, acknowledge its terms, enable it and log in. Claude must not do the Google login.
- **Provider entry** for `config/providers.md` in the apps, once the proxy runs and a provider is logged in (take the model ids from `GET http://127.0.0.1:7461/v1/models`):
  ```yaml
  - id: acp
    kind: openai-compat
    base_url: http://127.0.0.1:7461/v1
    json_schema: false        # the proxy rejects response_format
    concurrency: 2
    models:
      - id: antigravity/gemini-3.8-flash
        family: gemini
        context: 1000000
  ```
- **Terms:** clause 6 of https://antigravity.google/terms forbids "using the Service in connection with products not provided by us" and "using third party software, tools, or services to access the Service", gives "using OpenClaw with Antigravity OAuth" as an example, and says it "may be grounds for suspension or termination of your Antigravity and/or Gemini CLI accounts". Accounts were suspended from February 2026, and appeals were slow.
  - Both routes break clause 6 when a book factory is the client. The proxy is only less detectable.
  - If used at all, use an account the user can afford to lose, not the one that holds the Flow Pro plan.
  - Also check whether the DeepSeek Harness setup is itself at risk: it uses the same plugin with the same Google account.
- **The allowed way to get Gemini:** a Gemini API key (AI Studio, has a free tier) or OpenRouter, both already provider kinds in the apps.

## Each tool's own roadmap

Work that touches only one tool, done in its repo on its own ticket branch.

| Tool | Roadmap | Open there |
|---|---|---|
| Scriptorium | `C:\projects\Personal\scriptorium\ROADMAP.md` | nothing after `SCP-20-25_fixes` (SCP-20 to 25); check the SCP-19 settings migration at the next start |
| Book Translator | `C:\projects\Personal\book-translator\ROADMAP.md` | nothing after `BTT-15-20_fixes` (BTT-15 to 20) |
| VN Studio | `C:\projects\Personal\visual-novels-orchestrator\ROADMAP.md` | nothing planned after `VNO-20-23_fixes` (VNO-20 to 24); "Later": Start buttons, VibeTTS auto-start, "Open in" while a headless studio holds the lock, hard kill leaves started services, Flow follow-ups; help-screen strings for the 35 languages other than hr |
| Pixel Studio | `C:\projects\Personal\pixel-art-generator\ROADMAP.md` | nothing (PAR-07 to PAR-13 done) |
| Chiptune Studio | `C:\projects\Personal\midi-generator\ROADMAP.md` | nothing |
| comfy-mcp | `C:\projects\Personal\comfy-mcp\ROADMAP.md` | a bypassed subgraph is dropped; the rest of the TTS Audio Suite engines are not mapped |
| ACP proxy | `C:\projects\Personal\api-acp-proxy\ROADMAP.md` | text only (not needed by the hub) |
| flow-music-mcp | `C:\projects\Personal\flow-music-mcp\ROADMAP.md` | FMM-13 on its branch; failure states and the 4K download not seen live; Scenes, Library and Tools not automated; Studio panel later; optional repo rename |
