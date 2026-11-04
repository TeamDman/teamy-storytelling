# Conference preview: slice 01

This nine-second, 1280×720 presentation study transitions the previously
validated `first` orbit into a picture-in-picture inset. It displays the exact
`EVERY 20 TICKS` program and the `a` → `b` dirt transfer from the bundled
`Move1StackDirectGameTest.java`. The card is a presentation layout, not a
recreation of SFM's manager or editor UI. It does not animate inventories or
players; those remain separate source-grounded slices.

The script verifies the bundled source file and the preserved original orbit by
SHA-256 before creating output. The orbit itself is reconstructed, with the
limitations documented in the parent README. No original render is overwritten.

After restoring the parent project's inputs and `deliverable/output.mkv`:

```sh
source /workspace/storytelling-setup/activate.sh
python3 conference-preview/slice01.py
```

The result is written under the ignored `previews/conference-slice-01/`
directory. The script refuses to replace an existing preview. It uses Pillow,
FFmpeg and DejaVu fonts from the storytelling environment; it does not launch a
browser or Minecraft. The output has no audio.

## Slice 02: manager view

`slice02.py` adds a static manager-screen reconstruction beside the same
moving orbit. It uses the original SFM manager texture and disk icon plus
button geometry and text from the pinned
[`ManagerScreen.java`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/client/screen/ManagerScreen.java)
and disk slot position from
[`ManagerContainerMenu.java`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/common/containermenu/ManagerContainerMenu.java).
The font and button skin are approximations, and the running state and empty
player inventory are illustrative. This is not a captured game screenshot or
a reconstruction of the program editor. Exact historical UI parity is not
claimed.

Place these pinned upstream assets at the following ignored local paths before
running `python3 conference-preview/slice02.py`; the script checks their SHA-256
digests and the first orbit's digest:

- `.inputs/sfm-gui/manager.png`: [upstream asset](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/resources/assets/sfm/textures/gui/container/manager.png), SHA-256 `b6945789f1b663261a0c3bc6f922052a41f827cbd966e5014cadbc188eb7dea0`.
- `.inputs/sfm-gui/disk.png`: [upstream asset](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/resources/assets/sfm/textures/item/disk.png), SHA-256 `049bca9a9be439beca5979e8af504bb3c822eb06dbf390927de9f490ce0514e1`.

The result is written under ignored `previews/conference-slice-02/` and does
not replace earlier outputs. Source assets retain their original rights and
are not committed here.

## Slice 03: manager to V1 editor

`slice03.py` continues the manager preview with an illustrative pointer and
Edit action, then shows a reconstruction of the V1 program editor. At a
427×240 logical viewport, the 400×200 editor area at (13, 10) and footer
positions come from the pinned
[`SFMTextEditScreenV1.java`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/client/screen/text_editor/SFMTextEditScreenV1.java).
The exact `a` → `b` program is extracted from `Move1StackDirectGameTest.java`;
token categories and default colors come from the pinned
[`ProgramSyntaxHighlightingHelper.java`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/client/text_styling/ProgramSyntaxHighlightingHelper.java)
and [`SFMClientTheme.java`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/client/theme/SFMClientTheme.java).
Line numbers and suggestions are off according to the defaults in
[`SFMClientTextEditorConfig.java`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/common/config/SFMClientTextEditorConfig.java);
an actual player's settings may differ.

This is not a game capture. The font, button skin, background, pointer, and
click timing are approximations; the orbit inset is a presentation overlay,
not part of the game editor. The script verifies the prior manager preview,
orbit and test source by SHA-256, and refuses to overwrite its own output.
After restoring those inputs, run `python3 conference-preview/slice03.py` in
the activated storytelling environment. Its silent nine-second outputs are
written to the ignored `previews/conference-slice-03/` directory.

## Slice 04: corrected motion cadence

`slice04.py` combines the orbit-to-manager transition with the V1 editor
slice, keeping the original orbit and the manager layout generated by slice
02. It aligns the decoded video and still-image inputs to a 1/30-second time
base before compositing. The previous previews mixed the orbit's millisecond
time base with the layout's 30 fps clock; the opening repeated frames and
skipped world updates. The transition also uses a smoothstep easing curve.
No interpolated world frames are invented.

For the generated preview, a grayscale difference check on the 60 opening
frames found 20 near-static adjacent pairs in slice 01 and zero in slice 04;
the six-second editor inset had zero near-static pairs among its 179 frame
pairs. This verifies cadence in the files, not playback on every device.
Both outputs decode fully, with 420 frames at 1280×720 and 30 fps. Run
`python3 conference-preview/slice04.py` after generating slice 02 and
restoring the original orbit and source. It checks the input hashes and
preserves existing output under `previews/conference-slice-04/`.

## Slice 05: simpler presentation

`slice05.py` keeps the same source-grounded manager and editor views and
cadence correction, but removes the extra presentation captions around the UI.
Its 14-second output also decoded fully at 1280×720 and 30 fps. The opening
and editor-inset frame-difference checks found zero near-static adjacent pairs
across 59 and 179 pairs respectively. Its inputs and invocation match slice
04; generated files are preserved under `previews/conference-slice-05/`.

## Slice 08: inventory transfer cutaway

`slice08.py` depicts the source test's initial stack of 64 dirt in slot 0 of
barrel `a` and its asserted final state in slot 0 of barrel `b`, alongside the
editor and orbit. The SFM test barrel's
[`TestBarrelBlockEntity`](https://github.com/TeamDman/SuperFactoryManager/blob/e2ba833b2b235835d69475b641e24b22bfd9551a/platform/minecraft/src/main/java/ca/teamdman/sfm/common/blockentity/TestBarrelBlockEntity.java)
inherits the Minecraft barrel block entity. The saved dirt texture supplies
the reconstructed item icon. Input hashes are verified before rendering.

These side-by-side panels are an explanatory cutaway, not a first-person game
capture. The barrel screen's texture, font and item icon are approximations;
the simultaneous screens, flying stack and transfer timing are presentation
devices. The test specifies `EVERY 20 TICKS` and checks the eventual state; it
does not establish the displayed animation or a precise completion time. The
player inventory is illustrative. Actual first-person barrel views and
right-click animation remain future work.

Run `python3 conference-preview/slice08.py` after generating slice 05 and
restoring the orbit, source and dirt texture. Outputs are written under the
ignored `previews/conference-slice-08/` and never overwrite an existing cut.
The ten-second preview decoded fully at 1280×720, 30 fps and 300 frames. Its
world inset had zero near-static adjacent pairs out of 299, and the full and
empty inventory panels were verified to swap between endpoints.

## Slice 11: legacy-skin model

`skin_model.py` uses the supplied 64×32 skin (`libfile_a907459b10048191a799f556824ab6b3`,
SHA-256 `dc6d27c115e71009ced5a2bc41a24e918b45edf5a584e639ec56b832126d2635`)
to construct a classic-proportioned player with mirrored legacy arms and legs.
The saved skin's head-overlay region is fully transparent. The Blender model is
a static reconstruction, composited over the editor rather than placed in the
world. It does not reproduce first-person interaction, lighting, animation, or
claim a Minecraft capture. Side and back UVs have not been checked against an
actual player capture.

Place the exact skin at `.inputs/skin.png`, restore the orbit and generate
slice 05. Then run:

```sh
blender --background --threads 2 --python conference-preview/skin_model.py
python3 conference-preview/slice11.py
```

The model script refuses to overwrite files
under `previews/conference-slice-10/`; the video script preserves existing
output under `previews/conference-slice-11/`. Blender 4.3.2 was used here.
The compositor runs `verify_skin_model.py`: all 352 front-face pixel-center
samples, including both mirrored limbs, matched the skin within one channel
value in this render. This check does not verify the unseen faces or animation.
Both nine-second videos decoded fully at 1280×720 and 30 fps; the moving world
inset had zero near-static pairs out of 269.

## Slice 12: player in the reconstructed world

`world_player.py` imports all 195 faces from the saved `baked-scene.json`
and places the legacy-skin model in that three-dimensional fixture. It stages
the player on the existing command block, then raises and lowers the right arm
toward barrel `a`. Placement, pose, camera and timing are invented for the
shot. The gesture is a right-click *illustration*, not a verified Minecraft
animation; the barrel does not open and no inventory is manipulated here.
Blender's materials and sky differ from the original renderer; the beacon is a
simple static approximation and animated block atlases use their first frame.
This is not a game capture.

The script checks the legacy skin, baked geometry and grass atlas hashes.
`--verify` compares all 36 model-face rectangles, 144 UV corners and 1,632
pixel-center coordinates with an explicit legacy mapping table, including the
mirrored limbs. The separate slice 11 front render compares skin colors; there
is still no independent in-game reference for side/back face orientation.
The same check verifies that the staged hand enters the reconstructed `a`
barrel bounds at the gesture peak and the camera moves on all 179 frame
intervals. These are geometry and cadence checks, not proof of a real click.

After restoring the project assets, the exact skin and the baked world, run:

```sh
blender --background --threads 2 --python conference-preview/world_player.py -- --verify
blender --background --threads 2 --python conference-preview/world_player.py -- --render
python3 conference-preview/encode_world_player.py
```

The render and encoder refuse to replace existing frames or videos in the
ignored `previews/conference-slice-12/` directory. Blender 4.3.2 rendered
180 frames at 768×432 and 30 fps; both six-second videos decoded fully. A
grayscale frame-difference check found zero near-static adjacent pairs among
179; the independently evaluated camera positions also changed at every
frame. The lower resolution is intended for this short preview.

## Slice 13: open barrel and inventory

`world_barrel.py` continues the staged player gesture. It changes barrel `a`'s
north-facing front from the restored closed texture to the restored
`barrel_top_open.png` texture at the gesture peak, following the supplied
open-state block model. `compose_barrel.py` then shows an empty source-barrel
inventory: the saved walkthrough opens this barrel after the transfer. The
choice of timing and the arm animation are illustrative, not a recording of
the game.

The inventory screen remains an approximation. Its frame and slot pixels come
from the restored SFM manager texture; the three barrel rows are assembled
from those slot pixels, and the text uses an approximate font. The original
Minecraft 1.19.2 `generic_54.png` and bitmap font were not present in the
restored project, so actual vanilla-screen pixel parity is not established.
The screen, player inventory contents and camera view should not be treated as
a captured first-person view. The world rendering has the same approximations
described for slice 12.

After restoring the same scene and skin inputs as slice 12, run:

```sh
blender --background --threads 2 --python conference-preview/world_barrel.py -- --verify
blender --background --threads 2 --python conference-preview/world_barrel.py -- --render
python3 conference-preview/compose_barrel.py
```

The source manager texture must be restored at `.inputs/sfm-gui/manager.png`
as described for slice 02. Both scripts refuse to replace existing frames or
videos in ignored `previews/conference-slice-13/`. The open texture switch and
hand position were checked in Blender. Both videos fully decoded with 180
frames at 768×432 and 30 fps, and no near-static adjacent pairs were detected
in the decoded preview. Its reported container duration is 5.999 seconds.

## Slice 14: source and destination views

`barrel_views.py` stages two close viewpoints in the same reconstructed 3D
fixture. `compose_views.py` cuts from the slice 13 third-person gesture to the
empty source barrel, the destination barrel with 64 dirt, and the slice 05
editor. The barrel order and post-transfer contents come from the saved
`Move1StackDirectWalkthroughGamePuppet` and direct test. The viewpoint
positions, camera motion, cuts and screen timing are editorial; these are not
captured first-person views, and no first-person hand is rendered. The screens
and item icon retain the approximations described for slices 08 and 13.

After generating slices 05 and 13 and restoring their inputs, run:

```sh
blender --background --threads 2 --python conference-preview/barrel_views.py -- --verify
blender --background --threads 2 --python conference-preview/barrel_views.py -- --render
python3 conference-preview/compose_views.py
```

The scripts preserve existing files under ignored
`previews/conference-slice-14/`. Blender verification checks both open-state
selections and all 118 within-view camera steps, with one deliberate cut. Both
nine-second videos decoded fully with 270 frames at 768×432 and 30 fps; no
adjacent decoded frames were byte-identical. Image-wide differences are small
in the intentionally slow close views and the mostly static editor, especially
when the inventory overlays cover the moving scene; the camera-step check is
reported separately from those image measurements.

## Slice 16: provisional typography scaling proof

`compose_crisp_native.py` tests 720p composition without reducing the editor
image: the editor is read directly at 1280×720, and inventory pixels are
reconstructed at their native 176×166 size and enlarged exactly 3× with
nearest-neighbor sampling. The world frames are enlarged separately. The
preview uses H.264 4:4:4 to preserve colored text edges; some players may not
support this profile. This experiment **still uses the provisional DejaVu
font**, not the Minecraft font, and is not a font-fidelity validation.

After generating the slice 13 and 14 frame sequences, the slice 05 editor
image, and their inputs, run:

```sh
python3 conference-preview/compose_crisp_native.py
python3 conference-preview/compare_provisional_type.py
```

Outputs are written under ignored `previews/conference-slice-16/` and are not
overwritten. In the recorded editor crop, the earlier 432p preview was enlarged
to 720p for comparison. Its mean absolute channel error versus the unencoded
editor image was 10.192, compared with 0.386 for this proof; 7,952 pixels
versus zero had a maximum channel error above 20. Opaque inventory pixels in
the proof had mean channel error 0.054 against the pre-encode 3× overlay.
Both videos decoded fully at 1280×720, 30 fps and 270 frames. These checks
measure scaling and encoding, not correct Minecraft glyph design or metrics.

## Slice 17: two-character camera study

`multichar_scene.py` adds a neutral, untextured and explicitly labeled second
figure to the slice 13 fixture. It has no supplied skin or identity; its
position and the first player's gesture are staged. `compose_multichar.py`
cuts from that two-character shot to the two reconstructed barrel viewpoints
from slice 14. The viewpoints are editorial camera positions, not a game
recording, and do not include a first-person hand. No inventory UI or font is
shown in this cut.

After generating the slice 14 viewpoint frames and restoring the inputs for
slice 13, run:

```sh
blender --background --threads 2 --python conference-preview/multichar_scene.py -- --verify
blender --background --threads 2 --python conference-preview/multichar_scene.py -- --render
python3 conference-preview/compose_multichar.py
```

Outputs are preserved under ignored `previews/conference-slice-17/` and the
scripts refuse to replace them. The check confirms separate staged figures
and places the placeholder on the restored ground. Both seven-second outputs
decoded fully at 1280×720 and 30 fps, with 210 frames and no byte-identical
adjacent decoded frames. The cuts between viewpoints are intentional; this
check does not establish a real Minecraft animation or user-perceived
smoothness.

## Slice 18: integrated story cut

`compose_story.py` joins the existing orbit/manager shot (0–8 seconds), editor
(8–10), illustrated transfer (10–16), two-character staging (16–19), and
source/destination barrel viewpoints (19–23). The changes of view are editorial
cuts, not continuous first-person game footage. It checks the four input video
hashes and refuses to overwrite `previews/conference-slice-18/`.

The earlier qualifications still apply: the inventory screens and font are
provisional, the second figure is a labeled untextured placeholder, and the
player's gesture and viewpoints are staged. The saved test establishes the
program and inventory endpoints, not the illustrated transfer motion. The
23-second preview decoded fully at 1280×720 and 30 fps with 690 frames and no
byte-identical adjacent decoded frames. Representative frames from all five
sections were compared with their source shots. H.264 4:4:4 is used to retain
the sharper editor pixels; some players may not support this profile.

After generating slices 05, 08, 16 and 17 and restoring their inputs, run
`python3 conference-preview/compose_story.py` in the storytelling environment.

## Interaction evidence and animation limits

The saved SFM puppet's `SFMGamePuppetMinecraftRuntime.useBlock` calls
`gameMode.useItemOn` directly and contains no explicit player swing call. Its
capture sequence therefore does not establish a hand-swing animation or its
timing. The saved runtime source has SHA-256
`0cd355e0c6473efdff477b002fdfd7d5e7437506225f0c2b2fcc0e6a97a80c0d`.

The [Forge 1.19.2 client patch](https://github.com/MinecraftForge/MinecraftForge/blob/66e4ae51423e2dde5edd5ffea4a13dfab4621192/patches/minecraft/net/minecraft/client/Minecraft.java.patch)
(Git blob `d1459ef7b6d4a28ced95887f528f9f3f35969d12`) shows the normal
block-use path conditionally swinging after the interaction result, with an
additional Forge input-event swing condition. That supports a conditional
normal-player swing as a staging choice; it does not prove that the puppet
capture swung. A reported six-tick baseline and a 1.19.3 first-person formula
are research leads, not verified 1.19.2 timing or geometry. In particular, the
puppet's separate settle delay must not be treated as a swing duration. The
arm motion in slices 12–18 remains illustrative.

## Motion Canvas vertical slice (November 2026)

The new `production/story-project.ts` is a separate eight-second Motion Canvas
project. It renders the existing Three.js world directly through `Three`, adds
an articulated legacy-skin player in Three.js, and controls camera, gesture and
GUI visibility from one Motion Canvas time signal. This is a vertical slice,
not a port of the complete conference cut. The original orbit and every prior
preview are preserved. Blender and the previous FFmpeg composites are not inputs
for this slice. Motion Canvas's FFmpeg exporter encodes the final frames.

The opening player placement, arm swing, camera and screen timing are staged,
not captured gameplay; the arm motion is illustrative, and the barrel does not
change its world texture. The screen transition illustrates the source empty
and destination full endpoints, but does not itself depict a transfer. The dirt
item icon is still the earlier hand-built approximation. Side/back skin UVs and
animation have not been independently checked against a game capture. The world
retains the limitations in the parent README. There is no first-person hand.

`production/prepare_story_assets.py` verifies the official 1.19.2 client against
the pinned version metadata in `ground-truth/evidence/minecraft-1.19.2.json`
(21,644,740 bytes, SHA-1 `055b30d860ead928cba3849ba920c88b6950b654`)
before extracting its ASCII bitmap font, font mapping and vanilla
`generic_54.png` in memory. It composes the three-row barrel at native GUI
resolution, then uses nearest-neighbour 3x scaling at 1280×720. Only the ASCII
labels used here are supported. The source assets and generated layers remain
local and ignored. `font-comparison.png` compares the previous DejaVu
approximation with the real bitmap at the final output size. The player skin
is the separately supplied 64×32 file identified in slice 11 above.

To reproduce, restore and verify the input bundles as in the parent README, put
the verified skin at `.inputs/skin.png`, download the official pinned client
from the `downloads.client.url` in the verified version metadata to
`.inputs/minecraft-1.19.2-client.jar`, then run:

```sh
npm ci --ignore-scripts --no-audit --no-fund
python3 bake.py
python3 production/prepare_story_assets.py
STORY_ACTIVATE=/workspace/storytelling-setup/activate.sh bash render-story.sh
```

The asset script refuses to overwrite GUI layers and the renderer refuses to
replace its video. A configured Chromium sandbox and the other requirements in
the parent README are still required. On the reviewed cloud graphics path the
export completed at 1280×720, 30 fps, with 241 frames including Motion Canvas's
endpoint (8.033 seconds), and decoded fully. The initial version was visually
reviewed, then the camera corrected because it hid the player. The revised
preview and output-resolution font comparison are separately retained in
Library; generated media is not committed. The rendered preview is H.264
`yuv420p`, so chroma subsampling and compression can still affect coloured
edges even though GUI pixels were scaled without smoothing.

## Motion Canvas conference slice: manager, editor and transfer

`production/conference-project.ts` extends the Motion Canvas timeline to 15
seconds. After the staged world and player gesture, it shows a manager screen,
the V1 editor, and a side-by-side explanatory cutaway of barrels `a` and `b`.
A single visible 64-item stack moves from `a`'s first slot to `b`'s first slot.
The verified direct test specifies the program and the initial and eventual
slot contents; the camera, gesture, screen transitions, concurrent barrel
views, flight path, 1.5-second movement, manager running state, and empty
player inventory are illustrative. They are not recorded gameplay or evidence
of the actual completion time. The V1 layout, button positions and syntax
colours follow the pinned sources linked in slices 02 and 03; widget borders
and screen state remain approximations.

All screen text uses the verified Minecraft ASCII bitmap atlas, drawn at a
logical pixel size and enlarged with nearest-neighbour sampling. The SFM
manager background and disk icon use the pinned source assets documented in
slice 02. The official 1.19.2 dirt item model inherits `block/dirt`, which uses
`block/dirt.png` on all faces: there is no separate flat dirt item texture.
The item image uses that exact texture, cube geometry and the inherited GUI
rotation `[30,225,0]` and scale `0.625`; its software rasterization, face
lighting and placement are approximations, not a pixel-perfect vanilla item
renderer. Text colours may be affected by the H.264 4:2:0 encoding.

Restore the parent project's verified bundles, the supplied skin and pinned
client as described above. Restore the two hash-pinned SFM assets listed in
slice 02. Then run:

```sh
npm ci --ignore-scripts --no-audit --no-fund
python3 bake.py
python3 production/prepare_conference_assets.py
STORY_ACTIVATE=/workspace/storytelling-setup/activate.sh bash render-conference.sh
```

The asset generator checks the client, skin, SFM assets and direct-test source
before generating local ignored layers. It refuses to overwrite them; the
renderer also refuses to replace its output. The reviewed cloud render fully
decoded at 1280×720, 30 fps and 451 frames (15.033 seconds including the Motion
Canvas endpoint). The first render exposed a one-frame final flash; the revised
render holds the destination screen through the endpoint. The previous Motion
Canvas preview's SHA-256 remained
`8ec108f93bb3bbc5797d5477fef79601c71c789abc0de7d96a7cb90ea1387d30`.
The revised conference preview is retained separately in Library; generated
assets and media are not committed. `npm test` includes an independent timeline
boundary and continuity check; visual inspection of the decoded start, midpoint,
destination and final frames confirmed the staged transfer is visible.

## Motion Canvas conference composite: orbit and concurrent views

`production/composite-project.ts` is a separate 16-second Motion Canvas slice.
The existing Three.js orbit starts full frame and smoothly shrinks to an inset;
it continues to update on the same timeline while the manager, then the V1
editor, appears alongside cropped three-row views of barrels `a` and `b`.
The stack of 64 starts in `a`, follows a staged path, and finishes in `b`.
The source test supports the endpoints and program, not the path, timing,
simultaneous open screens, or the illustrative manager running state. The
player gesture and world remain reconstructions with the limitations above.

The only added presentation labels are `a` and `b`, needed to distinguish the
source and destination; player-inventory rows are intentionally cropped from
the two barrel views. The manager and editor use the actual bitmap font and
source-derived layouts, with approximate button skins. The editor's 296×240
logical layout follows the pinned V1 `editorLayout` calculation; its text and
controls are enlarged exactly 2×. The world inset, panel arrangement and
animation are presentation devices, not game captures. The dirt icon retains
the exact texture and approximate shading described in the preceding section.

After restoring the inputs and generating the earlier conference assets:

```sh
python3 production/prepare_composite_assets.py
STORY_ACTIVATE=/workspace/storytelling-setup/activate.sh bash render-composite.sh
```

The generator checks the prior layers and client hashes, and refuses to replace
existing output. Rendering similarly refuses to replace its preview. The
reviewed render decoded fully at 1280×720, 30 fps, and 481 frames (16.033 seconds
including the Motion Canvas endpoint). Visual inspection covered the manager,
editor, transfer and final states. A two-second decoded inset sample (60 frames)
had no identical adjacent pairs; this checks the sampled cadence, not every
playback device. The previous conference preview retained SHA-256
`6bb88346e6286cb707680ecf69ed901afc1e4638412207bdc70fd30aaa72e929`.
The new preview is stored separately in Library; acquired assets and generated
media remain untracked.
