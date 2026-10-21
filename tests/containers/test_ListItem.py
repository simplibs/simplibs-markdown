import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Heading import Heading
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.List import List
from simplibs.markdown.containers.ListItem import ListItem


def _make(blocks, options: dict) -> ListItem:
    """Create a ListItem from blocks and keyword options."""

    return ListItem(*blocks, **options)


def test_list_item_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = ListItem("a")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_list_item_stores_its_parameters() -> None:
    """Verify the attributes and the default of `checked`."""

    node = ListItem("a", "b", checked=True)

    assert isinstance(node.blocks, tuple)
    assert len(node.blocks) == 2
    assert node.checked is True
    assert ListItem("a").checked is None


# ----------------------------------------------------------------------
# Alone, an item is a bullet item
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "arguments, expected",
    [
        # One paragraph
        ((("a",), {}), ("- a",)),
        # A paragraph of several lines: the rest is indented under the text
        (((Paragraph("a", "b"),), {}), ("- a", "  b")),
        # Two paragraphs cannot be tight, so the item is written loose
        ((("a", "b"), {}), ("- a", "", "  b")),
        # A paragraph and a code block can be tight
        (((Paragraph("a"), CodeBlock("x")), {}), ("- a", "  ```", "  x", "  ```")),
        # A nested list stays inside the item
        (((Paragraph("a"), List("b", "c")), {}), ("- a", "  - b", "  - c")),
        # Checkbox
        ((("a",), {"checked": True}), ("- [x] a",)),
        ((("a",), {"checked": False}), ("- [ ] a",)),
        # The checkbox goes in front of the first line only
        (((Paragraph("a", "b"),), {"checked": True}), ("- [x] a", "  b")),
        # An item without content is the bare marker
        (((), {}), ("-",)),
    ],
)
def test_list_item_alone(arguments, expected) -> None:
    """Verify the lines of an item written on its own."""

    blocks, options = arguments

    node = ListItem(*blocks, **options)

    assert node.to_lines() == expected
    assert node.to_text() == "\n".join(expected)
    assert str(node) == "\n".join(expected)


# ----------------------------------------------------------------------
# needs_loose
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "blocks, expected",
    [
        ((), False),
        (("a",), False),
        # Two paragraphs one after another
        (("a", "b"), True),
        (("a", "b", "c"), True),
        (("a", CodeBlock("x"), "b"), False),             # something stands between them
        (("a", BlankLine(), "b"), False),
        ((CodeBlock("x"), "a"), False),
        ((Paragraph("a"), List("b"), Paragraph("c")), False),
        # One pair is enough
        (("a", CodeBlock("x"), "b", "c"), True),
    ],
)
def test_list_item_needs_loose(blocks, expected) -> None:
    """Verify only two neighbouring paragraphs force a loose list."""

    assert ListItem(*blocks).needs_loose is expected


# ----------------------------------------------------------------------
# content_lines: the content without the marker
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "loose, expected",
    [
        (False, ("a", "b")),
        (True, ("a", "", "b")),
    ],
)
def test_list_item_content_lines_loose_or_tight(loose, expected) -> None:
    """Verify `loose` puts a blank line between the blocks."""

    assert ListItem("a", "b").content_lines(loose) == expected


@pytest.mark.parametrize(
    "checked, first_line",
    [
        (True, "[x] a"),
        (False, "[ ] a"),
        (None, "a"),
    ],
)
def test_list_item_content_lines_has_the_checkbox_on_the_first_line(checked, first_line) -> None:
    """Verify the checkbox is part of the content, in front of the first line."""

    assert ListItem("a", "b", checked=checked).content_lines(True) == (first_line, "", "b")


def test_list_item_content_lines_of_an_empty_item() -> None:
    """Verify no content gives no lines."""

    assert ListItem().content_lines(False) == ()
    assert ListItem().content_lines(True) == ()


def test_list_item_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(ListItem("a"), "__dict__")


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("checked", [True, False])
@pytest.mark.parametrize(
    "blocks",
    [
        (),
        (None,),
        (CodeBlock("x"),),
        (Heading("h"),),
        (List("a"), "b"),
        (BlankLine(), "a"),
    ],
)
def test_list_item_rejects_a_checkbox_without_a_paragraph_first(subtests, checked, blocks) -> None:
    """Verify the checkbox needs text to stand in front of."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(blocks, {"checked": checked}),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_ITEM_CHECKED_WITHOUT_CONTENT",
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_list_item_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        ListItem,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
