import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.html import raise_html_void_tag_with_content_error


@pytest.mark.parametrize("tag", ["br", "img", "hr"])
def test_raise_html_void_tag_with_content_error_contract(subtests, tag) -> None:
    """Verify raise_html_void_tag_with_content_error names the tag in a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_html_void_tag_with_content_error,
        invalid_params=(tag,),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_VOID_TAG_WITH_CONTENT",
        label=f"content of <{tag}>",
        expected="No content for this tag.",
        problem=(
            f"<{tag}> is a void element.",
            "It has no closing tag, so it cannot hold content.",
        ),
        how_to_fix=(
            "Remove the content.",
            "Use a tag that can hold content, e.g. 'span' or 'div'.",
        ),
        exception=ValueError,
        verbose=False,
    )
