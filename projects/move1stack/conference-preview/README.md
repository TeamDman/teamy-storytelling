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
