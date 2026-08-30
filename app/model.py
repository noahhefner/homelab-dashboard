from dataclasses import dataclass, field


@dataclass
class Service:
    name: str
    url: str
    icon: str | None = None


@dataclass
class Bookmark:
    label: str
    url: str
    icon: str | None = None


@dataclass
class BookmarkGroup:
    name: str
    bookmarks: list[Bookmark] = field(default_factory=list)
    icon: str | None = None
    collapsed: bool = False


@dataclass
class DashboardConfig:
    title: str = "Homelab"
    services: list[Service] = field(default_factory=list)
    bookmark_groups: list[BookmarkGroup] = field(default_factory=list)
