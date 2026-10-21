import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.html import raise_html_comment_terminator_error


@pytest.mark.parametrize("text", ["ends --> early", ">starts with gt", "->starts with arrow"])
def test_raise_html_comment_terminator_error_contract(subtests, text) -> None:
    """Verify raise_html_comment_terminator_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_html_comment_terminator_error,
        invalid_params=(text,),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_COMMENT_TERMINATOR",
        label="HTML comment text",
        expected="Text without '-->' that does not start with '>' or '->'.",
        value=text,
        problem=(
            "The text contains '-->' or starts with '>' or '->'.",
            "The comment would end early and the rest would become visible.",
        ),
        how_to_fix=(
            "Remove or rephrase the closing sequence.",
            "Put a space before a leading '>'.",
        ),
        exception=ValueError,
        verbose=False,
    )
