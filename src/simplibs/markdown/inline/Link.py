# Outers
from .._common.helpers import as_inline, escape_label, escape_link_destination, escape_link_title, normalize_label
from .._common.validations import raise_param_invalid_type_error
from ..base_class import InlineMarkdown
# Inners
from ._validations.link import (
    raise_link_autolink_with_text_error,
    raise_link_empty_destination_error,
    raise_link_image_unsupported_kind_error,
    raise_link_kind_requires_label_error,
)
from .enums import LinkKind


class Link(InlineMarkdown):
    """A link or an image, in any of six forms.

    Args:
        text: The link text (or the alt text of an image). Not allowed for
            autolinks and bare URLs.
        dest: The destination (a URL or a path).
        title: An optional title.
        kind: The syntax form of the link.
        image: `True` writes an image (`!`) instead of a link.
        label: The label of a `LinkDefinition`; required for `REFERENCE`.
            Whitespace is collapsed and brackets are escaped, as in the definition.

    Raises:
        ParamError: If a parameter has the wrong type, the text or the label
            is missing where it is needed, the destination is empty, or the
            combination is not possible.
    """

    __slots__ = ("text", "dest", "title", "kind", "image", "label")

    def __init__(
        self,
        text=None,
        dest: str | None = None,
        title: str | None = None,
        kind: LinkKind = LinkKind.INLINE,
        image: bool = False,
        label: str | None = None,
    ) -> None:

        # 1. Validation
        # 1.1 Types
        if not isinstance(kind, LinkKind):
            raise_param_invalid_type_error("kind", kind, LinkKind)
        for name, value in (("dest", dest), ("title", title), ("label", label)):
            if value is not None and not isinstance(value, str):
                raise_param_invalid_type_error(name, value, str)

        # 1.2 An autolink and a bare URL are the destination and nothing else
        if kind in (LinkKind.AUTOLINK, LinkKind.BARE):
            if text is not None:
                raise_link_autolink_with_text_error(kind)
            if image:
                raise_link_image_unsupported_kind_error(kind)
            if not dest:
                raise_link_empty_destination_error(kind, dest)

        # 1.3 The other kinds need a text, and each needs its own second part
        else:
            if text is None:
                raise_param_invalid_type_error("text", text, "str | Markdown")
            if kind is LinkKind.INLINE and not dest:
                raise_link_empty_destination_error(kind, dest)
            if kind is LinkKind.REFERENCE and not label:
                raise_link_kind_requires_label_error(kind)

        # 1.4 The text becomes an inline node
        text_node = None if text is None else as_inline(text)

        # 2. Assignment
        self.text = text_node
        self.dest = dest
        self.title = title
        self.kind = kind
        self.image = image
        self.label = label

    def to_inline(self) -> str:

        # 1. An autolink and a bare URL are the destination
        if self.kind is LinkKind.AUTOLINK:
            return f"<{self.dest}>"
        if self.kind is LinkKind.BARE:
            return self.dest

        # 2. The other kinds share the text and the mark of an image
        bang = "!" if self.image else ""
        text = self.text.to_text()

        # 3. The kind decides what follows the text
        if self.kind is LinkKind.INLINE:
            title = f" {escape_link_title(self.title)}" if self.title else ""
            return f"{bang}[{text}]({escape_link_destination(self.dest)}{title})"
        if self.kind is LinkKind.REFERENCE:
            return f"{bang}[{text}][{escape_label(normalize_label(self.label))}]"
        if self.kind is LinkKind.COLLAPSED:
            return f"{bang}[{text}][]"
        return f"{bang}[{text}]"


_DESIGN_NOTES = """
# Link — One Node for Links and Images

## Purpose
A link and an image differ in a leading `!`, and a link has six spellings.
One node with a `kind` and an `image` flag covers all twelve combinations
without twelve classes.

## What Each Kind Needs
* `INLINE` — text and destination; the title is optional.
* `REFERENCE` — text and a label (the destination is in a `LinkDefinition`).
* `COLLAPSED`, `SHORTCUT` — text only (the label is the text).
* `AUTOLINK`, `BARE` — destination only.

## Added Since the Draft
Type checks of `dest`, `title` and `label`; without them a number would fail
later inside an escape function.

## The Label Is Written Like in the Definition
A `REFERENCE` link writes its label through `escape_label(normalize_label(label))`,
the same two functions `LinkDefinition` uses. A bracket or a backslash in the
label is therefore escaped on both sides, and the reference finds its
definition. The label is stored as it was given; the escaping happens in the
output.
"""
