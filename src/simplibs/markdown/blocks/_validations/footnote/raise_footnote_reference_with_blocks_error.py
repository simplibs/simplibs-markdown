from typing import NoReturn
from simplibs.exception import ParamError


def raise_footnote_reference_with_blocks_error(
    label: str,
) -> NoReturn:
    """Raise ParamError when a footnote reference gets blocks.

    Args:
        label: The label of the footnote.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_FOOTNOTE_REFERENCE_WITH_BLOCKS",
        label=f"footnote '{label}'",
        value=label,
        problem=(
            "A reference is only the marker in the text.",
            "The content belongs to the definition.",
        ),
        expected="No blocks for FootnoteRole.REFERENCE.",
        how_to_fix=(
            "Remove the blocks from the reference.",
            "Create a second Footnote with FootnoteRole.DEFINITION for the content.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_footnote_reference_with_blocks_error — Content in the Wrong Place

## Purpose
`[^1]` carries no text, so blocks passed to it would vanish from the output.
"""
