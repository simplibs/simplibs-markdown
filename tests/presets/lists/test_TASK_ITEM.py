import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.ListItem import ListItem
from simplibs.markdown.presets.lists import BULLET_LIST, DONE_ITEM, NUMBERED_LIST, TASK_ITEM


def test_task_item_builds_a_list_item_with_the_checked_flag_False() -> None:
    """Verify the kind of node, the checkbox state (unchecked) and the level."""

    node = TASK_ITEM("text")

    assert isinstance(node, ListItem)
    assert node.checked is False
    assert node.node_level is NodeLevel.BLOCK


def test_task_item_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert BULLET_LIST(TASK_ITEM("write tests"), TASK_ITEM("write docs")).to_lines() == ("- [ ] write tests", "- [ ] write docs")


@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("a",), ("- [ ] a",)),
        # The checkbox stands in front of the first line only
        ((Paragraph("a", "b"),), ("- [ ] a", "  b")),
        # Several paragraphs make the item loose
        (("a", "b"), ("- [ ] a", "", "  b")),
        # Something other than a paragraph may follow the first paragraph
        ((Paragraph("a"), CodeBlock("x")), ("- [ ] a", "  ```", "  x", "  ```")),
    ],
)
def test_task_item_alone(blocks, expected) -> None:
    """Verify an item written on its own."""

    assert TASK_ITEM(*blocks).to_lines() == expected


def test_task_item_in_a_numbered_list() -> None:
    """Verify it takes the marker of the list around it."""

    assert NUMBERED_LIST(TASK_ITEM("a"), "b").to_lines() == ("1. [ ] a", "2. b")


@pytest.mark.parametrize("blocks", [(), (CodeBlock("x"),), (BULLET_LIST("a"),)])
def test_task_item_rejects_an_item_that_does_not_start_with_text(subtests, blocks) -> None:
    """Verify the checkbox needs a paragraph to stand in front of."""

    assert_exception_function(
        subtests,
        TASK_ITEM,
        invalid_params=blocks,
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_ITEM_CHECKED_WITHOUT_CONTENT",
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_task_item_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        TASK_ITEM,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
