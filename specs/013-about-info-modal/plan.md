# Implementation Plan: About Info Modal

**Branch**: `013-about-info-modal` | **Date**: 2026-09-06 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/013-about-info-modal/spec.md`

## Summary

Replace the GitHub link in the homepage navbar with an "About" button that opens a Bootstrap modal. The modal shows: the dashboard title, the author's name, a short blurb describing the project, guidance on where the config file lives, and a link to the GitHub page (in a new tab). All styling/interaction uses Bootstrap components already shipped in the bundle (`bootstrap.bundle.min.js` is imported in `assets/app.js`, so the Modal component is available with zero new JS). The button reuses the existing icon-button styling; the previous `.github-link` CSS is repointed to an `.about-toggle` class. Scope is limited to the homepage navbar — the config editor page has no GitHub link and is unchanged.

## Technical Context

**Language/Version**: Python 3.14 (project `requires-python = ">=3.14"`)

**Primary Dependencies**: Flask (web framework), Bootstrap 5.3.8 (CSS + JS, vendored via Vite). `assets/app.js` imports `bootstrap/dist/js/bootstrap.bundle.min.js`, so the Modal component is already bundled and loaded on every page.

**Storage**: None — modal content is static markup in the homepage template; no config/model changes.

**Testing**: pytest (integration via Flask test client + BeautifulSoup, same pattern as `tests/integration/test_navbar.py`)

**Target Platform**: Linux server (self-hosted homelab), browsers on desktop and mobile

**Project Type**: Web application (Flask + Jinja2 templates + static Bootstrap/Vite bundle)

**Performance Goals**: No measurable impact — modal is static HTML toggled by the already-bundled component

**Constraints**: Must use the Bootstrap Modal component and Bootstrap utility classes per Principle VI (Framework-First Frontend). The about button MUST be a `<button>` (not an anchor) since it does not navigate. No custom JavaScript beyond what the bundled Bootstrap JS provides. Adopt `data-bs-theme` for dark-mode compliance (already handled globally by Bootstrap).

**Scale/Scope**: Single-user homelab dashboard; homepage template + one CSS `assets/app.css` change + a new integration test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Developer Experience First | PASS | Static template markup; no build/run-loop friction; tests follow existing patterns |
| II. Readability Over Cleverness | PASS | Standard Bootstrap modal markup; declarative `data-bs-toggle`/`data-bs-dismiss` attributes; no JS |
| III. Extensibility & Modularity | PASS | Self-contained markup in a single template + small CSS class rename; no coupling |
| IV. Testability | PASS | Test-First: integration tests assert modal presence/content/dismissal attributes in rendered HTML |
| V. YAGNI & Simplicity | PASS | Uses the Bootstrap modal already in the bundle — no new dependency, no custom JS |
| VI. Framework-First Frontend | PASS | Bootstrap `modal`/`modal-dialog`/`modal-content` components, `btn-close`, `bi-info-circle` icon; the only CSS change is repointing the existing icon-button style |
| Security Requirements | PASS | No secrets; no user-controlled content rendered in the modal; external GitHub link uses `target="_blank" rel="noopener noreferrer"` |

## Project Structure

### Documentation (this feature)

```text
specs/013-about-info-modal/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
app/
├── templates/
│   └── index.html       # Replace GitHub <a> with About <button data-bs-toggle="modal">
│                        #   data-bs-target="#about-modal">; add about modal markup
assets/
│   └── app.css          # Repoint .github-link styles to .about-toggle
tests/
└── integration/
    └── test_about_modal.py  # NEW: about button + modal content/dismissal tests
```

**Structure Decision**: Flat structure matches existing conventions. The modal lives inline in the homepage template (Jinja partials are not established; YAGNI). CSS changes are limited to renaming the selector group for the old GitHub link to the new About button.

## Complexity Tracking

> No Constitution Check violations. No complexity justifications needed.