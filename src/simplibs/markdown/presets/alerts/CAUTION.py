# Outers
from ...base_class import Markdown
from ...containers import Quote
from ...containers.enums import AlertKind


def CAUTION(*blocks: str | Markdown) -> Quote:
    """Build an alert about a risk or a negative outcome.

    Init Params:
        *blocks (str | Markdown): The content: strings, nodes or lists of them. Several
            blocks are separated by a quoted blank line.

    Markdown:
        A quote whose first line is `> [!CAUTION]`, followed by the quoted content.

    Example:
        CAUTION("This cannot be undone.")
        # Writes:
        # > [!CAUTION]
        # > This cannot be undone.

    Note:
        GitHub shows it as a highlighted alert. Other renderers show an ordinary quote with
        the first line `[!CAUTION]`.
    """
    return Quote(*blocks, alert=AlertKind.CAUTION)
