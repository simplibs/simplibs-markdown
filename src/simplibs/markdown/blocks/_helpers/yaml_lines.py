from typing import Any
# Inners
from .yaml_inline import yaml_inline
from .yaml_key import yaml_key


def yaml_lines(value: Any, depth: int = 0) -> list[str]:
    """Write a value as indented YAML lines.

    Args:
        value: Any supported value; dictionaries and lists nest.
        depth: The nesting depth; each level indents by two spaces.

    Returns:
        The lines of the YAML text.

    Raises:
        ConversionError: If a value or a key cannot be written as YAML.
    """

    # 1. The indentation of this level
    pad = "  " * depth

    # 2. A non-empty dictionary: one `key:` line per entry
    if isinstance(value, dict) and value:
        lines = []
        for key, item in value.items():
            head = f"{pad}{yaml_key(key)}:"

            # 2.1 A non-empty collection continues on the next lines
            if isinstance(item, (dict, list, tuple)) and item:
                lines.append(head)
                lines.extend(yaml_lines(item, depth + 1))

            # 2.2 Anything else stays on the line of its key
            else:
                lines.append(f"{head} {yaml_inline(item)}")
        return lines

    # 3. A non-empty list: one `-` line per item
    if isinstance(value, (list, tuple)) and value:
        lines = []
        for item in value:

            # 3.1 A non-empty collection continues on the next lines
            if isinstance(item, (dict, list, tuple)) and item:
                lines.append(f"{pad}-")
                lines.extend(yaml_lines(item, depth + 1))

            # 3.2 Anything else stays on the line of its dash
            else:
                lines.append(f"{pad}- {yaml_inline(item)}")
        return lines

    # 4. A scalar or an empty collection is one line
    return [pad + yaml_inline(value)]


_DESIGN_NOTES = """
# yaml_lines — A Small YAML Writer

## Purpose
Front matter is a few keys and lists. A writer for exactly that — dictionaries,
lists, scalars — is shorter than a dependency on a YAML library, and every
choice in it is visible.

## Not a General Serializer
No anchors, no multi-line strings, no sets, no dates. A value outside the
supported types is an error, not a guess.

## A Dash With a Nested Collection
`-` alone on its line, the content on the next lines one level deeper. It is
valid YAML and avoids the alignment rules of `- key: value`.
"""
