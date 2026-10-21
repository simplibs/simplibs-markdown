import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Footnote import Footnote
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.enums import FootnoteRole
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.Text import Text

DEFINITION = FootnoteRole.DEFINITION
REFERENCE = FootnoteRole.REFERENCE


def _make(label, blocks, options: dict) -> Footnote:
    """Create a Footnote from a label, blocks and keyword options."""

    return Footnote(label, *blocks, **options)


def test_footnote_is_a_markdown_node() -> None:
    """Verify the class."""

    assert isinstance(Footnote("1", "a"), Markdown)


def test_footnote_defaults() -> None:
    """Verify the default role is the definition."""

    node = Footnote("1", "a")

    assert node.role is DEFINITION
    assert node.label == "1"


def test_footnote_level_depends_on_the_role() -> None:
    """Verify a definition is a block and a reference is inline."""

    assert Footnote("1", "a").node_level is NodeLevel.BLOCK
    assert Footnote("1", "a", role=DEFINITION).node_level is NodeLevel.BLOCK
    assert Footnote("1", role=REFERENCE).node_level is NodeLevel.INLINE


# ----------------------------------------------------------------------
# Definition
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "blocks, expected",
    [
        (("a",), ("[^1]: a",)),
        # Several blocks: separated by a blank line, indented under the label
        (("a", "b"), ("[^1]: a", "", "    b")),
        (("a", "b", "c"), ("[^1]: a", "", "    b", "", "    c")),
        # A block with several lines
        ((Paragraph("a", "b"),), ("[^1]: a", "    b")),
        # A code block inside the note
        ((CodeBlock("x"),), ("[^1]: ```", "    x", "    ```")),
        # A document is unpacked
        ((Document("a", "b"),), ("[^1]: a", "", "    b")),
        # A nested list of blocks
        ((["a", ["b"]],), ("[^1]: a", "", "    b")),
        # `None` is skipped
        ((None, "a"), ("[^1]: a",)),
    ],
)
def test_footnote_definition(blocks, expected) -> None:
    """Verify the lines of a note."""

    node = Footnote("1", *blocks)

    assert node.to_lines() == expected
    assert node.to_text() == "\n".join(expected)


def test_footnote_definition_stores_blocks_as_a_tuple() -> None:
    """Verify the content is flattened into a tuple of block nodes."""

    node = Footnote("1", "a", Paragraph("b"))

    assert isinstance(node.blocks, tuple)
    assert [type(block) for block in node.blocks] == [Paragraph, Paragraph]


def test_footnote_label_is_written_as_given() -> None:
    """Verify the label is not changed."""

    assert Footnote("note-2", "a").to_lines() == ("[^note-2]: a",)


# ----------------------------------------------------------------------
# Reference
# ----------------------------------------------------------------------

def test_footnote_reference() -> None:
    """Verify the marker is only the label."""

    node = Footnote("1", role=REFERENCE)

    assert node.to_lines() == ("[^1]",)
    assert node.to_text() == "[^1]"
    assert str(node) == "[^1]"
    assert node.blocks == ()


def test_footnote_reference_stands_inside_a_line() -> None:
    """Verify a reference can be added to text, like any inline node."""

    result = Text("a") + Footnote("1", role=REFERENCE)

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "a[^1]"


def test_footnote_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Footnote("1", "a"), "__dict__")


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("label", ["", "a b", "a\tb", " a", "a\n", 1, None, ["a"]])
def test_footnote_rejects_a_label_that_is_not_usable(subtests, label) -> None:
    """Verify the label is a non-empty string without whitespace."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(label, ("a",), {}),
        exception_type=ParamError,
        error_name="MARKDOWN_FOOTNOTE_LABEL_INVALID",
        value=label,
        verbose=False,
    )


@pytest.mark.parametrize("role", ["definition", "reference", None, 1, True])
def test_footnote_rejects_a_role_of_the_wrong_type(subtests, role) -> None:
    """Verify `role` has to be a FootnoteRole."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=("1", ("a",), {"role": role}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'role'",
        expected="FootnoteRole",
        value=role,
        verbose=False,
    )


@pytest.mark.parametrize("blocks", [("a",), ("a", "b"), (None,), ([],), ("",)])
def test_footnote_rejects_blocks_for_a_reference(subtests, blocks) -> None:
    """Verify a reference is only the marker (even an empty argument counts)."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=("1", blocks, {"role": REFERENCE}),
        exception_type=ParamError,
        error_name="MARKDOWN_FOOTNOTE_REFERENCE_WITH_BLOCKS",
        value="1",
        verbose=False,
    )


@pytest.mark.parametrize("blocks", [(), (None,), ([],), ((), [None])])
def test_footnote_rejects_a_definition_without_blocks(subtests, blocks) -> None:
    """Verify a note needs content."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=("1", blocks, {}),
        exception_type=ParamError,
        error_name="MARKDOWN_NO_BLOCKS",
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_footnote_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=("1", ("a", value), {}),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )
