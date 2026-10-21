import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.html import raise_html_invalid_tag_error

_TEXT_PROBLEM = "A tag name starts with a letter and has no spaces or brackets."
_TYPE_PROBLEM = "The tag name is not a string."


@pytest.mark.parametrize(
    "tag, problem, exception",
    [
        # A wrong string is a ValueError
        ("1div", _TEXT_PROBLEM, ValueError),
        ("<div>", _TEXT_PROBLEM, ValueError),
        ("a b", _TEXT_PROBLEM, ValueError),
        # A wrong kind of value is a TypeError
        (1, _TYPE_PROBLEM, TypeError),
        (None, _TYPE_PROBLEM, TypeError),
    ],
)
def test_raise_html_invalid_tag_error_contract(subtests, tag, problem, exception) -> None:
    """Verify raise_html_invalid_tag_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_html_invalid_tag_error,
        invalid_params=(tag,),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_INVALID_TAG",
        label="HTML tag",
        expected="Letters, digits and '-', starting with a letter (e.g. 'details', 'my-tag').",
        value=tag,
        problem=problem,
        how_to_fix=(
            "Pass only the name, without '<' and '>'.",
            "Pass attributes through `attrs`.",
        ),
        exception=exception,
        verbose=False,
    )
