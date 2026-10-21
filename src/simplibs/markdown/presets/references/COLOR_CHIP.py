# Outers
from ...inline import InlineCode


def COLOR_CHIP(color: str) -> InlineCode:
    """Build a color code that GitHub shows with a color swatch.

    Init Params:
        color (str): The color as `#RRGGBB`, `rgb(...)` or `hsl(...)`.

    Markdown:
        The color as inline code (`` `#0969DA` ``).

    Example:
        COLOR_CHIP("#0969DA")
        # Writes: "`#0969DA`"

    Note:
        GitHub draws a small swatch next to such a code span; other renderers show plain
        code. The color is not checked.
    """
    return InlineCode(color)
