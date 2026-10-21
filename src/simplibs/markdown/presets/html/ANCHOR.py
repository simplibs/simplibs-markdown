# Outers
from ...blocks import Html
from ...blocks.enums import HtmlMode


def ANCHOR(name: str) -> Html:
    """Build an invisible anchor that a link can point to.

    Init Params:
        name (str): The id of the anchor, used after `#` in a link.

    Markdown:
        An empty `<a>` tag with an id (`<a id="name"></a>`).

    Example:
        ANCHOR("top")
        # Writes: "<a id=\\"top\\"></a>"

    Note:
        Link to it with `[text](#top)`. Use it where a heading cannot serve as the target.
    """
    return Html("a", attrs={"id": name}, mode=HtmlMode.INLINE)
