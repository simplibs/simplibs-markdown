from .raise_quote_unknown_alert_error import raise_quote_unknown_alert_error


_DESIGN_NOTES = """
# Quote Validations Sub-Package

## Purpose
Diagnostic raisers for the `Quote` node.

## Internal Components Registry

| Component                       | Type     | Description                                          |
| :------------------------------ | :------- | :--------------------------------------------------- |
| `raise_quote_unknown_alert_error`| Function | Raises `ParamError` when the alert is not an `AlertKind`. |
"""
