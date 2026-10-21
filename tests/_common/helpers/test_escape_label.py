import random
import re

import pytest
from simplibs.markdown._common.helpers import escape_label, normalize_label

_ESCAPABLE = re.compile(r"\\([!-/:-@\[-`{-~])")


@pytest.mark.parametrize(
    "label, expected",
    [
        # Nothing to escape
        ("", ""),
        ("ref", "ref"),
        ("Foo Bar", "Foo Bar"),
        ("a-b_c.d", "a-b_c.d"),
        # Brackets end a label early
        ("a]b", r"a\]b"),
        ("a[b", r"a\[b"),
        ("[x]", r"\[x\]"),
        ("]", r"\]"),
        ("[", r"\["),
        ("a[b]c", r"a\[b\]c"),
        # A backslash is doubled, and the backslashes added for the brackets are not
        (r"a\b", r"a\\b"),
        ("\\", r"\\"),
        (r"a\]b", r"a\\\]b"),
        ("a\\]", r"a\\\]"),
    ],
)
def test_escape_label(label, expected) -> None:
    """Verify the brackets and the backslashes, and only those, are escaped."""

    assert escape_label(label) == expected


@pytest.mark.parametrize("label", ["Foo   Bar", " a ", "a\tb", "a\nb"])
def test_escape_label_does_not_touch_whitespace(label) -> None:
    """Verify collapsing whitespace is the job of `normalize_label`."""

    assert escape_label(label) == label


def test_escape_label_does_not_normalize() -> None:
    """Verify the two functions stay separate: this one changes how the label is written, not what it is."""

    assert escape_label("a   [b]") == r"a   \[b\]"
    assert escape_label(normalize_label("a   [b]")) == r"a \[b\]"


def test_escape_label_returns_a_string() -> None:
    """Verify the type."""

    assert isinstance(escape_label("a"), str)


def _samples(count: int = 400) -> list[str]:
    """The same pseudo-random labels on every run."""

    rng = random.Random(20240603)
    alphabet = list("ab []\\.-_ ")
    return ["".join(rng.choices(alphabet, k=rng.randint(0, 8))) for _ in range(count)]


@pytest.mark.parametrize("label", _samples())
def test_escape_label_reads_back_as_the_original(label) -> None:
    """Verify a parser gets the label that was given."""

    assert _ESCAPABLE.sub(r"\1", escape_label(label)) == label


@pytest.mark.parametrize("label", _samples(200))
def test_escape_label_leaves_no_bare_bracket(label) -> None:
    """Verify no bracket is left that could end the label (every escaped pair is removed first)."""

    without_pairs = re.sub(r"\\.", "", escape_label(label), flags=re.DOTALL)

    assert "[" not in without_pairs
    assert "]" not in without_pairs
