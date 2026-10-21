# Outers
from ...base_class import Markdown
from ...blocks import Heading
from ...blocks.enums import HeadingStyle


def H2(inner: str | Markdown, style: HeadingStyle = HeadingStyle.ATX) -> Heading:
    """Build a heading of level 2.

    Init Params:
        inner (str | Markdown): The heading text: a string, an inline node or a list of
            them. It has to stay on one line.
        style (HeadingStyle): How the heading is written. Defaults to `HeadingStyle.ATX`
            (`# text`). `ATX_CLOSED` also closes it with hashes (`# text #`). `SETEXT`
            underlines the text instead.

    Markdown:
        A heading of level 2: 2 hashes followed by the text (`## text`).

    Example:
        H2("Installation")
        # Writes: "## Installation"

        H2("Installation", HeadingStyle.ATX_CLOSED)
        # Writes: "## Installation ##"

        H2("Installation", HeadingStyle.SETEXT)
        # Writes:
        # Installation
        # ------------
    """
    return Heading(inner, level=2, style=style)
