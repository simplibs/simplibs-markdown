from typing import NoReturn
from simplibs.exception import ParamError


def raise_heading_multiline_error(
    text: str,
) -> NoReturn:
    """Raise ParamError when the heading text spans several lines.

    Args:
        text: The rejected text.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_HEADING_MULTILINE",
        label="heading text",
        value=text,
        problem=(
            "A heading is one line.",
            "A line break would end the heading and start a paragraph.",
        ),
        expected="Text without line breaks.",
        how_to_fix=(
            "Shorten the heading to a single line.",
            "Put the rest into a Paragraph below the heading.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_heading_multiline_error — A Heading That Breaks in Two

## Purpose
`# first\\nsecond` is a heading followed by a paragraph. Refusing it keeps the
mistake from turning into a quiet change of structure.
"""
