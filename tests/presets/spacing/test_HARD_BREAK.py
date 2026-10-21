import pytest
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.inline.InlineJoin import InlineJoin
from simplibs.markdown.inline.LineBreak import LineBreak
from simplibs.markdown.presets.spacing import HARD_BREAK


def test_hard_break_is_a_ready_line_break_with_spaces() -> None:
    """Verify it is an instance, with the default style and the inline level."""

    assert isinstance(HARD_BREAK, LineBreak)
    assert HARD_BREAK.style is LineBreakStyle.SPACES
    assert HARD_BREAK.node_level is NodeLevel.INLINE


def test_hard_break_is_used_without_parentheses() -> None:
    """Verify it is not a function."""

    assert not callable(HARD_BREAK)


def test_hard_break_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    result = "first" + HARD_BREAK + "second"

    assert isinstance(result, InlineJoin)
    assert result.to_text() == "first  \nsecond"


def test_hard_break_text_and_lines() -> None:
    """Verify the two spaces and the line break."""

    assert HARD_BREAK.to_text() == "  \n"
    assert HARD_BREAK.to_lines() == ("  ", "")


def test_hard_break_may_be_used_more_than_once() -> None:
    """Verify one instance can be shared, because a node does not change."""

    result = "a" + HARD_BREAK + "b" + HARD_BREAK + "c"

    assert result.to_text() == "a  \nb  \nc"
