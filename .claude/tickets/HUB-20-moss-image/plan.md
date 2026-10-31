# HUB-20 moss-image engine

Scope (narrow reading): add ComfyUI's MOSS-Image text-to-image (template `image_moss_image_t2i`) as an image engine `moss-image` in the two places the hub generates assets: comfy-mcp (used by the hub skills) and edu-game-studio (its own copy of the engine registry). Not an edit engine: the model takes no reference image.

## Template facts (user/default/workflows/image_moss_image_t2i.json, subgraph)
- Models (all present): diffusion_models/moss_image_sft_int8_convrot.safetensors, text_encoders/qwen3.5_9b_w4a8_gptq.safetensors (CLIPLoader type `moss_image`), vae/flux2-vae_small.safetensors.
- Graph: UNETLoader(default) -> KSampler; CLIPLoader -> CLIPTextEncode (positive) and CLIPTextEncode (negative); EmptyFlux2LatentImage; KSampler; VAELoader -> VAEDecode -> SaveImage.
- Defaults: 1024x1024, 25 steps, CFG 2.5, er_sde / simple, denoise 1. Negative `nsfw, worst quality, bad anatomy, watermark, jpeg artifact`. Official: 50 steps, CFG 3, euler.
- Template switches: prompt enhancer (TextGenerate) is ON in the outer node, SkipLayerGuidanceDiTSimple (layer 22) switch is OFF. We build with both off: no enhancer (keeps one model load, deterministic prompt), no SLG.
- Sizes: multiples of 16, 1 to 2 MP recommended.

## Slices
1. comfy-mcp, branch `CMC-07_moss-image` from master: `DEFAULT_FILES.moss`, `FileGroups.moss`, `buildMossImage`, `ENGINES['moss-image']` (usesNegative, size 1024 square, defaults above, default negative text when the caller gives none), `mergeFiles`; engine list in `src/mcp/tools.ts`, `INSTRUCTIONS` in `src/mcp/server.ts`, README row, header comment, ROADMAP item CMC-07, test in `tests/graphs.test.ts`. Check `src/config.ts` / `service.ts` merge file groups generically.
2. edu-game-studio, new worktree `edu-game-studio-moss`, branch `EGS-23_moss-image` from `EGS-19_android` (c4c5294): same registry change in `src/engine/comfy/graphs.ts`, test in `tests/comfy-client.test.ts`, `seed/config/comfy.md` (`moss` group), ROADMAP item EGS-23.
3. hub, branch `HUB-20_moss-image` from master: one-line mention in `.claude/skills/make-visual-novel/SKILL.md` ComfyUI fallback line; README only if it lists engines. Leave `.agents/` untracked. Keep edits minimal (another worker edits README/ROADMAP/services.json on the HUB-19 branch).

## Verify
- `npm test`, `typecheck`, `lint` in both repos.
- Live: rebuild/start comfy-mcp (scripts\hub.ps1, never Scriptorium), `generate_image` engine `moss-image` at 1024x1024, record time and path. No paid credits.

## Out of scope
Prompt enhancer toggle, SLG toggle, bf16 / base checkpoint variants (override via `--files`).
