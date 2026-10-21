import pytest

# Test se spustí pouze pokud je nainstalována knihovna markdown-it-py
markdown_it = pytest.importorskip("markdown_it")

from simplibs.markdown.blocks.CodeBlock import CodeBlock
from simplibs.markdown.blocks.Heading import Heading
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.blocks.ThematicBreak import ThematicBreak
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.containers.List import List
from simplibs.markdown.containers.ListItem import ListItem
from simplibs.markdown.containers.Quote import Quote
from simplibs.markdown.containers.Table import Table
from simplibs.markdown.inline.Emphasis import Emphasis
from simplibs.markdown.inline.InlineCode import InlineCode
from simplibs.markdown.inline.Link import Link
from simplibs.markdown.inline.Text import Text


@pytest.fixture
def parser():
    """Return a configured MarkdownIt parser instance."""
    return markdown_it.MarkdownIt("commonmark")


@pytest.mark.parametrize(
    "text",
    [
        "Simple text",
        "Text with # hash, * star, _ underscore and ` backtick",
        "C# and F# programming languages",
        "snake_case_variable_name",
        "1. First item like text",
        "> Quote like text",
        "http://example.com?a=1&b=2",
    ],
)
def test_paragraph_roundtrip_parses_as_paragraph(parser, text) -> None:
    """Verify that Paragraph generates valid Markdown parsed back as a paragraph."""
    doc = Document(Paragraph(text))
    rendered = doc.to_text()

    tokens = parser.parse(rendered)
    token_types = [t.type for t in tokens]

    assert "paragraph_open" in token_types
    assert "paragraph_close" in token_types


@pytest.mark.parametrize(
    "text, level",
    [
        ("Title C#", 1),
        ("Heading with *stars*", 2),
        ("Complex # heading", 3),
    ],
)
def test_heading_roundtrip_parses_as_heading(parser, text, level) -> None:
    """Verify that Heading generates valid Markdown parsed back with matching level."""
    node = Heading(text, level=level)
    rendered = node.to_text()

    tokens = parser.parse(rendered)
    heading_tokens = [t for t in tokens if t.type == "heading_open"]

    assert len(heading_tokens) == 1
    assert heading_tokens[0].tag == f"h{level}"


def test_code_block_roundtrip_parses_as_code_fence(parser) -> None:
    """Verify that CodeBlock with nested backticks parses correctly without ending early."""
    code = "def hello():\n    return '```python\nprint(1)\n```'"
    node = CodeBlock(code, info="python")
    rendered = node.to_text()

    tokens = parser.parse(rendered)
    fence_tokens = [t for t in tokens if t.type == "fence"]

    assert len(fence_tokens) == 1
    assert fence_tokens[0].content.strip() == code.strip()


def test_list_roundtrip_parses_as_bullet_list(parser) -> None:
    """Verify that List generates valid Markdown structure parsed as bullet list."""
    node = List(ListItem("Item 1"), ListItem("Item 2"), ListItem("Item 3"))
    rendered = node.to_text()

    tokens = parser.parse(rendered)
    list_tokens = [t for t in tokens if t.type == "bullet_list_open"]

    assert len(list_tokens) == 1


def test_table_roundtrip_parses_as_table(parser) -> None:
    """Verify that Table with special characters in cells parses cleanly."""
    table = Table(
        ["Header A", "Header B"],
        [
            ["Cell | with pipe", "Cell with _underscore_"],
            ["Normal", "Data"],
        ],
    )
    # Povolíme GFM tabulky nad výchozím commonmark parserem bez linkify
    table_parser = markdown_it.MarkdownIt("commonmark", {"linkify": False}).enable("table")
    rendered = table.to_text()

    tokens = table_parser.parse(rendered)


def test_complex_document_roundtrip_parsing(parser) -> None:
    """Verify a complete multi-node document builds clean, valid Markdown without syntax errors."""
    doc = Document(
        Heading("Documentation", level=1),
        Paragraph("Welcome to " + Emphasis("simplibs-markdown") + "."),
        Quote("A quote with " + InlineCode("code") + " inside."),
        ThematicBreak(),
        List(
            ListItem("Check " + Link("docs", "https://example.com")),
            ListItem("Report " + Link("issues", "https://example.com/issues")),
        ),
    )
    rendered = doc.to_text()

    # Zkontrolujeme, že parser projde celý dokument bez výjimek
    tokens = parser.parse(rendered)
    assert len(tokens) > 0