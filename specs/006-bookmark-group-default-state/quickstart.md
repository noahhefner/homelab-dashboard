# Quickstart / Validation Guide: Bookmark Group Default State

**Date**: 2026-08-30
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Validation/run guide for the per-group open/closed default on page load. Config semantics
live in [contracts/group-default-state.md](contracts/group-default-state.md) and
[data-model.md](data-model.md); implementation belongs in `tasks.md`.

## Prerequisites

- The dashboard source; Python 3.14 + `uv` for running tests / the app.
- No new runtime dependencies.

## Running Tests / The App

```bash
uv run pytest
uv run -m app.server          # with CONFIG_PATH=config/example.yaml
```

## Configuring a Group's Initial State

Set an optional `collapsed: true|false` on a bookmark group to control its state on page
load:

```yaml
bookmark_groups:
  - name: Media
    collapsed: true        # starts closed
    bookmarks:
      - label: YouTube
        url: "https://www.youtube.com"
  - name: Finance          # no `collapsed` -> starts open
    bookmarks:
      - label: Bank
        url: "https://bank.example.com"
```

## Validation Scenarios

(**Spec**: FR-*, **Scenario**: US*)

### V1 — Closed group loads collapsed (US1, FR-001/FR-003)

- Configure a group with `collapsed: true` (fresh browser, no saved state for that group).
- Load the homepage and confirm the group renders collapsed.

### V2 — Open / unset group loads expanded (US1, FR-002)

- Configure a group with `collapsed: false` and another with no `collapsed` field.
- Load the homepage and confirm both render expanded.

### V3 — Per-group independence (US1, FR-005)

- Configure one group `collapsed: true` and another `collapsed: false`.
- Load the homepage and confirm each respects its own setting, unaffected by the other.

### V4 — Saved user choice wins (US2, FR-004)

- With a group configured `collapsed: true`, open (expand) it during a visit so the choice
  is saved.
- Reload and confirm it stays expanded (the saved choice beats the config default).

### V5 — Config change takes effect on reload (FR-006)

- Start with a group having no `collapsed` (open), no saved choice.
- Set `collapsed: true`, reload, and confirm it renders collapsed — no rebuild/restart.
