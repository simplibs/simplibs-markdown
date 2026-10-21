import importlib
from pathlib import Path

import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.Heading import Heading
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.containers.List import List
from simplibs.markdown.inline.Text import Text
from simplibs.markdown.output import MarkdownText

# `simplibs.markdown.output.MarkdownText` is the class, so the module has to be asked for by name
MODULE = importlib.import_module("simplibs.markdown.output.MarkdownText")


class _Counting(Markdown):
    """A block that counts how often it is rendered."""

    __slots__ = ("calls",)
    node_level = NodeLevel.BLOCK

    def __init__(self) -> None:
        self.calls = 0

    def to_lines(self) -> tuple[str, ...]:
        self.calls += 1
        return ("x",)


def _fake_write_text(monkeypatch, result="written.md") -> list:
    """Replace `write_text` in the module and return the list of its calls."""

    calls = []

    def fake(path, text, **options):
        calls.append((path, text, options))
        return result

    monkeypatch.setattr(MODULE, "write_text", fake)
    return calls


# ----------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------

def test_markdown_text_wraps_a_node_in_a_document() -> None:
    """Verify a node that is not a document is put into one."""

    node = Paragraph("a")

    result = MarkdownText(node)

    assert isinstance(result.document, Document)
    assert result.document.blocks[0] is node


def test_markdown_text_uses_a_document_as_it_is() -> None:
    """Verify a document is not wrapped again."""

    document = Document("a", "b")

    assert MarkdownText(document).document is document


@pytest.mark.parametrize(
    "node",
    [Text("a"), Paragraph("a"), Heading("a", 2), List("a")],
)
def test_markdown_text_accepts_any_kind_of_node(node) -> None:
    """Verify inline nodes, blocks and containers all work."""

    result = MarkdownText(node)

    assert isinstance(result.document, Document)
    assert result.text.endswith("\n")


@pytest.mark.parametrize(
    "node, text, lines",
    [
        (Paragraph("a"), "a\n", ("a",)),
        (Heading("Title"), "# Title\n", ("# Title",)),
        (Document("a", "b"), "a\n\nb\n", ("a", "", "b")),
        (List("a", "b"), "- a\n- b\n", ("- a", "- b")),
    ],
)
def test_markdown_text_text_and_lines(node, text, lines) -> None:
    """Verify the text ends with a newline and the lines do not."""

    result = MarkdownText(node)

    assert result.text == text
    assert result.lines == lines


def test_markdown_text_follows_the_settings_of_a_document() -> None:
    """Verify a document keeps its own `gap` and `final_newline`."""

    document = Document("a", "b", gap=2, final_newline=False)

    result = MarkdownText(document)

    assert result.text == "a\n\n\nb"
    assert result.lines == ("a", "", "", "b")


def test_markdown_text_attribute_types() -> None:
    """Verify the types of the attributes."""

    result = MarkdownText(Paragraph("a"))

    assert isinstance(result.text, str)
    assert isinstance(result.lines, tuple)


# ----------------------------------------------------------------------
# str, iteration, len
# ----------------------------------------------------------------------

def test_markdown_text_str_is_the_text() -> None:
    """Verify `str(...)` gives the whole text."""

    result = MarkdownText(Document("a", "b"))

    assert str(result) == result.text == "a\n\nb\n"


def test_markdown_text_iterates_over_the_lines() -> None:
    """Verify iteration gives the lines, in order."""

    result = MarkdownText(Document("a", "b"))

    assert list(result) == ["a", "", "b"]
    assert list(result) == list(result.lines)


def test_markdown_text_can_be_iterated_more_than_once() -> None:
    """Verify it is not a one-shot iterator."""

    result = MarkdownText(Document("a", "b"))

    assert list(result) == list(result)


def test_markdown_text_len_is_the_number_of_lines() -> None:
    """Verify `len(...)` counts lines, not characters."""

    result = MarkdownText(Document("a", "b"))

    assert len(result) == 3
    assert len(result) == len(result.lines)


def test_markdown_text_is_rendered_once() -> None:
    """Verify `str`, iteration and `len` do not render the node again."""

    node = _Counting()
    result = MarkdownText(node)
    calls = node.calls

    str(result)
    list(result)
    len(result)
    result.text
    result.lines

    assert calls > 0
    assert node.calls == calls


def test_markdown_text_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(MarkdownText(Paragraph("a")), "__dict__")


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("node", ["text", 42, 3.14, None, True, ["a"], {"a": 1}, b"bytes"])
def test_markdown_text_rejects_what_is_not_a_node(subtests, node) -> None:
    """Verify only a Markdown node is accepted (a plain string is not one)."""

    assert_exception_function(
        subtests,
        MarkdownText,
        invalid_params=(node,),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'node'",
        expected="Markdown",
        value=node,
        verbose=False,
    )


# ----------------------------------------------------------------------
# to_file: the call it makes
# ----------------------------------------------------------------------

def test_markdown_text_to_file_writes_its_text(monkeypatch) -> None:
    """Verify the finished text is handed to `write_text`, and replacing is the default."""

    calls = _fake_write_text(monkeypatch)
    result = MarkdownText(Document("a", "b"))

    result.to_file("out/notes.md")

    assert calls == [("out/notes.md", "a\n\nb\n", {"overwrite": True})]


def test_markdown_text_to_file_returns_what_write_text_returns(monkeypatch) -> None:
    """Verify the normalized path comes back as it is."""

    sentinel = object()
    _fake_write_text(monkeypatch, result=sentinel)

    assert MarkdownText(Paragraph("a")).to_file("x.md") is sentinel


def test_markdown_text_to_file_passes_overwrite_and_options_on(monkeypatch) -> None:
    """Verify `overwrite` and any extra option reach `write_text`."""

    calls = _fake_write_text(monkeypatch)

    MarkdownText(Paragraph("a")).to_file("x.md", overwrite=False, encoding="utf-8", newline="\n")

    assert calls == [("x.md", "a\n", {"overwrite": False, "encoding": "utf-8", "newline": "\n"})]


def test_markdown_text_to_file_passes_a_path_object_unchanged(monkeypatch) -> None:
    """Verify the path is not converted before `write_text` gets it."""

    calls = _fake_write_text(monkeypatch)
    path = Path("out") / "notes.md"

    MarkdownText(Paragraph("a")).to_file(path)

    assert calls[0][0] is path


def test_markdown_text_to_file_options_are_keyword_only() -> None:
    """Verify `overwrite` cannot be given by position."""

    with pytest.raises(TypeError):
        MarkdownText(Paragraph("a")).to_file("x.md", False)


# ----------------------------------------------------------------------
# to_file: a real file
# ----------------------------------------------------------------------

def test_markdown_text_to_file_writes_a_real_file(tmp_path) -> None:
    """Verify the file holds the text."""

    target = tmp_path / "notes.md"

    written = MarkdownText(Document("a", "b")).to_file(target)

    assert Path(written).exists()
    assert target.read_text(encoding="utf-8") == "a\n\nb\n"


def test_markdown_text_to_file_replaces_an_existing_file_by_default(tmp_path) -> None:
    """Verify `overwrite=True` is the default."""

    target = tmp_path / "notes.md"
    target.write_text("old", encoding="utf-8")

    MarkdownText(Paragraph("new")).to_file(target)

    assert target.read_text(encoding="utf-8") == "new\n"


def test_markdown_text_to_file_can_refuse_to_replace(tmp_path) -> None:
    """Verify `overwrite=False` fails and leaves the old file alone."""

    target = tmp_path / "notes.md"
    target.write_text("old", encoding="utf-8")

    with pytest.raises(Exception):
        MarkdownText(Paragraph("new")).to_file(target, overwrite=False)

    assert target.read_text(encoding="utf-8") == "old"
