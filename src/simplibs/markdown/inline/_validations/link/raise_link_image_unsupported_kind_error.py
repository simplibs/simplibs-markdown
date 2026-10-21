from typing import NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import LinkKind


def raise_link_image_unsupported_kind_error(
    kind: "LinkKind",
) -> NoReturn:
    """Raise ParamError when an image is requested as an autolink or a bare URL.

    Args:
        kind: The kind of the link being built (`AUTOLINK` or `BARE`).
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LINK_IMAGE_UNSUPPORTED_KIND",
        label="image flag",
        value=True,
        problem=(
            f"An image cannot use the link kind {kind.name}.",
            "Markdown has no image form for it.",
        ),
        expected="`image=False`, or a kind that supports images.",
        how_to_fix=(
            "Use INLINE, REFERENCE, COLLAPSED or SHORTCUT for an image.",
            "Set `image=False` to keep this kind.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_link_image_unsupported_kind_error — An Image Without an Image Syntax

## Purpose
`!<https://x.y>` is not an image. Only the four bracket forms can carry the
leading `!`.
"""
