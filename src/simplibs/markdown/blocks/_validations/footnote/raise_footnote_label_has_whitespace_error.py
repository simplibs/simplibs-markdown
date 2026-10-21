from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_footnote_label_has_whitespace_error(
    label: Any,
) -> NoReturn:
    """Raise ParamError when a footnote label is not a non-empty string without whitespace.

    Args:
        label: The rejected label.
    """

    # 1. A wrong kind of value is a TypeError, a wrong string is a ValueError
    is_text = isinstance(label, str)
    problem = (
        "A footnote label cannot be empty or contain whitespace."
        if is_text
        else "The label is not a string."
    )

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="MARKDOWN_FOOTNOTE_LABEL_INVALID",
        label="footnote label",
        value=label,
        problem=problem,
        expected="A non-empty string without spaces or tabs (e.g. '1', 'note').",
        how_to_fix=(
            "Use a short label such as '1' or 'source'.",
            "Replace spaces with '-' or '_'.",
        ),
        exception=ValueError if is_text else TypeError,
    )


_DESIGN_NOTES = """
# raise_footnote_label_has_whitespace_error — A Label That Ends at the Space

## Purpose
`[^my note]` is not a footnote reference, the renderer prints it as text.

## One Card, Two Exceptions
A string that is empty or has whitespace wraps `ValueError`; a value that is
not a string wraps `TypeError`.
"""
