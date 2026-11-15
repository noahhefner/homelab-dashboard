"""Shared helpers for tests that assert on rendered HTML.

These utilities parse raw HTML responses with BeautifulSoup (using Python's
stdlib ``html.parser`` backend) so tests can assert on the parsed DOM rather
than on whitespace-sensitive HTML strings.
"""

from bs4 import BeautifulSoup, Tag


def parse(html: str) -> BeautifulSoup:
    """Parse an HTML string into a BeautifulSoup document."""
    return BeautifulSoup(html, "html.parser")


def attr_str(tag: Tag, name: str) -> str | None:
    """Return a single-valued attribute as text, or None when absent or multi-valued."""
    value = tag.get(name)
    return value if isinstance(value, str) else None
