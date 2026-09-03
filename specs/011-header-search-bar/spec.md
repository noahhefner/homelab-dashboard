# Feature Specification: Header Search Bar

**Feature Branch**: `011-header-search-bar`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "I want to add a search bar to the header of the dashboard with a configurable search engine. The search bar should open a new tab and execute the search query with the configured search engine."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Search the Web from the Dashboard Header (Priority: P1)

As the dashboard owner, I want a search bar in the header so I can quickly look up information without leaving the dashboard or opening a new tab manually. When I type a query and submit, the results should open in a new tab using my preferred search engine.

**Why this priority**: This is the primary and only requested feature. It delivers standalone, immediate value — the owner can perform web searches directly from the dashboard header with one interaction.

**Independent Test**: Can be fully tested by loading any page with the navbar, typing a query into the search bar, submitting it, and confirming a new tab opens with the correct search results URL for the configured engine.

**Acceptance Scenarios**:

1. **Given** the dashboard is loaded and a search engine is configured, **When** the owner types a query into the search bar and presses Enter, **Then** a new browser tab opens with the search results for that query from the configured search engine.
2. **Given** the dashboard is loaded and a search engine is configured, **When** the owner types a query and clicks a search/submit button, **Then** a new browser tab opens with the search results for that query.
3. **Given** the dashboard is loaded and no search engine is configured, **When** the owner types a query and submits it, **Then** the search uses a sensible default engine (Google) and a new tab opens with results.
4. **Given** the owner submits the search bar with an empty query, **When** the form is submitted, **Then** no new tab opens and no error occurs.
5. **Given** the search bar is present on the homepage, **When** the owner views the page, **Then** the search bar is visible in the navbar without requiring any scrolling or interaction.
6. **Given** the search bar is present on the config editor page, **When** the owner views the page, **Then** the search bar is visible in the navbar.
7. **Given** the dashboard is loaded on a mobile-sized viewport, **When** the owner views the page, **Then** the search bar is completely hidden and does not take up any space in the navbar.

---

### Edge Cases

- Empty query on submit: the form should not open a new tab; the search bar should simply retain focus.
- Search engine URL template is missing or invalid in config: fall back to the default search engine (Google).
- Very long query strings: the search bar should handle them gracefully (truncate in the URL or let the browser handle it); no crash or broken layout.
- Browser blocks the new tab (pop-up blocker): the new-tab request should use standard `target="_blank"` behavior; the browser's own pop-up blocker handling applies.
- Config reload while the owner is typing: the search bar should not lose focus or clear the typed query.
- Search engine icon URL is broken or unreachable: the icon should degrade gracefully to the default magnifying-glass icon with no broken image placeholder visible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST display a search input field in the navbar on every page that has a navbar.
- **FR-002**: The search bar MUST be visually integrated into the existing navbar layout (consistent styling, spacing, and alignment with existing navbar elements).
- **FR-003**: The search bar MUST submit the query as a GET request to the configured search engine's URL, with the query as a parameter, and open the results in a new browser tab.
- **FR-004**: The search engine URL template MUST be configurable via the YAML config file as a top-level key (e.g., `search_engine`). The value MUST be a URL string containing a `{query}` placeholder that gets replaced with the URL-encoded search terms.
- **FR-005**: If no `search_engine` key is present in the config, the system MUST default to Google (`https://www.google.com/search?q={query}`).
- **FR-006**: If the configured `search_engine` value is missing the `{query}` placeholder or is otherwise invalid, the system MUST fall back to the default search engine and MUST NOT crash.
- **FR-007**: The search bar MUST support submission via pressing Enter and via clicking a visible search/submit button.
- **FR-008**: The search MUST NOT open a new tab if the query is empty or contains only whitespace.
- **FR-009**: The new tab MUST use `target="_blank"` and `rel="noopener"` for security.
- **FR-010**: The search bar MUST be accessible: it MUST have a visible label or accessible placeholder, and MUST be keyboard-navigable (focusable, submittable via Enter).
- **FR-011**: The search bar MUST be completely hidden on mobile viewports (below the Bootstrap mobile breakpoint) and MUST NOT occupy any space in the navbar at those sizes.
- **FR-012**: The system MUST display a configurable icon to the left of (before) the search input field indicating the configured search engine. The icon MUST be an external image URL specified via a top-level YAML key (`search_engine_icon`).
- **FR-013**: If no `search_engine_icon` is configured, the system MUST display a default magnifying-glass icon (Bootstrap `bi-search` icon) in place of the custom icon.
- **FR-014**: If the configured `search_engine_icon` URL fails to load (broken image), the system MUST fall back to the default magnifying-glass icon and MUST NOT show a broken image placeholder.
- **FR-015**: The search engine icon MUST be completely hidden on mobile viewports along with the rest of the search bar (FR-011).

### Key Entities

- **Search Engine Configuration**: A top-level YAML key (`search_engine`) containing a URL template string with a `{query}` placeholder (e.g., `https://duckduckgo.com/?q={query}`).
- **Search Engine Icon**: A top-level YAML key (`search_engine_icon`) containing an external image URL (e.g., `https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/google.svg`). Falls back to a default magnifying-glass icon when absent or broken.
- **Navbar**: The existing navigation bar present on the homepage and config editor pages, where the search bar will be added.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of non-empty search submissions result in a new tab opening with the correct search engine results URL.
- **SC-002**: 100% of empty/whitespace-only submissions result in no new tab opening.
- **SC-003**: The search bar is visible on first page load on all pages with a navbar, with no extra clicks or navigation required.
- **SC-004**: Configuring a custom search engine (e.g., DuckDuckGo) takes effect on the next page load without code changes.
- **SC-005**: The search bar does not alter the existing navbar layout or break any existing navbar functionality (theme toggle, config link, GitHub link).
- **SC-006**: On mobile viewports, the search bar occupies zero space in the navbar and does not affect the layout of other navbar elements.
- **SC-007**: When a custom search engine icon is configured, the icon loads and displays correctly on first page load on desktop viewports.
- **SC-008**: When no icon is configured or the icon URL is broken, the default magnifying-glass icon is shown with no broken image placeholder.

## Clarifications

### Session 2026-09-03

- Q: What format should the configurable search engine icon use? → A: External image URL (same as tile/bookmark icons)
- Q: Where should the search engine icon be positioned? → A: Before (left of) the search input field

## Assumptions

- The dashboard is a personal, single-owner homelab tool; the search bar does not require authentication or access control.
- The search engine URL template uses a simple `{query}` placeholder pattern (standard for most search engines).
- The search bar will be added to the navbar on all pages that currently have a navbar (homepage and config editor page).
- The default search engine is Google, which is a widely known and reasonable default for a personal tool.
- The existing navbar HTML is duplicated across templates; the search bar will be added to each template independently (consistent with the existing pattern of navbar duplication).
- The search bar is a simple HTML form with `method="GET"` and `target="_blank"` — no JavaScript is required for the core search-and-open behavior.
- The search bar will be positioned within the existing navbar flex layout, between the brand/title and the right-side icon buttons.
