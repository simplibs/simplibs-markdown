from typing import NoReturn
from simplibs.exception import ParamError


def raise_list_no_items_error() -> NoReturn:
    """Raise ParamError when a list is created without any item."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LIST_NO_ITEMS",
        label="list items",
        problem="A list needs at least one item.",
        expected="At least one string, node or `ListItem`.",
        how_to_fix=(
            "Pass the items as arguments.",
            "Do not create the list when there is nothing to list.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_list_no_items_error — A List With Nothing to List

## Purpose
An empty list renders as nothing. It has its own card because its content is
items, not blocks, and `raise_no_blocks_error` would name the wrong thing.
"""
