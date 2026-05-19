#!/bin/sh
# Build and package MyGames for TrollStore in one step
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

echo "=== MyGames iOS Build & Package ==="

"$SCRIPT_DIR/build.sh"
"$SCRIPT_DIR/package.sh"

echo "=== Done: $SCRIPT_DIR/../dist/MyGames.tipa ==="