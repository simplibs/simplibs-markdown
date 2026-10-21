# Outers
from ..base_class import Markdown
from ..base_class.enums import NodeLevel
from .._common.helpers import prefix_lines
from .._common.validations import raise_param_invalid_type_error
# Inners
from ._validations.list import (
    raise_list_item_not_list_item_error,
    raise_list_marker_ordered_mismatch_error,
    raise_list_no_items_error,
    raise_list_start_negative_error,
    raise_list_start_on_bullet_error,
)
from .enums import ListMarker
from .ListItem import ListItem


class List(Markdown):
    """A bullet or an ordered list.

    Args:
        *items: `ListItem` objects, or strings and nodes (each becomes one item).
        ordered: `True` writes a numbered list.
        marker: The marker. Defaults to `-` for bullets and `.` for numbers.
        start: The number of the first item of an ordered list.
        tight: `False` puts a blank line between the items.

    Raises:
        ParamError: If there is no item, an item is not usable, the marker does
            not fit the kind of list, or the start is not valid.
    """

    __slots__ = ("items", "ordered", "marker", "start", "tight")

    node_level = NodeLevel.BLOCK

    def __init__(
        self,
        *items,
        ordered: bool = False,
        marker: ListMarker | None = None,
        start: int = 1,
        tight: bool = True,
    ) -> None:

        # 1. Validation
        # 1.1 The marker: the default depends on the kind of list
        if marker is None:
            marker = ListMarker.DOT if ordered else ListMarker.DASH
        if not isinstance(marker, ListMarker):
            raise_param_invalid_type_error("marker", marker, ListMarker)
        if ordered != (marker in (ListMarker.DOT, ListMarker.PAREN)):
            raise_list_marker_ordered_mismatch_error(ordered, marker)

        # 1.2 The start number belongs to ordered lists only
        if isinstance(start, bool) or not isinstance(start, int) or start < 0:
            raise_list_start_negative_error(start)
        if not ordered and start != 1:
            raise_list_start_on_bullet_error(start)

        # 1.3 The items: a string or a node becomes an item of its own
        built = []
        for item in items:
            if isinstance(item, ListItem):
                built.append(item)
            elif isinstance(item, (str, Markdown)):
                built.append(ListItem(item))
            else:
                raise_list_item_not_list_item_error(item)
        if not built:
            raise_list_no_items_error()

        # 2. Assignment
        self.items = tuple(built)
        self.ordered = ordered
        self.marker = marker
        self.start = start
        self.tight = tight

    def to_lines(self) -> tuple[str, ...]:

        # 1. The list is loose when asked to be, or when an item cannot be tight
        loose = not self.tight or any(item.needs_loose for item in self.items)

        # 2. Write item by item
        lines = []
        for index, item in enumerate(self.items):

            # 2.1 The marker of this item; its width is the indentation of the item
            if self.ordered:
                marker = f"{self.start + index}{self.marker.value} "
            else:
                marker = f"{self.marker.value} "
            content = item.content_lines(loose)

            # 2.2 A loose list has a blank line between the items
            if index and loose:
                lines.append("")

            # 2.3 The content under the marker, or the bare marker for an empty item
            if content:
                lines.extend(prefix_lines(content, marker, " " * len(marker)))
            else:
                lines.append(marker.rstrip())

        return tuple(lines)


_DESIGN_NOTES = """
# List — Bullets and Numbers

## Purpose
One node for both kinds. The marker decides the look; `ordered` and the marker
must agree, which is checked when the list is built.

## Tight and Loose
Tight items stand on consecutive lines; loose items have a blank line between
them and their paragraphs are wrapped in `<p>` by renderers. A list is loose
when asked to be or when one of its items holds two paragraphs.

## Indentation
Every line after the first is indented by the width of its own marker
(`1. ` is 3, `10. ` is 4), so nested content stays inside the item.

## Known Gap
Two lists of the same marker one after another merge into one list in
CommonMark. Use another marker, or a `Html` comment, between them.
"""
