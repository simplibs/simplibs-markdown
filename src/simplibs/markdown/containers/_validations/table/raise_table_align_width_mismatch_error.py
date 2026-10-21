from typing import NoReturn
from simplibs.exception import ParamError


def raise_table_align_width_mismatch_error(
    align: tuple,
    expected_width: int,
) -> NoReturn:
    """Raise ParamError when the number of alignments differs from the number of columns.

    Args:
        align: The rejected alignments.
        expected_width: The number of columns in the header.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_TABLE_ALIGN_WIDTH_MISMATCH",
        label="table alignment",
        value=align,
        problem=(
            f"Alignments given: {len(align)}.",
            f"Columns in the table: {expected_width}.",
        ),
        expected=f"Exactly {expected_width} alignments, one per column.",
        how_to_fix=(
            "Pass one `TableAlign` for each column.",
            "Leave `align` out to keep every column unaligned.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_table_align_width_mismatch_error — A Separator Line That Is Too Short

## Purpose
The alignments are written into the separator row, which must have one cell
per column.
"""
