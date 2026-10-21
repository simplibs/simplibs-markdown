# Outers
from ...base_class import Markdown
from ...inline import Emphasis
from ...inline.enums import EmphasisKind


def STRIKETHROUGH(inner: str | Markdown) -> Emphasis:
    """Build struck-through text.

    Init Params:
        inner (str | Markdown): The text to strike through: a string, an inline node or a
            list of them. It must not be empty.

    Markdown:
        The text between two tildes (`~~text~~`).

    Example:
        "Price " + STRIKETHROUGH("10 EUR") + " 8 EUR"
        # Writes: "Price ~~10 EUR~~ 8 EUR"

    Note:
        Only the tilde writes strike-through, so there is no `marker` parameter.
    """
    return Emphasis(inner, EmphasisKind.STRIKE)
