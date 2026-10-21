import re

import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import InlineMarkdown
from simplibs.markdown.blocks.LinkDefinition import LinkDefinition
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.Link import Link
from simplibs.markdown.inline.Text import Text
from simplibs.markdown.inline.enums import LinkKind

INLINE = LinkKind.INLINE
REFERENCE = LinkKind.REFERENCE
COLLAPSED = LinkKind.COLLAPSED
SHORTCUT = LinkKind.SHORTCUT
AUTOLINK = LinkKind.AUTOLINK
BARE = LinkKind.BARE


def _make(arguments: dict) -> Link:
    """Create a Link from keyword arguments."""

    return Link(**arguments)


def _fail(subtests, arguments: dict, error_name: str, **fields) -> None:
    """Check that creating the link with these arguments raises a ParamError card."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(arguments,),
        exception_type=ParamError,
        error_name=error_name,
        verbose=False,
        **fields,
    )


def test_link_is_an_inline_node() -> None:
    """Verify the class."""

    assert isinstance(Link("t", "u"), InlineMarkdown)


def test_link_defaults() -> None:
    """Verify the defaults and the stored text node."""

    node = Link("text", "https://x.com")

    assert node.kind is INLINE
    assert node.image is False
    assert node.title is None
    assert node.label is None
    assert node.dest == "https://x.com"
    assert isinstance(node.text, Text)


def test_link_stores_none_for_the_text_of_an_autolink() -> None:
    """Verify there is no text node when there is no text."""

    assert Link(dest="https://x.com", kind=AUTOLINK).text is None


# ----------------------------------------------------------------------
# INLINE
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "arguments, expected",
    [
        ({"text": "text", "dest": "https://x.com"}, "[text](https://x.com)"),
        ({"text": "text", "dest": "u", "title": "Title"}, '[text](u "Title")'),
        ({"text": "alt", "dest": "u", "image": True}, "![alt](u)"),
        ({"text": "alt", "dest": "u", "title": "T", "image": True}, '![alt](u "T")'),
        # An empty alt text is allowed
        ({"text": "", "dest": "u", "image": True}, "![](u)"),
        ({"text": "", "dest": "u"}, "[](u)"),
        # An empty title is no title
        ({"text": "t", "dest": "u", "title": ""}, "[t](u)"),
        # A destination with a space goes into angle brackets
        ({"text": "t", "dest": "my file.pdf"}, "[t](<my file.pdf>)"),
        # A title with a double quote moves to single quotes
        ({"text": "t", "dest": "u", "title": 'say "hi"'}, "[t](u 'say \"hi\"')"),
        # The text is content: escaped
        ({"text": "a*b", "dest": "u"}, r"[a\*b](u)"),
        ({"text": "a]b", "dest": "u"}, r"[a\]b](u)"),
    ],
)
def test_link_inline(arguments, expected) -> None:
    """Verify the inline form, with an image, a title and the escaping."""

    node = Link(**arguments)

    assert node.to_inline() == expected
    assert node.to_text() == expected
    assert str(node) == expected
    assert node.to_lines() == (expected,)


@pytest.mark.parametrize(
    "text, expected",
    [
        (Text("x", escape=False), "[x](u)"),
        (Text("*x*", escape=False), "[*x*](u)"),
        (Emphasis("x"), "[*x*](u)"),
        (["a", Emphasis("b")], "[a*b*](u)"),
    ],
)
def test_link_text_may_be_a_node_or_a_list(text, expected) -> None:
    """Verify the text is inline content."""

    assert Link(text, "u").to_inline() == expected


def test_link_text_node_is_kept() -> None:
    """Verify an inline node given as text is not copied."""

    text = Emphasis("x")

    assert Link(text, "u").text is text


# ----------------------------------------------------------------------
# REFERENCE, COLLAPSED, SHORTCUT
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "arguments, expected",
    [
        ({"text": "text", "kind": REFERENCE, "label": "ref"}, "[text][ref]"),
        ({"text": "alt", "kind": REFERENCE, "label": "ref", "image": True}, "![alt][ref]"),
        # The label is normalized the way a definition's label is
        ({"text": "t", "kind": REFERENCE, "label": "  Foo   Bar "}, "[t][Foo Bar]"),
        # The destination is ignored: it lives in the definition
        ({"text": "t", "dest": "u", "kind": REFERENCE, "label": "r"}, "[t][r]"),
        ({"text": "text", "kind": COLLAPSED}, "[text][]"),
        ({"text": "alt", "kind": COLLAPSED, "image": True}, "![alt][]"),
        ({"text": "text", "kind": SHORTCUT}, "[text]"),
        ({"text": "alt", "kind": SHORTCUT, "image": True}, "![alt]"),
        # A label or a destination given to a kind that ignores them changes nothing
        ({"text": "t", "kind": COLLAPSED, "label": "x", "dest": "u"}, "[t][]"),
        ({"text": "t", "kind": SHORTCUT, "label": "x", "dest": "u"}, "[t]"),
    ],
)
def test_link_reference_forms(arguments, expected) -> None:
    """Verify the three forms that point to a definition."""

    assert Link(**arguments).to_inline() == expected


# ----------------------------------------------------------------------
# AUTOLINK, BARE
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "kind, expected",
    [
        (AUTOLINK, "<https://x.com>"),
        (BARE, "https://x.com"),
    ],
)
def test_link_autolink_and_bare_url(kind, expected) -> None:
    """Verify these two kinds are the destination and nothing else."""

    node = Link(dest="https://x.com", kind=kind)

    assert node.to_inline() == expected
    assert node.to_text() == expected


def test_link_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Link("t", "u"), "__dict__")


# ----------------------------------------------------------------------
# Errors: types
# ----------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["inline", None, 1, True])
def test_link_rejects_a_kind_of_the_wrong_type(subtests, kind) -> None:
    """Verify `kind` has to be a LinkKind."""

    _fail(
        subtests, {"text": "t", "dest": "u", "kind": kind},
        "MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'kind'", expected="LinkKind", value=kind,
    )


@pytest.mark.parametrize("name", ["dest", "title", "label"])
@pytest.mark.parametrize("value", [42, 3.14, True, ["x"], b"x"])
def test_link_rejects_a_text_parameter_of_the_wrong_type(subtests, name, value) -> None:
    """Verify `dest`, `title` and `label` have to be strings (or None)."""

    arguments = {"text": "t", "dest": "u", "kind": INLINE, name: value}

    _fail(
        subtests, arguments,
        "MARKDOWN_PARAM_INVALID_TYPE",
        label=f"parameter '{name}'", expected="str", value=value,
    )


def test_link_rejects_a_block_as_text(subtests) -> None:
    """Verify a block node cannot be the text of a link."""

    block = Paragraph("a")

    _fail(
        subtests, {"text": block, "dest": "u"},
        "MARKDOWN_BLOCK_IN_INLINE",
        value=block,
    )


@pytest.mark.parametrize("value", [42, 3.14, {"a": 1}])
def test_link_rejects_a_text_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    _fail(
        subtests, {"text": value, "dest": "u"},
        "MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
    )


# ----------------------------------------------------------------------
# Errors: what each kind needs
# ----------------------------------------------------------------------

@pytest.mark.parametrize("kind", [INLINE, REFERENCE, COLLAPSED, SHORTCUT])
def test_link_rejects_a_missing_text(subtests, kind) -> None:
    """Verify every kind except the autolinks needs a text."""

    _fail(
        subtests, {"dest": "u", "label": "r", "kind": kind},
        "MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'text'", expected="str | Markdown", value=None,
    )


@pytest.mark.parametrize("dest", [None, ""])
def test_link_inline_rejects_an_empty_destination(subtests, dest) -> None:
    """Verify an inline link needs a destination."""

    _fail(
        subtests, {"text": "t", "dest": dest},
        "MARKDOWN_LINK_EMPTY_DESTINATION",
        value=dest,
    )


@pytest.mark.parametrize("label", [None, ""])
def test_link_reference_rejects_a_missing_label(subtests, label) -> None:
    """Verify a reference link needs a label."""

    _fail(
        subtests, {"text": "t", "kind": REFERENCE, "label": label},
        "MARKDOWN_LINK_KIND_REQUIRES_LABEL",
    )


@pytest.mark.parametrize("kind", [AUTOLINK, BARE])
def test_link_autolink_rejects_a_text(subtests, kind) -> None:
    """Verify an autolink and a bare URL cannot carry a text."""

    _fail(
        subtests, {"text": "t", "dest": "u", "kind": kind},
        "MARKDOWN_LINK_AUTOLINK_WITH_TEXT",
    )


@pytest.mark.parametrize("kind", [AUTOLINK, BARE])
def test_link_autolink_rejects_an_image(subtests, kind) -> None:
    """Verify an autolink and a bare URL cannot be an image."""

    _fail(
        subtests, {"dest": "u", "kind": kind, "image": True},
        "MARKDOWN_LINK_IMAGE_UNSUPPORTED_KIND",
        value=True,
    )


@pytest.mark.parametrize("kind", [AUTOLINK, BARE])
@pytest.mark.parametrize("dest", [None, ""])
def test_link_autolink_rejects_an_empty_destination(subtests, kind, dest) -> None:
    """Verify an autolink and a bare URL need a destination."""

    _fail(
        subtests, {"dest": dest, "kind": kind},
        "MARKDOWN_LINK_EMPTY_DESTINATION",
        value=dest,
    )


# ----------------------------------------------------------------------
# The label of a reference link and the label of its definition
# ----------------------------------------------------------------------

_LABEL_IN_LINK = re.compile(r"^\[t\]\[((?:\\.|[^\]\\])*)\]$")
_LABEL_IN_DEFINITION = re.compile(r"^\[((?:\\.|[^\]\\])*)\]: ")
_ESCAPABLE = re.compile(r"\\([!-/:-@\[-`{-~])")

LABELS = [
    "ref",
    "Foo  Bar",
    "x]y",
    "x[y",
    "[x]",
    "a]",
    "a[",
    "]",
    "[",
    "x ] y",
    r"a\b",
    r"a\]b",
    "a\\",
    r"\\",
]


@pytest.mark.parametrize("label", LABELS)
def test_link_reference_label_is_written_like_the_label_of_its_definition(label) -> None:
    """Verify both nodes write the same label, so the reference finds its definition."""

    link = Link("t", kind=REFERENCE, label=label).to_text()
    definition = LinkDefinition(label, "u").to_text()

    in_link = _LABEL_IN_LINK.match(link)
    in_definition = _LABEL_IN_DEFINITION.match(definition)

    assert in_link is not None, link
    assert in_definition is not None, definition
    assert in_link.group(1) == in_definition.group(1)


@pytest.mark.parametrize("label", LABELS)
def test_link_reference_label_reads_back_as_the_normalized_label(label) -> None:
    """Verify a parser reads the label as the one that was given, with its whitespace collapsed."""

    link = Link("t", kind=REFERENCE, label=label).to_text()
    in_link = _LABEL_IN_LINK.match(link)

    assert in_link is not None, link
    assert _ESCAPABLE.sub(r"\1", in_link.group(1)) == " ".join(label.split())
