from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_html_invalid_attribute_error(
    name: Any,
) -> NoReturn:
    """Raise ParamError when an HTML attribute name is not valid.

    Args:
        name: The rejected attribute name.
    """

    # 1. A wrong kind of value is a TypeError, a wrong string is a ValueError
    is_text = isinstance(name, str)

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_HTML_INVALID_ATTRIBUTE",
        label="HTML attribute name",
        value=name,
        problem=(
            "An attribute name cannot contain spaces, quotes or '='."
            if is_text
            else "The attribute name is not a string."
        ),
        expected="Letters, digits and '-', '_', ':', '.', starting with a letter, '_' or ':'.",
        how_to_fix=(
            "Pass only the name as the key of `attrs`.",
            "Pass the value as the value of that key.",
        ),
        exception=ValueError if is_text else TypeError,
    )


_DESIGN_NOTES = """
# raise_html_invalid_attribute_error — An Attribute That Breaks the Tag

## Purpose
A name such as `onclick="x" id` would end the attribute and start another one.
Values are escaped by the node; names cannot be, so they are refused.

## One Card, Two Exceptions
A string that is not a valid name wraps `ValueError`; a value that is not a
string wraps `TypeError`.
"""
