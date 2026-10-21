import re
from typing import Final


TAG_NAME: Final = re.compile(r"[A-Za-z][A-Za-z0-9-]*")
"""Pattern of a valid HTML tag name."""


_DESIGN_NOTES = """
# TAG_NAME — What May Stand Between `<` and `>`

## Purpose
Letters, digits and hyphens, starting with a letter. It covers the standard
tags and custom elements (`my-tag`) and nothing that could break out of the
tag.
"""
