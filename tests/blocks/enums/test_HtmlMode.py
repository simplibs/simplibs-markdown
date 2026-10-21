from enum import Enum
import pytest
from simplibs.markdown.blocks.enums import HtmlMode


# The contract: every member and its value. A change here is a deliberate API change.
EXPECTED = {
    "BLOCK": "block",
    "INLINE": "inline",
    "COMMENT": "comment",
}


def test_html_mode_is_enum() -> None:
    """Verify HtmlMode is an Enum."""

    assert issubclass(HtmlMode, Enum)


def test_html_mode_members_and_values() -> None:
    """Verify HtmlMode holds exactly the expected members with the expected values."""

    assert {member.name: member.value for member in HtmlMode} == EXPECTED


def test_html_mode_has_no_aliases() -> None:
    """Verify no two members share a value (an alias would hide a member)."""

    assert len(HtmlMode.__members__) == len(HtmlMode)


@pytest.mark.parametrize("name, value", EXPECTED.items())
def test_html_mode_lookup(name, value) -> None:
    """Verify every member is found by its name and by its value."""

    assert HtmlMode[name].value == value
    assert HtmlMode(value) is HtmlMode[name]


@pytest.mark.parametrize("value", ["", "unknown", None, 0])
def test_html_mode_rejects_unknown_value(value) -> None:
    """Verify a value that belongs to no member raises ValueError."""

    with pytest.raises(ValueError):
        HtmlMode(value)


@pytest.mark.parametrize("member", list(HtmlMode))
def test_html_mode_value_is_lowercase_name(member) -> None:
    """Verify the value is the member name in lower case (values are identifiers only)."""

    assert member.value == member.name.lower()
