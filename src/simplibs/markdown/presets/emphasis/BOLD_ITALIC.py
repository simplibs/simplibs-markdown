# Outers
from ...base_class import Markdown
from ...inline import Emphasis
from ...inline.enums import EmphasisKind, EmphasisMarker


def BOLD_ITALIC(inner: str | Markdown, marker: EmphasisMarker | None = None) -> Emphasis:
    """Build text that is both strong and emphasized.

    Init Params:
        inner (str | Markdown): The text to make strong and emphasized: a string, an inline
            node or a list of them. It must not be empty.
        marker (EmphasisMarker | None): The character that wraps the text. Defaults to the
            asterisk; `EmphasisMarker.UNDERSCORE` writes underscores instead.

    Markdown:
        The text between three asterisks (`***text***`).

    Example:
        "Read " + BOLD_ITALIC("this") + " first."
        # Writes: "Read ***this*** first."

    Note:
        Whitespace at the edges of the text is moved outside the markers, because
        `** text **` would not render as emphasis. An underscore marker does not work inside
        a word (`snake_case`).
    """
    return Emphasis(inner, EmphasisKind.STRONG_EM, marker)
