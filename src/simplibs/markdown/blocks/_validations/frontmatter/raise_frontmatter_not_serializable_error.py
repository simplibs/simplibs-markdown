from typing import Any, NoReturn
from simplibs.exception import ConversionError


def raise_frontmatter_not_serializable_error(
    value: Any,
) -> NoReturn:
    """Raise ConversionError when a value cannot be written as YAML.

    Args:
        value: The rejected value (or dictionary key).
    """

    # 1. NaN and infinity are a wrong value, everything else is a wrong type
    is_non_finite = isinstance(value, float)

    # 2. Raise structured ConversionError
    raise ConversionError(
        error_name="MARKDOWN_FRONTMATTER_NOT_SERIALIZABLE",
        label="front matter value",
        value=value,
        problem=(
            "This value cannot be written into the front matter.",
            "NaN and infinity have no YAML form here."
            if is_non_finite
            else "Its type is not supported.",
        ),
        expected=(
            "A string, int, finite float, bool or None, "
            "or a dict, list or tuple of them (dict keys must be strings)."
        ),
        how_to_fix=(
            "Convert the value to one of these types first.",
            "Replace NaN and infinity with None or a string.",
        ),
        exception=ValueError if is_non_finite else TypeError,
    )


_DESIGN_NOTES = """
# raise_frontmatter_not_serializable_error — A Value YAML Cannot Hold

## Purpose
The front matter serializer writes only plain data. A date, a set or a custom
object would otherwise be guessed at, and the guess would differ per parser.

## `ConversionError`
The value is not a wrong parameter of the node, it fails in the conversion to
text, so this card is the one place where `ConversionError` is used.

## `value`
Also used for a dictionary key that is not a string.
"""
