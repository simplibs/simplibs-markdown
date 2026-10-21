# Outers
from ..base_class import InlineMarkdown
from .._common.enums import LineBreakStyle
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import LINE_BREAKS


class LineBreak(InlineMarkdown):
    """A hard line break inside a paragraph.

    Args:
        style: How the break is written.

    Raises:
        ParamError: If `style` is not a `LineBreakStyle`.
    """

    __slots__ = ("style",)

    def __init__(self, style: LineBreakStyle = LineBreakStyle.SPACES) -> None:

        # 1. Validation
        if not isinstance(style, LineBreakStyle):
            raise_param_invalid_type_error("style", style, LineBreakStyle)

        # 2. Assignment
        self.style = style

    def to_inline(self) -> str:

        # 1. The text of each style is in one table
        return LINE_BREAKS[self.style]


_DESIGN_NOTES = """
# LineBreak — A Break the Renderer Must Keep

## Purpose
A single newline in a paragraph is a space. A hard break needs one of three
spellings, and the author should choose it on purpose.

## Which Style
`SPACES` is invisible in an editor and often removed by one; `BACKSLASH` and
`HTML` survive. `HTML` is the only one that stays inside the line, which is
why a table cell can use it.
"""
