# Outers
from ...base_class import Markdown
from ...containers import List, ListItem
from ...containers.enums import ListMarker


def NUMBERED_LIST(
    *items: str | Markdown | ListItem,
    start: int = 1,
    marker: ListMarker = ListMarker.DOT,
    tight: bool = True,
) -> List:
    """Build a numbered list.

    Init Params:
        *items (str | Markdown | ListItem): The items. A string or a node becomes one item;
            pass a `ListItem` to put several blocks into an item.
        start (int): The number of the first item, 0 or more. Defaults to 1.
        marker (ListMarker): `ListMarker.DOT` (default, `1.`) or `PAREN` (`1)`).
        tight (bool): `False` puts a blank line between the items.

    Markdown:
        One line per item, numbered from `start` (`1. item`).

    Example:
        NUMBERED_LIST("first", "second")
        # Writes:
        # 1. first
        # 2. second

        NUMBERED_LIST("first", "second", start=3, marker=ListMarker.PAREN)
        # Writes:
        # 3) first
        # 4) second

    Note:
        Renderers continue the numbering by themselves, so only the number of the first item
        matters to them.
    """
    return List(*items, ordered=True, marker=marker, start=start, tight=tight)
