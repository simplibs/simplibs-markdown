# Outers
from ..base_class import InlineMarkdown
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._validations.math import raise_math_empty_expression_error


class Math(InlineMarkdown):
    """A math expression in `$...$` (inline) or `$$...$$` (display).

    Args:
        expr: The expression, written in LaTeX.
        display: `True` writes the display form.

    Raises:
        ParamError: If `expr` is not a string or has no visible content.
    """

    __slots__ = ("expr", "display")

    def __init__(self, expr: str, display: bool = False) -> None:

        # 1. Validation
        if not isinstance(expr, str):
            raise_param_invalid_type_error("expr", expr, str)
        if not expr.strip():
            raise_math_empty_expression_error(expr)

        # 2. Assignment
        self.expr = expr.strip()
        self.display = display

    def to_inline(self) -> str:

        # 1. One dollar for inline math, two for display math
        mark = "$$" if self.display else "$"
        return f"{mark}{self.expr}{mark}"


_DESIGN_NOTES = """
# Math — Why It Is Not `Text`

## Purpose
`Text` escapes `$`, so an expression written as a string would never be math.
This node writes the dollars on purpose.

## Known Limit
The expression is written as given. A `$` inside it is not escaped, so it can
end the math early; GitHub expects `\\$` there.
"""
