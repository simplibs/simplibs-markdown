import pytest
from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.markdown.base_class import Markdown
from simplibs.markdown.base_class.enums import NodeLevel
from simplibs.markdown.blocks.ThematicBreak import ThematicBreak
from simplibs.markdown.blocks.enums import BreakChar


def test_thematic_break_is_a_block_node() -> None:
    """Verify the class and the level."""

    node = ThematicBreak()

    assert isinstance(node, Markdown)
    assert node.node_level is NodeLevel.BLOCK


def test_thematic_break_defaults() -> None:
    """Verify a dash rule of three characters."""

    node = ThematicBreak()

    assert node.char is BreakChar.DASH
    assert node.length == 3
    assert node.to_lines() == ("---",)


@pytest.mark.parametrize(
    "char, length, expected",
    [
        (BreakChar.DASH, 3, "---"),
        (BreakChar.ASTERISK, 3, "***"),
        (BreakChar.UNDERSCORE, 3, "___"),
        (BreakChar.DASH, 10, "----------"),
        (BreakChar.ASTERISK, 5, "*****"),
    ],
)
def test_thematic_break_writes_the_character_repeated(char, length, expected) -> None:
    """Verify the rule is the character repeated `length` times."""

    node = ThematicBreak(char, length)

    assert node.to_lines() == (expected,)
    assert node.to_text() == expected
    assert str(node) == expected


def test_thematic_break_has_no_instance_dict() -> None:
    """Verify slots are in force."""

    assert not hasattr(ThematicBreak(), "__dict__")


@pytest.mark.parametrize("char", ["-", "*", 1, None, True])
def test_thematic_break_rejects_a_char_that_is_not_a_break_char(subtests, char) -> None:
    """Verify `char` has to be a BreakChar."""

    assert_exception_function(
        subtests,
        ThematicBreak,
        invalid_params=(char,),
        exception_type=ParamError,
        error_name="MARKDOWN_THEMATIC_BREAK_INVALID_CHAR",
        value=char,
        verbose=False,
    )


@pytest.mark.parametrize("length", [2, 1, 0, -5, "3", 2.5, None, True, False])
def test_thematic_break_rejects_a_length_below_three_or_not_an_integer(subtests, length) -> None:
    """Verify `length` has to be an integer of at least three (a bool is not)."""

    assert_exception_function(
        subtests,
        ThematicBreak,
        invalid_params=(BreakChar.DASH, length),
        exception_type=ParamError,
        error_name="MARKDOWN_THEMATIC_BREAK_TOO_SHORT",
        value=length,
        verbose=False,
    )


def test_thematic_break_checks_the_char_before_the_length(subtests) -> None:
    """Verify a wrong char is reported even when the length is wrong as well."""

    assert_exception_function(
        subtests,
        ThematicBreak,
        invalid_params=("-", 1),
        exception_type=ParamError,
        error_name="MARKDOWN_THEMATIC_BREAK_INVALID_CHAR",
        verbose=False,
    )
