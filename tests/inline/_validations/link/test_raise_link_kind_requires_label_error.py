import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.markdown.inline.enums import LinkKind
from simplibs.markdown.inline._validations.link import (
    raise_link_kind_requires_label_error,
)


@pytest.mark.parametrize(
    "kind", [LinkKind.REFERENCE, LinkKind.COLLAPSED, LinkKind.SHORTCUT]
)
def test_raise_link_kind_requires_label_error_contract(subtests, kind) -> None:
    """Verify raise_link_kind_requires_label_error names the link kind."""

    assert_exception_function(
        subtests,
        raise_link_kind_requires_label_error,
        invalid_params=(kind,),
        exception_type=ParamError,
        error_name="MARKDOWN_LINK_KIND_REQUIRES_LABEL",
        label="link label",
        expected="A non-empty `label` that matches a `LinkDefinition`.",
        problem=f"A link of kind {kind.name} points to a definition by its label.",
        how_to_fix=(
            "Pass `label=...`.",
            "Add a `LinkDefinition` with the same label to the document.",
        ),
        exception=ValueError,
        verbose=False,
    )
