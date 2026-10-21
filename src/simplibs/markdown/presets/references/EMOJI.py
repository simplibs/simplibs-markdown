# Outers
from ...inline import Reference
from ...inline.enums import ReferenceKind


def EMOJI(name: str) -> Reference:
    """Build an emoji by its name.

    Init Params:
        name (str): The name without the colons: lowercase letters, digits, `_`, `+` and
            `-`.

    Markdown:
        The name between two colons (`:name:`).

    Example:
        "Released " + EMOJI("tada")
        # Writes: "Released :tada:"

    Note:
        The shape is checked, not whether the platform knows the emoji.
    """
    return Reference(ReferenceKind.EMOJI, name)
