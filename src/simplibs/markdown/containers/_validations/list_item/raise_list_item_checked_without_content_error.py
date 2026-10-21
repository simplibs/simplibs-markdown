from typing import NoReturn
from simplibs.exception import ParamError


def raise_list_item_checked_without_content_error() -> NoReturn:
    """Raise ParamError when a task item does not start with a paragraph."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LIST_ITEM_CHECKED_WITHOUT_CONTENT",
        label="task item content",
        problem=(
            "The checkbox is written in front of the first line of text.",
            "Without a paragraph first, there is no line to put it in front of.",
        ),
        expected="A Paragraph (or a string) as the first content of the item.",
        how_to_fix=(
            "Start the item with a string or a Paragraph.",
            "Leave `checked` out for an item without a checkbox.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_list_item_checked_without_content_error — A Checkbox With No Line

## Purpose
`- [ ]` followed by a code block or nothing is not a task item. The checkbox
needs text on the same line.
"""
