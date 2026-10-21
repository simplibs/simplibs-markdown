from typing import Final


VOID_TAGS: Final[frozenset[str]] = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "source", "track", "wbr",
})
"""HTML tags that have no closing tag and cannot hold content."""


_DESIGN_NOTES = """
# VOID_TAGS — Elements That Close Themselves

## Purpose
`<br>`, `<img>`, `<hr>`... The `Html` node writes them without a closing tag
and refuses content for them.

## Source
The list of void elements of the HTML Standard.
"""
