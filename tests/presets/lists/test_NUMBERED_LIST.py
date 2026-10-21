import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.containers.List import List
from simplibs.markdown.containers.ListItem import ListItem
from simplibs.markdown.containers.enums import ListMarker
from simplibs.markdown.presets.lists import BULLET_LIST, NUMBERED_LIST


def test_numbered_list_builds_a_tight_ordered_list() -> None:
    """Verify the kind of node, the defaults and the level."""

    node = NUMBERED_LIST("a", "b")

    assert isinstance(node, List)
    assert node.ordered is True
    assert node.marker is ListMarker.DOT
    assert node.start == 1
    assert node.tight is True
    assert node.node_level is NodeLevel.BLOCK


@pytest.mark.parametrize(
    "arguments, options, expected",
    [
        # The examples from the docstring
        (("first", "second"), {}, ("1. first", "2. second")),
        (("first", "second"), {"start": 3, "marker": ListMarker.PAREN}, ("3) first", "4) second")),
        # Other starts and markers
        (("a", "b", "c"), {"start": 0}, ("0. a", "1. b", "2. c")),
        (("a", "b"), {"marker": ListMarker.PAREN}, ("1) a", "2) b")),
        # A loose list
        (("a", "b"), {"tight": False}, ("1. a", "", "2. b")),
        # One item
        (("only",), {}, ("1. only",)),
    ],
)
def test_numbered_list_lines(arguments, options, expected) -> None:
    """Verify the numbers, the marker and the spacing."""

    assert NUMBERED_LIST(*arguments, **options).to_lines() == expected


def test_numbered_list_nested_list_follows_the_width_of_the_number() -> None:
    """Verify a list inside an item is indented under the text."""

    node = NUMBERED_LIST(ListItem("a", BULLET_LIST("b")))

    assert node.to_lines() == ("1. a", "   - b")


def test_numbered_list_start_marker_and_tight_are_keyword_only() -> None:
    """Verify a value given by position is an item, not an option."""

    with pytest.raises(ParamError) as caught:
        NUMBERED_LIST("a", 3)

    assert caught.value.error_name == "MARKDOWN_LIST_ITEM_NOT_LIST_ITEM"


def test_numbered_list_has_no_ordered_parameter() -> None:
    """Verify the preset fixes the kind of list."""

    with pytest.raises(TypeError):
        NUMBERED_LIST("a", ordered=False)


@pytest.mark.parametrize("marker", [ListMarker.DASH, ListMarker.ASTERISK, ListMarker.PLUS])
def test_numbered_list_rejects_a_bullet_marker(marker) -> None:
    """Verify a dash, an asterisk or a plus belongs to bullet lists."""

    with pytest.raises(ParamError) as caught:
        NUMBERED_LIST("a", marker=marker)

    assert caught.value.error_name == "MARKDOWN_LIST_MARKER_ORDERED_MISMATCH"
    assert caught.value.value is marker


@pytest.mark.parametrize("start", [-1, "1", 1.5, None, True])
def test_numbered_list_rejects_a_start_that_is_not_a_non_negative_integer(start) -> None:
    """Verify `start` is an integer of zero or more (a bool is not)."""

    with pytest.raises(ParamError) as caught:
        NUMBERED_LIST("a", start=start)

    assert caught.value.error_name == "MARKDOWN_LIST_START_NEGATIVE"
    assert caught.value.value == start


def test_numbered_list_rejects_no_items(subtests) -> None:
    """Verify a list needs at least one item."""

    assert_exception_function(
        subtests,
        NUMBERED_LIST,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_NO_ITEMS",
        verbose=False,
    )
