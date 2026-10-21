from enum import Enum
import pytest
from simplibs.markdown.base_class.enums import NodeLevel


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "INLINE": "inline",
    "BLOCK": "block",
}


def test_node_level_is_enum() -> None:
    """Verify NodeLevel is an Enum."""

    assert issubclass(NodeLevel, Enum)


def test_node_level_members_and_values() -> None:
    """Verify NodeLevel holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in NodeLevel} == EXPECTED


def test_node_level_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(NodeLevel.__members__) == len(NodeLevel)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_node_level_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert NodeLevel[name].value == value
    assert NodeLevel(value) is NodeLevel[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_node_level_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        NodeLevel(value)


@pytest.mark.parametrize("member", list(NodeLevel))
def test_node_level_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
