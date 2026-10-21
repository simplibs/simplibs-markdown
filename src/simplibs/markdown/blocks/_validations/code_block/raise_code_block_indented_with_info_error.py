from typing import NoReturn
from simplibs.exception import ParamError


def raise_code_block_indented_with_info_error(
    info: str,
) -> NoReturn:
    """Raise ParamError when an indented code block gets an info string.

    Args:
        info: The rejected info string.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_CODE_BLOCK_INDENTED_WITH_INFO",
        label="code block info",
        value=info,
        problem=(
            "An indented code block has no fence.",
            "There is no place to write the info string.",
        ),
        expected="No info string for an indented block.",
        how_to_fix=(
            "Remove `info`.",
            "Use a fenced block (`indented=False`) to name the language.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_code_block_indented_with_info_error — A Language With Nowhere to Go

## Purpose
The info string lives on the fence line. Dropping it silently would lose the
language and the syntax highlighting.
"""
