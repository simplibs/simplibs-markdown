import pytest
from simplibs.markdown.blocks._helpers import YAML_RESERVED


def test_yaml_reserved_is_a_frozenset() -> None:
    """Verify the constant cannot be changed at runtime."""

    assert isinstance(YAML_RESERVED, frozenset)


def test_yaml_reserved_content() -> None:
    """Verify the words that YAML 1.1 reads as a value."""

    assert YAML_RESERVED == frozenset({"true", "false", "null", "yes", "no", "on", "off", "y", "n"})


@pytest.mark.parametrize("word", sorted(YAML_RESERVED))
def test_yaml_reserved_words_are_lowercase(word) -> None:
    """Verify the words are lowercase, because a key is compared in lower case."""

    assert word == word.casefold()
