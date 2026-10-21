import pytest
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document


class _Lines(Markdown):
    """A minimal block node, only to test what the base class gives."""

    __slots__ = ("lines",)
    node_level = NodeLevel.BLOCK

    def __init__(self, *lines: str) -> None:
        self.lines = lines

    def to_lines(self) -> tuple[str, ...]:
        return tuple(self.lines)


def test_markdown_cannot_be_instantiated() -> None:
    """Verify the base class is abstract."""

    with pytest.raises(TypeError):
        Markdown()


def test_markdown_subclass_must_implement_to_lines() -> None:
    """Verify a node without `to_lines` cannot be created."""

    class _Incomplete(Markdown):
        __slots__ = ()

    with pytest.raises(TypeError):
        _Incomplete()


def test_markdown_subclass_with_to_lines_can_be_created() -> None:
    """Verify `to_lines` is the only thing a node has to write."""

    assert isinstance(_Lines("a"), Markdown)


@pytest.mark.parametrize(
    "lines, expected",
    [
        ((), ""),
        (("a",), "a"),
        (("a", "b"), "a\nb"),
        (("a", "", "b"), "a\n\nb"),
        (("", ""), "\n"),
    ],
)
def test_markdown_to_text_joins_the_lines(lines, expected) -> None:
    """Verify `to_text` is the lines joined by line breaks, and nothing else."""

    assert _Lines(*lines).to_text() == expected


def test_markdown_to_text_has_no_trailing_newline() -> None:
    """Verify the text does not end with a line break."""

    assert not _Lines("a", "b").to_text().endswith("\n")


@pytest.mark.parametrize("lines", [(), ("a",), ("a", "b"), ("x", "", "y")])
def test_markdown_str_is_to_text(lines) -> None:
    """Verify `str(node)` is the rendered text."""

    node = _Lines(*lines)

    assert str(node) == node.to_text()


@pytest.mark.parametrize("lines", [("a",), ("a", "b"), ("it's",), ('say "hi"',)])
def test_markdown_repr_shows_the_class_and_the_text(lines) -> None:
    """Verify `repr` is `ClassName('text')`."""

    node = _Lines(*lines)

    assert repr(node) == f"_Lines({node.to_text()!r})"


def test_markdown_repr_example() -> None:
    """Verify one literal example of the representation."""

    assert repr(_Lines("a", "b")) == "_Lines('a\\nb')"


def test_markdown_subclass_with_slots_has_no_instance_dict() -> None:
    """Verify the base class adds no `__dict__`, so slots stay in force."""

    assert not hasattr(_Lines("a"), "__dict__")


# ----------------------------------------------------------------------
# `+` goes through add_nodes
# ----------------------------------------------------------------------

def test_markdown_add_with_a_string_on_the_right() -> None:
    """Verify `node + "text"` builds a document for a block node."""

    result = _Lines("a") + "b"

    assert isinstance(result, Document)
    assert [block.to_text() for block in result.blocks] == ["a", "b"]


def test_markdown_radd_with_a_string_on_the_left() -> None:
    """Verify `"text" + node` keeps the order."""

    result = "a" + _Lines("b")

    assert isinstance(result, Document)
    assert [block.to_text() for block in result.blocks] == ["a", "b"]


def test_markdown_add_with_another_node() -> None:
    """Verify two nodes give one document holding both."""

    first, second = _Lines("a"), Paragraph("b")

    result = first + second

    assert isinstance(result, Document)
    assert result.blocks[0] is first
    assert result.blocks[1] is second


@pytest.mark.parametrize("other", [5, 3.14, None, ["a"], {"a": 1}])
def test_markdown_add_with_a_foreign_operand_raises_type_error(other) -> None:
    """Verify Python raises TypeError when the other operand is neither a node nor a string."""

    with pytest.raises(TypeError):
        _Lines("a") + other

    with pytest.raises(TypeError):
        other + _Lines("a")
