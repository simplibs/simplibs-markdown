import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline._validations.entity import (
    raise_entity_codepoint_out_of_range_error,
)

_NUMBER_PROBLEM = "The code point lies outside the Unicode range."
_TYPE_PROBLEM = "The code point is not an integer."


@pytest.mark.parametrize(
    "codepoint, problem, exception",
    [
        # A wrong number is a ValueError
        (-1, _NUMBER_PROBLEM, ValueError),
        (0x110000, _NUMBER_PROBLEM, ValueError),
        # A wrong kind of value is a TypeError (a bool is not a number here)
        ("169", _TYPE_PROBLEM, TypeError),
        (169.0, _TYPE_PROBLEM, TypeError),
        (None, _TYPE_PROBLEM, TypeError),
        (True, _TYPE_PROBLEM, TypeError),
    ],
)
def test_raise_entity_codepoint_out_of_range_error_contract(
    subtests, codepoint, problem, exception
) -> None:
    """Verify raise_entity_codepoint_out_of_range_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_entity_codepoint_out_of_range_error,
        invalid_params=(codepoint,),
        exception_type=ParamError,
        error_name="MARKDOWN_ENTITY_CODEPOINT_OUT_OF_RANGE",
        label="entity code point",
        expected="An integer from 0 to 0x10FFFF.",
        value=codepoint,
        problem=problem,
        how_to_fix=(
            "Pass the code point as an integer, e.g. 169 or 0xA9.",
            "Use `name=` when the character has an HTML name.",
        ),
        exception=exception,
        verbose=False,
    )
