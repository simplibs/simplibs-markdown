from typing import NoReturn
from simplibs.exception import ParamError


def raise_html_void_tag_with_content_error(
    tag: str,
) -> NoReturn:
    """Raise ParamError when a void HTML tag gets content.

    Args:
        tag: The void tag (`"br"`, `"img"`...).
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="MARKDOWN_HTML_VOID_TAG_WITH_CONTENT",
        label=f"content of <{tag}>",
        problem=(
            f"<{tag}> is a void element.",
            "It has no closing tag, so it cannot hold content.",
        ),
        expected="No content for this tag.",
        how_to_fix=(
            "Remove the content.",
            "Use a tag that can hold content, e.g. 'span' or 'div'.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_html_void_tag_with_content_error — Text Inside `<br>`

## Purpose
`<br>text</br>` is not valid HTML; browsers read the `</br>` as another line
break. The set of void tags is kept by the `Html` node.
"""
