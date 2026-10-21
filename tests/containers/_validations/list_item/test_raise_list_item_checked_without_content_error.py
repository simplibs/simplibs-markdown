from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.list_item import (
    raise_list_item_checked_without_content_error,
)


def test_raise_list_item_checked_without_content_error_contract(subtests) -> None:
    """Verify raise_list_item_checked_without_content_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_list_item_checked_without_content_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_ITEM_CHECKED_WITHOUT_CONTENT",
        label="task item content",
        expected="A Paragraph (or a string) as the first content of the item.",
        problem=(
            "The checkbox is written in front of the first line of text.",
            "Without a paragraph first, there is no line to put it in front of.",
        ),
        how_to_fix=(
            "Start the item with a string or a Paragraph.",
            "Leave `checked` out for an item without a checkbox.",
        ),
        exception=ValueError,
        verbose=False,
    )
