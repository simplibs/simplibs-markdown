# Outers
from ...base_class import Markdown
from ...containers import Quote
from ...containers.enums import AlertKind


def TIP(*blocks: str | Markdown) -> Quote:
    """Build an alert with helpful advice.

    Init Params:
        *blocks (str | Markdown): The content: strings, nodes or lists of them. Several
            blocks are separated by a quoted blank line.

    Markdown:
        A quote whose first line is `> [!TIP]`, followed by the quoted content.

    Example:
        TIP("Run the tests before you commit.")
        # Writes:
        # > [!TIP]
        # > Run the tests before you commit.

    Note:
        GitHub shows it as a highlighted alert. Other renderers show an ordinary quote with
        the first line `[!TIP]`.
    """
    return Quote(*blocks, alert=AlertKind.TIP)
