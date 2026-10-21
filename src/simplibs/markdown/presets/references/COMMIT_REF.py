# Outers
from ...inline import Reference
from ...inline.enums import ReferenceKind


def COMMIT_REF(sha: str) -> Reference:
    """Build a reference to a commit.

    Init Params:
        sha (str): The hash: lowercase hexadecimal characters, 7 to 40 of them.

    Markdown:
        The hash as it is (`a1b2c3d`).

    Example:
        "Introduced in " + COMMIT_REF("a1b2c3d") + "."
        # Writes: "Introduced in a1b2c3d."

    Note:
        GitHub shortens the hash and links it to the commit.
    """
    return Reference(ReferenceKind.COMMIT, sha)
