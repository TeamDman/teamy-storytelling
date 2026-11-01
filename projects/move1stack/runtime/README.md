# Renderer modules

`world.mjs` loads the reconciled scene through the model baker and `scene.mjs` adapter. `timeline.mjs` evaluates deterministic animation timestamps; `profiles.mjs` isolates the source-supported cutout correction. The scene has been rendered and validated; see the production README and validation summary for scope and limits.

The adapter consumes `baked-scene.json`, generated from external input assets by `bake.py`. It does not infer missing geometry or capture-time settings. Materials explicitly specify texture, blending, alpha test and depth-write state. Animation is evaluated from the supplied timeline time, never wall time.
