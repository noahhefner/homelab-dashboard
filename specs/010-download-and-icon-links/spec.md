# Feature Specification: Download Config & Icon Links

**Feature Branch**: `010-download-and-icon-links`

**Created**: 2026-08-31

**Status**: Draft

**Input**: User description: "Implement a download feature to download the config yaml file from the editor page. Also add links to iconography websites on the editor page."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download Config YAML From the Editor Page (Priority: P1)

As the dashboard owner, I want to download the current config YAML file directly from the editor page so I can keep a local backup, share it, or move it to another machine without manually copying the file from the host.

**Why this priority**: This is the primary requested feature. It delivers immediate, standalone value — an owner can grab the config file with one click, no shell access needed. It is also the more complex of the two features and should be built first.

**Independent Test**: Can be fully tested by opening the editor page and clicking the download button, confirming a YAML file is saved to the local machine with the correct contents and filename.

**Acceptance Scenarios**:

1. **Given** the editor page is loaded, **When** the owner clicks the download button, **Then** a file named `dashboard.yaml` (or the basename of the configured config file) is saved to the owner's local downloads folder.
2. **Given** the editor page is loaded, **When** the download completes, **Then** the downloaded file contains exactly the current YAML content of the config file on disk.
3. **Given** the owner has editing enabled and has unsaved changes in the textarea, **When** the owner clicks download, **Then** the downloaded file reflects the on-disk version (not the unsaved editor content), and the owner is not confused about what was downloaded.
4. **Given** the config file cannot be read from disk, **When** the owner clicks download, **Then** a clear error message is shown instead of a broken or empty download.

---

### User Story 2 - Quick Links to Iconography Websites (Priority: P2)

As the dashboard owner editing my config, I want a clearly visible link to iconography websites on the editor page so I can quickly find and reference icons when adding or updating tile and bookmark icon URLs in the YAML.

**Why this priority**: This is a low-effort, high-value usability improvement. It directly supports the editing workflow by reducing the friction of finding icons. It is secondary to the download feature because it does not involve new server functionality.

**Independent Test**: Can be fully tested by opening the editor page and confirming that links to iconography websites are visible and clickable, opening the correct sites in a new tab.

**Acceptance Scenarios**:

1. **Given** the editor page is loaded, **When** the owner looks for icon resources, **Then** a section with links to recommended iconography websites is visible on the page.
2. **Given** the owner clicks an iconography link, **When** the browser handles the click, **Then** the link opens in a new browser tab without navigating away from the editor page.
3. **Given** the editor page is loaded in read-only mode (editing disabled), **When** the owner looks for icon resources, **Then** the iconography links are still visible and accessible.

---

### Edge Cases

- Config file missing or unreadable at download time: show a clear error message; do not download an empty or corrupted file.
- Very large config files: the download must complete without timing out at typical homelab config sizes.
- Browser blocks the download (pop-up blocker or download settings): the UI should degrade gracefully or provide a clear fallback message.
- Owner attempts to download while a save is in progress: the download should use the file as it exists on disk at the moment of request; no locking is required.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a clearly visible download button on the editor page that initiates a file download of the current config YAML.
- **FR-002**: The downloaded file MUST contain the exact, unmodified YAML content of the config file currently on disk.
- **FR-003**: The downloaded file MUST use the basename of the configured config file (e.g., `dashboard.yaml`) as the filename, not a generic or hardcoded name.
- **FR-004**: The download MUST work in both editing-enabled and read-only editor modes.
- **FR-005**: If the config file cannot be read, the system MUST show a clear error and MUST NOT download an empty or partial file.
- **FR-006**: The system MUST display a section on the editor page with links to at least the following iconography resources: dashboardicons.com and homarr-labs/dashboard-icons (GitHub repository).
- **FR-007**: Iconography links MUST open in a new browser tab (target `_blank`) without navigating away from the editor page.
- **FR-008**: Iconography links MUST be visible regardless of whether editing is enabled or disabled.
- **FR-009**: The download action MUST NOT interfere with unsaved editor changes; it downloads the on-disk file, not the textarea buffer.

### Key Entities

- **Config File on Disk**: The YAML file the dashboard is running from, served as the download payload.
- **Editor Page**: The existing `/config` page (read-only or editing mode) where the download button and icon links will appear.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of successful download requests result in a file that matches the on-disk config content byte-for-byte.
- **SC-002**: 100% of failed download attempts (file unreadable) produce a clear, user-facing error message.
- **SC-003**: Iconography links are visible and clickable on first page load without any additional navigation.
- **SC-004**: Download completes within 2 seconds for configs up to 100 KB (well beyond typical homelab config sizes).

## Assumptions

- The dashboard is a personal, single-owner homelab tool; the download feature does not require authentication or access control beyond what already exists for the editor page.
- "Download the config YAML" means serving the raw file from disk, not a transformed or re-exported version.
- The filename for the download should match the basename of the configured config file path (e.g., if `config/example.yaml` is loaded, the download is `example.yaml`).
- Unsaved textarea edits are not included in the download; this keeps the feature simple and avoids confusion about what is being downloaded.
- Iconography links will be static HTML; no external API or dynamic lookup is needed.
- The two recommended icon sources (dashboardicons.com and homarr-labs/dashboard-icons) are stable, well-known community resources for homelab dashboard icons.
