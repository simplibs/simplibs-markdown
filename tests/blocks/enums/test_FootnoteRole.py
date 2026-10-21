from enum import Enum
import pytest
from simplibs.markdown.blocks.enums import FootnoteRole


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "REFERENCE": "reference",
    "DEFINITION": "definition",
}


def test_footnote_role_is_enum() -> None:
    """Verify FootnoteRole is an Enum."""

    assert issubclass(FootnoteRole, Enum)


def test_footnote_role_members_and_values() -> None:
    """Verify FootnoteRole holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in FootnoteRole} == EXPECTED


def test_footnote_role_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(FootnoteRole.__members__) == len(FootnoteRole)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_footnote_role_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert FootnoteRole[name].value == value
    assert FootnoteRole(value) is FootnoteRole[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_footnote_role_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        FootnoteRole(value)


@pytest.mark.parametrize("member", list(FootnoteRole))
def test_footnote_role_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
