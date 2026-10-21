from enum import Enum
import pytest
from simplibs.markdown.inline.enums import EmphasisKind


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "EM": "em",
    "STRONG": "strong",
    "STRONG_EM": "strong_em",
    "STRIKE": "strike",
}


def test_emphasis_kind_is_enum() -> None:
    """Verify EmphasisKind is an Enum."""

    assert issubclass(EmphasisKind, Enum)


def test_emphasis_kind_members_and_values() -> None:
    """Verify EmphasisKind holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in EmphasisKind} == EXPECTED


def test_emphasis_kind_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(EmphasisKind.__members__) == len(EmphasisKind)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_emphasis_kind_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert EmphasisKind[name].value == value
    assert EmphasisKind(value) is EmphasisKind[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_emphasis_kind_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        EmphasisKind(value)


@pytest.mark.parametrize("member", list(EmphasisKind))
def test_emphasis_kind_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
