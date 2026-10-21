# Outers
from ...blocks import CodeBlock


def MATH_BLOCK(expr: str) -> CodeBlock:
    """Build a block that renders as a formula.

    Init Params:
        expr (str): The formula in LaTeX syntax.

    Markdown:
        A fenced code block with the info string `math`.

    Example:
        MATH_BLOCK("E = mc^2")
        # Writes:
        # ```math
        # E = mc^2
        # ```

    Note:
        For a formula inside a line, use `Math`.
    """
    return CodeBlock(expr, info="math")
