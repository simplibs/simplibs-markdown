from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_node_not_markdown_error(
    value: Any,
) -> NoReturn:
    """Raise ParamError when a value is neither a string nor a Markdown node.

    Args:
        value: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        label="content",
        value=value,
        problem="This value cannot be turned into Markdown.",
        expected="A string or a Markdown node (Text, Heading, Paragraph...).",
        how_to_fix=(
            "Pass a string, or build the node with the matching class.",
            "Convert other values with str() first.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_node_not_markdown_error — Something That Is Not Content

## Purpose
Content slots accept strings and nodes. A number or a `None` would otherwise
be written into the document as `str(value)` by accident.

## Why It Lives in `_common`
Used by `as_inline` (`base_class`) and `flatten_blocks` (`containers`).
"""
