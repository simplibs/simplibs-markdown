from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_list_item_not_list_item_error(
    item: Any,
) -> NoReturn:
    """Raise ParamError when a value cannot become a list item.

    Args:
        item: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="MARKDOWN_LIST_ITEM_NOT_LIST_ITEM",
        label="list item",
        value=item,
        problem="This value cannot be turned into a list item.",
        expected="A ListItem, a string or a Markdown node.",
        how_to_fix=(
            "Pass a string for a simple item.",
            "Wrap several blocks into `ListItem(...)`.",
            "Convert other values with str() first.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_list_item_not_list_item_error — An Item That Is Not Content

## Purpose
A number or a `None` in a list would be written as `str(value)` by accident.
Strings and nodes are wrapped in a `ListItem` automatically; anything else is
refused.
"""
