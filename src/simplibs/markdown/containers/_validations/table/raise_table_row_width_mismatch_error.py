from typing import NoReturn
from simplibs.exception import ParamError


def raise_table_row_width_mismatch_error(
    cells: tuple[str, ...],
    expected_width: int,
) -> NoReturn:
    """Raise ParamError when a row has a different number of cells than the header.

    Args:
        cells: The cells of the rejected row.
        expected_width: The number of columns in the header.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_TABLE_ROW_WIDTH_MISMATCH",
        label="table row",
        value=cells,
        problem=(
            f"Cells in the row: {len(cells)}.",
            f"Columns in the header: {expected_width}.",
        ),
        expected=f"Exactly {expected_width} cells in every row.",
        how_to_fix=(
            "Add the missing cells, or remove the extra ones.",
            "Use an empty string for a cell with no content.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_table_row_width_mismatch_error — A Row That Does Not Fit

## Purpose
GFM pads short rows and cuts long ones without a word, so data would be lost
or shifted into other columns. The check runs when the table is built.
"""
