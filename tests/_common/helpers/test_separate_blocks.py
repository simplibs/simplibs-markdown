import pytest
from simplibs.markdown._common.helpers import separate_blocks
from simplibs.markdown.blocks.BlankLine import BlankLine
from simplibs.markdown.blocks.LinkDefinition import LinkDefinition
from simplibs.markdown.blocks.Paragraph import Paragraph


def test_separate_blocks_without_blocks_gives_nothing() -> None:
    """Verify an empty input gives an empty tuple."""

    assert separate_blocks(()) == ()


def test_separate_blocks_one_block_has_no_separator() -> None:
    """Verify a single block is written as it is."""

    assert separate_blocks((Paragraph("a"),)) == ("a",)


def test_separate_blocks_returns_a_tuple() -> None:
    """Verify the result is a tuple."""

    assert isinstance(separate_blocks([Paragraph("a"), Paragraph("b")]), tuple)


@pytest.mark.parametrize(
    "gap, expected",
    [
        (0, ("a", "b", "c")),
        (1, ("a", "", "b", "", "c")),
        (2, ("a", "", "", "b", "", "", "c")),
    ],
)
def test_separate_blocks_gap(gap, expected) -> None:
    """Verify `gap` blank lines go between every two blocks."""

    blocks = (Paragraph("a"), Paragraph("b"), Paragraph("c"))

    assert separate_blocks(blocks, gap) == expected


def test_separate_blocks_default_gap_is_one() -> None:
    """Verify one blank line is the default."""

    assert separate_blocks((Paragraph("a"), Paragraph("b"))) == ("a", "", "b")


def test_separate_blocks_keeps_all_lines_of_a_multiline_block() -> None:
    """Verify a block with several lines is written whole."""

    blocks = (Paragraph("a", "b"), Paragraph("c"))

    assert separate_blocks(blocks) == ("a", "b", "", "c")


@pytest.mark.parametrize(
    "blocks, expected",
    [
        # The explicit blank line already is the separator, so no second one is added
        ((Paragraph("a"), BlankLine(1), Paragraph("b")), ("a", "", "b")),
        ((Paragraph("a"), BlankLine(2), Paragraph("b")), ("a", "", "", "b")),
        # At the ends, too
        ((BlankLine(1), Paragraph("a")), ("", "a")),
        ((Paragraph("a"), BlankLine(1)), ("a", "")),
        # Two blank lines in a row
        ((BlankLine(1), BlankLine(1)), ("", "")),
    ],
)
def test_separate_blocks_does_not_double_an_explicit_blank_line(blocks, expected) -> None:
    """Verify a BlankLine next to a block replaces the automatic separator."""

    assert separate_blocks(blocks) == expected


def test_separate_blocks_stacks_link_definitions() -> None:
    """Verify link definitions follow one another without blank lines."""

    blocks = (LinkDefinition("a", "x"), LinkDefinition("b", "y"), LinkDefinition("c", "z"))

    assert separate_blocks(blocks) == ("[a]: x", "[b]: y", "[c]: z")


def test_separate_blocks_separates_a_definition_from_other_blocks() -> None:
    """Verify the stacking applies only between two definitions."""

    blocks = (Paragraph("text"), LinkDefinition("a", "x"), LinkDefinition("b", "y"), Paragraph("end"))

    assert separate_blocks(blocks) == ("text", "", "[a]: x", "[b]: y", "", "end")


def test_separate_blocks_stacked_definitions_ignore_the_gap() -> None:
    """Verify definitions stack even when a larger gap is asked for."""

    blocks = (LinkDefinition("a", "x"), LinkDefinition("b", "y"), Paragraph("end"))

    assert separate_blocks(blocks, 2) == ("[a]: x", "[b]: y", "", "", "end")


def test_separate_blocks_accepts_a_generator() -> None:
    """Verify any iterable of blocks works."""

    blocks = (block for block in (Paragraph("a"), Paragraph("b")))

    assert separate_blocks(blocks) == ("a", "", "b")
