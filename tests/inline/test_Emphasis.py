import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.Text import Text
from simplibs.markdown.inline.enums import EmphasisKind, EmphasisMarker

ASTERISK = EmphasisMarker.ASTERISK
UNDERSCORE = EmphasisMarker.UNDERSCORE
TILDE = EmphasisMarker.TILDE


def test_emphasis_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(Emphasis("x"), InlineMarkdown)


def test_emphasis_defaults() -> None:
    """Verify the kind is EM and the marker follows from the kind."""

    node = Emphasis("x")

    assert node.kind is EmphasisKind.EM
    assert node.marker is ASTERISK
    assert Emphasis("x", EmphasisKind.STRIKE).marker is TILDE


def test_emphasis_stores_an_inline_node_as_inner() -> None:
    """Verify a string becomes a Text, a node is kept."""

    assert isinstance(Emphasis("x").inner, Text)

    inner = InlineCode("c")
    assert Emphasis(inner).inner is inner


@pytest.mark.parametrize(
    "kind, marker, expected",
    [
        # Asterisks
        (EmphasisKind.EM, None, "*x*"),
        (EmphasisKind.STRONG, None, "**x**"),
        (EmphasisKind.STRONG_EM, None, "***x***"),
        (EmphasisKind.EM, ASTERISK, "*x*"),
        # Underscores
        (EmphasisKind.EM, UNDERSCORE, "_x_"),
        (EmphasisKind.STRONG, UNDERSCORE, "__x__"),
        (EmphasisKind.STRONG_EM, UNDERSCORE, "___x___"),
        # Strike-through is the only kind written with a tilde
        (EmphasisKind.STRIKE, None, "~~x~~"),
        (EmphasisKind.STRIKE, TILDE, "~~x~~"),
    ],
)
def test_emphasis_wraps_the_content_in_the_marker(kind, marker, expected) -> None:
    """Verify the marker is repeated as often as the kind needs."""

    assert Emphasis("x", kind, marker).to_inline() == expected


@pytest.mark.parametrize(
    "inner, expected",
    [
        (" x ", " *x* "),
        ("  text  ", "  *text*  "),
        ("x ", "*x* "),
        (" x", " *x*"),
        ("a b", "*a b*"),
        (" a b ", " *a b* "),
    ],
)
def test_emphasis_moves_edge_whitespace_outside_the_markers(inner, expected) -> None:
    """Verify `** text **` is never written, because it is no emphasis in CommonMark."""

    assert Emphasis(inner).to_inline() == expected


def test_emphasis_edge_whitespace_with_a_strong_kind() -> None:
    """Verify the same for a repeated marker."""

    assert Emphasis("  text  ", EmphasisKind.STRONG).to_inline() == "  **text**  "


@pytest.mark.parametrize(
    "inner, expected",
    [
        ("a*b", r"*a\*b*"),                          # a string is content: escaped
        (Text("a*b", escape=False), "*a*b*"),        # raw text is kept
        (InlineCode("c"), "*`c`*"),                  # a node is written as it is
        (["a", InlineCode("b")], "*a`b`*"),          # a list is one inline run
    ],
)
def test_emphasis_inner_content(inner, expected) -> None:
    """Verify strings, nodes and lists as the content."""

    assert Emphasis(inner).to_inline() == expected


def test_emphasis_to_text_and_str() -> None:
    """Verify the inline text is the text."""

    node = Emphasis("x", EmphasisKind.STRONG)

    assert node.to_text() == "**x**"
    assert str(node) == "**x**"
    assert node.to_lines() == ("**x**",)


def test_emphasis_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Emphasis("x"), "__dict__")


@pytest.mark.parametrize("kind", ["em", None, 1, "EM", True])
def test_emphasis_rejects_a_kind_of_the_wrong_type(subtests, kind) -> None:
    """Verify `kind` has to be an EmphasisKind."""

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=("x", kind),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'kind'",
        expected="EmphasisKind",
        value=kind,
        verbose=False,
    )


@pytest.mark.parametrize("marker", ["*", "_", 1, True, ASTERISK.value])
def test_emphasis_rejects_a_marker_of_the_wrong_type(subtests, marker) -> None:
    """Verify `marker` has to be an EmphasisMarker."""

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=("x", EmphasisKind.EM, marker),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'marker'",
        expected="EmphasisMarker",
        value=marker,
        verbose=False,
    )


@pytest.mark.parametrize(
    "kind, marker",
    [
        (EmphasisKind.STRIKE, ASTERISK),
        (EmphasisKind.STRIKE, UNDERSCORE),
        (EmphasisKind.EM, TILDE),
        (EmphasisKind.STRONG, TILDE),
        (EmphasisKind.STRONG_EM, TILDE),
    ],
)
def test_emphasis_rejects_a_marker_that_does_not_fit_the_kind(subtests, kind, marker) -> None:
    """Verify only strike-through is written with a tilde."""

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=("x", kind, marker),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_MARKER_KIND_MISMATCH",
        value=marker,
        verbose=False,
    )


@pytest.mark.parametrize(
    "inner, rendered",
    [
        ("", ""),
        ("   ", "   "),
        ("\t", "\t"),
        (Text(""), ""),
        ([], ""),
    ],
)
def test_emphasis_rejects_content_with_nothing_to_emphasize(subtests, inner, rendered) -> None:
    """Verify empty or blank content raises the empty-inner card."""

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=(inner,),
        exception_type=ParamError,
        error_name="MARKDOWN_EMPHASIS_EMPTY_INNER",
        value=rendered,
        verbose=False,
    )


def test_emphasis_rejects_a_block_as_content(subtests) -> None:
    """Verify a block node cannot be emphasized."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=(block,),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, None, 3.14, {"a": 1}])
def test_emphasis_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


def test_emphasis_checks_the_kind_before_the_content(subtests) -> None:
    """Verify a wrong kind is reported even when the content is wrong as well."""

    assert_exception_function(
        subtests,
        Emphasis,
        invalid_params=("", "em"),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'kind'",
        verbose=False,
    )
