# HUB-46 changelog

## 2026-11-25 - HUB-46 step 2 phase B (alone timings, d3-turbo)

Phase B finished. Turbo changes no verdict: G1 stays a provisional GO for d3-flash; G2, G3 and G4 stay NO-GO.
Turbo's G3 is mostly unmeasured (7 of 50 chapters).

### creative-hub (branch `HUB-46_decision-model-pilot`)
- `.claude/tickets/HUB-46-decision-model-pilot/results.md`: new sections for the alone timings, d3-turbo, the phase B
  verdict and what phase B did not measure; converted to CRLF.
- `.claude/tickets/HUB-46-decision-model-pilot/plan.md`: phase A checklist line closed, phase B line added.
- Scratch only: `.claude/temp/hub-46/turbo_g3.mjs` (G3 shortest first, stop at first failure) and the raw outputs in
  `.claude/temp/hub-46/out/`.

### Deviations
- The Strata engine (pid 16584) kept 46 GB after the unload in the app; it was ended on the user's word.
- Turbo G3 stopped after 7 chapters: the 14,386-token chapter failed twice with a HIP AcceleratorError and RAM fell to
  about 0 GB free, so the 43 longer chapters were not run.

### Verification
- The alone runs gave the same answers as phase A on all 175 scored requests (max dP 0.0033).
- Alone latency is only 5-35% lower; G3 median is 20.3 s (mini) and 25.8 s (flash).
- Turbo agreement: G1 91.8% (1 wrong at 0.7), G2 67.6%, G4 81.0% (free choices 16 of 24), G3 5 of 7.
- After cleanup, the GPU was back to 0.8 GB dedicated and no pilot process was left running.
- Not run: turbo G3 on long chapters, turbo under llama-server, the Inkling plus ComfyUI state, the G1 0.7 cut-off on new cases.

### Follow-ups
- Steps 3 and 4 (AAP-55 sidecar, SCP-72 switch for G1) wait for a go.
- Optional: convert turbo to GGUF (about 52 GB on D:) to measure G3 on long chapters.

Commit status: committed on `HUB-46_decision-model-pilot` in the closing commit; not merged or pushed.

## 2026-11-25 - HUB-46 step 2 phase A (d3-mini, d3-flash)

The agreement run finished with the GPU busy (Strata loaded). Provisional verdicts: G1 GO for d3-flash; G2, G3 and G4
NO-GO for both models. d3-turbo and the alone state are not measured.

### creative-hub (branch `HUB-46_decision-model-pilot`)
- `scripts/decision-pilot.mjs` (new): sends each gate case to a `/v1/systemone` endpoint and writes the answer, P and
  latency per case to `.claude/temp/hub-46/out/<label>.jsonl`.
- `.claude/tickets/HUB-46-decision-model-pilot/results.md` (new): per-gate agreement, the G3 threshold sweep, the 20-case
  match, memory, go/no-go, rerun commands.
- `plan.md`: the runtime facts (ROCm PATH, -b/-ub) and the checklist.

### Deviations
- The G3 part of the 20-case match used the 5 shortest chapters, because transformers goes OOM on longer ones.
- The "busy" state is Strata loaded, not Inkling plus ComfyUI.
- The 90% bar is the default; the user has not answered that question.

### Verification
- Runs: d3-mini llama Q8, d3-flash llama Q8 and d3-flash transformers (G3 failed with OOM). results.md was checked, and
  no process of the run is left running.
- Not run: d3-turbo, the alone state, the Inkling plus ComfyUI state, a fresh-case check of the G1 0.7 threshold.

### Commit status
Committed on `HUB-46_decision-model-pilot` in the closing commit; not merged or pushed.

## 2026-11-25 - HUB-46 step 1 and runtime check

The gate cases are collected, and two runtimes serve d3 on the Strix Halo. The agreement comparison has not run yet.

### creative-hub (branch `HUB-46_decision-model-pilot`)
- `.claude/tickets/HUB-46-decision-model-pilot/plan.md`: status in-progress; model files on D:; the security read of the
  d3 code; the runtime result; the sidecar command now prefers llama-server; checklist updated.
- `discoveries.md`: new, eight findings.
- Scratch, not in git: `.claude/temp/hub-46/cases/G1-G4.jsonl` (187 cases), `collect/collect-cases.mjs`,
  `runtime/notes.md` and the toy scripts.

### Outside the repos
- `D:\DecisionModels`: d3-mini, d3-flash and d3-turbo (safetensors), the Q8 GGUFs of mini and flash, and `.venv`
  (python 3.12, torch 2.9.1+rocm gfx1151, torchvision 0.24.0, transformers 5.17.0, vllm-sr 0.4.0, which does not work on
  Windows), plus the uv cache. About 103 GB in all. Nothing was written to C:.

### Deviations
- G2 has 37 cases, which is all the job files hold.
- `current_answer` comes from each job's result summary, because raw replies are not stored.
- vllm-sr was dropped because it needs Linux or WSL.
- The plan's "llama-server via logprobs" fallback was replaced by llama.cpp's native `/v1/systemone`.

### Verification
- Case files: line counts 50/37/50/50; every row has 2 prompt messages; grep for key patterns found nothing.
- Runtimes: three toy questions on transformers and on llama-server gave the same answers (probabilities within 0.007).
  llama-server on port 18999 is stopped; the log line "decision model type: vllm-d3" is checked.
- Not run: the 20-case match check, d3-flash and d3-turbo, the memory states (a) alone and (b) beside Inkling plus
  ComfyUI, the agreement comparison.

### Commit status
Committed on `HUB-46_decision-model-pilot` in the closing commit; not merged or pushed.
