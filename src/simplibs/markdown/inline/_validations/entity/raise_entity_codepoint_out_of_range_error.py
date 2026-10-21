from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_entity_codepoint_out_of_range_error(
    codepoint: Any,
) -> NoReturn:
    """Raise ParamError when a code point is not a valid Unicode value.

    Args:
        codepoint: The rejected value.
    """

    # 1. A wrong kind of value is a TypeError, a wrong number is a ValueError
    is_number = isinstance(codepoint, int) and not isinstance(codepoint, bool)
    problem = (
        "The code point lies outside the Unicode range."
        if is_number
        else "The code point is not an integer."
    )

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_ENTITY_CODEPOINT_OUT_OF_RANGE",
        label="entity code point",
        value=codepoint,
        problem=problem,
        expected="An integer from 0 to 0x10FFFF.",
        how_to_fix=(
            "Pass the code point as an integer, e.g. 169 or 0xA9.",
            "Use `name=` when the character has an HTML name.",
        ),
        exception=ValueError if is_number else TypeError,
    )


_DESIGN_NOTES = """
# raise_entity_codepoint_out_of_range_error — Not a Unicode Value

## Purpose
`&#1114112;` is one past the last code point. Browsers show a replacement
character; the card stops it earlier.

## One Card, Two Exceptions
A number outside the range wraps `ValueError`, a value that is not a number
at all wraps `TypeError`, so the caller can catch them by the native type.
"""
