import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline._validations.emphasis import (
    raise_emphasis_empty_inner_error,
)


@pytest.mark.parametrize("inner_text", ["", "   ", "\t"])
def test_raise_emphasis_empty_inner_error_contract(subtests, inner_text) -> None:
    """Verify raise_emphasis_empty_inner_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_emphasis_empty_inner_error,
        invalid_params=(inner_text,),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_EMPTY_INNER",
        label="emphasis content",
        expected="Content with at least one visible character.",
        value=inner_text,
        problem=(
            "Emphasis needs something to emphasize.",
            "Markers around nothing are only stray punctuation.",
        ),
        how_to_fix=(
            "Pass the text to emphasize.",
            "Leave the emphasis out when there is nothing to emphasize.",
        ),
        exception=ValueError,
        verbose=False,
    )
