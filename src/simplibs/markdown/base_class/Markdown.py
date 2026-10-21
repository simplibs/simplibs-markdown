from abc import ABC, abstractmethod
from typing import Any
# Outers
from .._common.helpers import add_nodes
# Inners
from .enums import NodeLevel


class Markdown(ABC):
    """The base of every Markdown node.

    A node renders as a tuple of lines (`to_lines`) or as one text (`to_text`)
    and is composed with `+`.
    """

    __slots__ = ()

    node_level: NodeLevel

    # ----------------------------------------------------------------------
    # Rendering
    # ----------------------------------------------------------------------
    @abstractmethod
    def to_lines(self) -> tuple[str, ...]:
        """Render the node as lines without line endings."""
        raise NotImplementedError

    def to_text(self) -> str:
        """Render the node as one text."""

        # 1. The lines are the single source of truth
        return "\n".join(self.to_lines())

    # ----------------------------------------------------------------------
    # Dunder methods
    # ----------------------------------------------------------------------
    def __str__(self) -> str:
        return self.to_text()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.to_text()!r})"

    def __add__(self, other: Any) -> Any:

        # 1. The composition rules live in one helper
        return add_nodes(self, other)

    def __radd__(self, other: Any) -> Any:

        # 1. Same rules, the other operand stands on the left
        return add_nodes(other, self)


_DESIGN_NOTES = """
# Markdown — The Contract of Every Node

## Purpose
One abstract class says what a node is: it knows its `node_level`, renders
itself as lines, and can be added to another node or to a string.

## Lines Are the Source of Truth
`to_lines()` returns a tuple of lines, `to_text()` only joins them. A tuple of
lines is what can be nested safely — a quote or a list prefixes every line of
the block inside it.

## `+` Is One Helper
`__add__` and `__radd__` hand both operands to `add_nodes` (`_common/helpers`).
This file therefore names no concrete node, and the base class stays below
the nodes in the import graph.

## `node_level`
A class attribute set by the subclass (`NodeLevel.INLINE` or `BLOCK`). It is
named `node_level`, not `level`, because `Heading.level` is the number of the
heading.
"""
