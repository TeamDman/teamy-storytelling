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
