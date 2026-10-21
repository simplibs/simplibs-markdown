import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.thematic_break import (
    raise_thematic_break_too_short_error,
)


@pytest.mark.parametrize(
    "length, problem, exception",
    [
        # A wrong number is a ValueError
        (2, "Markdown needs three characters to see a thematic break.", ValueError),
        (0, "Markdown needs three characters to see a thematic break.", ValueError),
        (-5, "Markdown needs three characters to see a thematic break.", ValueError),
        # A wrong kind of value is a TypeError (a bool is not a number here)
        ("3", "The length is not an integer.", TypeError),
        (2.5, "The length is not an integer.", TypeError),
        (None, "The length is not an integer.", TypeError),
        (True, "The length is not an integer.", TypeError),
    ],
)
def test_raise_thematic_break_too_short_error_contract(
    subtests, length, problem, exception
) -> None:
    """Verify raise_thematic_break_too_short_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_thematic_break_too_short_error,
        invalid_params=(length,),
        exception_type=ParamError,
        error_name="MARKDOWN_THEMATIC_BREAK_TOO_SHORT",
        label="thematic break length",
        expected="An integer of 3 or more.",
        value=length,
        problem=problem,
        how_to_fix="Pass 3 or more, or leave `length` out for the default.",
        exception=exception,
        verbose=False,
    )
