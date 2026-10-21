import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ConversionError
from simplibs.markdown.blocks._validations.frontmatter import (
    raise_frontmatter_not_serializable_error,
)

_FINITE_PROBLEM = "NaN and infinity have no YAML form here."
_TYPE_PROBLEM = "Its type is not supported."


# NaN is left out on purpose: `nan != nan`, so the `value` check could never pass.
@pytest.mark.parametrize(
    "value, second_problem, exception",
    [
        # A non-finite float is a wrong value -> ValueError
        (float("inf"), _FINITE_PROBLEM, ValueError),
        (float("-inf"), _FINITE_PROBLEM, ValueError),
        # Everything else is a wrong type -> TypeError
        ({1, 2}, _TYPE_PROBLEM, TypeError),
        (b"bytes", _TYPE_PROBLEM, TypeError),
        (1 + 2j, _TYPE_PROBLEM, TypeError),
        (object, _TYPE_PROBLEM, TypeError),
    ],
)
def test_raise_frontmatter_not_serializable_error_contract(
    subtests, value, second_problem, exception
) -> None:
    """Verify raise_frontmatter_not_serializable_error chooses the right problem and exception."""

    assert_exception_function(
        subtests,
        raise_frontmatter_not_serializable_error,
        invalid_params=(value,),
        exception_type=ConversionError,
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        label="front matter value",
        expected=(
            "A string, int, finite float, bool or None, "
            "or a dict, list or tuple of them (dict keys must be strings)."
        ),
        value=value,
        problem=(
            "This value cannot be written into the front matter.",
            second_problem,
        ),
        how_to_fix=(
            "Convert the value to one of these types first.",
            "Replace NaN and infinity with None or a string.",
        ),
        exception=exception,
        verbose=False,
    )
