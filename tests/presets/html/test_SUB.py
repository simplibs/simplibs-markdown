import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Html import Html
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.presets.html import SUB


def test_sub_builds_an_inline_html_tag() -> None:
    """Verify the kind of node, the tag, the mode and the level."""

    node = SUB("x")

    assert isinstance(node, Html)
    assert node.tag == "sub"
    assert node.mode is HtmlMode.INLINE
    assert node.node_level is NodeLevel.INLINE


def test_sub_example_from_the_docstring() -> None:
    """Verify the sentence the docstring promises."""

    result = "H" + SUB("2") + "O"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "H<sub>2</sub>O"


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("x", "<sub>x</sub>"),
        ("", "<sub></sub>"),
        ("a*b", r"<sub>a\*b</sub>"),                 # a string is content: escaped
        (InlineCode("c"), "<sub>`c`</sub>"),         # a node is written as it is
        (["a", InlineCode("b")], "<sub>a`b`</sub>"), # a list is one line
    ],
)
def test_sub_content(inner, expected) -> None:
    """Verify how the content is written between the tags."""

    node = SUB(inner)

    assert node.to_lines() == (expected,)
    assert node.to_text() == expected


def test_sub_rejects_a_block_as_content(subtests) -> None:
    """Verify an inline tag cannot hold blocks."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        SUB,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_sub_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        SUB,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
