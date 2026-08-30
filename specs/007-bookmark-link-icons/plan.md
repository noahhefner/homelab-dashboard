# Implementation Plan: Bookmark Link Icons

**Branch**: `007-bookmark-link-icons` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/007-bookmark-link-icons/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Render a bookmark's configured `icon` as a remote image beside its text label, matching
how homelab service links render their icons. A full `http(s)` image URL is shown as an
`<img>`; a bookmark with no icon, or a non-URL/short-word icon value, falls back to the
plain text label (no monogram is needed because the label is always present). Because
short-word icons are unsupported anywhere in this project, this feature also replaces
every short-word icon value in `config/example.yaml` with a full remote image URL (or
removes it where no suitable URL exists), so the repo no longer contains unsupported
short-word icons.

## Technical Context

**Language/Version**: Python 3.14 backend (unchanged, Flask 3.x). Frontend is
server-rendered Jinja2 templates with Bootstrap 5.3 plus small vanilla JS.

**Primary Dependencies**: Flask 3.x, PyYAML (unchanged). Bootstrap 5.3.8 (unchanged,
feature 003). No new dependencies. The existing service-icon rendering pattern (feature
001 / feature 004) is replicated for bookmarks.

**Storage**: None (no database). The `icon` value is read from the YAML config, already
parsed into each `Bookmark` (as a string) via the existing `ConfigLoader`, and available
at render time.

**Testing**: pytest (`uv run pytest`) — unit + integration. Unit tests cover bookmark icon
rendering in the template (URL → `<img>`, non-URL → label fallback, unsafe value not
emitted as `src`). Integration tests cover the example config and that existing tests
still pass. The existing `test_views_services.py` tests establish the exact assertion
patterns (re-used).

**Target Platform**: Linux server (Docker host) serving the dashboard; modern browsers.

**Project Type**: web application (backend + frontend), a small, bounded config + UI
enhancement.

**Performance Goals**: No change — preserve the existing target (homepage interactive
under 2 seconds). Icons use the same lazy-loading behavior as service icons, and bookmark
icons only load when present.

**Constraints**:
- A bookmark icon is a full remote image URL (matching homelab); short-word icons are
  NOT supported anywhere and MUST be removed from the repo (spec FR-007/FR-008).
- Missing/invalid/unsafe icon values MUST fall back to the plain text label and never
  break the page or render an unsafe `src` (spec FR-002, edge cases; Security
  Requirements).
- Each bookmark renders independently; a missing/failed icon on one must not affect its
  neighbors (spec FR-004).
- Changing a bookmark's icon in the config takes effect on reload with no rebuild/restart
  (already provided by the config-reload mechanism).
- Output is HTML-escaped and validated so no injection is possible (Security
  Requirements).

**Scale/Scope**: Single-project enhancement. Touches the template (to render the icon),
the CSS (for bookmark icon sizing/placement), the example config + README (remove
short-word icons, document URL icons), plus tests. No model/schema change is required —
the `Bookmark.icon` field already exists and is parsed. Small and bounded.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate 1 — Extensibility & Modularity**: The change stays within the existing
config → schema → template boundaries. It consumes the already-parsed `Bookmark.icon`
field and renders it exactly like the existing service-icon path. No new modules or
entangled concerns. ✅

**Gate 2 — Testability (Test-First, NON-NEGOTIABLE)**: New tests (written first) verify:
a bookmark with a URL icon renders an `<img>` with that `src`; a bookmark with a non-URL
(or short-word) icon renders the plain label and no `<img>`; a bookmark with no icon
renders the plain label; an unsafe value (e.g., `javascript:`) is never emitted as `src`;
and the example config contains no short-word icons. These are deterministic static-markup
+ unit assertions, no network. ✅

**Gate 3 — YAGNI & Simplicity**: No new framework, storage, dependency, or server state.
Reuses the existing `Bookmark.icon` field and the existing service `<img>`-with-fallback
template pattern. No icon CDN mapping, no font-icon class mechanism, no new config key.
The simplest design that satisfies the spec. ✅

**Gate 4 — Security Requirements**: The icon is only emitted as an `<img src>` when it
passes the existing `url` validator (http/https), so unsafe values (`javascript:`, etc.)
are never rendered as sources — matching the service-icon behavior and its existing
tests. Output is HTML-escaped. No new secrets, network exposure, or injection surface. ✅

**Gate 5 — DX First / Readability**: Reuses the exact template pattern the reader already
knows from service icons, plus small CSS classes; the example config is corrected to
supported values. No added friction to the common dev loop. ✅

No violations; no Complexity Tracking table required until post-design re-check (see
bottom).

## Project Structure

### Documentation (this feature)

```text
specs/007-bookmark-link-icons/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (bookmark icon contract)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# MODIFIED: bookmark icon rendering + docs/tests
app/
├── templates/index.html          # MODIFIED: render bookmark.icon as <img> when it is a
│                                  valid URL; else render the plain text label (no image)
└── static/app.css                # MODIFIED: bookmark-link icon sizing/placement

config/example.yaml               # MODIFIED: replace all short-word icon values (group
                                  # and bookmark) with full remote image URLs or remove
README.md                         # MODIFIED: document bookmark icon = full image URL

tests/
├── unit/test_bookmark_icons.py   # NEW: bookmark icon rendering (URL img, non-URL fallback,
│                                  # no-icon label, unsafe src never emitted)
└── integration/test_bookmark_icons.py  # NEW: example config has no short-word icons;
                                  # bookmarks with URL icons render as <img>

contracts/                        # NEW: bookmark-icon contract (in specs/007/contracts/)
```

**Structure Decision**: Keep the single-project layout. The change is a thin, deliberate
extension of the existing service-icon template pattern applied to bookmarks, plus a
config/docs cleanup removing unsupported short-word icons. No structural reorganization.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No Constitution Check violations; this table is intentionally empty. (Re-checked after
Phase 1 — no violations. The design reuses the existing `Bookmark.icon` field, the
existing service-icon `<img>`/fallback template pattern, and the existing URL validator;
adds no dependency, module, or icon-mapping machinery; and is fully covered by
deterministic static-markup tests.)
