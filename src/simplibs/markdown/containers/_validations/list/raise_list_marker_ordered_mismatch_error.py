from typing import NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import ListMarker


def raise_list_marker_ordered_mismatch_error(
    ordered: bool,
    marker: "ListMarker",
) -> NoReturn:
    """Raise ParamError when the marker does not fit the kind of list.

    Args:
        ordered: Whether the list is ordered.
        marker: The rejected marker.
    """

    # 1. Name the kind of list in words
    list_kind = "ordered" if ordered else "bullet"

    # 2. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LIST_MARKER_ORDERED_MISMATCH",
        label="list marker",
        value=marker,
        problem=f"The marker {marker.name} cannot be used in {list_kind} lists.",
        expected="DOT or PAREN for an ordered list; DASH, ASTERISK or PLUS for a bullet list.",
        how_to_fix=(
            "Leave `marker` out to get the default for this list.",
            "Or pick a marker that fits the kind of list.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_list_marker_ordered_mismatch_error — `1-` and `* ` Swapped

## Purpose
`1- item` is not a list item and `* item` cannot be numbered. The check runs
when the list is built.

## Enums as Annotations Only
`ListMarker` is imported under `TYPE_CHECKING`, so the raiser has no import
dependency on the enum at runtime.
"""
