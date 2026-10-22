# Attribution and method

Original production source: MPL-2.0, under the repository license.

The official Motion Canvas examples at revision
`8ffefed144368d33de4b0e451894c718eb95d574` were reviewed for signal-driven
diagrams, code selection, progressive edits, and state transitions. Their code
is MIT, copyright 2022 motion-canvas. This production independently implements
those techniques with the qualified Motion Canvas 3.17.2 runtime. No upstream
audio, images, artwork, or substantial source blocks are included.

Reference scenes: `examples/motion-canvas/src/scenes/signalsCode.tsx` and
`examples/asset-code/src/scenes/state-machine.tsx`; grammar integration reference:
`examples/asset-code/src/nodes/Code.ts`.

Java, TOML and JSON highlighting uses the installed @wooorm/starry-night 1.7.0
TextMate grammar engine, vscode-textmate and vscode-oniguruma, feeding Motion
Canvas Code nodes. It is not manually assigned token coloring. Package licenses
and grammar notices remain in the installed dependencies; dependencies are not
redistributed in the extras archive.

Fonts: installed DejaVu Sans and DejaVu Sans Mono, rendered into the video;
font binaries are not redistributed. All diagrams are original schematics,
not Minecraft gameplay captures. Silent visuals are intended for Teamy's live
or recorded commentary; no generated narration is claimed.

Producer-supplied rendered Java excerpts are attributed to
TeamDman/SuperFactoryManager at commit
`8e349578d18511d8d5993b66a3ad3c7c957e5db4`. Corresponding authored Liquid
sources and exact omission boundaries are linked in `source-excerpts.md` in
extras. Editorial ellipsis comments in the animation are labeled omissions;
they are not represented as original Java lines.
