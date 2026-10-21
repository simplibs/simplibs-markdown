import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.footnote import (
    raise_footnote_reference_with_blocks_error,
)


@pytest.mark.parametrize("label", ["1", "note", "source-2"])
def test_raise_footnote_reference_with_blocks_error_contract(subtests, label) -> None:
    """Verify raise_footnote_reference_with_blocks_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_footnote_reference_with_blocks_error,
        invalid_params=(label,),
        exception_type=ParamError,
        error_name="MARKDOWN_FOOTNOTE_REFERENCE_WITH_BLOCKS",
        label=f"footnote '{label}'",
        expected="No blocks for FootnoteRole.REFERENCE.",
        value=label,
        problem=(
            "A reference is only the marker in the text.",
            "The content belongs to the definition.",
        ),
        how_to_fix=(
            "Remove the blocks from the reference.",
            "Create a second Footnote with FootnoteRole.DEFINITION for the content.",
        ),
        exception=ValueError,
        verbose=False,
    )
