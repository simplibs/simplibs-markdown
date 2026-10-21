from typing import NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import LinkKind


def raise_link_kind_requires_label_error(
    kind: "LinkKind",
) -> NoReturn:
    """Raise ParamError when a reference link has no label.

    Args:
        kind: The kind of the link being built.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_LINK_KIND_REQUIRES_LABEL",
        label="link label",
        problem=f"A link of kind {kind.name} points to a definition by its label.",
        expected="A non-empty `label` that matches a `LinkDefinition`.",
        how_to_fix=(
            "Pass `label=...`.",
            "Add a `LinkDefinition` with the same label to the document.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_link_kind_requires_label_error — A Reference Without a Name

## Purpose
`[text][]` with an empty label would point to a definition named after the
text; that is the COLLAPSED kind. A REFERENCE link must say which definition
it means.

## No `value`
The label was not given, so there is nothing to show.
"""
