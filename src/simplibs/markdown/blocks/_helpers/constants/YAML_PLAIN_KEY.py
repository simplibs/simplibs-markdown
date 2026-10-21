import re
from typing import Final


YAML_PLAIN_KEY: Final = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")
"""Pattern of a dictionary key that can be written in YAML without quotes: ASCII only."""


_DESIGN_NOTES = """
# YAML_PLAIN_KEY — Keys That Need No Quotes

## Purpose
`title`, `last-updated`, `_id`. Everything else (`my key`, `1st`, `a:b`) is
written in quotes, because an unquoted key is read differently by different
parsers.

## ASCII Only
A bare key is made of ASCII letters, digits, `_` and `-`, and does not start
with a digit or a hyphen. The pattern spells the class out instead of using
`\\w`, which in Python also matches letters such as `á` or `ž`: with it `název`
was written bare but `živnost` (a non-ASCII first letter) in quotes, and the
result depended on where the letter stood. Now every key with a non-ASCII
letter is quoted, wherever it stands, and the rule fits in one sentence.
"""
