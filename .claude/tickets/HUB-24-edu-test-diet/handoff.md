# HUB-24 handoff

State: DONE on edu-game-studio master 303ee0f (pushed). All tickets EGS-40..46 merged; worktrees removed.
Final: `yarn test` 501 tests / 38 s; `yarn test:e2e` 25 tests / 361 s. Before: 1928 / 103 s and 118 / 1095 s.
Details: changelog.md, timing-before.md, timing-after.md, plan.md.
Rule going forward: whoever changes a shell runs `yarn test:e2e`; EGS-20 CI runs test and test:e2e separately.
Open: the dropped Scriptorium wiring test; `yarn build` not run; check helpers.ts waitFor polling; user has not reviewed the trims.
Process: no PRs; merge locally and push master, never force-push.
