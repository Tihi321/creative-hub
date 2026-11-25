# HUB-46 results, phase A: d3-mini and d3-flash (2026-11-25)

Every number below was taken in the state **"busy GPU (Strata loaded)"**: Strata held about 55-68 GB of the 64 GB dedicated VRAM
through the ACP proxy for the whole run (adapter shared memory 17-29 GB), so the d3 weights and activations lived mostly in shared
memory. Not measured: d3-turbo, the "alone" state, the Inkling + ComfyUI state (see the end). **Provisional** until turbo and the
user's bar.

Cases: 187 collected, scored 49 / 34 / 50 / 42 (G1 / G2 / G3 / G4). Dropped: G1 one null answer; G2 the 3 nonfiction cases (forced
true by code); G4 8 cases with only one enabled format (nothing to pick, recorded as skipped). G3 baseline = the effective verdict
(29 pass, 21 revise). The baseline mixes models, so "agreement" is agreement with whichever model happened to answer, not accuracy.

## Runtime and method

- `scripts/decision-pilot.mjs` posts one question per case to `/v1/systemone` (state = system + user text, nothing trimmed; the
  longest case is 31,708 tokens; G1 739-3,361, G2 827-1,092, G4 710-11,045 tokens).
- llama-server Q8_0 (`D:\LlamaCpp\bin\ggml-org-b12681-rocm`, native `/v1/systemone`) with `-ngl all -c 65536 -b 49152 -ub 49152
  -np 1`. **Two things the earlier toy check in `notes.md` missed:** (1) this build only finds the GPU if the ROCm SDK `bin`
  (`C:\Program Files\AMD\ROCm\7.2\bin`) is on PATH (the proxy's AAP-58 fix); without it `--list-devices` prints "(none)" and it
  runs on the CPU. The toy llama numbers (730-875 ms) were CPU numbers. (2) A decision model reads the whole input in one pass, so
  `-b`/`-ub` must be at least the prompt length or the request fails with HTTP 500 "input too large".
- transformers (the repo's own `d3_server.py`, BF16, ROCm torch) on port 19000. It runs out of memory on inputs of about 19k
  tokens and more (G3). After one OOM the HIP context stays broken (`AcceleratorError`), so every later request fails until restart.

## Question wording (frozen)

v1 (used for every result below):
- G1 "Do the notes already answer the question?"; G2 "Does this outline need outside research before writing?"; G3 "Is the chapter
  consistent with the earlier story, with no continuity errors that must be fixed?" (yes = pass); G4 "Which format suits the source
  best?" (choice over the formats parsed from the prompt: id -> its description line).

One refinement allowed, tried on the first 10 G1 and first 10 G3 cases of d3-mini (llama):
- G1 v1: 10/10 agree, so no change.
- G3 v1: 6/10 agree; all 4 baseline "revise" were called pass (P(pass) 0.82-0.92). v2 inverted the question: "Does the new chapter
  contradict, or break, anything the book has already established (facts, names, timeline, character details)?", P(pass) = 1 - P(yes).
  Result: the same 6/10 and the same 4 misses. v2 gave no gain and was discarded; v1 stays. No further tuning.

## 20-case match check, d3-mini: transformers BF16 vs llama-server Q8_0 (plan Step 2 rule)

5 cases per gate. G3 could not use the first 5 on transformers (4 of the 5 are 19-28k tokens: OOM), so the G3 set is the 5 shortest
cases (7-11k tokens). Results: **1 of 20 answers differ; max |dP| = 0.0146** (G1 0.0084, G2 0.0088, G3 0.0061, G4 0.0146).
- The one difference: G4 case 0, a near-tie. transformers short-story 0.367 / novella 0.291 / novel 0.343; llama short-story 0.352 /
  novella 0.290 / novel 0.357 (confidence 0.004).
- Rule "flag if more than 1 of 20": **not flagged** (exactly 1), but it is at the edge. A wider check with d3-flash (llama Q8 vs transformers BF16
  on the full G1/G2/G4 run, n=125): 2 answers differ (G1 case 39 and G2 case 19, both within 0.5 +/- 0.03 of the line), max |dP| 0.048,
  no G4 difference. Treat llama-server Q8 as matching, except on near-ties.
- Speed on the same cases: llama Q8 is faster than transformers on this machine (G1 ~1.3 s vs 2.9 s; G3 11-37 s vs 17-38 s per case at
  7-11k tokens; llama G4 ~0.4 s vs 0.6 s).
- Files: `.claude/temp/hub-46/out/match20-*.jsonl`, comparer `.claude/temp/hub-46/compare.mjs`.

## Agreement per model, runtime and gate (P(yes) >= 0.5)

Confusion is baseline vs d3 (yes = covered / needs research / pass).

| model, runtime | gate | n | agree | agreement | p50 ms | p95 ms | base yes, d3 yes / base yes, d3 no / base no, d3 yes / base no, d3 no |
|---|---|---|---|---|---|---|---|
| d3-mini llama Q8 | G1 | 49 | 44 | 89.8% | 1235 | 2399 | 11 / 0 / 5 / 33 |
| d3-mini llama Q8 | G2 | 34 | 10 | 29.4% | 455 | 570 | 1 / 23 / 1 / 9 |
| d3-mini llama Q8 | G3 | 50 | 30 | 60.0% | 22,894 | 42,551 | 29 / 0 / 20 / 1 |
| d3-mini llama Q8 | G4 | 42 | 32 | 76.2% | 426 | 2904 | see below |
| d3-flash llama Q8 | G1 | 49 | 45 | 91.8% | 2076 | 3195 | 10 / 1 / 3 / 35 |
| d3-flash llama Q8 | G2 | 34 | 16 | 47.1% | 818 | 988 | 6 / 18 / 0 / 10 |
| d3-flash llama Q8 | G3 | 50 | 29 | 58.0% | 29,524 | 57,709 | 29 / 0 / 21 / 0 |
| d3-flash llama Q8 | G4 | 42 | 36 | 85.7% | 707 | 4396 | see below |
| d3-flash transformers BF16 | G1 | 49 | 44 | 89.8% | 3144 | 4972 | 10 / 1 / 4 / 34 |
| d3-flash transformers BF16 | G2 | 34 | 15 | 44.1% | 1239 | 1613 | 6 / 18 / 1 / 9 |
| d3-flash transformers BF16 | G3 | 1 of 50 | 1 | n/a | 36,469 | n/a | 49 requests failed: 2 OOM, then 47 AcceleratorError |
| d3-flash transformers BF16 | G4 | 42 | 36 | 85.7% | 1058 | 8204 | see below |

G4 confusion (disagreements only, baseline -> d3): mini llama: kids-choice-visual-story -> kids-visual-story x6,
choice-visual-novel -> visual-novel x3, short-story -> novel x1. flash llama: kids-choice-visual-story -> kids-visual-story x5,
short-story -> novella x1. flash transformers: the same six. 17 of the 18 G4 cases that carry "The owner fixed the format: use X" in
the prompt agree for mini (flash: not split out), against 15 of 24 free choices for mini (62.5%), so the G4 figures lean on the prompt
naming the answer. The misses are close siblings (choice-visual-novel vs visual-novel; kids-choice-visual-story vs kids-visual-story),
where the format description is nearly the same text.

Per baseline model (agree/n, mini llama then flash llama; models with n<4 left out):
- G1: deepseek-flash 23/28, 25/28; gemini-3.8-flash 14/14, 14/14; strata/qwen3.8-flash-next-low 6/6, 6/6.
- G2: strata/qwen3.8-flash-next 1/10, 3/10; deepseek-flash 5/13, 5/13; claude-code 4/9, 7/9.
- G3: deepseek-flash 13/16, 13/16; gemini-4-argon 6/15, 5/15; acp/strata/qwen3.8-flash-next-unsloth 2/9, 2/9; nail-qwen3.6 4/4, 4/4.
  (Low agreement is where those models said "revise".)
- G4: strata/qwen3.8-flash-next 11/11, 11/11; deepseek-flash 5/14, 9/14; claude-code 6/7, 6/7; nemotron 6/6, 6/6; claude-sonnet-5 4/4, 4/4.

Memory (adapter counters; amd-smi is broken; the Strata baseline before my runs was dedicated 68.3 GB, shared 22.3 GB, RAM free
about 20 GB; the counters cannot separate processes, and the proxy's own embed server also runs):
- d3-mini llama Q8: dedicated max 67.6 GB (min 55.8), shared max 28.9 GB, RAM free min 21 GB. The Q8 weights are 4.7 GB.
- d3-flash llama Q8: dedicated max 67.6 GB, shared max 25.3 GB, RAM free min 22.4 GB.
- d3-flash transformers BF16 (17.9 GB weights): dedicated max 68.3 GB, shared max 47.4 GB, **RAM free min 0.3 GB** during the G3
  OOM storm. The machine was within 0.3 GB of its limit. Stopped; nothing else was affected as far as I could see.
- d3-mini transformers BF16: only the 20-case check (about 9 GB), memory not sampled.

## G1 and G3 thresholds (calibration)

G3 sweep, P(pass) >= threshold auto-passes the chapter. "Lost revise" = auto-passed although the baseline said revise.

| threshold | mini: auto-passed | mini: lost revises | flash: auto-passed | flash: lost revises |
|---|---|---|---|---|
| 0.5 | 49/50 (98%) | 20 | 50/50 (100%) | 21 |
| 0.7 | 49/50 | 20 | 49/50 (98%) | 20 |
| 0.8 | 39/50 (78%) | 15 | 49/50 | 20 |
| 0.9 | 12/50 (24%) | 5 | 21/50 (42%) | 9 |
| 0.95 | 1/50 (2%) | 0 | 1/50 (2%) | 0 |
| 0.98 and 0.99 | 0 | 0 | 0 | 0 |

The only threshold with 0 lost revises (0.95) auto-passes 1 of 50 chapters. The model's P(pass) is 0.5-0.95 for almost everything,
and the 21 revises sit inside the same range as the 29 passes: it does not rank them. Also slow here: G3 p50 23-30 s per chapter
(prefill of 7-32k tokens in one pass), 19 min (mini) and 26 min (flash) for the 50 cases.

G1 sweep (post-hoc, 49 cases, only 11 baseline "covered"; do not read it as tuned): P(covered) >= 0.7 gives 9 auto-covered cases and
0 wrong for both models; at 0.5 mini has 5 wrong "covered" and flash 3 (the costly direction, since it would skip research the
baseline asked for). All the G1 misses are at P 0.52-0.69.

## Disagreement examples (book, case, reason)

- G1 mini: the-clockless-god-2 (P 0.69), the-silent-signal (0.61), the-clockless-god (0.57), france-s-atomic-clock (0.54): baseline "not
  covered", d3 "covered", all just over 0.5. flash: the-silent-summit (0.25, the one baseline "covered" called not covered).
- G2: d3 says "no research" almost always (mean P(yes) 0.20 mini, 0.27 flash; max 0.70 / 0.86) where the baseline said yes in 24 of 34,
  for example circuit-breaker (0.13), the-tide-table (0.10), windward-drift (0.35), the-clockless-god (0.43). Looks like the
  question is read as "is research required" against the fiction outline, not "would a good outline gain from research"; no
  re-wording was tried (the one allowed refinement was spent on G1/G3).
- G3: the-poisoned-well-of-harrowdale (0.92), the-light-at-worlds-end (0.88-0.91), echoes-in-the-deep (0.82), the-automaton-who-confessed
  (0.89): baseline "revise", d3 "pass".
- G4: short-story vs novel on a near-tie; choice-visual-novel vs visual-novel and kids-choice-visual-story vs kids-visual-story on
  sibling formats.

## Proposed bar and go/no-go (provisional)

Bar used as the default (open question 2 is unanswered): agreement >= 90% on the gate, and for G3 a threshold with 0 lost revises
that still auto-passes a useful share. Agreement with a mixed-model baseline is a proxy, not accuracy.

| gate | d3-mini (llama Q8) | d3-flash (llama Q8) | note |
|---|---|---|---|
| G1 research covered | NO-GO at 0.5 (89.8%); borderline | GO, provisionally (91.8%; transformers 89.8%) | flash only with a confidence threshold of about 0.7, which on 49 cases gave 0 wrong at 9/49 skipped searches. The threshold is post-hoc; check it on fresh cases before use |
| G2 needs research | NO-GO (29.4%) | NO-GO (47.1%) | d3 almost never says "needs research" |
| G3 continuity pre-gate | NO-GO (60%; 0 lost revises only at 0.95, 2% auto-passed) | NO-GO (58%; same) | it cannot tell revise from pass; and 23-30 s per chapter |
| G4 format pick | NO-GO (76.2%) | NO-GO at 90% (85.7%) | flash's misses are sibling formats and 17 of 18 owner-fixed cases are given in the prompt; free choices were not split out for flash |

Pick if only one model: d3-flash (higher than mini on G1, G2 and G4; level on G3; both are far from the bar on G2 and G3). turbo may change the G2/G3/G4 rows.
Do not start AAP-55/SCP-72 for G2, G3 or G4 on these numbers.

## Not measured

- **d3-turbo** and the **alone state**: not measured in phase A; see "Phase B" at the end (turbo does not change a verdict).
- "Alone" state: measured in phase B; the p50/p95 in the phase A tables are the busy-GPU numbers.
- **Inkling + ComfyUI state (b)**: not run.
- d3-mini transformers beyond the 20 cases; d3-flash llama vs transformers beyond the G1/G2/G4 run (G3 transformers failed on memory).
- Q8 vs BF16 on G3 beyond the 5 shortest chapters (transformers cannot hold the long ones).
- Accuracy against a ground truth (only agreement with the recorded baseline); several baseline models disagree with each other.
- Croatian; more than 49/34/50/42 cases, so a 2-point difference is within noise (one case is 2-3 points).

## Rerun

```
# 1. llama-server (needs the ROCm SDK bin on PATH, and -b/-ub >= the longest prompt)
.claude/temp/hub-46/runtime/start_llama.ps1 -Gguf D:/DecisionModels/ggml-org__vllm-d3-flash-GGUF/vllm-d3-flash-Q8_0.gguf -Port 18999 -Log <log>
# wait for "model loaded" in <log>, then:
fnm exec --using default node scripts/decision-pilot.mjs --url http://127.0.0.1:18999 --label d3-flash-llama
# transformers: .claude/temp/hub-46/runtime/start_tf.ps1 -Model D:/DecisionModels/vllm-sr__d3-flash -Port 19000 -Log <log>
# report: node .claude/temp/hub-46/report.mjs d3-flash-llama   (files in .claude/temp/hub-46/out/)
# stop: .claude/temp/hub-46/runtime/stop_llama.ps1 -Log <log>  (only kills the PID it started)
```

Raw output: `.claude/temp/hub-46/out/*.jsonl` (one record per case), memory samples `mem-*.csv`.

# Phase B (2026-11-25): alone state, and d3-turbo

Strata's engine was ended by the user before this phase. GPU dedicated usage at the start was 1.1 GB of 64 GB (the proxy's embed
server and the idle Strata app python processes were still running and were not touched). Same cases (175 scored requests: 49 / 34 /
50 / 42), same v1 questions, same runner as phase A. Raw files: `.claude/temp/hub-46/out/d3-{mini,flash}-llama-alone.jsonl`,
`d3-turbo-tf.jsonl`, `d3-turbo-tf-g3-run1.jsonl`, `mem-*-alone.csv`, `mem-d3-turbo-tf.csv`.

## Alone timings, llama-server Q8_0 (same args as phase A)

Answers are the same as phase A: **0 of 175 answers differ** for d3-mini (max |dP| 0.0033) and for d3-flash (max |dP| 0.0000), so
every agreement figure in phase A stands unchanged for these two models. Only the latency moved, and little: median and p90 in ms
(busy = phase A with Strata loaded):

| gate | mini busy med / p90 | mini alone med / p90 | flash busy med / p90 | flash alone med / p90 |
|---|---|---|---|---|
| G1 | 1235 / 2025 | 847 / 1256 | 2076 / 2836 | 1371 / 1996 |
| G2 | 455 / 542 | 425 / 481 | 818 / 967 | 700 / 793 |
| G3 | 22,894 / 34,849 | 20,307 / 30,909 | 29,524 / 44,988 | 25,796 / 38,198 |
| G4 | 426 / 1828 | 378 / 1313 | 707 / 2739 | 608 / 1966 |

Alone is 5-35% faster; the G3 chapters (7-32k tokens in one pass) take 20-26 s median even with the GPU to itself (about 17.5 min
for mini, 22 min for flash over the 50 cases), so the prefill is compute-bound, not memory-bound. G3 stays too slow for a per-chapter
pre-gate regardless of the GPU state. The G1 threshold 0.7 check gives the same result alone: 9 auto-covered cases, 0 wrong, for both.

Memory alone (adapter counters; the baseline before the run was dedicated 1.1 GB, shared 0.1 GB): mini dedicated max 23.9 GB,
shared max 9.5 GB, RAM free min 38.1 GB. flash dedicated max 31.4 GB, shared max 11.2 GB, RAM free min 37.4 GB. (The maxima
include the 49,152-token compute buffers of `-ub 49152`, not only the 4.7 / 9 GB weights.)

## d3-turbo (26B, BF16, transformers; no GGUF exists, nothing was downloaded or converted)

llama-server cannot load the BF16 safetensors folder (it needs a GGUF; none is on D: and none was fetched). Run through the repo's
own `d3_server.py` (transformers 5.17, ROCm torch, BF16, `prefix_bidir` attention, validated length 32,768; the same server
protocol as mini and flash, no request change needed). Load about 40 s plus about 4 min kernel warm-up. All caches on D:.

| gate | n | agree | agreement | median / p90 ms | base yes,d3 yes / yes,no / no,yes / no,no | note |
|---|---|---|---|---|---|---|
| G1 | 49 | 45 | 91.8% | 6824 / 9066 | 9 / 2 / 2 / 36 | threshold 0.7: 10 auto-covered, 1 wrong (flash and mini: 9 and 0). 0.5: 11 auto-covered, 2 wrong |
| G2 | 34 | 23 | 67.6% | 3299 / 3711 | 17 / 7 / 4 / 6 | much better than flash (47.1%) and mini (29.4%), still far from 90% |
| G3 | 7 of 50 run | 5 of 7 | n/a (see below) | 60,228 (median of 7) | | failed from 14,386 tokens up |
| G4 | 42 | 34 | 81.0% | 2799 / 8331 | see below | 18 of 18 owner-fixed agree, 16 of 24 free choices (66.7%); flash 17/18 and 19/24 (79.2%), mini 17/18 and 15/24 |

G4 misses: choice-visual-novel -> visual-novel x3, kids-choice-visual-story -> kids-visual-story x5 (the same sibling formats as
mini and flash). G2 per baseline model for turbo: strata/qwen3.8-flash-next 9/10, deepseek-flash 8/13, claude-code 5/9.

**G3 on turbo: only 7 of 50 chapters could be run.** Run shortest first (cases 11, 39, 12, 44, 13, 0, 21; 7,165-12,081 tokens, 33-87 s
each). The next case (case 9, 14,386 tokens) failed with HTTP 500 AcceleratorError (HIP "unspecified launch failure"); the memory
log shows RAM free fell to 1.2 GB and shared GPU memory to 50.6 GB at that moment, so this is the same memory exhaustion as with
flash. The server was killed and restarted, and case 9 was retried alone: **same failure**, so it is reproducible and not a
leftover broken context. The other 43 cases are longer (14,453 up to 31,708 tokens) and were **not run** (they were not attempted,
to avoid starving the machine's RAM again). Run: cases 11, 39, 12, 44, 13, 0, 21. Not run: the 43 others (every case >= 14,386 tokens).

On those 7 (2 baseline "revise"): turbo P(pass) 0.77, 0.72, 0.35, 0.41, 0.66, 0.62, 0.90 = 5 of 7 agree. It did mark one revise below 0.5
(case 12, 0.35) and a second at 0.66 (case 13); it called one baseline "pass" a fail (case 44, 0.41). mini and flash on the same 7:
P(pass) 0.83-0.93 for all, 5 of 7 agree (both revises missed). Threshold on the 7: 0.7 auto-passes 3 of 7 with 0 lost revises; 0.5 auto-passes
5 of 7 with 1 lost revise. This is a promising sign (turbo spreads its scores and does not call everything a pass) but 7 cases,
2 of them revise, prove nothing, and the long chapters, where a gate would pay off, cannot be run on this machine through transformers.
The G3 latency is also higher (33-87 s for 7-12k tokens) than llama Q8 on mini or flash (about 11-37 s at the same lengths).

Memory, d3-turbo transformers: dedicated max 68.1 GB (the 52 GB of BF16 weights plus activations; it hit the 64 GB dedicated limit
and spilled), shared max 50.6 GB, **RAM free min about 0 GB (0.0-1.2 GB in the failing request)**. The machine was at its limit
during the failure; no other process was stopped by it as far as I saw.

## Phase B verdict

Bar: agreement >= 90% on the gate (open question 2 still unanswered, so this default stands).

| gate | d3-mini | d3-flash | d3-turbo (transformers) | verdict |
|---|---|---|---|---|
| G1 | 89.8% | 91.8% | 91.8% | unchanged: GO provisionally for flash (or turbo) with threshold about 0.7; turbo takes about 7 s per call against 1-2 s, and its 0.7 gate had 1 wrong where flash and mini had 0. Flash is the pick |
| G2 | 29.4% | 47.1% | 67.6% | NO-GO, turbo is better but below the bar |
| G3 | 60.0% | 58.0% | 5 of 7, unmeasured | NO-GO: not proven for turbo, and no runtime here can run its long chapters |
| G4 | 76.2% | 85.7% | 81.0% | NO-GO (free choices 62.5-79.2%) |

**Turbo does not change a verdict.** Do not start AAP-55 / SCP-72 for G2, G3 or G4. For G1, flash on llama-server remains the one
provisional GO (and the threshold 0.7 should be checked on fresh cases before use).

## Phase B, not measured

- d3-turbo G3 for 43 of 50 chapters (>= 14,386 tokens); the gate result for turbo is therefore open. A turbo GGUF (llama-server)
  would probably run them, but none exists and none was converted or downloaded; ask the user before fetching or converting
  (converting the 52 GB BF16 would need the llama.cpp converter and about 52 GB of free space on D:; 240 GB free there).
- d3-turbo via llama-server, FP8 (27 GB) or any quantised variant.
- The Inkling + ComfyUI state (b).
- All Phase A "Not measured" items other than the alone state and turbo.
