import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Html import Html
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import HtmlMode
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text

BLOCK = HtmlMode.BLOCK
INLINE = HtmlMode.INLINE
COMMENT = HtmlMode.COMMENT


def _make(arguments: dict) -> Html:
    """Create an Html node from keyword arguments."""

    return Html(**arguments)


def test_html_is_a_markdown_node() -> None:
    """Verify the class."""

    assert isinstance(Html("div"), Markdown)


def test_html_level_depends_on_the_mode() -> None:
    """Verify an inline tag is inline, everything else is a block."""

    assert Html("div").node_level is NodeLevel.BLOCK
    assert Html("div", mode=BLOCK).node_level is NodeLevel.BLOCK
    assert Html("kbd", "C", mode=INLINE).node_level is NodeLevel.INLINE
    assert Html(mode=COMMENT, content="x").node_level is NodeLevel.BLOCK


def test_html_defaults() -> None:
    """Verify the defaults."""

    node = Html("div")

    assert node.mode is BLOCK
    assert node.content is None
    assert node.attrs == {}


# ----------------------------------------------------------------------
# Block tags
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "arguments, expected",
    [
        # No content: the opening and the closing tag
        ({"tag": "div"}, ("<div></div>",)),
        ({"tag": "my-tag"}, ("<my-tag></my-tag>",)),
        # The tag name is written in lower case
        ({"tag": "DIV"}, ("<div></div>",)),
        # A string stays on the line of the tag, and is escaped
        ({"tag": "summary", "content": "Title"}, ("<summary>Title</summary>",)),
        ({"tag": "p", "content": "a*b"}, (r"<p>a\*b</p>",)),
        ({"tag": "p", "content": ""}, ("<p></p>",)),
        # So does an inline node
        ({"tag": "summary", "content": Text("*x*", escape=False)}, ("<summary>*x*</summary>",)),
        # Attributes
        ({"tag": "a", "content": "x", "attrs": {"href": "u", "id": "i"}}, ('<a href="u" id="i">x</a>',)),
        ({"tag": "details", "attrs": {"open": True}}, ("<details open></details>",)),
        ({"tag": "div", "attrs": {"hidden": False, "id": None, "class": "x"}}, ('<div class="x"></div>',)),
        ({"tag": "a", "attrs": {"title": 'say "hi"'}}, ('<a title="say &quot;hi&quot;"></a>',)),
        # Void tags are the opening tag only
        ({"tag": "br"}, ("<br>",)),
        ({"tag": "img", "attrs": {"src": "a.png", "alt": "x"}}, ('<img src="a.png" alt="x">',)),
        ({"tag": "HR"}, ("<hr>",)),
    ],
)
def test_html_block_tag_on_one_line(arguments, expected) -> None:
    """Verify a tag with inline content, or none, is one line."""

    node = Html(**arguments)

    assert node.to_lines() == expected
    assert node.to_text() == "\n".join(expected)
    assert str(node) == "\n".join(expected)


@pytest.mark.parametrize(
    "content, body",
    [
        (Paragraph("a"), ("a",)),
        ([Paragraph("a"), Paragraph("b")], ("a", "", "b")),
        (["a"], ("a",)),                                   # a list is read as blocks
        (["a", "b"], ("a", "", "b")),
        (Document("a", "b"), ("a", "", "b")),
        ((Paragraph("a"), Paragraph("b", "c")), ("a", "", "b", "c")),
    ],
)
def test_html_block_content_gets_a_blank_line_on_each_side(content, body) -> None:
    """Verify blocks go between the tags, so the Markdown inside is read."""

    node = Html("details", content)

    assert node.to_lines() == ("<details>", "", *body, "", "</details>")


def test_html_stores_the_tag_in_lower_case_and_copies_the_attributes() -> None:
    """Verify the stored tag and that the attribute dictionary is a copy."""

    attrs = {"id": "x"}

    node = Html("DIV", attrs=attrs)

    attrs["id"] = "changed"
    attrs["extra"] = 1

    assert node.tag == "div"
    assert node.attrs == {"id": "x"}


# ----------------------------------------------------------------------
# Inline tags
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "content, expected",
    [
        ("C", "<kbd>C</kbd>"),
        (["a", "b"], "<kbd>ab</kbd>"),          # a list is one line in an inline tag
        (Text("x"), "<kbd>x</kbd>"),
        (None, "<kbd></kbd>"),
    ],
)
def test_html_inline_tag(content, expected) -> None:
    """Verify an inline tag is one line, whatever the content was given as."""

    assert Html("kbd", content, mode=INLINE).to_lines() == (expected,)


def test_html_inline_void_tag() -> None:
    """Verify a void tag is the opening tag in inline mode as well."""

    assert Html("br", mode=INLINE).to_lines() == ("<br>",)


def test_html_inline_tag_stands_inside_a_line() -> None:
    """Verify an inline tag can be added to text, like any inline node."""

    result = Text("Press ") + Html("kbd", "C", mode=INLINE)

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "Press <kbd>C</kbd>"


# ----------------------------------------------------------------------
# Comments
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "content, expected",
    [
        ("note", ("<!-- note -->",)),
        ("", ("<!-- -->",)),
        (None, ("<!-- -->",)),
        # More lines: the text between two marker lines
        ("a\nb", ("<!--", "a", "b", "-->")),
        # Nothing in a comment is escaped
        ("*x* # y", ("<!-- *x* # y -->",)),
    ],
)
def test_html_comment(content, expected) -> None:
    """Verify a comment on one line or on several."""

    assert Html(mode=COMMENT, content=content).to_lines() == expected


def test_html_comment_has_no_tag() -> None:
    """Verify the tag is None for a comment, whatever was passed."""

    assert Html(mode=COMMENT, content="x").tag is None
    assert Html("div", "x", mode=COMMENT).tag is None
    assert Html("div", "x", mode=COMMENT).to_lines() == ("<!-- x -->",)


def test_html_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Html("div"), "__dict__")


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("mode", ["block", "inline", None, 1, True])
def test_html_rejects_a_mode_of_the_wrong_type(subtests, mode) -> None:
    """Verify `mode` has to be an HtmlMode."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": "div", "mode": mode},),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'mode'",
        expected="HtmlMode",
        value=mode,
        verbose=False,
    )


@pytest.mark.parametrize("attrs", [["a"], "x", 1, True, ("a", 1)])
def test_html_rejects_attrs_that_are_not_a_dictionary(subtests, attrs) -> None:
    """Verify `attrs` has to be a dictionary (or None)."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": "div", "attrs": attrs},),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'attrs'",
        expected="dict",
        value=attrs,
        verbose=False,
    )


@pytest.mark.parametrize("tag", [None, 1, "", "1a", "a b", "<a>", "a_b", "é", ["div"]])
@pytest.mark.parametrize("mode", [BLOCK, INLINE])
def test_html_rejects_an_invalid_tag(subtests, tag, mode) -> None:
    """Verify the tag name is checked, and a missing tag is invalid for a tag."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": tag, "mode": mode},),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_INVALID_TAG",
        value=tag,
        verbose=False,
    )


def test_html_rejects_a_missing_tag(subtests) -> None:
    """Verify `Html()` without a tag is an error in block mode."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({},),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_INVALID_TAG",
        value=None,
        verbose=False,
    )


@pytest.mark.parametrize("tag", ["br", "img", "hr", "BR"])
@pytest.mark.parametrize("content", ["x", "", Text("x"), ["a"]])
def test_html_rejects_content_for_a_void_tag(subtests, tag, content) -> None:
    """Verify a void tag cannot hold content, not even an empty string."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": tag, "content": content},),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_VOID_TAG_WITH_CONTENT",
        verbose=False,
    )


@pytest.mark.parametrize("name", ["bad name", 'a"b', "a=b", "a>b", "1a", "", 1, None])
def test_html_rejects_an_invalid_attribute_name(subtests, name) -> None:
    """Verify an attribute name cannot break the tag."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": "div", "attrs": {name: "x"}},),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_INVALID_ATTRIBUTE",
        value=name,
        verbose=False,
    )


@pytest.mark.parametrize("content", [42, 3.14, True, {"a": 1}])
def test_html_rejects_content_that_is_not_content(subtests, content) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": "div", "content": content},),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=content,
        verbose=False,
    )


def test_html_rejects_a_block_in_an_inline_tag(subtests) -> None:
    """Verify an inline tag cannot hold blocks."""

    block = Paragraph("a")

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"tag": "kbd", "content": block, "mode": INLINE},),
        exception_type=ParamError,
        error_name="MARKDOWN_BLOCK_IN_INLINE",
        value=block,
        verbose=False,
    )


@pytest.mark.parametrize("content", [42, ["a"], Text("x"), True])
def test_html_rejects_a_comment_that_is_not_a_string(subtests, content) -> None:
    """Verify the content of a comment is a string."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"mode": COMMENT, "content": content},),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'content'",
        expected="str",
        value=content,
        verbose=False,
    )


@pytest.mark.parametrize("text", ["a --> b", ">x", "->x", "-->"])
def test_html_rejects_a_comment_that_would_end_early(subtests, text) -> None:
    """Verify the text cannot close the comment."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=({"mode": COMMENT, "content": text},),
        exception_type=ParamError,
        error_name="MARKDOWN_HTML_COMMENT_TERMINATOR",
        value=text,
        verbose=False,
    )
