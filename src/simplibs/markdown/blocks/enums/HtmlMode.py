from enum import Enum


class HtmlMode(Enum):
    """How an `Html` node stands in the document."""

    BLOCK = "block"
    INLINE = "inline"
    COMMENT = "comment"


_DESIGN_NOTES = """
# HtmlMode — Three Faces of Raw HTML

## Members
* `BLOCK` — a block with its own lines (`<details>...</details>`).
* `INLINE` — a tag inside a line (`<kbd>Ctrl</kbd>`).
* `COMMENT` — `<!-- text -->`, not a tag at all.

## Why a Mode Instead of Three Nodes
All three are written with the same few helpers. The cost is that
`Html.node_level` depends on the mode.
"""
