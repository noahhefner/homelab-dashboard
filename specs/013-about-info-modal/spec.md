# Feature Specification: About Info Modal

**Feature Branch**: `013-about-info-modal`

**Created**: 2026-09-06

**Status**: Draft

**Input**: User description: "Change the github link in the navbar into an about icon that opens a modal with information in it."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Open an About Modal from the Navbar (Priority: P1)

As the dashboard owner, I want the GitHub link in the homepage navbar replaced with an about icon that opens a modal, so I can view information about the dashboard without leaving the page. When I click the about icon, a modal opens on top of the page explaining what the dashboard is.

**Why this priority**: This is the primary requested change. It delivers immediate value — an in-page, non-navigating way to learn about the dashboard — and removes an external link from the primary navigation.

**Independent Test**: Can be fully tested by loading the homepage, clicking the about icon, and confirming a modal opens on top of the current page (URL unchanged, no new tab, no navigation).

**Acceptance Scenarios**:

1. **Given** the homepage is loaded, **When** the owner clicks the about icon in the navbar, **Then** a modal opens on top of the page presenting information about the dashboard.
2. **Given** the homepage is loaded, **When** the owner clicks the about icon, **Then** the current page URL does not change and no new browser tab opens.
3. **Given** the homepage navbar is displayed, **When** the owner views the navbar, **Then** the GitHub link from the previous version is no longer shown there.
4. **Given** the about modal is open, **When** the dashboard owner reads it, **Then** it contains a short description of what the dashboard is.
5. **Given** the about modal is open, **When** the owner wishes to view the project source, **Then** a link to the GitHub page is available inside the modal and opens in a new tab.
6. **Given** the about modal is open, **When** the owner reads it, **Then** it shows the dashboard author's name, a short blurb about what the project is, and guidance on where the config file lives.

---

### User Story 2 - Dismiss the About Modal and Keep it Accessible (Priority: P2)

As a user of the dashboard, I want the about modal to close easily and remain accessible, so I can get back to my dashboard quickly and use it with the keyboard or a screen reader.

**Why this priority**: The modal must not trap the user — dismissal and accessibility are what keep the modal unobtrusive. This is secondary to getting the modal to open with the right content.

**Independent Test**: Can be fully tested by opening the modal and confirming each dismissal method works (close button, clicking the backdrop, pressing Escape), and that the open/close cycle can be repeated without errors.

**Acceptance Scenarios**:

1. **Given** the about modal is open, **When** the owner clicks the close (X) button, **Then** the modal closes and the dashboard is fully usable again.
2. **Given** the about modal is open, **When** the owner clicks outside the modal (the dimmed backdrop), **Then** the modal closes.
3. **Given** the about modal is open, **When** the owner presses the Escape key, **Then** the modal closes.
4. **Given** the about modal is open, **When** the owner opens and closes it repeatedly, **Then** it opens and closes correctly every time with no errors.
5. **Given** the about modal is open on a mobile-sized viewport, **When** the owner interacts with it, **Then** it fits within the viewport and can be scrolled if its content is tall.
6. **Given** the dashboard is in dark mode, **When** the owner opens the about modal, **Then** the modal is legible and consistent with the dark theme.

---

### Edge Cases

- Modal opened repeatedly: each open must show a fresh, correctly positioned modal and never stack duplicate modals.
- Interaction with page behind the modal: the dimmed backdrop must prevent interaction with the underlying page while the modal is open.
- Keyboard focus: when the modal closes, keyboard focus should return to the about icon (or behave sensibly) rather than remaining trapped.
- No Bootstrap/JS failure: if the interactive script fails to load, the page must still render; the about button should not break the navbar.
- Empty/absent description content: the modal must still render with a sensible fallback (e.g., the default dashboard title) and never show a blank dialog.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The navbar on the homepage MUST replace the previous GitHub link with an "about" button/icon that does not navigate or open a new tab.
- **FR-002**: Clicking the about button MUST open a modal on top of the current page.
- **FR-003**: Opening the modal MUST NOT change the current URL and MUST NOT reload or navigate the page.
- **FR-004**: The modal MUST display a heading identifying the dashboard, the dashboard author's name, a short description (blurb) of what the project is, and guidance on where the config file is located.
- **FR-005**: The modal MUST include a link to the project's GitHub page that opens in a new tab with secure handling so the new tab cannot access the dashboard page.
- **FR-006**: The modal MUST be dismissible by an explicit close button, by clicking the dimmed backdrop, and by pressing the Escape key.
- **FR-007**: While the modal is open, the dimmed backdrop MUST prevent interaction with the page behind it.
- **FR-008**: The about button and modal MUST meet basic accessibility requirements: an accessible name for the button, proper dialog labeling, and keyboard operability for opening and closing.
- **FR-009**: The about button and modal MUST render and function correctly in both light and dark themes.
- **FR-010**: The modal MUST fit within the viewport on mobile screens, scrolling internally if the content is taller than the viewport.
- **FR-011**: Repeated open/close cycles MUST work without errors, duplicating modals, or accumulating page state.
- **FR-012**: The change MUST NOT affect any other navbar control (theme toggle, config link, back-to-dashboard link).

### Key Entities

- **About Modal**: A dialog presented on top of the homepage containing a heading, the author's name, a short project blurb, config-file location guidance, and a GitHub link.
- **About Button**: The navbar control that opens the About Modal, replacing the previous GitHub link. Accessible name, e.g., "About".

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of clicks on the about button open the modal without any page navigation or URL change.
- **SC-002**: 100% of dismissal attempts succeed using at least one of the three standard methods (close button, backdrop click, Escape).
- **SC-003**: The GitHub link inside the modal opens in a new tab in 100% of attempts.
- **SC-004**: The navbar shows the about icon instead of the GitHub link on 100% of homepage loads.
- **SC-005**: All existing navbar controls continue to function unchanged (theme toggle, config link) on 100% of page loads.
- **SC-006**: The modal opens and closes correctly across 10 consecutive open/close cycles with no errors or duplicated dialogs.
- **SC-007**: The modal content is legible and fully usable on mobile-size viewports and in dark mode.

## Assumptions

- The about icon replaces the GitHub link only on the homepage navbar; the config editor page's navbar never had a GitHub link and is unchanged.
- The modal content is static text authored in the template: the dashboard title, the author's name, a short one-paragraph blurb describing the project, a note about where the config file lives, and a link to the GitHub page. No runtime- or config-derived data is rendered. The config-location guidance is a static description (see the project's documented mount/`CONFIG_PATH` usage in the README).
- The source-repository link is preserved by moving it *into* the modal, so the ability to reach the project source from the dashboard is not lost by removing the navbar link.
- The dashboard is open source, so a public source-repository link is appropriate to display; the URL is unchanged from the current GitHub link.
- The modal is built with the project's existing frontend styling/interaction framework, consistent with the Framework-First Frontend principle; the plan must verify the framework's modal capabilities are available in the shipped bundle.