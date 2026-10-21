from types import MappingProxyType

import pytest
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.blocks._helpers import BREAK_SUFFIX
from simplibs.markdown.inline._helpers import LINE_BREAKS

EXPECTED = {
    LineBreakStyle.SPACES: "  ",
    LineBreakStyle.BACKSLASH: "\\",
    LineBreakStyle.HTML: "<br>",
}


def test_break_suffix_is_read_only() -> None:
    """Verify the table is a read-only mapping."""

    assert isinstance(BREAK_SUFFIX, MappingProxyType)

    with pytest.raises(TypeError):
        BREAK_SUFFIX[LineBreakStyle.HTML] = "<br/>"


def test_break_suffix_content() -> None:
    """Verify the exact suffix of every style."""

    assert dict(BREAK_SUFFIX) == EXPECTED


def test_break_suffix_covers_every_style() -> None:
    """Verify no LineBreakStyle is missing (a new style must get an entry)."""

    assert set(BREAK_SUFFIX) == set(LineBreakStyle)


@pytest.mark.parametrize("style", list(LineBreakStyle))
def test_break_suffix_has_no_newline(style) -> None:
    """Verify the suffix goes to the end of a line that is already split."""

    assert "\n" not in BREAK_SUFFIX[style]


@pytest.mark.parametrize("style", list(LineBreakStyle))
def test_break_suffix_is_the_start_of_the_inline_break(style) -> None:
    """Verify the inline table writes the same mark, only with the newline behind it."""

    rest = LINE_BREAKS[style][len(BREAK_SUFFIX[style]):]

    assert LINE_BREAKS[style].startswith(BREAK_SUFFIX[style])
    assert rest in ("", "\n")
