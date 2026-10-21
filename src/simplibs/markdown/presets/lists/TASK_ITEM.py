# Outers
from ...base_class import Markdown
from ...containers import ListItem


def TASK_ITEM(*blocks: str | Markdown) -> ListItem:
    """Build a list item with an empty checkbox.

    Init Params:
        *blocks (str | Markdown): The content of the item. It has to start with text.

    Markdown:
        An item with an unchecked box (`- [ ] item` inside a list).

    Example:
        BULLET_LIST(TASK_ITEM("write tests"), TASK_ITEM("write docs"))
        # Writes:
        # - [ ] write tests
        # - [ ] write docs

    Note:
        The checkbox is written in front of the first line of text, so an item that starts
        with code or a nested list is refused.
    """
    return ListItem(*blocks, checked=False)
