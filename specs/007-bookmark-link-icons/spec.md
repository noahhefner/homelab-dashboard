# Feature Specification: Bookmark Link Icons

**Feature Branch**: `007-bookmark-link-icons`

**Created**: 2026-08-30

**Status**: Draft

**Input**: User description: "Add support for icons for the bookmark links just like the icons on the homelab links."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Show an Icon for Each Bookmark (Priority: P1)

As the owner, I want each bookmark in a group to display a recognizable icon (e.g., a brand or product mark) just like the homelab service links do, so I can identify bookmarks at a glance without reading every label.

**Why this priority**: This is the core, explicit requirement. Icons are the primary visual identifier for links, matching the established visual identity of the homelab links. It makes the bookmarks column scannable and consistent with the rest of the dashboard.

**Independent Test**: Can be fully tested by configuring a bookmark with an icon, loading the page, and confirming that bookmark link renders that icon alongside (or in place of) its text label, with no code change or rebuild.

**Acceptance Scenarios**:

1. **Given** a bookmark with an icon configured, **When** the page renders, **Then** the bookmark link displays the configured icon.
2. **Given** a bookmark without an icon configured, **When** the page renders, **Then** the bookmark still shows its text label and remains usable (fallback).
3. **Given** a bookmark whose icon image fails to load, **When** the page renders, **Then** a sensible fallback (the text label) is shown rather than a broken image.

---

### User Story 2 - Configure a Bookmark Icon From the YAML Config (Priority: P1)

As the owner, I want to assign an icon to a bookmark by editing the YAML config file only, so I can add or change icons without touching application code or rebuilding.

**Why this priority**: Configurability via a single YAML file is a core requirement of the dashboard (feature 001) and bookmarks already carry an icon config field. Icons follow the same config-driven model as the homelab links.

**Independent Test**: Can be fully tested by adding or changing a bookmark icon reference in the YAML config, reloading the page, and confirming the bookmark reflects the change with no code change or rebuild.

**Acceptance Scenarios**:

1. **Given** the YAML config, **When** the owner adds an icon to a bookmark, **Then** after reload that bookmark link shows the icon.
2. **Given** a bookmark with an icon already assigned, **When** the owner removes or changes the icon, **Then** after reload the bookmark reflects the change (or falls back to the plain label).
3. **Given** a bookmark with an invalid or unrecognized icon value, **When** the page loads, **Then** the bookmark still renders with a usable fallback rather than breaking the page.

---

### User Story 3 - Consistent Visual Treatment With Homelab Links (Priority: P2)

As the owner, I want bookmark icons to look consistent in size, spacing, and fallback behavior with the homelab link icons, so the dashboard reads as one coherent interface rather than two competing styles.

**Why this priority**: Visual consistency helps the whole dashboard feel cohesive. This is secondary to actually rendering the icon, but it defines how the icon is presented alongside the label in the bookmark list.

**Independent Test**: Can be tested by loading a dashboard where both homelab services and bookmarks have icons and confirming they use the same visual language (similar image scaling/placement and the same text fallback approach).

**Acceptance Scenarios**:

1. **Given** both homelab and bookmark links with icons, **When** the page renders, **Then** both use the same icon presentation conventions.
2. **Given** a bookmark with no icon and a failed image, **When** the page renders, **Then** the bookmark shows its label text clearly without a broken or empty space.

---

### Edge Cases

- Bookmark with no icon configured: render the plain text label as today (fallback), so nothing looks broken.
- Bookmark icon image fails to load (bad URL, unreachable, wrong format): fall back to the plain text label so the link stays usable.
- Bookmark icon value that is not a valid image source: handle gracefully with the text fallback rather than erroring or breaking the page.
- A bookmark icon value that is a short word (e.g., `youtube` or `bank`): this form is unsupported; treat it as a broken/ignored icon that falls back to the plain text label, and it must be removed from the repository in favor of a full URL.
- A group where some bookmarks have icons and some do not: each bookmark renders independently; a missing icon on one must not affect its neighbors.
- Icon loading must not noticeably slow the page when many bookmarks have icons: use reasonable loading behavior (e.g., lazy loading) consistent with the existing performance target.
- Any rendered icon reference must be validated/escaped per the Constitution's Security Requirements to prevent injection.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render an icon for each bookmark where one is configured, alongside its text label.
- **FR-002**: The system MUST fall back to the plain text label when a bookmark has no icon or the configured icon fails to load, so the link remains usable and nothing looks broken.
- **FR-003**: The system MUST allow a bookmark icon to be assigned or changed through the YAML configuration file, taking effect on reload with no code change or rebuild.
- **FR-004**: The system MUST render each bookmark's icon independently; a missing or failed icon on one bookmark MUST NOT affect any other bookmark.
- **FR-005**: The system MUST validate and safely handle any icon reference rendered to the page to prevent injection attacks (per the Security Requirements).
- **FR-006**: The system MUST keep bookmark icon loading performant so the bookmarks column remains responsive with many icon-bearing bookmarks.
- **FR-007**: The system MUST treat only full remote image URLs as a valid bookmark icon; any short-word or otherwise non-URL icon value MUST be handled gracefully (falls back to the plain text label) and MUST NOT render as an image.
- **FR-008**: The repository (including the example config and any documentation) MUST NOT contain short-word bookmark icon values, since that form is unsupported; any such existing values MUST be replaced with full remote image URLs or removed.

### Key Entities *(include if feature involves data)*

- **Bookmark**: A labeled link within a bookmark group. Its existing `icon` value becomes the source of the rendered icon (in addition to its existing `label` and `url`). No new field or entity is introduced.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of bookmarks configured with an icon render that icon on the link when the page loads successfully.
- **SC-002**: 100% of bookmarks without an icon (or with a failed icon) render a clear text label so no link appears broken or empty.
- **SC-003**: An owner can add, change, or remove a bookmark's icon using only the YAML config, with the change visible after a page reload and no code change or rebuild.
- **SC-004**: The bookmarks column loads and becomes interactive within the existing performance target (bookmarks visible / page interactive under 2 seconds on a typical home network and standard device), including with icons on all configured bookmarks.

## Assumptions

- A bookmark icon follows the same treatment as a homelab link icon: a remote image shown next to the label, with the plain text label as the fallback when the image is absent or fails to load.
- Bookmarks already support an `icon` config value (parsed but currently not rendered); this feature renders it, so no new config field is required for the primary case.
- Icons are optional; the bookmarks column must render correctly with none configured.
- A missing or failed icon must never break the page or obscure the label; a text-label fallback is always available.
- A bookmark icon is supplied as a full remote image URL (e.g., from dashboard-icons), matching the homelab link icon treatment. Short-word icon values are NOT a supported icon form anywhere in this project and MUST be removed from the repository; any non-URL icon value falls back to the plain text label.
- The existing example config contains short-word icon values (e.g., `youtube`, `bank`, `play`) that are not supported. This feature MUST replace all such short-word bookmark icon values with full remote image URLs (or remove the icon value where no suitable URL exists), so the repository contains no unsupported short-word icons.
