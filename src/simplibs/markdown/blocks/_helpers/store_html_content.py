from typing import Any
# Outers
from..._common.helpers import as_inline, flatten_blocks
from ...base_class import Markdown
from ...base_class.enums import NodeLevel
from ..enums import HtmlMode


def store_html_content(content: Any, mode: HtmlMode) -> Any:
    """Turn the content of an HTML node into inline content or blocks.

    Args:
        content: A string, a node, or a list of them; or `None`.
        mode: How the node stands in the document.

    Returns:
        `None` for no content, one inline node for content that stays on the
        line of the tag, or a tuple of blocks.

    Raises:
        ParamError: If the content is not content, or an inline tag gets blocks.
    """

    # 1. No content
    if content is None:
        return None

    # 2. An inline tag holds a line, whatever it was given as
    if mode is HtmlMode.INLINE:
        return as_inline(content)

    # 3. A string or an inline node stays on the line of the tag
    if isinstance(content, str) or (
        isinstance(content, Markdown) and content.node_level is NodeLevel.INLINE
    ):
        return as_inline(content)

    # 4. Anything else is blocks
    items = content if isinstance(content, (list, tuple)) else (content,)
    return flatten_blocks(*items)


_DESIGN_NOTES = """
# store_html_content — One Line or Blocks

## Purpose
`<summary>Title</summary>` is a tag with a string and stays on one line.
`<details>` around a list and a paragraph is a tag with blocks and gets lines
of its own. This function decides which one it is.

## Inline Tags Take a List
`Html("kbd", ["Ctrl", "+", "C"], mode=HtmlMode.INLINE)` is one line. In the
draft a list was always read as blocks, which an inline tag then refused.
"""
