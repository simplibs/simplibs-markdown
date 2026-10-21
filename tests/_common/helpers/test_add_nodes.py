import pytest
from simplibs.markdown._common.helpers import add_nodes
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text


def _texts(blocks) -> list[str]:
    """The rendered text of every block, for a short comparison."""

    return [block.to_text() for block in blocks]


# ----------------------------------------------------------------------
# Inline with inline stays one line
# ----------------------------------------------------------------------

def test_add_nodes_two_inline_nodes_make_an_inline_join() -> None:
    """Verify two inline nodes become one InlineJoin."""

    result = add_nodes(Text("a"), Text("b"))

    assert isinstance(result, InlineJoin)
    assert len(result.parts) == 2
    assert result.to_text() == "ab"


def test_add_nodes_a_join_is_extended_not_nested() -> None:
    """Verify a join on one side gives its parts, so the result stays flat."""

    result = add_nodes(InlineJoin("a", "b"), Text("c"))

    assert isinstance(result, InlineJoin)
    assert len(result.parts) == 3
    assert result.to_text() == "abc"


def test_add_nodes_string_left_of_an_inline_node_becomes_escaped_text() -> None:
    """Verify a string next to an inline node takes its level and is escaped."""

    result = add_nodes("a*", Text("b"))

    assert isinstance(result, InlineJoin)
    assert [type(part) for part in result.parts] == [Text, Text]
    assert result.to_text() == r"a\*b"


def test_add_nodes_string_right_of_an_inline_node_becomes_escaped_text() -> None:
    """Verify the same rule when the string stands on the right."""

    result = add_nodes(Text("a"), "b*")

    assert isinstance(result, InlineJoin)
    assert result.to_text() == r"ab\*"


# ----------------------------------------------------------------------
# Anything with a block in it becomes a document
# ----------------------------------------------------------------------

def test_add_nodes_two_blocks_make_a_document() -> None:
    """Verify two blocks become a Document that holds them as they are."""

    first, second = Paragraph("a"), Paragraph("b")

    result = add_nodes(first, second)

    assert isinstance(result, Document)
    assert result.blocks[0] is first
    assert result.blocks[1] is second
    assert result.to_text() == "a\n\nb\n"


def test_add_nodes_inline_and_block_make_a_document() -> None:
    """Verify an inline node next to a block is wrapped into a paragraph."""

    result = add_nodes(Text("a"), Paragraph("b"))

    assert isinstance(result, Document)
    assert [type(block) for block in result.blocks] == [Paragraph, Paragraph]
    assert _texts(result.blocks) == ["a", "b"]


def test_add_nodes_string_left_of_a_block_becomes_a_paragraph() -> None:
    """Verify a string next to a block becomes a Paragraph on the left."""

    result = add_nodes("a", Paragraph("b"))

    assert isinstance(result, Document)
    assert [type(block) for block in result.blocks] == [Paragraph, Paragraph]
    assert _texts(result.blocks) == ["a", "b"]


def test_add_nodes_string_right_of_a_block_becomes_a_paragraph() -> None:
    """Verify a string next to a block becomes a Paragraph on the right."""

    result = add_nodes(Paragraph("a"), "b")

    assert isinstance(result, Document)
    assert _texts(result.blocks) == ["a", "b"]


def test_add_nodes_a_document_is_extended_not_nested() -> None:
    """Verify a Document on one side brings its blocks, so documents never nest."""

    result = add_nodes(Document("a", "b"), Paragraph("c"))

    assert isinstance(result, Document)
    assert _texts(result.blocks) == ["a", "b", "c"]


# ----------------------------------------------------------------------
# Not ours to compose
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "left, right",
    [
        ("a", "b"),              # two strings: Python's own `+` handles them
        (Text("a"), 5),
        (5, Text("a")),
        (Paragraph("a"), None),
        (None, Paragraph("a")),
        (Text("a"), ["b"]),
        (Text("a"), 3.14),
    ],
)
def test_add_nodes_returns_not_implemented(left, right) -> None:
    """Verify an operand that is neither a node nor a string is handed back to Python."""

    assert add_nodes(left, right) is NotImplemented


# ----------------------------------------------------------------------
# Through the `+` operator
# ----------------------------------------------------------------------

def test_plus_operator_inline_with_strings_on_both_sides() -> None:
    """Verify `"a" + node + "b"` is one line."""

    result = "a " + Text("b") + " c"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "a b c"


def test_plus_operator_blocks_make_a_document() -> None:
    """Verify `block + block` and `string + block` build a document."""

    result = "a" + Paragraph("b") + Paragraph("c")

    assert isinstance(result, Document)
    assert _texts(result.blocks) == ["a", "b", "c"]


def test_plus_operator_raises_type_error_for_a_foreign_operand() -> None:
    """Verify Python raises its own TypeError after `NotImplemented`."""

    with pytest.raises(TypeError):
        Text("a") + 5

    with pytest.raises(TypeError):
        5 + Text("a")
