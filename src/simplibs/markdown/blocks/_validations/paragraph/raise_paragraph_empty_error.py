from typing import NoReturn
from simplibs.exception import ParamError


def raise_paragraph_empty_error() -> NoReturn:
    """Raise ParamError when a paragraph has no non-empty line."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_PARAGRAPH_EMPTY",
        label="paragraph lines",
        problem=(
            "A paragraph needs at least one line with text.",
            "Empty lines separate blocks, they are not a block.",
        ),
        expected="At least one line with a visible character.",
        how_to_fix=(
            "Pass the text as one or more lines.",
            "Use BlankLine when you need an empty line.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_paragraph_empty_error — A Paragraph Made of Nothing

## Purpose
`Paragraph("", "  ")` would render as nothing and leave two blank lines
around it. An explicit empty line has its own node, `BlankLine`.
"""
