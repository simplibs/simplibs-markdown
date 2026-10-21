# Outers
from ...inline import Reference
from ...inline.enums import ReferenceKind


def MENTION(user: str) -> Reference:
    """Build a mention of a user.

    Init Params:
        user (str): The username without the `@`: letters, digits and hyphens, up to 39
            characters, starting with a letter or a digit.

    Markdown:
        The name with an at sign in front (`@user`).

    Example:
        "Thanks, " + MENTION("octocat") + "!"
        # Writes: "Thanks, @octocat!"

    Note:
        GitHub links and notifies the user. A team is
        `Reference(ReferenceKind.TEAM, "org/team")`. The shape is checked, not whether the
        user exists.
    """
    return Reference(ReferenceKind.MENTION, user)
