import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline.enums import ReferenceKind
from simplibs.markdown.inline._validations.reference import (
    raise_reference_invalid_value_error,
)


@pytest.mark.parametrize(
    "kind, value, expected, kind_name",
    [
        # A one-word kind
        (ReferenceKind.MENTION, "bad name", "a GitHub username", "mention"),
        # An underscore in the kind becomes a space
        (ReferenceKind.REPO_ISSUE, "issue-12", "owner/repo#123", "repo issue"),
        (ReferenceKind.COMMIT, None, "a hexadecimal SHA", "commit"),
    ],
)
def test_raise_reference_invalid_value_error_contract(
    subtests, kind, value, expected, kind_name
) -> None:
    """Verify raise_reference_invalid_value_error words the kind and passes `expected` through."""

    assert_exception_function(
        subtests,
        raise_reference_invalid_value_error,
        invalid_params=(kind, value, expected),
        exception_type=ParamError,
        error_name="MARKDOWN_REFERENCE_INVALID_VALUE",
        label=f"{kind_name} reference",
        expected=expected,
        value=value,
        problem=f"The value does not fit a {kind_name} reference.",
        how_to_fix=(
            "Check the value against the expected form.",
            "Use another ReferenceKind when it is a different kind of reference.",
        ),
        exception=ValueError,
        verbose=False,
    )
