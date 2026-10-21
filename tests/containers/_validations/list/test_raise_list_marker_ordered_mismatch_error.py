import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers.enums import ListMarker
from simplibs.markdown.containers._validations.list import (
    raise_list_marker_ordered_mismatch_error,
)


@pytest.mark.parametrize(
    "ordered, marker, list_kind",
    [
        # Bullet markers in an ordered list
        (True, ListMarker.DASH, "ordered"),
        (True, ListMarker.ASTERISK, "ordered"),
        (True, ListMarker.PLUS, "ordered"),
        # Ordered markers in a bullet list
        (False, ListMarker.DOT, "bullet"),
        (False, ListMarker.PAREN, "bullet"),
    ],
)
def test_raise_list_marker_ordered_mismatch_error_contract(
    subtests, ordered, marker, list_kind
) -> None:
    """Verify raise_list_marker_ordered_mismatch_error names the marker and the list kind."""

    assert_exception_function(
        subtests,
        raise_list_marker_ordered_mismatch_error,
        invalid_params=(ordered, marker),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_MARKER_ORDERED_MISMATCH",
        label="list marker",
        expected="DOT or PAREN for an ordered list; DASH, ASTERISK or PLUS for a bullet list.",
        value=marker,
        problem=f"The marker {marker.name} cannot be used in {list_kind} lists.",
        how_to_fix=(
            "Leave `marker` out to get the default for this list.",
            "Or pick a marker that fits the kind of list.",
        ),
        exception=ValueError,
        verbose=False,
    )
