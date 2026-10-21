# Outers
from ...base_class import Markdown
from ...blocks import Heading
from ...blocks.enums import HeadingStyle


def H3(inner: str | Markdown, style: HeadingStyle = HeadingStyle.ATX) -> Heading:
    """Build a heading of level 3.

    Init Params:
        inner (str | Markdown): The heading text: a string, an inline node or a list of
            them. It has to stay on one line.
        style (HeadingStyle): How the heading is written. Defaults to `HeadingStyle.ATX`
            (`# text`). `ATX_CLOSED` also closes it with hashes (`# text #`).

    Markdown:
        A heading of level 3: 3 hashes followed by the text (`### text`).

    Example:
        H3("Requirements")
        # Writes: "### Requirements"

    Note:
        The setext style exists only for levels 1 and 2; `Heading` raises `ParamError` for a
        higher level.
    """
    return Heading(inner, level=3, style=style)
