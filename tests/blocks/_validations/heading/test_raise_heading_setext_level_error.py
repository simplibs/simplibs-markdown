import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.heading import raise_heading_setext_level_error


@pytest.mark.parametrize("level", [3, 4, 6, 0])
def test_raise_heading_setext_level_error_contract(subtests, level) -> None:
    """Verify raise_heading_setext_level_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_heading_setext_level_error,
        invalid_params=(level,),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_SETEXT_LEVEL",
        label="heading level",
        expected="Level 1 or 2 for a setext heading.",
        value=level,
        problem=(
            "The setext style underlines the text with '=' or '-'.",
            "That gives only two levels.",
        ),
        how_to_fix=(
            "Use HeadingStyle.ATX for levels 3 to 6.",
            "Lower the level to 1 or 2.",
        ),
        exception=ValueError,
        verbose=False,
    )
