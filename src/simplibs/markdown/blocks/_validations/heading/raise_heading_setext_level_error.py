from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_heading_setext_level_error(
    level: Any,
) -> NoReturn:
    """Raise ParamError when a setext heading has a level above 2.

    Args:
        level: The rejected level.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_HEADING_SETEXT_LEVEL",
        label="heading level",
        value=level,
        problem=(
            "The setext style underlines the text with '=' or '-'.",
            "That gives only two levels.",
        ),
        expected="Level 1 or 2 for a setext heading.",
        how_to_fix=(
            "Use HeadingStyle.ATX for levels 3 to 6.",
            "Lower the level to 1 or 2.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_heading_setext_level_error — Two Underlines, Two Levels

## Purpose
Setext headings have no way to write a third level; the output would silently
be a different heading.
"""
