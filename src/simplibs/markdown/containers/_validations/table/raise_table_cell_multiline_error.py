from typing import NoReturn
from simplibs.exception import ParamError


def raise_table_cell_multiline_error(
    text: str,
) -> NoReturn:
    """Raise ParamError when a table cell contains a line break.

    Args:
        text: The rendered text of the rejected cell.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_TABLE_CELL_MULTILINE",
        label="table cell",
        value=text,
        problem=(
            "A table row is one line.",
            "A line break would end the row.",
        ),
        expected="Cell text without line breaks.",
        how_to_fix=(
            "Keep the cell on a single line.",
            "Use `LineBreak(LineBreakStyle.HTML)` for a break inside the cell.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_table_cell_multiline_error — A Row That Breaks in Two

## Purpose
GFM tables have no multi-line cells. The HTML line break is the only form
that stays on one line of the source.
"""
