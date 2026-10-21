# Outers
from ..enums import TableAlign


def pad_cell(text: str, width: int, align: TableAlign) -> str:
    """Pad a cell to the width of its column.

    Args:
        text: The rendered cell.
        width: The width of the column.
        align: The alignment of the column.

    Returns:
        The text padded with spaces on the side that the alignment leaves free.
    """

    # 1. Right-aligned text is padded on the left, centered on both sides
    if align is TableAlign.RIGHT:
        return text.rjust(width)
    if align is TableAlign.CENTER:
        return text.center(width)

    # 2. Left-aligned and unaligned text is padded on the right
    return text.ljust(width)


_DESIGN_NOTES = """
# pad_cell — Columns That Line Up in the Source

## Purpose
The table renders the same with or without padding. The padding makes the
source readable in an editor.

## Known Limit
Width is the number of characters (`len`). Wide characters (CJK) and
combining marks occupy another width on screen, so such a table is not
aligned in the source. The rendered table is not affected.
"""
