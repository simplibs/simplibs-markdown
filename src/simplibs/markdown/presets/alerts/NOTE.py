# Outers
from ...base_class import Markdown
from ...containers import Quote
from ...containers.enums import AlertKind


def NOTE(*blocks: str | Markdown) -> Quote:
    """Build an alert for information worth noticing.

    Init Params:
        *blocks (str | Markdown): The content: strings, nodes or lists of them. Several
            blocks are separated by a quoted blank line.

    Markdown:
        A quote whose first line is `> [!NOTE]`, followed by the quoted content.

    Example:
        NOTE("Back up your data first.")
        # Writes:
        # > [!NOTE]
        # > Back up your data first.

        NOTE("First paragraph.", "Second paragraph.")
        # Writes:
        # > [!NOTE]
        # > First paragraph.
        # >
        # > Second paragraph.

    Note:
        GitHub shows it as a highlighted alert. Other renderers show an ordinary quote with
        the first line `[!NOTE]`.
    """
    return Quote(*blocks, alert=AlertKind.NOTE)
