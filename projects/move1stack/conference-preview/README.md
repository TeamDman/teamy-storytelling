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
