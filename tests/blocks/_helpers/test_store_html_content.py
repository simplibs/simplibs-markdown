import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.blocks._helpers import store_html_content
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text

# Everything but INLINE follows the same path
BLOCK_MODES = [HtmlMode.BLOCK, HtmlMode.COMMENT]


def _texts(blocks) -> list[str]:
    """The rendered text of every block, for a short comparison."""

    return [block.to_text() for block in blocks]


# ----------------------------------------------------------------------
# No content
# ----------------------------------------------------------------------

@pytest.mark.parametrize("mode", list(HtmlMode))
def test_store_html_content_none_is_none(mode) -> None:
    """Verify no content stays no content in every mode."""

    assert store_html_content(None, mode) is None


# ----------------------------------------------------------------------
# An inline tag holds a line, whatever it was given as
# ----------------------------------------------------------------------

def test_store_html_content_inline_string_becomes_text() -> None:
    """Verify a string becomes a Text."""

    result = store_html_content("Ctrl", HtmlMode.INLINE)

    assert isinstance(result, Text)
    assert result.value == "Ctrl"


def test_store_html_content_inline_list_becomes_one_join() -> None:
    """Verify a list is one line of inline content, not blocks."""

    result = store_html_content(["Ctrl", "+", "C"], HtmlMode.INLINE)

    assert isinstance(result, InlineJoin)
    assert len(result.parts) == 3
    assert all(isinstance(part, Text) for part in result.parts)
    assert result.to_text() == "".join(part.to_text() for part in result.parts)


def test_store_html_content_inline_node_is_kept() -> None:
    """Verify an inline node passes through as it is."""

    node = Text("x")

    assert store_html_content(node, HtmlMode.INLINE) is node


def test_store_html_content_inline_rejects_a_block(subtests) -> None:
    """Verify a block node is refused in an inline tag."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        store_html_content,
        invalid_params=(block, HtmlMode.INLINE),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_store_html_content_inline_rejects_what_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        store_html_content,
        invalid_params=(value, HtmlMode.INLINE),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


# ----------------------------------------------------------------------
# Other modes: one line for a string or an inline node, blocks for the rest
# ----------------------------------------------------------------------

@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_string_stays_on_the_line(mode) -> None:
    """Verify a string is inline content, so the tag can stay on one line."""

    result = store_html_content("Title", mode)

    assert isinstance(result, Text)
    assert result.value == "Title"


@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_empty_string_is_inline_text(mode) -> None:
    """Verify the empty string is an empty Text, not a blank line."""

    result = store_html_content("", mode)

    assert isinstance(result, Text)
    assert result.value == ""


@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_inline_node_stays_on_the_line(mode) -> None:
    """Verify an inline node is kept as it is."""

    for node in (Text("x"), InlineJoin("a", "b")):
        assert store_html_content(node, mode) is node


@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_block_node_gives_a_tuple_of_blocks(mode) -> None:
    """Verify a block node comes back in a tuple, not copied."""

    paragraph = Paragraph("a")

    result = store_html_content(paragraph, mode)

    assert isinstance(result, tuple)
    assert len(result) == 1
    assert result[0] is paragraph


@pytest.mark.parametrize("mode", BLOCK_MODES)
@pytest.mark.parametrize("container", [list, tuple])
def test_store_html_content_a_list_is_blocks(mode, container) -> None:
    """Verify a list or a tuple is read as blocks, even a list of one string."""

    result = store_html_content(container(["a"]), mode)

    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], Paragraph)

    result = store_html_content(container(["a", Paragraph("b"), ""]), mode)

    assert [type(block) for block in result] == [Paragraph, Paragraph, BlankLine]
    assert _texts(result) == ["a", "b", ""]


@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_a_document_is_unpacked(mode) -> None:
    """Verify a document gives its blocks."""

    first, second = Paragraph("a"), Paragraph("b")

    result = store_html_content(Document(first, second), mode)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] is first
    assert result[1] is second


@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_rejects_what_is_not_content(subtests, mode) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        store_html_content,
        invalid_params=(42, mode),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=42,
        verbose=False,
    )


@pytest.mark.parametrize("mode", BLOCK_MODES)
def test_store_html_content_rejects_a_wrong_item_in_a_list(subtests, mode) -> None:
    """Verify the check reaches into the list."""

    assert_exception_function(
        subtests,
        store_html_content,
        invalid_params=(["a", 42], mode),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=42,
        verbose=False,
    )
