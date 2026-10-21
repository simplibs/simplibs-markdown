from enum import Enum
import pytest
from simplibs.markdown._common.enums import LineBreakStyle


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "SPACES": "spaces",
    "BACKSLASH": "backslash",
    "HTML": "html",
}


def test_line_break_style_is_enum() -> None:
    """Verify LineBreakStyle is an Enum."""

    assert issubclass(LineBreakStyle, Enum)


def test_line_break_style_members_and_values() -> None:
    """Verify LineBreakStyle holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in LineBreakStyle} == EXPECTED


def test_line_break_style_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(LineBreakStyle.__members__) == len(LineBreakStyle)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_line_break_style_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert LineBreakStyle[name].value == value
    assert LineBreakStyle(value) is LineBreakStyle[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_line_break_style_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        LineBreakStyle(value)


@pytest.mark.parametrize("member", list(LineBreakStyle))
def test_line_break_style_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
