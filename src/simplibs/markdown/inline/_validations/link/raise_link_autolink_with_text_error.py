from typing import NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import LinkKind


def raise_link_autolink_with_text_error(
    kind: "LinkKind",
) -> NoReturn:
    """Raise ParamError when an autolink or a bare URL gets link text.

    Args:
        kind: The kind of the link being built (`AUTOLINK` or `BARE`).
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LINK_AUTOLINK_WITH_TEXT",
        label="link text",
        problem=(
            f"A link of kind {kind.name} shows its destination as the text.",
            "It cannot carry a separate text.",
        ),
        expected="`text` left as None.",
        how_to_fix=(
            "Remove `text`.",
            "Use LinkKind.INLINE when the link needs its own text.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_link_autolink_with_text_error — Text Nobody Would See

## Purpose
`<https://x.y>` and a bare URL are written as the address itself. A text
passed alongside would be dropped without a word.
"""
