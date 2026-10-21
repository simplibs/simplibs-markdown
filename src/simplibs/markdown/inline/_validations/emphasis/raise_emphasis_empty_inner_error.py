from typing import NoReturn
from simplibs.exception import ParamError


def raise_emphasis_empty_inner_error(
    inner_text: str,
) -> NoReturn:
    """Raise ParamError when the emphasized content is empty or only whitespace.

    Args:
        inner_text: The rendered text of the content.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_EMPHASIS_EMPTY_INNER",
        label="emphasis content",
        value=inner_text,
        problem=(
            "Emphasis needs something to emphasize.",
            "Markers around nothing are only stray punctuation.",
        ),
        expected="Content with at least one visible character.",
        how_to_fix=(
            "Pass the text to emphasize.",
            "Leave the emphasis out when there is nothing to emphasize.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_emphasis_empty_inner_error — Emphasis Around Nothing

## Purpose
`****` or `* *` is not emphasis. The card is raised when the node is built,
so an empty node never reaches the output.

## `inner_text`
It is shown as the value, so a whitespace-only input is visible in the card.
"""
