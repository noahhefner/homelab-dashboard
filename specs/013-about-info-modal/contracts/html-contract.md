# Contracts: About Info Modal

**Feature**: 013-about-info-modal
**Date**: 2026-09-06

## HTML Contract

### About button (homepage navbar)

```html
<button type="button"
        class="btn btn-link nav-link p-1 about-toggle"
        data-bs-toggle="modal"
        data-bs-target="#about-modal"
        aria-label="About">
    <i class="bi bi-info-circle" aria-hidden="true"></i>
</button>
```

| Rule | Description |
|------|-------------|
| Element | `<button>` (not an anchor) — it must not navigate or open a tab |
| Position | Replaces the previous GitHub link, in the right-side navbar cluster |
| `data-bs-toggle` | `modal` |
| `data-bs-target` | `#about-modal` |
| `aria-label` | `About` (the icon is `aria-hidden`) |
| Styling | Reuses the `.about-toggle` icon-button style (formerly `.github-link`) |

### About modal (homepage)

```html
<div class="modal fade"
     id="about-modal"
     tabindex="-1"
     aria-labelledby="about-modal-title"
     aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-4" id="about-modal-title">About Homelab Dashboard</h1>
                <button type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Built by <strong>Noah Hefner</strong>.</p>
                <p>A single-page dashboard for your home server. Renders your tiles and
                   grouped bookmarks from one YAML file, served by a small Flask app inside
                   a single Docker container.</p>
                <p>Everything is configured in a single YAML file — by default
                   <code>config/example.yaml</code>. Set the <code>CONFIG_PATH</code>
                   environment variable to use a different file.</p>
            </div>
            <div class="modal-footer">
                <a href="https://github.com/noahhefner/homelab-dashboard"
                   class="btn btn-outline-primary"
                   target="_blank"
                   rel="noopener noreferrer">View on GitHub</a>
            </div>
        </div>
    </div>
</div>
```

| Rule | Description |
|------|-------------|
| `id` | `about-modal` (must match `data-bs-target`) |
| `aria-labelledby` | Points to the modal title (`about-modal-title`) |
| `aria-hidden` | `true` (managed by Bootstrap JS) |
| Dialog classes | `modal-dialog-centered modal-dialog-scrollable` — fits mobile viewports and scrolls internally (FR-010) |
| Close button | `btn-close` with `data-bs-dismiss="modal"` (FR-006) |
| Backdrop / Esc | Provided by the Bootstrap Modal component (FR-006/FR-007) |
| GitHub link | `target="_blank" rel="noopener noreferrer"` (FR-005, security) |
| Content | Heading, author name, project blurb, config-file guidance (static, per data-model.md) |

### Contract Rules

| Rule | Description |
|------|-------------|
| No GitHub `<a>` remains in the homepage navbar outside the modal | `bi-github` icon and `github-link` class are removed from `index.html` |
| The modal is present only on the homepage | The config editor page navbar is unchanged |
| Interaction does not navigate | Opening the modal must not change the URL (FR-003) |
| Dismissal | Close button, backdrop click, and Esc all close the modal (FR-006) |
| Backdrop | While open, the page behind is non-interactive (FR-007) |
| Dark mode | Modal inherits `data-bs-theme` styling — contrast is Bootstrap-managed (FR-009) |

## Contract Tests (backing the HTML contract)

Covered by `tests/integration/test_about_modal.py` additions:
- Homepage contains the about button (`button[data-bs-toggle="modal"][data-bs-target="#about-modal"]` with `aria-label="About"`).
- No `a.github-link` / `bi-github` anchor remains in the homepage navbar.
- The modal markup exists with the title, author name, project blurb, config-guidance text, and a GitHub link (`rel="noopener noreferrer"`).
- The about button is a `<button>`, not an anchor (no href).
- The config editor page is unchanged (no about button/modal present).