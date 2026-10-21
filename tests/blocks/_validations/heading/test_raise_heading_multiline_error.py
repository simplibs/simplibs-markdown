import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.heading import raise_heading_multiline_error


@pytest.mark.parametrize("text", ["first\nsecond", "a\r\nb", "\nleading"])
def test_raise_heading_multiline_error_contract(subtests, text) -> None:
    """Verify raise_heading_multiline_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_heading_multiline_error,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_MULTILINE",
        label="heading text",
        expected="Text without line breaks.",
        value=text,
        problem=(
            "A heading is one line.",
            "A line break would end the heading and start a paragraph.",
        ),
        how_to_fix=(
            "Shorten the heading to a single line.",
            "Put the rest into a Paragraph below the heading.",
        ),
        exception=ValueError,
        verbose=False,
    )
