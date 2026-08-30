# Feature Specification: Bookmark Group Default State

**Feature Branch**: `006-bookmark-group-default-state`

**Created**: 2026-08-30

**Status**: Draft

**Input**: User description: "Add a configuration option for bookmark groups to have them open or closed when the page loads. Should be configurable on a per-group basis."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configure a Group's Initial State (Priority: P1)

As the owner, I want to set whether each bookmark group is shown open or collapsed when the page loads, so I can control how much of the page is visible on first view without having to open or close groups every visit.

**Why this priority**: This is the core, explicit requirement. Per-group control over the initial open/closed state directly shapes the first impression and usefulness of the bookmarks sidebar. It is a small config-driven change with no dependencies on other features.

**Independent Test**: Can be fully tested by configuring a group to be closed (and another open) in the YAML config, loading the page, and confirming each group renders in its configured state with no code change or rebuild.

**Acceptance Scenarios**:

1. **Given** a bookmark group configured as closed, **When** the page loads (and no prior user preference exists), **Then** the group is displayed collapsed.
2. **Given** a bookmark group configured as open, **When** the page loads (and no prior user preference exists), **Then** the group is displayed expanded.
3. **Given** a group with no state configured, **When** the page loads (and no prior user preference exists), **Then** the group is displayed expanded (the existing default).
4. **Given** the state is changed in the config, **When** the page is reloaded (and no prior user preference exists), **Then** the group honors the new configured state.

---

### User Story 2 - Honor a User's Explicit Resizing Choice (Priority: P2)

As the owner, I want the state I deliberately set by opening or closing a group during a visit to be remembered, so my manual adjustments persist across visits.

**Why this priority**: The dashboard already remembers per-group collapse state across visits. The config must establish the default without fighting a user's explicit in-session choice, preserving that existing persisted behavior.

**Independent Test**: Can be tested by configuring a group as open, collapsing it during a visit, then reloading — the group should remain collapsed (the user's choice wins over the config default).

**Acceptance Scenarios**:

1. **Given** a group configured as open, **When** the user collapses it during a visit, **Then** on reload the group remains collapsed (persisted user choice takes precedence over the config default).
2. **Given** a group configured as closed, **When** the user expands it during a visit, **Then** on reload the group remains expanded.

---

### Edge Cases

- Group with no state configured: default to the existing behavior (open).
- A user has a previously persisted choice for a group: that choice takes precedence over any config default, so changing the config default does not override the user's explicit in-session action.
- Multiple groups: each group's state is configured independently; groups must not affect each other.
- A non-boolean or invalid value in config: handled gracefully (validation rejects or treats it as the default), never breaking the page.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow each bookmark group to be configured as open or closed for the initial page load, on a per-group basis.
- **FR-002**: When a group has no initial-state configured, the system MUST default it to open (expanded), preserving the existing behavior.
- **FR-003**: The system MUST respect the per-group configured initial state when the page first renders for a user with no previously saved choice for that group.
- **FR-004**: When a user has a previously saved open/closed choice for a group, the system MUST honor that saved choice rather than the config-derived default.
- **FR-005**: The state of one group MUST be independent of the state of other groups.
- **FR-006**: Changing the config-derived default MUST take effect on reload without a code change or rebuild, applied only to groups with no saved user choice.

### Key Entities *(include if feature involves data)*

- **BookmarkGroup**: A named collection of bookmarks. Gains an optional per-group initial-state setting (e.g., "collapsed" vs. "open") that controls its state on first page load, alongside the group's existing `name`, `icon`, and `bookmarks`.
- **Saved group state**: Each group's user-picked open/closed state, remembered across visits; takes precedence over the config default.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of groups with an explicit closed setting render collapsed on first load; 100% with an open setting (or no setting) render expanded, for a user with no saved choices.
- **SC-002**: A user can set any mix of open/closed groups per group, and each is rendered exactly as configured (independent of the others).
- **SC-003**: 100% of groups with a previously saved user choice keep that choice across reloads, regardless of the config default.
- **SC-004**: Changing any group's config-derived default is reflected after a page reload with no rebuild or restart.

## Assumptions

- The per-group initial state is expressed as a simple boolean-style config value (open vs. closed), applied independently to each group.
- The existing saved per-group user choice (from the current bookmark collapse behavior) takes precedence over the config default, so the config only establishes the initial state for groups with no saved user choice.
- Configuring a group as closed makes it collapsed on page load; configuring it as open (or leaving it unset) makes it expanded.
- All groups remain individually collapsible/expandable by the user after load; the config controls only the initial state.
- No new database or server-side persistence is introduced; the existing client-side saved state mechanism continues to be used.
