import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.table import (
    raise_table_cell_multiline_error,
)


@pytest.mark.parametrize("text", ["first\nsecond", "a\r\nb", "\nleading"])
def test_raise_table_cell_multiline_error_contract(subtests, text) -> None:
    """Verify raise_table_cell_multiline_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_table_cell_multiline_error,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_CELL_MULTILINE",
        label="table cell",
        expected="Cell text without line breaks.",
        value=text,
        problem=(
            "A table row is one line.",
            "A line break would end the row.",
        ),
        how_to_fix=(
            "Keep the cell on a single line.",
            "Use `LineBreak(LineBreakStyle.HTML)` for a break inside the cell.",
        ),
        exception=ValueError,
        verbose=False,
    )
