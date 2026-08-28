# Feature Specification: Bookmarks Sidebar Layout

**Feature Branch**: `002-bookmarks-sidebar-layout`

**Created**: 2026-08-28

**Status**: Draft

**Input**: User description: "Update the UI of the dashboard so that the bookmarks appear on the right side of the screen instead of below the homelab apps. On mobile, the bookmarks should move to below the homelab app, but on desktop they should be to the right."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See Bookmarks Beside the Apps on Desktop (Priority: P1)

As the owner, when I open the dashboard on a desktop or wide screen, I want the bookmarks to appear in a column on the right side of the screen rather than below the homelab apps, so that both apps and bookmarks are visible at the same time without scrolling.

**Why this priority**: This is the primary requested change—moving bookmarks out of the lower section into a right-hand column for desktop. It directly fulfills the core requirement and delivers the intended desktop layout.

**Independent Test**: Can be fully tested by opening the dashboard in a wide desktop viewport and confirming the bookmarks render in a column on the right side of the screen, with the homelab apps occupying the left/remaining area, rather than appearing below the apps.

**Acceptance Scenarios**:

1. **Given** a desktop/wide browser viewport, **When** the dashboard renders, **Then** the bookmark groups are displayed in a column on the right side of the screen.
2. **Given** a desktop viewport with bookmarks on the right, **When** the user views the page, **Then** the homelab apps remain visible in the main (left/remaining) area without being pushed below the bookmarks.
3. **Given** a desktop viewport, **When** the user clicks a bookmark, **Then** it still opens the correct destination just as it did before the layout change.

---

### User Story 2 - See Bookmarks Below the Apps on Mobile (Priority: P1)

As the owner, when I open the dashboard on a phone or narrow screen, I want the bookmarks to appear below the homelab apps, so the dashboard remains usable on small screens without cramped side-by-side content.

**Why this priority**: Responsive behavior for mobile is an explicit part of the request and builds directly on the base responsive requirement. It is peer-priority to desktop because both are core to the change.

**Independent Test**: Can be fully tested by opening the dashboard on a phone-width viewport and confirming the bookmarks appear below the homelab apps, with no horizontal scrolling and no broken or overlapping layout.

**Acceptance Scenarios**:

1. **Given** a phone-width viewport, **When** the dashboard renders, **Then** the bookmarks appear below the homelab apps rather than to their right.
2. **Given** a mobile viewport, **When** the dashboard renders, **Then** all bookmark groups remain fully reachable and usable with no horizontal scrolling.
3. **Given** a narrow viewport, **When** the user taps a bookmark, **Then** it opens the correct destination without requiring a mouse hover.

---

### User Story 3 - Responsive Reflow Between Breakpoints (Priority: P2)

As the owner, I want the bookmark placement to adapt automatically as I resize the window, so the dashboard always stays legible whether I am on a phone, tablet, or desktop.

**Why this priority**: This ensures the change degrades smoothly across all screen sizes and confirms the desktop/mobile behavior is triggered by the right viewport width. It is lower priority because it formalizes the transition behavior over the two primary placements.

**Independent Test**: Can be fully tested by resizing the browser window continuously from desktop width down to phone width and confirming the bookmarks reflow from a right-side column to a below-the-apps position smoothly, without overlapping or clipped content at any intermediate width.

**Acceptance Scenarios**:

1. **Given** a desktop-width viewport, **When** the user narrows the window past the mobile breakpoint, **Then** the bookmarks move from the right side to below the homelab apps.
2. **Given** a mobile-width viewport, **When** the user widens the window past the desktop breakpoint, **Then** the bookmarks move from below the apps to the right side.
3. **Given** any supported viewport width, **When** the dashboard renders, **Then** no content is clipped, overlapping, or pushed off-screen.

---

### Edge Cases

- How does the right-side bookmark column behave when there are many bookmark groups? The column should scroll or layout gracefully so it does not overflow the viewport or obscure the apps.
- What happens when the viewport falls in a gray area between typical mobile and desktop widths? The layout should reflow at a single, consistent breakpoint and remain usable across the entire range.
- What happens when there are very few or no bookmarks configured? The apps area should simply occupy the full width on desktop with no empty or broken right-side column.
- How does the change interact with existing bookmark collapse/expand behavior? Collapsed groups should remain collapsible and readable in whichever position they render.
- Do external bookmarks still target new tabs/open correctly? Yes, the destination behavior is unchanged by the layout repositioning.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: On desktop/wide viewports, the system MUST render the bookmarks in a column on the right side of the screen rather than below the homelab apps.
- **FR-002**: On desktop/wide viewports, the system MUST render the homelab apps in the main area (left/remaining space) so both apps and bookmarks are visible without scrolling.
- **FR-003**: On mobile/narrow viewports, the system MUST render the bookmarks below the homelab apps rather than to their right.
- **FR-004**: The system MUST switch between the desktop (right-side) and mobile (below-apps) bookmark placements automatically based on the viewport width.
- **FR-005**: The system MUST use a single, consistent breakpoint such that the reflow between desktop and mobile placements is deterministic and does not flicker or produce ambiguous intermediate states.
- **FR-006**: The system MUST preserve all existing bookmark behavior (groups, collapse/expand, opening destinations) in both desktop and mobile placements.
- **FR-007**: The system MUST keep all content reachable and free of horizontal scrolling on mobile/narrow viewports after the repositioning.
- **FR-008**: When no bookmarks are configured, the system MUST render the apps area filling the available width on desktop with no empty or broken right-side column.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a desktop-width viewport, bookmarks are verified to render in a right-side column in 100% of loads, with the apps visible in the main area.
- **SC-002**: On a phone-width viewport, bookmarks are verified to render below the homelab apps in 100% of loads, with no horizontal scrolling.
- **SC-003**: Resizing continuously across the desktop and mobile breakpoints produces a smooth reflow with no overlapping or clipped content at any width.
- **SC-004**: All existing bookmark interactions (open links, collapse/expand groups) continue to work correctly in both desktop and mobile placements with no regressions.

## Assumptions

- The repositioning is a layout/presentation change only; the bookmark data model, configuration, grouping, and link-opening behavior remain unchanged.
- A single viewport-width breakpoint (consistent with existing responsive behavior) separates mobile and desktop placements.
- The existing apps/primary content area remains the focus of the page on desktop, with bookmarks off to the right as a secondary column.
- A right-side column with many bookmarks will rely on natural page scrolling or contained scrolling rather than requiring new pagination.
- This feature does not add, remove, or reorganize any apps, bookmarks, or their configuration; it only changes where bookmarks are placed on screen.
