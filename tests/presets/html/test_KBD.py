import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Html import Html
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.presets.html import KBD


def test_kbd_builds_an_inline_html_tag() -> None:
    """Verify the kind of node, the tag, the mode and the level."""

    node = KBD("x")

    assert isinstance(node, Html)
    assert node.tag == "kbd"
    assert node.mode is HtmlMode.INLINE
    assert node.node_level is NodeLevel.INLINE


def test_kbd_example_from_the_docstring() -> None:
    """Verify the sentence the docstring promises."""

    result = "Press " + KBD("Enter") + "."

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Press <kbd>Enter</kbd>."


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("x", "<kbd>x</kbd>"),
        ("", "<kbd></kbd>"),
        ("a*b", r"<kbd>a\*b</kbd>"),                 # a string is content: escaped
        (InlineCode("c"), "<kbd>`c`</kbd>"),         # a node is written as it is
        (["a", InlineCode("b")], "<kbd>a`b`</kbd>"), # a list is one line
    ],
)
def test_kbd_content(inner, expected) -> None:
    """Verify how the content is written between the tags."""

    node = KBD(inner)

    assert node.to_lines() == (expected,)
    assert node.to_text() == expected


def test_kbd_rejects_a_block_as_content(subtests) -> None:
    """Verify an inline tag cannot hold blocks."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        KBD,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_kbd_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        KBD,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
