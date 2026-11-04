#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ -n "${STORY_ACTIVATE:-}" ]]; then source "$STORY_ACTIVATE"; fi
export DISPLAY="${DISPLAY:-:91}" LIBGL_ALWAYS_SOFTWARE=true GALLIUM_DRIVER=llvmpipe
if [[ -e media/move1stack-manager-flight-v3.mp4 ]]; then echo 'Preview exists; preserve it before rerendering.' >&2; exit 2; fi
if curl -fsS http://127.0.0.1:9002/manager-flight-render.html >/dev/null 2>&1; then echo 'Port 9002 already in use; stop the existing server.' >&2; exit 2; fi
mkdir -p evidence media
xvfb_pid=''
if [[ ! -S /tmp/.X11-unix/X91 ]]; then Xvfb :91 -screen 0 1280x900x24 -nolisten tcp > evidence/manager-flight-xvfb.log 2>&1 & xvfb_pid=$!; fi
(cd production; exec env NODE_OPTIONS="--require=$PWD/../runtime-settings.cjs" ../node_modules/.bin/vite --host 127.0.0.1 > ../evidence/manager-flight-vite.log 2>&1) & vite_pid=$!
trap 'kill "$vite_pid" 2>/dev/null || true; if [[ -n "$xvfb_pid" ]]; then kill "$xvfb_pid" 2>/dev/null || true; fi' EXIT
for attempt in {1..100}; do if curl -fsS http://127.0.0.1:9002/manager-flight-render.html >/dev/null 2>&1; then break; fi; sleep .2; done
node render-manager-flight.cjs
