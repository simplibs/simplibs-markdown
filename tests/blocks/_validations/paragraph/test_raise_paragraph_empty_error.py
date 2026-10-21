from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.paragraph import raise_paragraph_empty_error


def test_raise_paragraph_empty_error_contract(subtests) -> None:
    """Verify raise_paragraph_empty_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_paragraph_empty_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAGRAPH_EMPTY",
        label="paragraph lines",
        expected="At least one line with a visible character.",
        problem=(
            "A paragraph needs at least one line with text.",
            "Empty lines separate blocks, they are not a block.",
        ),
        how_to_fix=(
            "Pass the text as one or more lines.",
            "Use BlankLine when you need an empty line.",
        ),
        exception=ValueError,
        verbose=False,
    )
