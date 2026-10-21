import pytest
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.ThematicBreak import ThematicBreak
from simplibs.markdown.blocks.enums import BreakChar
from simplibs.markdown.containers.Document import Document
from simplibs.markdown.presets.headings import H1
from simplibs.markdown.presets.spacing import RULE


def test_rule_is_a_ready_thematic_break_of_three_dashes() -> None:
    """Verify it is an instance, with the default character and length."""

    assert isinstance(RULE, ThematicBreak)
    assert RULE.char is BreakChar.DASH
    assert RULE.length == 3
    assert RULE.node_level is NodeLevel.BLOCK


def test_rule_is_used_without_parentheses() -> None:
    """Verify it is not a function."""

    assert not callable(RULE)


def test_rule_text_and_lines() -> None:
    """Verify the three dashes."""

    assert RULE.to_lines() == ("---",)
    assert RULE.to_text() == "---"


def test_rule_example_from_the_docstring() -> None:
    """Verify the text the docstring promises."""

    result = H1("A") + RULE + "text"

    assert isinstance(result, Document)
    assert result.to_lines() == ("# A", "", "---", "", "text")


def test_rule_may_be_used_more_than_once() -> None:
    """Verify one instance can be shared, because a node does not change."""

    result = "a" + RULE + "b" + RULE + "c"

    assert result.to_lines() == ("a", "", "---", "", "b", "", "---", "", "c")
