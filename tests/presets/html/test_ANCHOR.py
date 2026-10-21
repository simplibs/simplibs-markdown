import pytest
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Html import Html
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.presets.html import ANCHOR


def test_anchor_builds_an_inline_a_tag_with_an_id() -> None:
    """Verify the kind of node, the tag, the attribute, the mode and the level."""

    node = ANCHOR("top")

    assert isinstance(node, Html)
    assert node.tag == "a"
    assert node.attrs == {"id": "top"}
    assert node.mode is HtmlMode.INLINE
    assert node.node_level is NodeLevel.INLINE


def test_anchor_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    assert ANCHOR("top").to_text() == '<a id="top"></a>'


@pytest.mark.parametrize(
    "name, expected",
    [
        ("top", '<a id="top"></a>'),
        ("section-2", '<a id="section-2"></a>'),
        ("a b", '<a id="a b"></a>'),
        # A quote cannot end the attribute
        ('a"b', '<a id="a&quot;b"></a>'),
        ("a&b", '<a id="a&amp;b"></a>'),
    ],
)
def test_anchor_name_is_written_as_an_escaped_attribute(name, expected) -> None:
    """Verify the name is the value of `id`."""

    assert ANCHOR(name).to_text() == expected


def test_anchor_stands_inside_a_line() -> None:
    """Verify it can be added to text, like any inline node."""

    result = "Intro " + ANCHOR("top") + " text"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == 'Intro <a id="top"></a> text'
