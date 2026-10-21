from enum import Enum


class AlertKind(Enum):
    """The kind of a GitHub alert. The value is the text written in `[!...]`."""

    NOTE = "NOTE"
    TIP = "TIP"
    IMPORTANT = "IMPORTANT"
    WARNING = "WARNING"
    CAUTION = "CAUTION"


_DESIGN_NOTES = """
# AlertKind — The Five Alerts of GitHub

## Purpose
An alert is a quote whose first line is `[!NOTE]` and so on. `.value` is the
word written between the brackets, in capitals as GitHub requires.

## Limit
Other renderers show an alert as an ordinary quote with that first line.
"""
