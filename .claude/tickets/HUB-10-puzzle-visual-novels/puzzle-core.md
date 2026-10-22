# The puzzle core as VN Studio makes it (VNO-13, commit f85c602 on VNO-10-19_hub-roadmap)

`vno_puzzle_generate {band, seed?}` answers `{seed, band, core, names, text, difficulty, ms, next}`. Core (seed 1, medium; `steps` = 27 deduction steps `{rule, cell: [a, b], value: "yes"|"no", clue?, from?}`):

```json
{"format":1,"kind":"murdle","size":3,"seed":1,"band":"medium",
 "categories":[{"key":"suspect","items":["s1","s2","s3"]},{"key":"weapon","items":["w1","w2","w3"]},{"key":"place","items":["p1","p2","p3"]}],
 "solution":{"s1":{"place":"p1","weapon":"w1"},"s2":{"place":"p3","weapon":"w2"},"s3":{"place":"p2","weapon":"w3"}},
 "clues":[{"id":"c1","type":"not","a":"s2","b":"w1"},{"id":"c2","type":"either","a":"p2","b":["w1","w3"]},{"id":"c3","type":"either","a":"s2","b":["p2","p3"]},{"id":"c4","type":"not","a":"s3","b":"w1"},{"id":"c5","type":"is","a":"s3","b":"p2"}],
 "murder":{"place":"p1","answer":{"suspect":"s1","weapon":"w1","place":"p1"}},
 "difficulty":{"steps":27,"score":37,"rules":{"clue":5,"elim":14,"last":6,"trans":2}},
 "steps":[]}
```
names: `{"s1":"Colonel Ash","s2":"Doctor Birch","s3":"Miss Cole","w1":"rope","w2":"candlestick","w3":"poison","p1":"library","p2":"kitchen","p3":"garden"}`
text: `{"c1":"Doctor Birch did not have the rope.","c2":"Either the rope or the poison was in the kitchen.","c3":"Doctor Birch was either in the kitchen or the garden.","c4":"Miss Cole did not have the rope.","c5":"Miss Cole was in the kitchen.","murder":"The body was found in the library."}`

- Ids: s1.. suspects, w1.. weapons, p1.. places. Clue types: is, not, either (b is a 2-item array).
- Back from Scriptorium: the hub passes the core + the story's names + each clue's prose text + clueAt (clue id -> beat id) through `vno_puzzle_set`; the prose is checked with `vno_puzzle_check_text` (a separate reader reads only the prose, from `vno_puzzle_get`'s `readBackTask`).
- Puzzle beat in a story: `{id, type: "puzzle", puzzle: key}`; entry `{key, kind, data (core), names, text, links?, clueAt?, onFail?, hints?, verified}`; edition `puzzles: {key: {names, text}}`.
