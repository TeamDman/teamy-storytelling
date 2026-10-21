# Make a story

The producer investigates the domain and supplies a portable brief: audience, objective, verified claims and numbers, screenshots/assets, provenance, verification status, and relevant tested demonstration commands. The storytelling worker consumes that material without cloning the producer repository. Distinguish measured evidence from schematic or generated illustrations. Never silently promote source-derived claims to runtime-tested facts.

Choose the provider that suits the presentation, or make alternatives for comparison. Preserve the factual constraints while choosing pacing, layout, transitions and narration creatively. Use native slides, canvases and webpages where useful; each still needs a meaningful video walkthrough. A static artifact alone is not video delivery.

## First smoke story

Use an explicitly synthetic example: three shapes start scattered, move into a row, then form a triangle. Show a short opening title, the transformation, and a closing view. Keep the story short and readable without audio. Test the actual provider's rendering; do not label a substitute renderer as that provider.

## Delivery

Each requested result contains exactly two top-level files:

- `output.mkv`: a playable video with a defined default presentation. Additional tracks or subtitles are optional.
- `extras.7z`: only the requested accompanying material. A zero-byte file means intentionally no extras; it is a sentinel, not a valid archive to extract. If content is requested, make a real tested 7z archive.

For the first PPTX and Excalidraw smoke demonstrations, include the editable native artifact. Other smoke tests can have empty extras even when generation used source files. Sources, manifests, screenshots and provenance are not mandatory extras unless requested.

MKV is a container, not a guarantee that every input can be repackaged losslessly. Prefer compatible stream-copy, then validate complete decoding, default tracks, timestamps and audio priming. If required, use a disclosed codec fallback. A prior local AAC test retained extra priming samples on remux, so successful muxing alone is insufficient. A practical baseline is H.264 8-bit yuv420p with compatible audio; determine exact supported settings in the cloud smoke tests.

For nonempty extras, use safe relative paths, reject traversal, absolute paths and links, and check archive integrity. Keep all accompanying files inside the archive. Avoid bundling dependencies or unrelated assets. Review public-source attribution before committing production materials.
