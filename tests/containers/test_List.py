import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.containers.List import List
from simplibs.markdown.containers.ListItem import ListItem
from simplibs.markdown.containers.enums import ListMarker
from simplibs.markdown.inline.Text import Text

DASH = ListMarker.DASH
ASTERISK = ListMarker.ASTERISK
PLUS = ListMarker.PLUS
DOT = ListMarker.DOT
PAREN = ListMarker.PAREN


def _make(items, options: dict) -> List:
    """Create a List from items and keyword options."""

    return List(*items, **options)


def test_list_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = List("a")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_list_defaults() -> None:
    """Verify a tight bullet list with dashes."""

    node = List("a")

    assert node.ordered is False
    assert node.marker is DASH
    assert node.start == 1
    assert node.tight is True


def test_list_ordered_default_marker_is_a_dot() -> None:
    """Verify the default marker follows the kind of list."""

    assert List("a", ordered=True).marker is DOT


# ----------------------------------------------------------------------
# Items
# ----------------------------------------------------------------------

def test_list_every_item_is_a_list_item() -> None:
    """Verify strings and nodes are wrapped, a ListItem is kept."""

    item = ListItem("c")

    node = List("a", Paragraph("b"), item, Text("d"))

    assert isinstance(node.items, tuple)
    assert all(isinstance(entry, ListItem) for entry in node.items)
    assert node.items[2] is item
    assert len(node.items) == 4


def test_list_a_document_is_one_item() -> None:
    """Verify a document given as an item gives one item with its blocks."""

    node = List(Document("a", "b"))

    assert len(node.items) == 1
    assert len(node.items[0].blocks) == 2


# ----------------------------------------------------------------------
# Bullets
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "marker, mark",
    [(None, "-"), (DASH, "-"), (ASTERISK, "*"), (PLUS, "+")],
)
def test_list_bullet_markers(marker, mark) -> None:
    """Verify the marker in front of every item."""

    node = List("a", "b", marker=marker)

    assert node.to_lines() == (f"{mark} a", f"{mark} b")


def test_list_to_text_and_str() -> None:
    """Verify the rendered text."""

    node = List("a", "b")

    assert node.to_text() == "- a\n- b"
    assert str(node) == "- a\n- b"
    assert repr(node) == "List('- a\\n- b')"


# ----------------------------------------------------------------------
# Numbers
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "options, expected",
    [
        ({}, ("1. a", "2. b", "3. c")),
        ({"marker": DOT}, ("1. a", "2. b", "3. c")),
        ({"marker": PAREN}, ("1) a", "2) b", "3) c")),
        ({"start": 5}, ("5. a", "6. b", "7. c")),
        ({"start": 0}, ("0. a", "1. b", "2. c")),
        ({"start": 1, "marker": PAREN}, ("1) a", "2) b", "3) c")),
    ],
)
def test_list_ordered(options, expected) -> None:
    """Verify the numbers count from `start`."""

    assert List("a", "b", "c", ordered=True, **options).to_lines() == expected


def test_list_ordered_indents_by_the_width_of_each_marker() -> None:
    """Verify the lines after the first stay inside their own item (`9. ` is 3, `10. ` is 4)."""

    items = [ListItem(Paragraph("x", "y")), ListItem(Paragraph("x", "y"))]

    node = List(*items, ordered=True, start=9)

    assert node.to_lines() == ("9. x", "   y", "10. x", "    y")


# ----------------------------------------------------------------------
# Tight and loose
# ----------------------------------------------------------------------

def test_list_loose_when_asked() -> None:
    """Verify `tight=False` puts a blank line between the items."""

    assert List("a", "b", "c", tight=False).to_lines() == ("- a", "", "- b", "", "- c")


def test_list_loose_ordered() -> None:
    """Verify the same for a numbered list."""

    assert List("a", "b", ordered=True, tight=False).to_lines() == ("1. a", "", "2. b")


def test_list_is_loose_when_one_item_has_two_paragraphs() -> None:
    """Verify one item that cannot be tight makes the whole list loose."""

    node = List(ListItem("a", "b"), "c")

    assert node.to_lines() == ("- a", "", "  b", "", "- c")


def test_list_tight_with_a_code_block_inside_an_item() -> None:
    """Verify a code block inside an item does not make the list loose."""

    node = List(ListItem(Paragraph("a"), CodeBlock("x")), "b")

    assert node.to_lines() == ("- a", "  ```", "  x", "  ```", "- b")


# ----------------------------------------------------------------------
# Items with content of their own
# ----------------------------------------------------------------------

def test_list_checkboxes() -> None:
    """Verify task items."""

    node = List(ListItem("a", checked=True), ListItem("b", checked=False), "c")

    assert node.to_lines() == ("- [x] a", "- [ ] b", "- c")


def test_list_nested_list_is_indented_under_its_item() -> None:
    """Verify a list inside an item."""

    node = List(ListItem(Paragraph("a"), List("b", "c")), "d")

    assert node.to_lines() == ("- a", "  - b", "  - c", "- d")


def test_list_nested_list_under_a_numbered_item() -> None:
    """Verify the indentation follows the width of the number."""

    node = List(ListItem(Paragraph("a"), List("b")), ordered=True)

    assert node.to_lines() == ("1. a", "   - b")


def test_list_empty_item_is_the_bare_marker() -> None:
    """Verify an item without content has no trailing space."""

    assert List(ListItem(), "a").to_lines() == ("-", "- a")
    assert List(ListItem(), ordered=True).to_lines() == ("1.",)
    assert List(ListItem(), ordered=True, marker=PAREN).to_lines() == ("1)",)


def test_list_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(List("a"), "__dict__")


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("marker", ["-", ".", 1, True, DASH.value])
def test_list_rejects_a_marker_of_the_wrong_type(subtests, marker) -> None:
    """Verify `marker` has to be a ListMarker."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a",), {"marker": marker}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'marker'",
        expected="ListMarker",
        value=marker,
        verbose=False,
    )


@pytest.mark.parametrize(
    "ordered, marker",
    [
        (True, DASH),
        (True, ASTERISK),
        (True, PLUS),
        (False, DOT),
        (False, PAREN),
    ],
)
def test_list_rejects_a_marker_that_does_not_fit_the_kind(subtests, ordered, marker) -> None:
    """Verify numbers need a dot or a parenthesis, bullets need a dash, an asterisk or a plus."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a",), {"ordered": ordered, "marker": marker}),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_MARKER_ORDERED_MISMATCH",
        value=marker,
        verbose=False,
    )


@pytest.mark.parametrize("start", [-1, -100, "1", 1.5, None, True, False])
@pytest.mark.parametrize("ordered", [True, False])
def test_list_rejects_a_start_that_is_not_a_non_negative_integer(subtests, start, ordered) -> None:
    """Verify `start` is an integer of zero or more (a bool is not)."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a",), {"ordered": ordered, "start": start}),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_START_NEGATIVE",
        value=start,
        verbose=False,
    )


@pytest.mark.parametrize("start", [0, 2, 10])
def test_list_rejects_a_start_for_a_bullet_list(subtests, start) -> None:
    """Verify only a numbered list has a number to start from."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a",), {"start": start}),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_START_ON_BULLET",
        value=start,
        verbose=False,
    )


@pytest.mark.parametrize("items", [()])
def test_list_rejects_a_list_without_items(subtests, items) -> None:
    """Verify a list needs at least one item."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(items, {}),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_NO_ITEMS",
        verbose=False,
    )


@pytest.mark.parametrize("item", [42, 3.14, None, True, ["a"], ("a",), {"a": 1}])
def test_list_rejects_an_item_that_is_not_usable(subtests, item) -> None:
    """Verify an item is a ListItem, a string or a node (a list of strings is not an item)."""

    assert_exception_function(
        subtests,
        List,
        invalid_params=("a", item),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_ITEM_NOT_LIST_ITEM",
        value=item,
        verbose=False,
    )


def test_list_checks_the_marker_before_the_items(subtests) -> None:
    """Verify a wrong marker is reported even when there are no items."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=((), {"marker": "-"}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'marker'",
        verbose=False,
    )
