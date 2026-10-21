from enum import Enum
import pytest
from simplibs.markdown.blocks.enums import FenceChar
from simplibs.markdown.inline.enums import EmphasisMarker


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "BACKTICK": "`",
    "TILDE": "~",
}


def test_fence_char_is_enum() -> None:
    """Verify FenceChar is an Enum."""

    assert issubclass(FenceChar, Enum)


def test_fence_char_members_and_values() -> None:
    """Verify FenceChar holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in FenceChar} == EXPECTED


def test_fence_char_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(FenceChar.__members__) == len(FenceChar)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_fence_char_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert FenceChar[name].value == value
    assert FenceChar(value) is FenceChar[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_fence_char_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        FenceChar(value)


@pytest.mark.parametrize("member", list(FenceChar))
def test_fence_char_value_is_single_character(member) -> None:
    """Verify the value is one character, so the node can repeat it (`value * n`)."""

    assert len(member.value) == 1


def test_fence_char_tilde_is_not_emphasis_marker_tilde() -> None:
    """Verify equal values do not make the two enums interchangeable."""

    assert FenceChar.TILDE.value == EmphasisMarker.TILDE.value
    assert FenceChar.TILDE != EmphasisMarker.TILDE
