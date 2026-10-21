import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown._common.validations import raise_block_in_inline_error


@pytest.mark.parametrize("value", ["# heading", 42, None, ["a", "b"]])
def test_raise_block_in_inline_error_contract(subtests, value) -> None:
    """Verify raise_block_in_inline_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_block_in_inline_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        label="inline content",
        expected="Text, emphasis, a link, inline code or another inline element.",
        value=value,
        problem="Block elements cannot be placed inside inline content.",
        how_to_fix=(
            "Put the block into a Document or a container such as Quote or List.",
            "Use an inline element in this place instead.",
        ),
        exception=TypeError,
        verbose=False,
    )
