# Outers
from ...inline import Link
from ...inline.enums import LinkKind


def BARE_URL(url: str) -> Link:
    """Build an address written as it is.

    Init Params:
        url (str): The address.

    Markdown:
        The address without any markup (`url`).

    Example:
        BARE_URL("https://example.com")
        # Writes: "https://example.com"

    Note:
        GitHub and similar renderers turn it into a link; strict CommonMark renderers leave
        it as plain text. Use `AUTOLINK` when that matters.
    """
    return Link(dest=url, kind=LinkKind.BARE)
