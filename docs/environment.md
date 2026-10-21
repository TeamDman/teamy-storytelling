# Environment setup

Target: a separate saved Codex cloud environment named `storytelling-env`, attached to this repository. Do not modify or clone a producer repository merely to make a video.

Include [TeamDman/teamy-docs](https://github.com/TeamDman/teamy-docs) as a second checkout through the supported multi-repository setup. It holds shared provider/reference documentation; this repository holds environment-specific usage and production materials. Read the shared documentation in place instead of copying it. Verify both checkouts are readable in a fresh cloud task. Provider documentation does not authorize paid calls, credentials or expanded permissions, and setup does not require changing teamy-docs.

## Initial status

This initial documentation commit does not assert that any provider is installed or cloud-tested. After setup, record exact versions, installation commands, runtime details and successful render commands here. Do not substitute an installation success for a render test.

## Tools to provision

| Provider | Official source and installation family | Runtime and validation |
| --- | --- | --- |
| PowerPoint | [PptxGenJS](https://github.com/gitbrent/PptxGenJS), npm `pptxgenjs` | Node.js; native PPTX, render via LibreOffice and record a slide walkthrough; retain editable deck when requested. |
| Excalidraw | [Excalidraw](https://github.com/excalidraw/excalidraw), npm `@excalidraw/excalidraw` | Browser/React; native scene plus meaningful pan/zoom walkthrough. |
| Motion Canvas | [Motion Canvas](https://github.com/motion-canvas/motion-canvas), npm `@motion-canvas/core`, `@motion-canvas/2d`, `@motion-canvas/vite-plugin`, `@motion-canvas/ffmpeg` | Node.js/Vite and browser renderer; verify actual video export, not just Vite build. |
| Original Manim / ManimGL | [3b1b/manim](https://github.com/3b1b/manim), PyPI `manimgl`, Python import `manimlib` | Isolated Python environment; OpenGL context, FFmpeg, platform libraries; test headless context availability. |
| Manim Community | [ManimCommunity/manim](https://github.com/ManimCommunity/manim), PyPI `manim` | Separate Python environment; Cairo/Pango and video support; use Cairo for initial smoke test. |
| ManimGX | [academa-labs/manimgx](https://github.com/academa-labs/manimgx), PyPI `manimgx` | Separate Python 3.13+ environment; Rust/wgpu engine bundled in wheels; validate Linux CPU Vulkan fallback if no GPU. |

Use official package registries and upstream installation documentation. Keep the three Manim implementations in separate virtual environments: their APIs and dependencies are not interchangeable. Do not install one over another. Pin resolved versions after a successful setup and record the OS/runtime used.

Shared tools: FFmpeg/ffprobe, 7-Zip, a browser suitable for rendering, LibreOffice for PPTX rendering, and openly licensed fonts. Install through official distro/vendor sources. LaTeX may be needed for later scenes, but the first smoke test can use plain text and shapes. GX includes its own typesetting and encoding path. Original project code licenses do not cover every bundled component: GX native distributions include copyleft encoder components; inspect their notices before redistributing tools.

## Cloud acceptance

1. Register the saved environment and record its actual name and ID in the task handoff.
2. In a fresh cloud task, check installed versions and render a short synthetic story with all six providers.
3. For each provider, report install, render, full video decoding and visual review separately; preserve the exact error if unsupported.
4. Deliver one `output.mkv` and one `extras.7z` per provider. Include the native PPTX or Excalidraw file for those tests; the other extras may intentionally be zero bytes.
5. Record reproducible commands and measured runtime/resource limits. Do not claim CPU/GPU or platform support based only on upstream claims.

No paid calls, new credentials, expanded persistent grants or network-security changes are implied by this setup. Stop at any such requirement and identify the exact action needed.
