# Implementation Plan: Download Config & Icon Links

**Branch**: `010-download-and-icon-links` | **Date**: 2026-08-31 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/010-download-and-icon-links/spec.md`

## Summary

Add a **download** control to the editor page (`/config`) that lets the owner save the
current config YAML to their machine, and add a small, always-visible set of **links to
iconography websites** on the same page to support finding tile/bookmark icons while
editing. The download serves the exact raw bytes of the config file currently on disk
(not the unsaved textarea buffer), uses the config file's basename as the download
filename, works in both editing and read-only modes, and surfaces a clear error if the
file cannot be read. The icon links (dashboardicons.com and the homarr-labs/dashboard-icons
GitHub repo) open in a new tab (`_blank`) and are present in both editing and read-only
modes. This extends the existing Flask + Bootstrap config page; no new dependencies.

## Technical Context

**Language/Version**: Python 3.14 backend (unchanged, Flask 3.x). Server-rendered Jinja2
with Bootstrap 5.3; small inline vanilla JS on the editor page; no frontend build step.

**Primary Dependencies**: None new. Reuses Flask's `send_file`/`Response` for the download
(no filesystem-serving beyond the existing `send_from_directory` favicons) and the present
`read_raw` helper in `app/editor.py` to read the exact on-disk bytes.

**Storage**: No database. Single YAML config file on disk (the already-loaded `CONFIG_PATH`),
served read-only as the download payload. The download adds no write path.

**Testing**: pytest (`uv run pytest`). Unit: a small `read_raw`-based download helper and
filename derivation. Integration: `GET /config/download` returns the exact file bytes with
the correct `Content-Disposition` filename in editing and read-only modes; returns a clear
error when the file is unreadable; `/config` renders the download button and the icon links
in both modes.

**Target Platform**: Linux server (Docker host) serving the dashboard; modern browsers.

**Project Type**: web application (backend + frontend); an additive read-only route + UI
affordances on the existing config page. Net-new but small; no architectural change.

**Performance Goals**: Preserve the existing target (page load under 2 seconds). A download
is a trivial static-file serve for homelab-sized configs (<100 KB) — must complete in well
under the spec's 2-second target (effective target: sub-second).

**Constraints**:
- **Download is read-only on-disk** (FR-002, FR-009): the served payload is exactly the
  bytes of the config file on disk (`read_raw`), never the unsaved textarea value.
- **Filename = config basename** (FR-003): e.g., `config/example.yaml` → `example.yaml`.
  Derived server-side from the resolved config path; never client-supplied or free-text.
- **Available in both modes** (FR-004, FR-008): the download button and icon links are
  present whether or not the `editor` flag is enabled.
- **Icon links open in a new tab** (FR-007): `target="_blank" rel="noopener noreferrer"`.
- **Injection-safe**: the download response sets a fixed `Content-Disposition` filename
  derived from the config path; no untrusted content is placed in the header. Icon links are
  static, reviewed URLs (no user input).
- **Security-grounded**: no new network exposure, no new secrets, no write path; the icon
  link URLs are fixed `https` destinations.

**Scale/Scope**: Single-owner homelab dashboard; one config file; one existing template
page; one new route plus template/JS additions and tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Testability (IV)** — GATE. Tests MUST be written first (red-green). The download route
  (exact bytes, correct filename, editing + read-only, unreadable-file error) and the
  rendered download button + icon links MUST have tests. — *Covered by the Testing plan;
  expanded in Phase 1.*
- **Developer Experience (I)** — GATE. The change MUST NOT add friction to
  `uv run pytest` / local run / `pnpm provision`. — *Satisfied: no new dependencies, no
  build step, no new runner; the feature is additive to the existing config page.*
- **Readability (II)** — GATE. New code MUST match surrounding structure and conventions.
  The download route mirrors the existing `view_config`/`save_config` pattern in
  `app/views.py`, reuses `read_raw` from `app/editor.py`, and the UI reuses Bootstrap
  button/link classes already used on the page. — *Satisfied by mirroring the established
  route + template patterns (Phase 1).*
- **Extensibility & Modularity (III)** — PASS. The download is a small read-only route in
  the existing `dashboard` blueprint; icon links are static template content. No new module
  boundaries are required.
- **YAGNI/Simplicity (V)** — PASS. The simplest design is one new route reusing `read_raw`
  and static template additions; no new abstraction, storage, or dependency.
- **Security Requirements** — GATE. The download reads only the fixed, resolved config path
  (no client path); `Content-Disposition` filename is derived server-side; icon links are
  trusted static `https` URLs opened with `noopener noreferrer`; no new write path, secrets,
  or network exposure. — *Satisfied; see contracts. No complexity justification required
  (Complexity Tracking intentionally empty).*

*Post-Phase-1 re-check:* See "Post-Design Constitution Re-Check" below.

## Project Structure

### Documentation (this feature)

```text
specs/010-download-and-icon-links/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output: download + icon-link design decisions
├── data-model.md        # Phase 1 output: payload/entities for the config download
├── quickstart.md        # Phase 1 output: how to run + verify the feature
├── contracts/           # Phase 1 output: download + icon-link UI contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
app/
├── views.py             # (modified) add GET /config/download route + filename derivation
├── editor.py            # (unchanged) reuses read_raw
└── templates/
    └── config.html      # (modified) add download button + icon-links section in both modes

tests/
├── unit/test_editor_config.py          # (modified) unit test for download filename helper
└── integration/test_config_download.py  # (new) download route + template rendering tests
```

**Structure Decision**: Keep the single-project Flask layout. The download is a small
read-only route added to the existing `dashboard` blueprint, and the icon links are static
template content in `config.html`. No reorganization, new module, or new dependency is
needed. Note: no filesystem writes are introduced — this feature is purely read + present.

## Post-Design Constitution Re-Check

*Must be confirmed after Phase 1 (data-model, contracts, quickstart) is generated.*

- **Testability (IV)** — GATE. Design adds tests for: exact on-disk byte download, correct
  basename filename, availability in editing and read-only modes, unreadable-file error, and
  the rendered download button + icon links. — *Confirmed in quickstart.md (V1–V5) and
  contracts.*
- **Developer Experience (I)** — GATE. No new deps/build; no runner change. — *Confirmed.*
- **Readability (II)** — GATE. Route mirrors `view_config`; reuses `read_raw`; template
  reuses Bootstrap button/link classes. — *Confirmed in data-model.md/contracts.*
- **Extensibility & Modularity (III)** — PASS.
- **YAGNI/Simplicity (V)** — PASS.
- **Security Requirements** — GATE. Only the fixed config path is read; filename derived
  server-side; icon links static trusted `https` opened with `noopener noreferrer`; no write
  path/exposure/secrets. — *Confirmed in contracts.*
- **Gate result**: PASS — no violations unjustified; no Complexity Tracking entry required.

## Complexity Tracking

> Intentionally empty — no Constitution violations require justification. The feature is a
> small read-only route reusing existing helpers plus static template content (PASS on
> III/V), with no new dependency or build step introduced.
