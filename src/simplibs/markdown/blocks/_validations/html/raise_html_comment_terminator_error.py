from typing import NoReturn
from simplibs.exception import ParamError


def raise_html_comment_terminator_error(
    text: str,
) -> NoReturn:
    """Raise ParamError when comment text would end the comment early.

    Args:
        text: The rejected comment text.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_HTML_COMMENT_TERMINATOR",
        label="HTML comment text",
        value=text,
        problem=(
            "The text contains '-->' or starts with '>' or '->'.",
            "The comment would end early and the rest would become visible.",
        ),
        expected="Text without '-->' that does not start with '>' or '->'.",
        how_to_fix=(
            "Remove or rephrase the closing sequence.",
            "Put a space before a leading '>'.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_html_comment_terminator_error — A Comment That Ends Itself

## Purpose
Everything after an early `-->` is rendered as normal content. This matters
most when the comment text comes from outside, e.g. from a file.
"""
