#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/dist"
APP_DIR="$BUILD_DIR/Payload/MyGames.app"

echo "=== Build MyGames for iOS ==="

rm -rf "$BUILD_DIR"
mkdir -p "$APP_DIR"

# 1. Compile Swift sources
echo ">>> Compiling Swift..."
xcrun -sdk iphoneos swiftc \
    -o "$APP_DIR/MyGames" \
    "$PROJECT_ROOT/ios/Sources/AppDelegate.swift" \
    "$PROJECT_ROOT/ios/Sources/ViewController.swift" \
    -target arm64-apple-ios14.0 \
    -O

echo ">>> Swift compilation done."

# 2. Copy Info.plist
cp "$PROJECT_ROOT/ios/Resources/Info.plist" "$APP_DIR/"

# 3. Copy web resources (exclude .git, ios, .github, dist)
echo ">>> Copying web resources..."
rsync -a \
    --exclude='.git' \
    --exclude='ios' \
    --exclude='.github' \
    --exclude='dist' \
    --exclude='README.md' \
    --exclude='.gitignore' \
    "$PROJECT_ROOT/" "$APP_DIR/"

# 4. Generate app icon
echo ">>> Generating app icon..."
python3 "$PROJECT_ROOT/ios/Scripts/gen-icon.py" "$APP_DIR/AppIcon.png"

echo "=== Build complete: $APP_DIR ==="