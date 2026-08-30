# Bookmark Link Icon Contract

**Date**: 2026-08-30
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

Contract for rendering bookmark link icons in the same way as homelab service icons, and
for keeping the repository free of unsupported icon values.

## Configuration

- A bookmark's optional `icon` field accepts a full remote image URL (`http(s)`) only.
- Any short-word icon value (e.g., `youtube`, `bank`, `play`) is **NOT** a supported form
  anywhere in this project and MUST be removed from the repository (example config and
  docs included), replaced with a full image URL or removed.

## Rendering / Behavior

- When a bookmark's `icon` is a valid `http(s)` URL, render it as an `<img>` beside the
  bookmark's text label, using lazy loading and the same fallback approach as service
  icons (spec FR-001).
- When a bookmark has no `icon`, or its `icon` is not a valid `http(s)` URL (e.g., a short
  word, malformed, or unsafe value), render only the text label — no `<img>`, no broken
  image (spec FR-002, FR-007).
- Each bookmark renders independently; a missing or failed icon on one bookmark MUST NOT
  affect any other (spec FR-004).

## Validation & Safety

- Only values that pass the existing `http(s)` URL validation may be emitted as an `<img
  src>`; unsafe values (e.g., `javascript:`) are NEVER rendered as a source (spec FR-005;
  Security Requirements).
- Rendered output is HTML-escaped.
- Changing a bookmark's `icon` in the YAML config takes effect on reload with no code
  change or rebuild (spec FR-003).

## Repository hygiene

- The example config and documentation MUST NOT contain short-word icon values (spec
  FR-008). Group-level and bookmark-level icons alike.

## Example

```yaml
bookmark_groups:
  - name: Media
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
        icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/youtube.svg"
      - label: Spotify
        url: "https://open.spotify.com"
        # no icon -> the text label is shown
```

## Verification

- A bookmark with a URL `icon` renders an `<img>` whose `src` is that URL.
- A bookmark with no `icon`, or with a short-word/non-URL `icon`, renders no `<img>` and
  shows its text label.
- Unsupported icon values (short words, `javascript:`) are never emitted as a `src`.
- `config/example.yaml` and README contain no short-word icon values.
- `uv run pytest` passes, including new tests for the rendering rules above.
