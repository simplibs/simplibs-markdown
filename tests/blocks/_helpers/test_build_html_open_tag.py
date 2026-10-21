import pytest
from simplibs.markdown.blocks._helpers import build_html_open_tag


@pytest.mark.parametrize(
    "tag, attrs, expected",
    [
        # No attributes
        ("br", {}, "<br>"),
        ("div", {}, "<div>"),
        # One attribute, quoted
        ("a", {"id": "top"}, '<a id="top">'),
        # Several, in the given order
        ("a", {"href": "x", "id": "y"}, '<a href="x" id="y">'),
        ("a", {"id": "y", "href": "x"}, '<a id="y" href="x">'),
        # `True` is a bare flag
        ("details", {"open": True}, "<details open>"),
        ("input", {"disabled": True, "required": True}, "<input disabled required>"),
        # `False` and `None` leave the attribute out
        ("div", {"hidden": False, "id": None, "class": "x"}, '<div class="x">'),
        ("div", {"hidden": False}, "<div>"),
        ("div", {"id": None}, "<div>"),
        # A flag next to a value
        ("details", {"open": True, "class": "box"}, '<details open class="box">'),
        # An empty string is a value, not an omission
        ("a", {"title": ""}, '<a title="">'),
        # Other types are written with str()
        ("td", {"colspan": 2}, '<td colspan="2">'),
        ("td", {"colspan": 0}, '<td colspan="0">'),
        ("td", {"colspan": 1}, '<td colspan="1">'),
        ("img", {"width": 1.5}, '<img width="1.5">'),
    ],
)
def test_build_html_open_tag(tag, attrs, expected) -> None:
    """Verify the tag, the order of the attributes and the flag rules."""

    assert build_html_open_tag(tag, attrs) == expected


@pytest.mark.parametrize(
    "value, escaped",
    [
        ('say "hi"', "say &quot;hi&quot;"),
        ("it's", "it&#x27;s"),
        ("a & b", "a &amp; b"),
        ("<b>", "&lt;b&gt;"),
        ('x" onclick="evil', "x&quot; onclick=&quot;evil"),
        ("plain", "plain"),
    ],
)
def test_build_html_open_tag_escapes_the_value(value, escaped) -> None:
    """Verify a value cannot end the attribute or the tag."""

    assert build_html_open_tag("a", {"title": value}) == f'<a title="{escaped}">'


@pytest.mark.parametrize("attrs", [{}, {"id": "x"}, {"open": True}, {"title": 'a"b'}])
def test_build_html_open_tag_is_one_tag(attrs) -> None:
    """Verify the result starts with '<', ends with '>' and has no '>' inside."""

    result = build_html_open_tag("a", attrs)

    assert result.startswith("<a")
    assert result.endswith(">")
    assert ">" not in result[:-1]
