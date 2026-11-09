---
# HUB-28 integration check (director-checker, opus, high), 2026-11-07
VERDICT: PASS (unchecked by a person: real phones, hearing the music, TV)

All A1-A12 PASS:
- Edu master 5b64706 rerun: yarn test 521/521, typecheck, lint and test:e2e 40/40 all exit 0.
- Site: npm run check PASSED (435.1 of 600 MB), test:unit 4/4, playwright 54/54.
- Pages run 42392671777 success at e47cdea.
- edu_lint was not rerun (needs the engine); its result is taken from the run log.

The user's complaint about the Encyclopedia index is fixed live:
- Viewport meta is served.
- The site uses no iframe or fixed box.
- suncev-sustav at 375 is one column with scrollWidth 375.
- The speaker panel works live: music 0.45 at 100, 0.148 at 50, paused at 0; Escape and the backdrop close it; settings persist.

German music is real audio:
- Tracks 60-116 s, about -18 dB; SFX 0.9-1.55 s; no placeholders; no spend.
- The live ogg files return 200.

Desktop: with the final player, the only change is the speaker button; the other differences are animation timing (evidence .claude/temp/hub-28/check/desk/, check/pxdiff.mjs).

Seams PASS: audio contract, 4 voice clip sites, --edu-corner, hub-bridge pill, publish rewrite of player.js (live md5 e20064fa contains the panel).

Findings (none blocks):
1. The run-log desktop note used old-player builds; corrected by this check.
2. TV remote inside the audio panel: the panel's capture listener (src/player/kit/audio-menu.ts:206-232) stops arrows, so a remote cannot reach Sound off, Reduce audio or Close; only Escape closes it. The remote Back key (461/10009) is taken by the bridge (creative-hub-web src/bridge/hub-bridge.js:451-455) and leaves the game. For the user.
3. Existing before HUB-28: the bridge Library pill (hub-bridge.js:87) covers the top-left "Title page" control for 4 s after load and after a touch near the top.
4. Pilot encyclopedia reader: inline gloss buttons are 34 px (inline-word exemption).
5. edu master 5b64706 is not pushed, as planned.

Evidence: C:/projects/Personal/creative-hub/.claude/temp/hub-28/check/
---
