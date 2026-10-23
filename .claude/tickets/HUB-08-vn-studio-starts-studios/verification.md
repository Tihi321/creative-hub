# HUB-08 live verification

2026-10-23, VN Studio master 2f22db1 (VNO-11 merged in PR #11), Pixel Studio and Chiptune Studio master builds, Strata down. Test project `hub08-13-autostart` (run log `runs/hub08-13-autostart.md`).

| Plan step | Result |
|---|---|
| 1 Build and restart VN Studio | Pass: `hub.ps1 build vn-studio pixel-studio chiptune-studio`, `start vn-studio comfyui` |
| 2 `config/autostart.md` seeded, no warning | Pass: `enabled: true`, registry = hub `services.json` |
| 3 Studios down | Pass: pixel-studio and chiptune-studio down before the jobs |
| 4 Test project | Pass: `hub08-13-autostart`, pixel art, chiptune music (nes, 1 track), chiptune sfx/ambience |
| 5 Music starts Chiptune Studio | Pass: `autostart chiptune-studio: down, starting ...electron.exe . --mcp-only (pid 23696)`, `up after 5.2 s`; music_01 v1.ogg with loop points; `logs/chiptune-studio.out.log` has the "started by VN Studio" header |
| 6 Art starts Pixel Studio | Pass: `up after 5.7 s`; `post pixel art with Pixel Studio`; no built-in pixelate warning |
| 7 ComfyUI started (Strata down) | Pass: `hub.ps1 stop comfyui`, `vno_asset_regen bg_harbour_night`: `autostart comfyui ... up after 42.6 s`, done v2.webp |
| 8 Off switch | Pass: `enabled: false`, chiptune stopped, `vno_asset_regen sfx_bell`: three attempts failed with "(auto-start: auto-start is off ...)", nothing started; switched back on |
| 9 `hub.ps1 stop` stops what VN Studio started | Pass (chiptune-studio and comfyui stopped by port); Scriptorium and Strata stayed down |

Not checked: `stopOnExit: true`; the Strata guard (Strata was not running); a studio that exits early (lock held by a desktop app).
