from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_quote_unknown_alert_error(
    alert: Any,
) -> NoReturn:
    """Raise ParamError when the alert of a quote is not an `AlertKind`.

    Args:
        alert: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="MARKDOWN_QUOTE_UNKNOWN_ALERT",
        label="quote alert",
        value=alert,
        problem="Only the five alert kinds of GitHub are known.",
        expected="An AlertKind member: NOTE, TIP, IMPORTANT, WARNING or CAUTION.",
        how_to_fix=(
            "Pass one of the `AlertKind` members.",
            "Leave `alert` out for a plain quote.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_quote_unknown_alert_error — An Alert Nobody Renders

## Purpose
`> [!INFO]` is not an alert. Renderers show it as an ordinary quote with a
strange first line, and the mistake stays in the output.
"""
