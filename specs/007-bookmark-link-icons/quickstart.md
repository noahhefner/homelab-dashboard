# Quickstart / Validation Guide: Bookmark Link Icons

**Date**: 2026-08-30
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Validation/run guide for rendering bookmark link icons. Config semantics live in
[contracts/bookmark-icon.md](contracts/bookmark-icon.md) and [data-model.md](data-model.md);
implementation belongs in `tasks.md`.

## Prerequisites

- The dashboard source; Python 3.14 + `uv` for running tests / the app.
- No new runtime dependencies.

## Running Tests / The App

```bash
uv run pytest
uv run -m app.server          # with CONFIG_PATH=config/example.yaml
```

## Configuring a Bookmark Icon

A bookmark's optional `icon` is a full remote image URL, shown beside the label:

```yaml
bookmark_groups:
  - name: Media
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
        icon: "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/youtube.svg"
      - label: Spotify
        url: "https://open.spotify.com"   # no icon -> label only
```

Short-word icons (e.g., `icon: youtube`) are unsupported and must be replaced with a full
URL or removed.

## Validation Scenarios

(**Spec**: FR-*, **Scenario**: US*)

### V1 — Bookmark with a URL icon renders an image (US1, FR-001)

- Configure a bookmark with a full image URL as its `icon`.
- Load the homepage and confirm the bookmark link shows that icon as an `<img>` beside its
  label.

### V2 — Bookmark without an icon shows the label (US1, FR-002)

- Configure a bookmark with no `icon` field.
- Load the homepage and confirm the bookmark shows its text label with no broken/empty
  image.

### V3 — Non-URL / short-word icon falls back to the label (US1, FR-007)

- Configure a bookmark with `icon: youtube` (a short word).
- Load the homepage and confirm it renders the text label and emits no `<img>` for that
  value (no broken image, page unaffected).

### V4 — Per-bookmark independence (US2, FR-004)

- In one group, give some bookmarks URL icons and leave others without.
- Load the homepage and confirm each bookmark renders independently; a missing/failed icon
  does not affect its neighbors.

### V5 — Config change / icon add-remove takes effect on reload (US2, FR-003)

- Given a bookmark with no icon, add a URL icon and reload — the icon appears.
- Remove it and reload — the label-only rendering returns. No rebuild/restart.

### V6 — Example config has no short-word icons (FR-008)

- Inspect `config/example.yaml` (and README) and confirm no `icon: <short-word>` values
  remain; all icons are full URLs or absent.

### V7 — Unsafe icon value is never a rendered source (FR-005, Security)

- With a bookmark `icon: "javascript:alert(1)"`, load the homepage and confirm the value
  is never emitted as an `<img src>` (falls back to the label).
