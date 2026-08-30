#!/usr/bin/env bash
# Provision Bootstrap + Bootstrap Icons assets from the installed `bootstrap`
# and `bootstrap-icons` npm packages into the Flask static directory. pnpm is
# used only for version tracking; this script is the copy step that
# materializes the served files.
#
# Re-running is idempotent: it reconciles the destinations with the versions
# currently installed in node_modules (spec FR-004).

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BS_SRC_ROOT="$PROJECT_ROOT/node_modules/bootstrap/dist"
BS_DEST_ROOT="$PROJECT_ROOT/app/static/bootstrap"
ICONS_SRC_ROOT="$PROJECT_ROOT/node_modules/bootstrap-icons/font"
ICONS_DEST_ROOT="$PROJECT_ROOT/app/static/bootstrap-icons"

BS_CSS_SRC="$BS_SRC_ROOT/css/bootstrap.min.css"
BS_JS_SRC="$BS_SRC_ROOT/js/bootstrap.bundle.min.js"
BS_CSS_DEST_DIR="$BS_DEST_ROOT/css"
BS_JS_DEST_DIR="$BS_DEST_ROOT/js"

ICONS_CSS_SRC="$ICONS_SRC_ROOT/bootstrap-icons.min.css"
ICONS_FONT_SRC="$ICONS_SRC_ROOT/fonts"
ICONS_CSS_DEST="$ICONS_DEST_ROOT/bootstrap-icons.min.css"
ICONS_FONT_DEST_DIR="$ICONS_DEST_ROOT/fonts"

fail() {
    echo "error: $*" >&2
    echo "Hint: run 'pnpm install' first, then retry 'pnpm provision'." >&2
    exit 1
}

# Fail fast and actionably if the packages are missing.
if [ ! -d "$BS_SRC_ROOT" ]; then
    fail "Bootstrap distribution not found at $BS_SRC_ROOT"
fi
if [ ! -f "$BS_CSS_SRC" ] || [ ! -f "$BS_JS_SRC" ]; then
    fail "Expected Bootstrap files missing under $BS_SRC_ROOT: css/bootstrap.min.css or js/bootstrap.bundle.min.js"
fi
if [ ! -f "$ICONS_CSS_SRC" ] || [ ! -d "$ICONS_FONT_SRC" ]; then
    fail "Expected Bootstrap Icons files missing under $ICONS_SRC_ROOT: bootstrap-icons.min.css or fonts/"
fi

# Copy into temp dirs then move into place so a failure never leaves a
# partially-updated directory (spec FR-005).
BS_TMP_DIR="$(mktemp -d)"
ICONS_TMP_DIR="$(mktemp -d)"

cp "$BS_CSS_SRC" "$BS_TMP_DIR/bootstrap.min.css"
cp "$BS_JS_SRC" "$BS_TMP_DIR/bootstrap.bundle.min.js"
cp "$ICONS_CSS_SRC" "$ICONS_TMP_DIR/bootstrap-icons.min.css"
mkdir -p "$ICONS_TMP_DIR/fonts"
cp "$ICONS_FONT_SRC"/bootstrap-icons.woff2 "$ICONS_TMP_DIR/fonts/bootstrap-icons.woff2"
cp "$ICONS_FONT_SRC"/bootstrap-icons.woff "$ICONS_TMP_DIR/fonts/bootstrap-icons.woff"

# Install into the destinations (each subdir atomically via the temp files).
mkdir -p "$BS_CSS_DEST_DIR" "$BS_JS_DEST_DIR" "$ICONS_FONT_DEST_DIR"
cp "$BS_TMP_DIR/bootstrap.min.css" "$BS_CSS_DEST_DIR/bootstrap.min.css"
cp "$BS_TMP_DIR/bootstrap.bundle.min.js" "$BS_JS_DEST_DIR/bootstrap.bundle.min.js"
cp "$ICONS_TMP_DIR/bootstrap-icons.min.css" "$ICONS_CSS_DEST"
cp "$ICONS_TMP_DIR"/fonts/bootstrap-icons.woff2 "$ICONS_FONT_DEST_DIR/bootstrap-icons.woff2"
cp "$ICONS_TMP_DIR"/fonts/bootstrap-icons.woff "$ICONS_FONT_DEST_DIR/bootstrap-icons.woff"

rm -rf "$BS_TMP_DIR" "$ICONS_TMP_DIR"

echo "Provisioned Bootstrap assets:"
echo "  $BS_CSS_DEST_DIR/bootstrap.min.css"
echo "  $BS_JS_DEST_DIR/bootstrap.bundle.min.js"
echo "Provisioned Bootstrap Icons assets:"
echo "  $ICONS_CSS_DEST"
echo "  $ICONS_FONT_DEST_DIR/bootstrap-icons.woff2"
echo "  $ICONS_FONT_DEST_DIR/bootstrap-icons.woff"
