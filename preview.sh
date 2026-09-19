#!/usr/bin/env bash
#
# Serve this directory over HTTP and open it in a browser.
#
# Why this exists: the pages link their assets with root-absolute paths
# (/assets/tailwind.css, /assets/fonts/fonts.css, /favicon.svg). Opening a page as a
# file:// URL resolves those against the FILESYSTEM root, so they all fail to load and
# the page renders with no Tailwind — no grid, no spacing, a giant logo. The absolute
# paths are correct for production (Pages serves from the domain root, and pd/ sits one
# level down), so the fix is to preview over HTTP, not to change the links.
#
#   ./preview.sh           # landing page
#   ./preview.sh pd/       # a specific path
#   ./preview.sh glass-box/data.html
#   PORT=9000 ./preview.sh
#
# Ctrl-C stops the server.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

PORT="${PORT:-8901}"
REQUEST_PATH="${1:-}"

# Step forward if the port is already taken, rather than failing or silently
# attaching to whatever is already there.
while lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; do
    echo "port $PORT is in use, trying $((PORT + 1))"
    PORT=$((PORT + 1))
done

# Bind to loopback only: this is a local preview, not something to put on the network.
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!

# Clear the trap first so this runs exactly once: without it a TERM fires cleanup and
# then the resulting exit fires it a second time through the EXIT trap.
cleanup() {
    trap - INT TERM EXIT
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
    printf '\nstopped\n'
}
trap cleanup INT TERM EXIT

# Wait for the server to actually answer before opening the browser, so the first
# load isn't a connection error.
for _ in $(seq 1 50); do
    if curl -fsS -o /dev/null "http://127.0.0.1:$PORT/" 2>/dev/null; then
        break
    fi
    sleep 0.1
done

URL="http://127.0.0.1:${PORT}/${REQUEST_PATH}"

echo "serving $(pwd)"
echo "        $URL"
echo "ctrl-c to stop"

open "$URL"

wait "$SERVER_PID"
