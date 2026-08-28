# Quickstart / Validation Guide: Homelab Dashboard Homepage

**Date**: 2026-08-28
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This guide lets you run the dashboard and validate the feature end-to-end. It is a
**validation/run guide**, not an implementation reference (implementation belongs in
`tasks.md`). Data details live in [data-model.md](data-model.md); config and HTTP
shapes live in [contracts/](contracts/).

## Prerequisites

- Python 3.14+ and `uv` (installed per https://docs.astral.sh/uv/), **or** Docker.
- The dashboard source (this repo).

## 1. Local Run (Development)

```bash
uv sync
. .venv/bin/activate
export CONFIG_PATH=config/example.yaml
python -m app.server
```

Open <http://localhost:5000>. You should see the services and bookmark groups from
`config/example.yaml`.

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

Refer to [contracts/config-contract.md](contracts/config-contract.md) for the config
schema and [contracts/http-contract.md](contracts/http-contract.md) for the HTTP
behavior.

### V1 — Services render as clickable tiles

Edit `config/example.yaml` so it lists a few services with `name`, `url`, and `icon`.
Load the page and confirm:
- Every service appears as a tile with its name and icon (or monogram fallback).
- Clicking a tile opens its URL in a new tab.

(**Spec**: FR-002, FR-003; **Scenario**: US1-1..3)

### V2 — Live config reload without restart

With the app running, edit the mounted `config.yaml`: add a service, then remove a
bookmark. Save the file and simply **refresh** the browser.
- The new service appears.
- The removed bookmark disappears.
- No backend or container restart was performed.

(**Spec**: FR-001, FR-008; **Scenario**: US2-1..2)

### V3 — Large number of bookmarks, grouped

Write a config with 100+ bookmarks distributed across 5+ named groups. Load the page
and confirm:
- Bookmarks are displayed within their groups (not one flat list).
- The page loads and is usable with no layout breakage within the SC-004 time target.

(**Spec**: FR-005, FR-009; **Scenario**: US3-1..2)

### V4 — Collapsible groups

On the loaded page, collapse and re-expand a bookmark group.
- The group toggles as expected.
- The collapsed/expanded state persists on the next visit.

(**Spec**: FR-006; **Scenario**: US3-3)

### V5 — Mobile responsiveness

Open the page at phone width (dev tools or a real phone).
- Tiles and bookmark groups arrange into a usable layout with **no horizontal scroll**.
- Tapping a tile opens the destination (no hover required).

(**Spec**: FR-007; **Scenario**: US4-1..3)

### V6 — Invalid config error handling

Temporarily corrupt `config.yaml` (e.g., bad indentation), then load the page.
- A clear, readable error message is shown — not a blank or broken page.

(**Spec**: FR-010; **Edge case**: malformed YAML)

## Automated Tests

Run the test suite (contract, unit, integration):

```bash
uv run pytest
```

Contract tests validate the config schema; integration tests validate load + live
reload + render. See `tasks.md` for the full task breakdown.
