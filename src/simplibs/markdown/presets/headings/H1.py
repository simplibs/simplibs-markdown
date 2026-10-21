# Outers
from ...base_class import Markdown
from ...blocks import Heading
from ...blocks.enums import HeadingStyle


def H1(inner: str | Markdown, style: HeadingStyle = HeadingStyle.ATX) -> Heading:
    """Build a heading of level 1.

    Init Params:
        inner (str | Markdown): The heading text: a string, an inline node or a list of
            them. It has to stay on one line.
        style (HeadingStyle): How the heading is written. Defaults to `HeadingStyle.ATX`
            (`# text`). `ATX_CLOSED` also closes it with hashes (`# text #`). `SETEXT`
            underlines the text instead.

    Markdown:
        A heading of level 1: 1 hash followed by the text (`# text`).

    Example:
        H1("Project")
        # Writes: "# Project"

        H1("Project", HeadingStyle.SETEXT)
        # Writes:
        # Project
        # =======

    Note:
        A document usually has one level 1 heading: its title.
    """
    return Heading(inner, level=1, style=style)
