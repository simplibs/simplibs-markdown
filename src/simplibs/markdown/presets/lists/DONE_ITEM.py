# Outers
from ...base_class import Markdown
from ...containers import ListItem


def DONE_ITEM(*blocks: str | Markdown) -> ListItem:
    """Build a list item with a checked checkbox.

    Init Params:
        *blocks (str | Markdown): The content of the item. It has to start with text.

    Markdown:
        An item with a checked box (`- [x] item` inside a list).

    Example:
        BULLET_LIST(DONE_ITEM("write code"), TASK_ITEM("write tests"))
        # Writes:
        # - [x] write code
        # - [ ] write tests

    Note:
        The checkbox is written in front of the first line of text, so an item that starts
        with code or a nested list is refused.
    """
    return ListItem(*blocks, checked=True)
