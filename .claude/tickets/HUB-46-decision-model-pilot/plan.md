---
status: draft
repos: [C:/projects/Personal/creative-hub, C:/projects/Personal/api-acp-proxy, C:/projects/Personal/scriptorium]
branch: HUB-46_decision-model-pilot
updated: 2026-11-25
---

# HUB-46: decision-model pilot

Build reading (one line, per the global scope rule): **the narrow reading first.** Measure whether a local decision model
agrees with today's reviewers on Scriptorium's yes/no and pick-one calls, offline and at $0. The proxy sidecar (AAP-55) and
the Scriptorium switch (SCP-72) are built only if that measurement passes the go/no-go gate in step 2.

## Why

A decision model (the Jev family and its open counterparts such as vLLM-SR d3) reads its input once and returns a choice, a
P(yes) or a score, with no prose. Its output can be wrong but never malformed. About a third of Scriptorium's LLM calls are
decision-shaped (close to half in long books), and every one goes through `chatJson` with a schema, a repair ask and job
retries. A decision model could make the small gates faster and stop the repair retries. It cannot replace the reviewers:
`withUsableNotes` needs notes on every "revise".

Source: HackerNoon, "20 best open-source AI decision models you can run locally in 2026" (23 Oct 2026, AI-assisted, numbers
from the Jev Decision Index 0.3.2 and vendor model cards). The Reddit post "I tested 14 decision models against local LLMs"
could not be fetched and has not been read. Neither source compares decision models with a local chat model such as Strata
on the same task. That comparison is this ticket's job.

## Open questions for the user

1. **Which models to download** (each download needs your yes, with its size and source). Proposal: measure the whole
   d3 family in step 2, so the pick rests on numbers, not on size alone:
   - **vLLM-SR d3-flash** (8.4B, Apache 2.0, BF16 17.9 GB, Q8 GGUF 9.5 GB; no Jev score found): the expected pick, small enough to sit
     beside Inkling and a ComfyUI model.
   - **vLLM-SR d3-turbo** (26.1B, Apache 2.0, BF16 ~52 GB or FP8 ~27 GB; Jev 70.2 text, 72.9 vision, project estimates):
     the upper bound. Its card names ROCm (`vllm-sr serve vllm-sr/d3-turbo --engine --platform rocm`).
   - **vLLM-SR d3-mini** (4.5B, Apache 2.0, BF16 9.7 GB): the floor.
   Not candidates, with the reason:
   - Mammoth-1 (27B, MIT, top open score 71.24 on Jev 0.4) and Elephant-1 (9B, 62.65): their cards require the OneJev
     runtime on one CUDA GPU (block-bidirectional attention). That runtime does not run on the AMD Strix Halo.
   - NVFP4 builds (Blink, Decider, JEV-35B NVFP4) need an NVIDIA Blackwell card. Blink v0.3 is not on Hugging Face.
   - H2O-Lightning-31B: non-commercial licence.
   - Hosted Jev, Liquid d1-ultra, Fastino GLiDE, SubQ Snap, Microsoft-Decision-1: paid APIs.
2. **The agreement bar** for step 2's go/no-go (proposed: at least 90% agreement with the current model on each gate, and
   no lost "revise" on the continuity gate at the chosen threshold).
3. **Whether Croatian matters here.** Scriptorium writes English books and Book Translator handles Croatian, so the pilot
   tests English only unless you want a Croatian sample.

## Model files (D: only)

All decision-model files, caches and any runtime venv live on D:. Nothing goes to C:. The user approved the downloads on
2026-11-25.

| Path | Source | Size |
|---|---|---|
| `D:\DecisionModels\vllm-sr__d3-mini` | `vllm-sr/d3-mini` (safetensors, BF16) | 9.1 GB |
| `D:\DecisionModels\vllm-sr__d3-flash` | `vllm-sr/d3-flash` | 16.8 GB |
| `D:\DecisionModels\vllm-sr__d3-turbo` | `vllm-sr/d3-turbo` | 52.2 GB |
| `D:\DecisionModels\ggml-org__vllm-d3-mini-GGUF` | Q8_0 + mmproj Q8_0 | 5.5 GB |
| `D:\DecisionModels\ggml-org__vllm-d3-flash-GGUF` | Q8_0 + mmproj Q8_0 | 10.2 GB |
| `D:\DecisionModels\.hf-home` | `HF_HOME` / xet cache for these downloads | - |

- Runtime venv for step 2: `D:\DecisionModels\.venv` (uv, `UV_CACHE_DIR=D:\DecisionModels\.uv-cache`).
- Each repo ships Python run with `trust_remote_code` (`modeling_d3.py`, `d3_engine.py`, `d3_runtime.py`, `d3_server.py`,
  `d3_kernels.py`) and a `readout.safetensors` decision head. The GGUFs very likely do not carry that head, which makes
  llama-server option 3 even less likely to match. Read that code before the first run.

## Scope

Candidate calls, all in `C:/projects/Personal/scriptorium/src/engine`:

| Gate | Where | Shape today | Pilot question |
|---|---|---|---|
| G1 research covered | `pipeline/researchHandlers.ts:122` (`check_notes`) | `{covered, missing}` | P(yes) "do these notes answer the question?" |
| G2 needs research | `pipeline/researchHandlers.ts:365` | `{needs_research, questions[]}` | P(yes) only. The questions still come from the LLM when the answer is yes |
| G3 continuity pre-gate | `pipeline/longHandlers.ts:115` | verdict + continuity score | P(pass). A clear pass skips the full check; anything else runs today's check as now |
| G4 format pick | `pipeline/handlers.ts:583` | format + title + genre | Choice over the enabled formats. Title and genre stay with the LLM |

Not in the pilot, noted for later: the VN script-analyst and edition-aligner classifiers, and an image pre-screen before the
VN/Edu art-critic and Cartoon frame-critic (multimodal d3 could pass the clear cases before the 2-minute Inkling review).

### Out of scope

- Replacing any reviewer, the fact-checker or child-safety (they must write notes; must-pass roles stay as they are).
- Changing `decide()` in `scoring.ts:60` or the model router's family rules.
- Any spend above $0, hosted Jev, paid endpoints.
- Putting a decision model in the exclusive Gufo/Strata/Llama rotation (a switch costs minutes; it would be slower, not faster).
- Starting Scriptorium without asking (it resumes its book factory).

## Steps

### 1. Collect the gate cases (hub, read only on Scriptorium data)

- Find out whether `books/<slug>/log.md` or the job files under `~/Scriptorium/jobs/` keep each gate's prompt and the model's
  answer. If yes, build the case set from finished books. If not, rebuild the prompts with Scriptorium's own
  `buildMessages` in a script, without starting the engine.
- Target: about 50 cases per gate (G1 to G4), saved to `.claude/temp/hub-46/cases/*.jsonl`
  (`{gate, prompt, current_answer, model}`).

### 2. Offline agreement run and go/no-go (hub, $0)

- **Runtime first.** The d3 cards serve decisions through `vllm-sr serve -e` (`POST /v1/systemone`) or transformers
  `model.system_one(...)` with `trust_remote_code`. They do not say that llama.cpp reproduces the decision readout, although
  ggml-org GGUFs exist for d3-mini and d3-flash. Try in this order on the Strix Halo (gfx1151):
  1. `vllm-sr serve --engine --platform rocm`.
  2. transformers on ROCm PyTorch.
  3. A llama-server GGUF, reading the answer token's logprobs.
  Option 3 counts only if its answers match option 1 or 2 on the same 20 cases. Record which runtime worked.
- **Memory.** With your yes on the downloads (question 1), run each model on its own port, outside the proxy, in two
  states: (a) alone, and (b) beside Inkling plus a ComfyUI image model loaded, which is the busiest real case. Record free
  VRAM in each state. A model that does not fit in state (b) can still win, but only as "runs when the GPU is free".
- **Pick on numbers.** `scripts/decision-pilot.mjs` (new) sends each case to each model as choice or yes-no, records the
  answer, P and latency, and compares it with `current_answer`. Report per model and gate:
  - agreement and the disagreements with their text
  - latency p50/p95
  - VRAM
  - calibration (a threshold sweep for G3)
  The pick is the smallest model within 2 points of the best agreement that fits in state (b).
- Write `results.md` here. **Go** only if the bar from question 2 is met on a gate; steps 3 and 4 cover only the gates that
  pass. **No-go:** close the ticket with the numbers.

### 3. Proxy sidecar (api-acp-proxy, AAP-55, only after go)

- A new non-exclusive local server `decide`, which is never part of the turn-taking, like `embed`
  (`src/local-servers.ts:9-12`). It has its own port and command and runs beside whichever chat model is up. Its command is
  whatever runtime step 2 found: a `vllm-sr serve` or Python process, or llama-server only if that passed.
- A proxy route `/v1/decide` passes `{state, questions}` through to the sidecar's `/v1/systemone` and returns the
  probabilities. Model id `acp/decide/<name>`.
- Settings entry and Monitor line, like `embed`.
- Tests: the sidecar does not stop the exclusive servers and is not stopped by them.

### 4. Scriptorium opt-in (scriptorium, SCP-72, only after go)

- For each gate that passed: a per-role config switch (off by default) that asks `acp/decide/<name>` first and falls back to
  today's call when P is below the threshold or the sidecar is down (the `confident_choice` pattern).
- The fallback path must stay exactly today's code path. Record in `made.md` which gates used the decision model.
- Tests: one per gate for "confident → decision used" and "unsure or down → old path".

### 5. Live check and records (hub)

- One short book run with the switch on, only with your yes to start Scriptorium. Compare its gate answers and time with the
  step 2 numbers.
- Run log `runs/hub-46-decision-pilot.md`, ROADMAP row, `changelog.md`.

## Files and modules to touch

| Step | Path |
|---|---|
| 1-2 | `scripts/decision-pilot.mjs` (new), `.claude/temp/hub-46/` (cases, raw output), `.claude/tickets/HUB-46-decision-model-pilot/results.md` |
| 3 | `api-acp-proxy`: `src/local-servers.ts`, `src/settings.ts`, a `/v1/decide` route, monitor view, tests; branch `AAP-55_decide-sidecar` |
| 4 | `scriptorium`: `src/engine/pipeline/researchHandlers.ts`, `longHandlers.ts`, `handlers.ts`, `pipeline/llm.ts` (a `decide` helper), config seed, tests; branch `SCP-72_decision-gates` |
| 5 | `runs/hub-46-decision-pilot.md`, `ROADMAP.md`, `changelog.md` |

## Checklist

- [ ] Open questions answered (model, bar, Croatian)
- [ ] Step 1: case set built (about 50 per gate)
- [ ] Step 2: agreement run, `results.md`, go/no-go recorded
- [ ] Step 3: AAP-55 merged (only after go)
- [ ] Step 4: SCP-72 merged (only after go)
- [ ] Step 5: live book run played back, run log, ROADMAP row moved to Done
