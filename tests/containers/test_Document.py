import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.Frontmatter import Frontmatter
from simplibs.markdown.blocks.LinkDefinition import LinkDefinition
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.Text import Text


def _make(blocks, options: dict) -> Document:
    """Create a Document from blocks and keyword options."""

    return Document(*blocks, **options)


def test_document_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = Document("a")

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_document_defaults() -> None:
    """Verify one blank line between blocks and a final newline."""

    node = Document("a")

    assert node.gap == 1
    assert node.final_newline is True


def test_document_stores_a_flat_tuple_of_blocks() -> None:
    """Verify strings become paragraphs and nodes are kept as they are."""

    paragraph = Paragraph("b")

    node = Document("a", paragraph)

    assert isinstance(node.blocks, tuple)
    assert isinstance(node.blocks[0], Paragraph)
    assert node.blocks[1] is paragraph


@pytest.mark.parametrize(
    "gap, expected",
    [
        (0, ("a", "b", "c")),
        (1, ("a", "", "b", "", "c")),
        (2, ("a", "", "", "b", "", "", "c")),
    ],
)
def test_document_gap(gap, expected) -> None:
    """Verify `gap` blank lines between every two blocks."""

    assert Document("a", "b", "c", gap=gap).to_lines() == expected


def test_document_one_block_has_no_separator() -> None:
    """Verify nothing is added around a single block."""

    assert Document("a").to_lines() == ("a",)


@pytest.mark.parametrize(
    "final_newline, expected",
    [
        (True, "a\n\nb\n"),
        (False, "a\n\nb"),
    ],
)
def test_document_to_text_final_newline(final_newline, expected) -> None:
    """Verify the text ends with a newline unless told otherwise."""

    node = Document("a", "b", final_newline=final_newline)

    assert node.to_text() == expected
    assert str(node) == expected


def test_document_lines_have_no_trailing_empty_line() -> None:
    """Verify `to_lines` does not carry the final newline, so a container can nest the document."""

    assert Document("a", "b").to_lines()[-1] == "b"
    assert Document("a", "b", final_newline=False).to_lines()[-1] == "b"


def test_document_repr_shows_the_text_with_its_newline() -> None:
    """Verify the representation."""

    assert repr(Document("a")) == "Document('a\\n')"


@pytest.mark.parametrize(
    "items",
    [
        (Document("a", "b"), "c"),
        ("a", Document("b", "c")),
        (["a", Document("b")], "c"),
    ],
)
def test_document_a_document_given_as_content_is_unpacked(items) -> None:
    """Verify documents never nest: the blocks of an inner document are the outer one's."""

    node = Document(*items)

    assert len(node.blocks) == 3
    assert all(isinstance(block, Paragraph) for block in node.blocks)
    assert node.to_lines() == ("a", "", "b", "", "c")


def test_document_an_inner_document_gives_up_its_own_gap_and_newline() -> None:
    """Verify only the outermost document decides how the text is spaced."""

    inner = Document("a", "b", gap=3, final_newline=False)

    node = Document(inner, "c")

    assert node.to_lines() == ("a", "", "b", "", "c")
    assert node.to_text().endswith("\n")


def test_document_inline_node_becomes_a_paragraph() -> None:
    """Verify an inline node is wrapped like a string."""

    node = Document(Text("a"), "b")

    assert [type(block) for block in node.blocks] == [Paragraph, Paragraph]


def test_document_none_and_empty_collections_add_nothing() -> None:
    """Verify they are skipped."""

    assert Document(None, "a", [], ((),)).to_lines() == ("a",)


def test_document_a_blank_line_node_replaces_the_automatic_gap() -> None:
    """Verify an explicit BlankLine is the separator, not a second one."""

    assert Document("a", BlankLine(2), "b").to_lines() == ("a", "", "", "b")


def test_document_link_definitions_stack() -> None:
    """Verify definitions follow each other without blank lines."""

    node = Document("text", LinkDefinition("a", "x"), LinkDefinition("b", "y"))

    assert node.to_lines() == ("text", "", "[a]: x", "[b]: y")


def test_document_with_front_matter_first() -> None:
    """Verify the usual layout of a Markdown file."""

    node = Document(Frontmatter({"title": "X"}), "text")

    assert node.to_text() == '---\ntitle: "X"\n---\n\ntext\n'


def test_document_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(Document("a"), "__dict__")


@pytest.mark.parametrize("gap", [-1, -10, "1", 1.5, None, True, False, [1]])
def test_document_rejects_a_gap_that_is_not_a_non_negative_integer(subtests, gap) -> None:
    """Verify `gap` is an integer of zero or more (a bool is not)."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(("a",), {"gap": gap}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'gap'",
        expected="non-negative int",
        value=gap,
        verbose=False,
    )


@pytest.mark.parametrize("blocks", [(), (None,), ([],), ((), [None]), (None, None)])
def test_document_rejects_no_content(subtests, blocks) -> None:
    """Verify a document needs at least one block."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=(blocks, {}),
        exception_type=ParamError,
        error_name="MARKDOWN_NO_BLOCKS",
        verbose=False,
    )


@pytest.mark.parametrize("value", [42, 3.14, True, {"a": 1}])
def test_document_rejects_content_that_is_not_content(subtests, value) -> None:
    """Verify a value that is no content raises the not-markdown card."""

    assert_exception_function(
        subtests,
        Document,
        invalid_params=("a", value),
        exception_type=ParamError,
        error_name="MARKDOWN_NODE_NOT_MARKDOWN",
        value=value,
        verbose=False,
    )


def test_document_checks_the_gap_before_the_content(subtests) -> None:
    """Verify a wrong gap is reported even when there is no content."""

    assert_exception_function(
        subtests,
        _make,
        invalid_params=((), {"gap": -1}),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'gap'",
        verbose=False,
    )
