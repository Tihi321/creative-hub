# Roadmap

The hub connects the tools, so everything that needs them running together lives here: live checks, productions, and features that span two or more tools. Each of those is a ticket with a plan in `.claude/tickets/HUB-NN-<name>/plan.md`, done one by one in the order below. Code changes still happen in each tool's own repo, on a branch named in that repo's style; the plan names it.

Work that touches only one tool is in that tool's own `ROADMAP.md` (table at the end).

## Tasks, in order

| # | Ticket | What | Code in | Needs |
|---|---|---|---|---|
| 1 | HUB-12 | `hub.ps1 start` returns when piped; deep `call` arguments survive | hub | |
| 2 | HUB-02 | Book Translator live check (BTT-11), with a Croatian VN edition of *The Clockless God* | none | HUB-12 helps |
| 3 | HUB-03 | VN Studio live check (VNO-08): a test game with CG, insert, SFX, ambience, scene music; Japanese, Arabic and Croatian editions; the user plays it | none | user plays |
| 4 | HUB-04 | Scriptorium live check (SCP-14), then the skill uses `wait_for_book` | hub | user's go-ahead to start Scriptorium |
| 5 | HUB-05 | Production: *The Hour That Happens Twice* in Croatian (EPUB) | none | HUB-02; user reads it |
| 6 | HUB-06 | Scriptorium writes VN Studio's new script lines (`CG:`, `INSERT:`, `SFX:`, `AMBIENCE:`, `Aliases:`) | scriptorium `SCP-16`, visual-novels-orchestrator `VNO-16` (CG characters at import, recommended) | HUB-03, HUB-04 |
| 7 | HUB-08 | VN Studio starts the studios it needs | visual-novels-orchestrator `VNO-11` | HUB-03 |
| 8 | HUB-07 | Flow as a VN Studio provider: images, then voices, then music | visual-novels-orchestrator `VNO-10`, flow-music-mcp `FMM-11` | HUB-03, flow-music-mcp's FMM-04 |
| 9 | HUB-10 | Puzzle visual novels: proof of concept, then VN Studio, then Scriptorium | visual-novels-orchestrator `VNO-12` (proof of concept), then `VNO-13`–`VNO-15`; scriptorium `SCP-18` | HUB-06 for the Scriptorium phase |
| 10 | HUB-11 | Screenplay → video: Scriptorium screenplay writer, Flow production, assembled video | scriptorium `SCP-17`, flow-music-mcp `FMM-12`, hub (`make-video` skill) | HUB-04, HUB-07 |
| — | HUB-09 | ACP proxy as a provider for Scriptorium and Book Translator | none | **on hold** (user, 2026-10-22) |

Each plan has its open questions for the user at the top. When a ticket is done, its plan's checklist is ticked, a `changelog.md` sits next to it, and its row moves to "Done" below.

Still open with no ticket: a native-speaker check of VN Studio's model-written game menus in the 33 languages the user cannot read (HUB-03 covers Croatian).

## Done

- **2026-10-20 to 2026-10-22, all merged to master:** Scriptorium SCP-08 to SCP-14, Book Translator BTT-08 to BTT-11, VN Studio VNO-04 to VNO-08, api-acp-proxy AAP-05, flow-music-mcp FMM-01 to FMM-03, and the hub's FMM-01 to FMM-03 (flow-music-mcp and acp-proxy registered, flow-mcp retired). Every item of the 2026-10-21 fix round is closed in code; the live checks are tasks 2 to 4 above.
- **End to end:** idea → Scriptorium book → VN Studio build → played by the user (*The Clockless God*, linear and choice VNs, `runs/the-clockless-god-vn.md`). Also a series book 2 (`runs/the-hour-that-happens-twice.md`) and a Croatian translation done by Claude through Book Translator (`runs/the-clockless-god.md`).

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
| Scriptorium | `C:\projects\Personal\scriptorium\ROADMAP.md` | fallbacks as an open list, small SCP-14 follow-ups, Electron tests |
| Book Translator | `C:\projects\Personal\book-translator\ROADMAP.md` | BTT-11 UI check, reload during a run |
| VN Studio | `C:\projects\Personal\visual-novels-orchestrator\ROADMAP.md` | VNO-08 test gaps |
| Pixel Studio | `C:\projects\Personal\pixel-art-generator\ROADMAP.md` | per-document tools, faster drawing, VN UI elements |
| Chiptune Studio | `C:\projects\Personal\midi-generator\ROADMAP.md` | motifs, SFX and ambience, port env var |
| comfy-mcp | `C:\projects\Personal\comfy-mcp\ROADMAP.md` | subgraph workflows, more speech engines, jobs lost on restart |
| ACP proxy | `C:\projects\Personal\api-acp-proxy\ROADMAP.md` | limits seen from the hub |
| flow-music-mcp | `C:\projects\Personal\flow-music-mcp\ROADMAP.md` | vocal songs, cost per song, Veo/720p, tests, Studio panel |
