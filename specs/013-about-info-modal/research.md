# Research: About Info Modal

**Feature**: 013-about-info-modal
**Date**: 2026-09-06

## R1: Is the Bootstrap Modal component available without new JS?

**Decision**: Yes — use the standard Bootstrap Modal markup (`data-bs-toggle="modal"`, `data-bs-target="#about-modal"`, `data-bs-dismiss="modal"`) with `modal`, `modal-dialog`, `modal-content`, `modal-header`, `modal-body`, `modal-footer`, and `btn-close` classes. No new JavaScript is written.

**Rationale**: `assets/app.js` already imports `bootstrap/dist/js/bootstrap.bundle.min.js` (line 2), so the Modal component and its `data-*` API ship in every page bundle. The modal is therefore a pure template addition (FR-002, FR-006, FR-011). This satisfies Principle VI (Framework-First Frontend) — the framework's component is the starting point — and Principle V (YAGNI) — zero new dependency or code.

**Alternatives considered**:
- Writing a small custom modal (custom JS + CSS): rejected per Principles V/VI — the framework already provides a tested modal with focus handling, Esc-to-close, backdrop-dismiss, and scroll behavior.
- Using a JS snippet to toggle a hidden div: rejected — reinvents the framework's component and loses built-in accessibility (FR-006/FR-008).

## R2: Button semantics and markup for the About control

**Decision**: Replace the GitHub `<a>` with a `<button type="button" class="btn btn-link nav-link p-1 about-toggle" data-bs-toggle="modal" data-bs-target="#about-modal" aria-label="About">` containing a Bootstrap Icons `bi-info-circle` icon.

**Rationale**: The control does NOT navigate, so a `<button>` is semantically correct (spec FR-001: no navigation, no new tab). The existing navbar icon-button look (used by the theme toggle and the previous GitHub link) is reused via the CSS group — `btn btn-link nav-link p-1` + the same color/size/hover/focus rules. `aria-label="About"` gives the icon its accessible name (FR-008). `bi-info-circle` is the conventional "About" glyph and is already bundled (Bootstrap Icons CSS is imported in `assets/app.css`).

**Alternatives considered**:
- Keeping an `<a href="#">`: rejected — an anchor implies navigation and is misleading for a modal trigger.
- A plain text "About" link: rejected — the navbar uses icon-only controls; an icon keeps the layout consistent.

## R3: Modal content per the user's clarification

**Decision**: The modal body contains, in order: the dashboard title as the modal heading, the author's name ("Noah Hefner"), a short blurb describing the project, a line about where the config file lives, and a footer with a link to the GitHub page.

**Rationale**: The user clarified the content: a GitHub link, the author's name, a blurb about what the project is, and where to put the config file (spec FR-004). The blurb reuses the project description from the README ("A single-page dashboard for your home server..."). The config-guidance text is a static sentence referencing the documented default (`config/example.yaml`, override with `CONFIG_PATH`), drawn from the README's Run sections. The GitHub link (`https://github.com/noahhefner/homelab-dashboard`, unchanged from the removed navbar link) goes in the modal footer with `target="_blank" rel="noopener noreferrer"` (FR-005, security requirements). All content is static — no runtime values rendered (scope containment, Principle V).

**Alternatives considered**:
- Rendering dynamic values (active `CONFIG_PATH`, version, loader state): rejected per YAGNI — the user asked for a general "where to put the config file", not the live path; static text keeps the feature declarative.
- Omitting the footer link and only keeping text: rejected — the user explicitly asked for a link to the GitHub page, and this preserves the removed link's function.

## R4: CSS handling for the renamed control

**Decision**: Rename the `.github-link` selector in `assets/app.css` to `.about-toggle` (it appears in four selector groups: base, `:hover`, dark-mode hover, `:focus-visible`). No new styles.

**Rationale**: The About button is the direct visual successor of the GitHub link (same position in the right-side navbar cluster, same icon-button treatment). The existing color/size/hover/focus rules apply unchanged, so renaming keeps the source of truth single and avoids dead CSS (Principle V: remove dead configuration; Principle II: readable, matching structure). The old `.github-link` class no longer exists in the template after the swap.

**Alternatives considered**:
- Reusing the `.github-link` class name on the new button: rejected — misleading name for an about control (Principle II).
- Duplicating the rules under a new name alongside `.github-link`: rejected — dead CSS (Principle V).

## R5: Scope — which pages get the About button

**Decision**: Homepage navbar only (`app/templates/index.html`). The config editor page (`app/templates/config.html`) is unchanged.

**Rationale**: The GitHub link being replaced exists only in the homepage navbar (verified in the codebase). The spec's assumption is explicit that the config page is out of scope, and its navbar (back + theme toggle) needs no about control. Changing it would exceed the requested scope (Principle V).

**Alternatives considered**:
- Adding the About button to the config page navbar too: rejected — not requested, out of scope.
- Templating a shared modal partial across pages: rejected per YAGNI — only the homepage uses it.

## R6: Security implications

**Decision**: No new security surface. The modal renders only static, first-party text. The single external link (GitHub page) uses `target="_blank" rel="noopener noreferrer"`, consistent with every existing external link in the app. No user- or third-party-controlled content enters the modal.

**Alternatives considered**: none — this is a verification, not a design choice.