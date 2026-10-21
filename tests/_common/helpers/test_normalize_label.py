import pytest
from simplibs.markdown._common.helpers import normalize_label


@pytest.mark.parametrize(
    "label, expected",
    [
        ("Foo Bar", "Foo Bar"),         # already normal
        ("  Foo Bar  ", "Foo Bar"),     # the ends are trimmed
        ("Foo     Bar", "Foo Bar"),     # a run of spaces collapses
        ("Foo\tBar", "Foo Bar"),        # a tab is whitespace
        ("Foo\nBar", "Foo Bar"),        # so is a line break
        (" a \t b \n c ", "a b c"),     # mixed whitespace
        ("FOO  Bar", "FOO Bar"),        # case is left as written
        ("single", "single"),
        ("", ""),
        ("   ", ""),                    # only whitespace leaves nothing
        ("\t\n", ""),
    ],
)
def test_normalize_label(label, expected) -> None:
    """Verify every run of whitespace becomes one space and the ends are trimmed."""

    assert normalize_label(label) == expected


@pytest.mark.parametrize("label", ["Foo   Bar", "  a\tb  ", "", "x"])
def test_normalize_label_is_idempotent(label) -> None:
    """Verify a normalized label does not change when it is normalized again."""

    once = normalize_label(label)
    assert normalize_label(once) == once
