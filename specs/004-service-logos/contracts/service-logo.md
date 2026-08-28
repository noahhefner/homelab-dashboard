# Service Logo Contract

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

Contract for how a service logo is configured, validated, and rendered.

## Configuration

- A service logo is supplied through the existing per-service `icon` field in the YAML
  config (no separate `logo` field, no bundled/local logo mechanism).
- The value may be:
  - **Absent / empty / non-URL** → the tile renders a monogram (first letter of the
    service name). This is the fallback path and MUST remain the default when no logo
    is configured (spec FR-002).
  - **A valid absolute `http(s)` URL** → the tile renders that URL as an `<img>` logo
    (spec FR-001, FR-004).
- Any valid absolute `http(s)` URL MUST be accepted; there is no host allow-list
  (spec FR-004).

## Validation & Safety

- The rendered logo `src` MUST pass `validate_url` (absolute `http`/`https` scheme and
  non-empty netloc) before it is used as an image source (spec FR-005).
- The rendered `src` and the service `name` MUST be HTML-escaped to prevent injection.
- `javascript:`/`data:`/relative/malformed values MUST NOT be rendered as an image
  source; they fall back to the monogram.

## Rendering

- Logo `<img>` elements use lazy loading (`loading="lazy"`) and an `onerror` fallback
  so a broken/unreachable URL degrades to the monogram without breaking the page
  (spec FR-002, FR-006 / SC-002).
- The dashboard MUST remain styled and usable when no logos are configured or when the
  recommended dashboardicons.com source is unreachable (feature must not depend on it).

## Recommended Source (encouragement only, not a requirement)

- Documentation and the example config SHOULD encourage sourcing logos from
  dashboardicons.com (spec FR-007). Direct assets follow the jsDelivr CDN pattern:
  `https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/<svg|png>/<name>.<ext>`.
- This source is optional; any valid remote image URL works and the dashboard MUST NOT
  require dashboardicons.com to be reachable.

## Documentation / Example

- `config/example.yaml` service entries SHOULD use dashboardicons.com logo URLs to
  demonstrate the recommended source.
- `README.md`/`quickstart.md` MUST document: how to assign a logo (set `icon` to a
  remote image URL) and where to find logos (dashboardicons.com).

## Verification

- With a service configured to a valid remote logo URL, the homepage renders that URL
  in an `<img>` tag (not a monogram).
- With a service configured to a non-URL or no logo, the homepage renders a monogram.
- A logo value that is not a valid URL is never emitted as an `<img src>`.
- `uv run pytest` passes, including new/updated tests covering the above.
