# UI/Layout Contract: Bookmarks Sidebar

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

This contract defines the observable, testable frontend layout produced by the
homepage template after the UIKit → Bootstrap migration. It captures the rendered
markup contract that integration tests assert against (spec FR-001..FR-008).

## Bootstrap Vendoring Contract

- Bootstrap 5 CSS and JS MUST be served from local static assets under
  `app/static/bootstrap/` and referenced from the template via
  `{{ url_for('static', filename='bootstrap/...') }}`.
- The rendered page MUST reference local `/static/bootstrap/...` URLs and MUST NOT
  reference any CDN or remote URL, so the UI works fully offline (spec FR-008/assumption).

## Responsive Grid Contract

The homepage body uses a single `.row` containing two columns:

| Viewport | Services/apps column | Bookmarks column | Result |
|----------|----------------------|------------------|--------|
| `≥ lg` (≥992px) | `col-lg-9` | `col-lg-3` | Two columns: apps left, bookmarks right |
| `< lg` (narrow/phone) | `col-12` | `col-12` | Stacked: apps first, bookmarks below |

Concretely:

- The services section MUST use grid classes `col-12 col-lg-9`.
- The bookmarks container MUST use grid classes `col-12 col-lg-3`.
- The services column MUST appear before the bookmarks column in the DOM so that on
  mobile the bookmarks naturally fall **below** the apps with no horizontal scroll.
- The two columns MUST be wrapped in an element with the `row` class.

### Breakpoint

- A single, consistent breakpoint (`lg`, 992px) separates desktop from mobile
  (spec FR-005). Reflow is handled entirely by Bootstrap grid so behavior is
  deterministic and non-flickering.

## Group Collapse Contract

- Each bookmark group header toggles its bookmarks using **Bootstrap's Collapse**
  component.
- Collapsed/expanded state persists across visits (feature 001 FR-006) — toggling
  writes to `localStorage` and the page re-applies persisted state on load.
- When no bookmarks are configured, the desktop page renders gracefully (apps area
  fills available width; no empty/broken right column) (spec FR-008).

## Markup Test Points

Integration tests verify at minimum:

- `col-12` and `col-lg-9` present on the services container.
- `col-12` and `col-lg-3` present on the bookmarks container.
- A `row` class wraps both columns.
- `/static/bootstrap/` asset references present; no `cdn` / insecure remote CSS.
- Viewport meta present (mobile readiness).
- Group names/labels still render (regression guard).

## Non-Changes

- Backend data model, YAML config schema, and validation are unchanged; see
  [config-contract](config-contract.md) (identical to feature 001).
