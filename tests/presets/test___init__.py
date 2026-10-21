import importlib
import inspect

import pytest
from simplibs.markdown import presets
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.inline.InlineJoin import InlineJoin

FAMILIES = {
    "alerts": {"CAUTION", "IMPORTANT", "NOTE", "TIP", "WARNING"},
    "code": {"GEOJSON", "MATH_BLOCK", "MERMAID", "STL", "TOPOJSON"},
    "emphasis": {"BOLD", "BOLD_ITALIC", "ITALIC", "STRIKETHROUGH"},
    "headings": {"H1", "H2", "H3", "H4", "H5", "H6"},
    "html": {"ANCHOR", "COMMENT", "DETAILS", "KBD", "MARK", "SUB", "SUP"},
    "links": {"AUTOLINK", "BARE_URL", "IMAGE"},
    "lists": {"BULLET_LIST", "DONE_ITEM", "NUMBERED_LIST", "TASK_ITEM"},
    "references": {"COLOR_CHIP", "COMMIT_REF", "EMOJI", "ISSUE_REF", "MENTION"},
    "spacing": {"EMPTY_LINE", "HARD_BREAK", "RULE"},
}
ALL_NAMES = set().union(*FAMILIES.values())

# Presets that are ready instances, used without parentheses
INSTANCES = {"HARD_BREAK", "RULE"}

# One valid call for every preset that is a function
MINIMAL_CALLS = {
    "CAUTION": ("a",), "IMPORTANT": ("a",), "NOTE": ("a",), "TIP": ("a",), "WARNING": ("a",),
    "GEOJSON": ("{}",), "MATH_BLOCK": ("x",), "MERMAID": ("graph TD; A-->B",), "STL": ("solid a",), "TOPOJSON": ("{}",),
    "BOLD": ("a",), "BOLD_ITALIC": ("a",), "ITALIC": ("a",), "STRIKETHROUGH": ("a",),
    "H1": ("a",), "H2": ("a",), "H3": ("a",), "H4": ("a",), "H5": ("a",), "H6": ("a",),
    "ANCHOR": ("top",), "COMMENT": ("a",), "DETAILS": ("s", "b"), "KBD": ("a",), "MARK": ("a",), "SUB": ("a",), "SUP": ("a",),
    "AUTOLINK": ("https://example.com",), "BARE_URL": ("https://example.com",), "IMAGE": ("alt", "a.png"),
    "BULLET_LIST": ("a",), "DONE_ITEM": ("a",), "NUMBERED_LIST": ("a",), "TASK_ITEM": ("a",),
    "COLOR_CHIP": ("#fff",), "COMMIT_REF": ("a1b2c3d",), "EMOJI": ("tada",), "ISSUE_REF": (1,), "MENTION": ("octocat",),
    "EMPTY_LINE": (),
}

# What each preset is: an inline node (stays on one line) or a block (stands on its own)
INLINE_NAMES = {
    "BOLD", "BOLD_ITALIC", "ITALIC", "STRIKETHROUGH",
    "ANCHOR", "KBD", "MARK", "SUB", "SUP",
    "AUTOLINK", "BARE_URL", "IMAGE",
    "COLOR_CHIP", "COMMIT_REF", "EMOJI", "ISSUE_REF", "MENTION",
    "HARD_BREAK",
}
BLOCK_NAMES = ALL_NAMES - INLINE_NAMES


def _build(name: str):
    """The preset itself if it is an instance, otherwise one valid call of it."""

    preset = getattr(presets, name)
    return preset if name in INSTANCES else preset(*MINIMAL_CALLS[name])


# ----------------------------------------------------------------------
# The list of presets
# ----------------------------------------------------------------------

def test_presets_all_is_the_complete_list() -> None:
    """Verify `__all__` holds exactly the presets of the families (a new preset must be added here)."""

    assert set(presets.__all__) == ALL_NAMES


def test_presets_all_has_no_duplicates() -> None:
    """Verify every name stands once."""

    assert len(presets.__all__) == len(set(presets.__all__))


@pytest.mark.parametrize("name", sorted(ALL_NAMES))
def test_presets_every_name_can_be_imported_from_the_package(name) -> None:
    """Verify the names in `__all__` exist."""

    assert hasattr(presets, name)


@pytest.mark.parametrize("family, names", sorted(FAMILIES.items()))
def test_presets_a_family_exports_its_presets(family, names) -> None:
    """Verify each sub-package holds its presets and nothing else public."""

    module = importlib.import_module(f"simplibs.markdown.presets.{family}")
    public = {name for name in dir(module) if not name.startswith("_")}

    assert public == names


@pytest.mark.parametrize("name", sorted(ALL_NAMES))
def test_presets_names_are_in_capitals(name) -> None:
    """Verify the naming convention: a preset is written like a constant."""

    assert name.isupper()


# ----------------------------------------------------------------------
# What a preset is
# ----------------------------------------------------------------------

@pytest.mark.parametrize("name", sorted(ALL_NAMES - INSTANCES))
def test_presets_a_function_is_documented_and_annotated(name) -> None:
    """Verify the convention: a summary line and the sections `Init Params`, `Markdown`, `Example`."""

    function = getattr(presets, name)
    doc = inspect.getdoc(function)

    assert callable(function)
    assert doc, f"{name} has no docstring"
    assert doc.splitlines()[0].endswith(".")
    for section in ("Init Params:", "Markdown:", "Example:"):
        assert section in doc, f"{name} has no '{section}' section"
    assert inspect.signature(function).return_annotation is not inspect.Signature.empty


@pytest.mark.parametrize("name", sorted(ALL_NAMES - INSTANCES))
def test_presets_a_function_lives_in_a_module_of_its_own_name(name) -> None:
    """Verify the file is named after the preset."""

    function = getattr(presets, name)

    assert function.__name__ == name
    assert function.__module__.rsplit(".", 1)[-1] == name


@pytest.mark.parametrize("name", sorted(INSTANCES))
def test_presets_an_instance_is_a_node_and_not_callable(name) -> None:
    """Verify the ready instances are nodes used without parentheses."""

    preset = getattr(presets, name)

    assert isinstance(preset, Markdown)
    assert not callable(preset)


def test_presets_minimal_calls_cover_every_function() -> None:
    """Verify this file knows how to call every preset (a new preset needs an entry)."""

    assert set(MINIMAL_CALLS) == ALL_NAMES - INSTANCES


@pytest.mark.parametrize("name", sorted(ALL_NAMES))
def test_presets_every_preset_gives_a_markdown_node(name) -> None:
    """Verify a valid call returns a node that writes some text."""

    node = _build(name)

    assert isinstance(node, Markdown)
    assert isinstance(node.to_text(), str)


# ----------------------------------------------------------------------
# Inline or block: what `+` makes of it
# ----------------------------------------------------------------------

@pytest.mark.parametrize("name", sorted(INLINE_NAMES))
def test_presets_inline_presets_stay_on_the_line(name) -> None:
    """Verify an inline preset next to a string gives one line of inline content."""

    node = _build(name)

    assert node.node_level is NodeLevel.INLINE
    assert isinstance("text " + node, InlineJoin)
    assert isinstance(node + " text", InlineJoin)


@pytest.mark.parametrize("name", sorted(BLOCK_NAMES))
def test_presets_block_presets_make_a_document(name) -> None:
    """Verify a block preset next to a string gives a document."""

    node = _build(name)

    assert node.node_level is NodeLevel.BLOCK
    assert isinstance("text" + node, Document)
    assert isinstance(node + "text", Document)
