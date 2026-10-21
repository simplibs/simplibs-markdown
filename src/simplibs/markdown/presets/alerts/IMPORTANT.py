# Outers
from ...base_class import Markdown
from ...containers import Quote
from ...containers.enums import AlertKind


def IMPORTANT(*blocks: str | Markdown) -> Quote:
    """Build an alert for information that is key to the reader's goal.

    Init Params:
        *blocks (str | Markdown): The content: strings, nodes or lists of them. Several
            blocks are separated by a quoted blank line.

    Markdown:
        A quote whose first line is `> [!IMPORTANT]`, followed by the quoted content.

    Example:
        IMPORTANT("The token is shown only once.")
        # Writes:
        # > [!IMPORTANT]
        # > The token is shown only once.

    Note:
        GitHub shows it as a highlighted alert. Other renderers show an ordinary quote with
        the first line `[!IMPORTANT]`.
    """
    return Quote(*blocks, alert=AlertKind.IMPORTANT)
