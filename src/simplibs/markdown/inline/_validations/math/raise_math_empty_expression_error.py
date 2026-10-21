from typing import NoReturn
from simplibs.exception import ParamError


def raise_math_empty_expression_error(
    expr: str,
) -> NoReturn:
    """Raise ParamError when a math expression is empty or only whitespace.

    Args:
        expr: The rejected expression.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_MATH_EMPTY_EXPRESSION",
        label="math expression",
        value=expr,
        problem="A math expression needs visible content.",
        expected="Text with at least one non-whitespace character.",
        how_to_fix=(
            "Pass the expression, e.g. 'E = mc^2'.",
            "Leave the element out when there is no expression.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_math_empty_expression_error — Dollar Signs Around Nothing

## Purpose
`$$` and `$ $` are not an expression; renderers print them as text or as an
error box. The card is raised at construction.
"""
