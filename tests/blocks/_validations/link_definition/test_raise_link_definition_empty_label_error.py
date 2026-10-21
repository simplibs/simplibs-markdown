from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.blocks._validations.link_definition import (
    raise_link_definition_empty_label_error,
)


def test_raise_link_definition_empty_label_error_contract(subtests) -> None:
    """Verify raise_link_definition_empty_label_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_link_definition_empty_label_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_DEFINITION_EMPTY_LABEL",
        label="link definition label",
        expected="A label with at least one visible character.",
        problem=(
            "A definition is found by its label.",
            "An empty label cannot be referenced.",
        ),
        how_to_fix="Pass the label that the reference links use.",
        exception=ValueError,
        verbose=False,
    )
