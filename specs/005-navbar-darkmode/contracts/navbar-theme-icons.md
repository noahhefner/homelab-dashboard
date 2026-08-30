# Navbar, Title & Theme Contract

**Date**: 2026-08-30
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

Contract for the configurable dashboard title, the Bootstrap navbar, the toggleable dark
mode, and the Bootstrap-icon dropdown indicators.

## Configurable Title

- The customizable dashboard title is supplied through the existing top-level `title`
  key in the YAML config.
- Resolution:
  - **Non-empty string** (after trimming) → that value is displayed.
  - **Absent / `null` / empty / whitespace-only** → the default **"Homelab"** (one word)
    is displayed (spec FR-002).
- The rendered title MUST be HTML-escaped to prevent injection (spec FR-001 / Security).
- A long title MUST NOT break the navbar layout (graceful wrapping/truncation).

## Navbar

- The top of the page MUST be a Bootstrap `navbar` component using the **`navbar-brand`**
  class for the title (user directive, builds on spec FR-003/FR-004).
- The **title** (the configurable text, or the default "Homelab") MUST appear on the
  **left** side of the navbar.
- The **theme toggle** MUST appear on the **right** side of the navbar.
- The navbar spans the top of the page on all breakpoints.

## Dark Mode & Theme Toggle

- The dashboard MUST support a light theme and a dark theme (spec FR-006).
- Activating the toggle MUST switch between the two themes (spec FR-007).
- The chosen theme MUST persist across page reloads (spec FR-008).
- With no prior choice, a sensible default applies: the system
  `prefers-color-scheme` preference, falling back to light when the system preference is
  absent (spec FR-009).
- Theme switching is client-side only (no page reload, no server state).

## Dropdown Indicator

- Bookmark group toggle indicators MUST be a Bootstrap Icon (e.g.,
  `bi bi-chevron-down`) rather than the literal carat character (spec FR-010).
- The icon SHOULD convey open/closed state (e.g., rotating when the group is collapsed),
  preserving the existing affordance.
- Bootstrap Icons assets are provisioned locally (gitignored) and loaded from the app's
  static assets; the dashboard MUST NOT depend on an external CDN for icons.

## Verification

- With a custom `title` set, the navbar `navbar-brand` shows that value; with no/empty
  title it shows "Homelab".
- The navbar renders with the brand class, title on the left, toggle on the right.
- The page renders the `data-bs-theme` attribute reflecting the theme; toggling changes it
  and persists across reload.
- No literal carat appears for dropdowns; a Bootstrap icon is present instead.
- `uv run pytest` passes, including new/updated tests covering the above.
