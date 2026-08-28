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


@dataclass
class DashboardConfig:
    title: str = "Home Lab"
    services: list[Service] = field(default_factory=list)
    bookmark_groups: list[BookmarkGroup] = field(default_factory=list)
