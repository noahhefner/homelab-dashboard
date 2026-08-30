# Feature Specification: Edit Config From Browser

**Feature Branch**: `008-edit-config-browser`

**Created**: 2026-08-30

**Status**: Draft

**Input**: User description: "Add a feature to edit the yaml configuration file directly from the browser."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View the Current Config in the Browser (Priority: P1)

As the dashboard owner, I want to open the current YAML configuration in a page in my browser so I can review exactly what the dashboard is running with, without shelling into the host or opening the file by hand.

**Why this priority**: Reading the current config is the safe, read-only foundation of the whole feature. It delivers immediate value on its own (a way to inspect the live config from a browser) and is the natural starting point for editing.

**Independent Test**: Can be fully tested by loading the config-view page and confirming the page displays the exact YAML currently loaded by the dashboard, with no ability to modify it.

**Acceptance Scenarios**:

1. **Given** a dashboard with a config file on disk, **When** the owner opens the config page, **Then** the page shows the current YAML content of the loaded config.
2. **Given** the owner is viewing the config page, **When** the page renders, **Then** no save or modify control is available in this view.
3. **Given** the current config file is not reachable or unreadable, **When** the owner opens the config page, **Then** a clear error message is shown rather than a broken or empty page.

---

### User Story 2 - Edit and Save the Config From the Browser (Priority: P1)

As the dashboard owner, I want to edit the YAML config text directly in my browser and save it, so I can make configuration changes (add a service, change a label, edit an icon, etc.) without editing a file on the host or rebuilding.

**Why this priority**: This is the core, explicit requirement. The dashboard already reloads when its config changes, so once a valid edit is written to file, the running dashboard reflects it.

**Independent Test**: Can be fully tested by editing a value in the browser, saving, and confirming the new value takes effect on the dashboard without touching the host or restarting the app.

**Acceptance Scenarios**:

1. **Given** the owner is on the config edit page, **When** they modify a valid value and save, **Then** the change is written to the config file and reflected by the dashboard after the config is (re)applied.
2. **Given** the owner submits malformed YAML, **When** they attempt to save, **Then** the save is rejected with a clear, specific error message and the previously valid config is left untouched.
3. **Given** the owner submits YAML that is valid but violates the dashboard's known config format (e.g., a missing required field), **When** they save, **Then** the dashboard reports the schema problem clearly instead of silently applying a broken config.
4. **Given** the config file cannot be written (e.g., permissions or disk), **When** the owner saves, **Then** a clear error is shown and the previous config remains intact.

---

### User Story 3 - Change Kick In Without Extra Steps (Priority: P1)

As the dashboard owner, I want saved config edits to take effect as soon as they are saved, so the dashboard and the config I just wrote stay in sync without a manual restart.

**Why this priority**: Applying changes automatically is what makes the browser editor convenient. It relies on the dashboard's existing ability to pick up config changes, so the owner sees the result of their edit immediately.

**Independent Test**: Can be fully tested by making a config edit in the browser, saving it, and confirming the dashboard reflects the change on a subsequent load without any manual reload or restart of the application.

**Acceptance Scenarios**:

1. **Given** the owner saves a valid edit, **When** the dashboard next loads (or next request), **Then** the new values are in effect without the owner performing any manual step.
2. **Given** an edit produces an invalid config, **When** the dashboard would otherwise have applied it, **Then** the dashboard keeps serving with the last valid config rather than failing for all users.

---

### User Story 4 - Recover From a Bad Edit (Priority: P2)

As the dashboard owner, I want a way to recover the last good configuration after a mistake, so a bad edit cannot permanently lose my working setup.

**Why this priority**: Edits can go wrong despite validation. A simple recovery path (a retained copy of the last valid config) protects against accidental data loss, which is painful to recover from otherwise. It is secondary to the core edit-and-apply flow.

**Independent Test**: Can be fully tested by making a self-inflicted bad or unwanted edit, saving, and confirming the owner can restore the previous working configuration from an in-browser action.

**Acceptance Scenarios**:

1. **Given** a previously valid config exists, **When** the owner saves a change and then chooses to revert, **Then** the owner can restore the prior config from the browser without manual file editing.
2. **Given** a failed or invalid save, **When** the owner inspects the state, **Then** the last valid config is still in place and recoverable.

---

### User Story 5 - Protect the Edit Action (Priority: P2)

As the dashboard owner, I want the ability to edit the config to be protected, so only I can change the configuration and can control whether this capability is exposed at all.

**Why this priority**: This dashboard may be reachable beyond the local network. Writing to the config file from the browser is a powerful and sensitive action, so it must be off by default and only enabled by my explicit choice.

**Independent Test**: Can be fully tested by confirming that, with editing not enabled, no save control is exposed even if the edit page is reachable; and once enabled in the config, editing becomes available.

**Acceptance Scenarios**:

1. **Given** editing is not enabled in the config flag, **When** a request attempts to edit or save, **Then** no edit/save capability is exposed and the owner can only view the config.
2. **Given** the owner enables editing in the config, **When** they save a change, **Then** the edit capability is available and saves succeed per the other user stories.

---

### Edge Cases

- Config file missing or unreadable at save time: show a clear error and leave the last valid state intact.
- Config write fails (permissions, disk full, path changed): surface a clear error; never silently lose the previous config.
- Empty YAML submitted: reject as invalid and keep the previous valid config.
- YAML that is valid but fails the dashboard's config/format rules: report the specific problem instead of applying a broken config.
- Editing while the dashboard is actively reading config: the write must not corrupt the file or crash the dashboard; the dashboard must keep serving valid data.
- Multiple edits in a row: each save produces a fresh valid file; recovery should reflect the most recent good state without growing unboundedly.
- Very large config files: the editor must remain usable (load, edit, save) without timing out at normal homelab config sizes.
- Stale view: if the config changed on disk since the owner opened the editor, saving must not silently overwrite newer changes (surface a "config changed since you opened" situation). [Assumed default; see Assumptions.]
- Any mirrored config text rendered back into the page must be escaped to prevent injection per the Security Requirements.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow the owner to view the current YAML config content in the browser.
- **FR-002**: The system MUST allow the owner to edit the YAML config text directly in the browser as raw plain text, preserving exactly the text the owner types; it MUST NOT be a field-by-field form and MUST NOT introduce rich-text/WYSIWYG behavior that could reformat the config.
- **FR-003**: The system MUST validate YAML syntax before committing a save; malformed YAML MUST be rejected with a clear, specific error and MUST NOT overwrite the existing valid config.
- **FR-004**: The system MUST validate the edited config against the dashboard's known config format (required fields/types) and surface any problems clearly before or instead of applying a broken configuration.
- **FR-005**: When a valid edit is saved, the system MUST write the change to the config file and the dashboard MUST reflect it when config is next applied, without the owner performing any manual restart.
- **FR-006**: The system MUST preserve and allow recovery of the last known-good configuration so a bad edit does not cause permanent data loss.
- **FR-007**: If the config file or its directory is not writable, the system MUST show a clear error and MUST NOT lose the previous config.
- **FR-008**: The system MUST keep serving the last valid configuration in the event of an invalid save so the dashboard does not go down for all users.
- **FR-009**: The system MUST prevent injection: any config content rendered into the page MUST be escaped appropriately, and any values used by the dashboard MUST continue to be validated as they are today.
- **FR-010**: The edit capability MUST be opt-in and disabled by default: it is exposed only when the owner explicitly enables it via a flag in the existing config file. Read-only viewing of the config MUST always be available.
- **FR-011**: The system MUST surface a warning when the config changed on disk since the editor was opened, to avoid silently overwriting newer changes. [Assumed default; see Assumptions.]

### Key Entities *(include if feature involves data)*

- **Configuration**: The YAML document the dashboard is currently running from. It is the primary artifact read and (edit capability) written by this feature.
- **Config File on Disk**: The persistence target for edits. Its writability and integrity affect save success and recovery.
- **Recent Good Config (Backup)**: A retained copy of the last known-valid configuration used for recovery (bounded, per Assumptions).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid config edits made in the browser are written to file and, once config is (re)applied, reflected by the dashboard.
- **SC-002**: 100% of malformed-YAML save attempts are rejected with a clear error and leave the previously valid config untouched.
- **SC-003**: An owner can recover the last known-good config from the browser after a bad edit, with no data loss to the working setup.
- **SC-004**: The config view and editor page load within the existing page-load target (page visible/interactive under 2 seconds on a typical home network and standard device).
- **SC-005**: Editing is disabled by default; an owner can enable it via a flag in the config, and once enabled, saves work. While disabled, no edit/save capability is exposed and attempts to edit are blocked.

## Assumptions

- The dashboard is a personal, single-owner homelab tool; the normal operating model is one trusted owner.
- "Directly in the browser" means editing the raw YAML text (not a structured per-field form), matching the wording of the requirement.
- **Editor choice (resolved)**: The editor is a plain `<textarea>` (raw text), NOT a rich-text/WYSIWYG editor such as Tiptap. This keeps the frontend dependency-free (no editor library, no bundler/build step), guarantees an exact byte-for-byte round-trip of the YAML (no silent reformatting that could corrupt the config), and best matches the raw-text editing requirement. Syntax highlighting is intentionally out of scope.
- The editor operates on the single primary dashboard config file that the running dashboard loads (not arbitrary server files, and not creating new files).
- Saving applies through the dashboard's existing ability to pick up config changes; no separate manual apply step is required in the default flow.
- A retained recent-good-config backup is bounded (e.g., a small rotating set or a single recent copy) rather than an unbounded history; the default is a single retained last-known-good copy.
- Stale-editor detection: if the config changed on disk after the editor was opened, the system should surface it before overwriting (FR-011). This is the assumed safe default.
- **Access control (resolved)**: The edit capability is opt-in and disabled by default. It is exposed only after the owner explicitly enables editing via a flag in the existing config file. The owner controls this flag (the existing security-grounded config validation applies to it), so editing is never implicitly exposed. Viewing the config remains always available.

## Clarifications

### Session 2026-08-30

- Q: Which editor component should the config editor use, given the goal of reducing frontend complexity? → A: Option A — a plain `<textarea>` (raw YAML text editor; no rich-text editor / no bundler / no frontend build step).

