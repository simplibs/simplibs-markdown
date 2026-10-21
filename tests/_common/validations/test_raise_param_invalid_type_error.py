import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown._common.validations import raise_param_invalid_type_error


@pytest.mark.parametrize(
    "param_name, value, expected, expected_text",
    [
        # A type is shown by its name
        ("kind", "bold", int, "int"),
        ("marker", 1, str, "str"),
        # A phrase is shown as it is
        ("content", None, "str | Markdown", "str | Markdown"),
        ("start", -1, "positive int", "positive int"),
    ],
)
def test_raise_param_invalid_type_error_contract(
    subtests, param_name, value, expected, expected_text
) -> None:
    """Verify raise_param_invalid_type_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_param_invalid_type_error,
        invalid_params=(param_name, value, expected),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label=f"parameter '{param_name}'",
        expected=expected_text,
        value=value,
        problem=f"Parameter '{param_name}' received a value of the wrong type.",
        how_to_fix=f"Pass {expected_text} as '{param_name}'.",
        exception=TypeError,
        verbose=False,
    )
