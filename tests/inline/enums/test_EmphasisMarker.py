from enum import Enum
import pytest
from simplibs.markdown.inline.enums import EmphasisMarker


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "ASTERISK": "*",
    "UNDERSCORE": "_",
    "TILDE": "~",
}


def test_emphasis_marker_is_enum() -> None:
    """Verify EmphasisMarker is an Enum."""

    assert issubclass(EmphasisMarker, Enum)


def test_emphasis_marker_members_and_values() -> None:
    """Verify EmphasisMarker holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in EmphasisMarker} == EXPECTED


def test_emphasis_marker_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(EmphasisMarker.__members__) == len(EmphasisMarker)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_emphasis_marker_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert EmphasisMarker[name].value == value
    assert EmphasisMarker(value) is EmphasisMarker[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_emphasis_marker_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        EmphasisMarker(value)


@pytest.mark.parametrize("member", list(EmphasisMarker))
def test_emphasis_marker_value_is_single_character(member) -> None:
    """Verify the value is one character, so the node can repeat it (`value * n`)."""

    assert len(member.value) == 1
