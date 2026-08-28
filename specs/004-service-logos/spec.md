# Feature Specification: Service Logos

**Feature Branch**: `004-service-logos`

**Created**: 2026-08-28

**Status**: Draft

**Input**: User description: "Add support for logos for the homelab services."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Show a Recognizable Logo for Each Service (Priority: P1)

As the owner, I want each service on my dashboard homepage to display a recognizable logo (e.g., a brand or product mark) instead of only a text monogram, so I can identify services at a glance.

**Why this priority**: The dashboard's core value is a single landing page where every service is immediately identifiable. Logos are the primary visual identifier, building on the existing tile display (feature 001).

**Independent Test**: Can be fully tested by configuring a service with a logo and loading the page, confirming the service tile renders that logo rather than a bare monogram fallback.

**Acceptance Scenarios**:

1. **Given** a service with a logo configured, **When** the homepage renders, **Then** the service tile displays the configured logo.
2. **Given** a service without a logo configured, **When** the homepage renders, **Then** the existing fallback (monogram or default icon) is shown so the tile remains identifiable.
3. **Given** a service whose logo image fails to load, **When** the homepage renders, **Then** a sensible fallback is shown rather than a broken image.

---

### User Story 2 - Configure a Logo Without Writing Code (Priority: P1)

As the owner, I want to assign a logo to a service by editing the YAML config file only, so I can change or add logos without touching application code or rebuilding.

**Why this priority**: Configurability via a single YAML file is a core, explicit requirement of the dashboard (feature 001, US2). Logos must follow the same model.

**Independent Test**: Can be fully tested by adding a logo reference to a service in the YAML config, reloading the page, and confirming the logo appears with no code change or rebuild.

**Acceptance Scenarios**:

1. **Given** a single YAML config, **When** the user adds a logo reference to a service, **Then** after reload the service tile shows that logo.
2. **Given** a YAML config with a logo already assigned, **When** the user removes or changes the logo, **Then** after reload the tile reflects the change (or falls back to the default).
3. **Given** a valid but unrecognized logo reference, **When** the page loads, **Then** the tile still renders with a fallback rather than breaking the page.

---

### User Story 3 - Keep the Repository Free of Large Binary Assets (Priority: P2)

As the developer, I want logos optional and manageable without bloating the repository or requiring me to host images, so the repository stays lean and the config stays simple.

**Why this priority**: Keeping logos lightweight and optional preserves the lean-repository approach established with pnpm-based asset management (feature 003), and avoids forcing users to self-host image files.

**Independent Test**: Can be tested by confirming that adding a logo requires only a reference (not large committed binaries), and that the dashboard still renders cleanly when no logos are configured.

**Acceptance Scenarios**:

1. **Given** the dashboard with logos configured, **When** the repository is inspected, **Then** only lightweight logo definitions (not large binary blobs) are required in version control.
2. **Given** a fresh checkout without logos present, **When** the page loads, **Then** the page still renders styled and usable via the existing fallback.

---

### Edge Cases

- What happens when a logo URL is broken, unreachable, or the wrong format? A fallback (monogram/default icon) must render so the tile stays clear (consistent with feature 001).
- What if a service is configured with a logo value that is not a valid remote image URL (e.g., a plain word)? The system should fall back gracefully (monogram/default) rather than error or break the page.
- What if a user references a remote logo image? Logos are expected to be supplied as remote image URLs only (no bundled or local logo files), matching the existing `icon` behavior; the system must render them and fall back on failure.
- How does the system avoid loading logos that would slow the page (large images, many services)? Reasonable loading behavior (e.g., lazy loading, caching) must keep the page fast (consistent with SC-004 of feature 001).
- What rendered-form safety is needed for a logo path/URL? Any rendered third-party content must be validated/escaped per the Constitution's Security Requirements.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render a logo for each service where one is configured, in place of the default monogram/icon.
- **FR-002**: The system MUST fall back to a sensible default (monogram or default icon) when a service has no logo or the configured logo fails to load.
- **FR-003**: The system MUST allow a logo to be assigned to a service through the YAML configuration file, taking effect on reload with no code change or rebuild.
- **FR-004**: The system MUST accept any valid remote image URL as a service logo, provided through the existing `icon` configuration value (no separate, bundled, or local logo file mechanism is required).
- **FR-005**: The system MUST validate and safely handle any logo URL or rendered reference to prevent injection attacks (per the Security Requirements).
- **FR-006**: The system MUST keep logo loading performant so the page remains responsive with many logo-bearing services.
- **FR-007**: The documentation/config example MUST encourage (but not require) using logos from dashboardicons.com as a convenient source of service logos.

### Key Entities *(include if feature involves data)*

- **Service**: Represents a running service. Its existing `icon` value is the field through which a remote logo image is supplied (in addition to its existing name and URL). No new entity or separate `logo` field is introduced.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of services configured with a logo render that logo when the page loads successfully.
- **SC-002**: 100% of services without a logo (or with a failed logo) render a clear fallback so no tile appears broken or empty.
- **SC-003**: An owner can add, change, or remove a service's logo using only the YAML config, with the change visible after a page reload and no code change or rebuild.
- **SC-004**: The homepage remains fully usable and responsive with logos on all configured services, loading and becoming interactive within the existing performance target (under 2 seconds on a typical home network and standard device).

## Assumptions

- The dashboard already supports an `icon` field per service (remote image URL, else monogram fallback) from feature 001; logos are an evolution of this visual-identity capability.
- Logos are supplied as remote image URLs only — there is no bundled logo library and no local logo file mechanism.
- Service logos are provided by extending the existing `icon` field; no separate `logo` field is introduced.
- Changing or removing a logo must never break the page; a fallback is always required.
- Logos are optional; the dashboard must render correctly with none configured.
- Because logos are remote URLs only, the repository stays free of logo binaries (consistent with the lean-repository approach of feature 003).
- dashboardicons.com is a recommended source of reloadable service logos for convenience but is not a dependency; any valid remote image URL works and the dashboard must not depend on that external site being reachable.
