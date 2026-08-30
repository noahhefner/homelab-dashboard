from app.model import Bookmark, BookmarkGroup, DashboardConfig, Service
from app.security import validate_url


class ConfigValidationError(Exception):
    """Raised when the YAML config is invalid or cannot be parsed into the model."""


def _require_non_empty(value, field, where):
    if value is None or not str(value).strip():
        raise ConfigValidationError(f"{where}.{field} must be a non-empty string")
    return str(value)


def _parse_url(value, field, where):
    value = _require_non_empty(value, field, where)
    if not validate_url(value):
        raise ConfigValidationError(f"{where}.{field} must be a valid http/https URL")
    return value


def _parse_service(data, index):
    if not isinstance(data, dict):
        raise ConfigValidationError(f"services[{index}] must be a mapping")
    where = f"services[{index}]"
    name = _require_non_empty(data.get("name"), "name", where)
    url = _parse_url(data.get("url"), "url", where)
    icon = data.get("icon")
    if icon is not None:
        icon = str(icon)
    return Service(name=name, url=url, icon=icon)


def _parse_bookmark(data, index):
    if not isinstance(data, dict):
        raise ConfigValidationError(f"bookmarks[{index}] must be a mapping")
    where = f"bookmarks[{index}]"
    label = _require_non_empty(data.get("label"), "label", where)
    url = _parse_url(data.get("url"), "url", where)
    icon = data.get("icon")
    if icon is not None:
        icon = str(icon)
    return Bookmark(label=label, url=url, icon=icon)


def _parse_group(data, index):
    if not isinstance(data, dict):
        raise ConfigValidationError(f"bookmark_groups[{index}] must be a mapping")
    where = f"bookmark_groups[{index}]"
    name = _require_non_empty(data.get("name"), "name", where)
    icon = data.get("icon")
    if icon is not None:
        icon = str(icon)
    collapsed = data.get("collapsed")
    if collapsed is not None and not isinstance(collapsed, bool):
        raise ConfigValidationError(f"{where}.collapsed must be a boolean")
    bookmarks = []
    raw_bookmarks = data.get("bookmarks") or []
    if not isinstance(raw_bookmarks, list):
        raise ConfigValidationError(f"{where}.bookmarks must be a list")
    for bindex, bdata in enumerate(raw_bookmarks):
        bookmarks.append(_parse_bookmark(bdata, bindex))
    return BookmarkGroup(
        name=name, bookmarks=bookmarks, icon=icon, collapsed=bool(collapsed)
    )


def parse_dashboard(data):
    """Convert a raw parsed-YAML mapping into a validated DashboardConfig."""
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ConfigValidationError("top-level config must be a mapping")

    raw_title = data.get("title")
    title = str(raw_title).strip() if raw_title is not None else ""
    if not title:
        title = "Homelab"

    services = []
    raw_services = data.get("services") or []
    if not isinstance(raw_services, list):
        raise ConfigValidationError("services must be a list")
    for index, sdata in enumerate(raw_services):
        services.append(_parse_service(sdata, index))

    groups = []
    raw_groups = data.get("bookmark_groups") or []
    if not isinstance(raw_groups, list):
        raise ConfigValidationError("bookmark_groups must be a list")
    for index, gdata in enumerate(raw_groups):
        groups.append(_parse_group(gdata, index))

    return DashboardConfig(title=title, services=services, bookmark_groups=groups)
