# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import escape_label, escape_link_destination, escape_link_title, normalize_label
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._validations.link_definition import (
    raise_link_definition_empty_destination_error,
    raise_link_definition_empty_label_error,
)


class LinkDefinition(Markdown):
    """The target of reference links: `[label]: destination "title"`.

    Args:
        label: The label that reference links use. Whitespace is collapsed.
        dest: The destination (a URL or a path).
        title: An optional title.

    Raises:
        ParamError: If a parameter has the wrong type, or the label or the
            destination is empty.
    """

    __slots__ = ("label", "dest", "title")

    node_level = NodeLevel.BLOCK

    def __init__(self, label: str, dest: str, title: str | None = None) -> None:

        # 1. Validation
        # 1.1 Types
        if not isinstance(label, str):
            raise_param_invalid_type_error("label", label, str)
        if dest is not None and not isinstance(dest, str):
            raise_param_invalid_type_error("dest", dest, str)
        if title is not None and not isinstance(title, str):
            raise_param_invalid_type_error("title", title, str)

        # 1.2 The label is judged after its whitespace is collapsed
        label = normalize_label(label)
        if not label:
            raise_link_definition_empty_label_error()

        # 1.3 A definition points somewhere
        if not dest:
            raise_link_definition_empty_destination_error(dest)

        # 2. Assignment
        self.label = label
        self.dest = dest
        self.title = title

    def to_lines(self) -> tuple[str, ...]:

        # 1. Brackets and backslashes in the label would end it early; `Link` writes it the same way
        label = escape_label(self.label)

        # 2. The title is optional
        title = f" {escape_link_title(self.title)}" if self.title else ""

        # 3. One line
        return (f"[{label}]: {escape_link_destination(self.dest)}{title}",)


_DESIGN_NOTES = """
# LinkDefinition — Where a Reference Link Points

## Purpose
`[docs]: https://example.com` is invisible in the rendered document. Reference
links (`[text][docs]`) find it by the label.

## The Label Is Normalized and Escaped
`[Foo   Bar]` and `[Foo Bar]` are the same label for a renderer. The node
stores the collapsed form. When it is written, brackets and backslashes are
escaped by `escape_label`, and `Link` writes its label through the same two
functions, so both sides always agree.

## Definitions Stack
`separate_blocks` puts no blank line between two definitions.
"""
