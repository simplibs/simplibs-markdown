from typing import Any, TYPE_CHECKING
# Outers
from ..validations import raise_block_in_inline_error, raise_node_not_markdown_error
# Annotations
if TYPE_CHECKING:
    from ...base_class import Markdown


def as_inline(value: Any) -> "Markdown":
    """Turn a string, an inline node or a list of them into one inline node.

    Args:
        value: The content of an inline slot.

    Returns:
        An inline node (a string becomes escaped `Text`, a list an `InlineJoin`).

    Raises:
        ParamError: If the value is a block node or not content at all.
    """

    # 1. Lazy (upward) — the inline nodes are above `_common` in the import graph
    from ...base_class.enums import NodeLevel
    from ...base_class.Markdown import Markdown
    from ...inline.InlineJoin import InlineJoin
    from ...inline.Text import Text

    # 2. A string is plain text; special characters are escaped
    if isinstance(value, str):
        return Text(value)

    # 3. A node is accepted only when it can stand inside a line
    if isinstance(value, Markdown):
        if value.node_level is not NodeLevel.INLINE:
            raise_block_in_inline_error(value)
        return value

    # 4. A list or a tuple is joined into one line
    if isinstance(value, (list, tuple)):
        return InlineJoin(*value)

    # 5. Anything else is not content
    raise_node_not_markdown_error(value)


_DESIGN_NOTES = """
# as_inline — The Gate of Every Inline Slot

## Purpose
The content of emphasis, a link, a heading or a table cell may be given as a
string, a node or a list of them. This function is the one place that decides
what is accepted and what each form becomes.

## Why It Lives in `_common`
Used by `inline`, `blocks` and `containers`. It moved here from `Markdown.py`
because it is not part of the node contract.

## Lazy (Upward) Imports
It creates `Text` and `InlineJoin`, both above `_common`. `InlineJoin` calls
back to `as_inline` for each of its parts, which is why the imports are inside
the function.
"""
