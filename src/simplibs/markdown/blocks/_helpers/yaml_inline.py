import json
from typing import Any
# Outers
from .._validations.frontmatter import raise_frontmatter_not_serializable_error


def yaml_inline(value: Any) -> str:
    """Write a scalar, or an empty list or dictionary, as one YAML token.

    Args:
        value: `None`, a bool, an int, a finite float, a string, or an empty
            list, tuple or dictionary.

    Returns:
        The YAML text of the value.

    Raises:
        ConversionError: If the value has no inline YAML form.
    """

    # 1. The words YAML knows
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"

    # 2. Numbers; NaN and infinity have no YAML form here
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise_frontmatter_not_serializable_error(value)
        return repr(value)

    # 3. Strings are always quoted, so `"yes"` never turns into a boolean
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)

    # 4. Empty collections stay on the line of their key
    if isinstance(value, dict) and not value:
        return "{}"
    if isinstance(value, (list, tuple)) and not value:
        return "[]"

    # 5. Anything else is not supported
    raise_frontmatter_not_serializable_error(value)


_DESIGN_NOTES = """
# yaml_inline — Everything That Fits on One Line

## Purpose
Scalars and empty collections. A non-empty collection spans lines and is
written by `yaml_lines`.

## Strings Are Always Quoted
`"2024-01-01"`, `"yes"` and `"1.0"` would otherwise be read as a date, a
boolean and a number. Quoting costs readability and removes the guessing.

## Order Matters
`True` is tested before `int`, because a bool is an int in Python.
"""
