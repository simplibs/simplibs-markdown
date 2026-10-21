from enum import Enum
import pytest
from simplibs.markdown.containers.enums import ListMarker


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "DASH": "-",
    "ASTERISK": "*",
    "PLUS": "+",
    "DOT": ".",
    "PAREN": ")",
}


def test_list_marker_is_enum() -> None:
    """Verify ListMarker is an Enum."""

    assert issubclass(ListMarker, Enum)


def test_list_marker_members_and_values() -> None:
    """Verify ListMarker holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in ListMarker} == EXPECTED


def test_list_marker_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(ListMarker.__members__) == len(ListMarker)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_list_marker_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert ListMarker[name].value == value
    assert ListMarker(value) is ListMarker[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_list_marker_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        ListMarker(value)


@pytest.mark.parametrize("member", list(ListMarker))
def test_list_marker_value_is_single_character(member) -> None:
    """Verify the value is one character, so the node can repeat it (`value * n`)."""

    assert len(member.value) == 1
