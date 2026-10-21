import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline.enums import EmphasisKind, EmphasisMarker
from simplibs.markdown.inline._validations.emphasis import (
    raise_emphasis_marker_kind_mismatch_error,
)


@pytest.mark.parametrize(
    "kind, marker",
    [
        # Strike-through needs a tilde
        (EmphasisKind.STRIKE, EmphasisMarker.ASTERISK),
        (EmphasisKind.STRIKE, EmphasisMarker.UNDERSCORE),
        # Everything else cannot use a tilde
        (EmphasisKind.EM, EmphasisMarker.TILDE),
        (EmphasisKind.STRONG, EmphasisMarker.TILDE),
        (EmphasisKind.STRONG_EM, EmphasisMarker.TILDE),
    ],
)
def test_raise_emphasis_marker_kind_mismatch_error_contract(subtests, kind, marker) -> None:
    """Verify raise_emphasis_marker_kind_mismatch_error names the marker and the kind."""

    assert_exception_function(
        subtests,
        raise_emphasis_marker_kind_mismatch_error,
        invalid_params=(kind, marker),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_MARKER_KIND_MISMATCH",
        label="emphasis marker",
        expected="'~' for STRIKE; '*' or '_' for EM, STRONG and STRONG_EM.",
        value=marker,
        problem=(
            f"The marker {marker.name} cannot express {kind.name}.",
            "Strike-through is written with '~', everything else with '*' or '_'.",
        ),
        how_to_fix=(
            "Leave `marker` out to get the default for this kind.",
            "Or pick a marker that fits the kind.",
        ),
        exception=ValueError,
        verbose=False,
    )
