from enum import Enum
import pytest
from simplibs.markdown.inline.enums import ReferenceKind


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "MENTION": "mention",
    "TEAM": "team",
    "ISSUE": "issue",
    "REPO_ISSUE": "repo_issue",
    "COMMIT": "commit",
    "EMOJI": "emoji",
}


def test_reference_kind_is_enum() -> None:
    """Verify ReferenceKind is an Enum."""

    assert issubclass(ReferenceKind, Enum)


def test_reference_kind_members_and_values() -> None:
    """Verify ReferenceKind holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in ReferenceKind} == EXPECTED


def test_reference_kind_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(ReferenceKind.__members__) == len(ReferenceKind)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_reference_kind_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert ReferenceKind[name].value == value
    assert ReferenceKind(value) is ReferenceKind[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_reference_kind_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        ReferenceKind(value)


@pytest.mark.parametrize("member", list(ReferenceKind))
def test_reference_kind_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
