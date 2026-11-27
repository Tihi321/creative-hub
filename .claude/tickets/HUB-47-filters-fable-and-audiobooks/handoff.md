# HUB-47 handoff (2026-11-27, batch done except the user's listening)

## State
- Scriptorium is running with the **factory paused** and `only: null`.
- **the-iron-tide-2:** published at 8.29: 15 chapters, 8 endings, 24,631 words. The EPUB, cover and reader are in `books/the-iron-tide-2/out/`. Continuity is still 6, and the small path notes in ch 9 and ch 11 are left as they are. The old **the-iron-tide** stays rejected.
- **Model defaults (live):** see `runs/factory-2026-11-26.md` and the memory note model-order-cloud-first.
  - writer and architect: Opus 5
  - humanizer: Sonnet 5
  - reviewers: Neon
  - other roles: Hydrogen
  - shared fallbacks: Sonnet, Hydrogen, DeepSeek, Codex, then Strata, Gufo, Llama and Ollama
  - Neon is deliberately not a fallback row.
- **Audiobooks:** all 31 prose books have English audio (323 files, 74.9 h) in `books/<slug>/out/audio/`. Screenplay-format books have none, by the user's decision. The resume steps are in `runs/audiobooks-2026-11.md`.
- **Iron Tide audio drama:** a title track plus 15 chapter tracks and an .m3u in `books/the-iron-tide-2/out/audio/`. The narrator is bm_lewis, and each character has its own voice (the cast map is in `runs/audiobooks-2026-11.md`). The build files are in `.claude/temp/audiobooks/iron/`.
- **Checker:** a fresh director-checker passed every item on 2026-11-27. Listening is UNTESTED.

## Repos
- scriptorium master d7881fc (SCP-73, SCP-74)
- api-acp-proxy master 6a4e061 (AAP-69)
- creative-hub: the HUB-47 row is in ROADMAP.md, and the run logs are updated.

See the commit log for what was pushed.

## Open with the user
1. Listen to the pilots, Orvane, the audiobooks and the Iron Tide drama. Pell's voice sounds adult. The af_nicole books (The Salt Line, The Silent Summit) read about 40% slower; a future run could use speed 1.1.
2. Decide on the 5 blocked generated soother ideas: tallows-teething-troubles, the-ridge-of-lost-things, the-hoard-of-small-comforts, three-peaks-past-naptime, the-whistle-ring-roost.
3. Decide whether the humanizer may fall back to local models.
4. UNTESTED: the Codex fallback live, and Claude usage limits under factory load.
