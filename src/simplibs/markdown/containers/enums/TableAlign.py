from enum import Enum


class TableAlign(Enum):
    """The alignment of a table column."""

    NONE = "none"
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


_DESIGN_NOTES = """
# TableAlign — Where the Column Leans

## Purpose
The values are identifiers only; the form of the separator cell (`:--`,
`:-:`, `--:`) belongs to `Table`.

## Members
* `NONE` — no colon in the separator cell.
* `LEFT`, `CENTER`, `RIGHT` — a colon on the matching side.
"""
