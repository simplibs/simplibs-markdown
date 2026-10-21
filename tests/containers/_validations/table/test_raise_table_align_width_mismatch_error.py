import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers.enums import TableAlign
from simplibs.markdown.containers._validations.table import (
    raise_table_align_width_mismatch_error,
)


@pytest.mark.parametrize(
    "align, expected_width",
    [
        ((), 2),
        ((TableAlign.LEFT,), 3),
        ((TableAlign.LEFT, TableAlign.CENTER, TableAlign.RIGHT), 1),
    ],
)
def test_raise_table_align_width_mismatch_error_contract(
    subtests, align, expected_width
) -> None:
    """Verify raise_table_align_width_mismatch_error reports both counts."""

    assert_exception_function(
        subtests,
        raise_table_align_width_mismatch_error,
        invalid_params=(align, expected_width),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_ALIGN_WIDTH_MISMATCH",
        label="table alignment",
        expected=f"Exactly {expected_width} alignments, one per column.",
        value=align,
        problem=(
            f"Alignments given: {len(align)}.",
            f"Columns in the table: {expected_width}.",
        ),
        how_to_fix=(
            "Pass one `TableAlign` for each column.",
            "Leave `align` out to keep every column unaligned.",
        ),
        exception=ValueError,
        verbose=False,
    )
