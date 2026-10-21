# Outers
from ...base_class import Markdown
from ...containers import Quote
from ...containers.enums import AlertKind


def WARNING(*blocks: str | Markdown) -> Quote:
    """Build an alert for something that needs attention.

    Init Params:
        *blocks (str | Markdown): The content: strings, nodes or lists of them. Several
            blocks are separated by a quoted blank line.

    Markdown:
        A quote whose first line is `> [!WARNING]`, followed by the quoted content.

    Example:
        WARNING("This deletes all existing files.")
        # Writes:
        # > [!WARNING]
        # > This deletes all existing files.

    Note:
        GitHub shows it as a highlighted alert. Other renderers show an ordinary quote with
        the first line `[!WARNING]`.
    """
    return Quote(*blocks, alert=AlertKind.WARNING)
