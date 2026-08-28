# Config Contract: `config.yaml`

**Date**: 2026-08-28
**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

The single YAML configuration file is **unchanged** by this feature. This feature is
presentation-only and does not alter the config schema, fields, or validation rules.

For the full contract, see the authoritative definition in feature 001:
[`specs/001-homelab-dashboard/contracts/config-contract.md`](../../001-homelab-dashboard/contracts/config-contract.md)

## Summary (unchanged)

- `title` (optional, default `"Home Lab"`)
- `services` (optional list of `{name, url, icon?}`)
- `bookmark_groups` (optional list of `{name, icon?, bookmarks: [{label, url, icon?}]}`)

No schema changes are introduced or permitted by this feature.
