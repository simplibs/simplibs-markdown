# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
# Inners
from ._validations.thematic_break import (
    raise_thematic_break_invalid_char_error,
    raise_thematic_break_too_short_error,
)
from .enums import BreakChar


class ThematicBreak(Markdown):
    """A horizontal rule.

    Args:
        char: The character that draws the rule.
        length: How many characters to write; at least 3.

    Raises:
        ParamError: If `char` is not a `BreakChar` or `length` is below 3.
    """

    __slots__ = ("char", "length")

    node_level = NodeLevel.BLOCK

    def __init__(self, char: BreakChar = BreakChar.DASH, length: int = 3) -> None:

        # 1. Validation
        if not isinstance(char, BreakChar):
            raise_thematic_break_invalid_char_error(char)
        if isinstance(length, bool) or not isinstance(length, int) or length < 3:
            raise_thematic_break_too_short_error(length)

        # 2. Assignment
        self.char = char
        self.length = length

    def to_lines(self) -> tuple[str, ...]:

        # 1. The character repeated
        return (self.char.value * self.length,)


_DESIGN_NOTES = """
# ThematicBreak — A Rule That Is Not a Heading Underline

## Purpose
`---`, `***` and `___` draw a rule. A dash rule right under a line of text
would be a setext underline, but the node is a block and a blank line always
separates it from the previous block.
"""
