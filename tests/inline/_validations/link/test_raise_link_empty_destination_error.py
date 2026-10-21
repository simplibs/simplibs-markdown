import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline.enums import LinkKind
from simplibs.markdown.inline._validations.link import (
    raise_link_empty_destination_error,
)


@pytest.mark.parametrize(
    "kind, dest",
    [
        (LinkKind.INLINE, None),
        (LinkKind.INLINE, ""),
        (LinkKind.AUTOLINK, ""),
        (LinkKind.REFERENCE, None),
    ],
)
def test_raise_link_empty_destination_error_contract(subtests, kind, dest) -> None:
    """Verify raise_link_empty_destination_error names the link kind."""

    assert_exception_function(
        subtests,
        raise_link_empty_destination_error,
        invalid_params=(kind, dest),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_EMPTY_DESTINATION",
        label="link destination",
        expected="A non-empty URL or path.",
        value=dest,
        problem=f"A link of kind {kind.name} needs a destination.",
        how_to_fix=(
            "Pass the target as `dest`.",
            "Leave the link out when there is nowhere to point.",
        ),
        exception=ValueError,
        verbose=False,
    )
