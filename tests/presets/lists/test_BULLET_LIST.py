import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.containers.List import List
from simplibs.markdown.containers.ListItem import ListItem
from simplibs.markdown.containers.enums import ListMarker
from simplibs.markdown.presets.lists import BULLET_LIST, DONE_ITEM, TASK_ITEM


def test_bullet_list_builds_a_tight_bullet_list() -> None:
    """Verify the kind of node, the defaults and the level."""

    node = BULLET_LIST("a", "b")

    assert isinstance(node, List)
    assert node.ordered is False
    assert node.marker is ListMarker.DASH
    assert node.tight is True
    assert node.node_level is NodeLevel.BLOCK


@pytest.mark.parametrize(
    "arguments, options, expected",
    [
        # The examples from the docstring
        (("first", "second"), {}, ("- first", "- second")),
        (("first", "second"), {"marker": ListMarker.ASTERISK}, ("* first", "* second")),
        # The other marker
        (("a", "b"), {"marker": ListMarker.PLUS}, ("+ a", "+ b")),
        # A loose list
        (("a", "b"), {"tight": False}, ("- a", "", "- b")),
        # One item
        (("only",), {}, ("- only",)),
    ],
)
def test_bullet_list_lines(arguments, options, expected) -> None:
    """Verify the marker and the spacing."""

    assert BULLET_LIST(*arguments, **options).to_lines() == expected


def test_bullet_list_nested_example_from_the_docstring() -> None:
    """Verify a list inside an item."""

    node = BULLET_LIST("first", ListItem("second", BULLET_LIST("nested")))

    assert node.to_lines() == ("- first", "- second", "  - nested")


def test_bullet_list_with_task_items() -> None:
    """Verify checkboxes work in a bullet list."""

    node = BULLET_LIST(DONE_ITEM("a"), TASK_ITEM("b"), "c")

    assert node.to_lines() == ("- [x] a", "- [ ] b", "- c")


def test_bullet_list_marker_and_tight_are_keyword_only() -> None:
    """Verify a value given by position is an item, not the marker."""

    with pytest.raises(ParamError) as caught:
        BULLET_LIST("a", ListMarker.ASTERISK)

    assert caught.value.error_name == "MARKDOWN_LIST_ITEM_NOT_LIST_ITEM"


def test_bullet_list_has_no_numbering_parameters() -> None:
    """Verify a bullet list cannot be started from a number."""

    with pytest.raises(TypeError):
        BULLET_LIST("a", start=2)

    with pytest.raises(TypeError):
        BULLET_LIST("a", ordered=True)


@pytest.mark.parametrize("marker", [ListMarker.DOT, ListMarker.PAREN])
def test_bullet_list_rejects_a_numbering_marker(marker) -> None:
    """Verify a dot or a parenthesis belongs to numbered lists."""

    with pytest.raises(ParamError) as caught:
        BULLET_LIST("a", marker=marker)

    assert caught.value.error_name == "MARKDOWN_LIST_MARKER_ORDERED_MISMATCH"
    assert caught.value.value is marker


def test_bullet_list_rejects_no_items(subtests) -> None:
    """Verify a list needs at least one item."""

    assert_exception_function(
        subtests,
        BULLET_LIST,
        invalid_params=(),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_NO_ITEMS",
        verbose=False,
    )


@pytest.mark.parametrize("item", [42, None, ["a"], {"a": 1}])
def test_bullet_list_rejects_an_item_that_is_not_usable(subtests, item) -> None:
    """Verify an item is a string, a node or a ListItem."""

    assert_exception_function(
        subtests,
        BULLET_LIST,
        invalid_params=("a", item),
        exception_type=ParamError,
        error_name="MARKDOWN_LIST_ITEM_NOT_LIST_ITEM",
        value=item,
        verbose=False,
    )
