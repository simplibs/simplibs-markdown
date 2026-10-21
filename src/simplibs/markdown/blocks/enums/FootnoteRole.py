from enum import Enum


class FootnoteRole(Enum):
    """The part of a footnote that a node represents."""

    REFERENCE = "reference"
    DEFINITION = "definition"


_DESIGN_NOTES = """
# FootnoteRole — The Marker and the Note

## Members
* `REFERENCE` — `[^1]`, the marker inside a line of text (an inline node).
* `DEFINITION` — `[^1]: text`, the note itself (a block node).

## Why a Role Instead of Two Nodes
One label ties both together. The cost is that `Footnote.node_level` depends
on the role.
"""
