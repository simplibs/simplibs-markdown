# Outers
from ..base_class import InlineMarkdown
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import escape_text


class Text(InlineMarkdown):
    """Plain text. Characters with a Markdown meaning are escaped.

    Args:
        value: The text.
        escape: `False` writes the text as it is, so it can carry raw Markdown.

    Raises:
        ParamError: If `value` is not a string.
    """

    __slots__ = ("value", "escape")

    def __init__(self, value: str, escape: bool = True) -> None:

        # 1. Validation
        if not isinstance(value, str):
            raise_param_invalid_type_error("value", value, str)

        # 2. Assignment
        self.value = value
        self.escape = escape

    def to_inline(self) -> str:

        # 1. Escape the text unless it was meant as raw Markdown
        return escape_text(self.value) if self.escape else self.value


_DESIGN_NOTES = """
# Text — A String Is Content, Not Markdown

## Purpose
Every string passed into the library becomes `Text`, so its characters are
escaped and nothing in it is read as formatting.

## `escape=False`
The way out when a string is Markdown already, e.g. text that was generated
elsewhere. Nothing in the library sets it.

## Why Escaping Is the Default
The opposite choice would make `Paragraph("2024. was a year")` a list and
`Paragraph("a_b_c")` emphasis, with no error and no warning.
"""
