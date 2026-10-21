import pytest
from simplibs.markdown.inline._helpers import LINE_START_ESCAPED


def test_line_start_escaped_is_a_frozenset() -> None:
    """Verify the constant cannot be changed at runtime."""

    assert isinstance(LINE_START_ESCAPED, frozenset)


def test_line_start_escaped_content() -> None:
    """Verify exactly these characters are escaped at the start of a line."""

    assert LINE_START_ESCAPED == frozenset({"#", "+", "-", "="})


@pytest.mark.parametrize("char", sorted(LINE_START_ESCAPED))
def test_line_start_escaped_items_are_single_characters(char) -> None:
    """Verify every item is one character, so `escape_text` can test `body[0] in ...`."""

    assert len(char) == 1
