from typing import Any, NoReturn, TYPE_CHECKING
from simplibs.exception import ParamError
# Annotations
if TYPE_CHECKING:
    from ...enums import ReferenceKind


def raise_reference_invalid_value_error(
    kind: "ReferenceKind",
    value: Any,
    expected: str,
) -> NoReturn:
    """Raise ParamError when a value does not fit its kind of reference.

    Args:
        kind: The kind of reference being built.
        value: The rejected value.
        expected: What a valid value of this kind looks like, as a short phrase.
    """

    # 1. Name the kind in words, e.g. REPO_ISSUE -> "repo issue"
    kind_name = kind.name.lower().replace("_", " ")

    # 2. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_REFERENCE_INVALID_VALUE",
        label=f"{kind_name} reference",
        value=value,
        problem=f"The value does not fit a {kind_name} reference.",
        expected=expected,
        how_to_fix=(
            "Check the value against the expected form.",
            "Use another ReferenceKind when it is a different kind of reference.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_reference_invalid_value_error — A Mention That Would Not Link

## Purpose
`@some user` or `#abc` is plain text to the renderer: it never becomes a
link and nobody is told. The card is raised at construction.

## `expected` Comes From the Caller
The pattern for each kind lives next to the code that uses it
(`_REFERENCE_FORMS` in `Reference`), together with its description. The raiser
only prints what it is given, so the knowledge exists in one place.
"""
