from types import MappingProxyType

import pytest
from simplibs.markdown._common.enums import LineBreakStyle
from simplibs.markdown.inline._helpers import LINE_BREAKS

EXPECTED = {
    LineBreakStyle.SPACES: "  \n",
    LineBreakStyle.BACKSLASH: "\\\n",
    LineBreakStyle.HTML: "<br>",
}


def test_line_breaks_is_read_only() -> None:
    """Verify the table is a read-only mapping."""

    assert isinstance(LINE_BREAKS, MappingProxyType)

    with pytest.raises(TypeError):
        LINE_BREAKS[LineBreakStyle.HTML] = "<br/>"


def test_line_breaks_content() -> None:
    """Verify the exact text of every style."""

    assert dict(LINE_BREAKS) == EXPECTED


def test_line_breaks_covers_every_style() -> None:
    """Verify no LineBreakStyle is missing (a new style must get an entry)."""

    assert set(LINE_BREAKS) == set(LineBreakStyle)


@pytest.mark.parametrize("style", [LineBreakStyle.SPACES, LineBreakStyle.BACKSLASH])
def test_line_breaks_ending_styles_end_the_line(style) -> None:
    """Verify these two styles carry the newline themselves."""

    assert LINE_BREAKS[style].endswith("\n")


def test_line_breaks_html_stays_inside_the_line() -> None:
    """Verify the HTML style has no newline."""

    assert "\n" not in LINE_BREAKS[LineBreakStyle.HTML]
