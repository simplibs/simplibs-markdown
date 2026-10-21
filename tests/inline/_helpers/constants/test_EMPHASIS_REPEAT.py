from types import MappingProxyType

import pytest
from simplibs.markdown.inline._helpers import EMPHASIS_REPEAT
from simplibs.markdown.inline.enums import EmphasisKind

EXPECTED = {
    EmphasisKind.EM: 1,
    EmphasisKind.STRONG: 2,
    EmphasisKind.STRONG_EM: 3,
    EmphasisKind.STRIKE: 2,
}


def test_emphasis_repeat_is_read_only() -> None:
    """Verify the table is a read-only mapping."""

    assert isinstance(EMPHASIS_REPEAT, MappingProxyType)

    with pytest.raises(TypeError):
        EMPHASIS_REPEAT[EmphasisKind.EM] = 5


def test_emphasis_repeat_content() -> None:
    """Verify the repeat count of every kind."""

    assert dict(EMPHASIS_REPEAT) == EXPECTED


def test_emphasis_repeat_covers_every_kind() -> None:
    """Verify no EmphasisKind is missing (a new kind must get an entry)."""

    assert set(EMPHASIS_REPEAT) == set(EmphasisKind)


@pytest.mark.parametrize("kind", list(EmphasisKind))
def test_emphasis_repeat_counts_are_positive_integers(kind) -> None:
    """Verify every count is a whole number of at least one."""

    count = EMPHASIS_REPEAT[kind]

    assert isinstance(count, int)
    assert count >= 1
