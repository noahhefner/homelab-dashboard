# Implementation Plan: Edit Config From Browser

**Branch**: `008-edit-config-browser` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/008-edit-config-browser/spec.md`

## Summary

Let the dashboard owner view and edit the live YAML config directly in the browser.
Viewing the current config is always available; **editing is opt-in** (disabled by
default) and enabled by a flag in the config itself (spec FR-010 / Clarification Q1 →
Option B). On the frontend the YAML is edited in a **plain `<textarea>`** (owner choice —
Clarification Session 2026-08-30 → Option A) so the text round-trips byte-for-byte with
no rich-text editor and no bundler/build step. On save, the backend validates YAML syntax
and the dashboard's config format **before** committing; a malformed save is rejected and
the previous valid config is preserved. A retained copy of the last known-good config
enables recovery from a bad edit.

## Technical Context

**Language/Version**: Python 3.14 backend (unchanged, Flask 3.x). Frontend is
server-rendered Jinja2 with Bootstrap 5.3 plus one small vanilla-`<textarea>` editor page.

**Primary Dependencies**:
- Backend (unchanged): Flask 3.x, PyYAML (`yaml.safe_load` already used by `ConfigLoader`).
- Frontend: **none new**. The editor is a plain HTML `<textarea>`. No editor library, no
  bundler, and no build step are introduced (per Clarification Session 2026-08-30 → A).
- Reuses existing `ConfigLoader` hot-reload so a saved config is picked up without a
  restart.

**Storage**: No database. The config is a single YAML file on disk (the already-loaded
`CONFIG_PATH`). The feature adds writing that file (opt-in) and keeping a bounded backup
of the last known-good config for recovery.

**Testing**: pytest (`uv run pytest`) — unit + integration. Unit: YAML/format validation
gate, atomic-write behavior, escaping, opt-in enforcement (edit disabled by default), and
the exact byte round-trip of the saved text. Integration: end-to-end save that is
reflected by the running dashboard; malformed save leaves the prior config intact.

**Target Platform**: Linux server (Docker host) serving the dashboard; modern browsers.

**Project Type**: web application (backend + frontend); a config + small editor enhancement.

**Performance Goals**: Preserve the existing target (homepage interactive under 2
seconds). The editor page must remain interactive under 2 seconds on a typical home
network / standard device.

**Constraints**:
- **Editing is opt-in and disabled by default** (spec FR-010): no edit/save capability is
  exposed until the owner enables it via a flag in the existing config. Viewing is always
  available. (Security Requirements; default-deny.)
- **YAML must round-trip exactly**: the plain `<textarea>` returns the exact text the owner
  types (indentation, blank lines, comments, quoting); the backend must never reformat it
  (spec FR-002/FR-003/FR-008; Constitution II).
- **Never destroy the last good config**: malformed YAML, format violations, and write
  failures must be rejected/contained with a clear message and preserve the previous valid
  config (spec FR-003, FR-004, FR-007, FR-008).
- **Injection-safe**: any config text rendered back into the page is escaped; any value
  used by the dashboard continues to be validated (spec FR-009; Security Requirements).
- **Write is atomic** and performed only for the single primary config file (never
  arbitrary paths) (spec Assumptions; Security Requirements / least privilege).

**Scale/Scope**: Single-owner homelab dashboard; one config file; one editor page.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Testability (IV)**: GATE. Tests MUST be written alongside this change and approved.
  The save/validate contract and the YAML exact round-trip MUST have tests; a red-green
  cycle is required. — *Satisfied by the Testing plan above; expanded in Phase 1.*
- **Developer Experience (I)**: GATE. The change MUST NOT add friction to
  `uv run pytest` / `pnpm provision` / local run. — *Satisfied: no new frontend build step
  is added (the editor is a plain `<textarea>`), so the one-command dev loop is unchanged.*
- **Security Requirements**: GATE. Config editing writes to the server filesystem from a
  browser and must follow default-deny, near-atomic writes, path confinement to the single
  config file, output escaping, and no log/secrets exposure. — *Satisfied by the
  opt-in-by-default flag (FR-010), atomic write, path confinement, and escaping (FR-009).*
- **Readability (II) / Modularity (III)**: PASS — editing is a bounded module exposing a
  minimal contract (validate / save / read-back), mirroring the existing `ConfigLoader`
  separation.
- **YAGNI/Simplicity (V)**: PASS — the editor is a plain `<textarea>` (no editor
  dependency, no bundler, no build step), which is the simplest design that satisfies the
  requirement. No unjustified complexity is introduced; see Research for the rejected
  richer alternatives (e.g., Tiptap, CodeMirror, Monaco).

*Post-Phase-1 re-check: confirmed no gate violations; no complexity justification is
required (Complexity Tracking intentionally left empty).*

## Project Structure

### Documentation (this feature)

```text
specs/008-edit-config-browser/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output: editor decision + save-safety decisions
├── data-model.md        # Phase 1 output: config flag + save/validate/backup model
├── quickstart.md        # Phase 1 output: how to run + verify the feature
├── contracts/           # Phase 1 output: editor UI + save endpoint contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by this plan)
```

### Source Code (repository root)

```text
app/
├── __init__.py          # (reuse) create_app: register blueprint, loader
├── config.py            # ConfigLoader: expose read path + (new) editor flag accessor
├── views.py             # (new routes) /config (view), /config/save (opt-in POST)
├── editor.py            # (new) validate + atomic-write + read-back module (bounded)
├── static/
│   └── app.css, app.js  # (reuse) theme toggle etc. (textarea styled via app.css)
└── templates/
    ├── index.html       # (reuse)
    └── config.html      # (new) config view/edit page hosting the <textarea>
tests/
├── unit/test_editor_config.py        # (new) validation gate, atomic write, round-trip
├── unit/test_config_flag.py          # (new) opt-in default; read-only when disabled
└── integration/test_config_editor_flow.py  # (new) save -> reflected by dashboard
```

**Structure Decision**: Improvements are additive and mirrored to the existing single-module
Flask layout (`app/config.py`, `app/views.py`, `app/security.py`). A new small
`app/editor.py` houses the bounded write/validate/read-back contract so editing does not
tangle into rendering. No new frontend build pipeline is added (the editor is a plain
`<textarea>` served by the existing static/ template pipeline).

## Complexity Tracking

> Intentionally empty — no Constitution violations require justification. The editor is a
> plain `<textarea>` and no new frontend dependency or build step is introduced. The
> richer alternatives considered and rejected (Tiptap, CodeMirror, Monaco) are documented
> in research.md; their added complexity outweighs their benefit for raw-YAML editing.
