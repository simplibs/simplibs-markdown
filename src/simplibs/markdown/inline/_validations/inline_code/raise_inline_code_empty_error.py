from typing import NoReturn
from simplibs.exception import ParamError


def raise_inline_code_empty_error(
    text: str,
) -> NoReturn:
    """Raise ParamError when inline code is empty or only whitespace.

    Args:
        text: The rejected code text.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_INLINE_CODE_EMPTY",
        label="inline code",
        value=text,
        problem="Inline code needs visible content.",
        expected="Text with at least one non-whitespace character.",
        how_to_fix=(
            "Pass the code to show.",
            "Leave the element out when there is nothing to show.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_inline_code_empty_error — Code Spans With No Code

## Purpose
Backticks around nothing do not form a code span in CommonMark; they are
printed as two stray characters. The card prevents that at construction.
"""
