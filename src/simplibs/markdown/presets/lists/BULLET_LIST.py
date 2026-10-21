# Outers
from ...base_class import Markdown
from ...containers import List, ListItem
from ...containers.enums import ListMarker


def BULLET_LIST(
    *items: str | Markdown | ListItem,
    marker: ListMarker = ListMarker.DASH,
    tight: bool = True,
) -> list:
    """Build a bullet list.

    Init Params:
        *items (str | Markdown | ListItem): The items. A string or a node becomes one item;
            pass a `ListItem` to put several blocks into an item or to add a checkbox.
        marker (ListMarker): `ListMarker.DASH` (default), `ASTERISK` or `PLUS`.
        tight (bool): `False` puts a blank line between the items.

    Markdown:
        One line per item, each with the marker in front (`- item`).

    Example:
        BULLET_LIST("first", "second")
        # Writes:
        # - first
        # - second

        BULLET_LIST("first", "second", marker=ListMarker.ASTERISK)
        # Writes:
        # * first
        # * second

        BULLET_LIST("first", ListItem("second", BULLET_LIST("nested")))
        # Writes:
        # - first
        # - second
        #   - nested

    Note:
        A list that follows another list with the same marker merges with it. Use another
        marker, or a `COMMENT`, between them.
    """
    return List(*items, ordered=False, marker=marker, tight=tight)
