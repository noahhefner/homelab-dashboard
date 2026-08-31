from dataclasses import dataclass, field


@dataclass
class Tile:
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
class TileGroup:
    name: str
    tiles: list[Tile] = field(default_factory=list)
    icon: str | None = None


@dataclass
class DashboardConfig:
    title: str = "Homelab"
    tile_groups: list[TileGroup] = field(default_factory=list)
    bookmark_groups: list[BookmarkGroup] = field(default_factory=list)
