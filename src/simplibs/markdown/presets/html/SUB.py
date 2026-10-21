# Outers
from ...base_class import Markdown
from ...blocks import Html
from ...blocks.enums import HtmlMode


def SUB(inner: str | Markdown) -> Html:
    """Build subscript text.

    Init Params:
        inner (str | Markdown): The text inside the tag: a string, an inline node or a list
            of them.

    Markdown:
        The text between `<sub>` tags.

    Example:
        "H" + SUB("2") + "O"
        # Writes: "H<sub>2</sub>O"
    """
    return Html("sub", inner, mode=HtmlMode.INLINE)
