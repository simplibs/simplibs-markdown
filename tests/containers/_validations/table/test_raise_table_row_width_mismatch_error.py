import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.table import (
    raise_table_row_width_mismatch_error,
)


@pytest.mark.parametrize(
    "cells, expected_width",
    [
        ((), 2),
        (("a",), 2),
        (("a", "b", "c"), 2),
    ],
)
def test_raise_table_row_width_mismatch_error_contract(
    subtests, cells, expected_width
) -> None:
    """Verify raise_table_row_width_mismatch_error reports both counts."""

    assert_exception_function(
        subtests,
        raise_table_row_width_mismatch_error,
        invalid_params=(cells, expected_width),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_ROW_WIDTH_MISMATCH",
        label="table row",
        expected=f"Exactly {expected_width} cells in every row.",
        value=cells,
        problem=(
            f"Cells in the row: {len(cells)}.",
            f"Columns in the header: {expected_width}.",
        ),
        how_to_fix=(
            "Add the missing cells, or remove the extra ones.",
            "Use an empty string for a cell with no content.",
        ),
        exception=ValueError,
        verbose=False,
    )
