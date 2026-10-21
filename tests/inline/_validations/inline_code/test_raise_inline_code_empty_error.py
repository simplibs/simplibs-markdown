import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline._validations.inline_code import (
    raise_inline_code_empty_error,
)


@pytest.mark.parametrize("text", ["", "   ", "\t"])
def test_raise_inline_code_empty_error_contract(subtests, text) -> None:
    """Verify raise_inline_code_empty_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_inline_code_empty_error,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_INLINE_CODE_EMPTY",
        label="inline code",
        expected="Text with at least one non-whitespace character.",
        value=text,
        problem="Inline code needs visible content.",
        how_to_fix=(
            "Pass the code to show.",
            "Leave the element out when there is nothing to show.",
        ),
        exception=ValueError,
        verbose=False,
    )
