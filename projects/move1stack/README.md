# move_1_stack_direct reconstruction

A source-grounded full-scene Minecraft 1.19.2 / SFM orbit rendered by Motion Canvas 3.17.2 and Three.js 0.149.0. This checkpoint contains the renderer, tests, exact package lock, reproducible commands and input identities. It deliberately excludes acquired textures/models, decompilation, original screenshots, generated derivatives, videos, archives and private runtime diagnostics.

## Restore the inputs

`provenance.json` pins all three original Library records with exact Library/file IDs, versions, archive sizes and SHA-256 hashes. The current reconciled scene is **version 1**, not version 0. The original eight PNGs are in the reference bundle. The renderer handoff is retained as provenance; the committed source supersedes its older source and does not require restoring it over this checkout.

Use the **current Library skill's supported materialization workflow** as the consuming executor. For these resolved IDs, use the pinned `library_file_id`, `file_id` and filename from `provenance.json`; choose a local destination such as this project's ignored `.inputs/`. Do not invent download URLs, copy credentials, bypass TLS or networking, or assume a path returned in another executor is locally readable. Library access is required: the IDs themselves confer no permission.

After materializing the two ZIPs locally:

```sh
cd projects/move1stack
python3 prepare-inputs.py \
  --scene .inputs/move1stack-scene-bundle.zip \
  --references .inputs/sfm-move1stack-reference-1cfc20e8754c41e486856074bcd8d0c1.bundle.zip
python3 prepare-inputs.py --verify-existing
```

The script checks the pinned archive sizes/hashes, rejects unsafe archive entries, verifies the reconciled manifest hash, all 75 original asset hashes and reference checksums, then installs `ground-truth/` and `reference-evidence/`. Existing verified inputs are reused without overwriting them; differing inputs fail. View all eight PNGs before making visual changes.

## Reproduce both profiles

Requirements: Node/npm, Python 3 with Pillow and NumPy, FFmpeg/ffprobe with libx264, 7-Zip, Xvfb, and Debian Chromium with its normal sandbox configured. These are supplied by the qualified storytelling toolchain; this project does not modify system installation or security settings. If the toolchain needs activation, set `STORY_ACTIVATE` to its activation script before invoking `render.sh`.

```sh
npm ci --ignore-scripts --no-audit --no-fund
python3 bake.py
npm test
python3 -m unittest discover -s . -p 'test_prepare_inputs.py' -v

# First profile: 24-second, 1280x720, 30 fps, silent complete orbit.
MOVE1_PROFILE=first bash render.sh
python3 validate-video.py
python3 package-extras.py --profile first

# Separate source-supported filtering correction.
MOVE1_PROFILE=source-cutout bash render.sh
python3 validate-video.py candidates/filtering/deliverable
python3 package-extras.py --profile source-cutout
```

The first profile writes `deliverable/output.mkv` and `deliverable/extras.7z`. The correction writes the same contract under `candidates/filtering/deliverable/`. Packaging retains the MP4 preview inside extras and separately under ignored `previews/<profile>/preview.mp4`, leaving exactly the two contract files in the delivery directory. Packaging refuses to overwrite an existing extras archive. `render.sh` refuses to replace an existing video unless `MOVE1_OVERWRITE=1` is explicitly supplied. Stop an existing Vite server on port 9002 first.

The renderer uses loopback Vite and Xvfb :91. `runtime-settings.cjs` keeps editor settings in ignored `.settings/`. Chromium retains `chromiumSandbox:true`, excludes Playwright's unsafe SwiftShader default, and uses the qualified launch-scoped `--ignore-gpu-blocklist` compatibility flag. No `--no-sandbox`, TLS bypass or network-policy change is used. Some managed execution sandboxes require reviewed browser execution because the outer namespace presents the SUID helper owner differently; do not repair system permissions or disable Chromium sandboxing to work around that error.

Pure timeline/profile tests run without the acquired assets. Four geometry tests explicitly skip until inputs are restored and `bake.py` has run. `prepare-inputs.py` and its archive-safety tests use only Python's standard library. Full render/comparison checks require the external inputs and qualified graphics path.

## Scene and fidelity

The scene includes all 20 declared fixture/support blocks, north-facing solid barrels, animated manager, andesite floor, structure/command/button arrangement, layered beacon and lime glass, buried iron base, dirt patch, surrounding grass, outline and clear blue sky. Motion Canvas supplies every camera/animation timestamp. No screenshot billboards, cables, signs, chests or lectern are added.

The exact optical positions and yaw/pitch-derived forward vectors come from the reference manifest, translated by world origin (0,-60,0). No extra eye height or manager-centered lookAt is added. The 87-pixel caption is cropped before comparing the 1280x720 viewports. FOV 70 remains provisional because capture-time FOV was not recorded.

Barrel blockstate X+90 is baked as Three X-90 about the cube center. Beacon model boxes and face UVs come from the acquired JSON. The shell uses alpha discard .1; the rotating beam core writes depth, while the stationary .125-opacity halo does not. The smooth orbit retains a continuous beam. Figure 3's matched still preserves the observed missing rising beam; its cause is unknown.

The `source-cutout` profile disables mipmaps only for the beacon's three cutout textures, as distinguished by the supplied Minecraft CUTOUT/BLOCK_SHEET render state. Across all eight matched views, it changes 16 pixels in figure 5 and 76 in figure 7, reduces reference error there and leaves six views identical. This is a small source-conformance correction, not a substantial visible fidelity upgrade. See `validation-summary.json` and `candidates/filtering/refinement-summary.json`.

Largest remaining differences: the historical loaded-chunk horizon, terrain random pattern/sampling, vanilla AO/contact shading, lightmap/gamma/fog, unknown animation phase, beacon section/color/blending appearance and outline rasterization. The first profile's grass tint is a disclosed reference calibration, not a recovered capture setting; its seeded grass rotations are approximate. The full dirty capture tree, options and resource packs were not reconstructed. Optional cloud/moon helpers are not qualified as Minecraft fancy-cloud equivalence; no cloud/sun/moon is visible in the eight matched reference views. Do not invent settings or tune independently per camera to hide these limits.

Both profiles were rendered and visually reviewed. The final videos fully decoded with 720 frames and 24.000-second duration. The Motion Canvas export includes an endpoint frame; final encoding keeps decoded frames 0..719 at H.264 CRF18/yuv420p to avoid B-frame packet truncation. Package/runtime differences can change encoded bytes, atlas sampling or rasterization; this checkpoint enables scene reconstruction, not a promise of byte-identical encodes or archives. The preserved original artifact hashes are recorded in `validation-summary.json`.

## Rights and publication boundary

Original authored renderer code follows this repository's MPL-2.0 license. `production/Three.ts` and `smoke/Three.ts` adapt the official Motion Canvas examples at `8ffefed144368d33de4b0e451894c718eb95d574`; the MIT notice is retained beside each copy. Minecraft and SFM assets keep their original rights. They are restored locally from authorized Library inputs, not redistributed by this source checkpoint. Generated grass atlases/baked geometry and reference screenshots are also excluded from Git. Review rights before publishing any private extras archive or media separately.
