from typing import Final


YAML_RESERVED: Final[frozenset[str]] = frozenset({
    "true", "false", "null", "yes", "no", "on", "off", "y", "n",
})
"""Lowercase words that YAML 1.1 reads as a value, so a key with that name is quoted."""


_DESIGN_NOTES = """
# YAML_RESERVED — A Key That Would Become a Boolean

## Purpose
In YAML 1.1 `no:` and `n:` are the key `false`. The key is compared in lower
case, so `No` and `NO` are quoted as well.
"""
