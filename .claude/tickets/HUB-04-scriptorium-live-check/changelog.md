# HUB-04 changelog

2026-10-22, branch `HUB-02-13_roadmap-tasks`, commit ce6626d. Run log: `runs/the-umbrella-conductor.md`.

- Scriptorium live check on the SCP-14+ build: the settings and prompt migrations ran (fallbacks, 36 prompts), and `get_script` and `get_book` answer correctly.
- `wait_for_book` was verified on *The Umbrella Conductor* (score 8.53, $0.044). The skill now waits with it; `wait-book.ps1` stays for when the MCP link is down.

Verified: the migrations, `get_script`, `get_book` and `wait_for_book`.
Not verified: the LM Studio stop test (embeddings down, no job fails); the user reading the book.
Found: SCP-20 to SCP-25 (the title changed despite `title_fixed`, a guessed story year, an interleaved `log.md`, a long pitch, research for bedtime stories, a silent second instance). All are in Scriptorium's ROADMAP (PR #10, merged).
