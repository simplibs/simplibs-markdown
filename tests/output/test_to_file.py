import importlib
from pathlib import Path

import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.blocks.Heading import Heading
from simplibs.markdown.blocks.Paragraph import Paragraph
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.Text import Text
from simplibs.markdown.output import MarkdownText, to_file

# `simplibs.markdown.output.to_file` is the function and `...MarkdownText` is the class,
# so both modules have to be asked for by name
FILE_MODULE = importlib.import_module("simplibs.markdown.output.to_file")
TEXT_MODULE = importlib.import_module("simplibs.markdown.output.MarkdownText")


def _fake_write_text(monkeypatch, result="written.md") -> list:
    """Replace `write_text` in both modules that call it and return the list of calls."""

    calls = []

    def fake(path, text, **options):
        calls.append((path, text, options))
        return result

    monkeypatch.setattr(FILE_MODULE, "write_text", fake)
    monkeypatch.setattr(TEXT_MODULE, "write_text", fake)
    return calls


# ----------------------------------------------------------------------
# What is written
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "text",
    ["# raw", "# raw\n", "", "no newline added", "*not* escaped # at all"],
)
def test_to_file_a_string_is_written_as_it_is(monkeypatch, text) -> None:
    """Verify a string already is Markdown: not rendered, escaped or given a newline."""

    calls = _fake_write_text(monkeypatch)

    to_file(text, "x.md")

    assert calls == [("x.md", text, {"overwrite": True})]


@pytest.mark.parametrize(
    "node, text",
    [
        (Paragraph("a"), "a\n"),
        (Heading("Title"), "# Title\n"),
        (Text("a*b"), "a\\*b\n"),
        (Document("a", "b"), "a\n\nb\n"),
    ],
)
def test_to_file_a_node_is_rendered_first(monkeypatch, node, text) -> None:
    """Verify a node is written as a finished document, ending with a newline."""

    calls = _fake_write_text(monkeypatch)

    to_file(node, "x.md")

    assert calls == [("x.md", text, {"overwrite": True})]


def test_to_file_a_document_keeps_its_settings(monkeypatch) -> None:
    """Verify `gap` and `final_newline` of a document are respected."""

    calls = _fake_write_text(monkeypatch)

    to_file(Document("a", "b", gap=0, final_newline=False), "x.md")

    assert calls[0][1] == "a\nb"


def test_to_file_a_markdown_text_is_written_as_finished(monkeypatch) -> None:
    """Verify a finished text is not rendered again."""

    calls = _fake_write_text(monkeypatch)
    finished = MarkdownText(Document("a", "b"))

    to_file(finished, "x.md")

    assert calls == [("x.md", finished.text, {"overwrite": True})]


# ----------------------------------------------------------------------
# What comes back and what is passed on
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "source",
    ["text", Paragraph("a"), MarkdownText(Paragraph("a"))],
)
def test_to_file_returns_what_write_text_returns(monkeypatch, source) -> None:
    """Verify the normalized path comes back as it is, whatever the source was."""

    sentinel = object()
    _fake_write_text(monkeypatch, result=sentinel)

    assert to_file(source, "x.md") is sentinel


@pytest.mark.parametrize(
    "source",
    ["text", Paragraph("a"), MarkdownText(Paragraph("a"))],
)
def test_to_file_passes_overwrite_and_options_on(monkeypatch, source) -> None:
    """Verify `overwrite` and any extra option reach `write_text` for every kind of source."""

    calls = _fake_write_text(monkeypatch)

    to_file(source, "x.md", overwrite=False, encoding="utf-8", newline="\n")

    assert calls[0][2] == {"overwrite": False, "encoding": "utf-8", "newline": "\n"}


@pytest.mark.parametrize(
    "source",
    ["text", Paragraph("a"), MarkdownText(Paragraph("a"))],
)
def test_to_file_passes_a_path_object_unchanged(monkeypatch, source) -> None:
    """Verify the path is not converted before `write_text` gets it."""

    calls = _fake_write_text(monkeypatch)
    path = Path("out") / "notes.md"

    to_file(source, path)

    assert calls[0][0] is path


def test_to_file_options_are_keyword_only() -> None:
    """Verify `overwrite` cannot be given by position."""

    with pytest.raises(TypeError):
        to_file("text", "x.md", False)


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

@pytest.mark.parametrize("source", [42, 3.14, None, True, ["a"], {"a": 1}, b"bytes"])
def test_to_file_rejects_a_source_that_is_not_text_or_a_node(subtests, source) -> None:
    """Verify the card of `MarkdownText` is raised (a string is the only plain value allowed)."""

    assert_exception_function(
        subtests,
        to_file,
        invalid_params=(source, "x.md"),
        exception_type=ParamError,
        error_name="MARKDOWN_PARAM_INVALID_TYPE",
        label="parameter 'node'",
        expected="Markdown",
        value=source,
        verbose=False,
    )


def test_to_file_writes_nothing_for_a_wrong_source(monkeypatch) -> None:
    """Verify the check comes before any writing."""

    calls = _fake_write_text(monkeypatch)

    with pytest.raises(ParamError):
        to_file(42, "x.md")

    assert calls == []


# ----------------------------------------------------------------------
# A real file
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "source, expected",
    [
        ("raw # text", "raw # text"),
        (Paragraph("a"), "a\n"),
        (Document("a", "b"), "a\n\nb\n"),
        (MarkdownText(Heading("Title")), "# Title\n"),
    ],
)
def test_to_file_writes_a_real_file(tmp_path, source, expected) -> None:
    """Verify the file holds the text, for every kind of source."""

    target = tmp_path / "notes.md"

    written = to_file(source, target)

    assert Path(written).exists()
    assert target.read_text(encoding="utf-8") == expected


@pytest.mark.parametrize("source", ["new", Paragraph("new"), MarkdownText(Paragraph("new"))])
def test_to_file_replaces_an_existing_file_by_default(tmp_path, source) -> None:
    """Verify `overwrite=True` is the default."""

    target = tmp_path / "notes.md"
    target.write_text("old", encoding="utf-8")

    to_file(source, target)

    assert target.read_text(encoding="utf-8").startswith("new")


@pytest.mark.parametrize("source", ["new", Paragraph("new"), MarkdownText(Paragraph("new"))])
def test_to_file_can_refuse_to_replace(tmp_path, source) -> None:
    """Verify `overwrite=False` fails and leaves the old file alone."""

    target = tmp_path / "notes.md"
    target.write_text("old", encoding="utf-8")

    with pytest.raises(Exception):
        to_file(source, target, overwrite=False)

    assert target.read_text(encoding="utf-8") == "old"
