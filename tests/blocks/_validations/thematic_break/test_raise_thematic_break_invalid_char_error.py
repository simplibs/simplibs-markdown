import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.thematic_break import (
    raise_thematic_break_invalid_char_error,
)


@pytest.mark.parametrize("char", ["-", "#", 1, None])
def test_raise_thematic_break_invalid_char_error_contract(subtests, char) -> None:
    """Verify raise_thematic_break_invalid_char_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_thematic_break_invalid_char_error,
        invalid_params=(char,),
        exception_type=ParamError,
        error_name="MARKDOWN_THEMATIC_BREAK_INVALID_CHAR",
        label="thematic break character",
        expected="BreakChar.DASH, BreakChar.ASTERISK or BreakChar.UNDERSCORE.",
        value=char,
        problem="Only a dash, an asterisk or an underscore can draw a thematic break.",
        how_to_fix=(
            "Pass one of the `BreakChar` members.",
            "Leave `char` out to get the dash.",
        ),
        exception=TypeError,
        verbose=False,
    )
