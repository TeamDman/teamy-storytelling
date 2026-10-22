# Environment setup

Target: a separate saved Codex cloud environment named `storytelling-env`, attached to this repository. Do not modify or clone a producer repository merely to make a video.

Include [TeamDman/teamy-docs](https://github.com/TeamDman/teamy-docs) as a second checkout through the supported multi-repository setup. It holds shared provider/reference documentation; this repository holds environment-specific usage and production materials. Read the shared documentation in place instead of copying it. Verify both checkouts are readable in a fresh cloud task. Provider documentation does not authorize paid calls, credentials or expanded permissions, and setup does not require changing teamy-docs.

## Validation status

The saved environment has completed six-provider synthetic rendering in a fresh cloud task, with Library delivery verified. This is evidence for those smoke scenes and the tested saved version, not arbitrary scene compatibility or proof of a later environment refresh. Re-run a small acceptance check after changing tool installations. Reproducible installation and startup instructions belong to the saved environment; preserve them when refreshing documentation checkouts.

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

## Motion Canvas reference checkout

The official [motion-canvas/examples](https://github.com/motion-canvas/examples) repository is source reference material, not instructions or an additional installed renderer. `reference-lock.json` pins revision `8ffefed144368d33de4b0e451894c718eb95d574`, its MIT license digest and attribution (copyright 2022 motion-canvas). Preserve that notice when copying substantial code. The [shared example guide](https://github.com/TeamDman/teamy-docs/blob/main/src/making-videos.md#motion-canvas-example-scenes) points to code/visual synchronization, signals, camera diagrams and state-machine scenes.

After the existing runtime installer has sourced its activation script, append this command to the saved environment setup (replace the synthetic repository path with the environment's storytelling checkout):

```sh
python3 /path/to/teamy-storytelling/scripts/setup-references.py \
  --root "$STORY_ROOT/references"
```

The checkout is then at `$STORY_ROOT/references/motion-canvas-examples`. The script uses Python's standard library and Git, fetches the exact locked commit into a detached checkout, verifies origin/revision/cleanliness/license, and retains the upstream LICENSE and README. It does not install npm dependencies, run example code, initialize submodules, or change the qualified renderer. Existing matching checkouts are reused without network access. A dirty, unrelated or differently pinned checkout is left unchanged and reported; review and move it aside explicitly before an intended reference update.

Add the following offline check to startup/acceptance after activation:

```sh
python3 /path/to/teamy-storytelling/scripts/setup-references.py \
  --root "$STORY_ROOT/references" --check-only
```

Outside the saved runtime, omit `--root` to use `$STORY_ROOT/references` when `STORY_ROOT` is set, otherwise the repository's ignored `.references/` directory. Verify a fresh setup plus a second offline check after changing the lock. Regression checks for clean reuse, local-edit preservation, wrong origin/revision, failed fetch and license mismatch run with `python3 -m unittest discover -s tests -v`.

The upstream package uses Motion Canvas core/2d/ui 3.15.0, Vite plugin 3.14.1 and Vite `^4.3.5`; this is older than the qualified 3.17.2 renderer. Treat scenes as techniques to adapt, not guaranteed drop-in projects. Named timeline cues, dependencies and media provenance need review before running examples. No upstream example render is claimed by source-checkout verification.

Saving this repository change does not itself update the hosted environment's setup/startup fields. Apply both commands there only after the feature revision is available to that environment; preserve its existing installation and startup commands. A fresh cloud task must verify the pinned checkout before claiming the saved environment was refreshed.

## Cloud acceptance

1. Register the saved environment and record its actual name and ID in the task handoff.
2. In a fresh cloud task, verify the pinned reference checkout with `--check-only`, then check installed versions and render a short synthetic story with all six providers.
3. For each provider, report install, render, full video decoding and visual review separately; preserve the exact error if unsupported.
4. Deliver one `output.mkv` and one `extras.7z` per provider. Include the native PPTX or Excalidraw file for those tests; the other extras may intentionally be zero bytes.
5. Record reproducible commands and measured runtime/resource limits. Do not claim CPU/GPU or platform support based only on upstream claims.

No paid calls, new credentials, expanded persistent grants or network-security changes are implied by this setup. Stop at any such requirement and identify the exact action needed.

## Planned providers

Remotion, Psychopomp and a p5.js/p5.brush browser-frame pipeline inspired by PDoomVideo are candidates, not installed or tested additions. Read the shared [provider survey](https://github.com/TeamDman/teamy-docs/blob/main/src/making-videos.md#additional-storytelling-candidates) for dated source evidence and licensing boundaries.

- **Remotion:** React/TypeScript compositions with Node.js and browser rendering. Review its special commercial license eligibility before adoption; qualify browser dependencies and memory/concurrency using a synthetic scene.
- **Psychopomp:** Rust scene plans rendered by wgpu/FFmpeg. Upstream's early macOS/Metal evidence does not establish Linux cloud support. Qualify GPU backend and fonts separately; optional external narration services remain outside setup authorization.
- **PDoomVideo-inspired browser frames:** timestamp-addressable p5.js/p5.brush scenes, contact sheets, resumable frame batches and FFmpeg encoding. The reviewed upstream project has fixed music/duration and Windows Chrome/D3D11 assumptions. Implement a small independent synthetic scene before adopting the strategy; review dependency and asset rights separately from the package's ISC declaration. No upstream music or artwork is approved for reuse by this listing.

Each candidate must produce a meaningful video, pass full decoding and visual review, and deliver `output.mkv` plus instruction-selected `extras.7z`. An editable page, deck or canvas alone is not a video result. Use Library for file delivery; private-network hosting is not required for this workflow. No paid services, credentials, new security settings or upstream code execution were performed by this documentation update.
