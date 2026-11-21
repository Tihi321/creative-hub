## A-001 Approve the HUB-38 plan and answer Q1–Q9 (or accept the recommendations)
- status: answered
- asked: 2026-11-21 --:--
- by: director
- why: the plan is draft; no repo ticket starts until the user says yes and answers Q1–Q9
- options:
  - Approve the plan and answer Q1–Q9 as written
  - Approve the plan and accept the recommendations for Q1–Q9
  - Change the plan first
- recommendation: accept the recommendations for Q1–Q9
- default: the plan stays draft; nothing starts
- answer: Yes, as recommended (Q1–Q9: recommendations accepted), 2026-11-21 --:--

## A-002 Commit and merge the eight ticket branches, then give the go-ahead for the live-data step (stops the proxy and the running apps, edits config in seven data folders and the proxy's settings.json with backups)?
- status: answered
- asked: 2026-11-21 --:--
- by: director
- why: the live-data step (L0–L8) runs after the ticket work is merged, stops services and changes the user's data; each stop and GPU check needs the user's go-ahead
- default: the live-data step does not start; the branches stay unmerged
- answer: Commit and merge (2026-11-21): done locally, not pushed. The live-data go-ahead is asked separately (A-003).

## A-003 Go-ahead for the live-data step L0–L8: stop the ACP proxy (which also stops its Gufo server) and the running apps, back up and edit config in seven data folders and the proxy's settings.json, restart, then run the checks that load Strata onto the GPU?
- status: answered
- asked: 2026-11-21 --:--
- by: director
- why: the live-data step changes the user's data and restarts services; each stop and GPU check needs the user's go-ahead
- default: the live-data step does not start
- answer: Wait for AAP-42, then run it (2026-11-21 --:--). Done: see REQ-0030 log.

## A-004 Commit and merge AAP-43 (embeddings, uncommitted on its branch)? Push the nine repos? Which extra ideas to build? And your steps: install llama.cpp and Inkling in the ACP Proxy app, copy LM Studio's nomic file, run the Scriptorium probe, send one artist request in the Pixel window.
- status: open
- asked: 2026-11-21 --:--
- by: director
- answer (part): "Commit and merge" on 2026-11-21: AAP-43 committed and merged (8f2c913, 527f860), local, not pushed. Done.
- still open: push the nine repos; which extra ideas to build; your steps (install llama.cpp and Inkling, copy the nomic file, run the Scriptorium probe, one artist request in the Pixel window).
- push part: answered "Push all nine" on 2026-11-21 20:25 and done (nine repos pushed to origin, no force). A-004 stays open for the extra ideas and the user's steps.
