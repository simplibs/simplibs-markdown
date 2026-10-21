from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_heading_level_out_of_range_error(
    level: Any,
) -> NoReturn:
    """Raise ParamError when a heading level is not an integer from 1 to 6.

    Args:
        level: The rejected level.
    """

    # 1. A wrong kind of value is a TypeError, a wrong number is a ValueError
    is_number = isinstance(level, int) and not isinstance(level, bool)
    problem = (
        "Markdown has six heading levels."
        if is_number
        else "The level is not an integer."
    )

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_HEADING_LEVEL_OUT_OF_RANGE",
        label="heading level",
        value=level,
        problem=problem,
        expected="An integer from 1 to 6.",
        how_to_fix=(
            "Pass a level from 1 (the biggest) to 6 (the smallest).",
            "Use the presets H1 to H6 to avoid the number.",
        ),
        exception=ValueError if is_number else TypeError,
    )


_DESIGN_NOTES = """
# raise_heading_level_out_of_range_error — A Seventh Heading Level

## Purpose
`#######` is not a heading, it is a paragraph that starts with hashes.

## One Card, Two Exceptions
A number outside 1–6 wraps `ValueError`; anything that is not an integer
(`"2"`, `True`, `None`) wraps `TypeError`.
"""
