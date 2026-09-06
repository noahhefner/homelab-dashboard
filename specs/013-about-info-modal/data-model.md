# Data Model: About Info Modal

**Feature**: 013-about-info-modal
**Date**: 2026-09-06

## Entities

The feature involves no persisted or configurable data. The modal's content is static markup authored in the homepage template. For completeness, the rendered content surface is:

### About Modal Content (static, template-authored)

| Item | Value | Purpose |
|------|-------|---------|
| Heading | "About Homelab Dashboard" | Identifies the dialog (FR-004) |
| Author name | Noah Hefner | Credits the dashboard author (FR-004) |
| Project blurb | "A single-page dashboard for your home server. Renders your tiles and grouped bookmarks from one YAML file, served by a small Flask app inside a single Docker container." | Describes what the project is (FR-004) |
| Config guidance | "Everything is configured in a single YAML file — by default `config/example.yaml`. Set the `CONFIG_PATH` environment variable to use a different file." | Tells the owner where to put the config file (FR-004) |
| GitHub link | `https://github.com/noahhefner/homelab-dashboard` | Opens the project's GitHub page in a new tab (FR-005) |

### About Button (navbar control)

| Attribute | Value | Purpose |
|-----------|-------|---------|
| Element | `<button>` | No navigation — modal trigger only (FR-001) |
| Classes | `btn btn-link nav-link p-1 about-toggle` | Reuses existing navbar icon-button styling |
| `aria-label` | `About` | Accessible name (FR-008) |
| Icon | Bootstrap Icons `bi-info-circle` | Recognizable "About" glyph |

No validation rules, relationships, or state transitions apply — all values are constant static strings.