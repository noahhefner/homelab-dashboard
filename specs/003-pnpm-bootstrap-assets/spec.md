# Feature Specification: pnpm Bootstrap Assets

**Feature Branch**: `003-pnpm-bootstrap-assets`

**Created**: 2026-08-28

**Status**: Draft

**Input**: User description: "I want to use pnpm to facilitate the download process for the bootstrap assets. Not for a build tool or anything, but simply for tracking package versions and providing an easy mechanism for updating bootstrap assets. That way i can avoid commiting the assets to source control."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Provision Bootstrap Assets on a Fresh Checkout (Priority: P1)

As a developer setting up the dashboard on a new machine, I want to run a single simple command to fetch the pinned Bootstrap CSS and JS from a package registry and place them into the dashboard's static assets, so I get a working, correctly-styled page without manually downloading files or committing the assets to version control.

**Why this priority**: This is the core ask—replacing committed vendored assets with a registry-tracked mechanism. Without it there is no working offline-styled page on a new checkout.

**Independent Test**: Can be fully tested by starting from the repository as committed (with Bootstrap assets absent from version control), running the provisioning command, and confirming the Bootstrap CSS and JS exist in the static assets directory and the page renders using them.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repository without any Bootstrap asset files present, **When** the developer runs the provisioning command, **Then** the Bootstrap CSS and JS files appear in the intended static assets directory.
2. **Given** provisioning has completed, **When** the dashboard homepage loads, **Then** it is styled with Bootstrap exactly as before (no visual or functional regression).
3. **Given** a fresh checkout, **When** the developer inspects the version control status, **Then** no downloaded Bootstrap asset files are tracked or shown as changes (they are excluded from source control).

---

### User Story 2 - Track and Update the Bootstrap Version (Priority: P1)

As a developer, I want the Bootstrap version the dashboard uses to be recorded declaratively (not embedded in copied files), so I can see the pinned version at a glance and update to a new version through a simple, repeatable action.

**Why this priority**: Version tracking and easy updating are the explicit reasons for adopting a package manager here. This is peer-priority to provisioning because both are core to the request.

**Independent Test**: Can be fully tested by checking that the file which records the dependency clearly states the Bootstrap version, then bumping that version and re-running the provisioning command to confirm the refreshed assets reflect the new version.

**Acceptance Scenarios**:

1. **Given** the dependency record, **When** a developer reads it, **Then** it clearly indicates the pinned Bootstrap version being used.
2. **Given** a newer Bootstrap version is available, **When** the developer updates the recorded version and re-runs provisioning, **Then** the static assets are replaced with the newer version's files.
3. **Given** provisioning runs after a version change, **When** the page loads, **Then** it consistently uses the newly provisioned Bootstrap version.

---

### User Story 3 - Keep the Repository Clean of Asset Files (Priority: P2)

As a developer, I want the downloaded Bootstrap asset files to stay out of version control, so the repository stays lean and the package registry remains the single source of truth for those assets.

**Why this priority**: Keeping assets uncommitted is the stated motivation behind the request; it reduces repository weight and avoids binary/file churn. It is secondary only because provisioning must already exist for this to matter.

**Independent Test**: Can be fully tested by running provisioning and then checking the version control status, confirming that no Bootstrap asset files appear as untracked or modified.

**Acceptance Scenarios**:

1. **Given** provisioning has populated the static assets directory, **When** the developer runs the version control status command, **Then** no Bootstrap asset files are listed as untracked or modified.
2. **Given** a fresh checkout followed by provisioning, **When** the developer inspects the assets directory, **Then** the files exist locally but are excluded from source control commits.

---

### Edge Cases

- What if the provisioning command fails (e.g., no network, registry unavailable)? The developer should get a clear, actionable error message rather than a silently broken or partially-styled page, and the previous assets (if any) should not be left in a half-updated state.
- What if the provisional assets directory is empty on a fresh checkout (assets are gitignored)? The documentation must make it obvious to run provisioning before the page will be styled.
- What if the developer forgets to provision after checking out? At a minimum, a clear note or command in the developer docs/quickstart prevents confusion.
- What if the dependency record and the provisioned files get out of sync? Re-running the provisioning command should always restore a consistent state matching the recorded version.
- What about the environment that runs the dashboard (e.g., a container)? The container build must provision assets as part of its build so the deployed page is always styled, independent of whether a developer provisioned locally.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST record the Bootstrap version used by the dashboard declaratively in a dedicated dependency manifest (tracked in source control).
- **FR-002**: A single provisioning command MUST download the pinned Bootstrap CSS and JS from a package registry and place them into the dashboard's static assets directory.
- **FR-003**: The downloaded Bootstrap asset files MUST be excluded from source control (not committed), while the dependency manifest and any provisioning scripts remain tracked.
- **FR-004**: Re-running the provisioning command MUST update the static assets to match the currently recorded Bootstrap version.
- **FR-005**: Provisioning MUST fail with a clear, actionable message if it cannot complete (e.g., no network), and MUST not leave the static assets in a partially-updated or corrupted state.
- **FR-006**: The dashboard MUST continue to serve the Bootstrap assets from its static assets directory so the rendered page behavior is unchanged from the prior vendored-asset approach.
- **FR-007**: The container/production build MUST provision the Bootstrap assets so the deployed dashboard is correctly styled without requiring a separate local provisioning step.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fresh clone followed by running the provisioning command yields the correct Bootstrap CSS and JS in the static assets directory, verified by the dashboard rendering styled exactly as before.
- **SC-002**: The pinned Bootstrap version is readable in the dependency manifest in 100% of checkouts, and updating it then re-provisioning swaps the assets to the new version.
- **SC-003**: After provisioning, the version control status shows no tracked or untracked Bootstrap asset files (repository stays clean of downloaded assets).
- **SC-004**: The container build provisions assets and produces a correctly-styled dashboard with no manual step (single-command developer experience preserved).

## Assumptions

- pnpm is used **only** for dependency/version tracking and asset provisioning—not as a build or bundling tool, matching the user's explicit intent.
- Bootstrap is distributed as a standard package from which the compiled CSS/JS can be copied; no compilation is needed.
- Developers have `pnpm` (and `node`, required to run pnpm) available on their machines; the provisioning command may assume these are installed.
- The dashboard runtime itself acquires no new dependencies; pnpm is a developer tooling concern only.
- Local, non-committed Bootstrap assets are acceptable because provisioning is fast and repeatable; the package registry is the canonical source for versions.
- The prior feature (002) vendored Bootstrap under `app/static/bootstrap/`; this feature replaces that committed approach with the pnpm-tracked provisioning mechanism.
