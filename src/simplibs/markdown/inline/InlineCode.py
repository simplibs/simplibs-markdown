# Outers
from ..base_class import InlineMarkdown
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import choose_code_delimiter
from ._validations.inline_code import raise_inline_code_empty_error


class InlineCode(InlineMarkdown):
    """A code span. The backticks around it are chosen to fit its content.

    Args:
        text: The code. Line breaks become spaces.

    Raises:
        ParamError: If `text` is not a string or has no visible content.
    """

    __slots__ = ("text",)

    def __init__(self, text: str) -> None:

        # 1. Validation
        if not isinstance(text, str):
            raise_param_invalid_type_error("text", text, str)
        if not text.strip():
            raise_inline_code_empty_error(text)

        # 2. Assignment; a code span lives on one line
        self.text = text.replace("\n", " ")

    def to_inline(self) -> str:

        # 1. The delimiter and the padding depend on the backticks inside the code
        delimiter, body = choose_code_delimiter(self.text)
        return delimiter + body + delimiter


_DESIGN_NOTES = """
# InlineCode — Code With Any Content

## Purpose
`` `a`b` `` ends after `a`. The node picks a longer delimiter, so any text can
be code and nothing needs escaping inside it.

## Line Breaks
Become spaces, which is what renderers do with them anyway. A code span that
stays on one line also keeps table cells and headings valid.
"""
