import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.list import (
    raise_list_item_not_list_item_error,
)


@pytest.mark.parametrize("item", [42, 3.14, None, True, {"a": 1}])
def test_raise_list_item_not_list_item_error_contract(subtests, item) -> None:
    """Verify raise_list_item_not_list_item_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_list_item_not_list_item_error,
        invalid_params=(item,),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_ITEM_NOT_LIST_ITEM",
        label="list item",
        expected="A ListItem, a string or a Markdown node.",
        value=item,
        problem="This value cannot be turned into a list item.",
        how_to_fix=(
            "Pass a string for a simple item.",
            "Wrap several blocks into `ListItem(...)`.",
            "Convert other values with str() first.",
        ),
        exception=TypeError,
        verbose=False,
    )
