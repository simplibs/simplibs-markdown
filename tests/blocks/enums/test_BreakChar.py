from enum import Enum
import pytest
from simplibs.markdown.blocks.enums import BreakChar


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "DASH": "-",
    "ASTERISK": "*",
    "UNDERSCORE": "_",
}


def test_break_char_is_enum() -> None:
    """Verify BreakChar is an Enum."""

    assert issubclass(BreakChar, Enum)


def test_break_char_members_and_values() -> None:
    """Verify BreakChar holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in BreakChar} == EXPECTED


def test_break_char_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(BreakChar.__members__) == len(BreakChar)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_break_char_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert BreakChar[name].value == value
    assert BreakChar(value) is BreakChar[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_break_char_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        BreakChar(value)


@pytest.mark.parametrize("member", list(BreakChar))
def test_break_char_value_is_single_character(member) -> None:
    """Verify the value is one character, so the node can repeat it (`value * n`)."""

    assert len(member.value) == 1
