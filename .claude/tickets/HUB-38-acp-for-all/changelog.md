
# Changelog HUB-38

## 2026-11-22 - HUB-38, record of what landed (written in HUB-40 H3 from REQ-0030's Log and the repos' merge commits)

Outcome: every app reaches every LLM through the ACP proxy (`acp`, port 8787), local models and Scriptorium's embeddings included; LM Studio is not installed and not used.

Repo tickets (all merged `--no-ff` into each local master; merge commits read from `git log --merges` in each repo on 2026-11-22):
- api-acp-proxy: AAP-42 (local thinking), merge `72733cb` (commit `58b80c8`); AAP-43 (local embeddings), merge `527f860`. Pushed with the other repos on 2026-11-21 20:25.
- scriptorium: SCP-65, merge `32d45fe` (commit `09af6de`).
- book-translator: BTT-36, merge `47dd3b2` (commit `7476036`).
- visual-novels-orchestrator: VNO-67, merge `a952829` (commit `adec00c`).
- pixel-art-generator: PAR-19, merge `676fe7b` (commit `fc8c260`).
- midi-generator: MDI-18, merge `911dba3` (commit `173e831`).
- edu-game-studio: EGS-71, merge `f0d7d42` (commit `963f2a5`).
- cartoon-studio: CTS-54, merge `948f705` (commit `37f8a13`; its `.claude/tickets` is gitignored, so its ticket folder is not committed).
- creative-hub: hub docs and `services.json` fixed in `16713ea` (merge of `HUB-38_acp-for-all`, "embeddings through the proxy, LM Studio retired").

Live data steps (recorded in REQ-0030's Log; backups are the `*.bak-HUB-38` files beside each changed file in `BookTranslator`, `CartoonStudio`, `ChiptuneStudio`, `EduGames`, `PixelStudio`, `Scriptorium` and `VisualNovels` `config\`, with `*.bak-HUB-38-L2b` for Scriptorium's `providers.md` and `roles.md`):
- Apps rebuilt and config applied (L2-L8). Edu had 15 roles on `[paid, strata, lmstudio]` (the plan said 13), all moved to `[paid, acp]`; Edu and Cartoon `acp` models were `[]`, so only the six local rows were written.
- Proxy: the old listener was the portable exe from `D:\Programs\ACP-Proxy\ACP-Proxy-Portable-0.1.0-x64.exe`; it was replaced by Electron from the repo. Settings recorded: `listBareAliases` false, `timeoutMs` 900000, codex 4, antigravity 3, claude 2, strata 4.
- Scriptorium embeddings moved to `acp/llama/nomic-embed-text-v1.5` with the `lmstudio` provider off (L2b, H8).

Deviations and errors recorded in the Log:
- Director error, reversed: the Scriptorium book rewrite changed the keys of each book's `models:` job-count history map instead of the model-choice values; all 24 books were restored byte for byte (SHA-256 verified); a read-only scan then showed 0 old refs in model-choice fields. Never rewrite a book's `models:` history.
- Integration check of the eight tickets: FAIL with 2 should-fix (BTT-36 `strata/default` code defaults; VNO-67 probe default included paid `deepseek-flash`); re-check after polish round 1: PASS.
- AAP-43: first check FAIL with 3 should-fix (port check ran with embeddings disabled; default context 512 tokens too small; README backslash paths corrupted); re-check after polish 1: PASS (513 tests, typecheck clean). Technical call: the embedding `ctxSize` is per request, the server gets `-c ctxSize*maxConcurrent`.

Verification recorded as passed in the Log:
- C1 PASS: 29 model ids, none bare, six local ids listed.
- C4 PASS: strata chat with `reasoning_effort: none`, HTTP 200 in 64 s including cold load, no `reasoning_content`; without it `reasoning_content` is present.
- C9 PASS: proxy embeddings against Scriptorium's stored index, cosine 0.992-0.997 on 6 real chunks; a ref change re-indexes nothing; a 2048-token unpunctuated run is refused with 502.
- Scriptorium CLI probe PASS (streamed reply, cost 0, embedding dimension 768).
- Test counts of the repo workers: AAP-43 513 tests; AAP-42 511 tests (the workers' own numbers).

UNTESTED: every live check the Log does not mark as passed (the Log states "every live check is UNTESTED" on 2026-11-21 and then records only C1, C4, C9 and the Scriptorium probe as passed).

Follow-ups: HUB-39 (Inkling as the local vision model of the VN and Edu art-critic and the Cartoon frame-critic); HUB-40 (extra ideas).

Commit status: this file is new in HUB-40 (branch `HUB-40_extra-ideas`).
