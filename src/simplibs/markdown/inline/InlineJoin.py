# Outers
from ..base_class import InlineMarkdown
from .._common.helpers import as_inline


class InlineJoin(InlineMarkdown):
    """Several inline nodes written one after another.

    Args:
        *parts: Strings, inline nodes or lists of them. A nested join is
            unpacked, so the result is always one flat sequence.

    Raises:
        ParamError: If a part is a block node or not content at all.
    """

    __slots__ = ("parts",)

    def __init__(self, *parts) -> None:

        # 1. Turn every part into an inline node; a nested join gives its own parts
        flat = []
        for part in parts:
            node = as_inline(part)
            flat.extend(node.parts if isinstance(node, InlineJoin) else (node,))

        # 2. Assignment
        self.parts = tuple(flat)

    def to_inline(self) -> str:

        # 1. The parts are written without any separator
        return "".join(part.to_text() for part in self.parts)


_DESIGN_NOTES = """
# InlineJoin — What `+` Gives for Two Inline Nodes

## Purpose
`"Viz " + Link(...) + "."` is three nodes in one line. `add_nodes` builds the
join; the join itself knows only how to write its parts in a row.

## Moved Since the Draft
It lived in the same file as `Markdown`. It is a concrete inline node, so it
belongs here, and the base class no longer names any node.

## Flat
`(a + b) + c` and `a + (b + c)` give the same three parts, which keeps the
representation and the equality of joins simple.
"""
