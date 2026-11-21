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
- status: open
- asked: 2026-11-21 --:--
- by: director
- why: the live-data step (L0–L8) runs after the ticket work is merged, stops services and changes the user's data; each stop and GPU check needs the user's go-ahead
- default: the live-data step does not start; the branches stay unmerged
- answer:
