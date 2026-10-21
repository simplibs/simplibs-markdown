from enum import Enum
import pytest
from simplibs.markdown.containers.enums import TableAlign


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "NONE": "none",
    "LEFT": "left",
    "CENTER": "center",
    "RIGHT": "right",
}


def test_table_align_is_enum() -> None:
    """Verify TableAlign is an Enum."""

    assert issubclass(TableAlign, Enum)


def test_table_align_members_and_values() -> None:
    """Verify TableAlign holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in TableAlign} == EXPECTED


def test_table_align_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(TableAlign.__members__) == len(TableAlign)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_table_align_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert TableAlign[name].value == value
    assert TableAlign(value) is TableAlign[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_table_align_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        TableAlign(value)


@pytest.mark.parametrize("member", list(TableAlign))
def test_table_align_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
