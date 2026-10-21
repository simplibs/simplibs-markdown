import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.code_block import (
    raise_code_block_indented_with_info_error,
)


@pytest.mark.parametrize("info", ["python", "js", "text with spaces"])
def test_raise_code_block_indented_with_info_error_contract(subtests, info) -> None:
    """Verify raise_code_block_indented_with_info_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_code_block_indented_with_info_error,
        invalid_params=(info,),
        exception_type=ParamError,
        error_name="MARKDOWN_CODE_BLOCK_INDENTED_WITH_INFO",
        label="code block info",
        expected="No info string for an indented block.",
        value=info,
        problem=(
            "An indented code block has no fence.",
            "There is no place to write the info string.",
        ),
        how_to_fix=(
            "Remove `info`.",
            "Use a fenced block (`indented=False`) to name the language.",
        ),
        exception=ValueError,
        verbose=False,
    )
