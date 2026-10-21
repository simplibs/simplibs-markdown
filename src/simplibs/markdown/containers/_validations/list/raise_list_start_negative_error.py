from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_list_start_negative_error(
    start: Any,
) -> NoReturn:
    """Raise ParamError when the start of a list is not a non-negative integer.

    Args:
        start: The rejected start number.
    """

    # 1. A wrong kind of value is a TypeError, a wrong number is a ValueError
    is_number = isinstance(start, int) and not isinstance(start, bool)
    problem = (
        "A list cannot start below zero."
        if is_number
        else "The start is not an integer."
    )

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_LIST_START_NEGATIVE",
        label="list start",
        value=start,
        problem=problem,
        expected="An integer of 0 or more.",
        how_to_fix="Pass the number of the first item, e.g. 1.",
        exception=ValueError if is_number else TypeError,
    )


_DESIGN_NOTES = """
# raise_list_start_negative_error — A List Counting Below Zero

## Purpose
`-1. item` is not an ordered list item. CommonMark allows up to nine digits
and no sign.

## One Card, Two Exceptions
A negative number wraps `ValueError`; a value that is not an integer wraps
`TypeError`.
"""
