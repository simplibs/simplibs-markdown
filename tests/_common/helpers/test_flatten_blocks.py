import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown._common.helpers import flatten_blocks
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.Text import Text


def _texts(blocks) -> list[str]:
    """The rendered text of every block, for a short comparison."""

    return [block.to_text() for block in blocks]


def test_flatten_blocks_without_items_gives_an_empty_tuple() -> None:
    """Verify no items give no blocks."""

    assert flatten_blocks() == ()


def test_flatten_blocks_returns_a_tuple() -> None:
    """Verify the result is a tuple."""

    assert isinstance(flatten_blocks("a", "b"), tuple)


@pytest.mark.parametrize("items", [(None,), (None, None), ([],), ((), [None])])
def test_flatten_blocks_skips_none_and_empty_collections(items) -> None:
    """Verify `None` and empty collections add nothing."""

    assert flatten_blocks(*items) == ()


def test_flatten_blocks_string_becomes_a_paragraph() -> None:
    """Verify a string gets a paragraph around it."""

    (block,) = flatten_blocks("text")

    assert isinstance(block, Paragraph)
    assert block.to_lines() == ("text",)


def test_flatten_blocks_empty_string_becomes_a_blank_line() -> None:
    """Verify the empty string is the explicit empty line."""

    (block,) = flatten_blocks("")

    assert isinstance(block, BlankLine)
    assert block.count == 1


def test_flatten_blocks_block_node_goes_in_as_it_is() -> None:
    """Verify a block node is kept, not copied."""

    paragraph = Paragraph("a")
    blank = BlankLine(2)

    result = flatten_blocks(paragraph, blank)

    assert result[0] is paragraph
    assert result[1] is blank


def test_flatten_blocks_inline_node_gets_a_paragraph() -> None:
    """Verify an inline node is wrapped into a paragraph."""

    (block,) = flatten_blocks(Text("a"))

    assert isinstance(block, Paragraph)
    assert block.to_lines() == ("a",)


def test_flatten_blocks_document_is_unpacked() -> None:
    """Verify a document gives its own blocks and is not nested."""

    first, second = Paragraph("a"), Paragraph("b")

    result = flatten_blocks(Document(first, second))

    assert len(result) == 2
    assert result[0] is first
    assert result[1] is second


def test_flatten_blocks_nested_collections_are_flattened_in_order() -> None:
    """Verify lists and tuples nest to any depth and keep the order."""

    result = flatten_blocks("a", ["b", ("c", ["d"])], "e")

    assert _texts(result) == ["a", "b", "c", "d", "e"]


def test_flatten_blocks_mixes_every_kind_of_item() -> None:
    """Verify strings, inline nodes, blocks, documents and collections work together."""

    result = flatten_blocks(
        "a",
        Text("b"),
        Paragraph("c"),
        None,
        Document("d", "e"),
        ["", "f"],
    )

    assert _texts(result) == ["a", "b", "c", "d", "e", "", "f"]
    assert [type(block) for block in result] == [Paragraph] * 5 + [BlankLine, Paragraph]


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}, b"bytes"])
def test_flatten_blocks_rejects_what_is_not_content(subtests, value) -> None:
    """Verify an item that is neither a string nor a node raises the not-markdown card."""

    assert_exception_function(
        subtests,
        flatten_blocks,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


def test_flatten_blocks_rejects_a_wrong_item_inside_a_collection(subtests) -> None:
    """Verify the check reaches into nested collections."""

    assert_exception_function(
        subtests,
        flatten_blocks,
        invalid_params=("a", ["b", ["c", 42]]),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=42,
        verbose=False,
    )
