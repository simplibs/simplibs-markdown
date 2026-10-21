import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.html import raise_html_invalid_attribute_error

_TEXT_PROBLEM = "An attribute name cannot contain spaces, quotes or '='."
_TYPE_PROBLEM = "The attribute name is not a string."


@pytest.mark.parametrize(
    "name, problem, exception",
    [
        # A wrong string is a ValueError
        ("bad name", _TEXT_PROBLEM, ValueError),
        ('a"b', _TEXT_PROBLEM, ValueError),
        ("a=b", _TEXT_PROBLEM, ValueError),
        # A wrong kind of value is a TypeError
        (1, _TYPE_PROBLEM, TypeError),
        (None, _TYPE_PROBLEM, TypeError),
    ],
)
def test_raise_html_invalid_attribute_error_contract(
    subtests, name, problem, exception
) -> None:
    """Verify raise_html_invalid_attribute_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_html_invalid_attribute_error,
        invalid_params=(name,),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_INVALID_ATTRIBUTE",
        label="HTML attribute name",
        expected="Letters, digits and '-', '_', ':', '.', starting with a letter, '_' or ':'.",
        value=name,
        problem=problem,
        how_to_fix=(
            "Pass only the name as the key of `attrs`.",
            "Pass the value as the value of that key.",
        ),
        exception=exception,
        verbose=False,
    )
