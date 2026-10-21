# Outers
from ...blocks import Html
from ...blocks.enums import HtmlMode


def COMMENT(text: str) -> Html:
    """Build a comment that is not shown.

    Init Params:
        text (str): The comment. It must not contain `-->` or start with `>` or `->`.

    Markdown:
        The text between `<!--` and `-->`.

    Example:
        COMMENT("TODO: add an example")
        # Writes: "<!-- TODO: add an example -->"

    Note:
        A comment between two lists with the same marker keeps them apart; without it they
        merge into one list.
    """
    return Html(content=text, mode=HtmlMode.COMMENT)
