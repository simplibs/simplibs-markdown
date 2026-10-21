from html.entities import html5
# Outers
from ..base_class import InlineMarkdown
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._validations.entity import (
    raise_entity_codepoint_out_of_range_error,
    raise_entity_name_xor_codepoint_error,
    raise_entity_unknown_name_error,
)


class Entity(InlineMarkdown):
    """An HTML entity, by name (`&copy;`) or by code point (`&#169;`).

    Args:
        name: The entity name, with or without `&` and `;`.
        codepoint: The Unicode code point as an integer.

    Raises:
        ParamError: If both or neither are given, the name is unknown, or the
            code point is not a valid Unicode value.
    """

    __slots__ = ("name", "codepoint")

    def __init__(
        self,
        name: str | None = None,
        codepoint: int | None = None,
    ) -> None:

        # 1. Validation
        # 1.1 Exactly one of the two
        if (name is None) == (codepoint is None):
            raise_entity_name_xor_codepoint_error(name, codepoint)

        # 1.2 A name must be a known HTML5 entity
        if name is not None:
            if not isinstance(name, str):
                raise_param_invalid_type_error("name", name, str)
            name = name.strip("&;")
            if f"{name};" not in html5:
                raise_entity_unknown_name_error(name)

        # 1.3 A code point must be an integer inside the Unicode range
        else:
            is_integer = isinstance(codepoint, int) and not isinstance(codepoint, bool)
            if not is_integer or not 0 <= codepoint <= 0x10FFFF:
                raise_entity_codepoint_out_of_range_error(codepoint)

        # 2. Assignment
        self.name = name
        self.codepoint = codepoint

    def to_inline(self) -> str:

        # 1. A name is written between '&' and ';', a code point after '&#'
        return f"&{self.name};" if self.name is not None else f"&#{self.codepoint};"


_DESIGN_NOTES = """
# Entity — A Character Written as a Reference

## Purpose
`&nbsp;`, `&copy;` or `&#8203;` — characters that are hard to type or invisible.
The node checks the name against the HTML5 list, so a typo is an error and
not a literal `&nbsp` in the document.

## Why Not `Text`
`Text` escapes `&`, so an entity written as a string would be shown as text,
not rendered.

## Added Since the Draft
A type check of `name` (before `strip`) and a refusal of `bool` as a code
point.
"""
