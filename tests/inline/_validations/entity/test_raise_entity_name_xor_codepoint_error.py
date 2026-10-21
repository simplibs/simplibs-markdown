import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline._validations.entity import (
    raise_entity_name_xor_codepoint_error,
)


@pytest.mark.parametrize(
    "name, codepoint, mistake",
    [
        (None, None, "Neither was given."),
        ("copy", 169, "Both were given."),
        ("amp", 0, "Both were given."),
    ],
)
def test_raise_entity_name_xor_codepoint_error_contract(
    subtests, name, codepoint, mistake
) -> None:
    """Verify raise_entity_name_xor_codepoint_error says which of the two mistakes it was."""

    assert_exception_function(
        subtests,
        raise_entity_name_xor_codepoint_error,
        invalid_params=(name, codepoint),
        exception_type=ParamError,
        error_name="MARKDOWN_ENTITY_NAME_XOR_CODEPOINT",
        label="entity",
        expected="`name` (e.g. 'copy') or `codepoint` (e.g. 169), not both.",
        value={"name": name, "codepoint": codepoint},
        problem=(
            "Exactly one of `name` and `codepoint` is required.",
            mistake,
        ),
        how_to_fix="Pass only one of them.",
        exception=ValueError,
        verbose=False,
    )
