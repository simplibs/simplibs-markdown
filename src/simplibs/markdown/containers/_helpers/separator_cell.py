# Outers
from ..enums import TableAlign


def separator_cell(width: int, align: TableAlign) -> str:
    """Write the separator cell of a column.

    Args:
        width: The width of the column, at least 3.
        align: The alignment of the column.

    Returns:
        Dashes with a colon on each side that the alignment asks for.
    """

    # 1. A colon on the left aligns left, on the right aligns right, on both centers
    if align is TableAlign.LEFT:
        return ":" + "-" * (width - 1)
    if align is TableAlign.RIGHT:
        return "-" * (width - 1) + ":"
    if align is TableAlign.CENTER:
        return ":" + "-" * (width - 2) + ":"

    # 2. No alignment: dashes only
    return "-" * width


_DESIGN_NOTES = """
# separator_cell — The Row That Holds the Alignment

## Purpose
`:--`, `:-:`, `--:` and `---` are the only place where a table says how a
column is aligned.

## Minimum Width
The centered form needs three characters (`:-:`). `Table` never gives a
column less than 3.
"""
