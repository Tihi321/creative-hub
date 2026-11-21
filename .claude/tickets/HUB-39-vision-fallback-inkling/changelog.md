# Changelog HUB-39

## 2026-11-21 - HUB-39, hub tasks H1-H4 (docs only)

Outcome: the hub docs say the VN and Edu art-critic and the Cartoon frame-critic use `acp/llama/inkling-2-mini`; Pixel's vision rows are the only ones still on `lmstudio`.

creative-hub, branch `HUB-39_vision-fallback-inkling`:
- `CLAUDE.md`: the LM Studio sentence of line 11 replaced (H1).
- `services.json`: `lmstudio.note` sentence replaced (H2); file still parses.
- `README.md`: GPU exception appended to the ACP paragraph (H3).
- `.claude/skills/make-visual-novel/SKILL.md`, `.agents/skills/make-visual-novel/SKILL.md`: same added clause on the ComfyUI-out-of-memory bullet (H3).
- `ROADMAP.md`: row 32 HUB-39, status Planned (H4).

Deviations: none. README text was appended inside the existing line-76 paragraph; the ROADMAP row follows row 31.

Verification: `services.json` parsed with node, no stray control characters; `git diff` shows only these lines. Not run: the three repo tickets, L0-L3 live data, K0-K5 live checks (not this worker's part).

Follow-ups: L0-L3 and K0-K5 after the repo tickets merge.

Commit status: committed on the branch, not merged, not pushed.
