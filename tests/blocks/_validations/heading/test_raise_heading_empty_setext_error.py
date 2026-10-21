from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.heading import raise_heading_empty_setext_error


def test_raise_heading_empty_setext_error_contract(subtests) -> None:
    """Verify raise_heading_empty_setext_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_heading_empty_setext_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_HEADING_EMPTY_SETEXT",
        label="heading text",
        expected="Text with at least one visible character.",
        problem=(
            "A setext heading is the text with an underline below it.",
            "An underline alone is a thematic break.",
        ),
        how_to_fix=(
            "Pass the heading text.",
            "Use ThematicBreak when a line is all you need.",
        ),
        exception=ValueError,
        verbose=False,
    )
