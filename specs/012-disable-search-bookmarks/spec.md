# Feature Specification: Disable Search and Bookmarks

**Feature Branch**: `012-disable-search-bookmarks`

**Created**: 2026-09-06

**Status**: Draft

**Input**: User description: "Add a new configuration option to disable the search bar and another configuration option to disable the bookmarks. Some users may not want one or both of those."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Disable the Search Bar (Priority: P1)

As the dashboard owner, I want to turn off the header search bar, so my dashboard header shows only what I actually use. When I set the option, the search bar (and its icon) disappears completely from every page and stops taking up navbar space, while everything else stays exactly as it was.

**Why this priority**: This is one of the two explicitly requested capabilities. It delivers standalone value: owners who do not use the header search can reclaim a clean, minimal navbar immediately.

**Independent Test**: Can be fully tested by loading any page with the navbar under two configurations - the default config and one with the search bar disabled - and confirming the search bar renders in the first case and, in the second, is absent with no leftover space or errors.

**Acceptance Scenarios**:

1. **Given** the dashboard config does not change the search bar's default state, **When** the owner loads any page with a navbar, **Then** the search bar is visible exactly as it is today.
2. **Given** the dashboard config disables the search bar, **When** the owner loads the homepage, **Then** no search bar is shown and it occupies zero space in the navbar.
3. **Given** the dashboard config disables the search bar, **When** the owner loads the config editor page, **Then** no search bar is shown in its navbar.
4. **Given** the dashboard config disables the search bar but a custom search engine and icon are still configured, **When** the owner loads the dashboard, **Then** no search bar or search icon is shown and no error occurs.
5. **Given** the search bar is disabled, **When** the owner interacts with the remaining header elements (title, theme toggle, config link), **Then** those elements work exactly as before with available space rebalanced.

---

### User Story 2 - Disable the Bookmarks (Priority: P1)

As the dashboard owner, I want to turn off the bookmarks section, so my dashboard shows only the tiles I use and the freed space is put to work. When I set the option, all bookmark groups disappear, the reserved bookmarks area is removed, and the tiles use the available space.

**Why this priority**: This is the second of the two explicitly requested capabilities. Like the search bar toggle, it is independently valuable for owners who keep their bookmarks elsewhere.

**Independent Test**: Can be fully tested by loading the homepage under two configurations - the default config and one with bookmarks disabled - and confirming the bookmark groups render in the first case and, in the second, no bookmark group is visible and the tiles use the freed space.

**Acceptance Scenarios**:

1. **Given** the dashboard config does not change the bookmarks' default state, **When** the owner loads the homepage, **Then** the bookmark groups are visible exactly as they are today.
2. **Given** the dashboard config disables bookmarks, **When** the owner loads the homepage, **Then** no bookmark group is shown anywhere and no space is reserved for bookmarks.
3. **Given** the dashboard config disables bookmarks, **When** the owner loads the homepage, **Then** the tiles are still shown and use the space formerly occupied by the bookmarks.
4. **Given** the dashboard config disables bookmarks while bookmark groups still have per-group settings (e.g., collapsed state), **When** the owner loads the homepage, **Then** the entire bookmarks section remains hidden and no error occurs.
5. **Given** bookmarks are disabled, **When** the owner keeps the search bar enabled, **Then** the search bar still appears in the navbar exactly as before.

---

### User Story 3 - Disable Both for a Minimal Dashboard (Priority: P2)

As the dashboard owner, I want to disable both the search bar and the bookmarks at the same time, so I get a minimal dashboard showing only my tiles. Configuring both options together must result in a clean, fully functional dashboard with no errors.

**Why this priority**: The two options are intentionally independent, but the combined case proves they compose safely. It is the least common configuration, so it is lower priority than the individual toggles.

**Independent Test**: Can be fully tested by loading the homepage with both options disabled and confirming the page renders with the navbar and tiles, with no search bar, no bookmarks, and no errors.

**Acceptance Scenarios**:

1. **Given** both the search bar and bookmarks are disabled, **When** the owner loads the homepage, **Then** the page renders without errors and shows only the navbar and the tiles.
2. **Given** both options are disabled, **When** the owner loads the config editor page, **Then** it renders normally with its navbar intact and no search bar.

---

### Edge Cases

- **Option omitted**: If the config keys are absent, both features behave exactly as today (search bar and bookmarks shown) - the defaults.
- **Invalid option value**: If an option is set to a value that is not a valid on/off value, the dashboard loads without error and the affected feature falls back to its default (shown).
- **Both options disabled**: The dashboard still renders fully; no blank regions, no errors, and the tiles fill the available space.
- **Config values for hidden features**: Search engine/icon configuration and bookmark group configuration remain in the config file when the corresponding feature is hidden; they are ignored without error.
- **Live reload**: Changing the options in the config takes effect on the next page load without a restart.
- **Hit the theme toggle / config link while a feature is hidden**: All header elements that remain visible continue to work unchanged.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a top-level configuration option that controls whether the header search bar is shown, with "shown" as the default when the option is absent.
- **FR-002**: When the search bar option is set to hide it, the system MUST NOT display the search bar or its icon on any page with a navbar, and the search bar MUST NOT occupy any layout space.
- **FR-003**: When the search bar is hidden, the system MUST ignore any configured search engine and search icon settings without error.
- **FR-004**: The system MUST provide a top-level configuration option that controls whether the bookmarks section is shown, with "shown" as the default when the option is absent.
- **FR-005**: When the bookmarks option is set to hide it, the system MUST NOT display any bookmark group and MUST NOT reserve space for the bookmarks section.
- **FR-006**: When the bookmarks are hidden, the system MUST keep the tiles visible and use the space formerly occupied by the bookmarks for the remaining content.
- **FR-007**: The two options MUST be independent: setting one MUST NOT change the behavior of the other.
- **FR-008**: When both options are set to hide their features, the dashboard MUST still load and function normally (navbar, tiles, and config editor all working).
- **FR-009**: If either option is set to an invalid value, the system MUST fall back to showing the affected feature and MUST NOT crash or fail to load.
- **FR-010**: Changes to either option MUST take effect on the next page load without a restart or any code change.

### Key Entities

- **Search Bar Visibility Setting**: A top-level boolean configuration option that controls whether the navbar search bar is rendered. Present but defaulting to "shown".
- **Bookmarks Visibility Setting**: A top-level boolean configuration option that controls whether the bookmarks section (all bookmark groups) is rendered. Present but defaulting to "shown".
- **Bookmarks Section**: The existing collection of bookmark groups displayed on the dashboard; hidden in its entirety when its visibility setting is off.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: With the search bar option disabled, 100% of page loads render no search bar and no search icon, and the search bar occupies zero layout space.
- **SC-002**: With the bookmarks option disabled, 100% of page loads show zero bookmark groups and reserve zero space for the bookmarks section.
- **SC-003**: With both options disabled, the dashboard loads without errors and displays the remaining content (navbar and tiles) using the available space.
- **SC-004**: With both options in their default state, 100% of page loads render the search bar and bookmarks exactly as they do today.
- **SC-005**: Each option can be toggled independently: a configuration with only the search bar disabled still shows bookmarks, and vice versa.
- **SC-006**: 100% of configurations with invalid values for these options load without error and behave as if the options were at their default (shown).
- **SC-007**: Changing either option takes effect on the next page load, with no restart and no code changes required.

## Assumptions

- "Bookmarks" refers to the bookmark groups section of the dashboard; the tile groups are a separate, unrelated area and are never affected by the bookmarks option.
- The options are top-level boolean settings in the dashboard config, matching the style of existing top-level settings. Suggested key names (e.g., a "show" prefix) will be finalized during planning.
- When the search bar is hidden, its search engine icon is hidden too, since the icon only ever appears as part of the search bar.
- When bookmarks are hidden, the tiles expand to use the freed space rather than leaving a blank area.
- The dashboard already adopts config changes on the next page load without a restart; these options follow the same behavior.
- An invalid value for either option falls back to the default (shown) rather than failing to load, consistent with how the dashboard treats other misconfigured values.