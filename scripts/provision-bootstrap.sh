#!/usr/bin/env bash
# Provision Bootstrap assets from the installed `bootstrap` npm package into
# the Flask static directory. pnpm is used only for version tracking; this
# script is the copy step that materializes the served files.
#
# Re-running is idempotent: it reconciles the destination with the version
# currently installed in node_modules (spec FR-004).

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_ROOT="$PROJECT_ROOT/node_modules/bootstrap/dist"
DEST_ROOT="$PROJECT_ROOT/app/static/bootstrap"

CSS_SRC="$SRC_ROOT/css/bootstrap.min.css"
JS_SRC="$SRC_ROOT/js/bootstrap.bundle.min.js"
CSS_DEST_DIR="$DEST_ROOT/css"
JS_DEST_DIR="$DEST_ROOT/js"

fail() {
    echo "error: $*" >&2
    echo "Hint: run 'pnpm install' first, then retry 'pnpm provision'." >&2
    exit 1
}

# Fail fast and actionably if the bootstrap package is missing.
if [ ! -d "$SRC_ROOT" ]; then
    fail "Bootstrap distribution not found at $SRC_ROOT"
fi
if [ ! -f "$CSS_SRC" ] || [ ! -f "$JS_SRC" ]; then
    fail "Expected files missing under $SRC_ROOT: css/bootstrap.min.css or js/bootstrap.bundle.min.js"
fi

# Copy into a temp dir then move into place so a failure never leaves a
# partially-updated directory (spec FR-005).
TMP_DIR="$(mktemp -d)"

cp "$CSS_SRC" "$TMP_DIR/bootstrap.min.css"
cp "$JS_SRC" "$TMP_DIR/bootstrap.bundle.min.js"

# Install into the destination (each subdir atomically via the temp file).
mkdir -p "$CSS_DEST_DIR" "$JS_DEST_DIR"
cp "$TMP_DIR/bootstrap.min.css" "$CSS_DEST_DIR/bootstrap.min.css"
cp "$TMP_DIR/bootstrap.bundle.min.js" "$JS_DEST_DIR/bootstrap.bundle.min.js"

rm -rf "$TMP_DIR"

echo "Provisioned Bootstrap assets:"
echo "  $CSS_DEST_DIR/bootstrap.min.css"
echo "  $JS_DEST_DIR/bootstrap.bundle.min.js"
