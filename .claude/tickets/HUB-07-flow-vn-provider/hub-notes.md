# HUB-07 phase 4: what the hub needs (from VNO-10, commits cd3eab3..3f4f55d on VNO-10-19_hub-roadmap)

- Prereqs: `hub.ps1 start flow-music-mcp` (signed in, `yarn login` once); Gemini key in its .env; FLOW_MUSIC_MCP_UPLOAD_RIGHTS=agree only for uploading a non-Flow sheet. VN Studio default flowUrl http://127.0.0.1:7462/mcp (VNO_FLOW_URL / config/studios.md flowUrl to change); FLOW_MUSIC_MCP_TOKEN if a bearer token is used.
- Skill (make-visual-novel): `vno_update_settings {art: {provider: "flow"}, voice: {enabled: true, provider: "flow", langs: [...]}}`; check `vno_studios_status` (flow entry) first; `music.provider: "flow"` spends credits (cap flowMusicMaxSongs 4, music jobs run once); a small VN takes ~20-30 min of images; replace the "import Flow files by hand" text.
- README / services.json: VN Studio uses flow-music-mcp; auto-start does not cover it.
- ROADMAP: "Flow in VN Studio" done only after the user played it.
- Run log: media ids, remote ids, timings, credits.
- Not verified until the live run: `asset:<media id>` reference in the direct composer; likeness across sprites; 2K downloads under load; Gemini limits on a whole book; Croatian by ear; Flow Music loop quality; credit cost per song.
