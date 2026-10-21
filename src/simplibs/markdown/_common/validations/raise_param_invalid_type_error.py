from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_param_invalid_type_error(
    param_name: str,
    value: Any,
    expected: type | str,
) -> NoReturn:
    """Raise ParamError when a parameter has an unusable type.

    Args:
        param_name: The name of the offending parameter (`"kind"`).
        value: The rejected value.
        expected: The accepted type, or a short phrase when one type is not
            enough (`"str | Markdown"`, `"positive int"`).
    """

    # 1. A type is shown by its name, a phrase as it is
    expected_text = expected.__name__ if isinstance(expected, type) else expected

    # 2. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label=f"parameter '{param_name}'",
        value=value,
        problem=f"Parameter '{param_name}' received a value of the wrong type.",
        expected=expected_text,
        how_to_fix=f"Pass {expected_text} as '{param_name}'.",
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_param_invalid_type_error — One Type Guard for the Whole Library

## Purpose
Every node checks its constructor parameters by hand and every one of those
checks fails the same way: "this parameter has the wrong type". One card with
the parameter name and the expected type replaces a card per parameter.

## `expected`
Usually a class (`EmphasisKind`). A plain phrase is accepted for the cases
one class cannot describe (`"str | Markdown"`, `"positive int"`).

## Why It Lives in `_common`
Used by `inline`, `blocks`, `containers` and `output`.
"""
