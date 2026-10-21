# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import separate_blocks
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._helpers import ATTR_NAME, TAG_NAME, VOID_TAGS, build_html_open_tag, store_html_content
from ._validations.html import (
    raise_html_comment_terminator_error,
    raise_html_invalid_attribute_error,
    raise_html_invalid_tag_error,
    raise_html_void_tag_with_content_error,
)
from .enums import HtmlMode


class Html(Markdown):
    """Raw HTML: a block, an inline tag or a comment.

    Args:
        tag: The tag name. Not used for a comment.
        content: A string, a node, or a list of them. For a comment, a string.
        attrs: The attributes of the tag.
        mode: `BLOCK`, `INLINE` or `COMMENT`.

    Raises:
        ParamError: If a parameter is not valid, a void tag gets content, an
            inline tag gets a block, or a comment would end early.
    """

    __slots__ = ("tag", "content", "attrs", "mode")

    def __init__(
        self,
        tag: str | None = None,
        content=None,
        attrs: dict | None = None,
        mode: HtmlMode = HtmlMode.BLOCK,
    ) -> None:

        # 1. Validation
        # 1.1 The mode and the attributes
        if not isinstance(mode, HtmlMode):
            raise_param_invalid_type_error("mode", mode, HtmlMode)
        if attrs is not None and not isinstance(attrs, dict):
            raise_param_invalid_type_error("attrs", attrs, dict)
        attrs = dict(attrs or {})

        # 1.2 A comment is only text
        if mode is HtmlMode.COMMENT:
            text = "" if content is None else content
            if not isinstance(text, str):
                raise_param_invalid_type_error("content", content, str)
            if "-->" in text or text.startswith((">", "->")):
                raise_html_comment_terminator_error(text)
            tag = None
            stored = text

        # 1.3 A tag has a valid name, valid attributes and content that fits it
        else:
            if not isinstance(tag, str) or not TAG_NAME.fullmatch(tag):
                raise_html_invalid_tag_error(tag)
            tag = tag.lower()
            if tag in VOID_TAGS and content is not None:
                raise_html_void_tag_with_content_error(tag)
            for name in attrs:
                if not isinstance(name, str) or not ATTR_NAME.fullmatch(name):
                    raise_html_invalid_attribute_error(name)
            stored = store_html_content(content, mode)

        # 2. Assignment
        self.tag = tag
        self.content = stored
        self.attrs = attrs
        self.mode = mode

    @property
    def node_level(self) -> NodeLevel:

        # 1. An inline tag stands inside a line, everything else is a block
        return NodeLevel.INLINE if self.mode is HtmlMode.INLINE else NodeLevel.BLOCK

    def to_lines(self) -> tuple[str, ...]:

        # 1. A comment: one line, or the text between two marker lines
        if self.mode is HtmlMode.COMMENT:
            if "\n" in self.content:
                return ("<!--", *self.content.split("\n"), "-->")
            return (f"<!-- {self.content} -->" if self.content else "<!-- -->",)

        # 2. A void tag is only the opening tag
        opening = build_html_open_tag(self.tag, self.attrs)
        if self.tag in VOID_TAGS:
            return (opening,)

        # 3. A tag without content is the opening and the closing tag
        closing = f"</{self.tag}>"
        if self.content is None:
            return (opening + closing,)

        # 4. Inline content stays on the line of the tag
        if not isinstance(self.content, tuple):
            return (f"{opening}{self.content.to_text()}{closing}",)

        # 5. Blocks go between the tags, with blank lines so Markdown inside is read
        body = separate_blocks(self.content, gap=1)
        return (opening, "", *body, "", closing)


_DESIGN_NOTES = """
# Html — Raw HTML Without Raw Strings

## Purpose
`<details>`, `<kbd>`, `<sup>` and comments, written through validated parts.
The tag and the attribute names are checked, the values are escaped, so a
string from outside cannot break the tag.

## Blank Lines Around Block Content
`<details>` followed by a Markdown list is read as HTML to the end of the
block unless a blank line separates them. Block content therefore gets one on
each side.

## Changed From the Draft
* `tag` is `None` for a comment, whatever was passed.
* An inline tag takes a list of inline items (`["Ctrl", "+", "C"]`); the draft
  read a list as blocks and refused it.
* `attrs` must be a dictionary.

## Level Depends on the Mode
`node_level` is a property, like in `Footnote`. Three classes (`HtmlBlock`,
`HtmlInline`, `HtmlComment`) is the alternative and a round-2 decision.
"""
