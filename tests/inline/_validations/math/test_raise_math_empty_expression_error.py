import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline._validations.math import (
    raise_math_empty_expression_error,
)


@pytest.mark.parametrize("expr", ["", "   ", "\t"])
def test_raise_math_empty_expression_error_contract(subtests, expr) -> None:
    """Verify raise_math_empty_expression_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_math_empty_expression_error,
        invalid_params=(expr,),
        exception_type=ParamError,
        error_name="MARKDOWN_MATH_EMPTY_EXPRESSION",
        label="math expression",
        expected="Text with at least one non-whitespace character.",
        value=expr,
        problem="A math expression needs visible content.",
        how_to_fix=(
            "Pass the expression, e.g. 'E = mc^2'.",
            "Leave the element out when there is no expression.",
        ),
        exception=ValueError,
        verbose=False,
    )
