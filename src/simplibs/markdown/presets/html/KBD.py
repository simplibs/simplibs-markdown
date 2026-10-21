# Outers
from ...base_class import Markdown
from ...blocks import Html
from ...blocks.enums import HtmlMode


def KBD(inner: str | Markdown) -> Html:
    """Build a keyboard key.

    Init Params:
        inner (str | Markdown): The text inside the tag: a string, an inline node or a list
            of them.

    Markdown:
        The text between `<kbd>` tags.

    Example:
        "Press " + KBD("Enter") + "."
        # Writes: "Press <kbd>Enter</kbd>."
    """
    return Html("kbd", inner, mode=HtmlMode.INLINE)
