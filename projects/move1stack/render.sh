#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_root"
profile="${MOVE1_PROFILE:-first}"
if [[ "$profile" != first && "$profile" != source-cutout ]]; then echo "Unknown render profile" >&2; exit 2; fi
export MOVE1_PROFILE="$profile"
delivery_check=deliverable/output.mkv
if [[ "$profile" == source-cutout ]]; then delivery_check=candidates/filtering/deliverable/output.mkv; fi
if [[ -e "$delivery_check" && "${MOVE1_OVERWRITE:-0}" != 1 ]]; then
 echo "Preserving existing video; use MOVE1_OVERWRITE=1 to explicitly rerender this profile." >&2
 exit 2
fi
# This managed environment's installed toolchain; no security settings changed.
if [[ -n "${STORY_ACTIVATE:-}" ]]; then source "$STORY_ACTIVATE"; fi
export DISPLAY="${DISPLAY:-:91}"
export LIBGL_ALWAYS_SOFTWARE=true
export GALLIUM_DRIVER=llvmpipe
mkdir -p evidence
if curl -fsS http://127.0.0.1:9002/still.html >/dev/null 2>&1; then
 echo "Port 9002 already serves a renderer; stop it before starting this script." >&2
 exit 2
fi
node --test runtime/*.test.mjs
xvfb_pid=''
if [[ ! -S /tmp/.X11-unix/X91 ]]; then
 Xvfb :91 -screen 0 1280x900x24 -nolisten tcp > evidence/xvfb.log 2>&1 & xvfb_pid=$!
fi
(cd production && NODE_OPTIONS="--require=$project_root/runtime-settings.cjs" ../node_modules/.bin/vite --host 127.0.0.1 > ../evidence/vite.log 2>&1) & vite_pid=$!
trap 'kill "$vite_pid" 2>/dev/null || true; if [[ -n "$xvfb_pid" ]]; then kill "$xvfb_pid" 2>/dev/null || true; fi' EXIT
for attempt in {1..100}; do if curl -fsS http://127.0.0.1:9002/still.html >/dev/null; then break; fi; sleep .2; done
if [[ "$profile" == first ]]; then
 node capture-stills.cjs
 python3 compare.py
else
 node capture-candidate.cjs
 python3 candidates/filtering/evaluate.py
fi
node validate-render.cjs
node render-orbit.cjs
delivery_dir=deliverable
rendered_media=media/move1stack-orbit.mp4
if [[ "$profile" == source-cutout ]]; then
 delivery_dir=candidates/filtering/deliverable
 rendered_media=media/move1stack-source-cutout-orbit.mp4
fi
mkdir -p "$delivery_dir"
ffmpeg -v error -i "$rendered_media" -map 0:v:0 -vf 'setpts=N/(30*TB)' -frames:v 720 -r 30 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -disposition:v:0 default -metadata title='move_1_stack_direct — reconstructed orbit' -y "$delivery_dir/output.mkv"
ffmpeg -v error -i "$delivery_dir/output.mkv" -map 0:v:0 -c copy -movflags +faststart -y "$delivery_dir/preview.mp4"
ffmpeg -v error -i "$delivery_dir/output.mkv" -f null -
ffmpeg -v error -i "$delivery_dir/preview.mp4" -f null -
