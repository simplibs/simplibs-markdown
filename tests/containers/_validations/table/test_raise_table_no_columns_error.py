from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.table import raise_table_no_columns_error


def test_raise_table_no_columns_error_contract(subtests) -> None:
    """Verify raise_table_no_columns_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_table_no_columns_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_TABLE_NO_COLUMNS",
        label="table header",
        expected="A header with at least one cell.",
        problem="A table needs at least one column.",
        how_to_fix="Pass the column titles as the header.",
        exception=ValueError,
        verbose=False,
    )
