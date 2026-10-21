from typing import NoReturn
from simplibs.exception import ParamError


def raise_entity_unknown_name_error(
    name: str,
) -> NoReturn:
    """Raise ParamError when an entity name is not an HTML5 entity.

    Args:
        name: The rejected name, without `&` and `;`.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_ENTITY_UNKNOWN_NAME",
        label="entity name",
        value=name,
        problem=f"'&{name};' is not a known HTML entity.",
        expected="A name from the HTML5 entity list (e.g. 'amp', 'copy', 'nbsp').",
        how_to_fix=(
            "Check the spelling of the name.",
            "Use `codepoint=` for a character that has no name.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_entity_unknown_name_error — A Name Nobody Defined

## Purpose
An unknown `&name;` is not an error for a Markdown renderer, it is printed
as plain text. The mistake would be visible only in the finished document.
"""
