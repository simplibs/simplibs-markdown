from typing import Any


def add_nodes(left: Any, right: Any) -> Any:
    """Compose the two operands of `+`.

    Args:
        left: The left operand (a node or a string).
        right: The right operand (a node or a string).

    Returns:
        An `InlineJoin` for two inline operands, a `Document` otherwise, or
        `NotImplemented` when an operand is neither a node nor a string.
    """

    # 1. Lazy (upward) — every node type involved is above `_common`
    from ...base_class.enums import NodeLevel
    from ...base_class.Markdown import Markdown
    from ...blocks.Paragraph import Paragraph
    from ...containers.Document import Document
    from ...inline.InlineJoin import InlineJoin
    from ...inline.Text import Text

    # 2. A string takes the level of the node on the other side
    if isinstance(left, str) and isinstance(right, Markdown):
        left = Text(left) if right.node_level is NodeLevel.INLINE else Paragraph(left)
    elif isinstance(right, str) and isinstance(left, Markdown):
        right = Text(right) if left.node_level is NodeLevel.INLINE else Paragraph(right)

    # 3. Two operands that are not both nodes are not ours to compose
    if not (isinstance(left, Markdown) and isinstance(right, Markdown)):
        return NotImplemented

    # 4. Inline with inline stays one line
    if left.node_level is NodeLevel.INLINE and right.node_level is NodeLevel.INLINE:
        return InlineJoin(left, right)

    # 5. Anything with a block in it becomes a document
    return Document(left, right)


_DESIGN_NOTES = """
# add_nodes — What `+` Means

## Purpose
`"Viz " + Link(...) + "."` is one line; `Heading(...) + Paragraph(...)` is a
document. The rule is one function, used by both `__add__` and `__radd__`.

## Strings
A string next to an inline node becomes escaped `Text`; next to a block it
becomes a `Paragraph`. That is why `H1("A") + "text"` works and
`"text" + H1("A")` does too.

## `NotImplemented`
Returned, not raised, for `node + 5`, so Python can try the other operand and
finally raise its own `TypeError`.

## Lazy (Upward) Imports
The result is a node from a layer above `_common`. The imports are inside the
function so that `base_class` can import this helper without a cycle.
"""
