import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline._validations.entity import (
    raise_entity_unknown_name_error,
)


@pytest.mark.parametrize("name", ["copyy", "notanentity", ""])
def test_raise_entity_unknown_name_error_contract(subtests, name) -> None:
    """Verify raise_entity_unknown_name_error names the entity in a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_entity_unknown_name_error,
        invalid_params=(name,),
        exception_type=ParamError,
        error_name="MARKDOWN_ENTITY_UNKNOWN_NAME",
        label="entity name",
        expected="A name from the HTML5 entity list (e.g. 'amp', 'copy', 'nbsp').",
        value=name,
        problem=f"'&{name};' is not a known HTML entity.",
        how_to_fix=(
            "Check the spelling of the name.",
            "Use `codepoint=` for a character that has no name.",
        ),
        exception=ValueError,
        verbose=False,
    )
