# HUB-34: status and start check the health URL, not only the port

Found 2026-11-14 in the run of *The Rooster* (`runs/the-rooster.md`): `hub.ps1` showed lmstudio `up` while
`http://127.0.0.1:1234/v1/models` did not answer, so Scriptorium's embeddings were down and the book stalled after
chapter 1 with no client task waiting.

## Plan

1. `Get-Health` replaces `Get-HealthModel`: one request per listening service with an `http` URL, giving Ok and the model.
2. Status: a listening service whose URL does not answer is `no-http`, with a note naming `hub.ps1 start <id>`.
3. Start: on a held port whose URL does not answer, a service with `startWhenSilent: true` in `services.json`
   (lmstudio: `lms server start` is safe to repeat) runs its start again; any other gets a restart hint.
4. The wait after a start ends when the port listens and the URL answers; the timeout message says which failed.

## Changelog

- `scripts/hub.ps1`: `Get-Health`, `no-http` state and note, the start and wait changes above.
- `services.json`: `startWhenSilent: true` on lmstudio.
- Checked live: normal status; `lms server stop` -> down -> `hub.ps1 start lmstudio` -> up; a bare TCP listener on 1234
  -> `no-http` with the note, and `start` re-ran `lms server start` and reported that the URL did not answer.
