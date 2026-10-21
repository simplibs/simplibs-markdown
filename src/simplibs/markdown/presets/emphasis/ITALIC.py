# Outers
from ...base_class import Markdown
from ...inline import Emphasis
from ...inline.enums import EmphasisKind, EmphasisMarker


def ITALIC(inner: str | Markdown, marker: EmphasisMarker | None = None) -> Emphasis:
    """Build emphasized (italic) text.

    Init Params:
        inner (str | Markdown): The text to emphasize: a string, an inline node or a list of
            them. It must not be empty.
        marker (EmphasisMarker | None): The character that wraps the text. Defaults to the
            asterisk; `EmphasisMarker.UNDERSCORE` writes underscores instead.

    Markdown:
        The text between two single asterisks (`*text*`).

    Example:
        "Read " + ITALIC("this") + " first."
        # Writes: "Read *this* first."

        ITALIC("this", EmphasisMarker.UNDERSCORE)
        # Writes: "_this_"

    Note:
        Whitespace at the edges of the text is moved outside the markers, because
        `** text **` would not render as emphasis. An underscore marker does not work inside
        a word (`snake_case`).
    """
    return Emphasis(inner, EmphasisKind.EM, marker)
