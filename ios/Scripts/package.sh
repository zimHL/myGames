#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/dist"

APP_PATH="$(find "$BUILD_DIR/Payload" -maxdepth 2 -type d -name '*.app' | head -n 1)"
if [ -z "$APP_PATH" ]; then
    echo "No .app found in $BUILD_DIR/Payload"
    echo "Run ios/Scripts/build.sh first."
    exit 1
fi

echo "=== Package MyGames.tipa ==="

# 1. Resign with TrollStore entitlements
echo ">>> Signing with ldid..."
if command -v ldid >/dev/null 2>&1; then
    ldid -S"$PROJECT_ROOT/ios/Entitlements/TrollStore.plist" "$APP_PATH/MyGames"
    echo ">>> Signing done."
else
    echo ">>> WARNING: ldid not found, skipping signing."
    echo "    The .tipa may not install on TrollStore without signing."
fi

# 2. Create .tipa
echo ">>> Creating .tipa..."
cd "$BUILD_DIR"
zip -r MyGames.tipa Payload -x "._*" -x ".DS_Store" -x "__MACOSX" > /dev/null

echo "=== Package complete: $BUILD_DIR/MyGames.tipa ==="