from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_html_invalid_tag_error(
    tag: Any,
) -> NoReturn:
    """Raise ParamError when an HTML tag name is not valid.

    Args:
        tag: The rejected tag name.
    """

    # 1. A wrong kind of value is a TypeError, a wrong string is a ValueError
    is_text = isinstance(tag, str)

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_HTML_INVALID_TAG",
        label="HTML tag",
        value=tag,
        problem=(
            "A tag name starts with a letter and has no spaces or brackets."
            if is_text
            else "The tag name is not a string."
        ),
        expected="Letters, digits and '-', starting with a letter (e.g. 'details', 'my-tag').",
        how_to_fix=(
            "Pass only the name, without '<' and '>'.",
            "Pass attributes through `attrs`.",
        ),
        exception=ValueError if is_text else TypeError,
    )


_DESIGN_NOTES = """
# raise_html_invalid_tag_error — A Tag That Is Not a Name

## Purpose
`Html("div class=x")` would write a broken tag, and `Html("<div>")` would
double the brackets. The tag is only a name; the rest has its own parameters.

## One Card, Two Exceptions
A string that is not a valid name wraps `ValueError`; a value that is not a
string wraps `TypeError`.
"""
