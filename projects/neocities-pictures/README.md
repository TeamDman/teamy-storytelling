# Neocities from Scratch: picture placement

An original, synthetic Moon Snail Post Office demonstrates a specific intent: put the snail illustration beside its note when there is room, stack them when there is not, and keep a stamp attached to the postcard. The `.postcard` Grid places the image and note; `.stamp` is absolutely positioned relative to the postcard. The gallery uses a separate Grid. There is no account, real address, or third-party site content in the example.

## Try the page

From `example/`, serve the files with `python3 -m http.server 8765 --bind 127.0.0.1`, and open `http://127.0.0.1:8765/` in a browser. In the `.stamp` rule in `style.css`, change `right: 12px` to `right: 100px`; save and refresh. The stamp image moves left while the postcard, snail, and note stay put. Try `right: 40px`, then narrow the browser. The stamp is attached to the postcard, and absolute positioning can overlap its contents. For a static host, upload `index.html`, `style.css`, `snail.svg`, `garden.svg`, and `stamp.svg` together, preserving their names and relative locations.

## Rebuild the film

This environment's installed dependencies are Chromium, FFmpeg, Node with Playwright, Python 3, Noto Serif and DejaVu fonts, and eSpeak NG 1.52.0. Set `NODE_PATH` to the directory containing the installed `playwright` package. Set `ESPEAK_BIN` if `espeak-ng` is not on `PATH`; if using an extracted Debian package, also set its library and data search paths. The voice here was obtained from the signed Debian repository as `espeak-ng`, `espeak-ng-data`, `libespeak-ng1`, `libpcaudio0` and `libsonic0`, extracted to a scratch directory. For an extracted amd64 tree, point `ESPEAK_BIN` at its `usr/bin/espeak-ng`, `ESPEAK_LIB` at `usr/lib/x86_64-linux-gnu/libespeak-ng.so.1`, and both `ESPEAK_DATA_PATH` and `LD_LIBRARY_PATH` at its `usr/lib/x86_64-linux-gnu`. The event worker also tests this library path as a fallback when `ESPEAK_LIB` is absent. No network or paid voice service is needed after these tools are available.

```sh
# Run in this production directory; output/ is ignored by Git.
export OUTPUT_DIR="$PWD/output"
export NODE_PATH="${STORY_ROOT}/node/node_modules"  # installed environment
node film/capture.cjs
python3 film/audio.py
# Optional short 720p review segment (absolute seconds):
CLIP_START=101 CLIP_END=127 CLIP_LABEL=grid node film/render.cjs clip
node film/render.cjs film
ffmpeg -v error -i "$OUTPUT_DIR/film.mp4" -f null -
```

`capture.cjs` serves a temporary copy of the example on loopback, captures actual Chromium output at several viewport sizes, edits that copy's CSS and refreshes, and asserts wide/narrow layout, stamp movement at both widths, the 40px exercise, gap, and alt-text behavior. The timestamp-addressed canvas animation is rendered by Chromium and encoded by FFmpeg at 15 fps, 1920×1080, H.264/yuv420p with AAC. It uses a 1280×720 drawing surface scaled to delivery resolution. `audio.py` produces local synthetic speech, `timeline.json`, and SRT. A fresh eSpeak worker per utterance supplies word events; its synthesized PCM must match the speech WAV before cue times are accepted. Caption starts follow word events with an 80ms lead; rare missing word events are interpolated. Only trailing silence is trimmed; `film/captions.srt` is the reviewed timing for the delivered voice version. Captures and generated media are intentionally untracked. Browser views in the film are captures of the example; editor, source/Inspector, and box diagrams are explicitly schematic. No Neocities publishing takes place in this workflow.

Motion Canvas was installed, but its sample Vite export in this cloud instance failed while creating its settings directory under an unavailable home directory. The film therefore uses the installed Chromium canvas/FFmpeg renderer, not Motion Canvas. For further exploration, an educational VS Code/Live Server setup can provide auto-refresh, and Excalidraw can help sketch layout relationships; neither was used to make this film.

## Sources and asset notes

- Neocities describes its in-browser editor, uploading, and static hosting at [neocities.org](https://neocities.org/); its [official CLI guide](https://neocities.org/cli) shows `index.html`, CSS and image uploads. Its [official blog](https://blog.neocities.org/blog/2013/07/10/neocities-can-now-handle-two-million-web-sites) gives the `yourname.neocities.org` address pattern. No account was created or page published.
- The snail, garden, and decorative stamp SVG illustrations, page design, animation, and script are original to this production. The repository's MPL-2.0 applies to original source contributions; no video binary or font file is included in Git.
- Noto Serif is distributed under SIL OFL 1.1 (Google, [Noto](https://github.com/notofonts/noto-fonts)); DejaVu Sans and Sans Mono are distributed under the Bitstream Vera permission license with DejaVu changes in the public domain ([DejaVu fonts](https://dejavu-fonts.github.io/)). Fonts are local installed rendering dependencies and are not bundled here.
- eSpeak NG is a local synthetic voice, not an impersonation; its Debian packages and data retain their own licenses. Film speech and editable text are supplied in `film/script.json`; captions are available separately.
