import pytest
from simplibs.markdown.blocks._helpers import VOID_TAGS


def test_void_tags_is_a_frozenset() -> None:
    """Verify the constant cannot be changed at runtime."""

    assert isinstance(VOID_TAGS, frozenset)


def test_void_tags_content() -> None:
    """Verify the void elements of the HTML Standard."""

    assert VOID_TAGS == frozenset({
        "area", "base", "br", "col", "embed", "hr", "img",
        "input", "link", "meta", "source", "track", "wbr",
    })


@pytest.mark.parametrize("tag", sorted(VOID_TAGS))
def test_void_tags_are_lowercase(tag) -> None:
    """Verify the names are lowercase, as `Html` compares them."""

    assert tag == tag.lower()


@pytest.mark.parametrize("tag", ["div", "span", "a", "p", "details", "summary", "kbd", "my-tag"])
def test_void_tags_do_not_hold_ordinary_tags(tag) -> None:
    """Verify tags that hold content are not in the set."""

    assert tag not in VOID_TAGS
