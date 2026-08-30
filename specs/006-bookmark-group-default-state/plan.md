# Implementation Plan: Bookmark Group Default State

**Branch**: `006-bookmark-group-default-state` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-bookmark-group-default-state/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Add a per-group configuration option that controls whether a bookmark group starts
**open** or **closed** when the page loads. The config value establishes the default
initial state for each group; when a user has already saved an explicit open/closed
choice for a group (the existing remembered-collapse behavior), that saved choice takes
precedence over the config default. This is delivered as a new optional per-group YAML
field, surfaced to the browser through a data attribute on the group toggle, and consumed
by the existing client-side collapse logic in `app/static/app.js`.

## Technical Context

**Language/Version**: Python 3.14 backend (unchanged, Flask 3.x). Frontend is
server-rendered Jinja2 templates with Bootstrap 5.3 collapse plus small vanilla JS.

**Primary Dependencies**: Flask 3.x, PyYAML (unchanged). Bootstrap 5.3.8 (unchanged,
feature 003). No new dependencies. The existing bookmark collapse/persistence behavior
from feature 002 is extended.

**Storage**: None (no database). Per-group collapse state already persists in the browser
`localStorage` (feature 002); the config default is read from the YAML file (re-parsed per
request via the existing `ConfigLoader`).

**Testing**: pytest (`uv run pytest`) — unit + integration. Unit tests cover the new
schema/model `collapsed` field (parsing, validation, default false). Integration tests
assert the rendered toggle carries the configured default state, and that existing tests
still pass.

**Target Platform**: Linux server (Docker host) serving the dashboard; modern browsers.

**Project Type**: web application (backend + frontend), a small, bounded config + UI
enhancement.

**Performance Goals**: No change — preserve existing target (homepage interactive under 2
seconds); no new network or storage cost (the config default is embedded as an attribute
and consumed client-side).

**Constraints**:
- Per-group configurability: each group is configured independently (spec FR-001/FR-005).
- Missing/invalid state must fall back gracefully to the default (open) and never break
  the page (spec FR-002, edge cases).
- A user's previously saved open/closed choice for a group MUST take precedence over the
  config default (spec FR-004).
- Changing the config default takes effect on reload with no rebuild/restart (spec
  FR-006) — already provided by the config-reload mechanism.
- The config value is a boolean open/closed choice; it only sets the initial state, and
  groups remain manually togglable after load (Assumptions).

**Scale/Scope**: Single-project enhancement. Touches the group model/schema, the template
(to emit the default onto the toggle), the client JS (to prefer saved state, else the
config default), plus tests, example config, and docs. Small and bounded.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: The change stays within the existing group
config → schema → template → client-collapse boundaries. It extends the `BookmarkGroup`
entity with one optional attribute and threads it to the existing browser persistence
logic. No new modules or entangled concerns. ✅

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: New tests (written first) verify:
schema parsing of the `collapsed` field (true/false/absent/invalid) with default false; the
rendered group toggle carries the configured default as a data attribute; and the existing
collapse test expectations still hold. Deterministic static-markup + unit assertions, no
network. ✅

**Gate 3 — YAGNI & Simplicity**: No new framework, storage, or server state. Reuses the
existing YAML field pattern (like `icon`) and the existing localStorage collapse logic.
No per-account or settings UI. The simplest design that satisfies the spec. ✅

**Gate 4 — Security Requirements**: The config value is a boolean rendered into a
template data attribute and HTML-escaped; the group name (already escaped) is unchanged.
No new secrets, network exposure, or injection surface. ✅

**Gate 5 — DX First / Readability**: Adding one documented field is low-friction; the JS
change is a small, clearly-commented addition to the existing collapse block. No added
friction to the common dev loop. ✅

No violations; no Complexity Tracking table required until post-design re-check (see
bottom).

## Project Structure

### Documentation (this feature)

```text
specs/006-bookmark-group-default-state/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (per-group default-state contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# MODIFIED: per-group default state + docs/tests
app/
├── model.py                      # MODIFIED: BookmarkGroup gains `collapsed: bool = False`
├── schema.py                     # MODIFIED: _parse_group parses+validates `collapsed` (default false)
├── templates/index.html          # MODIFIED: emit configured default onto the group toggle
│                                  (e.g., data-default-collapsed="true|false")
└── static/app.js                 # MODIFIED: prefer saved state, else the config default

config/example.yaml               # MODIFIED (optional): document/example per-group `collapsed`
README.md                         # MODIFIED: document the per-group collapsed option

tests/
├── unit/test_schema.py                    # MODIFIED: assert collapsed parsing/default/validation
├── unit/test_model.py                     # NEW (or MODIFIED): collapsed default
├── unit/test_bookmark_group_state.py      # MODIFIED: assert the JS prefers saved state else config default
└── integration/test_bookmark_groups.py    # MODIFIED: assert rendered default-state attribute

contracts/                      # NEW: group default-state contract (in specs/006/contracts/)
```

**Structure Decision**: Keep the single-project layout. The change is a thin, deliberate
extension of the existing per-group config and the existing client-side collapse
persistence (feature 002). No structural reorganization.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty. (Re-checked after
Phase 1 — no violations.)
