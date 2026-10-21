import pytest
from simplibs.markdown.inline._helpers import ALWAYS_ESCAPED, LINE_START_ESCAPED


def test_always_escaped_is_a_frozenset() -> None:
    """Verify the constant cannot be changed at runtime."""

    assert isinstance(ALWAYS_ESCAPED, frozenset)


def test_always_escaped_content() -> None:
    """Verify exactly these characters are escaped wherever they stand."""

    assert ALWAYS_ESCAPED == frozenset({"\\", "`", "*", "_", "[", "]", "<", ">", "&", "~", "$"})


@pytest.mark.parametrize("char", sorted(ALWAYS_ESCAPED))
def test_always_escaped_items_are_single_characters(char) -> None:
    """Verify every item is one character, so `escape_text` can test `char in ...`."""

    assert len(char) == 1


def test_always_escaped_does_not_overlap_line_start_escaped() -> None:
    """Verify no character is in both sets, which would escape it twice."""

    assert ALWAYS_ESCAPED.isdisjoint(LINE_START_ESCAPED)
