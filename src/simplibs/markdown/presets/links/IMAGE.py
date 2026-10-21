# Outers
from ...base_class import Markdown
from ...inline import Link


def IMAGE(alt: str | Markdown, src: str, title: str | None = None) -> Link:
    """Build an image.

    Init Params:
        alt (str | Markdown): The description shown when the image cannot load, and read by
            screen readers.
        src (str): The address or the path of the image.
        title (str | None): An optional title, shown when the pointer rests on the image.

    Markdown:
        A link with a leading exclamation mark (`![alt](src "title")`).

    Example:
        IMAGE("Logo", "img/logo.png")
        # Writes: "![Logo](img/logo.png)"

        IMAGE("Logo", "img/logo.png", "Our logo")
        # Writes: "![Logo](img/logo.png \\"Our logo\\")"

    Note:
        For a link without the leading `!`, use `Link(text, dest)`. An address with spaces
        or unbalanced parentheses is wrapped in `<...>` automatically.
    """
    return Link(alt, src, title, image=True)
