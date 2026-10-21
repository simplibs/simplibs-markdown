from typing import NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import EmphasisKind, EmphasisMarker


def raise_emphasis_marker_kind_mismatch_error(
    kind: "EmphasisKind",
    marker: "EmphasisMarker",
) -> NoReturn:
    """Raise ParamError when the marker cannot express the emphasis kind.

    Args:
        kind: The requested kind of emphasis.
        marker: The rejected marker.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_EMPHASIS_MARKER_KIND_MISMATCH",
        label="emphasis marker",
        value=marker,
        problem=(
            f"The marker {marker.name} cannot express {kind.name}.",
            "Strike-through is written with '~', everything else with '*' or '_'.",
        ),
        expected="'~' for STRIKE; '*' or '_' for EM, STRONG and STRONG_EM.",
        how_to_fix=(
            "Leave `marker` out to get the default for this kind.",
            "Or pick a marker that fits the kind.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_emphasis_marker_kind_mismatch_error — A Marker for the Wrong Kind

## Purpose
`~~text~~` is strike-through and `*text*` is emphasis; swapping the markers
would silently produce a different element. The check runs when the node
is built.

## Enums as Annotations Only
`EmphasisKind` and `EmphasisMarker` are imported under `TYPE_CHECKING`, so the
raiser has no import dependency on the enums at runtime.
"""
