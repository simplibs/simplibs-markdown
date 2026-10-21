import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.enums import EmphasisKind, EmphasisMarker
from simplibs.markdown.presets.emphasis import STRIKETHROUGH


def test_strikethrough_builds_an_emphasis_of_this_kind() -> None:
    """Verify the kind of node, the kind, the default marker and the level."""

    node = STRIKETHROUGH("x")

    assert isinstance(node, Emphasis)
    assert node.kind is EmphasisKind.STRIKE
    assert node.marker is EmphasisMarker.TILDE
    assert node.node_level is NodeLevel.INLINE


def test_strikethrough_writes_the_marker_around_the_text() -> None:
    """Verify the default form."""

    assert STRIKETHROUGH("x").to_text() == "~~x~~"


def test_strikethrough_example_from_the_docstring() -> None:
    """Verify the sentence the docstring promises."""

    result = "Price " + STRIKETHROUGH("10 EUR") + " 8 EUR"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Price ~~10 EUR~~ 8 EUR"


def test_strikethrough_has_no_marker_parameter() -> None:
    """Verify only the tilde writes strike-through, so a marker cannot be given."""

    with pytest.raises(TypeError):
        STRIKETHROUGH("x", EmphasisMarker.TILDE)

    with pytest.raises(TypeError):
        STRIKETHROUGH("x", marker=EmphasisMarker.TILDE)


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("a*b", r"~~a\*b~~"),              # a string is content: escaped
        (InlineCode("c"), "~~`c`~~"),      # a node is written as it is
        (["a ", InlineCode("b")], "~~a `b`~~"),
        (" x ", " ~~x~~ "),                # edge whitespace moves outside the marks
    ],
)
def test_strikethrough_content(inner, expected) -> None:
    """Verify strings, nodes, lists and the whitespace rule."""

    assert STRIKETHROUGH(inner).to_text() == expected


@pytest.mark.parametrize("inner", ["", "   ", "\t"])
def test_strikethrough_rejects_an_empty_content(subtests, inner) -> None:
    """Verify there has to be something to emphasize."""

    assert_exception_function(
        subtests,
        STRIKETHROUGH,
        invalid_params=(inner,),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_EMPTY_INNER",
        verbose=False,
    )
