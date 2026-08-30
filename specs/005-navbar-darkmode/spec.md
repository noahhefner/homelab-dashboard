# Feature Specification: Navbar & Dark Mode

**Feature Branch**: `005-navbar-darkmode`

**Created**: 2026-08-30

**Status**: Draft

**Input**: User description: "Make the following UI Updates: 1) Replace the HOME LAB text at the top of the dashboard with a bit of customizable text. The text should be configurable from the config file. (If no text is provided, set it as Homelab, one word). 2) Add a navbar to the top of the page and put the Homelab text in it on the left side. 3) Add support for dark mode and make it toggleable. The toggle should be in the navbar on the right side. 4) I don't like the carat for the dropdowns. Replace that with bootstrap icons."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Customizable Dashboard Title (Priority: P1)

As the owner, I want to replace the fixed "HOME LAB" heading at the top of the page with a title I can set in the config file, so I can personalize the dashboard's name.

**Why this priority**: The page title is the most visible branding element. Making it configurable is a small change that directly serves the owner's identity for the dashboard, and it is a prerequisite for placing the title in the new navbar.

**Independent Test**: Can be fully tested by setting a title in the config, reloading the page, and confirming the new title appears where the old "HOME LAB" text did.

**Acceptance Scenarios**:

1. **Given** the config includes a custom title, **When** the page loads, **Then** that custom title is displayed at the top of the dashboard in place of the old "HOME LAB" text.
2. **Given** the config includes no title, **When** the page loads, **Then** the default title "Homelab" (one word) is displayed.
3. **Given** the config title is changed, **When** the page is reloaded, **Then** the displayed title reflects the change with no code change or rebuild.

---

### User Story 2 - Persistent Navbar with Title and Theme Toggle (Priority: P1)

As the owner, I want a navigation bar at the top of the page containing the dashboard title on the left and a dark-mode toggle on the right, so I always have clear branding and quick access to switching themes.

**Why this priority**: The navbar is the structural change that hosts both the customizable title (US1) and the dark-mode toggle (US3). It frames the whole UI and is required for the other updates to be placed sensibly.

**Independent Test**: Can be fully tested by loading the page and confirming a navbar spans the top, with the title on the left and the theme toggle visible on the right.

**Acceptance Scenarios**:

1. **Given** the page loads, **Then** a navbar is displayed across the top of the page.
2. **Given** the page loads, **Then** the dashboard title appears on the left side of the navbar.
3. **Given** the page loads, **Then** a visible, easily reachable theme toggle appears on the right side of the navbar.

---

### User Story 3 - Toggleable Dark Mode (Priority: P1)

As the owner, I want to switch the dashboard between light and dark themes using a toggle, so I can view the dashboard comfortably in different lighting conditions.

**Why this priority**: Dark mode is a core quality-of-life feature driven by a clearly stated toggle in the navbar, affecting the entire look of the dashboard.

**Independent Test**: Can be fully tested by clicking the toggle, confirming the theme switches between light and dark, and confirming the choice is retained when navigating or reloading the page.

**Acceptance Scenarios**:

1. **Given** the dashboard in light mode, **When** the user activates the toggle, **Then** the dashboard switches to dark mode.
2. **Given** the dashboard in dark mode, **When** the user activates the toggle, **Then** the dashboard switches back to light mode.
3. **Given** the user has chosen a theme, **When** the page is reloaded, **Then** the chosen theme is preserved rather than reset.
4. **Given** a user has not yet made a choice, **When** the page loads, **Then** a sensible default theme is shown.

---

### User Story 4 - Replace Dropdown Carats with Bootstrap Icons (Priority: P3)

As the owner, I want the dropdown indicators (currently carat/chevron symbols) replaced with the standard Bootstrap icons, so the UI looks consistent with the Bootstrap-based styling.

**Why this priority**: This is a cosmetic consistency improvement. It does not affect behavior of the dropdowns and can be shipped independently without blocking the other updates.

**Independent Test**: Can be fully tested by opening any dropdown and confirming its indicator is rendered using the Bootstrap icon set rather than the previous carat character.

**Acceptance Scenarios**:

1. **Given** any dropdown on the page, **When** it is displayed, **Then** its indicator is rendered as a Bootstrap icon.
2. **Given** the dropdown is open or closed, **When** the indicator state changes, **Then** an appropriate Bootstrap icon reflects the state.

---

### Edge Cases

- What happens when the config title is empty, whitespace-only, or missing? The default "Homelab" must be shown.
- What happens when the config title is a very long string? The navbar title should remain readable and not break the layout (truncated or wrapped gracefully).
- Does the theme choice persist across reloads? Yes — the user's selection must be retained, with a sensible default when no choice has been made.
- What if the user's browser has a system-level dark-mode preference? The dashboard should respect a sensible default that does not surprise the user.
- If Bootstrap icon assets are unavailable or fail to load, the dropdowns must still function and remain discoverable (fallback without breaking the page).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render a page title that is configurable through the config file, replacing the current fixed "HOME LAB" heading.
- **FR-002**: When no configurable title is provided, the system MUST display the default "Homelab" (one word).
- **FR-003**: The system MUST display a navigation bar (navbar) across the top of the page at all times.
- **FR-004**: The navbar MUST display the configurable title on its left side.
- **FR-005**: The navbar MUST display a theme toggle on its right side.
- **FR-006**: The system MUST support at least two themes: a light theme and a dark theme.
- **FR-007**: The theme toggle MUST switch the dashboard between the light and dark themes on user activation.
- **FR-008**: The system MUST preserve the user's chosen theme across page reloads.
- **FR-009**: When the user has not yet chosen a theme, the system MUST apply a sensible default.
- **FR-010**: The system MUST render dropdown indicators using Bootstrap icons instead of the previous carat/chevron character.

### Key Entities *(include if feature involves data)*

- **Dashboard title**: The user-facing name of the dashboard, provided in the config file with a defined default of "Homelab".
- **Theme preference**: The user's choice of light or dark theme, retained so it persists across page reloads.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of page loads display the configurable title where the old "HOME LAB" text appeared, using the default "Homelab" when none is set.
- **SC-002**: 100% of page loads display a navbar spanning the top, with the title on the left and the theme toggle on the right.
- **SC-003**: A user can switch between light and dark themes with a single activation of the toggle, and the choice persists across reloads.
- **SC-004**: 100% of dropdown indicators render as Bootstrap icons, with no functional change to how dropdowns open and close.

## Assumptions

- A single top-level config field (building on the existing `title` value in the config file) is the mechanism for the customizable dashboard title; an empty or missing value yields the default "Homelab".
- Dark mode applies to the entire page (all existing sections, including services and bookmark groups), not just a subset.
- The theme toggle is a client-side setting; no user accounts or per-user server-side persistence are introduced.
- Default theme: respects the user's operating-system/browser preference, falling back to light when no system preference exists.
- The Bootstrap icon library (already part of the project's Bootstrap-based styling) is used for dropdown indicators; no new icon dependency is required.
- Existing dropdown behavior and content are unchanged; only the visual indicator is replaced.
