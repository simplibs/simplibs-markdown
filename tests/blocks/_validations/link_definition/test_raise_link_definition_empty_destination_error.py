import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.link_definition import (
    raise_link_definition_empty_destination_error,
)


@pytest.mark.parametrize("dest", [None, ""])
def test_raise_link_definition_empty_destination_error_contract(subtests, dest) -> None:
    """Verify raise_link_definition_empty_destination_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_link_definition_empty_destination_error,
        invalid_params=(dest,),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_DEFINITION_EMPTY_DESTINATION",
        label="link definition destination",
        expected="A non-empty URL or path.",
        value=dest,
        problem="A definition exists to say where a label points.",
        how_to_fix=(
            "Pass the target as `dest`.",
            "Leave the definition out when there is no target.",
        ),
        exception=ValueError,
        verbose=False,
    )
