# Outers
from ...base_class import Markdown
from ...blocks import Html
from ...blocks.enums import HtmlMode


def SUP(inner: str | Markdown) -> Html:
    """Build superscript text.

    Init Params:
        inner (str | Markdown): The text inside the tag: a string, an inline node or a list
            of them.

    Markdown:
        The text between `<sup>` tags.

    Example:
        "x" + SUP("2")
        # Writes: "x<sup>2</sup>"
    """
    return Html("sup", inner, mode=HtmlMode.INLINE)
