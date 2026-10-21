import re
from typing import Final


ATTR_NAME: Final = re.compile(r"[A-Za-z_:][-A-Za-z0-9_:.]*")
"""Pattern of a valid HTML attribute name."""


_DESIGN_NOTES = """
# ATTR_NAME — A Name That Cannot End the Attribute

## Purpose
Values are escaped by `build_html_open_tag`. Names cannot be escaped, so only
the characters of the HTML specification are allowed, which also keeps out
spaces, quotes and `=`.
"""
