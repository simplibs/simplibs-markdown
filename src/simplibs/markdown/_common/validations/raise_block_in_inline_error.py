from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_block_in_inline_error(
    value: Any,
) -> NoReturn:
    """Raise ParamError when a block element is placed inside inline content.

    Args:
        value: The rejected block node (or a collection that holds one).
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        label="inline content",
        value=value,
        problem="Block elements cannot be placed inside inline content.",
        expected="Text, emphasis, a link, inline code or another inline element.",
        how_to_fix=(
            "Put the block into a Document or a container such as Quote or List.",
            "Use an inline element in this place instead.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_block_in_inline_error — A Block Inside a Line

## Purpose
A heading inside bold text, or a table inside a link, has no Markdown form.
The card is raised when the node is built, not when the output turns out wrong.

## Why It Lives in `_common`
Used by `as_inline` (`base_class`) and `Html` in inline mode (`blocks`).
"""
