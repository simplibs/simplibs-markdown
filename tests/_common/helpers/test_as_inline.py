import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown._common.helpers import as_inline
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text


@pytest.mark.parametrize("value", ["plain", "a*b", "", "# not a heading"])
def test_as_inline_string_becomes_escaped_text(value) -> None:
    """Verify a string becomes a Text with escaping on."""

    result = as_inline(value)

    assert isinstance(result, Text)
    assert result.value == value
    assert result.escape is True
    assert result.to_text() == Text(value).to_text()


def test_as_inline_string_is_escaped() -> None:
    """Verify the special characters of a string are escaped in the output."""

    assert as_inline("a*b").to_text() == r"a\*b"


@pytest.mark.parametrize(
    "node",
    [Text("a"), Text("b", escape=False), InlineJoin("a", "b")],
)
def test_as_inline_inline_node_is_returned_as_it_is(node) -> None:
    """Verify an inline node passes through without being copied or wrapped."""

    assert as_inline(node) is node


@pytest.mark.parametrize("container", [list, tuple])
def test_as_inline_collection_becomes_one_join(container) -> None:
    """Verify a list or a tuple is joined into one inline node."""

    result = as_inline(container(["a", Text("b")]))

    assert isinstance(result, InlineJoin)
    assert [type(part) for part in result.parts] == [Text, Text]
    assert result.to_text() == "ab"


def test_as_inline_empty_collection_gives_an_empty_join() -> None:
    """Verify an empty list is accepted and renders as nothing."""

    result = as_inline([])

    assert isinstance(result, InlineJoin)
    assert result.parts == ()
    assert result.to_text() == ""


def test_as_inline_nested_collections_are_flattened() -> None:
    """Verify nested lists end up as one flat sequence of parts."""

    result = as_inline(["a", ["b", ("c",)]])

    assert isinstance(result, InlineJoin)
    assert len(result.parts) == 3
    assert result.to_text() == "abc"


@pytest.mark.parametrize("block", [Paragraph("text"), BlankLine(), Document("a")])
def test_as_inline_rejects_a_block_node(subtests, block) -> None:
    """Verify a block node raises the block-in-inline card."""

    assert_exception_function(
        subtests,
        as_inline,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


def test_as_inline_rejects_a_block_inside_a_collection(subtests) -> None:
    """Verify one block among inline parts is enough to refuse the whole list."""

    block = Paragraph("text")

    assert_exception_function(
        subtests,
        as_inline,
        invalid_params=(["a", block],),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, None, True, {"a": 1}, b"bytes"])
def test_as_inline_rejects_what_is_not_content(subtests, value) -> None:
    """Verify a value that is neither a string, a node nor a collection raises the not-markdown card."""

    assert_exception_function(
        subtests,
        as_inline,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


def test_as_inline_rejects_a_non_content_part_of_a_collection(subtests) -> None:
    """Verify one wrong part in a list raises the not-markdown card for that part."""

    assert_exception_function(
        subtests,
        as_inline,
        invalid_params=(["a", 42],),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=42,
        verbose=False,
    )
