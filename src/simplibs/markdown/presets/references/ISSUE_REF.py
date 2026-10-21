# Outers
from ...inline import Reference
from ...inline.enums import ReferenceKind


def ISSUE_REF(number: int | str) -> Reference:
    """Build a reference to an issue or a pull request.

    Init Params:
        number (int | str): The number without the `#`.

    Markdown:
        The number with a hash in front (`#12`).

    Example:
        "Fixes " + ISSUE_REF(12) + "."
        # Writes: "Fixes #12."

    Note:
        An issue of another repository is
        `Reference(ReferenceKind.REPO_ISSUE, "owner/repo#12")`.
    """
    return Reference(ReferenceKind.ISSUE, number)
