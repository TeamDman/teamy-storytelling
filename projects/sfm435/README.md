# SFM 4.35 — three Motion Canvas treatments

Three distinct silent review films for Teamy's live commentary:

| Project | Treatment | Duration | Visual logic |
|---|---|---:|---|
| `route` | Keep the route open | 3:44 | Persistent dispatch route; local destination stop versus source-record lifetime |
| `forensic` | The one-FE gap | 3:46 | Rewind from the symptom through a ledger and replay the scope change |
| `atlas` | Inside the release | 3:50 | Continuous descent through authored source, runtime payload and nested execution scopes |

Canonical delivery for each is exactly `output.mkv` and `extras.7z`. Separate MP4
previews are conveniences outside that two-file contract. All videos are
1920×1080, 24 fps, silent H.264 yuv420p. There is no invented narration track or
custom player. Pause cards are editorial cues, not player controls.

## Reproduce in the qualified environment

Use the installed dependency tree qualified in `ENVIRONMENT.md`; do not
install or upgrade providers as a side effect of reproducing this production.
From this production directory, link its `node_modules` to that qualified tree,
then start the local Vite service:

```sh
node -r ./scripts/runtime.cjs node_modules/vite/bin/vite.js
```

In a second terminal with the qualified FFmpeg, Chromium and 7-Zip on PATH:

```sh
node scripts/render.mjs route
node scripts/render.mjs forensic
node scripts/render.mjs atlas
python3 scripts/package.py route
python3 scripts/package.py forensic
python3 scripts/package.py atlas
```

The package script also requires the review-specific handoff documents under
`handoff/`. They are delivered in the archive, but excluded from Git because
historical demonstration commands contain producer-environment paths. Place
those documents back in `handoff/` to reproduce the exact archive.

For an exact-time visual check:

```sh
node scripts/render.mjs route --stills=25,53,115,121,132,212
```

Sources use Motion Canvas scenes, signals, groups, clipping, Code, and the
qualified native FFmpeg exporter. `highlight.ts` connects the installed
TextMate grammar engine to Motion Canvas Code, with local WebAssembly assets.
Experimental Code draw hooks are explicitly enabled only to keep unselected
source readable during selections. No renderer dependencies are modified.

`director.ts` records cue and chapter starts from the final generator timeline.
`scripts/package.py` derives FFmpeg chapter metadata from that record, preserves the
native export's inclusive closing boundary frame, remuxes the canonical MKV, generates a fast-start
MP4 preview, decodes both fully, validates frame count and chapters, and tests the
7-Zip archive. Its `validation.json` describes completed checks for that build. Encoded films include
one closing boundary frame (about 0.042 seconds) beyond the named scene duration;
the final packaged cue and chapter include it.

## Evidence boundary

The producer handoff pins rendered Java and captured runtime payloads to
`8e349578d18511d8d5993b66a3ad3c7c957e5db4`. The file map is **captured MC 1.21.1
runtime payloads including GameTests**, not a release-JAR inventory. It uses the
producer's lexically sorted path indices and 44 columns. Printed-view equality
is not behavioral equivalence. Full category definitions and exact source
excerpts are in the extras.

The known automatic baseline and fixed characterization tests both passed,
with different expected outcomes. The full manual drain-and-second-pulse
walkthrough remains unverified. On-screen diagrams are schematics; no Orbit
captures are included. D01baseline and D02fixed require local preparation; the
archive preserves the historical tested cloud commands with their limitations.

No release approval, public publishing, repository push, or merge is implied.
See `ATTRIBUTION.md` for source and asset attribution.
