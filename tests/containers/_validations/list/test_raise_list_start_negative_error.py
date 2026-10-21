import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.containers._validations.list import (
    raise_list_start_negative_error,
)


@pytest.mark.parametrize(
    "start, problem, exception",
    [
        # A wrong number is a ValueError
        (-1, "A list cannot start below zero.", ValueError),
        (-100, "A list cannot start below zero.", ValueError),
        # A wrong kind of value is a TypeError (a bool is not a number here)
        ("1", "The start is not an integer.", TypeError),
        (1.5, "The start is not an integer.", TypeError),
        (None, "The start is not an integer.", TypeError),
        (True, "The start is not an integer.", TypeError),
    ],
)
def test_raise_list_start_negative_error_contract(
    subtests, start, problem, exception
) -> None:
    """Verify raise_list_start_negative_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_list_start_negative_error,
        invalid_params=(start,),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_START_NEGATIVE",
        label="list start",
        expected="An integer of 0 or more.",
        value=start,
        problem=problem,
        how_to_fix="Pass the number of the first item, e.g. 1.",
        exception=exception,
        verbose=False,
    )
