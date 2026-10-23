# HUB-14 changelog

- `scripts/video-plan.mjs`: title-card keyframe prompt drops the style's "no text/lettering/captions" clauses and asks for the title large and legible; `voices` gives voice-over and Narrator lines the style "as a voice-over narrator"; `insert` shots keep only the characters their action text names (cast, references, prompt); Flow video `spent` and Flow Music `musicSpent` are separate, each with its own budget (`budget.credits`, `budget.musicCredits`, default 10, `--music-budget N`), shown apart in the dry run and the `record` summary; 720p Omni prices 4/6/8/10 s = 7/10/12/15, all `seen`.
- `scripts/video-plan.test.mjs`: price, balance and new HUB-14 tests.
- `.claude/skills/make-video/SKILL.md`: tool calls get 660 s (only `flow_wait` caps at 50); notes on the two budgets, the prices, insert shots, title cards and the voice-over style.
- Old `plan.json` files without `musicCredits` still work (default 10); their `budget.spent` is recalculated on the next `record` without music credits.
