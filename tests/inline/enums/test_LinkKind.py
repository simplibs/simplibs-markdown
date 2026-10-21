from enum import Enum
import pytest
from simplibs.markdown.inline.enums import LinkKind


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "INLINE": "inline",
    "REFERENCE": "reference",
    "COLLAPSED": "collapsed",
    "SHORTCUT": "shortcut",
    "AUTOLINK": "autolink",
    "BARE": "bare",
}


def test_link_kind_is_enum() -> None:
    """Verify LinkKind is an Enum."""

    assert issubclass(LinkKind, Enum)


def test_link_kind_members_and_values() -> None:
    """Verify LinkKind holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in LinkKind} == EXPECTED


def test_link_kind_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(LinkKind.__members__) == len(LinkKind)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_link_kind_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert LinkKind[name].value == value
    assert LinkKind(value) is LinkKind[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_link_kind_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        LinkKind(value)


@pytest.mark.parametrize("member", list(LinkKind))
def test_link_kind_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
