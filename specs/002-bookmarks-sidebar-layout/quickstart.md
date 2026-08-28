# Quickstart / Validation Guide: Bookmarks Sidebar Layout

**Date**: 2026-08-28
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This guide lets you run the dashboard and validate this feature end-to-end: bookmarks
on the right on desktop, below the apps on mobile, using **vendored Bootstrap** with no
internet connectivity. It is a validation/run guide — implementation belongs in
`tasks.md`. Data details live in [data-model.md](data-model.md); UI/grid behavior lives
in [contracts/ui-contract.md](contracts/ui-contract.md).

## Prerequisites

- Python 3.14+ and `uv` (per https://docs.astral.sh/uv/), **or** Docker.
- This repo with the vendored Bootstrap assets present under `app/static/bootstrap/`.

## 1. Local Run (Development)

```bash
uv sync
. .venv/bin/activate
export CONFIG_PATH=config/example.yaml
python -m app.server
```

Open <http://localhost:5000>.

## 2. Run as a Single Docker Container (Production)

```bash
docker build -t homelab-dashboard .
docker run --rm -p 5000:5000 \
  -e CONFIG_PATH=/app/config/config.yaml \
  -v "$PWD/config/example.yaml:/app/config/config.yaml:ro" \
  homelab-dashboard
```

Open <http://localhost:5000>.

## 3. Validation Scenarios (prove the feature works)

Refer to [contracts/ui-contract.md](contracts/ui-contract.md) for the grid/collapse
contract and [contracts/http-contract.md](contracts/http-contract.md) for HTTP behavior.

### V1 — Bookmarks on the right on desktop

Load the page in a **wide desktop** browser window (≥992px).
- The homelab apps occupy the main left area.
- The bookmark groups appear in a **right-hand column** beside the apps — not below them.
- Both apps and bookmarks are visible without scrolling.

(**Spec**: FR-001, FR-002; **Scenario**: US1-1..3; **Contract**: grid >= lg)

### V2 — Bookmarks below the apps on mobile

Resize the window to **phone width** (<992px) or use device emulation.
- The bookmarks now appear **below** the homelab apps.
- There is **no horizontal scrolling**; everything is reachable.

(**Spec**: FR-003, FR-007; **Scenario**: US2-1..3, US3-3; **Contract**: grid < lg)

### V3 — Smooth responsive reflow

Continuously resize the window from desktop width down to phone width and back.
- At the breakpoint, the bookmarks move from the right column to below the apps (and
  back).
- No content is clipped, overlapping, or pushed off-screen at any width.

(**Spec**: FR-004, FR-005; **Scenario**: US3-1..2; **Contract**: single `lg` breakpoint)

### V4 — Collapsible groups still work

Collapse and re-expand a bookmark group in **both** desktop and mobile placements.
- The group toggles correctly.
- The open/closed state persists on the next visit.

(**Spec**: FR-006; **feature 001** FR-006; **Contract**: group collapse)

### V5 — Offline / vendored Bootstrap

Turn off internet connectivity (or inspect the rendered HTML), then load the page.
- The page still renders and styles correctly (Bootstrap served from
  `/static/bootstrap/...`).
- There are **no** CDN URLs in the rendered HTML.

(**Spec**: user requirement "vendor Bootstrap assets, works without internet";
**Assumption**: offline; **Contract**: no remote/CDN asset refs)

### V6 — No-bookmarks graceful state

Set a config with no `bookmark_groups` and load on desktop.
- The apps area fills the available width; there is no empty/broken right column.

(**Spec**: FR-008; **Edge case**: no bookmarks)

## Automated Tests

Run the full suite (contract, unit, integration):

```bash
uv run pytest
```

Integration tests assert the new grid classes (`col-12 col-lg-9` / `col-12 col-lg-3`),
the `row` wrapper, the offline `/static/bootstrap/...` asset references, and regressions
for group rendering. See `tasks.md` for the task breakdown.
