import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.code_block import (
    raise_code_block_info_has_backtick_error,
)


@pytest.mark.parametrize("info", ["py`thon", "`", "a ` b"])
def test_raise_code_block_info_has_backtick_error_contract(subtests, info) -> None:
    """Verify raise_code_block_info_has_backtick_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_code_block_info_has_backtick_error,
        invalid_params=(info,),
        exception_type=ParamError,
        error_name="MARKDOWN_CODE_BLOCK_INFO_HAS_BACKTICK",
        label="code block info",
        expected="An info string without a backtick, or a tilde fence.",
        value=info,
        problem=(
            "A backtick inside the info string would end the opening fence.",
            "The line would no longer start a code block.",
        ),
        how_to_fix=(
            "Remove the backtick from the info string.",
            "Use FenceChar.TILDE for the fence.",
        ),
        exception=ValueError,
        verbose=False,
    )
