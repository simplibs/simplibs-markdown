import pytest
from simplibs.markdown.base_class import InlineMarkdown, Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.InlineJoin import InlineJoin


class _Fixed(InlineMarkdown):
    """A minimal inline node, only to test what the base class gives."""

    __slots__ = ("inline",)

    def __init__(self, inline: str) -> None:
        self.inline = inline

    def to_inline(self) -> str:
        return self.inline


def test_inline_markdown_is_a_markdown() -> None:
    """Verify an inline node is a Markdown node."""

    assert issubclass(InlineMarkdown, Markdown)
    assert isinstance(_Fixed("a"), Markdown)


def test_inline_markdown_node_level_is_inline() -> None:
    """Verify the level is set once, for every inline node."""

    assert InlineMarkdown.node_level is NodeLevel.INLINE
    assert _Fixed("a").node_level is NodeLevel.INLINE


def test_inline_markdown_cannot_be_instantiated() -> None:
    """Verify the base class is abstract."""

    with pytest.raises(TypeError):
        InlineMarkdown()


def test_inline_markdown_subclass_must_implement_to_inline() -> None:
    """Verify `to_inline` is the only thing an inline node has to write."""

    class _Incomplete(InlineMarkdown):
        __slots__ = ()

    with pytest.raises(TypeError):
        _Incomplete()


@pytest.mark.parametrize("text", ["", "a", "a b", "*x*", "a\nb", "a\n"])
def test_inline_markdown_to_text_is_to_inline(text) -> None:
    """Verify an inline node is already one string."""

    assert _Fixed(text).to_text() == text


def test_inline_markdown_to_text_does_not_use_the_lines() -> None:
    """Verify `to_text` does not go through `to_lines`."""

    class _NoLines(_Fixed):
        __slots__ = ()

        def to_lines(self):
            raise AssertionError("to_lines must not be called")

    assert _NoLines("a").to_text() == "a"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", ("",)),
        ("a", ("a",)),
        ("a b", ("a b",)),
        ("a\nb", ("a", "b")),
        ("a\n\nb", ("a", "", "b")),
        ("a\n", ("a", "")),
        ("\n", ("", "")),
    ],
)
def test_inline_markdown_to_lines_splits_at_line_breaks(text, expected) -> None:
    """Verify only a line break inside the text gives more than one line."""

    assert _Fixed(text).to_lines() == expected


@pytest.mark.parametrize("text", ["", "a", "a\nb", "x\n\ny"])
def test_inline_markdown_lines_and_text_agree(text) -> None:
    """Verify joining the lines gives the text back."""

    node = _Fixed(text)

    assert "\n".join(node.to_lines()) == node.to_text()


def test_inline_markdown_str_and_repr() -> None:
    """Verify the shared dunder methods work on the inline text."""

    node = _Fixed("a*b")

    assert str(node) == "a*b"
    assert repr(node) == "_Fixed('a*b')"


def test_inline_markdown_add_gives_an_inline_join() -> None:
    """Verify two inline nodes added together stay one line."""

    result = _Fixed("a") + _Fixed("b")

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "ab"
