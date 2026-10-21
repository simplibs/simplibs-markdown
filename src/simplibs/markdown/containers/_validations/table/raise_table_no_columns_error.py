from typing import NoReturn
from simplibs.exception import ParamError


def raise_table_no_columns_error() -> NoReturn:
    """Raise ParamError when a table header has no column."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_TABLE_NO_COLUMNS",
        label="table header",
        problem="A table needs at least one column.",
        expected="A header with at least one cell.",
        how_to_fix="Pass the column titles as the header.",
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_table_no_columns_error — A Table Without Columns

## Purpose
The header decides the width of every row and of the separator line. With no
cells there is nothing to measure.
"""
