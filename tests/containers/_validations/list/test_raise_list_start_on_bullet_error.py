import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.list import (
    raise_list_start_on_bullet_error,
)


@pytest.mark.parametrize("start", [0, 2, 10])
def test_raise_list_start_on_bullet_error_contract(subtests, start) -> None:
    """Verify raise_list_start_on_bullet_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_list_start_on_bullet_error,
        invalid_params=(start,),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_START_ON_BULLET",
        label="list start",
        expected="`start=1` (the default) for a bullet list.",
        value=start,
        problem="Only an ordered list has numbers to start from.",
        how_to_fix=(
            "Remove `start`.",
            "Use `ordered=True` to number the list.",
        ),
        exception=ValueError,
        verbose=False,
    )
