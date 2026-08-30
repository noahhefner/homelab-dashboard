# Quickstart / Validation Guide: Navbar & Dark Mode

**Date**: 2026-08-30
**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Validation/run guide for the navbar, configurable title, dark mode, and Bootstrap-icon
dropdown indicators. Details of the config semantics live in
[contracts/navbar-theme-icons.md](contracts/navbar-theme-icons.md) and
[data-model.md](data-model.md); implementation belongs in `tasks.md`, and implementation
details are intentionally omitted here.

## Prerequisites

- The dashboard source; Python 3.14 + `uv` for running tests / the app.
- Node.js (≥18) + pnpm to provision vendor assets. Run `pnpm setup` (= `pnpm install &&
  pnpm provision`) once so both Bootstrap and Bootstrap Icons assets exist for styling and
  icons.

## Running Tests / The App

```bash
pnpm setup               # provisions Bootstrap + Bootstrap Icons static assets
uv run pytest            # contract, unit, integration suites
uv run -m app.server     # with CONFIG_PATH=config/example.yaml
```

## Configuring the Title

The customizable dashboard text is the top-level `title` in the YAML config:

```yaml
title: "My Homelab"
```

- With `title` set, that value (including multi-word) appears in the navbar brand on the
  left.
- If `title` is **omitted, empty, or whitespace-only**, the navbar shows the default
  **"Homelab"** (one word).

## Validation Scenarios

(**Spec**: FR-*, **Scenario**: US*)

### V1 — Custom title renders in the navbar brand (US1, FR-001)

- Set `title: "My Lab"` in the config.
- Load the homepage and confirm the navbar `navbar-brand` on the left shows "My Lab"
  (replacing the old "HOME LAB" heading).

### V2 — Default title when none provided (US1/FR-002, data-model)

- Remove `title` from the config (or set it to an empty string).
- Load the homepage and confirm the navbar brand shows "Homelab" (one word).

### V3 — Navbar structure and toggle placement (US2, FR-003/004/005)

- Load the homepage.
- Confirm a `navbar` spans the top, the title is on the left, and the theme toggle is on
  the right.

### V4 — Dark mode toggles and persists (US3, FR-006/007/008/009)

- Load the homepage; confirm the page renders a sensible default theme (system
  preference, else light).
- Activate the toggle; confirm the theme switches (the `data-bs-theme` attribute changes
  and tiles/bookmarks restyle).
- Reload the page; confirm the chosen theme is preserved.

### V5 — Dropdown uses a Bootstrap icon, not a carat (US4, FR-010)

- Open any bookmark group toggle.
- Confirm its indicator is a Bootstrap icon (e.g., `bi-chevron-down`) and that no literal
  carat (`▾`) character is used.

### V6 — Provisioning includes Bootstrap Icons (feature 003 pattern)

- Run `pnpm setup` on a fresh checkout.
- Confirm `app/static/bootstrap-icons/bootstrap-icons.min.css` and the font files
  exist and are gitignored; confirm `package.json`/`pnpm-lock.yaml` track the pinned
  `bootstrap-icons` dependency.
