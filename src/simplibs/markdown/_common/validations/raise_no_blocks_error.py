from typing import NoReturn
from simplibs.exception import ParamError


def raise_no_blocks_error(
    owner: str,
) -> NoReturn:
    """Raise ParamError when a container is created without any content.

    Args:
        owner: The container class (`"Quote"`, `"Document"`...).
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_NO_BLOCKS",
        label=f"{owner} content",
        problem=f"{owner} needs at least one block.",
        expected="At least one block, or a string for a plain paragraph.",
        how_to_fix=(
            f"Pass the content of the {owner} as arguments.",
            "Do not create the container when there is nothing to put in it.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_no_blocks_error — A Container With Nothing in It

## Purpose
An empty `Document`, `Quote` or footnote definition renders as nothing or as
a stray marker. The card names the container, so one raiser serves them all.

## Why It Lives in `_common`
Used by `Footnote` (`blocks`) and by `Quote` and `Document` (`containers`).
`List` has its own card for missing items.
"""
