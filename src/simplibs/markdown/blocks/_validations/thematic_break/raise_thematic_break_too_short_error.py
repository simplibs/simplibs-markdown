from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_thematic_break_too_short_error(
    length: Any,
) -> NoReturn:
    """Raise ParamError when a thematic break has fewer than 3 characters.

    Args:
        length: The rejected length.
    """

    # 1. A wrong kind of value is a TypeError, a wrong number is a ValueError
    is_number = isinstance(length, int) and not isinstance(length, bool)
    problem = (
        "Markdown needs three characters to see a thematic break."
        if is_number
        else "The length is not an integer."
    )

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_THEMATIC_BREAK_TOO_SHORT",
        label="thematic break length",
        value=length,
        problem=problem,
        expected="An integer of 3 or more.",
        how_to_fix="Pass 3 or more, or leave `length` out for the default.",
        exception=ValueError if is_number else TypeError,
    )


_DESIGN_NOTES = """
# raise_thematic_break_too_short_error — Two Dashes Are Just Text

## Purpose
`--` is a paragraph, and under a line of text it is a setext underline.

## One Card, Two Exceptions
A number below 3 wraps `ValueError`; a value that is not an integer wraps
`TypeError`.
"""
