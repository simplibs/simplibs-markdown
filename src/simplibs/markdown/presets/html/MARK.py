# Outers
from ...base_class import Markdown
from ...blocks import Html
from ...blocks.enums import HtmlMode


def MARK(inner: str | Markdown) -> Html:
    """Build highlighted text.

    Init Params:
        inner (str | Markdown): The text inside the tag: a string, an inline node or a list
            of them.

    Markdown:
        The text between `<mark>` tags.

    Example:
        "This is " + MARK("important") + "."
        # Writes: "This is <mark>important</mark>."

    Note:
        Not every renderer shows the highlight.
    """
    return Html("mark", inner, mode=HtmlMode.INLINE)
