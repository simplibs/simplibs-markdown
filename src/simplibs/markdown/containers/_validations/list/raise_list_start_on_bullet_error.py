from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_list_start_on_bullet_error(
    start: Any,
) -> NoReturn:
    """Raise ParamError when a bullet list gets a start number.

    Args:
        start: The rejected start number.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LIST_START_ON_BULLET",
        label="list start",
        value=start,
        problem="Only an ordered list has numbers to start from.",
        expected="`start=1` (the default) for a bullet list.",
        how_to_fix=(
            "Remove `start`.",
            "Use `ordered=True` to number the list.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_list_start_on_bullet_error — A Number Without Numbering

## Purpose
`start=5` on a bullet list would be accepted and ignored. Refusing it shows
the mistake where it was made.
"""
