from abc import abstractmethod
# Inners
from .enums import NodeLevel
from .Markdown import Markdown


class InlineMarkdown(Markdown):
    """The base of nodes that live inside a line and render as one string."""

    __slots__ = ()

    node_level = NodeLevel.INLINE

    @abstractmethod
    def to_inline(self) -> str:
        """Render the node as a string that can stand inside a line."""
        raise NotImplementedError

    def to_text(self) -> str:

        # 1. An inline node is already one string
        return self.to_inline()

    def to_lines(self) -> tuple[str, ...]:

        # 1. Only text with a line break inside gives more than one line
        return tuple(self.to_inline().split("\n"))


_DESIGN_NOTES = """
# InlineMarkdown — A Node Inside a Line

## Purpose
Text, emphasis, links and the other inline nodes only differ in how they
write themselves, so each implements `to_inline()` and gets `to_text()` and
`to_lines()` for free.

## `to_text()` Does Not Go Through the Lines
The default `to_text()` of `Markdown` joins the lines. For an inline node the
string is already there, so it is returned as it is.
"""
