from typing import NoReturn
from simplibs.exception import ParamError


def raise_heading_empty_setext_error() -> NoReturn:
    """Raise ParamError when a setext heading has no text."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_HEADING_EMPTY_SETEXT",
        label="heading text",
        problem=(
            "A setext heading is the text with an underline below it.",
            "An underline alone is a thematic break.",
        ),
        expected="Text with at least one visible character.",
        how_to_fix=(
            "Pass the heading text.",
            "Use ThematicBreak when a line is all you need.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_heading_empty_setext_error — An Underline Without a Title

## Purpose
`===` on its own line is not a heading, and `---` is a rule. An ATX heading
may be empty (`#`), a setext heading may not.
"""
