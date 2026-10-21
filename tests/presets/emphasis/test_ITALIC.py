import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.enums import EmphasisKind, EmphasisMarker
from simplibs.markdown.presets.emphasis import ITALIC


def test_italic_builds_an_emphasis_of_this_kind() -> None:
    """Verify the kind of node, the kind, the default marker and the level."""

    node = ITALIC("x")

    assert isinstance(node, Emphasis)
    assert node.kind is EmphasisKind.EM
    assert node.marker is EmphasisMarker.ASTERISK
    assert node.node_level is NodeLevel.INLINE


def test_italic_writes_the_marker_around_the_text() -> None:
    """Verify the default form."""

    assert ITALIC("x").to_text() == "*x*"


def test_italic_example_from_the_docstring() -> None:
    """Verify the sentence the docstring promises."""

    result = "Read " + ITALIC("this") + " first."

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Read *this* first."


def test_italic_underscore_marker() -> None:
    """Verify the other marker."""

    node = ITALIC("x", EmphasisMarker.UNDERSCORE)

    assert node.marker is EmphasisMarker.UNDERSCORE
    assert node.to_text() == "_x_"


def test_italic_marker_may_be_given_by_name() -> None:
    """Verify the second parameter can be a keyword."""

    assert ITALIC("x", marker=EmphasisMarker.UNDERSCORE).to_text() == "_x_"


def test_italic_rejects_a_tilde_marker(subtests) -> None:
    """Verify only strike-through is written with a tilde."""

    assert_exception_function(
        subtests,
        ITALIC,
        invalid_params=("x", EmphasisMarker.TILDE),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_MARKER_KIND_MISMATCH",
        value=EmphasisMarker.TILDE,
        verbose=False,
    )


@pytest.mark.parametrize("marker", ["*", "_", 1, True])
def test_italic_rejects_a_marker_of_the_wrong_type(subtests, marker) -> None:
    """Verify the marker has to be an EmphasisMarker."""

    assert_exception_function(
        subtests,
        ITALIC,
        invalid_params=("x", marker),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'marker'",
        expected="EmphasisMarker",
        value=marker,
        verbose=False,
    )


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("a*b", r"*a\*b*"),              # a string is content: escaped
        (InlineCode("c"), "*`c`*"),      # a node is written as it is
        (["a ", InlineCode("b")], "*a `b`*"),
        (" x ", " *x* "),                # edge whitespace moves outside the marks
    ],
)
def test_italic_content(inner, expected) -> None:
    """Verify strings, nodes, lists and the whitespace rule."""

    assert ITALIC(inner).to_text() == expected


@pytest.mark.parametrize("inner", ["", "   ", "\t"])
def test_italic_rejects_an_empty_content(subtests, inner) -> None:
    """Verify there has to be something to emphasize."""

    assert_exception_function(
        subtests,
        ITALIC,
        invalid_params=(inner,),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_EMPTY_INNER",
        verbose=False,
    )
