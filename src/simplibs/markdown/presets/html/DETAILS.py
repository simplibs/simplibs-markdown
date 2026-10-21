# Outers
from ...base_class import Markdown
from ...blocks import Html


def DETAILS(summary: str | Markdown, *body: str | Markdown, expanded: bool = False) -> Html:
    """Build a collapsible section.

    Init Params:
        summary (str | Markdown): The line that stays visible and opens the section.
        *body (str | Markdown): The hidden content: strings, nodes or lists of them.
        expanded (bool): `True` shows the section open from the start (the `open`
            attribute).

    Markdown:
        A `<details>` block with a `<summary>` and the body.

    Example:
        DETAILS("Show more", "Hidden text.")
        # Writes:
        # <details>
        #
        # <summary>Show more</summary>
        #
        # Hidden text.
        #
        # </details>

        DETAILS("Show more", "Hidden text.", expanded=True)
        # Writes:
        # <details open>
        #
        # <summary>Show more</summary>
        #
        # Hidden text.
        #
        # </details>

    Note:
        Blank lines are written around the body, so that Markdown inside it (lists, code) is
        read as Markdown and not as HTML.
    """
    head = Html("summary", summary)
    return Html("details", [head, *body], attrs={"open": True} if expanded else None)
