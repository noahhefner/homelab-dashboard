# Research: Download Config & Icon Links

**Feature**: [spec.md](spec.md) · **Phase 0** · **Date**: 2026-08-31

## Decisions

### D1 — How to serve the download

- **Decision**: Add a single read-only route `GET /config/download` in the existing
  `dashboard` blueprint that reuses `read_raw(loader.path)` to read the exact on-disk bytes
  and returns them with `Content-Disposition: attachment` and the `yml`/`yaml` mimetype.
- **Rationale**: The spec requires the download to be the exact on-disk content (FR-002),
  not the unsaved textarea buffer (FR-009). `read_raw` already returns the verbatim file
  text and raises `ConfigEditorError` on failure — exactly the semantics needed. A dedicated
  GET route keeps the download side-effect-free (no write path) and trivially testable.
- **Alternatives considered**:
  - A client-side blob download from the textarea value — rejected: would ship the unsaved
    buffer (violates FR-009) and is not testable server-side for byte-exactness.
  - Flask `send_file` on the config path — viable but more machinery than needed; returning
    the text from `read_raw` with an explicit `Response` is simpler and reuses the existing
    error path.

### D2 — Download filename

- **Decision**: Derive the filename server-side from the basename of the resolved config
  path (`os.path.basename(loader.path)`), e.g. `config/example.yaml` → `example.yaml`.
- **Rationale**: Spec FR-003 requires the config basename, not a generic/hardcoded name, and
  it must be derived from the fixed server path — never client-supplied (Security
  Requirements). Adding a `; filename=` to the `Content-Disposition` header with that fixed
  basename is the standard, safe approach.
- **Alternatives considered**:
  - Hardcoded `dashboard.yaml` — rejected: loses the actual config filename (FR-003).
  - Client-supplied filename — rejected on security grounds (untrusted header input).

### D3 — Where/how to render the download button and icon links

- **Decision**: Add a persistent toolbar row at the top of `config.html` (above the
  editor/read-only view) that is rendered in **both** editing and read-only modes. It holds
  a "Download config" button styled as a Bootstrap button with a download icon, and a
  small "Icon sources" section with two `target="_blank" rel="noopener noreferrer"` links
  (dashboardicons.com and the homarr-labs/dashboard-icons GitHub repo).
- **Rationale**: Spec FR-004/FR-008 require the download button and icon links in both
  modes. A single top-level toolbar avoids duplicating markup inside the `{% if
  editing_enabled %}`/`{% else %}` branches and keeps the controls always reachable.
- **Alternatives considered**:
  - Placing buttons only in the editing form — rejected: icon links must also show in
    read-only mode (FR-008).
  - A JavaScript-only download — rejected: not warranted (see D1) and harms testability.

### D4 — Error handling for unreadable config

- **Decision**: When `read_raw` raises `ConfigEditorError` (file missing/unreadable), the
  download route returns an error response (e.g., `404`/`500` with a clear message) and the
  page's existing error rendering path (`view_config`) continues to show the current
  "Unable to load the configuration" alert.
- **Rationale**: Spec FR-005 requires that a failed download never return an empty/partial
  file and does surface a clear error. Reusing the existing `ConfigEditorError` from
  `editor.py` keeps one error contract.
- **Alternatives considered**: An empty `200` download — rejected (FR-005).

### D5 — Iconography link targets

- **Decision**: Use the two fixed, trusted sources already referenced by the project
  (`https://dashboardicons.com` and `https://github.com/homarr-labs/dashboard-icons`), each
  opened with `rel="noopener noreferrer"` in a new tab. No dynamic lookup, no user input.
- **Rationale**: Spec FR-006/FR-007 name these exact resources; they are static, `https`,
  and established community sources for homelab dashboard icons (already cited in
  `config/example.yaml` and README). Static markup needs no validation beyond a fixed URL.
- **Alternatives considered**: A configurable list of icon sources — rejected: YAGNI (V);
  the spec calls for fixed links.

## Constraints confirmed

- No new frontend dependency or build step (read-only route + static template content).
- Download is strictly read-only; no write path introduced.
- Filename and URLs are never derived from client input.
