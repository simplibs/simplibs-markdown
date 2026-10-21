# Outers
from ...inline import Link
from ...inline.enums import LinkKind


def AUTOLINK(url: str) -> Link:
    """Build a link that shows its own address.

    Init Params:
        url (str): The address, written between angle brackets.

    Markdown:
        The address between angle brackets (`<url>`).

    Example:
        AUTOLINK("https://example.com")
        # Writes: "<https://example.com>"

    Note:
        Works in every Markdown renderer, because the brackets say that it is a link.
        `BARE_URL` is the shorter form.
    """
    return Link(dest=url, kind=LinkKind.AUTOLINK)
