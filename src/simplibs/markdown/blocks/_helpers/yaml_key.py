import json
from typing import Any
# Outers
from .._validations.frontmatter import raise_frontmatter_not_serializable_error
# Inners
from simplibs.markdown.blocks._helpers.constants.YAML_PLAIN_KEY import YAML_PLAIN_KEY
from simplibs.markdown.blocks._helpers.constants.YAML_RESERVED import YAML_RESERVED


def yaml_key(key: Any) -> str:
    """Write a dictionary key as YAML.

    Args:
        key: The key; it has to be a string.

    Returns:
        The key as it is when that is safe (an ASCII word that is not a reserved
        value), otherwise in double quotes.

    Raises:
        ConversionError: If the key is not a string.
    """

    # 1. Only strings are keys
    if not isinstance(key, str):
        raise_frontmatter_not_serializable_error(key)

    # 2. A plain ASCII word that is not a reserved value is written bare
    if YAML_PLAIN_KEY.fullmatch(key) and key.casefold() not in YAML_RESERVED:
        return key

    # 3. Everything else is a quoted string
    return json.dumps(key, ensure_ascii=False)


_DESIGN_NOTES = """
# yaml_key — One Rule for a Key

## Purpose
Most keys are plain words and stay readable. The rest is quoted with the JSON
form, which is also valid YAML.

## What Stays Bare
An ASCII word (`YAML_PLAIN_KEY`) that YAML 1.1 does not read as a value
(`YAML_RESERVED`: `no`, `on`, `null`...). A key with a non-ASCII letter is
quoted wherever the letter stands, so `název` and `živnost` are treated alike.

## `ensure_ascii=False`
A quoted key in Czech stays `"název"` and does not turn into `"n\\u00e1zev"`.
"""
