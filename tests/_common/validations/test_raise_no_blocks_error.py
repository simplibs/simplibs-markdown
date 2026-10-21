import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown._common.validations import raise_no_blocks_error


@pytest.mark.parametrize("owner", ["Quote", "Document", "Footnote"])
def test_raise_no_blocks_error_contract(subtests, owner) -> None:
    """Verify raise_no_blocks_error names the container in a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_no_blocks_error,
        invalid_params=(owner,),
        exception_type=ParamError,
        error_name="MARKDOWN_NO_BLOCKS",
        label=f"{owner} content",
        expected="At least one block, or a string for a plain paragraph.",
        problem=f"{owner} needs at least one block.",
        how_to_fix=(
            f"Pass the content of the {owner} as arguments.",
            "Do not create the container when there is nothing to put in it.",
        ),
        exception=ValueError,
        verbose=False,
    )
