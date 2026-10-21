from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.list import raise_list_no_items_error


def test_raise_list_no_items_error_contract(subtests) -> None:
    """Verify raise_list_no_items_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_list_no_items_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_NO_ITEMS",
        label="list items",
        expected="At least one string, node or `ListItem`.",
        problem="A list needs at least one item.",
        how_to_fix=(
            "Pass the items as arguments.",
            "Do not create the list when there is nothing to list.",
        ),
        exception=ValueError,
        verbose=False,
    )
