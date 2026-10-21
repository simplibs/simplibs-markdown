# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import flatten_blocks, prefix_lines, separate_blocks
from .._common.validations import raise_no_blocks_error, raise_param_invalid_type_error
# Inners
from ._validations.footnote import (
    raise_footnote_label_has_whitespace_error,
    raise_footnote_reference_with_blocks_error,
)
from .enums import FootnoteRole


class Footnote(Markdown):
    """A footnote: the marker in the text or the note itself.

    Args:
        label: The label that ties the marker to the note. No whitespace.
        *blocks: The content of the note. Only for a definition.
        role: `REFERENCE` writes `[^label]` (an inline node), `DEFINITION`
            writes `[^label]: content` (a block node).

    Raises:
        ParamError: If the label is not usable, the role has the wrong type,
            a reference gets blocks, or a definition has none.
    """

    __slots__ = ("label", "blocks", "role")

    def __init__(
        self,
        label: str,
        *blocks,
        role: FootnoteRole = FootnoteRole.DEFINITION,
    ) -> None:

        # 1. Validation
        # 1.1 The label is a non-empty string without whitespace
        if not isinstance(label, str) or not label or any(char.isspace() for char in label):
            raise_footnote_label_has_whitespace_error(label)

        # 1.2 The role, and what each role may hold
        if not isinstance(role, FootnoteRole):
            raise_param_invalid_type_error("role", role, FootnoteRole)
        if role is FootnoteRole.REFERENCE and blocks:
            raise_footnote_reference_with_blocks_error(label)
        flat = flatten_blocks(*blocks)
        if role is FootnoteRole.DEFINITION and not flat:
            raise_no_blocks_error("Footnote")

        # 2. Assignment
        self.label = label
        self.blocks = flat
        self.role = role

    @property
    def node_level(self) -> NodeLevel:

        # 1. A marker stands inside a line, a note is a block
        return NodeLevel.INLINE if self.role is FootnoteRole.REFERENCE else NodeLevel.BLOCK

    def to_lines(self) -> tuple[str, ...]:

        # 1. The marker is only the label
        if self.role is FootnoteRole.REFERENCE:
            return (f"[^{self.label}]",)

        # 2. The note: the blocks separated by blank lines, indented under the label
        body = separate_blocks(self.blocks, gap=1)
        return prefix_lines(body, f"[^{self.label}]: ", "    ")


_DESIGN_NOTES = """
# Footnote — A Marker and a Note With One Label

## Purpose
`[^1]` in the text and `[^1]: the note` at the end are two nodes of different
levels that belong together by the label. One class with a `role` keeps the
label and the pairing in one place.

## Level Depends on the Role
`node_level` is a property here. That is the price of one class for two
levels; the alternative is two classes (`FootnoteReference` and
`FootnoteDefinition`), which is a round-2 decision.

## Indentation of the Note
The first line follows `[^1]: `, the other lines are indented by four spaces,
so a note can have several paragraphs.
"""
