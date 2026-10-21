# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.validations import raise_param_invalid_type_error


class BlankLine(Markdown):
    """One or more explicit empty lines.

    Args:
        count: How many empty lines.

    Raises:
        ParamError: If `count` is not a positive integer.
    """

    __slots__ = ("count",)

    node_level = NodeLevel.BLOCK

    def __init__(self, count: int = 1) -> None:

        # 1. Validation
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise_param_invalid_type_error("count", count, "positive int")

        # 2. Assignment
        self.count = count

    def to_lines(self) -> tuple[str, ...]:

        # 1. Empty strings, one per line
        return ("",) * self.count


_DESIGN_NOTES = """
# BlankLine — Space That the Author Asked For

## Purpose
Blocks are separated by one blank line automatically. This node sets the
number of blank lines at its place, and it is what `""` becomes in a block
slot.

## Replaces the Separator, Does Not Add to It
`separate_blocks` writes no separator next to a `BlankLine`. `BlankLine(1)`
therefore gives the same single blank line as no node at all, and
`BlankLine(3)` gives three blank lines in total, not four.
"""
