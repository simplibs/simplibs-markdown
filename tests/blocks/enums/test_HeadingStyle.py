from enum import Enum
import pytest
from simplibs.markdown.blocks.enums import HeadingStyle


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "ATX": "atx",
    "ATX_CLOSED": "atx_closed",
    "SETEXT": "setext",
}


def test_heading_style_is_enum() -> None:
    """Verify HeadingStyle is an Enum."""

    assert issubclass(HeadingStyle, Enum)


def test_heading_style_members_and_values() -> None:
    """Verify HeadingStyle holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in HeadingStyle} == EXPECTED


def test_heading_style_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(HeadingStyle.__members__) == len(HeadingStyle)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_heading_style_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert HeadingStyle[name].value == value
    assert HeadingStyle(value) is HeadingStyle[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_heading_style_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        HeadingStyle(value)


@pytest.mark.parametrize("member", list(HeadingStyle))
def test_heading_style_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
