# Outers
from ...base_class import Markdown
from ...inline import Emphasis
from ...inline.enums import EmphasisKind, EmphasisMarker


def BOLD(inner: str | Markdown, marker: EmphasisMarker | None = None) -> Emphasis:
    """Build strong (bold) text.

    Init Params:
        inner (str | Markdown): The text to make strong: a string, an inline node or a list
            of them. It must not be empty.
        marker (EmphasisMarker | None): The character that wraps the text. Defaults to the
            asterisk; `EmphasisMarker.UNDERSCORE` writes underscores instead.

    Markdown:
        The text between two asterisks (`**text**`).

    Example:
        "Read " + BOLD("this") + " first."
        # Writes: "Read **this** first."

        BOLD("this", EmphasisMarker.UNDERSCORE)
        # Writes: "__this__"

    Note:
        Whitespace at the edges of the text is moved outside the markers, because
        `** text **` would not render as emphasis. An underscore marker does not work inside
        a word (`snake_case`).
    """
    return Emphasis(inner, EmphasisKind.STRONG, marker)
