from enum import Enum
import pytest
from simplibs.markdown.containers.enums import AlertKind


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "NOTE": "NOTE",
    "TIP": "TIP",
    "IMPORTANT": "IMPORTANT",
    "WARNING": "WARNING",
    "CAUTION": "CAUTION",
}


def test_alert_kind_is_enum() -> None:
    """Verify AlertKind is an Enum."""

    assert issubclass(AlertKind, Enum)


def test_alert_kind_members_and_values() -> None:
    """Verify AlertKind holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in AlertKind} == EXPECTED


def test_alert_kind_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(AlertKind.__members__) == len(AlertKind)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_alert_kind_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert AlertKind[name].value == value
    assert AlertKind(value) is AlertKind[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_alert_kind_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        AlertKind(value)


@pytest.mark.parametrize("member", list(AlertKind))
def test_alert_kind_value_is_name_in_capitals(member) -> None:
    """Verify the value is the capitalized word written in `[!...]`, as GitHub requires."""

    assert member.value == member.name
    assert member.value.isupper()
