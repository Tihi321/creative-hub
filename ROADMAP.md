# Roadmap

The hub connects the tools, so everything that needs them running together lives here: live checks, productions, and features that span two or more tools. Each of those is a ticket with a plan in `.claude/tickets/HUB-NN-<name>/plan.md`, done one by one in the order below. Code changes still happen in each tool's own repo, on a branch named in that repo's style; the plan names it.

Work that touches only one tool is in that tool's own `ROADMAP.md` (table at the end).

## Tasks, in order

| # | Ticket | What | Code in | Needs | Status (2026-10-22) |
|---|---|---|---|---|---|
| 1 | HUB-12 | `hub.ps1 start` returns when piped; deep `call` arguments survive | hub | | Done |
| 2 | HUB-02 | Book Translator live check (BTT-11), with a Croatian VN edition of *The Clockless God* | none | HUB-12 helps | Done: edition aligned 1221/0/0; the user plays it |
| 3 | HUB-03 | VN Studio live check (VNO-08): a test game with CG, insert, SFX, ambience, scene music; Japanese, Arabic and Croatian editions; the user plays it | none | user plays | Done up to the user's play (`vno-media-test`) |
| 4 | HUB-04 | Scriptorium live check (SCP-14), then the skill uses `wait_for_book` | hub | user's go-ahead to start Scriptorium | Done (*The Umbrella Conductor*; `wait_for_book` is in the skill) |
| 5 | HUB-05 | Production: *The Hour That Happens Twice* in Croatian (EPUB) | none | HUB-02; user reads it | Done; EPUB in `runs/the-hour-that-happens-twice/`; the user reads it |
| 6 | HUB-06 | Scriptorium writes VN Studio's new script lines (`CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, `Aliases:`) | scriptorium `SCP-16`, visual-novels-orchestrator `VNO-16` (CG characters at import, recommended) | HUB-03, HUB-04 | Code done (SCP-16, VNO-16); H1 contract check passed; H2 live adaptation after the PRs merge |
| 7 | HUB-13 | VN Studio makes sound effects and ambience with Chiptune Studio (`sound.sfxEngine` / `ambienceEngine: "chiptune"`); from midi-generator's roadmap | visual-novels-orchestrator `VNO-19` | HUB-03 | Code done; live check after the PRs merge |
| 8 | HUB-08 | VN Studio starts the studios it needs | visual-novels-orchestrator `VNO-11` | HUB-03 | Code done; live check after the PRs merge |
| 9 | HUB-07 | Flow as a VN Studio provider: images, then voices, then music | visual-novels-orchestrator `VNO-10`, flow-music-mcp `FMM-11` | HUB-03, flow-music-mcp's FMM-04 | Code done; live check after the PRs merge (music spends credits) |
| 10 | HUB-10 | Puzzle visual novels: proof of concept, then VN Studio, then Scriptorium | visual-novels-orchestrator `VNO-12` (proof of concept), then `VNO-13`–`VNO-15`; scriptorium `SCP-18` | HUB-06 for the Scriptorium phase | Phases 1-2 done (VNO-12, VNO-13); phases 3-4 in progress (VNO-14, VNO-15, SCP-18); phase 5 production after the PRs merge |
| 11 | HUB-11 | Screenplay → video: Scriptorium screenplay writer, Flow production, assembled video | scriptorium `SCP-17`, flow-music-mcp `FMM-12`, hub (`make-video` skill) | HUB-04, HUB-07 | Phases 1, 2a, 2b done (SCP-17, FMM-12, `make-video` skill; not tried live); phase 3 production after the PRs merge |
| — | HUB-09 | ACP proxy as a provider for Scriptorium and Book Translator | none | **on hold** (user, 2026-10-22) | On hold |

The code of HUB-06, 07, 08, 10, 11 and 13 sits on branches, not merged yet: VN Studio `VNO-10-19_hub-roadmap`, Scriptorium `SCP-16-18_hub-roadmap`, flow-music-mcp `FMM-11-12_hub-roadmap`. The PRs come next; the live checks and productions marked "after the PRs merge" start then.

Each plan has its open questions for the user at the top. When a ticket is done, its plan's checklist is ticked, a `changelog.md` sits next to it, and its row moves to "Done" below.

Still open with no ticket: a native-speaker check of VN Studio's model-written game menus in the 33 languages the user cannot read (HUB-03 covers Croatian).

## Done

- **2026-10-22, hub roadmap run (code on branches, PRs next):** HUB-12, HUB-02 to HUB-05 done; HUB-06, 07, 08, 10, 11 and 13 coded (VNO-10 to VNO-16 and VNO-19, SCP-16 to SCP-18 in part, FMM-11, FMM-12, the `make-video` skill). Productions: the Croatian VN edition of *The Clockless God* and *The Hour That Happens Twice* in Croatian (EPUB), model work by Claude, $0. Open: the user plays or reads them, and the live checks after the PRs merge.
- **2026-10-20 to 2026-10-22, all merged to master:** Scriptorium SCP-08 to SCP-14, Book Translator BTT-08 to BTT-11, VN Studio VNO-04 to VNO-08, api-acp-proxy AAP-05, flow-music-mcp FMM-01 to FMM-03, and the hub's FMM-01 to FMM-03 (flow-music-mcp and acp-proxy registered, flow-mcp retired). Every item of the 2026-10-21 fix round is closed in code; the live checks are tasks 2 to 4 above.
- **End to end:** idea → Scriptorium book → VN Studio build → played by the user (*The Clockless God*, linear and choice VNs, `runs/the-clockless-god-vn.md`). Also a series book 2 (`runs/the-hour-that-happens-twice.md`) and a Croatian translation done by Claude through Book Translator (`runs/the-clockless-god.md`).

## Found during the run

Bugs and gaps found on 2026-10-22, in `.claude/tickets/HUB-02-13-roadmap-tasks/followups.md`. Each goes into that tool's own `ROADMAP.md`:

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

The user asked (2026-10-22) whether Scriptorium and Book Translator could use their Antigravity (Google) account's models the way the DeepSeek Harness does. **Decision (user, 2026-10-22): no Antigravity login of our own in the apps; use the ACP proxy, accepting the terms risk below. On hold for now** ("no need for now, later if needed"); the steps are in HUB-09.

- **How the DeepSeek Harness does it:** the plugin `dsh-tool-antigravity` 0.3.6 (`@cortexkit/antigravity-auth-core`, in `~\.dsh\profiles\desktop`) runs its own Google OAuth with Antigravity's client id, calls Google's private Cloud Code endpoints with the Antigravity CLI's User-Agent, and rotates accounts on 429. That is the pattern Google suspends accounts for.
- **The ACP proxy** (`acp-proxy` in `services.json`, port 7461, `PROXY_IGNORE_SAMPLING=1`) runs Google's own signed `agy_acp_server`, so the tokens never leave Google's program. Setup left for the user: install the Antigravity server, acknowledge its terms, enable it and log in. Claude must not do the Google login.
- **Provider entry** for `config/providers.md` in both apps, once the proxy runs and a provider is logged in (take the model ids from `GET http://127.0.0.1:7461/v1/models`):
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
| Scriptorium | `C:\projects\Personal\scriptorium\ROADMAP.md` | fallbacks as an open list, small SCP-14 follow-ups, Electron tests; `title_fixed` ignored, false story year in rewrite prompts, `log.md` interleaving, packaged-app instance lock |
| Book Translator | `C:\projects\Personal\book-translator\ROADMAP.md` | BTT-11 UI check, reload during a run; QA false "untranslated" on VN lines, brief overwritten by the glossary pass, glossary substring matching, English cover in exports, stale lock pid reuse |
| VN Studio | `C:\projects\Personal\visual-novels-orchestrator\ROADMAP.md` | VNO-08 test gaps; lost ComfyUI job, partial `hr` UI strings in older projects |
| Pixel Studio | `C:\projects\Personal\pixel-art-generator\ROADMAP.md` | per-document tools, faster drawing, VN UI elements |
| Chiptune Studio | `C:\projects\Personal\midi-generator\ROADMAP.md` | motifs, port env var (SFX and ambience done by VN Studio, VNO-19; nothing else open from it) |
| comfy-mcp | `C:\projects\Personal\comfy-mcp\ROADMAP.md` | subgraph workflows, more speech engines, jobs lost on restart |
| ACP proxy | `C:\projects\Personal\api-acp-proxy\ROADMAP.md` | limits seen from the hub |
| flow-music-mcp | `C:\projects\Personal\flow-music-mcp\ROADMAP.md` | vocal songs, cost per song, Veo/720p, tests, Studio panel (FMM-11 voice hooks and FMM-12 `flow_assemble` timeline on a branch) |
