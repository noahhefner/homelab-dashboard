# Feature Specification: Tile Link Groups (Services Rebranded as "Tiles")

**Feature Branch**: `009-service-link-groups`

**Created**: 2026-08-31

**Status**: Draft

**Input**: User description: "Add the ability to split the service links into groups. Each group should have a header with the name of the group. There's no collapsing or uncollapsing the service groups like the bookmarks. They should always be visible. Also add a header above the bookmark accordion that just says 'Bookmarks' (hardcoded, not configurable). Also, rebrand the services section as 'Tiles' — comb through the entire repository and update verbiage referring to services to 'tiles'."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Use the Flat "Tiles" List (Priority: P1)

As the owner, I want to list my links in a single flat `tiles` list, so the simplest kind of dashboard — a plain row of tiles with no grouping — is supported.

**Why this priority**: The flat list is the simplest valid configuration form and remains the foundation of the feature. As part of the rebrand (Clarification Q1 → A), the former `services` key is renamed to `tiles`; existing configs must be updated to use the new key.

**Independent Test**: Can be fully tested by writing a config that uses a flat `tiles` list and confirming all tiles render as app tiles in the main area, with no group headers and no errors.

**Acceptance Scenarios**:

1. **Given** a config that defines links in a single flat `tiles` list, **When** the dashboard loads, **Then** all tiles render as app tiles in the main area.
2. **Given** a flat `tiles` list with no group declarations, **When** the dashboard renders, **Then** no group headers or grouping behavior is introduced.
3. **Given** a config still using the legacy `services` key, **When** the dashboard loads, **Then** the key is not recognized as tiles (the legacy key is not supported, per Clarification Q1 → A).

---

### User Story 2 - Organize Tiles Into Named Groups With Always-Visible Headers (Priority: P1)

As the owner, I want to organize my links into named groups, each with a header showing the group name, so I can segment my tiles (for example, Media, Networking, Storage) instead of one long flat list.

**Why this priority**: This is the core, explicit requirement. Grouping tiles by name with visible headers directly delivers the requested organization. Unlike bookmark groups, tile groups are never collapsible — every group and every tile is always visible.

**Independent Test**: Can be fully tested by writing a config that places tiles into two or more named groups and confirming the dashboard renders each group as a distinct, labeled section of tiles, with every group visible and no collapse/expand control.

**Acceptance Scenarios**:

1. **Given** a config that groups links under named group sections, **When** the dashboard loads, **Then** each group renders as its own labeled section of tiles, with a header showing the group name.
2. **Given** a config with multiple named tile groups, **When** the page renders, **Then** each tile appears only within its own group and not elsewhere.
3. **Given** a config where groups appear in a defined order, **When** the page renders, **Then** the groups appear in the order they are declared in the config.
4. **Given** grouped tiles on a desktop viewport, **When** the page renders, **Then** every tile group and all of its tiles are visible without any collapsing, expanding, or toggling interaction.

---

### User Story 3 - Set an Icon for Each Tile Group (Priority: P2)

As the owner, I want to optionally set an icon for a tile group, so group headers are visually distinguishable and consistent with the existing bookmark group behavior.

**Why this priority**: An optional group icon improves scannability and matches the established pattern for bookmark groups. It is secondary to the grouping capability itself.

**Independent Test**: Can be fully tested by giving a tile group an icon in the config and confirming the icon renders next to the group's name, while groups without an icon render the name alone.

**Acceptance Scenarios**:

1. **Given** a tile group configured with an icon, **When** the page renders, **Then** the icon is displayed beside the group name.
2. **Given** a tile group without an icon configured, **When** the page renders, **Then** the group header shows the name without a broken or empty icon element.

---

### User Story 4 - Move Between Flat and Grouped Layouts Effortlessly (Priority: P2)

As the owner, I want to be able to switch a tile between being grouped and ungrouped, or move it between groups, by editing the config text, so I can reorganize my layout over time as my home lab grows.

**Why this priority**: Reorganization is the natural follow-on to grouping. It makes the config a real organizing tool rather than a one-time setup, and it exercises the config loader and validation.

**Independent Test**: Can be fully tested by moving a tile from one group to another (or to no group) in the config file and confirming, on reload, that the tile renders in its new location.

**Acceptance Scenarios**:

1. **Given** a tile currently in one named group, **When** I move it to a different group in the config, **Then** on reload the tile renders in the new group.
2. **Given** a grouped tile, **When** I move it out of any group (into the flat list), **Then** on reload it renders in the ungrouped area.
3. **Given** a tile group is renamed in the config, **When** the page reloads, **Then** the group header shows the new name and its tiles are unchanged.

---

### User Story 5 - See a "Bookmarks" Header Above the Bookmark Accordion (Priority: P1)

As the owner, I want a header that reads "Bookmarks" to appear above the bookmark accordion, so the bookmarks section is clearly labeled.

**Why this priority**: This is an explicit, small requirement that labels an unlabeled section. It is fixed/hardcoded and does not depend on the config.

**Independent Test**: Can be fully tested by loading the dashboard and confirming the text "Bookmarks" renders as a heading immediately above the bookmark accordion, regardless of configuration.

**Acceptance Scenarios**:

1. **Given** the dashboard renders with bookmark groups, **When** I view the page, **Then** a heading reading "Bookmarks" appears directly above the bookmark accordion.
2. **Given** the heading is present, **When** I change any config setting, **Then** the heading still reads "Bookmarks" (it is hardcoded and not configurable).

---

### User Story 6 - Rebrand Everything as "Tiles" (Internal and User-Facing) (Priority: P1)

As the owner, I want everything formerly referred to as "services" to be renamed to "tiles" throughout the entire repository — internal code, config keys, CSS classes, tests, documentation, and user-facing labels — so the terminology is fully consistent everywhere.

**Why this priority**: This is an explicit rebranding requirement that affects every facet of the repository, not just visible text. The user wants no "services" terminology remaining anywhere in the codebase.

**Independent Test**: Can be fully tested by searching the entire repository for "services" (case-insensitive, excluding the git history and the "National Benefits Services" bookmark label) and confirming no applicable reference remains — every config key, identifier, class, label, and doc now uses "tiles".

**Acceptance Scenarios**:

1. **Given** the dashboard's main content section (formerly services), **When** it is labeled or referenced (in code, config, or UI), **Then** it is called "Tiles".
2. **Given** the repository's documentation, configuration examples, and code identifiers, **When** they reference the section formerly known as services, **Then** they use "tiles" terminology exclusively.
3. **Given** a repository-wide search for the string "services", **When** performed over source/config/docs (excluding git history), **Then** no applicable reference to the former services section remains using "services"; the term "tiles" is used consistently.

---

### User Story 7 - Use Tiles for Both Homelab and External Services (Priority: P2)

As the owner, I want the dashboard's documentation and example config to make clear that a tile can link to either an internal homelab service or an external service (e.g., an email provider's webmail, a cloud account portal, a SaaS admin console), so the naming "tiles" is understood as a general-purpose link, not only homelab services.

**Why this priority**: This is a positioning/documentation clarification that broadens what a tile represents. It does not change the underlying mechanics (any `http(s)` URL in a tile already works) but informs how the feature is described and exemplified.

**Independent Test**: Can be fully tested by reviewing the README and example config comments: they must present tiles as links to both internal homelab services and external services, with at least one example of each kind.

**Acceptance Scenarios**:

1. **Given** the README or example config documents tiles, **When** the owner reads it, **Then** it states/illustrates that tiles can point to both internal homelab services and external services (e.g., webmail, cloud portals).
2. **Given** a tile configured with an external `http(s)` URL (e.g., an email provider), **When** the homepage renders and the tile is clicked, **Then** it opens the external destination in a new tab exactly like any other tile.

---

### Edge Cases

- What happens when a config mixes grouped and ungrouped tiles in the same file? Grouped tiles render in their groups, and any ungrouped tiles render in a default/unnamed area without error.
- What happens when a tile group is empty? The group should render gracefully without errors (an empty labeled section, or omitted) rather than breaking the page.
- What happens when a group is missing a required field (name)? The config should be rejected with a clear, specific validation error rather than silently producing a broken group.
- What happens if the same tile name appears in more than one group? Each is treated as an independent entry and rendered where configured; no deduplication is required.
- How does grouping interact with the live-reload and in-browser editor features? Grouped config must validate and reload the same way flat config does today.
- Tile groups have no collapse/expand: there must never be a collapse/expand control or persisted open/closed state for tile groups (unlike bookmark groups).
- The "Bookmarks" header must remain fixed regardless of whether any bookmark groups are configured (show it when the accordion is present; behavior with zero groups confirmed in planning).
- Tiles may point to either internal homelab services or external services (e.g., an email provider's webmail, a cloud account portal, a SaaS admin console). A tile's URL may be any valid `http(s)` address; it is opened in a new tab regardless of target.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST rename the flat config key and all related identifiers from "services" to "tiles" throughout the repository, replacing the previous `services`/`service_groups` keys with `tiles`/`tile_groups`. [Clarification Q1 → A: breaking change; the legacy `services` key is NOT supported.]
- **FR-002**: The system MUST allow tiles to be organized into one or more named groups within the config.
- **FR-003**: The system MUST render each named tile group as its own labeled section of tiles, in the order the groups are declared in the config.
- **FR-004**: The system MUST render each tile only within the group (or flat section) where it is configured.
- **FR-005**: The system MUST allow a tile group to have an optional icon, rendered beside the group name when present.
- **FR-006**: When a config contains both grouped and ungrouped tiles, the system MUST render grouped tiles in their named sections and the ungrouped tiles in a default/unnamed section, without error.
- **FR-007**: The system MUST validate tile-group configuration (e.g., a missing required group name, or a non-list structure) and report clear, specific errors.
- **FR-008**: Changing group membership, names, or icons in the config MUST take effect on reload without a code change or rebuild (consistent with existing live-reload behavior).
- **FR-009**: Grouped and ungrouped tile configuration MUST be editable through the in-browser config editor and pass the same validation as edited flat config.
- **FR-010**: Each tile group MUST render a visible header displaying the group name; there MUST be no collapse/expand control and no persisted open/closed state for tile groups — they are always visible.
- **FR-011**: The system MUST render a fixed, hardcoded header reading "Bookmarks" directly above the bookmark accordion; it MUST NOT be configurable.
- **FR-012**: The system MUST rebrand the former "services" section and all related terminology to "Tiles" across EVERY facet of the repository — config keys, internal identifiers, CSS classes, tests, documentation, and user-facing labels — so no applicable "services" reference remains.
- **FR-013**: Documentation and the example config MUST present a tile as usable for both internal homelab services and external services (e.g., an email provider, a cloud account portal), with at least one example of each kind; any valid `http(s)` tile URL opens in a new tab regardless of whether its target is internal or external.

### Key Entities *(include if feature involves data)*

- **Tile** (formerly "Service"): A clickable tile (name, URL, optional icon) that opens a target in a new tab. A tile may point to an internal homelab service OR an external service (e.g., an email provider, a cloud account portal, a SaaS admin console). Currently exists in a flat list; gains the ability to be organized into a group.
- **TileGroup** (formerly "ServiceGroup"): A named collection of tiles (name, optional icon, and the list of tiles it contains), mirroring the existing `BookmarkGroup` pattern, that controls how tiles are grouped and displayed. Tile groups are always visible (no collapse).
- **DashboardConfig**: The top-level config that will now hold a grouped structure for tiles (or a flat `tiles` list); the former `services`/`service_groups` keys are renamed to `tiles`/`tile_groups`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A config using the new flat `tiles` list loads and renders all tiles in the main area with no regrouping and no errors.
- **SC-002**: A config with two or more named tile groups renders each group as its own correctly labeled section (with a visible header), with every tile appearing only where configured, in declared order, and every group/tile fully visible (no collapse).
- **SC-003**: An owner can organize, reorganize, group, and ungroup tiles purely by editing the config text, with changes taking effect on reload with no rebuild or restart in 100% of valid edits.
- **SC-004**: 100% of malformed group configurations (e.g., missing group name or invalid structure) produce a clear, specific validation error rather than a broken or blank page.
- **SC-005**: The text "Bookmarks" renders as a header above the bookmark accordion on 100% of page loads; it is hardcoded and unaffected by any configuration.
- **SC-006**: After the rebrand, a repository-wide review (source, config, CSS, tests, docs; excluding git history) confirms no applicable "services" reference remains for the former services feature, and every config key, identifier, class, label, and doc uses "tiles" consistently.
- **SC-007**: Documentation and the example config convey that a tile can link to either an internal homelab service or an external service (e.g., webmail, cloud account portals), using examples of both kinds.

## Assumptions

- Grouping tiles is a configuration and rendering change only; the destination, opening-in-new-tab, icon, and monogram behaviors of individual tiles are unchanged.
- Tile grouping reflects the existing `bookmark_groups` pattern (a named group with an optional icon), for consistency and ease of maintenance — **except** that tile groups are never collapsible (no collapse/expand and no saved open/closed state).
- The rebrand is a **breaking change**: the former `services`/`service_groups` config keys are renamed to `tiles`/`tile_groups`, and the legacy keys are NOT supported (Clarification Q1 → A). Existing configs must be updated by the owner.
- The rebrand applies to **every facet** of the repository (internal and user-facing): config keys, Python identifiers/classes, CSS class names, tests, documentation, example config, and user-facing labels. The only "services" text that may remain is unrelated content (e.g., a bookmark label such as "National Benefits Services") and references in git history.
- Tiles may point to either internal homelab services or external services (e.g., email providers, cloud account portals); a tile URL is any valid `http(s)` address opened in a new tab.
- The exact config syntax for grouped tiles (e.g., whether grouped tiles are declared as a nested list under a `tile_groups` key, matching the flat `tiles` key) is a design/planning decision and is intentionally left to the planning phase.
- Ungrouped tiles, when grouped tile sections exist, appear in a default/unnamed section at a consistent location (e.g., top or after all groups — to be confirmed in planning).
- No browser-driver checkbox, drag-and-drop, or in-page reordering is required; organization is done through the config text, consistent with how all dashboard layout is configured today.
- The "Bookmarks" header is hardcoded in the UI and is not configurable.

## Clarifications

### Session 2026-08-31

- Q: Should the service→tile rebrand include renaming the public YAML config key (currently `services`), and should the old key still be accepted for backward compatibility? → A: Option A — rename `services`→`tiles` (and `service_groups`→`tile_groups`) everywhere in the repository, internal and user-facing. This is a breaking change: the legacy `services`/`service_groups` keys are NOT supported and existing configs must be updated (reflected in FR-001, FR-012, US1, US6, Assumptions).
